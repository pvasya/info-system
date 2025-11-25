from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import unquote
from core.router import Router

class RequestHandler(BaseHTTPRequestHandler):
    router = Router()

    def do_GET(self):
        from config import STATIC_DIR
        if self.path.startswith(STATIC_DIR):
            self.serve_static()
        else:
            self.router.handle(self)

    def do_POST(self):
        self.router.handle(self)

    def serve_static(self):
        filepath = unquote(self.path.lstrip('/')) 
        full_path = os.path.join(os.getcwd(), filepath)

        if os.path.exists(full_path) and os.path.isfile(full_path):
            self.send_response(200)
            self.send_header('Content-type', self.guess_type(full_path))
            self.end_headers()
            with open(full_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'File Not Found')

    def guess_type(self, path):
        if path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.jpg') or path.endswith('.jpeg'):
            return 'image/jpeg'
        elif path.endswith('.png'):
            return 'image/png'
        elif path.endswith('.svg'):
            return 'image/svg+xml'
        return 'application/octet-stream'

if __name__ == '__main__':
    from config import HOST, PORT
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f"Server running at http://{HOST}:{PORT}")
    server.serve_forever()
