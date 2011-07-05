import Image
import os,sys,random
import pprint



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
    
    

#Generate a robohash-
hashlist = getPNG(random.choice(['blue','brown','green','orange','grey','pink','purple','red','white','yellow']))
hashlist.sort()
pprint.pprint(hashlist)
robohash = Image.open(hashlist[0])
for png in hashlist:
    img = Image.open(png) 
    # robohash = Image.composite(robohash,img,.1)
    robohash.paste(img,(0,0),img)

robohash.save("out.png")


