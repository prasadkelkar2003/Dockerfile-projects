from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Hello World from a Hardened Container!")

    # Quiet down standard logging to keep container logs clean
    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    print("Starting secure server on port 8000...", flush=True)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nClean shutdown received. Exiting...", flush=True)
        sys.exit(0)
