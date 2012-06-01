#!/usr/bin/python
from mover import *
import sys
if __name__ == '__main__':
    if len(sys.argv) < 2:
        names = ['How I Met Your Mother', 'The Big Bang Theory', 'The Simpsons', 'Fringe', 'Futurama', 'Top Gear']
    else:
        names = []
        for show in sys.argv[1:]:
            names.append(show)
    print("Shows: " + str(names))
    fromdir = "/media/Gargant/Downloads/torrent"
    todir = "/media/Gargant/Film/TV-Serier/"
    print 'Moving files from ' + fromdir + ' to ' + todir
    for name in names:
        print '\nLooking for episodes of ' + name
        filepattern = generate_filepattern(name)
        for filepath in locate(filepattern, fromdir):
            (path, filename) = os.path.split(filepath)
            #Check if it already exists
            (formatted_name, season, episode, episodename, extension) = get_formatted_name(filename, name)
            print("\nFormatted name: " + formatted_name)
            try:
                exists = False
                #First make sure the folder exists (needed for new seasons and shows)
                season = season[1] if season[0] == '0' else season
                seasondir = os.path.join(todir, name, "Season {}".format(season))
                if not os.path.exists(seasondir):
                    os.makedirs(seasondir)
                #Walk the tree, if we find a file with correct name then stop
                for newfile in locate(formatted_name, seasondir):
                    exists = True
                    break
                if not exists:
                    print("Linking " + filename)
                    link_file(name, filename, path, seasondir) 
                else:
                    print "Exists, apparently..."
            except OSError as errormsg:
                print "Couldn't handle " + filename + " because " +str(errormsg)
    
        #Rename all episodes!
        #Bit of a double loop, prevpath makes sure only one pass per directory is done
        #prevpath = ''
        #for file in locate(filepattern, "E:\\Film\\TV-Serier\\Fringe\\"):
            #(path, filename) = os.path.split(file)
            #if prevpath != path:
            #rename_file(name, filename, path)
            #    prevpath = path

