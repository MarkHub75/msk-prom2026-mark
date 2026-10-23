import sys,re,html
t=sys.stdin.read()
t=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',t)
t=re.sub(r'(?s)<[^>]+>','\n',t)
t=html.unescape(t)
lines=[l.strip() for l in t.splitlines()]
out=[];prev=None
for l in lines:
    if l and l!=prev: out.append(l)
    prev=l
print('\n'.join(out))
