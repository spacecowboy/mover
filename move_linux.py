#!/usr/bin/python

import sys
import os

from tvnamer.tvdb_api.tvdb_api import Tvdb
from tvnamer.main import findFiles
from tvnamer.utils import FileParser
from tvnamer.tvnamer_exceptions import (InvalidFilename, DataRetrievalError,
                                        ShowNotFound, SeasonNotFound,
                                        EpisodeNotFound, EpisodeNameNotFound)

_fromdir = "/media/Gargant/Downloads/torrent"
_todir = "/media/Gargant/Film/TV-Serier/"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        paths = [_fromdir]
    else:
        paths = sys.argv[1:]

    print('Moving files from {} to {}'.format(paths, _todir))

    episodes_found = []

    #Look for video files
    for validfile in findFiles(paths):
        #Parse the filename
        parser = FileParser(validfile)
        try:
            episode = parser.parse()
        except InvalidFilename as e:
            print("\nInvalid filename: {}".format(e))
            continue
        else:
            #Need show name
            if episode.seriesname is None:
                print("\nSeries name not found: {}".format(validfile))
                continue
            else:
                episodes_found.append(episode)

    if not episodes_found:
        exit('\nNo episodes found...')

    # Sort episodes by series, season and episode
    episodes_found.sort(key=lambda x: x.sortable_info())

    # Time to get info from the net
    tvdb = Tvdb()

    for episode in episodes_found:
        try:
            episode.populateFromTvdb(tvdb)
        except (DataRetrievalError, ShowNotFound, SeasonNotFound,
                EpisodeNotFound, EpisodeNameNotFound) as e:
            print(("\nSkipping {0.originalfilename}" +
                  "due to {1}").format(episode, e))
            continue

        formatted_name = episode.generateFilename()
        print("\nFormatted name: " + formatted_name)
        try:
            seasondir = os.path.join(_todir, episode.seriesname,
                                     "Season {}".format(episode.seasonnumber))
        except AttributeError as e:
            #Could be anime, they dont have seasons
            seasondir = os.path.join(_todir, episode.seriesname)

        #Make sure directory exists
        if not os.path.exists(seasondir):
            os.makedirs(seasondir)

        #Make sure file doesn't already exist there
        if os.path.exists(os.path.join(seasondir, formatted_name)):
            print("Already exists...")
        else:
            try:
                os.link(episode.fullpath,
                        os.path.join(seasondir, formatted_name))
                print("Linked " + os.path.join(seasondir, formatted_name))
            except OSError as emsg:
                print(("Coundnt link {} because" +
                       " {}").format(episode.fullpath, emsg))
                continue
