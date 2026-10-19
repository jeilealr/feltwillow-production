import json
import math
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from scene_match import compare, landmark_metrics, sha256, SCHEMA, COORDS
try:
    from PIL import Image, ImageCms
except ImportError:
    Image = None


class LandmarkTests(unittest.TestCase):
    def data(self):
        return {'schema': SCHEMA, 'coordinate_system': COORDS,
                'reference_sha256': 'a'*64, 'render_sha256': 'b'*64,
                'points': [{'id': 'root', 'reference_xy':[0.1,0.2], 'render_xy':[0.2,0.3]}]}

    def run_metrics(self, data):
        return landmark_metrics(data,'a'*64,'b'*64,(101,101))

    def test_distances_are_supplied_point_measurements(self):
        result=self.run_metrics(self.data())
        self.assertAlmostEqual(result['mean_distance_pixels'], math.sqrt(200))
        self.assertEqual(result['points'][0]['status'],'measured_not_approved')

    def test_unmeasured_remains_unmeasured(self):
        d=self.data();d['points'][0]['render_xy']=None
        r=self.run_metrics(d)
        self.assertEqual(r['unmeasured_count'],1);self.assertIsNone(r['mean_distance_pixels'])

    def test_stale_hash_rejected(self):
        d=self.data(); d['reference_sha256']='c'*64
        with self.assertRaisesRegex(ValueError,'stale'): self.run_metrics(d)

    def test_duplicate_ids_rejected(self):
        d=self.data();d['points']*=2
        with self.assertRaisesRegex(ValueError,'duplicate'):self.run_metrics(d)

    def test_invalid_coordinates_rejected(self):
        for value in ([True,0], [1.01,0], [float('nan'),0], [0], '0,0'):
            with self.subTest(value=value):
                d=self.data();d['points'][0]['reference_xy']=value
                with self.assertRaises(ValueError):self.run_metrics(d)

    def test_wrong_coordinate_system_rejected(self):
        d=self.data();d['coordinate_system']='world_xyz'
        with self.assertRaises(ValueError):self.run_metrics(d)


@unittest.skipIf(Image is None,'Pillow unavailable')
class ImageMatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.a=self.root/'ref.png';self.b=self.root/'render.png';self.out=self.root/'new-review'
        Image.new('RGB',(100,60),(140,80,30)).save(self.a)
        Image.new('RGB',(100,60),(130,70,30)).save(self.b)

    def test_requires_color_assumption(self):
        with self.assertRaisesRegex(ValueError,'Untagged'):compare(self.a,self.b,self.out)
        self.assertFalse(self.out.exists())

    def test_comparison_preserves_sources(self):
        before=(sha256(self.a),sha256(self.b))
        r=compare(self.a,self.b,self.out,assume_srgb=True)
        self.assertEqual(r['visual_approval'],'not_assessed')
        self.assertEqual(r['mean_absolute_display_channel_error_0_255'],[10.0,10.0,0.0])
        self.assertFalse(r['resized_or_warped'])
        self.assertEqual(before,(sha256(self.a),sha256(self.b)))
        with Image.open(self.out/'overlay_50.png') as im:self.assertEqual(im.size,(100,60))

    def test_existing_output_refused(self):
        self.out.mkdir();(self.out/'keep.txt').write_text('keep')
        with self.assertRaises(ValueError):compare(self.a,self.b,self.out,assume_srgb=True)
        self.assertEqual((self.out/'keep.txt').read_text(),'keep')

    def test_dimensions_not_silently_resized(self):
        Image.new('RGB',(90,60)).save(self.b)
        with self.assertRaisesRegex(ValueError,'equal dimensions'):compare(self.a,self.b,self.out,assume_srgb=True)
        self.assertFalse(self.out.exists())

    def test_alpha_must_be_composited(self):
        Image.new('RGBA',(100,60),(50,50,50,0)).save(self.b)
        with self.assertRaisesRegex(ValueError,'transparent'):compare(self.a,self.b,self.out,assume_srgb=True)

    def test_bad_icc_profile_not_ignored(self):
        Image.new('RGB',(100,60)).save(self.b,icc_profile=b'bad profile')
        with self.assertRaisesRegex(ValueError,'profile'):compare(self.a,self.b,self.out,assume_srgb=True)

    def test_real_srgb_icc_profile(self):
        profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
        for p in [self.a,self.b]:Image.new('RGB',(100,60),(120,80,30)).save(p,icc_profile=profile)
        r=compare(self.a,self.b,self.out)
        self.assertEqual(r['mean_absolute_display_channel_error_0_255'],[0.,0.,0.])

    def test_16bit_rgb_png_refused(self):
        import struct, zlib
        def chunk(kind, data):
            return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
        raw=(b'\x00'+struct.pack('>HHH',30000,20000,10000)*100)*60
        self.b.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',100,60,16,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
        with self.assertRaisesRegex(ValueError,'8-bit'):compare(self.a,self.b,self.out,assume_srgb=True)
        self.assertFalse(self.out.exists())

    def test_stale_landmarks_create_no_output(self):
        p=self.root/'points.json'
        p.write_text(json.dumps({'schema':SCHEMA,'coordinate_system':COORDS,'points':[]}))
        with self.assertRaisesRegex(ValueError,'stale'):compare(self.a,self.b,self.out,p,True)
        self.assertFalse(self.out.exists())

    def test_annotated_points(self):
        p=self.root/'points.json'
        p.write_text(json.dumps({'schema':SCHEMA,'coordinate_system':COORDS,
          'reference_sha256':sha256(self.a),'render_sha256':sha256(self.b),
          'points':[{'id':'rock','reference_xy':[0.4,0.5],'render_xy':[0.45,0.5]}]}))
        r=compare(self.a,self.b,self.out,p,True)
        self.assertTrue((self.out/'landmarks.png').is_file())
        self.assertEqual(r['landmarks']['measured_count'],1)

    def test_duplicate_json_key_refused(self):
        p=self.root/'points.json';p.write_text('{"schema":"a", "schema":"b"}')
        with self.assertRaisesRegex(ValueError,'Duplicate'):compare(self.a,self.b,self.out,p,True)

    def test_no_auto_approval_for_identical_images(self):
        self.b.write_bytes(self.a.read_bytes())
        r=compare(self.a,self.b,self.out,assume_srgb=True)
        self.assertEqual(r['visual_approval'],'not_assessed')
        self.assertIsNone(r['landmarks'])

if __name__=='__main__':unittest.main()
