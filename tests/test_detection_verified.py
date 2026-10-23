"""Operational manifest evidence checks; no broker/network calls."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4
import numpy as np
from ml.detection.verified_manifest import prepare_verified_manifest


def put(path,value):
    path.write_text(json.dumps(value))


def fixture(root,name="helmet"):
    model=name+"-v1";decoder="detect_v8" if name=="helmet" else "split_pose_v8"
    source=root/"detection"/name;compiler=root/"linq-sdk"/(name+"-compile");capture=root/"linq-rpc"/(name+"-001");stage=root/"linq-rpc"/name
    for d in (source,compiler,capture,stage):d.mkdir(parents=True)
    (source/"weights.onnx").write_bytes(b"trusted-source-graph-fixture")
    (compiler/"model.tpu").write_bytes(b"compiled-test-fixture-not-real-hardware")
    h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    manifest={"model_id":model,"decoder":decoder,"classes":["helmet","bare_head"] if name=="helmet" else ["person"],
              "input":{"name":"images","shape":[1,3,8,8],"dtype":"float32","layout":"NCHW","scale":1/255},
              "source":"https://example.invalid/no-uri-in-new-manifest","artifacts":{"onnx":{"file":"weights.onnx","sha256":h(source/"weights.onnx")}}}
    if name=="helmet":
        manifest["output_name"]="output0";output={"output0":np.array([[[4],[4],[2],[2],[.9],[.1]]],np.float32)}
    else:
        names={"boxes":"b","class_scores":"s","keypoint_xy":"xy","keypoint_scores":"p"};manifest["split_outputs"]=names
        output={"b":np.array([[[4],[4],[2],[2]]],np.float32),"s":np.full((1,1,1),.9,np.float32),"xy":np.full((1,17,2,1),4,np.float32),"p":np.full((1,17,1,1),.8,np.float32)}
        manifest["output_shapes"]={key:list(v.shape) for key,v in output.items()}
    put(source/"manifest.json",manifest)
    inp={"images":np.zeros((1,3,8,8),np.float32)}
    specs=lambda arrays:[{"name":key,"shape":list(v.shape),"dtype":v.dtype.name} for key,v in arrays.items()]
    ph=h(compiler/"model.tpu")
    put(compiler/"compile-report.json",{"model_id":model,"compile_status":"PASS","stages":{"compile":{"status":"PASS"}},"program_sha256":ph,"source_onnx_sha256":manifest["artifacts"]["onnx"]["sha256"],"inputs":specs(inp),"outputs":specs(output)})
    request=str(uuid4());c={"schema_version":"1.0","capture_id":str(uuid4()),"model_id":model,"journal_request_id":request,"status":"completed","call_started":True,"call_completed":True,"program":{"sha256":ph},"artifacts":{}}
    for kind,arrays in [("inputs",inp),("outputs",output)]:
        np.savez(capture/(kind+".npz"),**arrays)
        c["artifacts"][kind]={"file":kind+".npz","sha256":h(capture/(kind+".npz"))}
        c[kind]={key:{"shape":list(v.shape),"dtype":v.dtype.name,"nbytes":v.nbytes,"sha256":hashlib.sha256(v.tobytes()).hexdigest()} for key,v in arrays.items()}
    put(capture/"capture.json",c)
    put(capture/"response.json",{"status":"completed","status_code":0,"request_id":request,"response_id":request,"journal_request_id":request,"remote_completion":"response_received","outputs":{s["name"]:{"shape":s["shape"],"dtype":s["dtype"]} for s in specs(output)}})
    put(stage/"staging-receipt.json",{"status":"STAGED","model_id":model,"program_name":name+"-v1.tpu","program_sha256":ph,"bytes":(compiler/"model.tpu").stat().st_size,"remote_completion":"response_received"})
    return source,compiler,capture,stage


class VerifiedManifestTests(unittest.TestCase):
    def test_derives_identity_runtime_abi_without_modifying_source(self):
        for name in ("helmet","pose-split"):
            with self.subTest(name=name),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);source,_,_,_=fixture(root,name);before=(source/"manifest.json").read_bytes()
                m=prepare_verified_manifest(name,root)
                self.assertTrue(m["linq"]["runtime_abi_verified"])
                self.assertEqual(m["linq"]["program_name"],name+"-v1.tpu")
                self.assertEqual(m["linq"]["input_map"],{"images":"images"})
                self.assertEqual(set(m["linq"]["output_map"]),{v["name"] for v in m["linq"]["outputs"]})
                self.assertNotIn("source",m)
                self.assertFalse(m["linq"]["independent_hardware_attestation"])
                self.assertEqual((source/"manifest.json").read_bytes(),before)

    def test_rejects_failed_or_uncorrelated_response(self):
        for key,value in [("status_code",1),("status_code",False),("response_id",str(uuid4())),("status","failed")]:
            with self.subTest(key=key,value=value),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);_,_,capture,_=fixture(root)
                p=capture/"response.json";d=json.loads(p.read_text());d[key]=value;put(p,d)
                with self.assertRaises(ValueError):prepare_verified_manifest("helmet",root)

    def test_rejects_source_abi_or_onnx_mismatch(self):
        for change in ("input","decoder","onnx"):
            with self.subTest(change=change),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);source,_,_,_=fixture(root)
                p=source/"manifest.json";d=json.loads(p.read_text())
                if change=="input":d["input"]["shape"]=[1,3,16,16]
                elif change=="decoder":d["decoder"]="pose_v8"
                else:(source/"weights.onnx").write_bytes(b"modified graph")
                put(p,d)
                with self.assertRaises(ValueError):prepare_verified_manifest("helmet",root)

    def test_rejects_receipt_and_capture_integrity_mismatch(self):
        for change in ("receipt","capture","program","output"):
            with self.subTest(change=change),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);_,compiler,capture,stage=fixture(root)
                if change=="receipt":
                    p=stage/"staging-receipt.json";d=json.loads(p.read_text());d["program_sha256"]="0"*64;put(p,d)
                elif change=="capture":(capture/"outputs.npz").write_bytes(b"bad NPZ")
                elif change=="program":(compiler/"model.tpu").write_bytes(b"changed program")
                else:
                    p=capture/"response.json";d=json.loads(p.read_text());d["outputs"]["output0"]["shape"]=[1,7,1];put(p,d)
                with self.assertRaises(ValueError):prepare_verified_manifest("helmet",root)

    @unittest.skipUnless(Path('/workspace/artifacts/linq-rpc/pose-split-001/capture.json').is_file(),"real local captures unavailable")
    def test_existing_actual_captures_validate_and_decode(self):
        for name in ("helmet","pose-split"):
            with self.subTest(name=name):
                m=prepare_verified_manifest(name)
                self.assertTrue(m["linq"]["runtime_abi_verified"])
                self.assertEqual(m["linq"]["target_video_quality"],"NOT_EVALUATED")


if __name__=="__main__":unittest.main()
