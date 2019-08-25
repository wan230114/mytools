# 测试：

# 按流程的运行顺序，进行job间排序
python3 ../../sjms.py s2-2.job -s  >out0_sorted
# 只打印job名字
python3 ../../sjms.py s2-2.job -s -v >out0_sorted_names
python3 ../../sjms.py s2-2.job -sv >out0_sorted_names2
python3 ../../sjms.py s2-2.job -vs >out0_sorted_names3

# 从s2-2.job中提取：pasa2,evm,training_snap,PASA4training,training_glimmHMM
python3 ../../sjms.py s2-2.job -k pasa2,evm,training_snap,PASA4training,training_glimmHMM >out1_tiqu

# 从s2-2.job中提取：...。并按流程的运行顺序，进行job间排序
python3 ../../sjms.py s2-2.job -k pasa2,evm,training_snap,PASA4training,training_glimmHMM -s >out1_tiqu_sorted
# 只打印jobname
python3 ../../sjms.py s2-2.job -k pasa2,evm,training_snap,PASA4training,training_glimmHMM -vs >out1_tiqu_sorted_names

# 帮助文档
python3 ../../sjms.py -h >out4_print_help

