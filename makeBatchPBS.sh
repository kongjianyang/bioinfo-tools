#!/bin/bash

for i in 2 4 6 8;
do
        SCRIPT="#/bin/bash\n#PBS -l nodes=1:ppn=$i,walltime=00:10:00,naccesspolicy=shared\n\n"
        SCRIPT+="#PBS -q scholar\n#PBS -m ae\n#PBS -M tang389@purdued.edu\n"
        SCRIPT+="#PBS -N large.$i\n\n"
        SCRIPT+="cd \$PBS_O_WORKDIR\nmodule load bioinfo\nmodule load blast/2.7.1+\n\n"
        SCRIPT+="blastp -db ProtFam -outfmt 6 -evalue 1e-4 -num_threads $i -query largeSet.fasta -out Blast.$i.out"
        echo -e $SCRIPT >blastTestScripted.pbs
        qsub blastTestScripted.pbs
        sleep 2
done
