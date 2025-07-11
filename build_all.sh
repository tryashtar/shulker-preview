#!/bin/sh
for dir in ./*
do
   if [ -f "$dir/beet.yaml" ]
   then
      printf '%s\n' "$dir"
      uv run -m beet --project "$dir"
   fi
done
