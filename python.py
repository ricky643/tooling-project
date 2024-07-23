from http.server import HTTPServer, BaseHTTPRequestHandler

# Class inherits from BaseHTTPRequestHandler
class helloHandler(BaseHTTPRequestHandler):
    # Handle all GET requests
    def do_GET(self):
        # First thing, send back a response
        # 200 means the file has been found and it can serve the webpage 
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        # Must close the headers
        self.end_headers()
        # Writes to the page
        # For HTTP servers, cannot send strings directly, encode method encodes string into bytes and serves onto webpage as a string
        self.wfile.write("Hello Ricardo".encode())
 
    

if __name__ == '__main__':
    PORT = 8000
    # Instance of HTTPServer class
    # Takes in two arguments: tuple which contains hostname (going to be served on localhost)
    # Takes in the port number
    # Second argument is the request handler
    server = HTTPServer(('', PORT), helloHandler)
    print("Server running on port %s" % PORT)
    server.serve_forever()
