#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmc, xbmcplugin, xbmcgui, xbmcaddon, os, shutil
import xbmcvfs, re, base64, tools, time, subprocess, json
from collections import OrderedDict

dialog = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()
release = "/etc/os-release"

	##### ADDON TVH WIZARD by Tnds #####
addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addondata   = xbmc.translatePath(addon.getAddonInfo('profile'))
addonchaver = os.path.join(addondata, 'version')
addonicon   = os.path.join(addonfolder, 'resources/icon.png')

	##### ADDON SERVICE TVHEADEND #####
addontvh            = xbmcaddon.Addon(id='service.tvheadend42')
addontvhname        = addontvh.getAddonInfo('name')
addontvhfolder      = addontvh.getAddonInfo('path')

	##### DESTINATION #####
addontvhdest        = xbmc.translatePath(addontvh.getAddonInfo('profile'))
addontvhconfig      = os.path.join(addontvhdest, 'config')
addontvhacontrol    = os.path.join(addontvhdest, 'accesscontrol/')
addontvhpass        = os.path.join(addontvhdest, 'passwd/')
addontvhdvbapi      = os.path.join(addontvhdest, 'caclient/')
dvbapifile          = os.path.join(addontvhdest, 'caclient/6fe6f142570588eb975ddf49861ce970')
addontvhdvb         = os.path.join(addontvhdest, 'input/dvb')
addontvhtuners      = os.path.join(addontvhdest, 'input/linuxdvb/adapters/')
addontvhimgcache    = os.path.join(addontvhdest, 'imagecache/')
addontvhdvrconf     = os.path.join(addontvhdest, 'dvr/config/')
addontvhdefaultdvr  = os.path.join(addontvhdest, 'dvr/config/8d0f5b7ae354d956d7fe5db25f5d0d24')
addontvhprofile     = os.path.join(addontvhdest, 'profile/')

	##### ADDON PVR TVHEADEND CLIENT #####
addonpvrtvh         = xbmcaddon.Addon(id='pvr.hts')
addonpvrtvhname     = addonpvrtvh.getAddonInfo('name')
addonpvrtvhfolder   = addonpvrtvh.getAddonInfo('path')
addonpvrtvhdata     = xbmc.translatePath(addonpvrtvh.getAddonInfo('profile'))
addonpvrtvhsettings = os.path.join(addonpvrtvhdata, 'settings.xml')

   ##### USERDATA #####
userdata = os.path.join("/storage/.kodi/userdata/")
advanced = os.path.join(userdata, 'advancedsettings.xml')


def langString(id):
	return addon.getLocalizedString(id)

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout

class Tvheadend():

	def __init__(self):
		self.tvh_config()
		self.tvh_users()
		if tools.return_data('TVHWIZARD', 'STRING', 'dvbapioscam', 2) == 1:
			self.tvh_dvbapi()
		if tools.return_data('TVHWIZARD', 'STRING', 'dvbcards', 2) == 1:
			self.tvh_tunners()
		if tools.return_data('TVHWIZARD', 'STRING', 'recording', 2) == 1:
			self.tvh_recording()
		self.tvh_pvr()
		self.kodi_config()
#		self.tvh_guide()

	def tvh_config(self):
		if '"tndsconfig":' in open(addontvhconfig).read():
			dialog.notification(addonname, langString(50061), xbmcgui.NOTIFICATION_WARNING, 2000)
		else:
			tools.changekeyjson(addontvhconfig, 'wizard', 'tndsconfig')
			#expert mode
			tools.updateJsonFile(addontvhconfig, 'uilevel', 2)
			#web language
			tools.addkeyjson(addontvhconfig, 'language_ui', "por")	
			tools.addkeyjson(addontvhconfig, 'language_ui', "eng")
			#epg language
			tools.addkeyjson(addontvhconfig, 'language', ['por','eng'])

	def tvh_users(self):
		userdefault = os.listdir(addontvhacontrol)[0]
		defaultuser = "%s%s" % (addontvhacontrol, userdefault)
		
		if not 'Default access entry' in open(defaultuser).read():
			dialog.notification(addonname, langString(50069), xbmcgui.NOTIFICATION_WARNING, 5000)
		else:
			if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
				if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
					if tools.return_data('USERS', 'ID', 2, 1) == 'tvhadmin':
						self.create_users()
				else:
					if tools.return_data('USERS', 'ID', 1, 1) == 'tvhadmin':
						self.create_users()
			if tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
				if tools.return_data('USERS', 'ID', 1, 1) == 'tvhadmin':
					self.create_users()
					
	def create_users(self):
		adminuser  = tools.return_data('USERS', 'PROGRAM', 'tvhadmin', 2)
		adminpass  = tools.return_data('USERS', 'PROGRAM', 'tvhadmin', 3)
		clientuser = tools.return_data('USERS', 'PROGRAM', 'tvhclient', 2)
		clientpass = tools.return_data('USERS', 'PROGRAM', 'tvhclient', 3)
		
		userdefault = os.listdir(addontvhacontrol)[0]
		defaultuser = "%s%s" % (addontvhacontrol, userdefault)

		# Create password folder
		if not os.path.exists(addontvhpass):
			os.makedirs(addontvhpass)
		# Disable Default access entry
		tools.updateJsonFile(defaultuser, 'enabled', False)
		tools.updateJsonFile(addontvhconfig, 'digest', 2)
			
		# Create administrator user
		adminpath = "%s%s" % (addontvhacontrol, "90989e141bf7c77bcaecaef8da1e0054")			
		with open(adminpath, "w") as outfile:
			json.dump({'enabled':True, 'username':adminuser, 
				'change':['change_rights'], 'uilevel':2, 'streaming':['basic', 'advanced', 'htsp'], 
				'dvr':['basic','htsp','all','all_rw','failed'], 'webui':True, 'admin':True, 
				'comment':'Administrator access entry'}, outfile, indent=4)
		
		# Create administrator password
		## enconde pass
		encoded = base64.b64encode(adminpass)
		tvhpass = "VFZIZWFkZW5kLUhpZGUt"
		passenconded = "%s%s" % (tvhpass, encoded)
		## create pass
		passadmin = "%s%s" % (addontvhpass, "cb77ac54d4e6d859c1890b770f9fbe3a")
		with open(passadmin, "w") as outfile:
			json.dump({'enabled':True, 'username':adminuser, 'password2':passenconded, 
				'comment':'Pass of Adminstrator', 'wizard':False}, outfile, sort_keys=True, indent=4)
		
		# Create client user
		clientpath = "%s%s" % (addontvhacontrol, "95275ba5e99a33a72b5081c870e179d8")
		with open(clientpath, "w") as outfile:
			json.dump({'enabled':True, 'username':clientuser, 
				'change':['change_rights'], 'streaming':['basic', 'advanced', 'htsp'], 
				'dvr':['basic','htsp','all','all_rw','failed'], 'webui':True,
				'comment':'Client access entry'}, outfile, indent=4)

		# Create client password
		## enconde pass	
		encoded = base64.b64encode(clientpass)
		tvhpass = "VFZIZWFkZW5kLUhpZGUt"
		passenconded = "%s%s" % (tvhpass, encoded)
		##create pass
		passadmin = "%s%s" % (addontvhpass, "8597d99ed41fe710bff95567a24372ba")
		with open(passadmin, "w") as outfile:
			json.dump({'enabled':True, 'username':clientuser, 'password2':passenconded, 
				'comment':'Pass of Client', 'wizard':False}, outfile, sort_keys=True, indent=4)

	def tvh_dvbapi(self):
	
		dvbapip    = tools.return_data('OSCAM', 'PROTOCOL', 'dvbapi', 3)
		dvbapiport = tools.return_data('OSCAM', 'PROTOCOL', 'dvbapi', 4)
		
		newcamdhost = tools.return_data('READERS', 'PROTOCOL', 'newcamd', 3)
		newcamduser = tools.return_data('READERS', 'PROTOCOL', 'newcamd', 4)
		newcamdpass = tools.return_data('READERS', 'PROTOCOL', 'newcamd', 5)
		newcamdport = tools.return_data('READERS', 'PROTOCOL', 'newcamd', 6)
		newcamdkey  = tools.return_data('READERS', 'PROTOCOL', 'newcamd', 7)

		if os.path.exists(dvbapifile):
			dialog.notification(addonname, langString(50062), xbmcgui.NOTIFICATION_WARNING, 2000)
		else:
			defaultdvbapi = os.listdir(addontvhdvbapi)[0]
			dvbapidefault = "%s%s" % (addontvhdvbapi, defaultdvbapi)
			tools.updateJsonFile(dvbapidefault, 'enabled', False)
			#oscam pc
			if tools.return_data('OSCAM', 'PROTOCOL', 'dvbapi', 2) == 'pc':
				with open(dvbapifile, "w") as outfile:
					json.dump({'mode':5, 'camdfilename':dvbapip, 'port':dvbapiport, 'class':'caclient_capmt', 
						'index':1, 'enabled':True, 'name':'tvh'}, outfile, sort_keys=True, indent=4)
			
			elif tools.return_data('READERS', 'PROTOCOL', 'newcamd', 2) == 'deskey1':
				with open(dvbapifile, "w") as outfile:
					json.dump({'deskey':newcamdkey, 'username':newcamduser, 'password':newcamdpass, 'hostname':newcamdhost, 'port':newcamdport,
						'emm':True, 'emmex':True, 'keepalive_interval':30, 'class':'caclient_cwc', 'index':1, 'enabled':True, 'name':'tvh'}, outfile, sort_keys=True, indent=4)
			elif tools.return_data('READERS', 'PROTOCOL', 'newcamd', 2) == 'deskey2':
				with open(dvbapifile, "w") as outfile:
					json.dump({'deskey':newcamdkey, 'username':newcamduser, 'password':newcamdpass, 'hostname':newcamdhost, 'port':newcamdport,
						'emm':True, 'emmex':True, 'keepalive_interval':30, 'class':'caclient_cwc', 'index':1, 'enabled':True, 'name':'tvh'}, outfile, sort_keys=True, indent=4)

	def tvh_tunners(self):
		nosnetwork      = "d2e2dd7ba943289f15a46ee502e13b12"
		nowonetwork     = "00e7faf22eece16481b49486b74d81e2"
		tdtnetwork      = "3b71a44c08543bd024fad8630f745d60"
		meonetwork      = "f06c23593ca3971f3ff00f4eaa565fb2"
		vodafonenetwork = "fd3e986178c77d3687b337718c332a39"
		hispanetwork    = "1c2f2758a410776103317afc11abbc8e"
		claronetwork    = "87f9a21e2b1b98c057c424d7ab4cd9c9"
		netnetwork      = "099f5b5ce2a8edb9f41b63481fdaf52b"
	#	astranetwork    = ""
	#	hotbirdnetwork  = ""

		if tools.return_data('TVHWIZARD', 'STRING', 'wetek', 2) == 1:
			if tools.return_data('TVHWIZARD', 'STRING', 'wetekplay', 2) == 1:
				if tools.return_data('TVHWIZARD', 'STRING', 'wdvbc', 2) == 1:
					wetektuner = os.listdir(addontvhtuners)[0]
					wdvbc = "%s%s" % (addontvhtuners, wetektuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
							self.tvh_channels('nos')
							self.tvh_picons('nos')
							tools.dvbc(wdvbc, nosnetwork)
						else:
							self.tvh_channels('nosfree')
							self.tvh_picons('nosfree')
							tools.dvbc(wdvbc, nosnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
						self.tvh_channels('nowo')
						self.tvh_picons('nowo')
						tools.dvbc(wdvbc, nowonetwork)					
				elif tools.return_data('TVHWIZARD', 'STRING', 'wdvbs', 2) == 1:
					wetektuners1 = os.listdir(addontvhtuners)[0]
					wdvbs1 = "%s%s" % (addontvhtuners, wetektuners1)
					wetektuners2 = os.listdir(addontvhtuners)[1]
					wdvbs2 = "%s%s" % (addontvhtuners, wetektuners2)
					if tools.return_data('TVHWIZARD', 'STRING', 'wplnb1', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
							self.tvh_channels('hispasat')
							self.tvh_picons('hispasat')
							if '/dev/dvb/adapter0' in open(wdvbs1).read():
								tools.dvbs(wdvbs1, hispanetwork)
							if '/dev/dvb/adapter0' in open(wdvbs2).read():
								tools.dvbs(wdvbs2, hispanetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
							self.tvh_channels('astra')
							self.tvh_picons('astra')
							if '/dev/dvb/adapter0' in open(wdvbs1).read():
								tools.dvbs(wdvbs1, astranetwork)
							if '/dev/dvb/adapter0' in open(wdvbs2).read():
								tools.dvbs(wdvbs2, astranetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
							self.tvh_channels('hotbird')
							self.tvh_picons('hotbird')
							if '/dev/dvb/adapter0' in open(wdvbs1).read():
								tools.dvbs(wdvbs1, hotbirdnetwork)
							if '/dev/dvb/adapter0' in open(wdvbs2).read():
								tools.dvbs(wdvbs2, astranetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'wplnb2', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
							self.tvh_channels('hispasat')
							self.tvh_picons('hispasat')
							if '/dev/dvb/adapter1' in open(wdvbs1).read():
								tools.dvbs(wdvbs1, hispanetwork)
							if '/dev/dvb/adapter1' in open(wdvbs2).read():
								tools.dvbs(wdvbs2, hispanetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
							self.tvh_channels('astra')
							self.tvh_picons('astra')
							if '/dev/dvb/adapter1' in open(wdvbs1).read():
								tools.dvbs(wdvbs1, astranetwork)
							if '/dev/dvb/adapter1' in open(wdvbs2).read():
								tools.dvbs(wdvbs2, astranetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
							self.tvh_channels('hotbird')
							self.tvh_picons('hotbird')
							if '/dev/dvb/adapter1' in open(wdvbs1).read():
								tools.dvbs(wdvbs1, hotbirdnetwork)
							if '/dev/dvb/adapter1' in open(wdvbs2).read():
								tools.dvbs(wdvbs2, astranetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'wplnboth', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
							self.tvh_channels('hispasat')
							self.tvh_picons('hispasat')
							tools.dvbs(wdvbs1, hispanetwork)
							tools.dvbs(wdvbs2, hispanetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
							self.tvh_channels('astra')
							self.tvh_picons('astra')
							tools.dvbs(wdvbs1, astranetwork)
							tools.dvbs(wdvbs2, astranetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
							self.tvh_channels('hotbird')
							self.tvh_picons('hotbird')
							tools.dvbs(wdvbs1, hotbirdnetwork)
							tools.dvbs(wdvbs2, astranetwork)
				elif tools.return_data('TVHWIZARD', 'STRING', 'wdvbt', 2) == 1:
					wetektuner = os.listdir(addontvhtuners)[0]
					wdvbt = "%s%s" % (addontvhtuners, wetektuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
						self.tvh_channels('tdt')
						self.tvh_picons('tdt')
						tools.dvbt(wdvbt, tdtnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
						self.tvh_channels('meo')
						self.tvh_picons('meo')
						tools.dvbt(wdvbt, meonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
						self.tvh_channels('vodafone')
						self.tvh_picons('vodafone')
						tools.dvbt(wdvbt, vodafonenetwork)
			elif tools.return_data('TVHWIZARD', 'STRING', 'wetekplay2', 2) == 1:
				if tools.return_data('TVHWIZARD', 'STRING', 'wdvbc', 2) == 1:
					wetek2tuner = os.listdir(addontvhtuners)[0]
					w2dvbc = "%s%s" % (addontvhtuners, wetek2tuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
							if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
								self.tvh_channels('nos')
								self.tvh_picons('nos')
								tools.dvbc(w2dvbc, nosnetwork)
							else:
								self.tvh_channels('nosfree')
								self.tvh_picons('nosfree')
								tools.dvbc(w2dvbc, nosnetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
							self.tvh_channels('nowo')
							self.tvh_picons('nowo')
							tools.dvbc(w2dvbc, nowonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
							self.tvh_channels('net')
							self.tvh_picons('net')
							tools.dvbc(w2dvbc, netnetwork)
				elif tools.return_data('TVHWIZARD', 'STRING', 'wdvbs', 2) == 1:
					wetek2tuners = os.listdir(addontvhtuners)[0]
					w2dvbs = "%s%s" % (addontvhtuners, wetek2tuners)
					if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
							self.tvh_channels('hispasat')
							self.tvh_picons('hispasat')
							tools.dvbs(w2dvbs, hispanetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
							self.tvh_channels('astra')
							self.tvh_picons('astra')
							tools.dvbs(w2dvbs, astranetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
							self.tvh_channels('hotbird')
							self.tvh_picons('hotbird')
							tools.dvbs(w2dvbs, hotbirdnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
							self.tvh_channels('clarotv')
							self.tvh_picons('clarotv')
							tools.dvbs(w2dvbs, claronetwork)						
				elif tools.return_data('TVHWIZARD', 'STRING', 'wdvbt', 2) == 1:
					wetek2tuner = os.listdir(addontvhtuners)[0]
					w2dvbt = "%s%s" % (addontvhtuners, wetek2tuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
						self.tvh_channels('tdt')
						self.tvh_picons('tdt')
						tools.dvbt(w2dvbt, tdtnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
						self.tvh_channels('meo')
						self.tvh_picons('meo')
						tools.dvbt(w2dvbt, meonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
						self.tvh_channels('vodafone')
						self.tvh_picons('vodafone')
						tools.dvbt(w2dvbt, vodafonenetwork)
		elif tools.return_data('TVHWIZARD', 'STRING', 'k', 2) == 1:
			if tools.return_data('TVHWIZARD', 'STRING', 'k1plus', 2) == 1:
				if tools.return_data('TVHWIZARD', 'STRING', 'kdvbc', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbc = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
							if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
								self.tvh_channels('nos')
								self.tvh_picons('nos')
								tools.dvbc(kdvbc, nosnetwork)
							else:
								self.tvh_channels('nosfree')
								self.tvh_picons('nosfree')
								tools.dvbc(kdvbc, nosnetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
							self.tvh_channels('nowo')
							self.tvh_picons('nowo')
							tools.dvbc(kdvbc, nowonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
							self.tvh_channels('net')
							self.tvh_picons('net')
							tools.dvbc(kdvbc, netnetwork)
				elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbs', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbs = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
							self.tvh_channels('hispasat')
							self.tvh_picons('hispasat')
							tools.dvbs(kdvbs, hispanetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
							self.tvh_channels('astra')
							self.tvh_picons('astra')
							tools.dvbs(kdvbs, astranetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
							self.tvh_channels('hotbird')
							self.tvh_picons('hotbird')
							tools.dvbs(kdvbs, hotbirdnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
							self.tvh_channels('clarotv')
							self.tvh_picons('clarotv')
							tools.dvbs(kdvbs, claronetwork)						
				elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbt', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbt = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
						self.tvh_channels('tdt')
						self.tvh_picons('tdt')
						tools.dvbt(kdvbt, tdtnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
						self.tvh_channels('meo')
						self.tvh_picons('meo')
						tools.dvbt(kdvbt, meonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
						self.tvh_channels('vodafone')
						self.tvh_picons('vodafone')
						tools.dvbt(kdvbt, vodafonenetwork)
			if tools.return_data('TVHWIZARD', 'STRING', 'k1pro', 2) == 1:
				if tools.return_data('TVHWIZARD', 'STRING', 'kdvbc', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbc = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
							if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
								self.tvh_channels('nos')
								self.tvh_picons('nos')
								tools.dvbc(kdvbc, nosnetwork)
							else:
								self.tvh_channels('nosfree')
								self.tvh_picons('nosfree')
								tools.dvbc(kdvbc, nosnetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
							self.tvh_channels('nowo')
							self.tvh_picons('nowo')
							tools.dvbc(kdvbc, nowonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
							self.tvh_channels('net')
							self.tvh_picons('net')
							tools.dvbc(kdvbc, netnetwork)			
				elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbs', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbs = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
							self.tvh_channels('hispasat')
							self.tvh_picons('hispasat')
							tools.dvbs(kdvbs, hispanetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
							self.tvh_channels('astra')
							self.tvh_picons('astra')
							tools.dvbs(kdvbs, astranetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
							self.tvh_channels('hotbird')
							self.tvh_picons('hotbird')
							tools.dvbs(kdvbs, hotbirdnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
							self.tvh_channels('clarotv')
							self.tvh_picons('clarotv')
							tools.dvbs(kdvbs, claronetwork)
				elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbt', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbt = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
						self.tvh_channels('tdt')
						self.tvh_picons('tdt')
						tools.dvbt(kdvbt, tdtnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
						self.tvh_channels('meo')
						self.tvh_picons('meo')
						tools.dvbt(kdvbt, meonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
						self.tvh_channels('vodafone')
						self.tvh_picons('vodafone')
						tools.dvbt(kdvbt, vodafonenetwork)
			if tools.return_data('TVHWIZARD', 'STRING', 'k2pro', 2) == 1:
				if tools.return_data('TVHWIZARD', 'STRING', 'kdvbc', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbc = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
							if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
								self.tvh_channels('nos')
								self.tvh_picons('nos')
								tools.dvbc(kdvbc, nosnetwork)
							else:
								self.tvh_channels('nosfree')
								self.tvh_picons('nosfree')
								tools.dvbc(kdvbc, nosnetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
							self.tvh_channels('nowo')
							self.tvh_picons('nowo')
							tools.dvbc(kdvbc, nowonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
							self.tvh_channels('net')
							self.tvh_picons('net')
							tools.dvbc(kdvbc, netnetwork)
				elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbs', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbs = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
							self.tvh_channels('hispasat')
							self.tvh_picons('hispasat')
							tools.dvbs(kdvbs, hispanetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
							self.tvh_channels('astra')
							self.tvh_picons('astra')
							tools.dvbs(kdvbs, astranetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
							self.tvh_channels('hotbird')
							self.tvh_picons('hotbird')
							tools.dvbs(kdvbs, hotbirdnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
							self.tvh_channels('clarotv')
							self.tvh_picons('clarotv')
							tools.dvbs(kdvbs, claronetwork)
				elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbt', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbt = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
						self.tvh_channels('tdt')
						self.tvh_picons('tdt')
						tools.dvbt(kdvbt, tdtnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
						self.tvh_channels('meo')
						self.tvh_picons('meo')
						tools.dvbt(kdvbt, meonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
						self.tvh_channels('vodafone')
						self.tvh_picons('vodafone')
						tools.dvbt(kdvbt, vodafonenetwork)
			if tools.return_data('TVHWIZARD', 'STRING', 'k3pro', 2) == 1:
				if tools.return_data('TVHWIZARD', 'STRING', 'kdvbc', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbc = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
							if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
								self.tvh_channels('nos')
								self.tvh_picons('nos')
								tools.dvbc(kdvbc, nosnetwork)
							else:
								self.tvh_channels('nosfree')
								self.tvh_picons('nosfree')
								tools.dvbc(kdvbc, nosnetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
							self.tvh_channels('nowo')
							self.tvh_picons('nowo')
							tools.dvbc(kdvbc, nowonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
							self.tvh_channels('net')
							self.tvh_picons('net')
							tools.dvbc(kdvbc, netnetwork)
				elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbs', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbs = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
							self.tvh_channels('hispasat')
							self.tvh_picons('hispasat')
							tools.dvbs(kdvbs, hispanetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
							self.tvh_channels('astra')
							self.tvh_picons('astra')
							tools.dvbs(kdvbs, astranetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
							self.tvh_channels('hotbird')
							self.tvh_picons('hotbird')
							tools.dvbs(kdvbs, hotbirdnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
							self.tvh_channels('clarotv')
							self.tvh_picons('clarotv')
							tools.dvbs(kdvbs, claronetwork)
				elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbt', 2) == 1:
					ktuner = os.listdir(addontvhtuners)[0]
					kdvbt = "%s%s" % (addontvhtuners, ktuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
						self.tvh_channels('tdt')
						self.tvh_picons('tdt')
						tools.dvbt(kdvbt, tdtnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
						self.tvh_channels('meo')
						self.tvh_picons('meo')
						tools.dvbt(kdvbt, meonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
						self.tvh_channels('vodafone')
						self.tvh_picons('vodafone')
						tools.dvbt(kdvbt, vodafonenetwork)	
		elif tools.return_data('TVHWIZARD', 'STRING', 'khadas', 2) == 1:
			if tools.return_data('TVHWIZARD', 'STRING', 'kvim2', 2) == 1:
				if tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbc', 2) == 1:
					kvtvtuner = os.listdir(addontvhtuners)[0]
					kvtvdvbc = "%s%s" % (addontvhtuners, kvtvtuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
							self.tvh_channels('nos')
							self.tvh_picons('nos')
							tools.dvbc(kvtvdvbc, nosnetwork)
						else:
							self.tvh_channels('nosfree')
							self.tvh_picons('nosfree')
							tools.dvbc(kvtvdvbc, nosnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
						self.tvh_channels('nowo')
						self.tvh_picons('nowo')
						tools.dvbc(kvtvdvbc, nowonetwork)
				elif tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbs', 2) == 1:
					kvtvtuner = os.listdir(addontvhtuners)[0]
					kvtvdvbs = "%s%s" % (addontvhtuners, kvtvtuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
						self.tvh_channels('hispasat')
						self.tvh_picons('hispasat')
						tools.dvbs(kvtvdvbs, hispanetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
						self.tvh_channels('astra')
						self.tvh_picons('astra')
						tools.dvbs(kvtvdvbs, astranetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
						self.tvh_channels('hotbird')
						self.tvh_picons('hotbird')
						tools.dvbs(kvtvdvbs, hotbirdnetwork)
				elif tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbt', 2) == 1:
					kvtvtuner = os.listdir(addontvhtuners)[0]
					kvtvdvbt = "%s%s" % (addontvhtuners, kvtvtuner)
					if tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
						self.tvh_channels('tdt')
						self.tvh_picons('tdt')
						tools.dvbt(kvtvdvbt, tdtnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
						self.tvh_channels('meo')
						self.tvh_picons('meo')
						tools.dvbt(kvtvdvbt, meonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
						self.tvh_channels('vodafone')
						self.tvh_picons('vodafone')
						tools.dvbt(kvtvdvbt, vodafonenetwork)
		elif tools.return_data('TVHWIZARD', 'STRING', 'generic', 2) == 1:
			for tuner in os.listdir(addontvhtuners):
				tuners = addontvhtuners+tuner
				if tools.return_data('TVHWIZARD', 'STRING', 'usb', 2) == 1:
					if tools.return_data('TVHWIZARD', 'STRING', 'gdvbc', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
							if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
								self.tvh_channels('nos')
								self.tvh_picons('nos')
								tools.dvbc(tuners, nosnetwork)
							else:
								self.tvh_channels('nosfree')
								self.tvh_picons('nosfree')
								tools.dvbc(tuners, nosnetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
							self.tvh_channels('nowo')
							self.tvh_picons('nowo')
							tools.dvbc(tuners, nowonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbs', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
							self.tvh_channels('hispasat')
							self.tvh_picons('hispasat')
							tools.dvbs(tuners, hispanetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
							self.tvh_channels('astra')
							self.tvh_picons('astra')
							tools.dvbs(tuners, astranetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
							self.tvh_channels('hotbird')
							self.tvh_picons('hotbird')
							tools.dvbs(tuners, hotbirdnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbt', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
							self.tvh_channels('tdt')
							self.tvh_picons('tdt')
							tools.dvbt(tuners, tdtnetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
							self.tvh_channels('meo')
							self.tvh_picons('meo')
							tools.dvbt(tuners, meonetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
							self.tvh_channels('vodafone')
							self.tvh_picons('vodafone')
							tools.dvbt(tuners, vodafonenetwork)
				elif tools.return_data('TVHWIZARD', 'STRING', 'pcix', 2) == 1:
					if tools.return_data('TVHWIZARD', 'STRING', 'gdvbc', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
							if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
								self.tvh_channels('nos')
								self.tvh_picons('nos')
								tools.dvbc(tuners, nosnetwork)
							else:
								self.tvh_channels('nosfree')
								self.tvh_picons('nosfree')
								tools.dvbc(tuners, nosnetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
							self.tvh_channels('nowo')
							self.tvh_picons('nowo')
							tools.dvbc(tuners, nowonetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbs', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
							self.tvh_channels('hispasat')
							self.tvh_picons('hispasat')
							tools.dvbs(tuners, hispanetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
							self.tvh_channels('astra')
							self.tvh_picons('astra')
							tools.dvbs(tuners, astranetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
							self.tvh_channels('hotbird')
							self.tvh_picons('hotbird')
							tools.dvbs(tuners, hotbirdnetwork)
					elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbt', 2) == 1:
						if tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
							self.tvh_channels('tdt')
							self.tvh_picons('tdt')
							tools.dvbt(tuners, tdtnetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
							self.tvh_channels('meo')
							self.tvh_picons('meo')
							tools.dvbt(tuners, meonetwork)
						elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
							self.tvh_channels('vodafone')
							self.tvh_picons('vodafone')
							tools.dvbt(tuners, vodafonenetwork)

	def tvh_channels(self, path):

		url = '%s%s%s' % ("https://addons.tnds82.xyz/addon/tvhwizard/channels/", path, ".zip")
		url_version = '%s%s%s' % ("https://addons.tnds82.xyz/addon/tvhwizard/channels/", path, "version")
		tools.channels(url)
		header = "Channels"
		channelsFile = os.path.join('/tmp/tnds82', path, 'channel.zip')
		tools.extract(channelsFile,addontvhdest,dp,header)
		header1 = "Networks"
		if not os.path.exists(addontvhdvb):
			os.makedirs(addontvhdvb)
		networkFile = os.path.join('/tmp/tnds82', path, 'networks.zip')
		tools.extract(networkFile,addontvhdvb,dp,header1)
		subprocess_cmd('%s %s %s' % ('wget -O', addonchaver, url_version))

	def tvh_picons(self, path):

		url = '%s%s%s' % ("https://addons.tnds82.xyz/addon/tvhwizard/picons/", path, ".zip")
		tools.picons(url)
		### Image Cache ###
		if not os.path.exists(addontvhimgcache):
			os.makedirs(addontvhimgcache)
		imgcache = "%s%s" % (addontvhimgcache, "config")
		with open(imgcache, "w") as outfile:
			json.dump({'enabled':True, 'ignore_sslcert':False, 'ok_period': 168, 'fail_period': 24}, outfile, sort_keys=True, indent=4)

	def tvh_recording(self):		
		if tools.return_data('RECORDS', 'ID', 1, 1) == '':
			recordingpath = '/storage/recordings'
		else:
			recordingpath = tools.return_data('RECORDS', 'ID', 1, 1)

		if 'tndsdvr' in open(addontvhdefaultdvr).read():
			dialog.notification(addonname, langString(50070), xbmcgui.NOTIFICATION_WARNING, 2000)
		else:
			tools.addkeyjson(addontvhdefaultdvr, 'tndsdvr', 'true')
			if tools.return_data('TVHWIZARD', 'STRING', 'mkvprofile', 2) == 1:
				if 'Generic' in open(release).read():
					if tools.check_mkvprofile(6, addontvhprofile):
						tools.recording_profile(tools.check_mkvprofile(6, addontvhprofile),recordingpath, addontvhdvrconf, "Matroska")
					elif tools.check_mkvprofile(5, addontvhprofile):
						tools.recording_profile(tools.check_mkvprofile(5, addontvhprofile),recordingpath, addontvhdvrconf, "Matroska")
					elif tools.check_mkvprofile(4, addontvhprofile):
						tools.recording_profile(tools.check_mkvprofile(4, addontvhprofile),recordingpath, addontvhdvrconf, "Matroska")
					elif tools.check_mkvprofile(3, addontvhprofile):
						tools.recording_profile(tools.check_mkvprofile(3, addontvhprofile),recordingpath, addontvhdvrconf, "Matroska")
					elif tools.check_mkvprofile(2, addontvhprofile):
						tools.recording_profile(tools.check_mkvprofile(2, addontvhprofile),recordingpath, addontvhdvrconf, "Matroska")
					elif tools.check_mkvprofile(1, addontvhprofile):
						tools.recording_profile(tools.check_mkvprofile(1, addontvhprofile),recordingpath, addontvhdvrconf, "Matroska")
					elif tools.check_mkvprofile(0, addontvhprofile):
						tools.recording_profile(tools.check_mkvprofile(0, addontvhprofile),recordingpath, addontvhdvrconf, "Matroska")
				else:
					if tools.check_mkvprofile(2, addontvhprofile):
						tools.recording_profile(tools.check_mkvprofile(2, addontvhprofile),recordingpath, addontvhdvrconf, "Matroska")
					elif tools.check_mkvprofile(1, addontvhprofile):
						tools.recording_profile(tools.check_mkvprofile(1, addontvhprofile),recordingpath, addontvhdvrconf, "Matroska")
					elif tools.check_mkvprofile(0, addontvhprofile):
						tools.recording_profile(tools.check_mkvprofile(0, addontvhprofile),recordingpath, addontvhdvrconf, "Matroska")

				if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
					if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
						if tools.return_data('USERS', 'ID', 2, 1) == 'tvhadmin':
							adminuserpath = os.path.join(addontvhdest, 'accesscontrol/90989e141bf7c77bcaecaef8da1e0054')
							tools.addkeyjson(adminuserpath, 'dvr_config', ['42c91dae1ea94fbc2a46d456491b4179'])
						else:
							userdefault = os.listdir(addontvhacontrol)[0]
							defaultuser = "%s%s" % (addontvhacontrol, userdefault)
							tools.addkeyjson(defaultuser, 'dvr_config', ['42c91dae1ea94fbc2a46d456491b4179'])
						if tools.return_data('USERS', 'ID', 3, 1) == 'tvhclient':
							clientuserpath = os.path.join(addontvhdest, 'accesscontrol/95275ba5e99a33a72b5081c870e179d8')
							tools.addkeyjson(clientuserpath, 'dvr_config', ['42c91dae1ea94fbc2a46d456491b4179'])
					else:
						if tools.return_data('USERS', 'ID', 1, 1) == 'tvhadmin':
							adminuserpath = os.path.join(addontvhdest, 'accesscontrol/90989e141bf7c77bcaecaef8da1e0054')
							tools.addkeyjson(adminuserpath, 'dvr_config', ['42c91dae1ea94fbc2a46d456491b4179'])
						else:
							userdefault = os.listdir(addontvhacontrol)[0]
							defaultuser = "%s%s" % (addontvhacontrol, userdefault)
							tools.addkeyjson(defaultuser, 'dvr_config', ['42c91dae1ea94fbc2a46d456491b4179'])
						if tools.return_data('USERS', 'ID', 2, 1) == 'tvhclient':
							clientuserpath = os.path.join(addontvhdest, 'accesscontrol/95275ba5e99a33a72b5081c870e179d8')
							tools.addkeyjson(clientuserpath, 'dvr_config', ['42c91dae1ea94fbc2a46d456491b4179'])
				elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
					if tools.return_data('USERS', 'ID', 1, 1) == 'tvhadmin':
						adminuserpath = os.path.join(addontvhdest, 'accesscontrol/90989e141bf7c77bcaecaef8da1e0054')
						tools.addkeyjson(adminuserpath, 'dvr_config', ['42c91dae1ea94fbc2a46d456491b4179'])
					else:
						userdefault = os.listdir(addontvhacontrol)[0]
						defaultuser = "%s%s" % (addontvhacontrol, userdefault)
						tools.addkeyjson(defaultuser, 'dvr_config', ['42c91dae1ea94fbc2a46d456491b4179'])
					if tools.return_data('USERS', 'ID', 2, 1) == 'tvhclient':
						clientuserpath = os.path.join(addontvhdest, 'accesscontrol/95275ba5e99a33a72b5081c870e179d8')
						tools.addkeyjson(clientuserpath, 'dvr_config', ['42c91dae1ea94fbc2a46d456491b4179'])

	def tvh_pvr(self):
		pvruser  = tools.return_data('PVR', 'PROGRAM', 'tvh_htsp', 2)
		pvrpass  = tools.return_data('PVR', 'PROGRAM', 'tvh_htsp', 3)
		pvripbox = tools.return_data('PVR', 'PROGRAM', 'tvh_htsp', 4)

		if not os.path.exists(addonpvrtvhdata):
			os.makedirs(addonpvrtvhdata)
		if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
			if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
				if tools.return_data('USERS', 'ID', 2, 1) == 'tvhadmin':
					tools.pvrsettings(addonpvrtvhsettings, pvripbox, pvrpass, pvruser)
				else:
					tools.pvrsettings(addonpvrtvhsettings, pvripbox, '', '')
			else:
				if tools.return_data('USERS', 'ID', 1, 1) == 'tvhadmin':
					tools.pvrsettings(addonpvrtvhsettings, pvripbox, pvrpass, pvruser)
				else:
					tools.pvrsettings(addonpvrtvhsettings, pvripbox, '', '')
		elif tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
			if tools.return_data('USERS', 'ID', 1, 1) == 'tvhadmin':
				tools.pvrsettings(addonpvrtvhsettings, pvripbox, pvrpass, pvruser)
			else:
				tools.pvrsettings(addonpvrtvhsettings, pvripbox, '', '')
		#Enable Live TV
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled","value":true},"id":1}')

	def kodi_config(self):
		if os.path.exists(advanced):
			dialog.notification(addonname, langString(50072), xbmcgui.NOTIFICATION_WARNING, 2000)
		else:
			#channel group
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.usebackendchannelnumbers","value":true},"id":1}')
			#Video 16:9
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"videoplayer.stretch43","value":4},"id":1}')

