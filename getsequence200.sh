#!/bin/bash

#function to get protein sequence > 200

# reference http://www.cnblogs.com/chengmo/archive/2010/10/13/1850145.html

ORIGFILE="$1"

awk '/^>/{printf("\n%s\t",$0);next;}{printf("%s",$0);}END{printf("\n");}' "$ORIGFILE" | awk '{if (length($2)>200) print $1, "length:", length($2), "\n" $2}'
