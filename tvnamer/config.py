#!/usr/bin/env python

"""Holds Config singleton
"""

from config_defaults import defaults

#I dont want brackets!
_my_prefs = {
    # Formats for renamed files. Variations for with/without episode,
    # and with/without season number.
    'filename_with_episode':
     '%(seriesname)s - S%(seasonnumber)02dE%(episode)s - %(episodename)s%(ext)s',
    'filename_without_episode':
     '%(seriesname)s - S%(seasonnumber)02dE%(episode)s%(ext)s',

    # Seasonless filenames.
    'filename_with_episode_no_season':
      '%(seriesname)s - %(episode)s - %(episodename)s%(ext)s',
    'filename_without_episode_no_season':
     '%(seriesname)s - %(episode)s%(ext)s',

    # Date based filenames.
    # Series - [2012-01-24] - Ep name.ext
    'filename_with_date_and_episode':
     '%(seriesname)s - [%(episode)s] - %(episodename)s%(ext)s',
    'filename_with_date_without_episode':
     '%(seriesname)s - [%(episode)s]%(ext)s',

    # Anime filenames.
    # [AGroup] Series - 02 - Some Ep Name [CRC1234].ext
    # [AGroup] Series - 02 [CRC1234].ext
    'filename_anime_with_episode':
     '[%(group)s] %(seriesname)s - %(episode)s - %(episodename)s [%(crc)s]%(ext)s',

    'filename_anime_without_episode':
     '[%(group)s] %(seriesname)s - %(episode)s [%(crc)s]%(ext)s',
    # Same, without CRC value
    'filename_anime_with_episode_without_crc':
     '[%(group)s] %(seriesname)s - %(episode)s - %(episodename)s%(ext)s',

    'filename_anime_without_episode_without_crc':
     '[%(group)s] %(seriesname)s - %(episode)s%(ext)s',

    #Join multiple episodes as E01E02E03
    #Instead of E01-02-03
    'episode_separator': 'E',

    }

Config = dict(defaults)
Config.update(_my_prefs)
