from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        with open('received_binary', 'wb') as f:
            f.write(body)
        self.send_response(200)
        self.end_headers()

httpd = HTTPServer(('', 8000), Handler)
httpd.serve_forever()
