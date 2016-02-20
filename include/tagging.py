import os
import sys
import argparse
import timeit
from crawler import crawl
from db import db, search

class tagAdd(object):
    def add_tag(self, tags, filein):
            db().tagassign(filein, tags)
            print("Tags %s assigned to %s" % (str(tags), filein))
    
    def bulk(self, file_paths, tags):
        for filein in file_paths:
            tagAdd().add_tag(tags, filein)

    def individual(self, file_paths, tags):
            tagAdd().add_tag(tags, filein)
    
    def filepath(self, file_paths, tag_exclude):
        for filein in file_paths:
            tags = filein.split('/')
            if tag_exclude is not None:
                tags[:] = [tag for tag in tags if tag not in tag_exclude]
                print(tags)
            tagAdd().add_tag(tags, filein)
    def timetest(self, file_paths):
        numbers = []
        for filein in file_paths:
            try:
                tags = filein.split('/')
                t = timeit.Timer('tagAdd().add_tag(tags, filein)', setup='from tagging import tagAdd; tags = "fl"; filein = "%s"' % filein)
                time_taken = t.timeit(1)
                numbers.append(time_taken)
            except:
                break
            print("It took %s seconds to hash %s" %(time_taken, filein))
        #print(numbers)
        avg = 0
        for number in numbers:
            avg = avg + number
        total = avg
        avg = avg / len(numbers)
        print("\nMean tag time is %s, total tag time is %s" % (avg, total))
