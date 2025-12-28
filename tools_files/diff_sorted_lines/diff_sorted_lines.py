
import sys
print(sys.version)
with open(sys.argv[1], "rb") as fi1, \
        open(sys.argv[2], "rb") as fi2:
    n = 0
    while True:
        n += 1
        line1 = fi1.readline()
        line2 = fi2.readline()
        # print(line1, line2)
        if not line1:
            break
        L1 = line1.rstrip().split(b"\t")
        L2 = line2.rstrip().split(b"\t")
        L1.sort()
        L2.sort()
        if L1 == L2:
            continue
        else:
            raise AssertionError(f"检测未通过, 第 {n} 行不一致,\nfile1:{line1.decode()}vs\nfile2:{line2.decode()}")
    print("检测通过")