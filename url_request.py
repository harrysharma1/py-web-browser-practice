import socket
import ssl
import test

class URL:
    def __init__(self,url):
        # scheme  hostname    path
        # http://example.org/index.html
    
        self.scheme, url=url.split("://", 1)
        assert self.scheme in ["http","https"]
        if "/" not in url:
            url = url+"/"
        self.host, url = url.split("/", 1)
        self.path = "/"+ url
        
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443
        
        if ":" in self.host:
            self.host, port = self.host.split(":",1)
            self.port = int(port)


    
    """
    Sends http request for resource to server and displays body
    """
    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        
        # Connect to host through port 80 if http or port 443 if https
        s.connect((self.host,self.port))
        
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        
        # Make request to url
        s.send(("GET {} HTTP/1.0\r\n".format(self.path) + \
                "Host: {}\r\n\r\n".format(self.host)) \
               .encode("utf8"))

        # Get server response to request
        response = s.makefile("r", encoding="utf-8", newline="\r\n")
        
        statusline = response.readline()
        version, status, explaination = statusline.split(" ", 2)
        # print(f'version:{version}')
        # print(f'status:{status}')
        # print(f'explaination:{explaination}')
        
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
            response_headers['http-version'] = version
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        
        body = response.read()
        s.close()
        
        return body
    
def show(body):
        in_tag = False 
        for c in body:
            if c == "<":
                in_tag = True
            elif c == ">":
                in_tag = False
            elif not in_tag:
                print(c,end="")
    
def load(url):
        body = url.request()
        show(body)

"""
Local testing for show function using AREPL
"""
# show("he<body>llo</body>")
# show('he<body>llo</body>')
# show('he<body>l</body>lo')
# show('he<body>l<div>l</div>o</body>')
# show('he<body>l</div>lo')
# show('he<body>l<div>l</body>o</div>')

"""
Testing to see if the URL class's member variables show the correct thing
"""
# url_a = "http://test.test:90"
# a = URL(url_a)
# print(f"url: {url_a}")
# print(f"URL(scheme={a.scheme}, host={a.scheme}, port={a.port}, path='{a.path}')")

# print("\n")

# url_b = "http://test.test"
# b = URL(url_b)
# print(f"url: {url_b}")
# print(f"URL(scheme={b.scheme}, host={b.scheme}, port={b.port}, path='{b.path}')")

# print("\n")

# url_c = "http://test.test/example1"
# c = URL(url_c)
# print(f"url: {url_c}")
# print(f"URL(scheme={c.scheme}, host={c.scheme}, port={c.port}, path='{c.path}')")



"""
Testing to see if requests work as expected
"""

# url = "http://test.test/example1"
# a = URL(url)
# print(a.request())


if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))

            
            
        