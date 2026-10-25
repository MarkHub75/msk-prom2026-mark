#!/bin/sh
# sheet.sh OUT COLS W img...  -> contact sheet
OUT=$1; COLS=$2; W=$3; shift 3
args=""; n=0; filt=""
for f in "$@"; do args="$args -i $f"; filt="$filt[$n]scale=$W:-2,setsar=1[s$n];"; n=$((n+1)); done
lay=""; i=0; while [ $i -lt $n ]; do lay="$lay[s$i]"; i=$((i+1)); done
pos=""; i=0; while [ $i -lt $n ]; do c=$((i % COLS)); r=$((i / COLS)); x=""; y="";
  if [ $c -eq 0 ]; then x=0; else x=$(seq -s+ 0 $((c-1)) | sed 's/[0-9]\+/w0/g'); fi
  if [ $r -eq 0 ]; then y=0; else y=$(seq -s+ 0 $((r-1)) | sed 's/[0-9]\+/h0/g'); fi
  pos="$pos$x"_"$y|"; i=$((i+1)); done
/c/ffmpeg/bin/ffmpeg -v error -y $args -filter_complex "$filt${lay}xstack=inputs=$n:layout=${pos%|}:fill=black" -frames:v 1 -q:v 3 $OUT
