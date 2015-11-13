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
            
            #uses add function to add file in list to db file, clears list and does next file
            tagsin = raw_input("What tags do you want to assign? (Separate byone space)")
            filenames.append(tagsin)

            db().add(filenames) 
            del filenames[:]
            count += 1

    global conn
    conn = sqlite3.connect('tags.db') #sqlite3.connect creates file if it doesn't exist
    global c
    c = conn.cursor()

    #adds tables and columns to db file
    def create(self):  
        c.execute('''CREATE TABLE hashtable
                (filename text,
                hash int,
                tags text);''')
        c.execute('''CREATE TABLE tagtable
                (tag text,
                hash int);''')
        print("Table created")
        conn.commit()
    
    #writes filenames and their respective hashes to db file
    def add(self, files): 
        c.execute('INSERT INTO hashtable VALUES (?, ?, ?)', files)
        conn.commit()

sys.argv.pop(0) #removes first entry from sys.argv (the script's filename)
filein = sys.argv

if os.stat('tags.db').st_size == 0: #checks if db file has table in it by filesize
    db().create()

db().hashlist()
print("Files %s hashed and added to the database" % filein)
