shelp='''
./test2.job:
           s1                             p1                         pp1
          /  \                           /
         s2  s2.1                       p2
        /  \    \                  
       s3  s3.1  s3.2              
      /  \  /                      
     s4  s4.1 ___                   
    /    /  \    \                
   s6   s5  s5.1 s5.2              
'''

# 指定快捷方式，可加入环境变量
alias sjms='python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/sjms.py'

# 1：提取s2, s3, s3.1, s4.1
sjms ./test2.job -s  -k s2,s3,s3.1,s4.1 >out2.1_tiqu1       # 方法1：-k 暴力提取（适用job量少时）
sjms ./test2.job -s  -a s2  -b s4.1 -d s4,s6 >out2.1_tiqu2  # 方法2：-d删除s4,s6
sjms ./test2.job -s  -a s2  -b s3,s4.1       >out2.1_tiqu3  # 方法3：-b去除s3之后
sjms ./test2.job -s  -a s2  -b s3,s4.1 -v >out2.1_tiqu_name1   # 只打印名字 
sjms ./test2.job -vs -a s2  -b s3,s4.1    >out2.1_tiqu_name2   # 只打印名字

# 2：提取s2, s3.1, s4.1, s2.1
sjms ./test2.job -s -k s2,s3.1,s4.1,s2.1  >out2.2_tiqu2              # 方法1：-k 暴力提取
sjms ./test2.job -s -k s2.1 -a s2 -b s3,s4.1 -d s3  >out2.2_tiqu2    # 方法2：-a去除s3和s4.1之后，-d删除s3
sjms ./test2.job -s -k s2.1 -a s2 -b s4.1 -d s3,s4,s6  >out2.2_tiqu3 # 方法3：-a去除s4.1之>后，-d删除s3,s4,s6

# 3: 提取s2, s3, s3.1, s4, s4.1, s6, s2.1, s3.2。【s2和s2.1之后的流程，并去除s4.1之后的流程】
sjms ./test2.job -s -a s2,s2.1 -b s4.1    >out2.3_tiqu1
sjms ./test2.job -s -a s2,s2.1 -d s5,s5.1,s5.2 >out2.3_tiqu2

# other，参数重复问题
sjms ./test2.job -s -k s2.1    -a s2 -b s4.1  >out2.4_tiqu
sjms ./test2.job -s -k s2,s2.1 -a s2 -b s4.1  >out2.4_tiqu2  # -k与-a之间会自动去重
