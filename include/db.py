import sys
import os
import sqlite3
import hashlib

class db(object):
    count = 0
    #hashes input file and adds it and its tags to db
    def hash_filein(self, filein, tags):
        h = hashlib.md5()
        with open(filein, 'rb') as f:
            buff = f.read()
            h.update(buff)
            md5hash = h.hexdigest()
        db().tagassign(filein, md5hash, tags)
    
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
    
        
class search(object):
    def regex(self, tag_hashlist, hashes, tag):
        temphash = []
        if '~' in tag:
            tag_hashlist.extend(hashes)
        else:
            for h in tag_hashlist:
                print(regex)
                if '-' in tag and h in hashes:
                    print("%s is minus and %s will be removed" % (tag, h))
                    temphash.append(h)
                elif regex == False and h not in hashes:
                    temphash.append(h)
                    print("either and or a big dumb")
            for h in temphash:
                tag_hashlist.remove(h)
        return tag_hashlist
    
    def results(self, tags):
        global regex
        file_list = []
        tag_hashlist = []
        initial = False
        print(tags)
        for tag in tags:
            regex = True
            print(tag)
            if '~' in tag:
                tagin = tag.translate(None, '~')
            elif '-' in tag:
                print("MINUS")
                tagin = tag.translate(None, '-')
            else:
                tagin = tag
                regex = False
            c.execute('SELECT hashes FROM tagtable WHERE tag = ?', (tagin,))
            hashes = c.fetchone()[0]
            if len(hashes) <= 33 and initial == False:
                tag_hashlist = hashes
            else:
                hashes = hashes.split(', ')
                if initial == False:
                    tag_hashlist.extend(hashes)
            tag_hashlist = search().regex(tag_hashlist, hashes, tag)
            initial = True
        for h in tag_hashlist:
            c.execute('SELECT filename FROM hashtable WHERE hashes = ?', (h,))
            filename = c.fetchone()
            file_list.append(filename)
        print(file_list)
        return file_list
                


conn = sqlite3.connect('tags.db') #creates empty db file if it doesn't exist
c = conn.cursor()

if os.stat('tags.db').st_size == 0: #checks if db file has table in it by filesize
    db().create()

