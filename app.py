from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import webbrowser, threading, os, json

ROOT = Path(__file__).resolve().parent
HOST = '127.0.0.1'
PORT = int(os.environ.get('SPACE_EVOLUTION_PORT', '8765'))
EXPORT_DIR = ROOT / 'exports'
PROJECT_SAVE_PATH = EXPORT_DIR / 'space-evolution-project.json'
MAX_SAVE_BYTES = 4 * 1024 * 1024

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def do_GET(self):
        if self.path == '/api/health':
            body = json.dumps({'ok': True, 'app': 'sayelf-space-evolution', 'version': '1.0.0'}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/':
            self.path = '/webui/index.html'
        return super().do_GET()
    def do_POST(self):
        if self.path != '/api/save-project':
            self.send_error(404, 'Not found')
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_SAVE_BYTES:
            self.send_error(413, 'Project payload is too large or empty')
            return
        try:
            payload = json.loads(self.rfile.read(length).decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_error(400, 'Invalid project JSON')
            return
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        PROJECT_SAVE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        body = json.dumps({'ok': True, 'path': str(PROJECT_SAVE_PATH), 'filename': PROJECT_SAVE_PATH.name}, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def open_browser():
    webbrowser.open(f'http://{HOST}:{PORT}/')

if __name__ == '__main__':
    print(f'Sayelf Space Evolution v1.0 running at http://{HOST}:{PORT}/')
    print('Press Ctrl+C to stop.')
    threading.Timer(0.8, open_browser).start()
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
