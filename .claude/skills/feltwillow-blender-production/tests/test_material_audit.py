from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from blender_material_audit import upstream_nodes, digest, label

class MaterialGraphTests(unittest.TestCase):
    def setUp(self):
        self.nodes=[{'id':'image','type':'ShaderNodeTexImage'}, {'id':'bump','type':'ShaderNodeBump'},
                    {'id':'shader','type':'ShaderNodeBsdfPrincipled'},
                    {'id':'output','type':'ShaderNodeOutputMaterial','active_output':True},
                    {'id':'unused','type':'ShaderNodeTexImage'}]
        self.links=[{'from':'image','to':'bump'},{'from':'bump','to':'shader'},{'from':'shader','to':'output'}]
    def test_connected_path(self):self.assertEqual(upstream_nodes(self.nodes,self.links), {'image','bump','shader','output'})
    def test_unconnected_not_present(self):self.assertNotIn('unused',upstream_nodes(self.nodes,self.links))
    def test_cycle_terminates(self):self.links.append({'from':'shader','to':'bump'});self.assertIn('image',upstream_nodes(self.nodes,self.links))
    def test_inactive_output(self):self.nodes[3]['active_output']=False;self.assertEqual(upstream_nodes(self.nodes,self.links),set())
    def test_missing_endpoints(self):self.links.append({'from':'missing','to':'output'});self.assertNotIn('missing',upstream_nodes(self.nodes,self.links))
    def test_empty(self):self.assertEqual(upstream_nodes([],[]),set())
    def test_group_not_falsely_resolved(self):
        n=[{'id':'group','type':'ShaderNodeGroup'},{'id':'output','type':'ShaderNodeOutputMaterial','active_output':True}]
        self.assertEqual(upstream_nodes(n,[{'from':'group','to':'output'}]),{'group','output'})
    def test_inputs_not_mutated(self):
        import copy
        a,b=copy.deepcopy(self.nodes),copy.deepcopy(self.links);upstream_nodes(self.nodes,self.links);self.assertEqual((a,b),(self.nodes,self.links))
    def test_hash_and_external_label(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'source';p.write_bytes(b'abc')
            self.assertEqual(digest(p),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
            self.assertEqual(label(p,Path(temp)),'source')
            self.assertEqual(label(p,Path(temp)/'other'),'[external]/source')

if __name__ == '__main__':unittest.main()
