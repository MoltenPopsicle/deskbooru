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
    parser.add_argument('-p', '--path', nargs='*', help='Tag all files under a directory recursively by their parent directories e.g. a file under /home/user would be tagged home and user. If the first argument passed to -p is not a directory, it will be interpreted as a tag or list of tags (separate by a comma and a space) to NOT assign to files')
    parser.add_argument('-f', '--filename', nargs='*', help='Tag files or directories of files by their filename, tags seperated by a hyphen e.g. a file named python-important-due_friday would be tagged python, important, and due_friday')
    parser.add_argument('--timetest', nargs='?', help='Test the speed of the hasing/adding function using the path argument')
    args = parser.parse_args()
    
    if args.bulk is not None:
        tags = args.bulk[0].split(', ')
        dirs = args.bulk[1:]
        for directory in dirs:
            files = crawl().get_filepaths(directory)
            print(files)
            tagging.tagAdd().bulk(files, tags)
    
    if args.individual is not None:
        for directory in args.individual:
            if os.path.isdir(directory):
                files = crawl().get_filepaths(directory)
                for file in files:
                    tags = input("Tags to assign to %s: " % file).split(', ')
                    file = os.path.realpath(file)
                    tagging.tagAdd().add_tag(tags, file)
            else:
                file = os.path.realpath(directory)
                print(file)
                tags = input("Tags to assign to %s: " % directory).split(', ')
                tagging.tagAdd().add_tag(tags, file)
    
    if args.path is not None:
        tag_exclude = ['']
        dirs = []
        if os.path.isdir(args.path[0]):
            dirs.extend(args.path)
        else:
            tag_exclude = args.path[0].split(', ')
            dirs.extend(args.path[1:])
        for directory in dirs:
            files = crawl().get_filepaths(directory)
            tagging.tagAdd().filepath(files, tag_exclude)
    
    if args.filename is not None:
        try:
            if os.path.isdir(args.filename[0]):
                directory = os.path.abspath(args.filename[0])
                files = crawl().get_filepaths(directory)
            else:
                files = (os.path.abspath(args.filename[0]), )
        #So that the user can use both -f and -p, the index error returned when trying to use them both is handled as performing the normal filename argument except on the directory given to -p. Will figure out a better way to do this later.
        except IndexError:
            if os.path.isdir(args.path[0]) == False:
                args.path.pop(0)
            for path in args.path:
                files = crawl().get_filepaths(path)
        for file in files:
            tagging.tagAdd().filename(file)
    
    if args.timetest is not None:
        directory = args.timetest
        files = crawl().get_filepaths(directory)
        tagging.tagAdd().timetest(files)

if args.command == "search":
    taglist = args.options[0].split(' ')
    search().results(taglist)

if args.command == "rm":
    parser._actions[-1].container._remove_action(parser._actions[-1])
    parser.add_argument("-t", "--tag", nargs='*', help="Remove specific tag(s) from file(s)")
    parser.add_argument("filepath", nargs='*', help="File(s) or directories to remove")
    args = parser.parse_args()
    if args.tag:
        tags_remove = args.tag[0]
        filepaths = args.tag[1:]
    else:
        filepaths = args.filepath
    for filepath in filepaths:
        filepath = os.path.abspath(filepath)
        if os.path.isdir(filepath):
            files = crawl().get_filepaths(filepath)
        else:
            files = filepath
        if args.tag is None:
            db().rm(filepath)
        else:
            db().rm(filepath, tags_remove)
    #if os.path.isdir(args.filepath[0]):
    #    print("is dir")
    #else:
    #    print("is not dir")
    #db().remove(args.filepath)
