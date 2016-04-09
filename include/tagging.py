import os
import sys
import argparse
import timeit
from crawler import crawl
from db import db, search

class tagAdd(object):
    def add_tag(self, tags, filein):
            assign = db().tagassign(filein, tags)
            if assign == "No change":
                print("File %s already tagged" % filein)
            else:
                print("Tags %s assigned to %s" % (str(tags), filein))
    def bulk(self, file_paths, tags):
        for filein in file_paths:
            tagAdd().add_tag(tags, filein)

    def individual(self, file_paths, tags):
            tagAdd().add_tag(tags, filein)
    
    def filepath(self, file_paths, tag_exclude):
        for filein in file_paths:
            tags = filein.split('/')
            tag_exclude.append('')
            tag_exclude.append(os.path.basename(filein))
            tags[:] = [tag for tag in tags if tag not in tag_exclude]
            tagAdd().add_tag(tags, filein)
    def filename(self, file_paths):
        file = os.path.basename(file_paths)
        tags = file.split('-')
        if '.' in file:
            filetype = file.split('.')[-1]
            tags.append("type:" + filetype)
        tagAdd().add_tag(tags, file_paths)
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
            print("It took %s seconds to add %s to the database" %(time_taken, filein))
        avg = 0
        for number in numbers:
            avg = avg + number
        total = avg
        avg = avg / len(numbers)
        print("\nMean tag time is %s, total tag time is %s for %s files" % (avg, total, len(numbers)))
