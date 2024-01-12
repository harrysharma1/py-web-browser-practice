import socket

class URL:
    def __init__(self,url):
        # scheme  hostname    path
        # http://example.org/index.html
    
        self.scheme, url=url.split("://", 1)
        assert self.scheme == "http"

        if "/" not in url:
            url = url+"/"
            
        self.host, url = url.split("/", 1)
        self.path = "/"+ url
    
    def request(self):
        # 
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host,80))
        