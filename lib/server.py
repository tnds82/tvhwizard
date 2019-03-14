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
addonlog    = os.path.join(addondata, 'data/')
addonchaver = os.path.join(addonlog, 'version')
addonicon   = os.path.join(addonfolder, 'resources/icon.png')


	##### ADDON SERVICE TVHEADEND #####
addontvh       = xbmcaddon.Addon(id='service.tvheadend42')
addontvhname   = addontvh.getAddonInfo('name')
addontvhfolder = addontvh.getAddonInfo('path')

	##### ADDON PVR TVHEADEND CLIENT #####
addonpvrtvh         = xbmcaddon.Addon(id='pvr.hts')
addonpvrtvhname     = addonpvrtvh.getAddonInfo('name')
addonpvrtvhfolder   = addonpvrtvh.getAddonInfo('path')
addonpvrtvhdata     = xbmc.translatePath(addonpvrtvh.getAddonInfo('profile'))
addonpvrtvhsettings = os.path.join(addonpvrtvhdata, 'settings.xml')

	##### DESTINATION #####
addontvhdest       = xbmc.translatePath(addontvh.getAddonInfo('profile'))
addontvhchannel    = os.path.join(addontvhdest, 'channel')
addontvhdvb        = os.path.join(addontvhdest, 'input/dvb')
addontvhconfig     = os.path.join(addontvhdest, 'config')
addontvhsettings   = os.path.join(addontvhdest, 'settings.xml')
addontvhdvbapi     = os.path.join(addontvhdest, 'caclient/')
addontvhtuners     = os.path.join(addontvhdest, 'input/linuxdvb/adapters/')
addontvhacontrol   = os.path.join(addontvhdest, 'accesscontrol/')
addontvhpass       = os.path.join(addontvhdest, 'passwd/')
addontvhdefaultdvr = os.path.join(addontvhdest, 'dvr/config/8d0f5b7ae354d956d7fe5db25f5d0d24')
addontvhdvrconf    = os.path.join(addontvhdest, 'dvr/config/')
addontvhprofile    = os.path.join(addontvhdest, 'profile/')
addontvhimgcache   = os.path.join(addontvhdest, 'imagecache/')
addontvhimgmeta    = os.path.join(addontvhdest, 'imagecache/meta')
addontvhtimeconf   = os.path.join(addontvhdest, 'timeshift/config')
addontvhtime       = os.path.join(addontvhdest, 'timeshift/')

	##### PICONS #####
piconpath    = "/storage/.kodi/userdata/picons/*"
piconsympath = "/storage/picons/vdr/"

	##### DVBAPI #####
dvbapifile = os.path.join(addontvhdest, 'caclient/6fe6f142570588eb975ddf49861ce970')
dvbapip    = addon.getSetting('ipdvbapi')
dvbapiport = addon.getSetting('portdvbapi')

	##### NEWCAMD #####
newcamdhost = addon.getSetting('newcamdhost')
newcamdpass = addon.getSetting('newcamdpass')
newcamdport = addon.getSetting('newcamdport')
newcamduser = addon.getSetting('newcamduser')


   ##### USERS #####
adminuser  = addon.getSetting('useradmin')
adminpass  = addon.getSetting('passadmin')
clientuser = addon.getSetting('userclient')
clientpass = addon.getSetting('passclient')

   ##### Recording #####
recordingpath = addon.getSetting('pathrecording')

   ##### PVR #####
ipbox = addon.getSetting('ipbox')

   ##### USERDATA #####
userdata = os.path.join("/storage/.kodi/userdata/")
advanced = os.path.join(userdata, 'advancedsettings.xml')

######################### MENUS PLUGIN ###############################

def langString(id):
	return addon.getLocalizedString(id)

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout

##### CONFIGURATION #####
def tvh_config():
	if '"tndsconfig":' in open(addontvhconfig).read():
		dialog.notification(addonname, langString(50061), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:

			tools.changekeyjson(addontvhconfig, 'wizard', 'tndsconfig')

			#expert mode
			if addon.getSetting('tvhexpert') == 'true':
				tools.updateJsonFile(addontvhconfig, 'uilevel', 2)

			#web language
			if addon.getSetting('languipt') == 'true':
				tools.addkeyjson(addontvhconfig, 'language_ui', "por")
			
			if addon.getSetting('languien') == 'true':
				tools.addkeyjson(addontvhconfig, 'language_ui', "eng")

			#epg language
			if addon.getSetting('langepg') == 'true':
				tools.addkeyjson(addontvhconfig, 'language', ['por','eng'])
				if addon.getSetting('langepgen') == 'false':
					tools.addkeyjson(addontvhconfig, 'language', ['por'])
				elif addon.getSetting('langepgpt') == 'false':
					tools.addkeyjson(addontvhconfig, 'language', ['eng'])

##### USERS #####
def tvh_users():
	userdefault = os.listdir(addontvhacontrol)[0]
	defaultuser = "%s%s" % (addontvhacontrol, userdefault)
	if not 'Default access entry' in open(defaultuser).read():
		dialog.notification(addonname, langString(50069), xbmcgui.NOTIFICATION_WARNING, 5000)
	else:
		# Create administrator user with password
		if addon.getSetting('logadmin') == 'true':
			# Disable Default access entry
			tools.updateJsonFile(defaultuser, 'enabled', False)
			tools.updateJsonFile(addontvhconfig, 'digest', 2)
			
			adminpath = "%s%s" % (addontvhacontrol, "90989e141bf7c77bcaecaef8da1e0054")			
			with open(adminpath, "w") as outfile:
				json.dump({'enabled':True, 'username':adminuser, 
					'change':['change_rights'], 'uilevel':2, 'streaming':['basic', 'advanced', 'htsp'], 
					'dvr':['basic','htsp','all','all_rw','failed'], 'webui':True, 'admin':True, 
					'comment':'Administrator access entry'}, outfile, indent=4)
			
			# Create Admin Password
			newpath = addontvhpass
			if not os.path.exists(newpath):
				os.makedirs(newpath)
			
			#enconde pass
			encoded = base64.b64encode(adminpass)
			tvhpass = "VFZIZWFkZW5kLUhpZGUt"
			passenconded = "%s%s" % (tvhpass, encoded)

			#create pass
			passadmin = "%s%s" % (addontvhpass, "cb77ac54d4e6d859c1890b770f9fbe3a")
			with open(passadmin, "w") as outfile:
				json.dump({'enabled':True, 'username':adminuser, 'password2':passenconded, 
					'comment':'Pass of Adminstrator', 'wizard':False}, outfile, sort_keys=True, indent=4)

	# Create client user with password
	if addon.getSetting('logclient') == 'true':
			if addon.getSetting('userclient') == '':
				userclient = '*'
			else:
				userclient = clientuser
				
				# Create Client Password
				newpath = addontvhpass
				if not os.path.exists(newpath):
					os.makedirs(newpath)
				
				#enconde pass	
				encoded = base64.b64encode(clientpass)
				tvhpass = "VFZIZWFkZW5kLUhpZGUt"
				passenconded = "%s%s" % (tvhpass, encoded)
				
				#create pass
				passadmin = "%s%s" % (addontvhpass, "8597d99ed41fe710bff95567a24372ba")
				with open(passadmin, "w") as outfile:
					json.dump({'enabled':True, 'username':clientuser, 'password2':passenconded, 
						'comment':'Pass of Client', 'wizard':False}, outfile, sort_keys=True, indent=4)

			# Create user client
			clientpath = "%s%s" % (addontvhacontrol, "95275ba5e99a33a72b5081c870e179d8")
			with open(clientpath, "w") as outfile:
				json.dump({'enabled':True, 'username':userclient, 
					'change':['change_rights'], 'streaming':['basic', 'advanced', 'htsp'], 
					'dvr':['basic','htsp','all','all_rw','failed'], 'webui':True,
					'comment':'Client access entry'}, outfile, indent=4)

##### DVBAPI #####
def tvh_dvbapi():
	if os.path.exists(dvbapifile):
		dialog.notification(addonname, langString(50062), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		defaultdvbapi = os.listdir(addontvhdvbapi)[0]
		dvbapidefault = "%s%s" % (addontvhdvbapi, defaultdvbapi)
		tools.updateJsonFile(dvbapidefault, 'enabled', False)

#		addontvh.setSetting(id='PRELOAD_CAPMT_CA', value='true')

		if addon.getSetting('dvbapichoose') == 'newcamd':
			if addon.getSetting('deskey1') == 'true':
				with open(dvbapifile, "w") as outfile:
					json.dump({'deskey':'01:02:03:04:05:06:07:08:09:10:11:12:13:14', 'username':newcamduser, 'password':newcamdpass, 'hostname':newcamdhost, 'port':newcamdport,
						'emm':True, 'emmex':True, 'keepalive_interval':30, 'class':'caclient_cwc', 'index':1, 'enabled':True, 'name':'tvh'}, outfile, sort_keys=True, indent=4)
			if addon.getSetting('deskey2') == 'true':
				with open(dvbapifile, "w") as outfile:
					json.dump({'deskey':'10:10:10:10:10:10:10:10:10:10:11:12:13:14', 'username':newcamduser, 'password':newcamdpass, 'hostname':newcamdhost, 'port':newcamdport,
						'emm':True, 'emmex':True, 'keepalive_interval':30, 'class':'caclient_cwc', 'index':1, 'enabled':True, 'name':'tvh'}, outfile, sort_keys=True, indent=4)

		
		#oscam pc-nodmx
		if addon.getSetting('dvbapichoose') == 'pc-nodmx':
#			if not os.path.exists(addontvhdvbapi):
#				os.makedirs(addontvhdvbapi)

			with open(dvbapifile, "w") as outfile:
				json.dump({'mode':4, 'camdfilename':'/tmp/camd.socket', 'port':0, 'class':'caclient_capmt', 
					'index':1, 'enabled':True, 'name':'tvh'}, outfile, sort_keys=True, indent=4)
		
		#oscam pc
		if addon.getSetting('dvbapichoose') == 'pc':
#			if not os.path.exists(addontvhdvbapi):
#				os.makedirs(addontvhdvbapi)

			with open(dvbapifile, "w") as outfile:
				json.dump({'mode':5, 'camdfilename':dvbapip, 'port':dvbapiport, 'class':'caclient_capmt', 
					'index':1, 'enabled':True, 'name':'tvh'}, outfile, sort_keys=True, indent=4)

##### ADD CHANNELS #####
def tvh_channels(path):

	url = '%s%s%s' % ("https://addons.tnds82.xyz/tvhwizard/channels/", path, ".zip")
	url_version = '%s%s%s' % ("https://addons.tnds82.xyz/tvhwizard/channels/", path, "version")
	tools.channels(url)
	header = "Channels"
	channelsFile = os.path.join('/tmp/tnds82', path, 'channel.zip')
	tools.extract(channelsFile,addontvhdest,dp,header)
	header1 = "Networks"
	if not os.path.exists(addontvhdvb):
		os.makedirs(addontvhdvb)
	networkFile = os.path.join('/tmp/tnds82', path, 'networks.zip')
	tools.extract(networkFile,addontvhdvb,dp,header1)
	header = "Image Cache"
	imgcacheFile = os.path.join('/tmp/tnds82', path, 'meta.zip')
	tools.extract(imgcacheFile,addontvhimgcache,dp,header)
	if not os.path.exists(addonlog):
		os.makedirs(addonlog)
	subprocess_cmd('%s %s %s' % ('wget -O', addonchaver, url_version))

##### PICONS #####
def tvh_picons(path):

	url = '%s%s%s' % ("https://addons.tnds82.xyz/tvhwizard/picons/", path, ".zip")
	tools.picons(url, path)

	### Image Cache ###
	imgcachepath = addontvhimgcache
	if not os.path.exists(imgcachepath):
		os.makedirs(imgcachepath)
	imgcache = "%s%s" % (addontvhimgcache, "config")
	with open(imgcache, "w") as outfile:
		json.dump({'enabled':True, 'ignore_sslcert':False, 'ok_period': 168, 'fail_period': 24}, outfile, sort_keys=True, indent=4)
				
##### DVB INPUTS #####
def tvh_tunners():
	nosnetwork      = "d2e2dd7ba943289f15a46ee502e13b12"
	nowonetwork     = "00e7faf22eece16481b49486b74d81e2"
	tdtnetwork      = "3b71a44c08543bd024fad8630f745d60"
	meonetwork      = "f7fcf1c68e088087ed89c5214264e876"
	vodafonenetwork = "fd3e986178c77d3687b337718c332a39"
	hispanetwork    = "1c2f2758a410776103317afc11abbc8e"
	claronetwork    = "87f9a21e2b1b98c057c424d7ab4cd9c9"
	netnetwork      = "099f5b5ce2a8edb9f41b63481fdaf52b"
#	astranetwork    = "b49667f409cd90d954431ce14ea69405"
#	hotbirdnetwork  = ""

	
	if addon.getSetting('wetek') == 'true':
		if addon.getSetting('wetekplay') == 'true':
			if addon.getSetting('wdvbc') == 'true':
				wetektuner = os.listdir(addontvhtuners)[0]
				wdvbc = "%s%s" % (addontvhtuners, wetektuner)
				if addon.getSetting('nos') == 'true':
					if addon.getSetting('start') == 'tvhwosc':
						tvh_channels('nos')
						tvh_picons('nos')
						tools.dvbc(wdvbc, nosnetwork)
					else:
						tvh_channels('nosfree')
						tvh_picons('nosfree')
						tools.dvbc(wdvbc, nosnetwork)
				elif addon.getSetting('nowo') == 'true':
					tvh_channels('nowo')
					tvh_picons('nowo')
					tools.dvbc(wdvbc, nowonetwork)
			elif addon.getSetting('wdvbs') == 'true':
				wetektuners1 = os.listdir(addontvhtuners)[0]
				wdvbs1 = "%s%s" % (addontvhtuners, wetektuners1)
				wetektuners2 = os.listdir(addontvhtuners)[1]
				wdvbs2 = "%s%s" % (addontvhtuners, wetektuners2)
				if addon.getSetting('wplnb1') == 'true':
					if addon.getSetting('hispasat') == 'true':
						tvh_channels('hispasat')
						tvh_picons('hispasat')
						if '/dev/dvb/adapter0' in open(wdvbs1).read():
							tools.dvbs(wdvbs1, hispanetwork)
						if '/dev/dvb/adapter0' in open(wdvbs2).read():
							tools.dvbs(wdvbs2, hispanetwork)
					elif addon.getSetting('astra') == 'true':
						tvh_channels('astra')
						tvh_picons('astra')
						if '/dev/dvb/adapter0' in open(wdvbs1).read():
							tools.dvbs(wdvbs1, astranetwork)
						if '/dev/dvb/adapter0' in open(wdvbs2).read():
							tools.dvbs(wdvbs2, astranetwork)
					elif addon.getSetting('hotbird') == 'true':
						tvh_channels('hotbird')
						tvh_picons('hotbird')
						if '/dev/dvb/adapter0' in open(wdvbs1).read():
							tools.dvbs(wdvbs1, hotbirdnetwork)
						if '/dev/dvb/adapter0' in open(wdvbs2).read():
							tools.dvbs(wdvbs2, astranetwork)
				elif addon.getSetting('wplnb2') == 'true':
					if addon.getSetting('hispasat') == 'true':
						tvh_channels('hispasat')
						tvh_picons('hispasat')
						if '/dev/dvb/adapter1' in open(wdvbs1).read():
							tools.dvbs(wdvbs1, hispanetwork)
						if '/dev/dvb/adapter1' in open(wdvbs2).read():
							tools.dvbs(wdvbs2, hispanetwork)
					elif addon.getSetting('astra') == 'true':
						tvh_channels('astra')
						tvh_picons('astra')
						if '/dev/dvb/adapter1' in open(wdvbs1).read():
							tools.dvbs(wdvbs1, astranetwork)
						if '/dev/dvb/adapter1' in open(wdvbs2).read():
							tools.dvbs(wdvbs2, astranetwork)
					elif addon.getSetting('hotbird') == 'true':
						tvh_channels('hotbird')
						tvh_picons('hotbird')
						if '/dev/dvb/adapter1' in open(wdvbs1).read():
							tools.dvbs(wdvbs1, hotbirdnetwork)
						if '/dev/dvb/adapter1' in open(wdvbs2).read():
							tools.dvbs(wdvbs2, astranetwork)
				elif addon.getSetting('wplnboth') == 'true':
					if addon.getSetting('hispasat') == 'true':
						tvh_channels('hispasat')
						tvh_picons('hispasat')
						tools.dvbs(wdvbs1, hispanetwork)
						tools.dvbs(wdvbs2, hispanetwork)
					elif addon.getSetting('astra') == 'true':
						tvh_channels('astra')
						tvh_picons('astra')
						tools.dvbs(wdvbs1, astranetwork)
						tools.dvbs(wdvbs2, astranetwork)
					elif addon.getSetting('hotbird') == 'true':
						tvh_channels('hotbird')
						tvh_picons('hotbird')
						tools.dvbs(wdvbs1, hotbirdnetwork)
						tools.dvbs(wdvbs2, astranetwork)
			elif addon.getSetting('wdvbt') == 'true':
				wetektuner = os.listdir(addontvhtuners)[0]
				wdvbt = "%s%s" % (addontvhtuners, wetektuner)
				if addon.getSetting('tdt') == 'true':
					tvh_channels('tdt')
					tvh_picons('tdt')
					tools.dvbt(wdvbt, tdtnetwork)
				elif addon.getSetting('meo') == 'true':
					tvh_channels('meo')
					tvh_picons('meo')
					tools.dvbt(wdvbt, meonetwork)
				elif addon.getSetting('vodafone') == 'true':
					tvh_channels('vodafone')
					tvh_picons('vodafone')
					tools.dvbt(wdvbt, vodafonenetwork)
		elif addon.getSetting('wetekplay2') == 'true':
			if addon.getSetting('wdvbc') == 'true':
				wetek2tuner = os.listdir(addontvhtuners)[0]
				w2dvbc = "%s%s" % (addontvhtuners, wetek2tuner)
				if addon.getSetting('nos') == 'true':
					if addon.getSetting('start') == 'tvhwosc':
						tvh_channels('nos')
						tvh_picons('nos')
						tools.dvbc(w2dvbc, nosnetwork)
					else:
						tvh_channels('nosfree')
						tvh_picons('nosfree')
						tools.dvbc(w2dvbc, nosnetwork)
				elif addon.getSetting('nowo') == 'true':
					tvh_channels('nowo')
					tvh_picons('nowo')
					tools.dvbc(w2dvbc, nowonetwork)
			elif addon.getSetting('wdvbs') == 'true':
				wetek2tuners = os.listdir(addontvhtuners)[0]
				w2dvbs = "%s%s" % (addontvhtuners, wetek2tuners)
				if addon.getSetting('hispasat') == 'true':
					tvh_channels('hispasat')
					tvh_picons('hispasat')
					tools.dvbs(w2dvbs, hispanetwork)
				elif addon.getSetting('astra') == 'true':
					tvh_channels('astra')
					tvh_picons('astra')
					tools.dvbs(w2dvbs, astranetwork)
				elif addon.getSetting('hotbird') == 'true':
					tvh_channels('hotbird')
					tvh_picons('hotbird')
					tools.dvbs(w2dvbs, hotbirdnetwork)
			elif addon.getSetting('wdvbt') == 'true':
				wetek2tuner = os.listdir(addontvhtuners)[0]
				w2dvbt = "%s%s" % (addontvhtuners, wetek2tuner)
				if addon.getSetting('tdt') == 'true':
					tvh_channels('tdt')
					tvh_picons('tdt')
					tools.dvbt(w2dvbt, tdtnetwork)
				elif addon.getSetting('meo') == 'true':
					tvh_channels('meo')
					tvh_picons('meo')
					tools.dvbt(w2dvbt, meonetwork)
				elif addon.getSetting('vodafone') == 'true':
					tvh_channels('vodafone')
					tvh_picons('vodafone')
					tools.dvbt(w2dvbt, vodafonenetwork)
#		elif addon.getSetting('wetekplay2s') == 'true':
	elif addon.getSetting('k') == 'true':
		if addon.getSetting('k1plus') == 'true':
			if addon.getSetting('kdvbc') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbc = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('nos') == 'true':
					if addon.getSetting('start') == 'tvhwosc':
						tvh_channels('nos')
						tvh_picons('nos')
						tools.dvbc(kdvbc, nosnetwork)
					else:
						tvh_channels('nosfree')
						tvh_picons('nosfree')
						tools.dvbc(kdvbc, nosnetwork)
				elif addon.getSetting('nowo') == 'true':
					tvh_channels('nowo')
					tvh_picons('nowo')
					tools.dvbc(kdvbc, nowonetwork)
			elif addon.getSetting('kdvbs') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbs = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('hispasat') == 'true':
					tvh_channels('hispasat')
					tvh_picons('hispasat')
					tools.dvbs(kdvbs, hispanetwork)
				elif addon.getSetting('astra') == 'true':
					tvh_channels('astra')
					tvh_picons('astra')
					tools.dvbs(kdvbs, astranetwork)
				elif addon.getSetting('hotbird') == 'true':
					tvh_channels('hotbird')
					tvh_picons('hotbird')
					tools.dvbs(kdvbs, hotbirdnetwork)
			elif addon.getSetting('kdvbt') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbt = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('tdt') == 'true':
					tvh_channels('tdt')
					tvh_picons('tdt')
					tools.dvbt(kdvbt, tdtnetwork)
				elif addon.getSetting('meo') == 'true':
					tvh_channels('meo')
					tvh_picons('meo')
					tools.dvbt(kdvbt, meonetwork)
				elif addon.getSetting('vodafone') == 'true':
					tvh_channels('vodafone')
					tvh_picons('vodafone')
					tools.dvbt(kdvbt, vodafonenetwork)
#			elif addon.getSetting('kdvbts') == 'true':
#			elif addon.getSetting('kdvbcs') == 'true':
		if addon.getSetting('k1pro') == 'true':
			if addon.getSetting('kdvbc') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbc = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('nos') == 'true':
					if addon.getSetting('start') == 'tvhwosc':
						tvh_channels('nos')
						tvh_picons('nos')
						tools.dvbc(kdvbc, nosnetwork)
					else:
						tvh_channels('nosfree')
						tvh_picons('nosfree')
						tools.dvbc(kdvbc, nosnetwork)
				elif addon.getSetting('nowo') == 'true':
					tvh_channels('nowo')
					tvh_picons('nowo')
					tools.dvbc(kdvbc, nowonetwork)
			elif addon.getSetting('kdvbs') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbs = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('hispasat') == 'true':
					tvh_channels('hispasat')
					tvh_picons('hispasat')
					tools.dvbs(kdvbs, hispanetwork)
				elif addon.getSetting('astra') == 'true':
					tvh_channels('astra')
					tvh_picons('astra')
					tools.dvbs(kdvbs, astranetwork)
				elif addon.getSetting('hotbird') == 'true':
					tvh_channels('hotbird')
					tvh_picons('hotbird')
					tools.dvbs(kdvbs, hotbirdnetwork)
			elif addon.getSetting('kdvbt') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbt = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('tdt') == 'true':
					tvh_channels('tdt')
					tvh_picons('tdt')
					tools.dvbt(kdvbt, tdtnetwork)
				elif addon.getSetting('meo') == 'true':
					tvh_channels('meo')
					tvh_picons('meo')
					tools.dvbt(kdvbt, meonetwork)
				elif addon.getSetting('vodafone') == 'true':
					tvh_channels('vodafone')
					tvh_picons('vodafone')
					tools.dvbt(kdvbt, vodafonenetwork)
#			elif addon.getSetting('kdvbts') == 'true':
#			elif addon.getSetting('kdvbcs') == 'true':
		if addon.getSetting('k2pro') == 'true':
			if addon.getSetting('kdvbc') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbc = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('nos') == 'true':
					if addon.getSetting('start') == 'tvhwosc':
						tvh_channels('nos')
						tvh_picons('nos')
						tools.dvbc(kdvbc, nosnetwork)
					else:
						tvh_channels('nosfree')
						tvh_picons('nosfree')
						tools.dvbc(kdvbc, nosnetwork)
				elif addon.getSetting('nowo') == 'true':
					tvh_channels('nowo')
					tvh_picons('nowo')
					tools.dvbc(kdvbc, nowonetwork)
			elif addon.getSetting('kdvbs') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbs = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('hispasat') == 'true':
					tvh_channels('hispasat')
					tvh_picons('hispasat')
					tools.dvbs(kdvbs, hispanetwork)
				elif addon.getSetting('astra') == 'true':
					tvh_channels('astra')
					tvh_picons('astra')
					tools.dvbs(kdvbs, astranetwork)
				elif addon.getSetting('hotbird') == 'true':
					tvh_channels('hotbird')
					tvh_picons('hotbird')
					tools.dvbs(kdvbs, hotbirdnetwork)
			elif addon.getSetting('kdvbt') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbt = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('tdt') == 'true':
					tvh_channels('tdt')
					tvh_picons('tdt')
					tools.dvbt(kdvbt, tdtnetwork)
				elif addon.getSetting('meo') == 'true':
					tvh_channels('meo')
					tvh_picons('meo')
					tools.dvbt(kdvbt, meonetwork)
				elif addon.getSetting('vodafone') == 'true':
					tvh_channels('vodafone')
					tvh_picons('vodafone')
					tools.dvbt(kdvbt, vodafonenetwork)
#			elif addon.getSetting('kdvbts') == 'true':
#			elif addon.getSetting('kdvbcs') == 'true':
		if addon.getSetting('k3pro') == 'true':
			if addon.getSetting('kdvbc') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbc = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('nos') == 'true':
					if addon.getSetting('start') == 'tvhwosc':
						tvh_channels('nos')
						tvh_picons('nos')
						tools.dvbc(kdvbc, nosnetwork)
					else:
						tvh_channels('nosfree')
						tvh_picons('nosfree')
						tools.dvbc(kdvbc, nosnetwork)
				elif addon.getSetting('nowo') == 'true':
					tvh_channels('nowo')
					tvh_picons('nowo')
					tools.dvbc(kdvbc, nowonetwork)
			elif addon.getSetting('kdvbs') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbs = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('hispasat') == 'true':
					tvh_channels('hispasat')
					tvh_picons('hispasat')
					tools.dvbs(kdvbs, hispanetwork)
				elif addon.getSetting('astra') == 'true':
					tvh_channels('astra')
					tvh_picons('astra')
					tools.dvbs(kdvbs, astranetwork)
				elif addon.getSetting('hotbird') == 'true':
					tvh_channels('hotbird')
					tvh_picons('hotbird')
					tools.dvbs(kdvbs, hotbirdnetwork)
			elif addon.getSetting('kdvbt') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbt = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('tdt') == 'true':
					tvh_channels('tdt')
					tvh_picons('tdt')
					tools.dvbt(kdvbt, tdtnetwork)
				elif addon.getSetting('meo') == 'true':
					tvh_channels('meo')
					tvh_picons('meo')
					tools.dvbt(kdvbt, meonetwork)
				elif addon.getSetting('vodafone') == 'true':
					tvh_channels('vodafone')
					tvh_picons('vodafone')
					tools.dvbt(kdvbt, vodafonenetwork)
#			elif addon.getSetting('kdvbts') == 'true':
#			elif addon.getSetting('kdvbcs') == 'true':
	elif addon.getSetting('generic') == 'true':
		for tuner in os.listdir(addontvhtuners):
			tuners = addontvhtuners+tuner
			if addon.getSetting('usb') == 'true':
				if addon.getSetting('gdvbc') == 'true':
					if addon.getSetting('nos') == 'true':
						if addon.getSetting('start') == 'tvhwosc':
							tvh_channels('nos')
							tvh_picons('nos')
							tools.dvbc(tuners, nosnetwork)
						else:
							tvh_channels('nosfree')
							tvh_picons('nosfree')
							tools.dvbc(tuners, nosnetwork)
					elif addon.getSetting('nowo') == 'true':
						tvh_channels('nowo')
						tvh_picons('nowo')
						tools.dvbc(tuners, nowonetwork)
				elif addon.getSetting('gdvbs') == 'true':
					if addon.getSetting('hispasat') == 'true':
						tvh_channels('hispasat')
						tvh_picons('hispasat')
						tools.dvbs(tuners, hispanetwork)
					elif addon.getSetting('astra') == 'true':
						tvh_channels('astra')
						tvh_picons('astra')
						tools.dvbs(tuners, astranetwork)
					elif addon.getSetting('hotbird') == 'true':
						tvh_channels('hotbird')
						tvh_picons('hotbird')
						tools.dvbs(tuners, hotbirdnetwork)
				elif addon.getSetting('gdvbt') == 'true':
					if addon.getSetting('tdt') == 'true':
						tvh_channels('tdt')
						tvh_picons('tdt')
						tools.dvbt(tuners, tdtnetwork)
					elif addon.getSetting('meo') == 'true':
						tvh_channels('meo')
						tvh_picons('meo')
						tools.dvbt(tuners, meonetwork)
					elif addon.getSetting('vodafone') == 'true':
						tvh_channels('vodafone')
						tvh_picons('vodafone')
						tools.dvbt(tuners, vodafonenetwork)
			elif addon.getSetting('pcix') == 'true':
				if addon.getSetting('gdvbc') == 'true':
					if addon.getSetting('nos') == 'true':
						if addon.getSetting('start') == 'tvhwosc':
							tvh_channels('nos')
							tvh_picons('nos')
							tools.dvbc(tuners, nosnetwork)
						else:
							tvh_channels('nosfree')
							tvh_picons('nosfree')
							tools.dvbc(tuners, nosnetwork)
					elif addon.getSetting('nowo') == 'true':
						tvh_channels('nowo')
						tvh_picons('nowo')
						tools.dvbc(tuners, nowonetwork)
				elif addon.getSetting('gdvbs') == 'true':
					if addon.getSetting('hispasat') == 'true':
						tvh_channels('hispasat')
						tvh_picons('hispasat')
						tools.dvbs(tuners, hispanetwork)
					elif addon.getSetting('astra') == 'true':
						tvh_channels('astra')
						tvh_picons('astra')
						tools.dvbs(tuners, astranetwork)
					elif addon.getSetting('hotbird') == 'true':
						tvh_channels('hotbird')
						tvh_picons('hotbird')
						tools.dvbs(tuners, hotbirdnetwork)
				elif addon.getSetting('gdvbt') == 'true':
					if addon.getSetting('tdt') == 'true':
						tvh_channels('tdt')
						tvh_picons('tdt')
						tools.dvbt(tuners, tdtnetwork)
					elif addon.getSetting('meo') == 'true':
						tvh_channels('meo')
						tvh_picons('meo')
						tools.dvbt(tuners, meonetwork)
					elif addon.getSetting('vodafone') == 'true':
						tvh_channels('vodafone')
						tvh_picons('vodafone')
						tools.dvbt(tuners, vodafonenetwork)
	elif addon.getSetting('brasil') == 'true':
		if addon.getSetting('k1plus') == 'true':
			if addon.getSetting('kdvbc') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbc = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('net') == 'true':
					tvh_channels('net')
					tvh_picons('net')
					tools.dvbc(kdvbc, netnetwork)
			elif addon.getSetting('kdvbs') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbs = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('clarotv') == 'true':
					tvh_channels('clarotv')
					tvh_picons('clarotv')
					tools.dvbs(kdvbs, claronetwork)
		if addon.getSetting('k1pro') == 'true':
			if addon.getSetting('kdvbc') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbc = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('net') == 'true':
					tvh_channels('net')
					tvh_picons('net')
					tools.dvbc(kdvbc, netnetwork)
			elif addon.getSetting('kdvbs') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbs = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('clarotv') == 'true':
					tvh_channels('clarotv')
					tvh_picons('clarotv')
					tools.dvbs(kdvbs, claronetwork)
		if addon.getSetting('k2pro') == 'true':
			if addon.getSetting('kdvbc') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbc = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('net') == 'true':
					tvh_channels('net')
					tvh_picons('net')
					tools.dvbc(kdvbc, netnetwork)
			elif addon.getSetting('kdvbs') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbs = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('clarotv') == 'true':
					tvh_channels('clarotv')
					tvh_picons('clarotv')
					tools.dvbs(kdvbs, claronetwork)
		if addon.getSetting('k3pro') == 'true':
			if addon.getSetting('kdvbc') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbc = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('net') == 'true':
					tvh_channels('net')
					tvh_picons('net')
					tools.dvbc(kdvbc, netnetwork)
			elif addon.getSetting('kdvbs') == 'true':
				ktuner = os.listdir(addontvhtuners)[0]
				kdvbs = "%s%s" % (addontvhtuners, ktuner)
				if addon.getSetting('clarotv') == 'true':
					tvh_channels('clarotv')
					tvh_picons('clarotv')
					tools.dvbs(kdvbs, claronetwork)

##### Recording #####
def tvh_recording():
	if 'tndsdvr' in open(addontvhdefaultdvr).read():
		dialog.notification(addonname, langString(50070), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		tools.addkeyjson(addontvhdefaultdvr, 'tndsdvr', 'true')
		if addon.getSetting('recordprofile') == '0':
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
			elif 'Virtual' in open(release).read():
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
			if addon.getSetting('logadmin') == 'true':
				adminuserpath = (addontvhacontrol+"90989e141bf7c77bcaecaef8da1e0054")
				tools.addkeyjson(adminuserpath, 'dvr_config', ['42c91dae1ea94fbc2a46d456491b4179'])
			if addon.getSetting('logclient') == 'true':
				clientuserpath = (addontvhacontrol+"95275ba5e99a33a72b5081c870e179d8")
				tools.addkeyjson(clientuserpath, 'dvr_config', ['42c91dae1ea94fbc2a46d456491b4179'])
				
		elif addon.getSetting('recordprofile') == '1':
			if 'Generic' in open(release).read():
				if tools.check_passprofile(6, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(6, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(5, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(5, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(4, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(4, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(3, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(3, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(2, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(2, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(1, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(1, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(0, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(0, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
			elif 'Virtual' in open(release).read():
				if tools.check_passprofile(6, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(6, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(5, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(5, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(4, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(4, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(3, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(3, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(2, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(2, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(1, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(1, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(0, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(0, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
			else:
				if tools.check_passprofile(2, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(2, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(1, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(1, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
				elif tools.check_passprofile(0, addontvhprofile):
					tools.recording_profile(tools.check_passprofile(0, addontvhprofile),recordingpath, addontvhdvrconf, "Pass-thru")
			if addon.getSetting('logadmin') == 'true':
				adminuser = "%s%s" % (addontvhacontrol, "90989e141bf7c77bcaecaef8da1e0054")
				tools.addkeyjson(adminuser, 'dvr_config', '42c91dae1ea94fbc2a46d456491b4179')
			if addon.getSetting('logclient') == 'true':
				clientuser = "%s%s" % (addontvhacontrol, "95275ba5e99a33a72b5081c870e179d8")
				tools.addkeyjson(clientuser, 'dvr_config', '42c91dae1ea94fbc2a46d456491b4179')
					
		elif addon.getSetting('recordprofile') == '2':
			if 'Generic' in open(release).read():
				if tools.check_htspprofile(6, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(6, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(5, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(5, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(4, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(4, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(3, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(3, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(2, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(2, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(1, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(1, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(0, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(0, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
			if 'Virtual' in open(release).read():
				if tools.check_htspprofile(6, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(6, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(5, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(5, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(4, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(4, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(3, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(3, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(2, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(2, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(1, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(1, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(0, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(0, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
			else:
				if tools.check_htspprofile(2, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(2, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(1, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(1, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
				elif tools.check_htspprofile(0, addontvhprofile):
					tools.recording_profile(tools.check_htspprofile(0, addontvhprofile),recordingpath, addontvhdvrconf, "HTSP")
			if addon.getSetting('logadmin') == 'true':
				adminuser = "%s%s" % (addontvhacontrol, "90989e141bf7c77bcaecaef8da1e0054")
				tools.addkeyjson(adminuser, 'dvr_config', '42c91dae1ea94fbc2a46d456491b4179')
			if addon.getSetting('logclient') == 'true':
				clientuser = "%s%s" % (addontvhacontrol, "95275ba5e99a33a72b5081c870e179d8")
				tools.addkeyjson(clientuser, 'dvr_config', '42c91dae1ea94fbc2a46d456491b4179')

		elif addon.getSetting('recordprofile') == '3':
			if addon.getSetting('tvhexpert') == 'true':
				tools.updateJsonFile(addontvhdefaultdvr, 'storage', recordingpath)
	
##### PVR Config #####
def tvh_pvr():
	if os.path.exists(addonpvrtvhdata):
		if ipbox in open(addonpvrtvhsettings).read():
			dialog.notification(addonname, langString(50071), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		if not os.path.exists(addonpvrtvhdata):
			os.makedirs(addonpvrtvhdata)
		if addon.getSetting('userclient') == '':
			tools.pvrsettings(addonpvrtvhsettings, ipbox, '', '')
		else:
			tools.pvrsettings(addonpvrtvhsettings, ipbox, clientpass, clientuser)
		#Enable Live TV
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled","value":true},"id":1}')

##### Kodi Config #####		
def kodi_config():
	if os.path.exists(advanced):
		dialog.notification(addonname, langString(50072), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		#Optimization
		if addon.getSetting('optim') == 'true':
			if 'VERSION_ID="7.0"' in open(release).read():
				tools.advancedsettings_jarvis(advanced)
			if 'VERSION_ID="8.0"' in open(release).read():
				tools.advancedsettings_krypton(advanced)
			if 'VERSION_ID="8.2"' in open(release).read():
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
