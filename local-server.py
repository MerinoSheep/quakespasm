from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import webbrowser

# Define the custom request handler
class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

# Define the directory you want to serve
directory_to_serve = "C:/Users/bizom/Documents/GitHub/quakespasm/build"
os.chdir(directory_to_serve)

# Define the HTTP server and the port
httpd = HTTPServer(('0.0.0.0', 9999), CustomHTTPRequestHandler)

# Open the default web browser
webbrowser.open_new_tab(f"http://localhost:9999")

# Start the server
print(f"Serving HTTP on port 9999 (http://localhost:9999)...")
httpd.serve_forever()