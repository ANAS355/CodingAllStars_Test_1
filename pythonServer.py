from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi 
from dataclasses import dataclass

hostName = "localhost"
serverPort = 8080

@dataclass
class TestURL:
    url: str = ""
    status: bool = False
    img_status: bool = False
    translation_status: bool = False
    inner_pages_img_status: bool = False
    inner_pages_translation_status: bool = False

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        page = "<html><head><title>https://pythonbasics.org</title></head>"
        page += "<p>Request: %s</p>" % self.path
        page += "<body>"
        page += "<p>This is an example web server.</p>"
        page += "<form method='POST' enctype='multipart/form-data' action='/'>"
        page += "<input name='user_urls' type='text'></input>"
        page += "<button type='submit'>Submit</button>"
        page += "</form>"
        page += "</body></html>"
        self.wfile.write(bytes(page, "utf-8"))

    def do_POST(self):
        print("POST called")
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            user_urls = fields.get("user_urls")[0].split(",")
            user_urls_list = [TestURL(url) for url in user_urls]
            print(user_urls_list)
        self.send_response(301)
        self.send_header("Content-type", "text/html")
        self.send_header("Location", "/")
        self.end_headers()


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")