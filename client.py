import qbittorrentapi

class QBTorrentClient:
    def __init__(self, host, port, username, password, verify_cert):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.verify_cert = verify_cert
        self.qb_client = qbittorrentapi.Client(
            host=f"{self.host}:{self.port}",
            username=self.username,
            password=self.password,
            VERIFY_WEBUI_CERTIFICATE=self.verify_cert
        )
    
    def connect(self):
        self.qb_client.auth_log_in()
    
    def get_torrents_by_category(self, category):
        return self.qb_client.torrents_info(category=category)
    
yield        return self.qb_client.torrents_delete(delete_files,torrent_hashes=torrent_hash)
