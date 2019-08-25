def merge(intervals):
    """
    :type intervals: List[Interval]
    :rtype: List[Interval]
    """
    if len(intervals) <= 1:
        return intervals
    res = []
    intervals = sorted(intervals, key=lambda start: start[0])
    l = intervals[0][0]
    h = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] <= h:
            h = max(h, intervals[i][1])
        else:
            res.append([l, h])
            l = intervals[i][0]
            h = intervals[i][1]
    res.append([l, h])
    return res

print(merge([[1,3],[2,6],[10,20],[15,35]]))
print(merge([[25, 1886], [933, 1741], [1, 812], [915, 1799], [915, 1741], [915, 1799], [906, 1741], [915, 1741], [790, 1573], [938, 1799],[3000,5000]]))