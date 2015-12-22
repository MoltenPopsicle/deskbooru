import os
import sys
import argparse
from crawler import crawl
from db import db, search

class add(object):
    def standard(self):
        file_paths = []
        filestuff = []
        for file_or_dir in arg_filepath:
            if os.path.isdir(file_or_dir) == True:
                file_paths.extend(crawl().get_filepaths(file_or_dir))
            else:
                file_paths.append(os.path.abspath(file_or_dir))
        choice = raw_input("BULK, FILEPATH, STANDARD or SEARCH?")
        if choice == 'SEARCH':
            tags = raw_input("Tags to search for: ")
            search().results(tags) 
        elif choice == 'FILEPATH':
            tags = filein.split('/')
        elif choice == 'BULK':
            tags = raw_input("Tags to assign to all files: ")
        for filein in file_paths:
            if choice == 'STANDARD':
                tags = raw_input("Tags to assign to %s" % filein)
            db().hash_filein(filein, tags) 
        print(filestuff)

parser = argparse.ArgumentParser()
parser.add_argument('filepath', nargs='+', help='the directory or file(s) you would like to tag')
args = parser.parse_args()
arg_filepath = args.filepath
add().standard()
