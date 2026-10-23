from copy import deepcopy
import io,json
from pathlib import Path
import tempfile
import unittest
import zipfile
import numpy as np
from PIL import Image
from ml.quality.helmet.repair import apply_reviews
from ml.quality.helmet.curate import curate


class HelmetDataTests(unittest.TestCase):
    def test_review_preserves_source_and_rejects_outside_box(self):
        original={'dataset_digest':'old','images':[{'image_id':'a','width':100,'height':100,'annotations':[{'class_name':'bare_head','bbox_xyxy':[10,10,20,20]}],'class_coverage':{'bare_head':'partial'}}]}
        p={'a':{'reviewer':'AI-agent','reason':'blind full-head review','annotations':[{'class_name':'bare_head','bbox_xyxy':[8,5,23,25]}],'ignore_regions':[],'class_coverage':{'bare_head':'complete'}}}
        result=apply_reviews(original,p)
        self.assertEqual(result['images'][0]['source_annotations'],original['images'][0]['annotations'])
        self.assertEqual(original['dataset_digest'],'old')
        self.assertEqual(result['parent_dataset_digest'],'old')
        bad=deepcopy(p);bad['a']['annotations'][0]['bbox_xyxy']=[-1,0,5,5]
        with self.assertRaises(ValueError):apply_reviews(original,bad)
        with self.assertRaises(ValueError):apply_reviews(original,{'unknown':p['a']})

    def test_exact_cluster_crossing_official_test_never_selected_for_val(self):
        rng=np.random.default_rng(123);data=[]
        for _ in range(2):
            im=Image.fromarray(rng.integers(0,256,(32,32,3),dtype=np.uint8));out=io.BytesIO();im.save(out,format='PNG');data.append(out.getvalue())
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);archive=root/'source.zip'
            with zipfile.ZipFile(archive,'w') as z:
                for split,name,blob in [('train','parent',data[0]),('val','alias',data[0]),('test','testalias',data[0]),('val','independent',data[1])]:
                    z.writestr(f'images/{split}/{name}.png',blob);z.writestr(f'labels/{split}/{name}.txt','0 .5 .5 .5 .5\n')
            report=curate(archive,root/'extracted',root/'artifacts',count=2)
            dataset=json.loads((root/'artifacts/development-dataset.json').read_text())
            self.assertEqual(report['cross_split_components'],1)
            self.assertEqual([i['image_id'] for i in dataset['images']],['construction:val:independent.png'])

    def test_unsafe_archive_path_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);archive=root/'source.zip'
            with zipfile.ZipFile(archive,'w') as z:z.writestr('../outside.txt','bad')
            with self.assertRaises(ValueError):curate(archive,root/'extracted',root/'artifacts')
            self.assertFalse((root/'outside.txt').exists())


if __name__=='__main__':unittest.main()
