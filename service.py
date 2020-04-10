#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmcplugin,xbmcgui,xbmcaddon,os,socket,time,xbmc,json, urllib2
from lib import tools

addon         = xbmcaddon.Addon(id='script.tvhwizard')
addonname     = addon.getAddonInfo('name')
addonfolder   = addon.getAddonInfo('path')
addonicon     = os.path.join(addonfolder, 'resources/icon.png')
addondata     = xbmc.translatePath(addon.getAddonInfo('profile'))
database      = os.path.join(addondata, 'tvhwizard.db')
release       = "/etc/os-release"

def langString(id):
    return addon.getLocalizedString(id)

def writeLog(message, level=xbmc.LOGDEBUG):
    xbmc.log('[%s %s] %s' % (xbmcaddon.Addon().getAddonInfo('id'),
                             xbmcaddon.Addon().getAddonInfo('version'),
                             message), level)

class Services():

    def __init__(self):
        if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
            if tools.return_data('TVHWIZARD', 'STRING', 'changeip', 2) == 1:
                time.sleep(3)
                self.checkip_and_change_pt()
                from lib import status
                status.Status()
        elif tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
            if tools.return_data('TVHWIZARD', 'STRING', 'changeip', 2) == 1:
                time.sleep(3)
                self.checkip_and_change_br()
                from lib import status
                status.Status()

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def checkip_and_change_br(self):
        addonpvr         = xbmcaddon.Addon(id='pvr.hts')
        addonpvrdata     = xbmc.translatePath(addonpvr.getAddonInfo('profile'))
        addonpvrsettings = os.path.join(addonpvrdata, 'settings.xml')

        new_ip = self.get_ip_address()
        old_ip = addon.getSetting('tvhip')

        if new_ip == old_ip:
            writeLog("The ip of the config's is the same as the current ip", xbmc.LOGNOTICE)
        else:
            addonpvr.setSetting(id='host', value=new_ip)
            tools.update_data('PVR', 'IP', self.get_ip_address(), 'ID', 1)
            writeLog("The ip of config's has been updated", xbmc.LOGNOTICE)
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50041), 5000, addonicon))
            xbmc.executebuiltin('RestartApp')		

    def checkip_and_change_pt(self):
        addonpvr         = xbmcaddon.Addon(id='pvr.hts')
        addonpvrdata     = xbmc.translatePath(addonpvr.getAddonInfo('profile'))
        addonpvrsettings = os.path.join(addonpvrdata, 'settings.xml')

        new_ip = self.get_ip_address()
        old_ip = addon.getSetting('tvhip')

        ipdvbapi = tools.return_data('OSCAM', 'PROTOCOL', 'dvbapi', 3)

        if new_ip == old_ip:
            writeLog("The ip of the config's is the same as the current ip", xbmc.LOGNOTICE)
        else:
            if tools.return_data('TVHWIZARD', 'STRING', 'dvbapioscam', 2) == 1:
                if 'NAME="LibreELEC"' in open(release).read():
                    addontvh = xbmcaddon.Addon(id='service.tvheadend42')
                    addontvhdest = xbmc.translatePath(addontvh.getAddonInfo('profile'))
                else:
                    addontvh = xbmcaddon.Addon(id='service.tvheadend43')
                    addontvhdest = xbmc.translatePath(addontvh.getAddonInfo('profile'))
                dvbapifile = os.path.join(addontvhdest, 'caclient/6fe6f142570588eb975ddf49861ce970')

                if old_ip == ipdvbapi:
                    tools.update_data('OSCAM', 'IP', self.get_ip_address(), 'ID', 1)
                    tools.updateJsonFile(dvbapifile, 'camdfilename', new_ip)
                    time.sleep(1)
                    if 'NAME="LibreELEC"' in open(release).read():
                        os.system('systemctl restart service.tvheadend42')
                    else:
                        os.system('systemctl restart service.tvheadend43')
            addonpvr.setSetting(id='host', value=new_ip)
            tools.update_data('PVR', 'IP', self.get_ip_address(), 'ID', 1)
            writeLog("The ip of config's has been updated", xbmc.LOGNOTICE)
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50041), 5000, addonicon))
            xbmc.executebuiltin('RestartApp')		

if __name__ == '__main__':
    if not os.path.exists(database):
        tools.create_database()
        Services()
    else:
        Services()