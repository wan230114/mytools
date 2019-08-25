# Definition for an interval.
class Interval:

    def __init__(self, s=0, e=0):
        self.start = s
        self.end = e


class Solution:

    def merge(self, intervals):
        """
        :type intervals: List[Interval]
        :rtype: List[Interval]
        """
        if len(intervals) <= 1:
            return intervals
        res = []
        intervals = sorted(intervals, key=lambda start: start.start)
        l = intervals[0].start
        h = intervals[0].end
        for i in range(1, len(intervals)):
            if intervals[i].start <= h:
                h = max(h, intervals[i].end)
            else:
                res.append([l, h])
                l = intervals[i].start
                h = intervals[i].end
        res.append([l, h])
        return res

solution = Solution()
print(solution.merge([Interval(1, 3),
                Interval(5, 10),
                    Interval(2, 6),
                    Interval(7, 18),
                    Interval(19, 23),
                    Interval(15, 20),
                    Interval(16, 30),
                    Interval(21, 25),
                    Interval(35, 40),
                    Interval(45, 50),
                    Interval(46, 52),
                    Interval(53, 54)]))