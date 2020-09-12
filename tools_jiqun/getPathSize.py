#!/usr/bin/env python3
import os
import sys


def getsize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            try:
                size += os.path.getsize(os.path.join(root, f))
            except FileNotFoundError:
                pass
                # sys.stderr.write("Warning. file not found: %s\n" %
                #                  os.path.join(root, f))
            # print(f)
    return size


if len(sys.argv) > 1:
    for path in sys.argv[1:]:
        print(getsize(path), path, sep="\t")
else:
    print(getsize("./"), "./", sep="\t")
