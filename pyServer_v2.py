#!/usr/bin/python3

# MIT License
#
# Copyright (c) 2021
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Programmers:
#             Stanley Switaj - CEO/Lead Programmer
#

import http.server
import socketserver
import os

import urllib

from pathlib import Path
from html import escape

PORT = 8001

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):


    def do_POST(self):
    
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print(f"""POST request,\nPath: {{}}\nHeaders:\n{{}}\n\nBody:\n{{}}\n""".format(
                str(self.path), str(self.headers), post_data.decode('utf-8')))

        html = ''
        #html = "POST request for {}\n".format(self.path)
        #content = json.loads( post_data.decode('utf-8') )
        html = post_data.decode('utf-8')

        headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0' }
        content = requests.get(website_url, headers=headers)
        
        if content.status_code == 200:
            pass    

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(html))
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
        
        #return  http.server.SimpleHTTPRequestHandler.do_POST(self)



    def do_GET(self):
        
        video_name = ''
        video_val = ''
        
        if self.path.find('?'):
            idx = self.path.find('?')
            para = escape(self.path[idx+1:])
        
        
            if para.find('='):
                idx = para.find('=')
                video_name = para[:idx]
                video_val = para[idx+1:]
        

        if (video_name != '' and video_val != ''):

            video = urllib.parse.unquote(video_val)
        
            image_path = str(Path(video).parent)
            image_name = str(Path(video).stem)
            image =  image_path + '/' + image_name + '.png'

            os.system(f"""xplayer-video-thumbnailer '{video}' '{image}' > /dev/null 2>&1 """)            
            
            html = ''
        
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(html))
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        #return  http.server.SimpleHTTPRequestHandler.do_GET(self)

handler_object = MyHttpRequestHandler


def server_run():

    try:
        with socketserver.TCPServer(("127.0.0.1", PORT), handler_object, bind_and_activate=False) as server:
            print('Starting Python Web Server... ( CTRL+C to stop )')
            server.allow_reuse_address = True
            server.server_bind()
            server.server_activate()
            server.serve_forever()
            
    except ConnectionResetError:
        server_run()
    finally:
        print('exit server')

server_run()


