import pathlib,json,requests,hashlib,subprocess,imageio_ffmpeg,concurrent.futures
p=pathlib.Path('_WORK/MATERIALS/W2-10');a=json.loads((p/'MANIFEST.json').read_text());fs=[]
for x in a:
 if x['folder']['name'] in ['0_safe_walkway_violation','4_safe_walkway']:
  sortedfiles=sorted(x['files'],key=lambda f:f['size']);fs.extend([sortedfiles[0],sortedfiles[-1]])
print([(f['filename'],f['size']) for f in fs]);ff=imageio_ffmpeg.get_ffmpeg_exe();out=[]
for f in fs:
 dest=p/f['filename'];r=requests.get(f['content_details']['download_url'],timeout=60);dest.write_bytes(r.content)
 assert hashlib.sha256(r.content).hexdigest()==f['content_details']['sha256_hash']
 v=subprocess.run([ff,'-hide_banner','-i',str(dest)],capture_output=True,text=True);(p/(f['filename']+'.ffmpeg.txt')).write_text(v.stderr,encoding='utf8')
 subprocess.run([ff,'-hide_banner','-loglevel','error','-i',str(dest),'-vf','fps=1/3,scale=640:-1','-frames:v','7',str(p/(f['filename']+'-%02d.jpg'))],capture_output=True)
 out.append({'filename':f['filename'],'id':f['id'],'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest(),'probe':v.stderr})
(p/'SAMPLE_OBSERVATIONS.json').write_text(json.dumps(out,indent=2),encoding='utf8');print('downloaded',len(out))
