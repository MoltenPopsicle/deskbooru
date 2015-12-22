import os
import sys
import argparse
from crawler import crawl
from db import db, search

class add(object):
    def standard(self):
        file_paths = []
        global counter
        counter = 0
        for file_or_dir in arg_filepath:
            if os.path.isdir(file_or_dir) == True:
                file_paths.extend(crawl().get_filepaths(file_or_dir))
            else:
                file_paths.append(os.path.abspath(file_or_dir))
        choice = raw_input("BULK, FILEPATH, STANDARD or SEARCH: ")
        if choice == 'SEARCH':
            tags = raw_input("Tags to search for: ").split(' ')
            search().results(tags) 
        elif choice == 'BULK':
            tags = raw_input("Tags to assign to all files: ").split(' ')
            for filein in file_paths:
                db().hash_filein(filein, tags) 
                print("Tags %s assigned to %s" % (str(tags), filein))
                counter += 1
        if choice == 'STANDARD':
            for filein in file_paths:
                tags = raw_input("Tags to assign to %s" % filein)
                db().hash_filein(filein, tags) 
                print("Tags %s assigned to %s" % (str(tags), filein))
                counter += 1
        elif choice == 'FILEPATH':
            for filein in file_paths:
                tags = filein.split('/')
                db().hash_filein(filein, tags) 
                print("Tags %s assigned to %s" % (str(tags), filein))
                counter += 1

parser = argparse.ArgumentParser()
parser.add_argument('filepath', nargs='+', help='the directory or file(s) you would like to tag')
args = parser.parse_args()
arg_filepath = args.filepath
add().standard()
