#!/bin/sh
for dir in ./*
do
   if [ -f "$dir/beet.yaml" ]
   then
      printf '%s\n' "$dir"
      (cd "$dir" && uv run -m beet)
   fi
done
