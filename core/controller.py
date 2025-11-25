from core.view import render_template
from core.session import load_session
import json
from urllib.parse import unquote

class BaseController:
    def __init__(self, request_handler):
        self.req = request_handler
        self.user = load_session(request_handler)

    def render(self, template_name, context=None, status=200):
        render_template(self.req, template_name, context or {}, status)

    def redirect(self, location):
        self.req.send_response(302)
        self.req.send_header('Location', location)
        self.req.end_headers()

    def parse_form(self):
        length = int(self.req.headers.get('Content-Length', 0))
        if length == 0:
            return {}
            
        data = self.req.rfile.read(length).decode('utf-8')
        form_data = {}
        
        for pair in data.split('&'):
            if '=' not in pair:
                continue
                
            key, *value_parts = pair.split('=')
            key = unquote(key.replace('+', ' '))
            value = unquote('='.join(value_parts).replace('+', ' '))
            form_data[key] = value
            
        return form_data

    def json_response(self, data, status=200):
        self.req.send_response(status)
        self.req.send_header('Content-Type', 'application/json')
        self.req.send_header('Access-Control-Allow-Origin', '*')
        self.req.end_headers()
        self.req.wfile.write(json.dumps(data).encode('utf-8'))

    def require_login(self):
        if not self.user:
            self.redirect('/login')
            return False
        return True