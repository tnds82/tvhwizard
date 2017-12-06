#!/usr/bin/env python
# -*- coding: UTF-8 -*-
################################################################################
#      This file is part of LibreELEC - https://libreelec.tv
#      Copyright (C) 2016-2017 Team LibreELEC
#      Copyright (C) 2017 Tnds82 (tndsrepo@gmail.com)
#
#  LibreELEC is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  LibreELEC is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with LibreELEC.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

import xbmcplugin,xbmcgui,xbmcaddon,os,socket,time,xbmc
from lib import status

addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addonicon   = os.path.join(addonfolder, 'resources/icon.png')

def langString(id):
	return addon.getLocalizedString(id)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
	
def checkip_andchange():
	addonpvr         = xbmcaddon.Addon(id='pvr.hts')
	addonpvrdata     = xbmc.translatePath(addonpvr.getAddonInfo('profile'))
	addonpvrsettings = os.path.join(addonpvrdata, 'settings.xml')

	newip = get_ip_address()
	oldip = addon.getSetting('ipbox')
	ipdvbapi = addon.getSetting('ipdvbapi')
	changeip = {ipdvbapi:newip}
	if newip == oldip:
		addon.setSetting(id='tvhip', value=newip)
		print newip
	else:
		if addon.getSetting('dvbapichoose') == 'pc':
			addontvh     = xbmcaddon.Addon(id='service.tvheadend42')
			addontvhdest = xbmc.translatePath(addontvh.getAddonInfo('profile'))
			dvbapifile   = os.path.join(addontvhdest, 'caclient/6fe6f142570588eb975ddf49861ce970')
			if oldip == ipdvbapi:
				from resources.lib import tools
				addon.setSetting(id='ipdvbapi', value=newip)
				tools.change_words(dvbapifile, changeip)
		addon.setSetting(id='ipbox', value=newip)
		addonpvr.setSetting(id='host', value=newip)
		addon.setSetting(id='tvhip', value=newip)
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(5041), 5000, addonicon))
		time.sleep(1)
		xbmc.executebuiltin('RestartApp')

if addon.getSetting('changeip') == 'true':
	time.sleep(3)
	checkip_andchange()
	status.status()

