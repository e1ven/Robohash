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
import md5
import pprint
import Image
import hashlib
import urllib
import random 
import urllib2
from tornado.options import define, options
try: 
   from hashlib import md5 as md5_func
except ImportError:
   from md5 import new as md5_func
import cStringIO

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
       listdir = os.listdir(path)
       listdir.sort()
       for ls in listdir:
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
        # string = urllib.quote_plus(string)
        
        if "ignoreext" in self.request.arguments:
            client_ignoreext = tornado.escape.xhtml_escape(self.get_argument("ignoreext"))
        else:
            client_ignoreext = None
            
            
        #Change to a usuable format
        if string.endswith(('.png','.gif','.jpg','.bmp','.jpeg','.ppm','.datauri')):
            ext = string[string.rfind('.') +1 :len(string)] 
            if ext.lower() == 'jpg':
                ext = 'jpeg'            
        else:
            ext = "png"
            
            
        if client_ignoreext != "false":
            if string.endswith(('.png','.gif','.jpg','.bmp','.jpeg','.ppm','.datauri')):
                string = string[0:string.rfind('.')]
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
            
            
            
        if "gravatar" in self.request.arguments:    
            if tornado.escape.xhtml_escape(self.get_argument("gravatar")) == 'yes':
                default = "404"
                # construct the url
                gravatar_url = "https://secure.gravatar.com/avatar/" + hashlib.md5(string.lower()).hexdigest() + "?"
                gravatar_url += urllib.urlencode({'default':default, 'size':str(sizey)})
            if tornado.escape.xhtml_escape(self.get_argument("gravatar")) == 'hashed':
                string = urllib.quote(string)
                default = "404"
                # construct the url
                gravatar_url = "https://secure.gravatar.com/avatar/" + string + "?"
                gravatar_url += urllib.urlencode({'default':default, 'size':str(sizey)})
            try:
                f = urllib2.urlopen(urllib2.Request(gravatar_url))
                self.redirect(gravatar_url, permanent=False)  
                return 0
            except:
              badGravatar = True
  
        if "set" in self.request.arguments:
            if tornado.escape.xhtml_escape(self.get_argument("set")) == 'any':
                client_set = sets[r.hasharray[1] % len(sets) ]
            if self.get_argument("set") in sets:
                client_set =  tornado.escape.xhtml_escape(self.get_argument("set"))  
        else:
            #If no set specified, you get set 1
            client_set = "set1"
        
        ##Let people define multiple sets, so I can add more.
        if "sets" in self.request.arguments:
            newsets = tornado.escape.xhtml_escape(self.get_argument("sets")).split(",");
            replaceset = []
            for s in newsets:
                if s in sets:
                    replaceset.append(s)
            client_set = replaceset[r.hasharray[1] % len(replaceset) ]

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
        
        

        self.set_header("Content-Type", "image/" + ext)
        hashlist = r.getHashList(client_set)

        #OK, here's where we do some creative sorting.
        #Basically, we have two integers before every file
        #The first one ensure FS order, which is necessary to match the RH.org server
        #The second one ensures build order.
        #The FS order is only necessary during picking elements. Now, we want the second sort
        #So create a new list, ordered by the second integer
        hlcopy = []
        for element in hashlist:
            element = element[0:element.find("/",element.find("#") -4) +1] + element[element.find("#") +1:len(element)]
            hlcopy.append(element)
        #Now, combine them into tuples, and sort. A tuples list always sorts by the FIRST element.
        duality = zip(hlcopy,hashlist)
        duality.sort()
        pprint.pprint(duality)
        hlcopy,hashlist = zip(*duality)
        pprint.pprint(hlcopy)
        print "------"
        pprint.pprint(hashlist)

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
            backgrounds = os.listdir(client_bgset)
            backgrounds.sort()
            for ls in backgrounds:
                if not ls.startswith("."):
                    bglist.append(client_bgset + "/" + ls)
            bg = Image.open(bglist[r.hasharray[3] % len(bglist)])
            bg = bg.resize((1024,1024))
            bg.paste(robohash,(0,0),robohash)
            robohash = bg               
                           
        robohash = robohash.resize((sizex,sizey),Image.ANTIALIAS)    
        if ext != 'datauri':
          robohash.save(self,format=ext)
        else:
          fakefile = cStringIO.StringIO()
          robohash.save(fakefile,format='jpeg')
          fakefile.seek(0)
          data_uri = fakefile.read().encode("base64").replace("\n", "")
          self.write("data:image/jpeg;base64," + data_uri)






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
        (r'/(crossdomain\.xml)', tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__),
        "static/")}),
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
