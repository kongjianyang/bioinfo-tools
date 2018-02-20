#!/bin/bash

ORIGFILE="$1"

awk '/^>/{printf("\n%s\t",$0);next;}{printf("%s",$0);}END{printf("\n");}' "$ORIGFILE" | awk '{print $1"\n"$2}'
