#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds82
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import xbmcplugin,xbmcgui,xbmcaddon,os,socket,time

addon            = xbmcaddon.Addon(id='script.tvhwizard')
addonname        = addon.getAddonInfo('name')
addonfolder      = addon.getAddonInfo('path')
addonicon        = os.path.join(addonfolder, 'icon.png')

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
		print "Same IP, nothing needed to be done." 
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
		
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(5041), 5000, addonicon))
		time.sleep(1)
		os.system("reboot")
	
if addon.getSetting('updatetvh') == 'true':
	from resources.lib import update
	update.zone_channels()

if addon.getSetting('changeip') == 'true':
	checkip_andchange()
