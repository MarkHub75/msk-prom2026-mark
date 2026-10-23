exec(open('_WORK/M08/fetch.py',encoding='utf-8-sig').read().split('a=list(')[0])
urls={
'ava_labels2':'https://research.google.com/ava/download/ava_action_list_v2.2_for_activitynet_2019.pbtxt',
'avadownloadscript':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v1.2.0/tools/data/ava/download_annotations.sh',
'loading':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v1.2.0/mmaction/datasets/transforms/loading.py',
'skeletondata':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v1.2.0/tools/data/skeleton/README.md',
'posecode':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v1.2.0/mmaction/datasets/transforms/pose_transforms.py',
'ntusite':'https://rose1.ntu.edu.sg/dataset/actionRecognition/',
'ntulabels':'https://raw.githubusercontent.com/open-mmlab/mmaction2/v1.2.0/tools/data/skeleton/label_map_ntu60.txt',
'onlinetsm':'https://raw.githubusercontent.com/mit-han-lab/temporal-shift-module/master/online_demo/README.md',
'videomaeoriginal':'https://raw.githubusercontent.com/MCG-NJU/VideoMAE/main/README.md',
'kineticsreadme':'https://s3.amazonaws.com/kinetics/400/readme.md',
'k400val':'https://s3.amazonaws.com/kinetics/400/annotations/val.csv',
}
a=list(concurrent.futures.ThreadPoolExecutor(8).map(lambda kv:get(*kv),urls.items()));(out/'access3.json').write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
