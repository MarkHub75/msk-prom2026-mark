#!/bin/sh
# Fresh promo world: argus-real pack, no broadcasts, no events of the pack yet.
cd /c/Users/User/Documents/argus-promo
PID=$(netstat -ano | grep '127.0.0.1:8030 ' | grep LISTEN | awk '{print $5}' | head -1)
[ -n "$PID" ] && taskkill //PID $PID //T //F >/dev/null 2>&1
sleep 2
rm -rf data/app-promo
(env -u SAFEWATCH_FAKE PYTHONUNBUFFERED=1 /c/Users/User/AppData/Roaming/Python/Python312/Scripts/uv.exe run safewatch serve --seed > ../argus-promo-serve.log 2>&1 &)
for i in $(seq 1 40); do curl -s 127.0.0.1:8030/api/health >/dev/null && break; sleep 1; done
sleep 4
curl -s 127.0.0.1:8030/api/system | head -c 120; echo
