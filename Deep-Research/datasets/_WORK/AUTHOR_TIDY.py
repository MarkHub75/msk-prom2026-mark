from pathlib import Path
import re

p = Path(__file__).with_name('HUMAN_DRAFT.md')
text = p.read_text(encoding='utf-8')
protected = []
pattern = r'```[\s\S]*?```|`[^`\n]*`|\]\([^\n]*?\)|https?://[^\s)]+'
def hide(m):
    protected.append(m.group())
    return f'\x00{len(protected)-1}\x00'
text = re.sub(pattern, hide, text)
text = re.sub(r'([А-Яа-яЁё])(?=\d)', r'\1 ', text)
text = re.sub(r'(\d)(?=[А-Яа-яЁё])', r'\1 ', text)
words = 'trainval|train|val|test|TXTval|COCO|Kaggle|version|id|union|letterbox|SPIE|Table|CSV|ZIP|JPEG|failures|stems|ID|mask|foot|sample|sizes|Mendeley|Archive|recount|Sensors|Approach|class|counts|actual|published|web|membership|intersections|labels|revision|publication|modified|Core|supplementary|Unlabeled|external|advertised|inventory|displayed|start|tbn|fps|FPS|Terms|Goggles|Mask|image|excerpt|split|objects'
text = re.sub(r'(?<![\w])('+words+r')(?=\d)', r'\1 ', text)
text = re.sub(r'(\d)(?=(?:GB\b|FPS\b|px\b|frames\b|s\b|h\b|m\b|HOI\b|actions\b|input\b|NV-))', r'\1 ', text)
text = re.sub(r'—(?=\d)', '— ', text)
subs = {
    'TableII':'Table II', 'Table3':'Table 3', 'TableII':'Table II',
    'CC BY4.0':'CC BY 4.0', 'CC BY-NC4.0':'CC BY-NC 4.0',
    'CC BY-NC3.0':'CC BY-NC 3.0', 'CC BY-NC-SA4.0':'CC BY-NC-SA 4.0',
    'Apache2.0':'Apache 2.0', 'Kagglev1':'Kaggle v1', 'Mendeleyv1':'Mendeley v1',
    'releasev0.1.0':'release v0.1.0', 'tagv0.0.0':'tag v0.0.0',
    'PhysicalAI-Event-Videosv1.0':'PhysicalAI-Event-Videos v1.0',
    'Zenodo12659325v1':'Zenodo 12659325 v1', 'Zenodo19926448v1':'Zenodo 19926448 v1',
    'BY4.0':'BY 4.0', 'H.2641920':'H.264 1920', 'H.264480':'H.264 480',
    'UNVIPC2122CR3-PF40-A':'UNV IPC2122 CR3-PF40-A',
    'cardCC':'card CC', 'CardCC':'Card CC', 'articleCC':'article CC', 'ArticleCC':'Article CC',
    'Brief110791':'Brief 110791', 'classifierW/':'classifier W/',
    'chunksNV-':'chunks NV-', 'et al.2022':'et al. 2022',
    'Duan et al.2022':'Duan et al. 2022', 'AliyunOSS':'Aliyun OSS',
    'Head30':'Head 30', 'head30':'head 30', 'nativebox':'native box',
    'inputpixels':'input pixels', 'rows:SFCHD':'rows: SFCHD',
    'VOCwidth':'VOC width', 'fileSHA256':'file SHA256',
    'decoded-pixelSHA256':'decoded-pixel SHA256', 'frozenGT':'frozen GT',
    'SFCHD50,552':'SFCHD 50,552', 'SFCHD50,559':'SFCHD 50,559',
    'SH17sample228':'SH17 sample 228', 'SH17raw-release-members76,007':'SH17 raw release-members 76,007',
    'SH17raw76,008':'SH17 raw 76,008', 'CPPEtest207':'CPPE test 207',
    'SH17release/raw':'SH17 release/raw', 'SFCHDintersection':'SFCHD intersection',
    'SHELXML':'SHEL XML', 'CPPEannotations':'CPPE annotations',
    'Smokerdecode':'Smoker decode', 'Önalmanifest':'Önal manifest',
    'SARDraw':'SARD raw', 'PhysicalAIfamily':'PhysicalAI family',
    'SHWDhat/person':'SHWD hat/person', 'SHEL5Khead_with_helmet/head':'SHEL5K head_with_helmet/head',
    'SHELperson':'SHEL person', 'headID':'head ID',
    'SFCHDfactory':'SFCHD factory', 'SH17broad':'SH17 broad',
    'SHELhead/person-state':'SHEL head/person-state', 'CPPEbroad':'CPPE broad',
    'SFCHDval':'SFCHD val', 'tinytest':'tiny test', 'Önalcurated':'Önal curated',
    'Önal1080p':'Önal 1080p', '640input':'640 input', 'LinQthroughput':'LinQ throughput',
    'sourceGT':'source GT', 'targetIDs':'target IDs', 'targetID':'target ID',
    'SFCHDprefix/run':'SFCHD prefix/run', 'Önalviews':'Önal views',
    'SHELextraperson':'SHEL extra person', 'SHELextra':'SHEL extra',
    'SH17off/on':'SH17 off/on', 'SHWDheads':'SHWD heads', 'CPPEsubtypes':'CPPE subtypes',
    'PictorApproach':'Pictor Approach', 'Constructionno_':'Construction no_',
    'CPPE15':'CPPE 15', 'CHVbare-head':'CHV bare-head', 'SH17conditions':'SH17 conditions',
    'SCUTresearch-only':'SCUT research-only', 'CPPE-HF':'CPPE-HF',
    'originalCPPE':'original CPPE', 'PhysicalAIchunks':'PhysicalAI chunks',
    'internalAGPL':'internal AGPL', 'фото2024':'фото 2024',
    'SHELmulti-geometry':'SHEL multi-geometry', 'SHWDhead':'SHWD head',
    'Constructionpart-local':'Construction part-local', 'SmokerRGB':'Smoker RGB',
    'CPPE1-based':'CPPE 1-based', 'HF0-based':'HF 0-based',
    'input640':'input 640', 'SFCHDnotice':'SFCHD notice',
}
for a,b in subs.items():
    text = text.replace(a,b)
text = re.sub(r'\x00(\d+)\x00', lambda m: protected[int(m[1])], text)
text = text.replace('`image1120.jpg`', '`image 1120.jpg`')
text = text.replace('`foot`6', '`foot` (ID 6)')
text = re.sub(r'`([^`\n]+)`', lambda m: '`' + m[1].strip() + '`', text)
p.write_text(text, encoding='utf-8')
print(f'{len(text):,} characters; {len(text.split()):,} whitespace-delimited words')
