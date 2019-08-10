#!/usr/bin/env python3

import os
import sys
from pathlib import Path

def create_file(filename, buf = None):
    if buf == None:
        path = Path(filename)
        path.touch(exist_ok = True)
    elif not os.path.exists(filename):
        mode = 'a' if os.path.exists(filename) else 'w'
        with open(filename, mode) as f:
                f.write(buf)
                f.close()

def create_dir(dirname):
    path = Path(dirname)
    path.mkdir(parents = True, exist_ok = True)

def touch_layers(args):
    TARGET = args[1]
    LAYER = "layer"
    DEPTH = int(args[2])
    NFILES = int(args[3])
    FILENAME = "file"

    path = TARGET
    for depth in range(0, DEPTH):
        path = path + "/" + LAYER + str(depth)
        create_dir(path)
        for count in range(0, NFILES):
            filename = path + "/" + FILENAME + str(count)
            create_file(filename)
            print(filename)


if __name__ == "__main__":
    touch_layers(sys.argv)


