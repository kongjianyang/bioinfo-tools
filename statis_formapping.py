#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 09:16:50 2018

@author: liangtang
"""
import os
import os.path
from os import listdir

os.chdir('/Volumes/scratch/WholeRNAseq_NutriNet/04Mapping/output')

filepath = '/Volumes/scratch/WholeRNAseq_NutriNet/04Mapping/output'

filename_list=listdir(filepath)

h=[]

for filename in filename_list:
        if filename[-3:]=='err':
                h.append(filename)
print h

myfile=open('statis_formapping.txt','w')

for i in h:
    with open(i, 'r') as f:
        lines = f.readlines()
        a = i, lines[4], lines[5], lines[6], lines[7], lines[8], lines[9]
        myfile.write(str(a) + '\n')
        
myfile.close()
        
