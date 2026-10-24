"""Cleanup preserves selected bytes and resolves only explicit archived sources."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from production import audio_visual_plan as av
from production import selected_scene_review as selected
from production import serve_scene_review as server


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data))


class RetainedSourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name).resolve()
        self.logical='character/characters/lion_and_mouse_v7/Milo/poses/old.png'
        self.prefix='stories/lion_and_mouse_v7/history/retained_sources'
        self.archived=self.prefix+'/files/'+self.logical
        p=self.root/self.archived;p.parent.mkdir(parents=True);p.write_bytes(b'original source bytes')
        self.path=p
        self.index=self.root/self.prefix/'INDEX.json'
        write(self.index,{'schema':'feltwillow.retained-sources.v1','files':{self.logical:{'archived_path':self.archived,'sha256':sha(p)}}})

    def tearDown(self):
        self.tmp.cleanup()

    def test_archived_provenance_is_readable_but_write_path_stays_original(self):
        self.assertEqual(av.source_file(self.root,self.logical),self.path)
        self.assertEqual(av.local(self.root,self.logical),self.root/self.logical)
        self.assertFalse(av.local(self.root,self.logical).exists())
        self.path.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'missing or changed'):
            av.source_file(self.root,self.logical)

    def test_archive_mapping_cannot_escape_archive_or_repository(self):
        data=json.loads(self.index.read_text())
        for bad in ['other/location.png',self.prefix+'/files/../../../../../../outside.png']:
            data['files'][self.logical]['archived_path']=bad;write(self.index,data)
            with self.assertRaises(ValueError):av.source_file(self.root,self.logical)

    def test_review_server_keeps_original_url_and_explicit_asset_allowlist(self):
        gallery=self.root/'review/index.html';gallery.parent.mkdir()
        gallery.write_text('<img src="../'+self.logical+'">')
        assets=server.gallery_assets(self.root,Path('review/index.html'))
        self.assertEqual(assets['/'+self.logical],self.path)
        self.assertNotIn('/'+self.archived,assets)
        self.assertEqual(len(assets),2)


class SelectionTests(unittest.TestCase):
    def test_selected_images_require_live_bytes_not_an_archived_substitute(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'stories/lion_and_mouse_v7'
            image=root/'selected.png';Image.new('RGB',(3,2),'red').save(image)
            audio=root/'line.wav';audio.write_bytes(b'fixed WAV bytes')
            meta=root/'line.json';meta.write_text('{}')
            facts={'wav':'line.wav','sha256':sha(audio),'metadata':'line.json','metadata_sha256':sha(meta),'metadata_text':'and'}
            side=root/'selected.json';write(side,{'image_id':'S05-L005-B01-I01','sha256':sha(image)})
            row={'image_id':'S05-L005-B01-I01','path':'selected.png','sha256':sha(image),'sidecar':{'path':'selected.json','sha256':sha(side)},'line_id':'S05-L005','dimensions':[3,2],'audio':facts}
            write(folder/selected.LEDGER,{'decision':'owner_selected_scene_images','reviewer':'project_owner','images':[row],'count':1,'counts_by_scene':{'S05':1}})
            write(folder/'selected_images/IMAGE_REUSE.json',{'reuse_of':row['image_id'],'path':row['path'],'sha256':row['sha256'],'audio':facts})
            self.assertEqual(selected.verify(root,'lion_and_mouse_v7')[1]['count'],1)
            image.unlink()
            with self.assertRaisesRegex(ValueError,'Selected bytes changed'):
                selected.verify(root,'lion_and_mouse_v7')

    def test_duplicate_selected_paths_do_not_double_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'stories/lion_and_mouse_v7'
            image=root/'selected.png';Image.new('RGB',(3,2),'red').save(image)
            audio=root/'line.wav';audio.write_bytes(b'wav');meta=root/'line.json';meta.write_text('{}')
            side=root/'selected.json';write(side,{'image_id':'S05-L005-B01-I01','sha256':sha(image)})
            row={'image_id':'S05-L005-B01-I01','path':'selected.png','sha256':sha(image),'sidecar':{'path':'selected.json','sha256':sha(side)},'line_id':'S05-L005','dimensions':[3,2],'audio':{'wav':'line.wav','sha256':sha(audio),'metadata':'line.json','metadata_sha256':sha(meta)}}
            write(folder/selected.LEDGER,{'decision':'owner_selected_scene_images','reviewer':'project_owner','images':[row,row],'count':2,'counts_by_scene':{'S05':2}})
            with self.assertRaisesRegex(ValueError,'Duplicate'):
                selected.verify(root,'lion_and_mouse_v7')


if __name__=='__main__':unittest.main()
