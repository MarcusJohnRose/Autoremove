from client import QBTorrentClient
from database import TorrentDatabase
import datetime
import json
import os

absolute_path = os.path.dirname(__file__)

config_file  = "config.json"
# Load config from json file
with open(os.path.join(absolute_path,config_file)) as f:
    config = json.load(f)

# Initialize qBittorrent client
qb_client = QBTorrentClient(
    host=config['host'],
    port=config['port'],
    username=config['username'],
    password=config['password'],
    verify_cert=config['verify_cert']
)
qb_client.connect()

# Initialize database
db = TorrentDatabase(db_file=os.path.join(absolute_path,'torrents.db'))

def check_tracker(list,torrent):
    for tracker in list:
        if tracker["URL"] in torrent.tracker:
            return True
    return False


def get_tracker_rules(list,torrent):
    for tracker in list:
        if tracker["URL"] in torrent.tracker:
            return [tracker["min_ratio"],tracker["min_age"]]


# Get torrents for each category and delete old ones
for category in config['categories']:
    torrents = qb_client.get_torrents_by_category(category)
    category_age_limit_hours = config['categories'][category]['max_age_hours']
    category_min_ratio = config['categories'][category]['min_ratio']
    
    for torrent in torrents:
        ageMet = False
        ratioMet = False
        now = datetime.datetime.now()
        added_on = datetime.datetime.fromtimestamp(torrent.added_on)
        age_in_hours = (now - added_on).total_seconds() / 3600
        
        if  check_tracker(config["trackers"],torrent):
            tracker_miniumss = get_tracker_rules(list,torrent)
            min_age = tracker_miniumss(0)
            min_ratio = tracker_miniumss(1)
        else:
            min_age = category_age_limit_hours
            min_ratio = category_min_ratio

        #Check age vs age limit
        if age_in_hours > min_age:
            ageMet = True 
        
        #Check ratio vs ratio limit
        ratio=torrent.ratio
        if ratio >= min_ratio:
            ratioMet = True
        
        # Delete torrent and save information to database
        if ratioMet and ageMet:
            qb_client.delete_torrent(True,torrent.hash)    
            db.insert_torrent(name=torrent.name,size=torrent.size,ratio=torrent.ratio,added=added_on,removed_on=now,age_when_removed=age_in_hours,tracker=torrent.tracker,category=category)

