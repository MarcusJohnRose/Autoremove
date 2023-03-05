import sqlite3
import datetime

class TorrentDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS torrents 
                     (name text, size real, ratio real, added_date text, removed_date text, age_at_removal real, tracker text,category text)''')
        conn.commit()
        conn.close()

    def insert_torrent(self, name,size,ratio,added,removed_on,age_when_removed,tracker,category):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        now = datetime.datetime.now()
        #age_at_removal = (now - datetime.datetime.fromtimestamp(added)).total_seconds() / 3600.0
        c.execute('''INSERT INTO torrents 
                     (name, size, ratio, added_date, removed_date, age_at_removal, tracker,category) 
                     VALUES (?, ?, ?, ?, ?, ?, ?,?)''', 
                  (name, size, ratio, added,removed_on,age_when_removed, tracker,category))
        conn.commit()
        conn.close()

    def update_torrent(self, torrent):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        removed_date = datetime.datetime.now()
        c.execute('''UPDATE torrents SET removed_date=?, age_at_removal=? WHERE name=?''', 
                  (removed_date, (removed_date - datetime.datetime.fromtimestamp(torrent.added_on)).total_seconds() / 3600.0, torrent.name))
        conn.commit()
        conn.close()
