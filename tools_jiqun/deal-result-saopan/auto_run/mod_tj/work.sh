#########################################################################
# File Name: work.sh
# Author: caohong
# mail: caohong@novogene.com
# Created Time: Wed 19 Jul 2017 07:19:18 PM CST
#########################################################################
#!/bin/bash
qsub -V -cwd -l vf=1G -b n -sync y  -q plant2.q,plant1.q,all.q,plant.q,joyce.q ./geShell.sh
sh ./qsub_scan.sh
