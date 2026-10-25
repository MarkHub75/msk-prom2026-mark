#!/bin/sh
# frames1fps.sh VIDEO NAME : run from review/; one exact frame at k+0.5 s (k=0..29) with a time label, plus 5x2 sheets
V=$1; O=$2; mkdir -p $O; rm -f $O/*.jpg
for k in $(seq 0 29); do t=$k.5; n=$(printf %02d $k)
  /c/ffmpeg/bin/ffmpeg -v error -y -ss $t -i $V -frames:v 1 -q:v 2 -vf "drawtext=fontfile=arial.ttf:text='$t s':x=12:y=12:fontsize=40:fontcolor=yellow:box=1:boxcolor=black@0.6" $O/t$n.jpg
done
for s in 0 1 2; do /c/ffmpeg/bin/ffmpeg -v error -y -start_number $((s*10)) -i $O/t%02d.jpg -frames:v 10 -vf "scale=768:-2,tile=5x2" $O-sheet$s.jpg; done
