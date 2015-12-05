import sys
import os
import sqlite3
import hashlib

class db(object):
    
    #hashes input file
    def hashlist(self, filein):
        h = hashlib.md5()
        count = 0
        for arg in filein:
            with open(arg, 'rb') as f:
                buff = f.read()
                h.update(buff)
                md5hash = h.hexdigest()
            
            #uses add function to add file in list to db file, clears list and does next file
            rawtags = raw_input("Tags to assign to %s (separate by one space): " % filein[count])
            tagsin = rawtags.split()
            
            db().add(filein[count], md5hash, tagsin) 
            count += 1


    global conn
    #sqlite3.connect creates file if it doesn't exist already
    conn = sqlite3.connect('tags.db')  
    global c
    c = conn.cursor()

    #adds tables and columns to db file
    def create(self):  
        c.execute('''CREATE TABLE hashtable
                (hashes text UNIQUE,
                filename text);''')
        c.execute('''CREATE TABLE tagtable
                (tag text PRIMARY KEY,
                hashes text);''')
        print("Table created")
        conn.commit()
    
    #writes filenames and their respective hashes to db file
    def add(self, file, hashin, tags): 
        c.execute('INSERT OR REPLACE INTO hashtable (hashes,filename) VALUES (?,?)', (hashin, file,))
        for tag in tags:
            c.execute('INSERT OR IGNORE INTO tagtable (tag) VALUES (?)', (tag,)) 
            #pulls all hashes from tag's row in a list, then appends the list with the new hash and joins it with a comma and space so that the row can be updated
            c.execute('SELECT hashes FROM tagtable WHERE tag = ?', (tag,))
            oldhashes = c.fetchone()[0] 
            if oldhashes is None:
                hashes = hashin
            elif hashin in oldhashes == True:
                hashes = oldhashes
            else:
                hashes = ', '.join([oldhashes, hashin]) 
           
           #updates row 
            c.execute('UPDATE tagtable SET hashes = ? WHERE tag = ?', (hashes, tag,))
        print(hashes)
        conn.commit()

if os.stat('tags.db').st_size == 0: #checks if db file has table in it by filesize
    db().create()

