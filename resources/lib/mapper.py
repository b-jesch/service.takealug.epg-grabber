# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import xbmcgui

import json
import os

ADDON = xbmcaddon.Addon(id="service.takealug.epg-grabber")
addon_name = ADDON.getAddonInfo('name')
addon_version = ADDON.getAddonInfo('version')
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
temppath = os.path.join(datapath, "temp")

# Make a debug logger
def log(message, loglevel=xbmc.LOGDEBUG):
    xbmc.log('[{} {}] {}'.format(addon_name, addon_version, message), loglevel)

# Make OSD Notify Messages
OSD = xbmcgui.Dialog()

def notify(title, message, icon=xbmcgui.NOTIFICATION_INFO):
    OSD.notification(title, message, icon)

def map_genres(items_genre,genre_format,genres_json,genres_warnings_tmp):
    if genre_format == 'eit':
        with open(genres_json, 'r') as c: eit_genre = json.load(c)
        genrelist = items_genre.split(',')
        genres_mapped = list()
        for genre in genrelist:
            if genre not in eit_genre['categories']['DE']:
                warnings = '\n' + ']EIT GENRE WARNING[' + ' "' + genre + '" ' + 'Is not in EIT Genre List' + '\n'
                with open(genres_warnings_tmp, 'ab') as f:
                    f.write(warnings)
                genres_mapped.append(genre)
            else:
                genres_mapped.append(eit_genre['categories']['DE'][genre])
        return ", ".join(genres_mapped)

    elif genre_format == 'provider':
        channels_mapped = items_genre
        return str(channels_mapped)

def map_channels(channel_id, channel_format,channels_json,channels_warnings_tmp):
    if channel_format == 'rytec':
        with open(channels_json, 'r') as c:
            rytec_id = json.load(c)

        if (channel_id) not in rytec_id['channels']['DE']:
            warnings = '\n' + ']CHANNEL WARNING[' + ' "' + channel_id + '" ' + 'Is not in Rytec List' + '\n'
            with open(channels_warnings_tmp, 'ab') as f:
               f.write(warnings)
            channels_mapped = channel_id
        else :
            channel_mapped = rytec_id['channels']['DE'][channel_id]
            channels_mapped = channel_id.replace(channel_id, channel_mapped)

        c.close()
        return str(channels_mapped)

    elif channel_format == 'provider':
        channels_mapped = channel_id
        return str(channels_mapped)

def create_channel_warnings(channels_warnings_tmp, channels_warnings, provider,channel_pull):
    ## Create Channel Warnings Textfile
    if os.path.isfile(channels_warnings_tmp):
        lines_seen = set()  # holds lines already seen
        outfile = open(channels_warnings, "w")
        for line in open(channels_warnings_tmp, "r"):
            if line not in lines_seen:  # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()
        ## Add Information for Pull Requests
        with open(channels_warnings, 'ab') as f:
            f.write(channel_pull)
        ## Print Content of Channel Warnings Textfile in Kodi LOG
        warnings_channels = open(channels_warnings, "r").read()
        log(provider + '' + warnings_channels, xbmc.LOGNOTICE)

def create_genre_warnings(genres_warnings_tmp, genres_warnings, provider, genre_pull):
    ## Create Genre Warnings Textfile
    if os.path.isfile(genres_warnings_tmp):
        lines_seen = set()  # holds lines already seen
        outfile = open(genres_warnings, "w")
        for line in open(genres_warnings_tmp, "r"):
            if line not in lines_seen:  # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()
        ## Add Information for Pull Requests
        with open(genres_warnings, 'ab') as f:
            f.write(genre_pull)
        ## Print Content of Genres Warnings Textfile in Kodi LOG
        warnings_genres = open(genres_warnings, "r").read()
        log(provider + '' + warnings_genres, xbmc.LOGNOTICE)