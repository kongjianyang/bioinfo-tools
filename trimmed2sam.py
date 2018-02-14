#!/usr/bin/python
# PBS cluster job submission in Python

from popen2 import popen2
import time
import os
import os.path
from os import listdir

filepath = '/scratch/halstead/t/tang389/WholeRNAseq_NutriNet/03Trimming'
filename_list=listdir(filepath)

h=[]

for filename in filename_list:
        if filename[-7:]=='trimmed':
                h.append(filename)
print h
# Loop over jobs
for i in h:

    # Open a pipe to the qsub command.
        output, input = popen2('qsub')

        job_name = "tri2sam.job.%s" % i[:4]
        walltime = "03:00:00"
        processors = "nodes=1:ppn=20"
        queue = "li2627"
        command = "bowtie2 -p 20 -x /scratch/halstead/t/tang389/WholeRNAseq_NutriNet/01GenomeData/B73_genome -U /scratch/halstead/t/tang389/WholeRNAseq_NutriNet/03Trimming/%s -S /scratch/halstead/t/tang389/WholeRNAseq_NutriNet/04Mapping/%s.sam" % (i, i)
        job_string = """#!/bin/bash
        #PBS -N %s
        #PBS -l walltime=%s
        #PBS -l %s
        #PBS -o /scratch/halstead/t/tang389/WholeRNAseq_NutriNet/04Mapping/output/%s.out
        #PBS -e /scratch/halstead/t/tang389/WholeRNAseq_NutriNet/04Mapping/output/%s.err
        #PBS -q %s
        date
        module load bioinfo
        module load bowtie2/2.3.2
        cd /scratch/halstead/t/tang389/WholeRNAseq_NutriNet/04Mapping
        %s
        date""" % (job_name, walltime, processors, job_name, job_name, queue, command)

    # Send job_string to qsub
        input.write(job_string)
        input.close()

    # Print job and the system response to the screen as it's submitted
        print output.read()
        time.sleep(3)
