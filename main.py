from client import QBTorrentClient
from database import TorrentDatabase
import datetime
import json

# Load config from json file
with open('config.json') as f:
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
db = TorrentDatabase(db_file='torrents.db')

# Get torrents for each category and delete old ones
for category in config['categories']:
    torrents = qb_client.get_torrents_by_category(category)
    age_limit_hours = config['categories'][category]['max_age_hours']
    for torrent in torrents:
        print(torrent)
        now = datetime.datetime.now()
        added_on = datetime.datetime.fromtimestamp(torrent.added_on)
        age_in_hours = (now - added_on).total_seconds() / 3600
        if age_in_hours > age_limit_hours:
            # Delete torrent and save information to database
            db.insert_torrent(
                name=torrent.name,
                size=torrent.size,
                ratio=torrent.ratio,
                added=added_on,
                removed_on=now,
                age_when_removed=age_in_hours,
                tracker=torrent.tracker,
                category=category
            )
            qb_client.delete_torrent(torrent.hash)
