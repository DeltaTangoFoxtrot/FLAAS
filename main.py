from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote_plus
import time
import json
import os.path

hostName = "localhost"
hostPort = 8080

if os.path.isfile("config.json"):
    with open("config.json") as f:
        data = json.load(f)
        hostName = data.get("hostName", "localhost")
        hostPort = data.get("hostPort", 8080)

def GetMetadata(getParams):
    title = getParams.get("t", "You Fell For It Fool")
    image = getParams.get("i", "https://i.imgur.com/z5ux7q9.png")
    description = getParams.get("d", "Thunder Cross Split Attack")
    url = ""
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
    title = unquote_plus(title)
    image = unquote_plus(image)
    description = unquote_plus(description)
    url = unquote_plus(url)
    portType = unquote_plus(postType)
    return title, image, description, url, postType

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        getParams = parse_qs(urlparse(self.path).query)
        title, image, description, url, postType = GetMetadata(getParams)
        self.wfile.write(bytes("<html><head>", "utf-8"))
        self.wfile.write(bytes("<meta property='og:title' content='" + title + "' />", "utf-8"))
        self.wfile.write(bytes("<meta property='og:image' content='" + image + "' />", "utf-8"))
        self.wfile.write(bytes("<meta property='og:description' content='" + description + "' />", "utf-8"))
        self.wfile.write(bytes("<meta property='og:url' content='" + url + "' />", "utf-8"))
        self.wfile.write(bytes("<meta property='og:type' content='" + postType + "' />", "utf-8"))
        self.wfile.write(bytes("</head>", "utf-8"))
        self.wfile.write(bytes("<body><img src='https://i.imgur.com/z5ux7q9.png' alt='You fell for it fool' style='max-width: 100vw;max-height: 100vh;' />", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    myServer = HTTPServer((hostName, hostPort), MyServer)
    print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
