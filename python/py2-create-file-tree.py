#!/usr/bin/env python

import os
import sys

def create_file(filename, buf = None):
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode) as f:
        if buf != None:
            f.write(buf)
        f.close()

def touch_layers(args):
    TARGET = args[1]
    LAYER = "layer"
    DEPTH = int(args[2])
    NFILES = int(args[3])
    FILENAME = "file"

    path = TARGET
    if not os.path.exists(path):
        os.mkdir(path)
    for depth in range(0, DEPTH):
        path = path + "/" + LAYER + str(depth)
        if not os.path.exists(path):
            os.mkdir(path)
        for count in range(0, NFILES):
            filename = path + "/" + FILENAME + str(count)
            if not os.path.exists(filename):
                create_file(filename)
            print filename


if __name__ == "__main__":
    touch_layers(sys.argv)


