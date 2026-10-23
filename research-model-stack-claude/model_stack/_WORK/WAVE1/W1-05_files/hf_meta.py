import sys,json,urllib.request
for rid in sys.argv[1:]:
    j=json.load(urllib.request.urlopen(f"https://huggingface.co/api/models/{rid}"))
    print("=====",rid,"sha",j['sha'],"lic",j.get('cardData',{}).get('license') if j.get('cardData') else None,"mod",j.get('lastModified'),"created",j.get('createdAt'))
    print(" tags",j.get('tags'))
    try:
        t=json.load(urllib.request.urlopen(f"https://huggingface.co/api/models/{rid}/tree/main?recursive=true"))
        for f in t:
            if f['type']=='file': print("  ",f['path'],f.get('size'),(f.get('lfs') or {}).get('oid'))
    except Exception as e: print("tree err",e)
