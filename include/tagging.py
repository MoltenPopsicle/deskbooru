import os
import sys
import argparse
import timeit
from crawler import crawl
from db import db, search

class tagAdd(object):
    def add_tag(self, tags, filein):
            db().hash_filein(filein, tags)
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
        for filein in file_paths:
            tags = filein.split('/')
            t = timeit.Timer('tagAdd().add_tag(tags, filein)', setup='from tagging import tagAdd; tags = "fl"; filein = "%s"' % filein)
            time_taken = t.timeit(1)
            print("It took %s seconds to hash %s" %(time_taken, filein))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bulk', nargs='?') 
    parser.add_argument('-f', '--filepath_name', nargs='?')
    parser.add_argument('--timetest', nargs='?')
    args = parser.parse_args()
    print(args)
    if args.filepath_name is not None:
        tagAdd().filepath(crawl().get_filepaths(filepath_name))
    elif args.bulk is not None:
        tagAdd().bulk(crawl().get_filepaths(args.bulk))
