#!/bin/sh
# finalize.sh RAW.mp4 OUT.mp4 POSTER_T POSTER.jpg
# two-pass loudnorm to −18 LUFS / −1.5 dBTP (quiet bed under live speech), poster frame baked in as frame 0
F=/c/ffmpeg/bin/ffmpeg; RAW=$1; OUT=$2; T=$3; P=$4; TMP=${OUT%.mp4}.tmp.mp4
J=$($F -hide_banner -nostats -i $RAW -af loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$J" | grep "\"$1\"" | sed 's/.*: *"\(.*\)".*/\1/'; }
$F -v error -y -i $RAW -t 30 -c:v copy -af "loudnorm=I=-18:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,atrim=0:30,asetpts=N/SR/TB" -ar 48000 -c:a aac -b:a 192k $TMP
$F -v error -y -ss $T -i $TMP -frames:v 1 -q:v 2 $P
$F -v error -y -i $TMP -i $P -filter_complex "[0:v][1:v]overlay=0:0:enable='eq(n,0)'[v]" -map "[v]" -map 0:a -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -c:a copy -t 30 -movflags +faststart $OUT
rm -f $TMP
/c/ffmpeg/bin/ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,duration -of compact $OUT
$F -hide_banner -nostats -i $OUT -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|Peak" | tr -s ' ' | tr '\n' ' '; echo
