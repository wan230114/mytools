source /home/chenjun/.bashrc

cd /ifs/TJPROJ3/Plant/chenjun/Admin/02.saopan
cat lastdate |xargs -i echo "cd {}/result_stat_scan && sh qsub-run.sh"|sh

