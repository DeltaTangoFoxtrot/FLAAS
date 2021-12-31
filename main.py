from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
from urllib.parse import urlparse, parse_qs, unquote_plus
import time
import json
import os.path
import socket
import ssl

hostName = "localhost"
hostPort = 8080

if os.path.isfile("config.json"):
    with open("config.json") as f:
        data = json.load(f)
        hostName = data.get("hostName", "localhost")
        hostPort = data.get("hostPort", 8080)
        certificate = data.get("certificate",None)
        key = data.get("key",None)

def GetRedirectScript(link):
    if link == "":
        return ""
    return "<script type=\"text/javascript\"> window.location.replace(\"" + link + "\")  </script>"

def GetMetadata(getParams):
    title = getParams.get("t", "You Fell For It Fool")
    image = getParams.get("i", "https://i.imgur.com/z5ux7q9.png")
    description = getParams.get("d", "Thunder Cross Split Attack")
    redirect = getParams.get("r", "")
    url = getParams.get("u", hostName)
    postType = "Article"

    if isinstance(title, list):
        if len(title) == 1:
            title = title[0]
        else:
            title = "Whoopsy Daisy Title"
    if isinstance(image, list):
        if len(image) == 1:
            image = image[0]
        else:
            image = "Whoopsy Daisy Image"
    if isinstance(description, list):
        if len(description) == 1:
            description = description[0]
        else:
            description = "Whoopsy Daisy Image"
    if isinstance(redirect, list):
        if len(redirect) == 1:
            redirect = redirect[0]
        else:
            redirect = "Whoopsy Daisy Redirect"
    if isinstance(url, list):
        if len(url) == 1:
            url = url[0]
        else:
            url = "Whoopsy Daisy Redirect"
    title = unquote_plus(title)
    image = unquote_plus(image)
    description = unquote_plus(description)
    url = unquote_plus(url)
    portType = unquote_plus(postType)
    return title, image, description, url, postType, redirect

class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        return self.do_GET()
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        getParams = parse_qs(urlparse(self.path).query)
        title, image, description, url, postType, redirect = GetMetadata(getParams)
        self.wfile.write(bytes("<html><head>", "utf-8"))
        self.wfile.write(bytes("<meta property='og:title' content='" + title + "' />", "utf-8"))
        self.wfile.write(bytes("<meta property='og:image' content='" + image + "' />", "utf-8"))
        self.wfile.write(bytes("<meta property='og:description' content='" + description + "' />", "utf-8"))
        self.wfile.write(bytes("<meta property='og:url' content='" + url + "' />", "utf-8"))
        self.wfile.write(bytes("<meta property='og:type' content='" + postType + "' />", "utf-8"))
        self.wfile.write(bytes("</head>", "utf-8"))
        self.wfile.write(bytes("<body><img src='https://i.imgur.com/z5ux7q9.png' alt='You fell for it fool' style='max-width: 100vw;max-height: 100vh;' />", "utf-8"))
        self.wfile.write(bytes(GetRedirectScript(redirect), "utf-8"))   
        self.wfile.write(bytes("</body></html>", "utf-8"))

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == "__main__":
    myServer = ThreadingSimpleServer((hostName, hostPort), MyServer)
    if certificate and key:
        myServer.socket = ssl.wrap_socket(myServer.socket, key, certificate, server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2, ca_certs=None, do_handshake_on_connect=True, suppress_ragged_eofs=True, ciphers='ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!3DES:!MD5:!PSK')
    print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
