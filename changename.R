#!/usr/bin/env Rscript
names = read.table("/scratch/halstead/t/tang389/WholeRNAseq_NutriNet/02RNAseqData/RNAlibraryNames.csv", sep = ",", header = T, stringsAsFactor=F)
existingFile = list.files("/scratch/halstead/t/tang389/WholeRNAseq_NutriNet/02RNAseqData",pattern="*.fastq")
names = names[names$fastq_name %in% existingFile,]
for (i in 1:nrow(names)){
  file.rename(from=file.path("/scratch/halstead/t/tang389/WholeRNAseq_NutriNet/02RNAseqData",as.character(names[i,][1])), to=file.path("/scratch/halstead/t/tang389/WholeRNAseq_NutriNet/02RNAseqData", as.character(names[i,][2])))
}
