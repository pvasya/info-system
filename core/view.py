from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

def render_template(request_handler, template_name, context, status=200):
    content = env.get_template(template_name).render(**context)
    request_handler.send_response(status)
    request_handler.send_header('Content-type', 'text/html; charset=utf-8')
    request_handler.end_headers()
    request_handler.wfile.write(content.encode('utf-8'))