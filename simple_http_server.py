import ssl

try:
    from BaseHTTPServer import HTTPServer
except:
    from http.server import HTTPServer

try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except:
    from http.server import SimpleHTTPRequestHandler

if __name__ == '__main__':
    httpd = HTTPServer(('', 443), SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='./cert.pem', keyfile='./key.pem', ssl_version=ssl.PROTOCOL_TLSv1)
    httpd.serve_forever()
