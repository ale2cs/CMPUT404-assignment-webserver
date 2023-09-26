#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Resources:
# https://www.geeksforgeeks.org/how-to-convert-bytes-to-string-in-python/
# https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists-2/
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        components = self.data.decode().split()
        request, path, version = components[0], components[1], components[2]
        content_type = path.split('.')[-1]
        ver = 'HTTP/1.1'
        folder = './www'  # only serve files from ./www
        allowed_types = {'html', 'css'}  # supported mime-types for HTML and CSS

        if version == 'HTTP/1.1' and request == 'GET':
            if os.path.isdir(f'{folder}{path}'):  # valid directory
                if path.endswith('/'):
                    # return index.html from directories from paths that end in /
                    with open(f'{folder}{path}index.html', 'r') as f:
                        file_content = f.read()
                    response = f'{ver} 200 OK\nContent-Type: text/html\n\n{file_content}'
                else:
                    response = f'{ver} 301 Moved Permanently\nLocation: {path}/\n\n'
            elif content_type in allowed_types: 
                # return files that are supported
                try:
                    with open(f'{folder}{path}', 'r') as f:
                        file_content = f.read()
                    response = f'{ver} 200 OK\nContent-Type: text/{content_type}\n\n{file_content}'
                except FileNotFoundError:
                    # 404 error for files that don't exist
                    response = f'{ver} 404 Not Found\n\n'
            else:
                # 404 error for invalid directories and unsupported file types
                response = f'{ver} 404 Not Found\n\n'
        elif request != 'GET':
            response = f'{ver} 405 Method Not Allowed\n\n'
        elif version != 'HTTP/1.1':
            response = f'{ver} 505 HTTP Version Not Supported'
        else:
            response = f'{ver} 400 Bad Request\n\n'

        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(response.encode())
         

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
