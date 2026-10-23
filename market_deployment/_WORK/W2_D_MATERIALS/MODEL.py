"""Reproduce the report's assumed scenarios. P and L deliberately remain unknown."""
import json,pathlib
factor=sum(1/1.1**t for t in range(1,4))
rows=[]
for name,h,q,hai,s,repair in [('conservative',60,0,40,144000,0),('base',120,.5,20,96000,0),('optimistic',160,1,10,72000,0),('unfit_cameras',120,.5,40,192000,180000),('base_q0',120,0,20,96000,0)]:
    annual=12*h*800*q
    o=s+12*hai*800+.3*8760*8
    initial=300000+repair
    net=annual-o
    rows.append(dict(name=name,H=h,q=q,H_ai=hai,S=s,O_A=o,G=annual,C_A=net,NPV_A_constant=net*factor-initial,NPV_A_unknown_term='-(P+L)',TCO_A3_constant=initial+3*o,NPV_N_constant=(net-29606.4)*factor-initial-1012000))
result=dict(all_numerical_costs_are_assumptions=True,known_price_LinQ=False,NPV_factor=factor,rows=rows)
path=pathlib.Path(__file__).with_name('MODEL_RESULTS.json')
path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
