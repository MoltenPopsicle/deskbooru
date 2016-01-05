import os
import sys
import argparse
import timeit
from crawler import crawl
from db import db, search

class tagAdd(object):
    def add_tag(self, tags, filein):
            db().hash_filein(filein, tags) 
            #print("Tags %s assigned to %s" % (str(tags), filein))
    
    def bulk(self, file_paths):
        tags = raw_input("Tags to assign to all files: ").split(' ')
        for filein in file_paths:
            tagAdd().add_tag(tags, filein) 
    
    def individual(self, file_paths):
        for filein in file_paths:
            tags = raw_input("Tags to assign to %s" % filein)
            tagAdd().add_tag(tags, filein)
    
    def filepath(self, file_paths):
        for filein in file_paths:
            tags = filein.split('/')
            t = timeit.Timer('tagAdd().add_tag(tags, filein)', setup='from __main__ import tagAdd; tags = "fl"; filein = "%s"' % filein)
            time_taken = t.timeit(1)
            print("It took %s seconds to hash %s" %(time_taken, filein))

parser = argparse.ArgumentParser()
parser.add_argument('--bulk', nargs='?') 
parser.add_argument('--directory', nargs='?')
args = parser.parse_args()
if args.directory is not None:
    tagAdd().filepath(crawl().get_filepaths(args.directory))
elif args.bulk is not None:
    tagAdd().bulk(args.bulk)
