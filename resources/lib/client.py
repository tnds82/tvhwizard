#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
#########################################################################################
import xbmc,xbmcgui,xbmcaddon,os,tools

dialog = xbmcgui.Dialog()

	##### ADDON TVH WIZARD by Tnds #####
addon             = xbmcaddon.Addon(id='script.tvhwizard.tnds')
addonname         = addon.getAddonInfo('name')
addonfolder       = addon.getAddonInfo('path')

	##### ADDON PVR TVHEADEND CLIENT #####
addonpvrtvh         = xbmcaddon.Addon(id='pvr.hts')
addonpvrtvhname     = addonpvrtvh.getAddonInfo('name')
addonpvrtvhfolder   = addonpvrtvh.getAddonInfo('path')
addonpvrtvhdata     = xbmc.translatePath(addonpvrtvh.getAddonInfo('profile'))
addonpvrtvhsettings = os.path.join(addonpvrtvhdata, 'settings.xml')

	##### KODI TV CONFIG #####
kodiguiset          = '/storage/.kodi/userdata/guisettings.xml'

   ##### PVR #####
tvhip   = addon.getSetting('tvhip')
tvhuser = addon.getSetting('tvhusername')
thvpass = addon.getSetting('tvhpassword')

userdata = os.path.join("/storage/.kodi/userdata/")
advanced = os.path.join(userdata, 'advancedsettings.xml')

def langString(id):
	return addon.getLocalizedString(id)

def pvr_config():
	if os.path.exists(addonpvrtvhdata):
		if '"epg_async" value="true"' in open(addonpvrtvhsettings).read():
			dialog.notification(addonname, langString(5042), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		if not os.path.exists(addonpvrtvhdata):
			os.makedirs(addonpvrtvhdata)
			tools.pvrsettings(addonpvrtvhsettings, tvhip, thvpass, tvhuser)
		#Enable Live TV
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled","value":true},"id":1}')

def kodi_config():
	release = "/etc/os-release"
	if os.path.exists(advanced):
		dialog.notification(addonname, langString(5043), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		#Optimization
		if addon.getSetting('optim') == 'true':
			if 'VERSION_ID="7.0"' in open(release).read():
				tools.advancedsettings_jarvis(advanced)
			if 'VERSION_ID="8.0"' in open(release).read():
				tools.advancedsettings_krypton(advanced)

	#channel group
	if addon.getSetting('syncgroup') == 'true':
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.syncchannelgroups","value":true},"id":1}')
	else:
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.syncchannelgroups","value":false},"id":1}')

	#channel number
	if addon.getSetting('syncchannels') == 'true':
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.usebackendchannelnumbers","value":true},"id":1}')
	else:
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.usebackendchannelnumbers","value":false},"id":1}')
		
	#Play maximized
	if addon.getSetting('playmax') == 'true':
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrplayback.playminimized","value":false},"id":1}')
	else:
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrplayback.playminimized","value":true},"id":1}')
		
	#Video 16:9
	if addon.getSetting('video169') == 'true':
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"videoplayer.stretch43","value":4},"id":1}')
	else:
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"videoplayer.stretch43","value":0},"id":1}')
		
	#Last Channel
	if addon.getSetting('lastchannel') == 'true':
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrplayback.startlast","value":2},"id":1}')	
	if addon.getSetting('lastchannel') == 'false':
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrplayback.startlast","value":0},"id":1}')

##### Guide Config #####

def tvh_guide():
	if addon.getSetting('disableup') == 'true':
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"epg.preventupdateswhileplayingtv","value":false},"id":1}')
	else:
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"epg.preventupdateswhileplayingtv","value":true},"id":1}')
	upinterval = addon.getSetting('upinterval')
	xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"epg.epgupdate","value":'+ upinterval +'},"id":1}')

