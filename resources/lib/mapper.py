# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import xbmcgui
import json
import os
import codecs

ADDON = xbmcaddon.Addon(id="service.takealug.epg-grabber")
addon_name = ADDON.getAddonInfo('name')
addon_version = ADDON.getAddonInfo('version')
loc = ADDON.getLocalizedString
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
temppath = os.path.join(datapath, "temp")

# Make a debug logger
def log(message, loglevel=xbmc.LOGDEBUG):
    xbmc.log('[{} {}] {}'.format(addon_name, addon_version, message), loglevel)

# Make OSD Notify Messages
OSD = xbmcgui.Dialog()

def notify(title, message, icon=xbmcgui.NOTIFICATION_INFO):
    OSD.notification(title, message, icon)

def map_genres(items_genre,genre_format,genres_json,genres_warnings_tmp, lang):
    if genre_format == 'eit':
        with codecs.open(genres_json, 'r', 'utf-8') as c: eit_genre = json.load(c)
        genrelist = items_genre.split(',')
        genres_mapped = list()
        for genre in genrelist:
            if genre not in eit_genre['categories'][lang.upper()]:
                warnings = '\n ]EIT GENRE WARNING[ "{}" Is not in EIT Genre List \n'.format(genre)
                with codecs.open(genres_warnings_tmp, 'ab' , 'utf-8') as f:
                    f.write(warnings)
                genres_mapped.append(genre)
            else:
                genres_mapped.append(eit_genre['categories'][lang.upper()][genre])
        return ",".join(genres_mapped)

    elif genre_format == 'provider':
        channels_mapped = items_genre
        return str(channels_mapped)

def map_channels(channel_id, channel_format,channels_json,channels_warnings_tmp, lang):
    if channel_format == 'rytec':
        with codecs.open(channels_json, 'r', 'utf-8') as c:
            rytec_id = json.load(c)

        if (channel_id) not in rytec_id['channels'][lang.upper()]:
            warnings = '\n ]CHANNEL WARNING[ "{}" Is not in Rytec List \n'.format(channel_id)
            with codecs.open(channels_warnings_tmp, 'ab', 'utf-8') as f:
               f.write(warnings)
            channels_mapped = channel_id
        else :
            channel_mapped = rytec_id['channels'][lang.upper()][channel_id]
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
        outfile = codecs.open(channels_warnings, "w", 'utf-8')
        for line in codecs.open(channels_warnings_tmp, "r", 'utf-8'):
            if line not in lines_seen:  # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()
        ## Add Information for Pull Requests
        with codecs.open(channels_warnings, 'ab', 'utf-8') as f:
            f.write(channel_pull)
        ## Print Content of Channel Warnings Textfile in Kodi LOG
        warnings_channels = codecs.open(channels_warnings, "r", 'utf-8').read()
        log('{} {}'.format(provider,warnings_channels), xbmc.LOGNOTICE)

def create_genre_warnings(genres_warnings_tmp, genres_warnings, provider, genre_pull):
    ## Create Genre Warnings Textfile
    if os.path.isfile(genres_warnings_tmp):
        lines_seen = set()  # holds lines already seen
        outfile = codecs.open(genres_warnings, "w", 'utf-8')
        for line in codecs.open(genres_warnings_tmp, "r", 'utf-8'):
            if line not in lines_seen:  # not a duplicate
                outfile.write(line)
                lines_seen.add(line)
        outfile.close()
        ## Add Information for Pull Requests
        with codecs.open(genres_warnings, 'ab', 'utf-8') as f:
            f.write(genre_pull)
        ## Print Content of Genres Warnings Textfile in Kodi LOG
        warnings_genres = codecs.open(genres_warnings, "r", 'utf-8').read()
        log('{} {}'.format(provider, warnings_genres), xbmc.LOGNOTICE)