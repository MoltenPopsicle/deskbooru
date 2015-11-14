import sys
import os
import sqlite3
import hashlib

class db(object):
    
    #hashes input file
    def hashlist(self):
        h = hashlib.md5()
        count = 0
        for arg in filein:
            with open(arg, 'rb') as f:
                buff = f.read()
                h.update(buff)
                md5hash = h.hexdigest()
            
            #uses add function to add file in list to db file, clears list and does next file
            rawtags = raw_input("What tags do you want to assign to %s? (Separate by one space) " % filein[count])
            tagsin = rawtags.split()
            
            db().add(filein[count], md5hash, tagsin) 
            count += 1


    global conn
    conn = sqlite3.connect('tags.db') #sqlite3.connect creates file if it doesn't exist
    global c
    c = conn.cursor()

    #adds tables and columns to db file
    def create(self):  
        c.execute('''CREATE TABLE hashtable
                (hash integer PRIMARY KEY,
                filename text);''')
        c.execute('''CREATE TABLE tagtable
                (tag text PRIMARY KEY,
                hashes integer);''')
        print("Table created")
        conn.commit()
    
    #writes filenames and their respective hashes to db file
    def add(self, files, hash, tags): 
        c.execute('INSERT OR REPLACE INTO hashtable VALUES (?,?)', (hash, files))
        
        for tag in tags:
            c.execute('INSERT OR IGNORE INTO tagtable (tag) VALUES (?)', (tag,))
            
            c.execute('SELECT hashes FROM tagtable WHERE tag = ?', (tag,))
            oldhashes = c.fetchone()[0]
            if oldhashes is None:
                hashes = hash
            else:
                hashes = ' '.join([oldhashes, hash])
            
            c.execute('UPDATE tagtable SET hashes = ? WHERE tag = ?', (hashes, tag,))
        
        conn.commit()

sys.argv.pop(0) #removes first entry from sys.argv (the script's filename)
filein = sys.argv

if os.stat('tags.db').st_size == 0: #checks if db file has table in it by filesize
    db().create()

db().hashlist()
print("Files %s hashed and added to the database" % filein)
