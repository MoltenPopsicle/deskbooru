#!/usr/bin/python3
import sys
import os
import argparse
import sys
include_path = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.insert(0, include_path + '/include')
import tagging
from crawler import crawl
from db import search, db
#import search

parser = argparse.ArgumentParser()
parser.add_argument('command', nargs='?',  help='deskbooru command to use')
parser.add_argument('options', nargs=argparse.REMAINDER, help='options to pass to the deskbooru command')
args = parser.parse_args()


if args.command == "add":
    #remove options from the list of arguments, as options is useless for addition
    parser._actions[-1].container._remove_action(parser._actions[-1])
    parser.add_argument('-b', '--bulk', nargs='*', help='Tag all files under a directory recursively with one set of specified tags')
    parser.add_argument('-i', '--individual', nargs='*', help='Tag one or more files with a set of specified tags for each file')
    parser.add_argument('-p', '--path', nargs='*', help='Tag all files under a directory recursively by their parent directories e.g. a file under /home/user would be tagged home and user')
    parser.add_argument('--timetest', nargs='?', help='Test the speed of the hasing/adding function using the path argument')
    parser.add_argument('--nohash', help='Tag files without hashing them (NOT RECOMMENDED; duplicates and changes in filename WILL affect the database)')
    args = parser.parse_args()
    if args.bulk is not None:
        tags = args.bulk[0].split(' ')
        dirs = args.bulk[1:]
        for dir in dirs:
            files = crawl().get_filepaths(dir)
            print(files)
            tagging.tagAdd().bulk(files, tags)
    elif args.individual is not None:
        for dir in args.individual:
            if os.path.isdir(dir):
                files = crawl().get_filepaths(dir)
                for file in files:
                    tags = raw_input("Tags to assign to %s: " % file)
                    file = os.path.realpath(file)
                    tagging.tagAdd().add_tag(tags, file)
            else:
                file = os.path.realpath(dir)
                print(file)
                tags = raw_input("Tags to assign to %s: " % dir)
                tagging.tagAdd().add_tag(tags, file)
    elif args.path is not None:
        tag_exclude = args.path[0].split(' ')
        if '"' not in tag_exclude[0]:
            print("working")
            dirs = args.path
            tag_exclude = None
        else:
            dirs = args.path[1:]
        for dir in dirs:
            files = crawl().get_filepaths(dir)
            tagging.tagAdd().filepath(files, tag_exclude)
    elif args.timetest is not None:
        dir = args.timetest
        files = crawl().get_filepaths(dir)
        tagging.tagAdd().timetest(files)

if args.command == "search":
   search().results(args.options)

if args.command == "rm":
    parser._actions[-1].container._remove_action(parser._actions[-1])
    parser.add_argument("-t", "--tag", nargs='?', help="Remove specific tag(s) from file(s)")
    parser.add_argument("filepath", help="File(s) or filepath to remove")
    args = parser.parse_args()
    print(args.tag)
    db().remove(args.filepath[0], args.tag[0])
    #if os.path.isdir(args.filepath):
        #files = crawl().get_filepaths(args.filepath)
    #else:
        #files = args.filepath
    #print(files)
