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

def oscam_enable():  
	if 'Configuration of dvbapi throught Addon Config OSCam by tnds82' in open(addonoscamconfig).read():
		dialog.notification(addonname, langString(5053), xbmcgui.NOTIFICATION_INFO, 100)
	else:
		#strings
		tndscfg     ='# Configuration of dvbapi throught Addon Config OSCam by tnds82\n' 
		useroscam   = addon.getSetting('useroscam')
		passoscam   = addon.getSetting('passoscam')
		portoscam   = addon.getSetting('portoscam')
		webifport   = {"8888":portoscam}
		webifuser   = {"httpuser                      = oscam":"%s%s" %("httpuser                      = ", useroscam)}
		webifpass   = {"httppwd                       = oscam":"%s%s" %("httppwd                       = ", passoscam)}
		
		#config oscam
		tools.remove_words(addonoscamconfig, 23)
		tools.remove_words(addonoscamconfig, 23)
		tools.remove_words(addonoscamconfig, 23)
		tools.remove_words(addonoscamconfig, 23)
		tools.insert_words(addonoscamconfig, 2, tndscfg)
		
		#activate restart_on_resume 
		addonoscam.setSetting(id='RESTART_ON_RESUME', value='true')
		
		#user oscam
		if addon.getSetting('useroscam') == '':
			dialog.notification(addonname, langString(5054), xbmcgui.NOTIFICATION_INFO, 2000)
		else :
			tools.change_words(addonoscamconfig, webifuser)
		
		#pass oscam
		if addon.getSetting('passoscam') == '':
			dialog.notification(addonname, langString(5055), xbmcgui.NOTIFICATION_INFO, 2000)
		else :
			tools.change_words(addonoscamconfig, webifpass)

		#port oscam
		if addon.getSetting('portoscam') == '':
			dialog.notification(addonname, langString(5056), xbmcgui.NOTIFICATION_INFO, 2000)
		else :
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

		
def dvbapi_enable():
	if 'user                          = tvh' in open(addonoscamconfig).read():
		dialog.notification(addonname, langString(5057), xbmcgui.NOTIFICATION_INFO, 1000)

	else:
		portdvbapipc = addon.getSetting('portdvbapipc')

		if	addon.getSetting('boxtype') == 'pc-nodmx':
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
			dvbapi.write("boxtype                       = pc-nodmx\n")
			dvbapi.write("\n")
			dvbapi.close()
		
		if	addon.getSetting('boxtype') == 'pc':		
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
 

def cccam_enable():
	if 'nodeid                        = 6509F85610781478' in open(addonoscamconfig).read():
		dialog.notification(addonname, langString(5058), xbmcgui.NOTIFICATION_INFO, 1000)
	else:
		portcccam = addon.getSetting('portcccam')
		
		# create cccam.server
		createoscam = open(addonoscamconfig, 'a')
		createoscam.write("\n")
		createoscam.write("[cccam]\n")
		createoscam.write("port                          = %s\n" % portcccam)
		createoscam.write("nodeid                        = 6509F85610781478\n")
		createoscam.write("version                       = 2.3.0\n")
		createoscam.write("reshare                       = 1\n")
		createoscam.write("ignorereshare                 = 1\n")
		createoscam.write("stealth                       = 1\n")
		createoscam.write("updateinterval                = 60\n")
		createoscam.write("minimizecards                 = 1\n")
		createoscam.write("\n")
		createoscam.close()

	##### ADDON READERS #####			

def oscam_reader(server, number):	
	if server in open(addonoscamreader).read():
		dialog.notification(addonname, langString(5059), xbmcgui.NOTIFICATION_INFO, 1500)
	else:
		label     = addon.getSetting('%s%s%s' % ('name',number,'reader'))
		hostname  = addon.getSetting('%s%s%s' % ('ip',number,'reader'))
		hostname1 = addon.getSetting('%s%s%s' % ('ip',number,'reader1'))
		port      = addon.getSetting('%s%s%s' % ('port',number,'reader'))
		port1     = addon.getSetting('%s%s%s' % ('port',number,'reader1'))		
		username  = addon.getSetting('%s%s%s' % ('user',number,'reader'))
		passw     = addon.getSetting('%s%s%s' % ('pass',number,'reader'))
		
		#cccam
		if addon.getSetting('%s%s%s' % ('protocol',number,'reader')) == 'cccam':
			tools.readercccam(addonoscamreader, label, hostname, port, username, passw, server) 
		
		#newcamd
		if addon.getSetting('%s%s%s' % ('protocol',number,'reader')) == 'newcamd':
			tools.readernewcamd(addonoscamreader, label, username, passw, server) 

		#cs357x
		if addon.getSetting('%s%s%s' % ('protocol',number,'reader')) == 'cs357x':
			tools.readercs357x(addonoscamreader, label, hostname1, port1, username, passw, server)
	
	##### ADDON USERS #####

def oscam_user(user, number):
	if user in open(addonoscamuser).read():
		dialog.notification(addonname, langString(5060), xbmcgui.NOTIFICATION_INFO, 2000)
	else:
		username = addon.getSetting('%s%s%s' % ('user',number,'user'))
		passw = addon.getSetting('%s%s%s' % ('pass',number,'user'))
		tools.usercccam(addonoscamuser, username, passw, user)

