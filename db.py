import sys
import os
import sqlite3
import hashlib

class db(object):
    
    global filenames
    filenames = [] #list of all files and hashes to insert into db file

    #hashes input file
    def hashlist(self):
        h = hashlib.md5()
        count = 0
        for arg in filein:
            with open(arg, 'rb') as f:
                buff = f.read()
                h.update(buff)
                md5hash = h.hexdigest()
                filenames.append(filein[count]) #adds filename to list
                filenames.append(md5hash) #adds the hash to list
                filenames.append('''
''') #adds a newline to the list
                count += 1
 
    global conn
    conn = sqlite3.connect('tags.db') #sqlite3.connect creates file if it doesn't exist
    global c
    c = conn.cursor()

    #adds table and columns to db file
    def create(self):  
        c.execute('''CREATE TABLE files
                (filename text,
                hash integer);''')
        print("Table created")
        conn.commit()
    
    #writes filenames and their respective hashes to db file
    def add(self): 
        c.execute('INSERT INTO files VALUES (?, ?)', filenames)
        print("Files hashed and added")
        conn.commit()

sys.argv.pop(0) #removes first entry from sys.argv (the script's filename)
filein = sys.argv

if os.stat('tags.db').st_size == 0: #checks if db file has table in it by filesize
    db().create()

db().hashlist()
print filenames
conn.close()
