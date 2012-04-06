import subprocess
import ConfigParser
import string
import shutil
import re

# New instance with 'bar' and 'baz' defaulting to 'Life' and 'hard' each
#config = ConfigParser.SafeConfigParser({'bar': 'Life', 'baz': 'hard'})
#config.read('example.cfg')

import os, fnmatch
from tvdb_api import Tvdb

def formatname(text=''):
    return string.replace(text, ' ', '*')

def generate_filepattern(showname, season='', episode=''):
    name = ""
    for char in showname:
        if str.lower(char) in string.lowercase + string.digits:
            name += '[' + str.lower(char) + str.upper(char) + ']'
        else:
            name += char
    pattern = name + '*?' + season + '*?' + episode + '*[am][vkp][iv4]'
    return string.replace(pattern, ' ', '*')

def quote(text=''):
    '''Surrounds the text with double-qoutes. Needed for commandline operations in windows
    for paths which use spaces'''
    return '"' + text + '"'

def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)
            
def unzip(filepattern, dir):
    '''Unzips all files matching the pattern within the directory.'''
    for file in locate(filepattern, dir):
        for zippedfile in fnmatch.filter([file], "*7z") or fnmatch.filter([file], "*zip") or fnmatch.filter([file], "*rar"):
            subprocess.Popen(quote('C:\\Program Files (x86)\\7-Zip\\7z.exe') + " e -y " + quote(zippedfile), shell=True)
            print "unzipped " + zippedfile
            
def copy_file(file, to_dir, extensions = ['avi', 'mkv', 'mp4']):
    '''Moves all files matching the pattern with the (optional) extensions with the from_dir to the to_dir'''
    #files = []
    #for ext in extensions:
        #for file in locate(filepattern + '.' + ext, from_dir):
            #files.append(file)
        
    #for file in files:
    try:
        #On linux, this will throw an exception if we copy to NTFS, where permissions do not exist, ignore that error
        try:
            shutil.copy(file, to_dir)
        except OSError as error:
            if 'Errno 1' in str(error):
                pass
            else:
                raise
        print "Copied " + file + " to " + to_dir
        #    os.remove(file)
        #print "Removed " + file
    except OSError as errormsg:
        print "Couldn't copy " + file + " because %s" % errormsg
        raise

def link_file(name, filename, path, to_dir, extensions = ['avi', 'mkv', 'mp4']):
    (formatted_name, season, episode, episodename, extension) = get_formatted_name(filename, name)
    if formatted_name:
        #path = path + '\\'
        #Only for avi and mkv files
        if extension in extensions or extension.replace('.','') in extensions:
            try:
                os.link(os.path.join(path, filename), os.path.join(to_dir,formatted_name))
                print("Linked {}".format(os.path.join(to_dir, formatted_name)))
            except OSError as emsg:
                print("Coundnt link {} because {}".format(filename, emsg))
                raise


def get_formatted_name(filename, name):
    #print(name, filename)
    matches = re.match(r"[a-zA-Z\s\.\-_\d\(\)]+?[seaonSEAON\s\.\-_\[\]]+(?P<season>\d?\d)[xXepisodEPISOD\s\.\-_\[\]]+(?P<episode>\d?\d).*(?P<extension>\.[a-zA-Z0-9]+)", filename)
    if matches:
        season = matches.group('season')
        episode = matches.group('episode')
        #append zero
        if len(season) == 1:
            season = '0' + season
        if len(episode) == 1:
            episode = '0' + episode
        extension = matches.group('extension')
        tvdb_instance = Tvdb(interactive=False, cache=True)
        name = tvdb_instance[name]['seriesname']
        episodename = ''
        try:
            episodename = tvdb_instance[name][int(season)][int(episode)]['episodename']
        except:
            print("shit happened: S" + str(season) + "E" + str(episode))
            raise tvdb_exceptions.tvdb_episodenotfound
        #Remove illegal chars
        episodename = re.sub(r'["\*\/\\\|\<\>\?\:]', '', episodename)
        formatted_name = name.title() + ' - S' + season + 'E' + episode + ' - ' + episodename + extension
        return (formatted_name, season, episode, episodename, extension)
    else:
        return ('', '', '', '', '')

def rename_file(name, filename, path, extensions = ['avi', 'mkv', 'mp4']):
    #get season and episode number
    (formatted_name, season, episode, episodename, extension) = get_formatted_name(filename, name)
    if formatted_name:
        #path = path + '\\'
        #Only for avi and mkv files
        if extension in extensions or extension.replace('.', '') in extensions:
            try:
                os.rename(os.path.join(path, filename), os.path.join(path, formatted_name))
                print "Renamed " + os.path.join(path, formatted_name)
            except OSError as errormsg:
                print "Couldn't rename " + filename + " because %s" % errormsg
                print "episodename: %s" % episodename
                raise

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    
    #f = open('tvshows.txt', 'r')
    #names = f.readlines()
    names = ['How I Met Your Mother', 'Bored to Death', 'The Big Bang Theory', 'The Simpsons', 'Top Gear', 'Mythbusters', 'Big Love', 'Fringe', 'Boardwalk Empire', 'Dexter', 'House', 'Burnistoun', 'Breaking Bad', 'Futurama', 'The IT Crowd']
    #names = ['The Big Bang Theory']
    dir = "E:\\Downloads\\torrent"
    todir = "E:\\Film\\TV-Serier\\"
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

