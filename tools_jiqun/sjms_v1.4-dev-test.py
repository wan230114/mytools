r'''需求说明：
说明：
    提取树图中某一节点之后的点。
示例：

          1
         / \
        2   3
       / \   \
      4   5   8
     / \
    6   7
输入：
    iters = [2, 3]
    D_orders = {1: {2, 3}, 2: {4, 5}, 3:{8}, 4: {6, 7}}
输出：
    L = [2, 4, 5, 6, 7, 3, 8]
'''

iters = [2, 3]
D_orders = {1: {2, 3}, 2: {4, 5}, 3: {8}, 4: {6, 7}}


def get_afters_job(iters, D_orders):
    iters2 = []
    for x in iters:
        if x in D_orders:
            result = []
            tmp = {x}
            while tmp:
                for xx in tmp.copy():
                    if xx not in result:
                        result.append(xx)
                    tmp.remove(xx)
                    if xx in D_orders:
                        for x in D_orders[xx]:
                            tmp.add(x)
            iters2 += result
    return iters2


print(get_afters_job(iters, D_orders))
