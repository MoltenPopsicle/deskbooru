import sys
import os
import sqlite3
import hashlib

class db(object):
    count = 0
    #ids input file and adds it and its tags to db
    def hash_filein(self, filein, tags):
        h = hashlib.md5()
        with open(filein, 'rb') as f:
            buff = f.read()
            h.update(buff)
            md5hash = h.hexdigest()
        db().tagassign(filein, md5hash, tags)
    
    #adds tables and columns to db file
    def create(self):  
        c.execute('''CREATE TABLE IDtable
                (filename text,
                tags text,
                filesize int);''')
        c.execute('''CREATE TABLE tagtable
                (tag text PRIMARY KEY,
                ids text);''')
        print("Table created")
        conn.commit() 

    #writes filenames and their respective ids to db file
    def tagassign(self, file, tags, *args):
        filesize = os.path.getsize(file)
        idtable_tags = str(tags).replace('[','')
        idtable_tags = idtable_tags.replace(']', '')
        idtable_tags = idtable_tags.replace("'", '')
        c.execute('INSERT OR REPLACE INTO IDtable (filename, tags, filesize) VALUES (?,?,?)', (file, idtable_tags, filesize,))
        for tag in tags:
            c.execute('INSERT OR IGNORE INTO tagtable (tag) VALUES (?)', (tag,))
            #pulls all ids from tag's row in a list, then appends the list with the new hash and joins it with a comma and space so that the row can be updated
            c.execute('SELECT ids FROM tagtable WHERE tag = ?', (tag,))
            oldids = str(c.fetchone()[0])
            c.execute('SELECT ROWID FROM IDtable where filename = ?', (file,))
            newid = str(c.fetchone()[0])
            if newid in oldids:
                return "No change"
            elif oldids != "None":
                ids = ', '.join([oldids, newid])
            else:
                ids = newid
           #updates row
            c.execute('UPDATE tagtable SET ids = ? WHERE tag = ?', (ids, tag,))  
        conn.commit()
    
    def rm(self, file, *args):
        c.execute('SELECT ROWID FROM IDtable WHERE filename = ?', (file,))
        file_id = c.fetchone()[0]
        #Check whether the file is to be removed, or if tags are to be removed from a file. If the file is to be removed totally, it must be removed from the ID table, and the tags whose ID lists need to have the ID of the file removed are every tag the file was tagged with. Else the tags are the ones specified and the file is not removed from the ID table. 
        if args:
            tag_removal = args
            print("Tags %s to be removed from %s" % (str(tag_removal), file))
        else:
            c.execute('SELECT tags FROM IDtable WHERE ROWID = ?', (file_id,))
            tag_removal = c.fetchone()[0].split(', ')
            c.execute('DELETE FROM IDtable where ROWID = ?', (file_id,))
            print("File %s removed from the database" % file)
            print("FileID")
            print(file_id)
        for tag in tag_removal:
            c.execute('SELECT IDs from tagtable where tag = ?', (tag,))
            oldids = c.fetchone()[0]
            ids = oldids.split(', ')
            print(ids)
            ids.remove(str(file_id))
            ids = str(ids)
            exclude = ['[', ']', "'"]
            ids = ids.join(ch for ch in ids if ch not in exclude)
            print(ids)
            c.execute('UPDATE tagtable SET IDs = ? where tag = ?', (ids, tag,))
        conn.commit() 
class search(object):
    def regex(self, tag_idlist, ids, tag):
        tempid = []
        if '~' in tag:
            tag_idlist.extend(ids)
        else:
            for i in tag_idlist:
                if '-' in tag and i in ids:
                    tempid.append(i)
                elif regex == False and i not in ids:
                    tempid.append(i)
            for i in tempid:
                tag_idlist.remove(i)
        return tag_idlist
    
    def results(self, tags):
        global regex
        file_list = []
        tag_idlist = []
        initial = False
        for tag in tags:
            regex = True
            if '~' in tag:
                tagin = tag.replace('~','')
            elif '-' in tag:
                tagin = tag.replace('-','')
            else:
                tagin = tag
                regex = False
            c.execute('SELECT IDs FROM tagtable WHERE tag = ?', (tagin,))
            ids = c.fetchone()[0]
            ids = ids.split(', ')
            if len(ids) == 1 and initial == False:
                tag_idlist = ids
            else:
                if initial == False:
                    tag_idlist.extend(ids)
            tag_idlist = self.regex(tag_idlist, ids, tag)
            initial = True
        print(tag_idlist)
        for file_id in tag_idlist:
            c.execute('SELECT filename FROM IDtable WHERE ROWID = ?', (file_id,))
            filename = c.fetchone()[0]
            file_list.append(filename)
        print(file_list)
        return file_list
                

conn = sqlite3.connect('tags.db') #creates empty db file if it doesn't exist
c = conn.cursor()

if os.stat('tags.db').st_size == 0: #checks if db file has table in it by filesize
    db().create()

