#!/usr/bin/python2
import sys
import os
import subprocess
import argparse
import sys
include_path = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.insert(0, include_path + '/include')
import tagging
from crawler import crawl
#import search

print(sys.path)
parser = argparse.ArgumentParser()
parser.add_argument('command', nargs='?',  help='deskbooru command to use')
parser.add_argument('options', nargs=argparse.REMAINDER, help='options to pass to the deskbooru command')
args = parser.parse_args()
args.options = None

print(args)
print(args.command)
print(args.options)

if args.command == "add":
    parser.add_argument('-b', '--bulk', nargs='?', help='Tag all files under a directory recursively with one set of specified tags')
    parser.add_argument('-i', '--individual', nargs='*', help='Tag one or more files with a set of specified tags for each file')
    parser.add_argument('-p', '--path', nargs='?', help='Tag all files under a directory recursively by their parent directories e.g. a file under /home/user would be tagged home and user')
    parser.add_argument('--timetest', nargs='?', help='Test the speed of the hasing/adding function using the path argument')
    parser._handle_conflict_resolve(None, [(
    args = parser.parse_args()
    print(args)
    print(args.bulk)
