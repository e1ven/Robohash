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
import robohash
import os
import pprint
import Image
import hashlib
import urllib

try: 
   from hashlib import md5 as md5_func
except ImportError:
   from md5 import new as md5_func


class Robohash(object):
   def __init__(self,string):
       hash = hashlib.sha512()
       hash.update(string)
       self.hexdigest = hash.hexdigest()
       self.hasharray = []

   def createHashes(self,count):
       #Create and store a series of hash-values
       #Basically, split up a hash (SHA/md5/etc) into X parts
       for i in range(0,count):
           #Get 1/numblocks of the hash
           blocksize = (len(self.hexdigest) / count)
           currentstart = (1 + i) * blocksize - blocksize
           currentend = (1 +i) * blocksize
           self.hasharray.append(int(self.hexdigest[currentstart:currentend],16))            

   def dirCount(self,path):
       #return the count of just the directories beneath me.
       return sum([len(dirs) for (root, dirs, files) in os.walk(path)])

   def getHashList(self,map):
       #Kinda a complicated function. 
       #Basically, we're recursively calling ourselves, and keeping track of the depth
       #Since we use two return values, we're storing them in a map.
       #Each iteration, if we hit a directory, recurse
       #If not, choose the appropriate file, given the hashes, stored above
       path = map['path']
       depth = map['depth']
       completelist = []
       locallist = []
       for ls in os.listdir(path):
           if not ls.startswith("."):
               if os.path.isdir(path + "/" + ls):
                   returnval = self.getHashList({'path': path + "/" + ls ,'depth': depth + 1})
                   subfiles = returnval['completelist']
                   if subfiles is not None:
                       completelist = completelist + subfiles
               else:
                   locallist.append( path + "/" + ls)

       if len(locallist) > 0:
           elementchoice = self.hasharray[map['depth']] % len (locallist)
           luckyelement = locallist[elementchoice]
           locallist = []
           locallist.append(luckyelement)    

       completelist = completelist + locallist   
       return {'completelist':completelist,'depth':depth}





class ImgHandler(tornado.web.RequestHandler):
    def get(self,string=None):
        self.content_type = 'application/json'
        #Create a hash for the string as given
        if string is None:
            string = self.request.remote_ip
        string = urllib.quote_plus(string)
        r = Robohash(string)
        r.createHashes(r.dirCount("blue"))
        
        #Change to a usuable format
        if string.endswith(('.png','.gif','.jpg','bmp','im','jpeg','pcx','ppm','tiff','xbm')):
            ext = string[string.rfind('.') +1 :len(string)] 
        else:
            ext = "png"
        self.set_header("Content-Type", "image/" + ext)
        hashlist = r.getHashList({'path':"blue",'depth':0})['completelist']
        hashlist.sort()
        pprint.pprint(hashlist)
        robohash = Image.open(hashlist[0])
        for png in hashlist:
            img = Image.open(png) 
            robohash.paste(img,(0,0),img)
        robohash.save(self,format=ext)
        # self.write("Running in Random mode:<br>")
        # self.write("<img src='/images/" + string + "'>")

application = tornado.web.Application([
    (r"/images/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__),
    "static/images")}),

    (r"/", ImgHandler),
    (r"/(.*)", ImgHandler),

])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
