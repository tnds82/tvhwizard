#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmc, xbmcplugin, xbmcgui, xbmcaddon, os, shutil, xbmcvfs, re, tools

dialog = xbmcgui.Dialog()

	##### ADDON TVH WIZARD by Tnds #####
addon             = xbmcaddon.Addon(id='script.tvhwizard')
addonname         = addon.getAddonInfo('name')
addonfolder       = addon.getAddonInfo('path')

	##### ADDON SERVICE OSCAM #####
addonoscam         = xbmcaddon.Addon(id='service.softcam.oscam')
addonoscamname     = addonoscam.getAddonInfo('name')
addonoscamfolder   = addonoscam.getAddonInfo('path')

	##### ADDON SERVICE OSCAM (Userdata) #####
addonoscamuserdata = xbmc.translatePath(addonoscam.getAddonInfo('profile'))
addonoscamsettings = os.path.join(addonoscamuserdata, 'settings.xml')
addonoscamconfig = os.path.join(addonoscamuserdata, 'config/oscam.conf')
addonoscamreader = os.path.join(addonoscamuserdata, 'config/oscam.server')
addonoscamuser = os.path.join(addonoscamuserdata, 'config/oscam.user')
addonoscamdvbapi = os.path.join(addonoscamuserdata, 'config/oscam.dvbapi')


def langString(id):
	return addon.getLocalizedString(id)

class Oscam():

	def __init__(self):
		self.oscam_enable()
		self.dvbapi_enable()
		self.oscam_readers()
	
	def oscam_enable(self):  
		if 'Configuration of dvbapi throught Addon Config OSCam by tnds82' in open(addonoscamconfig).read():
			dialog.notification(addonname, langString(50053), xbmcgui.NOTIFICATION_INFO, 100)
		else:
			#strings
			tndscfg     ='# Configuration of dvbapi throught Addon Config OSCam by tnds82\n' 
			useroscam   = tools.return_data('USERS', 'PROGRAM', 'oscam', 2)
			passoscam   = tools.return_data('USERS', 'PROGRAM', 'oscam', 3)
			portoscam   = tools.return_data('USERS', 'PROGRAM', 'oscam', 4)
			webifuser   = {"httpuser                      = oscam":"%s%s" %("httpuser                      = ", useroscam)}
			webifpass   = {"httppwd                       = oscam":"%s%s" %("httppwd                       = ", passoscam)}
			webifport   = {"httpport                      = 8888":"%s%s" %("httpport                      = ", portoscam)}
			
			#config oscam
			tools.remove_words(addonoscamconfig, 2)
			tools.remove_words(addonoscamconfig, 25)
			tools.remove_words(addonoscamconfig, 25)
			tools.remove_words(addonoscamconfig, 25)
			tools.remove_words(addonoscamconfig, 25)
			tools.insert_words(addonoscamconfig, 2, tndscfg)
			
			#activate restart_on_resume 
			addonoscam.setSetting(id='RESTART_ON_RESUME', value='true')

			#user oscam
			tools.change_words(addonoscamconfig, webifuser)
			#pass oscam
			tools.change_words(addonoscamconfig, webifpass)
			#port oscam
			tools.change_words(addonoscamconfig, webifport)
			
			# create oscam.server
			readers = open(addonoscamreader, 'a')
			readers.write("# Configuration of readers throught Addon Config OSCam by tnds82\n")
			readers.write("\n")
			readers.close()

			# create oscam.user
			readers = open(addonoscamuser, 'a')
			readers.write("# Configuration of users throught Addon OSCam by tnds82\n")
			readers.write("\n")
			readers.write("[account]\n")
			readers.write("user                          = tvh\n")
			readers.write("description                   = tvh\n")
			readers.write("keepalive                     = 1\n")
			readers.write("au                            = 1\n")
			readers.write("group                         = 1\n")
			readers.write("\n")
			readers.close()

			# create oscam.dvbapi
			readers = open(addonoscamdvbapi, 'a')
			readers.write("############### Meo Mapping ################\n")
			readers.write("#M: 1814 0100:005221 #MEO Mapping\n")
			readers.write("#I: 1814 #MEO Mapping\n")
			readers.write("\n")
			readers.close()

		
	def dvbapi_enable(self):
		if 'user                          = tvh' in open(addonoscamconfig).read():
			dialog.notification(addonname, langString(50057), xbmcgui.NOTIFICATION_INFO, 1000)
		else:
			portdvbapipc = tools.return_data('OSCAM', 'PROTOCOL', 'dvbapi', 4)
			dvbapi = open(addonoscamconfig, 'a')
			dvbapi.write("[dvbapi]\n")
			dvbapi.write("enabled                       = 1\n")
			dvbapi.write("au                            = 1\n")
			dvbapi.write("pmt_mode                      = 4\n")
			dvbapi.write("request_mode                  = 1\n")
			dvbapi.write("delayer                       = 60\n")
			dvbapi.write("user                          = tvh\n")
			dvbapi.write("read_sdt                      = 2\n")
			dvbapi.write("write_sdt_prov                = 1\n")
			dvbapi.write("boxtype                       = pc\n")
			dvbapi.write("listen_port                   = %s\n" % portdvbapipc)
			dvbapi.write("\n")
			dvbapi.close()
 

	def oscam_readers(self):
		if tools.return_data('TVHWIZARD', 'STRING', 'rfirst', 2) == 1:
			self.oscam_reader('reader1', 'Server 1')
		if tools.return_data('TVHWIZARD', 'STRING', 'rsecond', 2) == 1:
			self.oscam_reader('reader2', 'Server 2')
		if tools.return_data('TVHWIZARD', 'STRING', 'rthird', 2) == 1:
			self.oscam_reader('reader3', 'Server 3')
		if tools.return_data('TVHWIZARD', 'STRING', 'rfourth', 2) == 1:
			self.oscam_reader('reader4', 'Server 4')
		if tools.return_data('TVHWIZARD', 'STRING', 'rfifth', 2) == 1:
			self.oscam_reader('reader5', 'Server 5')

	def oscam_reader(self, reader, server):
		if server in open(addonoscamreader).read():
			dialog.notification(addonname, langString(50059), xbmcgui.NOTIFICATION_INFO, 1500)
		else:
			label     = tools.return_data('READERS', 'READER', reader, 2)
			hostname  = tools.return_data('READERS', 'READER', reader, 3)
			username  = tools.return_data('READERS', 'READER', reader, 4)
			passw     = tools.return_data('READERS', 'READER', reader, 5)
			port      = tools.return_data('READERS', 'READER', reader, 6)
			
			#cccam
			tools.readercccam(addonoscamreader, label, hostname, port, username, passw, server) 
		