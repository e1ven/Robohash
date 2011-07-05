#!/usr/bin/env python
#
# Copyright 2011 Pluric
    

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import socket
import re
import os 
import pprint
import Image
import random

try: 
   from hashlib import md5 as md5_func
except ImportError:
   from md5 import new as md5_func

def getPNG(path):
    completelist = []
    locallist = []
    for ls in os.listdir(path):
        if not ls.startswith("."):
            if os.path.isdir(path + "/" + ls):
                subfiles = getPNG(path + "/" + ls)
                if subfiles is not None:
                    completelist = completelist + subfiles
            else:
                locallist.append( path + "/" + ls)
    
    if len(locallist) > 0:
        luckyelement = locallist[random.randrange(0,len(locallist))]
        locallist = []
        locallist.append(luckyelement)    
        
    completelist = completelist + locallist            
    return completelist
    
    

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #Generate a robohash-
        hashlist = getPNG(random.choice(['blue','brown','green','orange','grey','pink','purple','red','white','yellow']))
        hashlist.sort()
        robohash = Image.open(hashlist[0])
        for png in hashlist:
            img = Image.open(png) 
            robohash.paste(img,(0,0),img)
        robohash.save("static/images/out.png")
        self.write("Running in Random mode:<br>")
        self.write("<img src='/images/out.png'>")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/images/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__),
    "static/images")}),

])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
