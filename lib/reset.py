#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmc, xbmcgui, xbmcaddon, os, shutil, time

import subprocess

dialog = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()

	##### ADDON TVH WIZARD by Tnds #####
addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addonicon   = os.path.join(addonfolder, 'resources/icon.png')
addondata   = xbmc.translatePath(addon.getAddonInfo('profile'))

	##### ADDON SERVICE TVHEADEND #####
addontvh       = xbmcaddon.Addon(id='service.tvheadend42')
addontvhname   = addontvh.getAddonInfo('name')
addontvhfolder = addontvh.getAddonInfo('path')


def langString(id):
	return addon.getLocalizedString(id)
	
def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout

class Reset():

	def __init__(self):
		self.reset_oscam()
		self.reset_tvheadend42()
		self.reset_pvr()
		self.reset_kodi()
		self.reset_tvhwizard()
		self.reset_picons()
		self.reboot()
		
	def reset_oscam(self):
		subprocess_cmd("rm -r $HOME/.kodi/userdata/addon_data/service.softcam.oscam")
		os.system('systemctl restart service.softcam.oscam')
		
	def reset_tvheadend42(self):
		subprocess_cmd("rm -r $HOME/.kodi/userdata/addon_data/service.tvheadend42")
		os.system('systemctl restart service.tvheadend42')

	def reset_pvr(self):
		subprocess_cmd("rm -r $HOME/.kodi/userdata/addon_data/pvr.hts")

	def reset_kodi(self):
#		subprocess_cmd("rm -r $HOME/.kodi/userdata/advancedsettings.xml")
		#channel group
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.usebackendchannelnumbers","value":false},"id":1}')
		#Video 16:9
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"videoplayer.stretch43","value":0},"id":1}')
		
	def reset_tvhwizard(self):
		subprocess_cmd("rm -r $HOME/.kodi/userdata/addon_data/script.tvhwizard/***")

	def reset_picons(self):
		subprocess_cmd("rm $HOME/picons/vdr/*.png")
		subprocess_cmd("rm $HOME/.kodi/userdata/Thumbnails/*/*.png")
		subprocess_cmd("rm $HOME/.kodi/userdata/Database/Textures13.db")

	def reboot(self):
		time.sleep(1)
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50026), 2000, addonicon))
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50023), 2000, addonicon))
		xbmc.executebuiltin('Reboot')