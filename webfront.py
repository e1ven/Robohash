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
from tornado.options import define, options
try: 
   from hashlib import md5 as md5_func
except ImportError:
   from md5 import new as md5_func

define("port", default=80, help="run on the given port", type=int)

class Robohash(object):
   def __init__(self,string):
       hash = hashlib.sha512()
       hash.update(string)
       self.hexdigest = hash.hexdigest()
       self.hasharray = []
       #Start this at 3, so earlier is reserved
       #0 = Color
       #1 = Set
       #2 = bgset
       #3 = BG
       self.iter = 4
                     
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
        
        robo = [
"""
             ,     ,
             (\\____/)
              (_oo_)
                (O)
              __||__    \\)
           []/______\\[] /
           / \\______/ \\/
          /    /__\\
         (\\   /____\\ """,
"""
                 _______
               _/       \\_
              / |       | \\
             /  |__   __|  \\
            |__/((o| |o))\\__|
            |      | |      |
            |\\     |_|     /|
            | \\           / |
             \\| /  ___  \\ |/
              \\ | / _ \\ | /
               \\_________/
                _|_____|_
           ____|_________|____
          /                   \\  -- Mark Moir

 
""",
"""                     .andAHHAbnn.
                     .aAHHHAAUUAAHHHAn.
                    dHP^~"        "~^THb.
              .   .AHF                YHA.   .
              |  .AHHb.              .dHHA.  |
              |  HHAUAAHAbn      adAHAAUAHA  |
              I  HF~"_____        ____ ]HHH  I
             HHI HAPK""~^YUHb  dAHHHHHHHHHH IHH
             HHI HHHD> .andHH  HHUUP^~YHHHH IHH
             YUI ]HHP     "~Y  P~"     THH[ IUP
              "  `HK                   ]HH'  "
                  THAn.  .d.aAAn.b.  .dHHP
                  ]HHHHAAUP" ~~ "YUAAHHHH[
                  `HHP^~"  .annn.  "~^YHH'
                   YHb    ~" "" "~    dHF
                    "YAb..abdHHbndbndAP"
                     THHAAb.  .adAHHF
                      "UHHHHHHHHHHU"
                        ]HHUUHHHHHH[
                      .adHHb "HHHHHbn.
               ..andAAHHHHHHb.AHHHHHHHAAbnn..
          .ndAAHHHHHHUUHHHHHHHHHHUP^~"~^YUHHHAAbn.
            "~^YUHHP"   "~^YUHHUP"        "^YUP^"
                 ""         "~~"
""",
"""                                 /~@@~\\,
                  _______ . _\\_\\___/\\ __ /\\___|_|_ . _______
                 / ____  |=|      \\  <_+>  /      |=|  ____ \\
                 ~|    |\\|=|======\\\\______//======|=|/|    |~
                  |_   |    \\      |      |      /    |    |
                   \\==-|     \\     |  2D  |     /     |----|~~)
                   |   |      |    |      |    |      |____/~/
                   |   |       \\____\\____/____/      /    / /
                   |   |         {----------}       /____/ /
                   |___|        /~~~~~~~~~~~~\\     |_/~|_|/
                    \\_/        [/~~~~~||~~~~~\\]     /__|\\
                    | |         |    ||||    |     (/|[[\\)
                    [_]        |     |  |     |
                               |_____|  |_____|
                               (_____)  (_____)
                               |     |  |     |
                               |     |  |     |
                               |/~~~\\|  |/~~~\\|
                               /|___|\\  /|___|\\
                              <_______><_______>""",
"""                                      _____
                                        /_____\\
                                   ____[\\`---'/]____
                                  /\\ #\\ \\_____/ /# /\\
                                 /  \\# \\_.---._/ #/  \\
                                /   /|\\  |   |  /|\\   \\
                               /___/ | | |   | | | \\___\\
                               |  |  | | |---| | |  |  |
                               |__|  \\_| |_#_| |_/  |__|
                               //\\\\  <\\ _//^\\\\_ />  //\\\\
                               \\||/  |\\//// \\\\\\\\/|  \\||/
                                     |   |   |   |
                                     |---|   |---|
                                     |---|   |---|
                                     |   |   |   |
                                     |___|   |___|
                                     /   \\   /   \\
                                    |_____| |_____|
                                    |HHHHH| |HHHHH|
                              """, 
"""                                        ()               ()
                                            \\             /
                                           __\\___________/__
                                          /                 \\
                                         /     ___    ___    \\
                                         |    /   \\  /   \\   |
                                         |    |  H || H  |   |
                                         |    \\___/  \\___/   |
                                         |                   |
                                         |  \\             /  |
                                         |   \\___________/   |
                                         \\                   /
                                          \\_________________/
                                         _________|__|_______
                                       _|                    |_
                                      / |                    | \\
                                     /  |            O O O   |  \\
                                     |  |                    |  |
                                     |  |            O O O   |  |
                                     |  |                    |  |
                                     /  |                    |  \\
                                    |  /|                    |\\  |
                                     \\| |                    | |/
                                        |____________________|
                                           |  |        |  |
                                           |__|        |__|
                                          / __ \\      / __ \\
                                          OO  OO      OO  OO
                              """]
                              
        self.write(self.render_string('templates/root.html',ip=ip,robo=random.choice(robo)))

class ImgHandler(tornado.web.RequestHandler):
    def get(self,string=None):
        
        colors = ['blue','brown','green','grey','orange','pink','purple','red','white','yellow']
        sets = ['set1','set2','set3']
        bgsets = ['bg1','bg2']
        
        #Create a hash for the string as given
        if string is None:
            string = self.request.remote_ip
        string = urllib.quote_plus(string)
        r = Robohash(string)
          
        #Create 10 hashes. This should be long enough for the current crop of variables.
        #This is probably not insecure, sicne we'd be modding anyway. This just spreads it out more.
        r.createHashes(11)
        
        
                
        #Now, customize the request if possible.
        client_color = ""
        client_set = ""
        client_bgset = ""
        sizex = 300
        sizey = 300
        
        if "size" in self.request.arguments:
            sizelist = self.get_argument("size").split(tornado.escape.xhtml_escape("x"),3)
            if ((int(sizelist[0]) > 0) and (int(sizelist[0]) < 4096)):
                sizex = int(sizelist[0])
            if ((int(sizelist[0]) > 0) and (int(sizelist[0]) < 4096)):
                sizey = int(sizelist[1])        
            
        if "set" in self.request.arguments:
            if tornado.escape.xhtml_escape(self.get_argument("set")) == 'any':
                client_set = sets[r.hasharray[1] % len(sets) ]
            if self.get_argument("set") in sets:
                client_set =  tornado.escape.xhtml_escape(self.get_argument("set"))  
        else:
            #If no set specified, you get set 1
            client_set = "set1"
            
        
        if client_set == 'set1':
            client_set = colors[r.hasharray[0] % len(colors) ]    
            
        if "color" in self.request.arguments:
                if self.get_argument("color") in colors:
                    client_set = tornado.escape.xhtml_escape(self.get_argument("color"))
                    
        if "bgset" in self.request.arguments:
            if self.get_argument("bgset") in bgsets:
                client_bgset = tornado.escape.xhtml_escape(self.get_argument("bgset"))
            else:
                client_bgset = bgsets[r.hasharray[2] % len(bgsets) ]

                                
                                
        #If they don't specify a color, use hashvalue        
        if ((client_color == "") and (client_set == "")):
            client_set = colors[r.hasharray[0] % len(colors) ]
        
        
        #Change to a usuable format
        if string.endswith(('.png','.gif','.jpg','.bmp','.im','.jpeg','.pcx','.ppm','.tiff','.xbm','tif')):
            ext = string[string.rfind('.') +1 :len(string)] 
            if ext.lower() == 'jpg':
                ext = 'jpeg'            
            if ext.lower() == 'tif':
                ext = 'tiff'
        else:
            ext = "png"
        self.set_header("Content-Type", "image/" + ext)
        hashlist = r.getHashList(client_set)
        hashlist.sort()
        robohash = Image.open(hashlist[0])
        robohash = robohash.resize((1024,1024))
        for png in hashlist:
            img = Image.open(png) 
            img = img.resize((1024,1024))
            robohash.paste(img,(0,0),img)
        if ext == 'bmp':
            #Flatten bmps
            r, g, b, a = robohash.split()
            robohash = Image.merge("RGB", (r, g, b))
        
        if client_bgset is not "":
            bglist = []
            for ls in os.listdir(client_bgset).sort():
                if not ls.startswith("."):
                    bglist.append(client_bgset + "/" + ls)
            bg = Image.open(bglist[r.hasharray[3] % len(bglist)])
            bg = bg.resize((1024,1024))
            bg.paste(robohash,(0,0),robohash)
            robohash = bg               
                           
        robohash = robohash.resize((sizex,sizey),Image.ANTIALIAS)    
        robohash.save(self,format=ext)





def main():
    tornado.options.parse_command_line()
    # timeout in seconds
    timeout = 10
    socket.setdefaulttimeout(timeout)

    settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "9b90a85cfe46cad5ec136ee44a3fa332",
    "login_url": "/login",
    "xsrf_cookies": True,
    }

    application = tornado.web.Application([
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__),
        "static/")}),
        (r"/", MainHandler),
        (r"/(.*)", ImgHandler),
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application,xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
