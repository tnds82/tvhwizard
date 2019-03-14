#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmcplugin,xbmcgui,xbmcaddon,os,socket,time,xbmc,json
from lib import status

addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addonicon   = os.path.join(addonfolder, 'resources/icon.png')

def langString(id):
	return addon.getLocalizedString(id)

def writeLog(message, level=xbmc.LOGDEBUG):
    xbmc.log('[%s %s] %s' % (xbmcaddon.Addon().getAddonInfo('id'),
                             xbmcaddon.Addon().getAddonInfo('version'),
                             message.encode('utf-8')), level)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def changeippvr():
	addonpvr         = xbmcaddon.Addon(id='pvr.hts')
	addonpvrdata     = xbmc.translatePath(addonpvr.getAddonInfo('profile'))
	addonpvrsettings = os.path.join(addonpvrdata, 'settings.xml')
	
	new_ip = get_ip_address()
	old_ip = addon.getSetting('ipbox')
	
	if new_ip == old_ip:
		addon.setSetting(id='tvhip', value=new_ip)
		writeLog("The ip of the config's is the same as the current ip", xbmc.LOGNOTICE)
	else:
		addonpvr.setSetting(id='host', value=new_ip)
		addon.setSetting(id='ipbox', value=new_ip)
		addon.setSetting(id='tvhip', value=new_ip)
		writeLog("The ip of config's has been updated", xbmc.LOGNOTICE)
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50041), 5000, addonicon))
		time.sleep(1)
		xbmc.executebuiltin('RestartApp')
		
		

def checkip_andchange():
	addonpvr         = xbmcaddon.Addon(id='pvr.hts')
	addonpvrdata     = xbmc.translatePath(addonpvr.getAddonInfo('profile'))
	addonpvrsettings = os.path.join(addonpvrdata, 'settings.xml')

	newip = get_ip_address()
	oldip = addon.getSetting('tvhip')
	ipdvbapi = addon.getSetting('ipdvbapi')
	changeip = {ipdvbapi:newip}
	if newip == oldip:
		addon.setSetting(id='tvhip', value=newip)
		print newip
	else:
		if addon.getSetting('dvbapichoose') == 'pc':
			addontvh = xbmcaddon.Addon(id='service.tvheadend42')
			addontvhdest = xbmc.translatePath(addontvh.getAddonInfo('profile'))
			dvbapifile = os.path.join(addontvhdest, 'caclient/6fe6f142570588eb975ddf49861ce970')
			if oldip == ipdvbapi:
				from lib import tools
				os.system('systemctl stop service.tvheadend42')
				addon.setSetting(id='ipdvbapi', value=newip)
				tools.change_words(dvbapifile, changeip)
				os.system('systemctl start service.tvheadend42')
		addonpvr.setSetting(id='host', value=newip)
		addon.setSetting(id='tvhip', value=newip)
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50041), 5000, addonicon))
		time.sleep(1)
		xbmc.executebuiltin('RestartApp')

if addon.getSetting('portugal') == 'true':
	if addon.getSetting('changeip') == 'true':
		time.sleep(3)
		checkip_andchange()
		status.status()
elif addon.getSetting('brasil') == 'true':
	if addon.getSetting('changeip') == 'true':
		time.sleep(3)
		changeippvr()
		status.statusbr()