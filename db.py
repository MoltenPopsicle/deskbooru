import sys
import os
import sqlite3
import hashlib

class db(object):
    
    #hashes input file
    def hashlist(self, filein):
        def hash_filein(filein):
            h = hashlib.md5()
            with open(filein, 'rb') as f:
                buff = f.read()
                h.update(buff)
                return h.hexdigest()
        #uses tagassign function to add file in list to db file, clears list and does next file
        for arg in filein:
            rawtags = raw_input("Tags to assign to %s (separate by one space): " % arg)
            tagsin = rawtags.split()
            md5hash = hash_filein(arg)
            db().tagassign(arg, md5hash, tagsin) 


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
    def tagassign(self, file, hash, tags): 
        c.execute('INSERT OR REPLACE INTO hashtable (hashes,filename) VALUES (?,?)', (hash, file,))
        for tag in tags:
            c.execute('INSERT OR IGNORE INTO tagtable (tag) VALUES (?)', (tag,))
            #pulls all hashes from tag's row in a list, then appends the list with the new hash and joins it with a comma and space so that the row can be updated
            c.execute('SELECT hashes FROM tagtable WHERE tag = ?', (tag,))
            oldhashes = c.fetchone()[0]
            if oldhashes is None:
                hashes = hash
            elif hash in oldhashes:
                hashes = oldhashes
            else:
                hashes = ', '.join([oldhashes, hash])
           #updates row 
            c.execute('UPDATE tagtable SET hashes = ? WHERE tag = ?', (hashes, tag,))  
        conn.commit()
    
        
    def search(self, tags):
        tag_hashlist = []
        for tag in tags:
            c.execute('SELECT hashes FROM tagtable WHERE tag = ?', (tag,))
            hashes = c.fetchone()
            print(hashes)
            if len(hashes) > 33:
                hashes = hashes.split(', ') 
            #tag_hashlist.extend(hashes)
            tag_hashlist.append(hashes)
	print(tag_hashlist + '\n')
                        
                        
                

                


conn = sqlite3.connect('tags.db') #creates empty db file if it doesn't exist
c = conn.cursor()

if os.stat('tags.db').st_size == 0: #checks if db file has table in it by filesize
    db().create()

