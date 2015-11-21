import os
import sys
import argparse
from crawler import crawl
from db import db

class tag:
    
    def add(self):
        if os.path.isdir(arg_filepath[0]) == True:
            dir = str(arg_filepath[0])
            file_paths = crawl().get_filepaths(dir)
        else:
            file_paths = arg_filepath
        db().hashlist(file_paths)





parser = argparse.ArgumentParser()
parser.add_argument('filepath', nargs='+', help='the directory or file(s) you would like to tag')
args = parser.parse_args()
arg_filepath = args.filepath

tag().add()
