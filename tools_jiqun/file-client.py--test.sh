# 本示例下载SRR4036107数据，并进行解压（转发脚本目前仅支持1人下载，后来者会显示排队，请协商使用）
# 通过如下命令可以获取到sra的网址(获取到之后可以直接ctrl+c终止,国内网很难下通的)，https://sra-download.ncbi.nlm.nih.gov/sos/sra-pub-run-1/SRR4036107/SRR4036107.1，将其复制下来进行数据转发
# 命令：/ifs/TJPROJ3/Plant/chenjun/software/sratoolkit/sratoolkit.2.9.6-centos_linux64/bin/prefetch SRR4036107 -v -O .


# 1) 数据转发下载
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/file-client.py https://sra-download.ncbi.nlm.nih.gov/sos/sra-pub-run-1/SRR4036107/SRR4036107.1
# 2) 文件命名
mv SRR4036107.1 SRR4036107.sra
# 3) 下载结束邮件提醒
python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py 1170101471@qq.com -c "下载好了，`pwd`" 
# 4) 提交解压命令
echo "/ifs/TJPROJ3/Plant/chenjun/software/sratoolkit/sratoolkit.2.9.6-centos_linux64/bin/fastq-dump --split-3 SRR4036107.sra --gzip -O ./" >SRR4036107.sra--unzip.sh
echo "python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py 1170101471@qq.com -c 解压完毕" >>SRR4036107.sra--unzip.sh
qsub -cwd -l vf=0.3g,p=1 SRR4036107.sra--unzip.sh



# 另外，若想实时查看下载速度可以在目录下运行词条命令：
#   while true;do sleep 10 && du -b --block-size M SRR4036107.1 ; done
