shelp='''
           s1
          /  \
         s2  s2.1
        /  \    \
       s3  s3.1  s3.2
      /  \  /
     s4  s4.1 ___
         /  \    \
        s5  s5.1 s5.2
'''

# 指定快捷方式，可加入环境变量
alias sjms='python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_jiqun/sjms.py'

# 提取s2到s4.1的流程，加上s2.1
sjms ./test2.job -s -k s2,s2.1  -a s2 -b s3,s4.1 >out2.1_tiqu

