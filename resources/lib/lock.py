#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
#########################################################################################
import xbmc, xbmcgui, xbmcaddon, os, sys, json, hashlib

addon             = xbmcaddon.Addon(id='script.tvhwizard')
addonname         = addon.getAddonInfo('name')
addonfolder       = addon.getAddonInfo('path')
addonicon         = os.path.join(addonfolder, 'resources/icon.png')

addondata         = xbmc.translatePath(addon.getAddonInfo('profile'))
addonsettings     = os.path.join(addonfolder, 'resources/settings.xml')
addonresources    = os.path.join(addonfolder, 'resources/')
addonsubsettings  = os.path.join(addonfolder, 'resources/lib/subsettings')

addondatasettings = os.path.join(addondata, 'settings.xml')

dialog            = xbmcgui.Dialog()

def langString(id):
	return addon.getLocalizedString(id)

def check_settings():
	if not os.path.exists(addondata):
		os.makedirs(addondata)
		
		addon.setSetting(id='parentalcfg', value='false')
		addon.setSetting(id='addonpin', value='')
		
	else:
		if not '<setting id="parentalcfg"' in open(addondatasettings).read():

			addon.setSetting(id='parentalcfg', value='false')

		if not '<setting id="addonpin"' in open(addondatasettings).read():

			addon.setSetting(id='addonpin', value='')			

def password():
	# enable password
	if '<setting id="parentalcfg" value="false" />' in open(addondatasettings).read():
		blocked = dialog.input(langString(5044), type=xbmcgui.INPUT_PASSWORD)
		
		addon.setSetting(id='parentalcfg', value='true')
		addon.setSetting(id='addonpin', value=blocked)

		dialog.notification(addonname, langString(5045), xbmcgui.NOTIFICATION_INFO, 2000)
	
	#disable password
	else:
		password = addon.getSetting('addonpin')
		unlock = dialog.input(langString(5046), type=xbmcgui.INPUT_PASSWORD, option=xbmcgui.PASSWORD_VERIFY);

		if unlock == password:
			addon.setSetting(id='parentalcfg', value='false')
			addon.setSetting(id='addonpin', value='')

			dialog.notification(addonname, langString(5047), xbmcgui.NOTIFICATION_INFO, 2000)

		else:
			dialog.ok(addonname, langString(5035))

def run():
	check_settings()	
	password()

def parental_control():
	jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrparental.enabled", "value":%s},"id":1}'
	jsonNotify = '{"jsonrpc":"2.0", "method":"GUI.ShowNotification", "params":{"title":"PVR", "message":"%s","image":""}, "id":1}'
	jsonSetPin = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrparental.pin", "value":%s},"id":1}'
	jsonGetPVR = '{"jsonrpc":"2.0","method":"Settings.GetSettingValue", "params":{"setting":"pvrparental.pin"},"id":1}'

	pvrlock = addon.getSetting('pvrparental')
	disable = "[COLOR red]Disable[/COLOR]"
	enable  = "[COLOR green]Enable[/COLOR]"
	
	if not os.path.exists(addondata):
		os.makedirs(addondata)
		
	if not 'setting id="pvrparental"' in open(addondatasettings).read():
		addon.setSetting(id='pvrparental', value="[COLOR red]Disable[/COLOR]")


	if disable == pvrlock:
		addon.setSetting(id='pvrparental', value=enable)
	
		xbmc.executeJSONRPC(jsonSetPVR % "true")
		xbmc.executeJSONRPC(jsonNotify % langString(5051))
	
	elif enable == pvrlock:
		
		pvrpin = json.loads(xbmc.executeJSONRPC(jsonGetPVR))['result']['value']
		pin = xbmcgui.Dialog().numeric(0, langString(5050))
		m = hashlib.md5()
		m.update(pin)
		
		if m.hexdigest() == pvrpin:
		
			addon.setSetting(id='pvrparental', value=disable)

			xbmc.executeJSONRPC(jsonSetPin % '""')
			xbmc.executeJSONRPC(jsonSetPVR % "false")
			xbmc.executeJSONRPC(jsonNotify % langString(5052))		

		else:
			dialog.ok(addontvhlockname, langString(5035))

