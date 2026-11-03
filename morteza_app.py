"""Small DevSecOps demonstration service. Python 3.11+."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def response(path):
    if path == '/health':
        return 200, {'status': 'ok', 'service': 'devsecops-platform-lab'}
    return 404, {'error': 'not_found'}


class Handler(BaseHTTPRequestHandler):
    server_version = 'PortfolioLab'
    sys_version = ''

    def do_GET(self):
        status, data = response(self.path.split('?', 1)[0])
        payload = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'none'; frame-ancestors 'none'")
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(payload)


if __name__ == '__main__':
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '8080'))
    print(f'Listening on http://{host}:{port}', flush=True)
    ThreadingHTTPServer((host, port), Handler).serve_forever()
