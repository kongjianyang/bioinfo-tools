#!/bin/sh
#PBS -l nodes=1:ppn=20
#PBS -l walltime=03:00:00
#PBS -q li2627
#PBS -j oe
#PBS -l mem=16GB

date

echo "Running bowtie2 mapping"
module load bioinfo
module load bowtie2/2.3.2
cd /scratch/halstead/t/tang389/WholeRNAseq_NutriNet/01GenomeData
bowtie2-build -f Zea_mays.AGPv3.22.dna.genome.fa B73_genome

date
