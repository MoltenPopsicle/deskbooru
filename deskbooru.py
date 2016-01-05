import sys
import os
import subprocess

include_path = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.insert(0, include_path + "/include")
try: 
    option = sys.argv[1]
except:
    print('''Insufficient arguments 
           USAGE: deskbooru.py [COMMAND] [COMMAND OPTIONS]
           For more, use 'deskbooru.py' ''')
    sys.exit()

if option == "add":
    command = include_path + '/include/tagging.py'
    subprocess.Popen(['python2', command, sys.argv[2], sys.argv[3]])
    print "add, good"
