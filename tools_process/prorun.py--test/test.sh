echo "
sleep 1 && echo 1
sleep 1 && echo 2
sleep 1 && echo 3
sleep 1 && echo 4
sleep 1 && echo 5
sleep 1 && echo 6
sleep 1 && rm 7
sleep 1 && echo 8
sleep 1 && echo 9
sleep 1 && rm 10
" | awk NF  > work.sh

cat work.sh | xargs -iCMD -P3 bash -c CMD

prorun -t 3 -l 2 work.sh -s

prorun -t 3 -l 2 work.sh
