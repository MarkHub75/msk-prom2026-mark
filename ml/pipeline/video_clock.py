"""Encoded presentation clock for file evidence, independent of OpenCV offsets."""
import json
import math
import subprocess


class FilePTS:
    def __init__(self,path):
        raw=subprocess.run(['ffprobe','-v','error','-threads','1','-select_streams','v:0',
            '-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(path)],
            capture_output=True,timeout=60,check=False)
        if raw.returncode:raise ValueError('encoded frame clock unavailable')
        records=json.loads(raw.stdout).get('frames',[])
        self.times=[float(f['best_effort_timestamp_time'])*1000 for f in records]
        if not self.times or any(not math.isfinite(t) or t<0 for t in self.times) or any(b<=a for a,b in zip(self.times,self.times[1:])):
            raise ValueError('encoded presentation clock must be finite and strictly advancing')

    def at(self,index):
        if type(index) is not int or not 0<=index<len(self.times):raise ValueError('decoded frame index outside encoded clock')
        return self.times[index]
