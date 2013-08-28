# This Python file uses the following encoding: utf-8
import os
import hashlib
import Image


class Robohash(object):
    """
    Robohash is a quick way of generating unique avatars for a site.
    The original use-case was to create somewhat memorable images to represent a RSA key.
    """

    def __init__(self,string,hashcount=11):
        """
        Creates our Robohasher
        Takes in the string to make a Robohash out of.
        """
        string = string.encode('utf-8')
        hash = hashlib.sha512()
        hash.update(string)
        self.hexdigest = hash.hexdigest()
        self.hasharray = []
        #Start this at 4, so earlier is reserved
        #0 = Color
        #1 = Set
        #2 = bgset
        #3 = BG
        self.iter = 4
        self._create_hashes(hashcount)
        
        # Get the list of backgrounds and RobotSets
        self.sets = self._listdirs('sets')
        self.bgsets = self._listdirs('backgrounds')

        # Get the colors in set1
        self.colors = self._listdirs('sets/set1')

    def _create_hashes(self,count):
        """
        Breaks up our hash into slots, so we can pull them out later.
        Essentially, it splits our SHA/MD5/etc into X parts.
        """
        for i in range(0,count):
             #Get 1/numblocks of the hash
             blocksize = int(len(self.hexdigest) / count)
             currentstart = (1 + i) * blocksize - blocksize
             currentend = (1 +i) * blocksize
             self.hasharray.append(int(self.hexdigest[currentstart:currentend],16))            

    def _listdirs(self,path):
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    def _get_list_of_files(self,path):
        """
        Go through each subdirectory of `path`, and choose one file from each to use in our hash.
        Continue to increase self.iter, so we use a different 'slot' of randomness each time.
        """

        chosen_files = []

        # Get a list of all subdirectories
        directories = []
        for root, dirs, files in os.walk(path, topdown=False):
            for name in dirs:
                if name[:1] is not '.':
                    directories.append(os.path.join(root, name))

        # Go through each directory in the list, and choose one file from each.
        # Add this file to our master list of robotparts.
        for directory in directories:
            files_in_dir = []
            for imagefile in os.listdir(directory):
                files_in_dir.append(os.path.join(directory,imagefile))

            # Use some of our hash bits to choose which file
            element_in_list = self.hasharray[self.iter] % len(files_in_dir)
            chosen_files.append(files_in_dir[element_in_list])
            self.iter += 1

        return chosen_files

    def assemble(self,roboset=None,format='png',bgset=None,sizex=300,sizey=300):
        """
        Build our Robot!
        Returns the robot image itself.
        """

        # Set a default set for the robot
        if roboset is None:
            roboset = self.sets[0]
        if roboset == 'set1':
            randomcolor = self.colors[self.hasharray[0] % len(self.colors) ]
            roboset = 'set1/' + randomcolor

        # Each directory in our set represents one piece of the Robot, such as the eyes, nose, mouth, etc.

        # Each directory is named with two numbers - The number before the # is the sort order.
        # This ensures that they always go in the same order when choosing pieces, regardless of OS.

        # The second number is the order in which to apply the pieces.
        # For instance, the head has to go down BEFORE the eyes, or the eyes would be hidden.

        # First, we'll get a list of parts of our robot.

        roboparts = self._get_list_of_files('sets/' + roboset)
        # Now that we've sorted them by the first number, we need to sort each sub-category by the second.
        roboparts.sort(key=lambda x: x.split("#")[1])

        if bgset is not None:
                bglist = []
                backgrounds = os.listdir('backgrounds/' + bgset)
                backgrounds.sort()
                for ls in backgrounds:
                        if not ls.startswith("."):
                                bglist.append('backgrounds/' + bgset + "/" + ls)
                background = bglist[self.hasharray[3] % len(bglist)]
    
        # Paste in each piece of the Robot.
        roboimg = Image.open(roboparts[0])
        roboimg = roboimg.resize((1024,1024))
        for png in roboparts:
                img = Image.open(png) 
                img = img.resize((1024,1024))
                roboimg.paste(img,(0,0),img)

        # If we're a BMP, flatten the image.
        if format == 'bmp':
                #Flatten bmps
                r, g, b, a = roboimg.split()
                roboimg = Image.merge("RGB", (r, g, b))
    
        if bgset is not None:
                bg = Image.open(background)
                bg = bg.resize((1024,1024))
                bg.paste(roboimg,(0,0),roboimg)
                roboimg = bg               
                                             
        self.img = roboimg.resize((sizex,sizey),Image.ANTIALIAS) 
        self.format = format

