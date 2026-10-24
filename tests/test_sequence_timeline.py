import tempfile,unittest
from pathlib import Path
from PIL import Image
from production.sequence_plan import digest
from production.sequence_timeline import compile_timeline,render_preview

class TimelineTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.image=self.root/'plate.png';Image.new('RGB',(32,32),'green').save(self.image)
    def row(self,id,start,end):
        return dict(id=id,kind='static_hold',source=dict(path=str(self.image),sha256=digest(self.image)),start_sample=start,end_sample=end)
    def test_C28_C40_C41_cumulative_frame_cells(self):
        rows=[self.row('forest',0,239040),self.row('pause',239040,249840),self.row('speech',249840,298800)]
        t=compile_timeline(rows,24000,298800)
        self.assertEqual(t['frame_cells'],199)
        self.assertEqual(sum(r['frame_cells'] for r in t['intervals']),199)
        self.assertEqual(t['intervals'][0]['frame_cells'],159)
        self.assertIn(t['intervals'][2]['frame_cells'],[32,33])
    def test_C28_gap_and_duplicate_rejected(self):
        with self.assertRaises(ValueError):compile_timeline([self.row('a',0,1000),self.row('b',1001,3000)],24000,3000)
        with self.assertRaises(ValueError):compile_timeline([self.row('a',0,1000),self.row('a',1000,3000)],24000,3000)
    def test_C48_unreviewed_join_or_retime_rejected(self):
        video=self.row('v',0,24000);video['kind']='video';video['source_mapping']={'frame_count':10}
        with self.assertRaisesRegex(ValueError,'whole-motion'):compile_timeline([video],24000,24000)
        video['whole_motion_review']={'status':'pass','reviewer':'fixture','source_sha256':digest(self.image)}
        with self.assertRaisesRegex(ValueError,'retime'):compile_timeline([video],24000,24000)
    def test_static_preview_is_encoded_and_pending(self):
        t=compile_timeline([self.row('plate',0,7500)],24000,7500)
        receipt=render_preview(t,self.root/'preview.mp4',32,32)
        self.assertEqual(receipt['frames'],5);self.assertEqual(receipt['visual_review'],'pending')
        from feltwillow.render_receipt import inspect_media
        self.assertEqual(inspect_media(Path(receipt['output']))[0],'passed')
