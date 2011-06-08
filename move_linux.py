#!/usr/bin/python
from mover import *

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    
    #f = open('tvshows.txt', 'r')
    #names = f.readlines()
    names = ['How I Met Your Mother', 'Bored to Death', 'The Big Bang Theory', 'The Simpsons', 'Top Gear', 'Mythbusters', 'Big Love', 'Fringe', 'Boardwalk Empire', 'Dexter', 'House', 'Burnistoun', 'Breaking Bad', 'Futurama', 'The IT Crowd']
    #names = ['The Big Bang Theory']
    dir = "/media/Gigant/Downloads/torrent"
    todir = "/media/Gigant/Film/TV-Serier/"
    print 'Moving files from ' + dir + ' to ' + todir
    for name in names:
        print 'Looking for episodes of ' + name
        filepattern = generate_filepattern(name)
        #print("Filepattern: " + str(filepattern))
        #unzip(filepattern, dir)
        for file in locate(filepattern, dir):
            (path, filename) = os.path.split(file)
            #Check if it already exists
            (formatted_name, season, episode, episodename, extension) = get_formatted_name(filename, name)
            print("Formatted name: " + str(formatted_name))
            try:
                newfiles = []
                for newfile in locate(formatted_name, todir + name):
                    newfiles.append(newfile)
                if len(newfiles) == 0:
                #Does not exist, copy the file, rename, then remove it
                    print "Copying " + filename + " to " + todir + name
                    copy_file(file, todir + name)
                        
                    print "Renaming " + filename
                    rename_file(name, filename, todir + name)
                else:
                    print "Exists, apparently...: " + str(newfiles)
            
                #It exists, try to remove the file then
                #print "Removing " + file
                #os.remove(file)
            except OSError as errormsg:
                print "Couldn't handle " + filename + " because %s" % errormsg
                
    
        #Rename all episodes!
        #Bit of a double loop, prevpath makes sure only one pass per directory is done
        #prevpath = ''
        #for file in locate(filepattern, "E:\\Film\\TV-Serier\\Fringe\\"):
            #(path, filename) = os.path.split(file)
            #if prevpath != path:
            #rename_file(name, filename, path)
            #    prevpath = path
