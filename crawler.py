#!/bin/python2
import os
from os.path import join, getsize
scanroot = input('Where do you want to scan\n? ')
print ('Scan root set to', scanroot)

for root, dirs, files in os.walk(scanroot):
    print root, "consumes",
    print sum(getsize(join(root, name)) for name in files),
    print "bytes in", len(files), "non-directory files"
