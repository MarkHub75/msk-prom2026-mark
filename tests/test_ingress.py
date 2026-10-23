import threading
import unittest
from ml.pipeline.ingress import LatestFrameSource

class IngressTest(unittest.TestCase):
    def test_bounded_source_keeps_latest_instead_of_backlog(self):
        done=threading.Event()
        class Capture:
            count=0
            def read(self):
                self.count+=1
                if self.count <=100:
                    return True, self.count
                done.set()
                return False,None
            def release(self): pass
        source=LatestFrameSource(Capture())
        self.assertTrue(done.wait(2))
        value=source.read()
        self.assertEqual(value[0],99)
        self.assertEqual(value[3],100)
        self.assertIsNone(source.read())
        source.close()
