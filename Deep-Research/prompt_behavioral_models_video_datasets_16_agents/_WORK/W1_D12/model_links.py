import re,pathlib
p=pathlib.Path('_WORK/W1_D12')
s=(p/'meccano_readme.txt').read_text();print('\n'.join(re.findall(r'https?[^)\s<>]+',s)))
