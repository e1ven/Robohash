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
import hashlib
import urllib
import random 
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
       self.iter = 1
                     
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

   def getHashList(self,path):
       #Each iteration, if we hit a directory, recurse
       #If not, choose the appropriate file, given the hashes, stored above
       
       completelist = []
       locallist = []
       for ls in os.listdir(path):
           if not ls.startswith("."):
               if os.path.isdir(path + "/" + ls):
                   subfiles  = self.getHashList(path + "/" + ls)
                   if subfiles is not None:
                       completelist = completelist + subfiles
               else:
                   locallist.append( path + "/" + ls)

       if len(locallist) > 0:
           elementchoice = self.hasharray[self.iter] % len(locallist)
           luckyelement = locallist[elementchoice]
           locallist = []
           locallist.append(luckyelement)    
           self.iter += 1
           

       completelist = completelist + locallist   
       return completelist



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        ip = self.request.remote_ip
        self.write(self.render_string('templates/root.html',ip=ip))

class ImgHandler(tornado.web.RequestHandler):
    def get(self,string=None):
        
        colors = ['blue','brown','green','grey','orange','pink','purple','red','white','yellow']
        sets = ['set1','set2','set3']
        
        self.content_type = 'application/json'
        #Create a hash for the string as given
        if string is None:
            string = self.request.remote_ip
        string = urllib.quote_plus(string)
        r = Robohash(string)
          
        #Create 10 hashes. This should be long enough for the current crop of variables.
        #This is probably not insecure, sicne we'd be modding anyway. This just spreads it out more.
        r.createHashes(10)
        
        
        #Now, customize the request if possible.
        client_color = ""
        if "color" in self.request.arguments:
                if self.get_argument("color") in colors:
                    client_set = tornado.escape.xhtml_escape(self.get_argument("color"))
                    
        #If they don't specify a color, use hashvalue        
        if client_color == "":
            client_set = colors[r.hasharray[0] % len(colors) ]
          
        if "set" in self.request.arguments:
                if self.get_argument("set") in sets:
                    client_set =  tornado.escape.xhtml_escape(self.get_argument("set"))   
                    #Set one is distributed     
                    if client_set == 'set1':
                        client_set = colors[r.hasharray[0] % len(colors) ]
        
        
        #Change to a usuable format
        if string.endswith(('.png','.gif','.jpg','bmp','im','jpeg','pcx','ppm','tiff','xbm')):
            ext = string[string.rfind('.') +1 :len(string)] 
            if ext == '.jpg':
                ext = '.jpeg'            
        else:
            ext = "png"
        self.set_header("Content-Type", "image/" + ext)
        hashlist = r.getHashList(client_set)
        hashlist.sort()
        robohash = Image.open(hashlist[0])
        for png in hashlist:
            img = Image.open(png) 
            robohash.paste(img,(0,0),img)
        if ext == 'bmp':
            #Flatten bmps
            r, g, b, a = robohash.split()
            robohash = Image.merge("RGB", (r, g, b))
        robohash.save(self,format=ext)

application = tornado.web.Application([
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__),
    "static/")}),

    (r"/", MainHandler),
    (r"/(.*)", ImgHandler),

])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
