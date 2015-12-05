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
            
            #uses tagassign function to add file in list to db file, clears list and does next file
            rawtags = raw_input("Tags to assign to %s (separate by one space): " % filein[count])
            tagsin = rawtags.split()
            
            db().tagassign(filein[count], md5hash, tagsin) 
            count += 1


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
            else:
                hashes = ', '.join([oldhashes, hash])      
           #updates row 
            c.execute('UPDATE tagtable SET hashes = ? WHERE tag = ?', (hashes, tag,)) 
        conn.commit()
    
        
    def search(self, tags):
        first_hashes = []
        seen = set()
        matched_hashes = []
        for tag in tags:
            c.execute('SELECT hashes FROM tagtable WHERE tag = ?', (tag,))
            tag_hashes = c.fetchone()
            tag_hashlist = tag_hashes[0].split(', ')
            first_hashes.extend(tag_hashlist)
        for current_hash in first_hashes:
            occurrences = first_hashes.count(current_hash)
            if occurrences != len(tags):
                first_hashes.remove(current_hash)
            else:
                matched_hashes.append(current_hash)
                
        print(str(matched_hashes) + '\n')
        print str(seen)
                        
                        
                

                


conn = sqlite3.connect('tags.db') #creates empty db file if it doesn't exist
c = conn.cursor()

if os.stat('tags.db').st_size == 0: #checks if db file has table in it by filesize
    db().create()

