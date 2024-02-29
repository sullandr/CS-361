import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000
HOST = 'localhost'

class myHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print ("GET request received")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path == '/req':
            self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>", "utf-8"))
            self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))
            self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    myServer = HTTPServer((HOST, PORT), myHandler)

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()