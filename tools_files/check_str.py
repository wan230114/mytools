"""输入两个路径检查不同的字符串个数"""

import sys

a, b = sys.argv[1:3]

LEN_a = len(a)
LEN_b = len(b)

if LEN_a == LEN_b:
    NUM = 0
    for i in range(LEN_b):
        # print(a[i], b[i])
        if a[i] != b[i]:
            NUM += 1
    print(NUM)
else:
    print(-1)
