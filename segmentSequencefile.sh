#!/bin/bash

module load bioinfo
module load blast/2.7.1+

awk 'NR%10000==1{FILE="Subset"++i;}{print >FILE}' $1
SETS=$(ls Subset* | wc -l)

#echo "Found $SETS subsets"
makeblastdb -dbtype 'prot' -in $1 -out ProtFam -title ProtFam -parse_seqids

for ((i=1; i<=$SETS; i++));
do
        echo "Processing Set $i"
done
