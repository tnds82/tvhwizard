#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmc, xbmcgui, xbmcaddon, os, shutil, tools
import time, subprocess, urllib2

dialog = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()
release = "/etc/os-release"

	##### ADDON TVH WIZARD by Tnds #####
addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addonicon   = os.path.join(addonfolder, 'resources/icon.png')
addondata   = xbmc.translatePath(addon.getAddonInfo('profile'))
channelver  = os.path.join(addondata, 'version')

	##### ADDON SERVICE TVHEADEND #####
if 'NAME="LibreELEC"' in open(release).read():
    addontvh         = xbmcaddon.Addon(id='service.tvheadend42')
    addontvhname     = addontvh.getAddonInfo('name')
    addontvhfolder   = addontvh.getAddonInfo('path')
else:
    if os.path.exists(xbmc.translatePath('special://home/addons/service.tvheadend42')):
        addontvh         = xbmcaddon.Addon(id='service.tvheadend42')
        addontvhname     = addontvh.getAddonInfo('name')
        addontvhfolder   = addontvh.getAddonInfo('path')   
    else:
        addontvh         = xbmcaddon.Addon(id='service.tvheadend43')
        addontvhname     = addontvh.getAddonInfo('name')
        addontvhfolder   = addontvh.getAddonInfo('path')


	##### DESTINATION #####
addontvhdest     = xbmc.translatePath(addontvh.getAddonInfo('profile'))
addontvhchannel  = os.path.join(addontvhdest, 'channel/')
addontvhdvb      = os.path.join(addontvhdest, 'input/dvb/')
addontvhnetwork  = os.path.join(addontvhdest, 'input/dvb/networks')
addontvhmeta     = os.path.join(addontvhdest, 'imagecache/meta')

def langString(id):
    return addon.getLocalizedString(id)
	
def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout

class Update():

    def __init__(self):
        self.channels()

    def channels(self):
        if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
            if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
                self.checkupdate('nos')
            else:
                self.checkupdate('nosfree')
        elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
            self.checkupdate('nowo')
        elif tools.return_data('TVHWIZARD', 'STRING', 'madeira', 2) == 1:
            self.checkupdate('madeira')
        elif tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
            self.checkupdate('hispasat')
        elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
            self.checkupdate('astra')
        elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
            self.checkupdate('hotbird')
        elif tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
            self.checkupdate('tdt')
        elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
            self.checkupdate('meo')
        elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
            self.checkupdate('vodafone')
        elif tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
            self.checkupdate('net')
        elif tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
            self.checkupdate('clarotv')
	
    def checkupdate(self, path):
        url = '%s%s%s' % ("https://addons.tnds82.xyz/addon/tvhwizard/update/channels/", path, ".zip")
        url_version = '%s%s%s' % ("https://addons.tnds82.xyz/addon/tvhwizard/update/channels/", path, "version")
        urlpicon = '%s%s%s' % ("https://addons.tnds82.xyz/addon/tvhwizard/update/picons/", path, ".zip")
        check = urllib2.urlopen(url_version)
        check1 = open(channelver, "r")
        for line1 in check:
            for line2 in check1:
                if line1==line2:
                    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50024), 2000, addonicon))
                else:
                    updatechannels = dialog.yesno(addonname, langString(50025))
                    if updatechannels == 0:
                        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50021), 2000, addonicon))
                    else:
                        self.update_channels(url, path, urlpicon)
                        subprocess_cmd('%s %s' % ('rm -r',  channelver))
                        subprocess_cmd('%s %s %s' % ('wget -O', channelver, url_version))
                        tools.delete_tempfolder()
                        tools.fixpicons()
                        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50020), 2000, addonicon))
                        time.sleep(2)
                        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50023), 2000, addonicon))
                        xbmc.executebuiltin('Reboot')

    def update_channels(self, url, path, urlpicon):
        channelsFile = os.path.join('/tmp/tnds82', path , 'channel.zip')
        networkFile  = os.path.join('/tmp/tnds82', path , 'networks.zip')
        if 'NAME="LibreELEC"' in open(release).read():
            os.system('systemctl stop service.tvheadend42')
        else:
            os.system('systemctl stop service.tvheadend43')
        if os.path.exists(addontvhchannel):
            shutil.rmtree(addontvhchannel)
        ## Channels ##
        header = "Channels"
        tools.channels(url)
        tools.extract(channelsFile,addontvhdest,dp,header)
        if os.path.exists(addontvhnetwork):
            shutil.rmtree(addontvhnetwork)
        header1 = "Networks"
        tools.extract(networkFile,addontvhdvb,dp,header1)
        ## Picons ##
        if os.path.exists(addontvhmeta):
            shutil.rmtree(addontvhmeta)
        subprocess_cmd("rm /storage/picons/vdr/*.png")
        tools.picons(urlpicon)
        if 'NAME="LibreELEC"' in open(release).read():
            os.system('systemctl start service.tvheadend42')
        else:
            os.system('systemctl start service.tvheadend43')
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50078), 5000, addonicon))