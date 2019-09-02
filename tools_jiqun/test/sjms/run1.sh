# 指定快捷方式，可加入环境变量
alias sjms='python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/sjms.py'

# 帮助文档
sjms -h >out1.0_print_help


# 测试：

# 1) -v -s 测试，-v只打印jobNames，-s打印按执行顺序排序后的job
# 按流程的运行顺序，进行job间排序
sjms ./test1.job -s  >out1.1_sorted
# 只打印job名字，真值参数可以直接拼接，类似于linux的`ls -lhtr`，以下结果一致
sjms ./test1.job -s -v >out1.1_sorted_names
sjms ./test1.job -sv >out1.1_sorted_names2
sjms ./test1.job -vs >out1.1_sorted_names3

# 2) -k 参数测试，用于提取指定job
# 从./test1.job中提取指定job
sjms ./test1.job -k pasa2,evm,training_snap,PASA4training,training_glimmHMM >out1.2_tiqu
# 从./test1.job中提取指定job。并按流程的运行顺序，进行job间排序
sjms ./test1.job -sk pasa2,evm,training_snap,PASA4training,training_glimmHMM >out1.2_tiqu_sorted
# 从./test1.job中提取指定job。并按流程的运行顺序，进行job间排序，只打印jobname
sjms ./test1.job -vsk pasa2,evm,training_snap,PASA4training,training_glimmHMM >out1.2_tiqu_sorted_names

# 3) -a 参数测试，用于提取某几个节点及之后流程预运行的job
sjms ./test1.job -s -k function_filter -a function_filter >out1.3_tiqu_get-afters
