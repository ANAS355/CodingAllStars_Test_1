from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    requestPath = self.path
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write("requested path: " + requestPath)


httpServer = HTTPServer(('127.0.0.1', 8080), RequestHandler)
httpServer.serve_forever()