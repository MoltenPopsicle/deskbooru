import os
import sys
import argparse
from crawler import crawl
from db import db

class tag:
    def add(self):
        file_paths = []
        filestuff = []
        for file_or_dir in arg_filepath:
            if os.path.isdir(file_or_dir) == True:
                file_paths.extend(crawl().get_filepaths(file_or_dir))
            else:
                file_paths.append(os.path.abspath(file_or_dir))
        for filein in file_paths:
            filein = filein.split('/')
            print(filein)
            filestuff.append(filein) 
        print(filestuff)
        db().hashlist(file_paths)





parser = argparse.ArgumentParser()
parser.add_argument('filepath', nargs='+', help='the directory or file(s) you would like to tag')
args = parser.parse_args()
arg_filepath = args.filepath

tag().add()
