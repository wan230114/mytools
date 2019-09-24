shelp='''
           s1                             p1                         pp1
          /  \                           /
         s2  s2.1                       p2
        /  \    \                  
       s3  s3.1  s3.2              
      /  \  /                      
     s4  s4.1 ___                   
         /  \    \                
        s5  s5.1 s5.2              
'''

# 指定快捷方式，可加入环境变量
alias sjms='python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/sjms.py'

# 提取s2到s4.1的流程
sjms ./test2.job -s -a s2 -b s3,s4.1 >out2.1_tiqu

# 提取s2之后的流程，并去除s4.1之后的流程，加上s2.1（-k与-a会自动去重）
sjms ./test2.job -s -k s2.1    -a s2 -b s4.1  >out2.2_tiqu
sjms ./test2.job -s -k s2,s2.1 -a s2 -b s4.1  >out2.2_tiqu2

# 提取s2之后的流程，并去除s4.1之后的流程，去除s4，加上s2.1
sjms ./test2.job -s -k s2.1 -a s2 -b s3,s4.1    >out2.3_tiqu
sjms ./test2.job -s -k s2.1 -a s2 -b s4.1 -d s4 >out2.3_tiqu2

# 提取s2和s2.1之后的流程，并去除s4.1之后的流程，去除s3和s4
sjms ./test2.job -s -k s2.1 -a s2,s2.1 -b s3,s4.1 -d s3 >out2.4_tiqu
