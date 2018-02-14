#!/bin/sh
#PBS -N unzip.job
#PBS -l nodes=1:ppn=20
#PBS -l walltime=03:00:00
#PBS -q li2627
#PBS -o /scratch/halstead/t/tang389/WholeRNAseq_NutriNet/02RNAseqData/output
#PBS -e /scratch/halstead/t/tang389/WholeRNAseq_NutriNet/02RNAseqData/output

date

echo "unzip bz2.file"

cd /scratch/halstead/t/tang389/WholeRNAseq_NutriNet/02RNAseqData

bzip2 -d *.bz2

echo "finished"

date
