#!/bin/bash
# runw.sh <preview|full> <outroot> name:action ...   (4 Blender processes in parallel; full writes <outroot>/<name>/)
BL="${BLENDER:-/c/Program Files/Blender Foundation/Blender 5.2/blender.exe}"; D="$(cd "$(dirname "$0")" && pwd -W 2>/dev/null || pwd)"
mode=$1; out=$2; shift 2; mkdir -p "$out/_logs"
printf "%s\n" "$@" | xargs -P 4 -I{} sh -c "x={}; n=\${x%%:*}; a=\${x##*:}; o=\"$out\"; [ $mode = full ] && o=\"$out/\$n\"; \"$BL\" -b --python \"$D/render_word.py\" -- \$n \$a $mode \"\$o\" > \"$out/_logs/\$n.log\" 2>&1; grep -E '^DONE|Error' \"$out/_logs/\$n.log\" | tail -2 | cut -c1-200"
