#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
#########################################################################################
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,os,shutil,xbmcvfs,re,base64,tools,time,subprocess

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
addontvhdvbapi     = os.path.join(addontvhdest, 'caclient')
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

### SPECIAL Wetek Play Image ###
def tvh_wetekspecial():
	tools.wetekexample()
	time.sleep( 5 )

##### CONFIGURATION #####

def tvh_config():
	if '"tndsconfig": "",' in open(addontvhconfig).read():
		dialog.notification(addonname, langString(5061), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		#remove tvhwizard
		tndscfg = {'	"wizard": "hello",':'    "tndsconfig": "",'}
		tools.change_words(addontvhconfig, tndscfg)

		#expert mode
		if addon.getSetting('tvhexpert') == 'true':
			experttvh = {'"uilevel": 1,':'"uilevel": 2,'}
			tools.change_words(addontvhconfig, experttvh)

		#web language
		if addon.getSetting('languipt') == 'true':
			uilangpt = '    "language_ui": "por",\n'
			tools.insert_words(addontvhconfig, 24, uilangpt)
		
		if addon.getSetting('languien') == 'true':
			uilangen = '    "language_ui": "eng",\n'
			tools.insert_words(addontvhconfig, 24, uilangen)

		#epg language
		if addon.getSetting('langepg') == 'true':
			#en
			epglangen = '    	"eng"\n'
			tools.insert_words(addontvhconfig, 15, epglangen)

			#pt
			epglangpt = '    	"por",\n'
			tools.insert_words(addontvhconfig, 15, epglangpt)

			if addon.getSetting('langepgen') == 'false':
				#pt
				epglangp = '    	"por"\n'
				tools.removeinsert_2words(addontvhconfig, 15, 15, 15, epglangp)
			if addon.getSetting('langepgpt') == 'false':
				#en
				epglange = '    	"eng"\n'
				tools.removeinsert_2words(addontvhconfig, 15, 15, 15, epglange)

##### DVBAPI #####

def tvh_dvbapi():
	if os.path.exists(dvbapifile):
		dialog.notification(addonname, langString(5062), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		addontvh.setSetting(id='PRELOAD_CAPMT_CA', value='true')
		
		#oscam pc-nodmx
		if addon.getSetting('dvbapichoose') == 'pc-nodmx':
			if not os.path.exists(addontvhdvbapi):
				os.makedirs(addontvhdvbapi)
			creatsoftcam = open(dvbapifile, 'a')
			creatsoftcam.write('{\n')
			creatsoftcam.write('	"mode": 4,\n')
			creatsoftcam.write('	"camdfilename": "/tmp/camd.socket",\n')
			creatsoftcam.write('	"port": 0,\n')
			creatsoftcam.write('	"class": "caclient_capmt",\n')
			creatsoftcam.write('	"index": 1,\n')
			creatsoftcam.write('	"enabled": true,\n')
			creatsoftcam.write('	"name": "tvheadend"\n')
			creatsoftcam.write('}\n')
			creatsoftcam.write('\n')
			creatsoftcam.close()
		
		#oscam pc
		if addon.getSetting('dvbapichoose') == 'pc':
			if not os.path.exists(addontvhdvbapi):
				os.makedirs(addontvhdvbapi)
			creatsoftcam = open(dvbapifile, 'a')
			creatsoftcam.write('{\n')
			creatsoftcam.write('	"mode": 5,\n')
			creatsoftcam.write('	"camdfilename": "%s",\n' % dvbapip)
			creatsoftcam.write('	"port": %s,\n' % dvbapiport)
			creatsoftcam.write('	"class": "caclient_capmt",\n')
			creatsoftcam.write('	"index": 1,\n')
			creatsoftcam.write('	"enabled": true,\n')
			creatsoftcam.write('	"name": "tvheadend"\n')
			creatsoftcam.write('}\n')
			creatsoftcam.write('\n')
			creatsoftcam.close()

##### ADD CHANNELS #####

def tvh_channels():
	tnds82 = "%s%s" % (addontvhchannel, "tnds82")
	if os.path.exists(tnds82):
		dialog.notification(addonname, langString(5063), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		tnds = open(tnds82, 'a')
		tnds.write("channels created by tnds82")
		tnds.close()
		
		### LISBON ###
		if addon.getSetting('lisbon') == 'true':
			url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/lisbon.zip"
			url_version = '"http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/lisbonversion"'
			tools.channels(url)
			header = "Channels"
			channelsFile = os.path.join('/storage/.kodi/tnds82/lisbon', 'channel.zip')
			tools.extract(channelsFile,addontvhdest,dp,header)
			header1 = "Networks"
			if not os.path.exists(addontvhdvb):
				os.makedirs(addontvhdvb)
			networkFile = os.path.join('/storage/.kodi/tnds82/lisbon', 'networks.zip')
			tools.extract(networkFile,addontvhdvb,dp,header1)
			if not os.path.exists(addonlog):
				os.makedirs(addonlog)
			subprocess_cmd('%s %s %s' % ('wget -O', addonchaver, url_version))


		### PORTO ###
		if addon.getSetting('porto') == 'true':
			url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/porto.zip"
			url_version = '"http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/portoversion"'
			tools.channels(url)
			header = "Channels"
			channelsFile = os.path.join('/storage/.kodi/tnds82/porto', 'channel.zip')
			tools.extract(channelsFile,addontvhdest,dp,header)
			header1 = "Networks"
			if not os.path.exists(addontvhdvb):
				os.makedirs(addontvhdvb)
			networkFile = os.path.join('/storage/.kodi/tnds82/porto', 'networks.zip')
			tools.extract(networkFile,addontvhdvb,dp,header1)
			if not os.path.exists(addonlog):
				os.makedirs(addonlog)
			subprocess_cmd('%s %s %s' % ('wget -O', addonchaver, url_version))
	
		### HISPASAT ###
		if addon.getSetting('hispasat') == 'true':
			url = "http://tnds82.xyz/tvhwizard/channels/dvbs/hispasat.zip"
			url_version = '"http://tnds82.xyz/tvhwizard/channels/dvbs/hispasatversion"'
			tools.channels(url)
			header = "Channels"
			channelsFile = os.path.join('/storage/.kodi/tnds82/hispasat', 'channel.zip')
			tools.extract(channelsFile,addontvhdest,dp,header)
			header1 = "Networks"
			if not os.path.exists(addontvhdvb):
				os.makedirs(addontvhdvb)
			networkFile = os.path.join('/storage/.kodi/tnds82/hispasat', 'networks.zip')
			tools.extract(networkFile,addontvhdvb,dp,header1)
			if not os.path.exists(addonlog):
				os.makedirs(addonlog)
			subprocess_cmd('%s %s %s' % ('wget -O', addonchaver, url_version))
	
		### ASTRA ###
		if addon.getSetting('astra') == 'true':
			url = "http://tnds82.xyz/tvhwizard/channels/dvbs/astra.zip"
			url_version = '"http://tnds82.xyz/tvhwizard/channels/dvbs/astraversion"'
			tools.channels(url)
			header = "Channels"
			channelsFile = os.path.join('/storage/.kodi/tnds82/astra', 'channel.zip')
			tools.extract(channelsFile,addontvhdest,dp,header)
			header1 = "Networks"
			if not os.path.exists(addontvhdvb):
				os.makedirs(addontvhdvb)
			networkFile = os.path.join('/storage/.kodi/tnds82/astra', 'networks.zip')
			tools.extract(networkFile,addontvhdvb,dp,header1)
			if not os.path.exists(addonlog):
				os.makedirs(addonlog)
			subprocess_cmd('%s %s %s' % ('wget -O', addonchaver, url_version))
			
		### AVEIRO ###
		if addon.getSetting('aveiro') == 'true':
			url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/aveiro.zip"
			url_version = '"http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/aveiroversion"'
			tools.channels(url)
			header = "Channels"
			channelsFile = os.path.join('/storage/.kodi/tnds82/aveiro', 'channel.zip')
			tools.extract(channelsFile,addontvhdest,dp,header)
			header1 = "Networks"
			if not os.path.exists(addontvhdvb):
				os.makedirs(addontvhdvb)
			networkFile = os.path.join('/storage/.kodi/tnds82/aveiro', 'networks.zip')
			tools.extract(networkFile,addontvhdvb,dp,header1)
			if not os.path.exists(addonlog):
				os.makedirs(addonlog)
			subprocess_cmd('%s %s %s' % ('wget -O', addonchaver, url_version))
			
		### LEIRIA ###
		if addon.getSetting('leiria') == 'true':
			url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/leiria.zip"
			url_version = '"http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/leiriaversion"'
			tools.channels(url)
			header = "Channels"
			channelsFile = os.path.join('/storage/.kodi/tnds82/leiria', 'channel.zip')
			tools.extract(channelsFile,addontvhdest,dp,header)
			header1 = "Networks"
			if not os.path.exists(addontvhdvb):
				os.makedirs(addontvhdvb)
			networkFile = os.path.join('/storage/.kodi/tnds82/leiria', 'networks.zip')
			tools.extract(networkFile,addontvhdvb,dp,header1)
			if not os.path.exists(addonlog):
				os.makedirs(addonlog)
			subprocess_cmd('%s %s %s' % ('wget -O', addonchaver, url_version))

##### PICONS #####

def tvh_picons():
	if os.path.exists(piconpath): #'"piconpath": "file:///storage/.kodi/userdata/picons"' in open(addontvhconfig).read():
		dialog.notification(addonname, langString(5064), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		### Download Picons ###
		if addon.getSetting('lisbon') == 'true':
			url = "http://tnds82.xyz/tvhwizard/picons/dvbc/portugal/picons.zip"
			tools.picons(url)
		if addon.getSetting('porto') == 'true':
			url = "http://tnds82.xyz/tvhwizard/picons/dvbc/portugal/picons.zip"
			tools.picons(url)
		if addon.getSetting('hispasat') == 'true':
			url = "http://tnds82.xyz/tvhwizard/picons/dvbs/hispasat.zip"
			tools.picons(url)
		if addon.getSetting('astra') == 'true':
			url = "http://tnds82.xyz/tvhwizard/picons/dvbs/astra.zip"
			tools.picons(url)
		if addon.getSetting('aveiro') == 'true':
			url = "http://tnds82.xyz/tvhwizard/picons/dvbc/portugal/picons.zip"
			tools.picons(url)
		if addon.getSetting('leiria') == 'true':
			url = "http://tnds82.xyz/tvhwizard/picons/dvbc/portugal/picons.zip"
			tools.picons(url)
		
		### Picons Path ###
		if not os.path.exists(piconsympath):
			os.makedirs(piconsympath)
		time.sleep( 1 )
		subprocess_cmd("%s %s %s" % ("ln -s", piconpath, piconsympath))

		### Image Cache ###
		if addon.getSetting('imagecache') == 'true' :
			imgcachepath = addontvhimgcache
			if not os.path.exists(imgcachepath):
				os.makedirs(imgcachepath)
			imgcache = "%s%s" % (addontvhimgcache, "config")
			configfile = open(imgcache, 'a')
			configfile.write('{\n')
			configfile.write('	"enabled": true,\n')
			configfile.write('	"ignore_sslcert": false,\n')
			configfile.write('	"ok_period": 168,\n')
			configfile.write('	"fail_period": 24\n')
			configfile.write('}\n')
			configfile.close()
			
			### LISBON ###
			if addon.getSetting('lisbon') == 'true':
				header = "Image Cache"
				imgcacheFile = os.path.join('/storage/.kodi/tnds82/lisbon', 'meta.zip')
				tools.extract(imgcacheFile,addontvhimgcache,dp,header)
			
			### PORTO ###
			if addon.getSetting('porto') == 'true':
				header = "Image Cache"
				imgcacheFile = os.path.join('/storage/.kodi/tnds82/porto', 'meta.zip')
				tools.extract(imgcacheFile,addontvhimgcache,dp,header)
				
			### HISPASAT ###
			if addon.getSetting('hispasat') == 'true':
				header = "Image Cache"
				imgcacheFile = os.path.join('/storage/.kodi/tnds82/hispasat', 'meta.zip')
				tools.extract(imgcacheFile,addontvhimgcache,dp,header)
				
			### ASTRA ###
			if addon.getSetting('astra') == 'true':
				header = "Image Cache"
				imgcacheFile = os.path.join('/storage/.kodi/tnds82/astra', 'meta.zip')
				tools.extract(imgcacheFile,addontvhimgcache,dp,header)

			### AVEIRO ###
			if addon.getSetting('aveiro') == 'true':
				header = "Image Cache"
				imgcacheFile = os.path.join('/storage/.kodi/tnds82/aveiro', 'meta.zip')
				tools.extract(imgcacheFile,addontvhimgcache,dp,header)

			### LEIRIA ###
			if addon.getSetting('leiria') == 'true':
				header = "Image Cache"
				imgcacheFile = os.path.join('/storage/.kodi/tnds82/leiria', 'meta.zip')
				tools.extract(imgcacheFile,addontvhimgcache,dp,header)
				
##### DVB INPUTS #####

def tvh_tunners():
	enableinput = '			"enabled": true,\n'
	dvbcnetwork = '				"2e3a376d8f26d0e7db2970d22f691ce3"\n' # Network Lisbon, Porto, Aveiro, Leiria
	hispanetwork = '				"f9f86bd361cdb5c3349163346ac173f7"\n' # Network Hispasat
	hispanetwork1 = '							"f9f86bd361cdb5c3349163346ac173f7"\n' #Network Hispasat
	astranetwork = '				"b49667f409cd90d954431ce14ea69405"\n' # Network Astra
	astranetwork1 = '							"b49667f409cd90d954431ce14ea69405"\n' #Network Astra
	
	### WETEK PLAY 2 ###
	if addon.getSetting('wetekp2enable') == 'true':
	
		### DVB-C ###
		if addon.getSetting('wetekp2dvbc') == 'true':
			wetek2tuner = os.listdir(addontvhtuners)[0]
			w2dvbc = "%s%s" % (addontvhtuners, wetek2tuner)
			if '"enabled": true' in open(w2dvbc).read():
				dialog.notification(addonname, langString(5065), xbmcgui.NOTIFICATION_WARNING, 2000)
			else:
				tools.wetek2cable(w2dvbc, enableinput, dvbcnetwork)
	
		###DVB-S ###
		if addon.getSetting('wetekp2dvbs') == 'true':
			wetek2tuner = os.listdir(addontvhtuners)[0]
			w2dvbs = "%s%s" % (addontvhtuners, wetek2tuner)
			if not '"enabled": false,' in open(w2dvbs).read():
				dialog.notification(addonname, langString(5065), xbmcgui.NOTIFICATION_WARNING, 2000)
			else:
				if addon.getSetting('astra') == 'true':
					tools.wetek2sat(w2dvbs, enableinput, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.wetek2sat(w2dvbs, enableinput, hispanetwork, hispanetwork1)
							
	### WETEK PLAY ###
	if addon.getSetting('wetekpenable') == 'true':
	
		### DVB-C ###
		if addon.getSetting('wetekpdvbc') == 'true':
			wetektuner = os.listdir(addontvhtuners)[0]
			wdvbc = "%s%s" % (addontvhtuners, wetektuner)
			if '"enabled": true' in open(wdvbc).read():
				dialog.notification(addonname, langString(5065), xbmcgui.NOTIFICATION_WARNING, 2000)
			else:
				tools.wetekcable(wdvbc, enableinput, dvbcnetwork)
	
		###DVB-S ###
		if addon.getSetting('wetekpdvbs') == 'true':
			wetektuners1 = os.listdir(addontvhtuners)[0]
			wdvbs1 = "%s%s" % (addontvhtuners, wetektuners1)
			wetektuners2 = os.listdir(addontvhtuners)[1]
			wdvbs2 = "%s%s" % (addontvhtuners, wetektuners2)
			if not '"enabled": false,' in open(wdvbs1).read():
				dialog.notification(addonname, langString(5065), xbmcgui.NOTIFICATION_WARNING, 2000)
			if not '"enabled": false,' in open(wdvbs2).read():
				dialog.notification(addonname, langString(5065), xbmcgui.NOTIFICATION_WARNING, 2000)
			else:
				wetekdvbs = dialog.yesno(addonname, langString(5066), "", "", langString(5067), langString(5068))
				if wetekdvbs == 0:
					dialog.notification(addonname, "LNB 2 Enabled")
					if '/dev/dvb/adapter1' in open(wdvbs1).read():
						if addon.getSetting('astra') == 'true':
							tools.weteksat(wdvbs1, enableinput, astranetwork, astranetwork1)
						if addon. getSetting('hispasat') == 'true':
							tools.weteksat(wdvbs1, enableinput, hispanetwork, hispanetwork1)
					if '/dev/dvb/adapter1' in open(wdvbs2).read():
						if addon.getSetting('astra') == 'true':
							tools.weteksat(wdvbs2, enableinput, astranetwork, astranetwork1)
						if addon. getSetting('hispasat') == 'true':
							tools.weteksat(wdvbs2, enableinput, hispanetwork, hispanetwork1)
				else:
					dialog.notification(addonname, "LNB 1 Enabled")
					if '/dev/dvb/adapter0' in open(wdvbs1).read():
						if addon.getSetting('astra') == 'true':
							tools.weteksat(wdvbs1, enableinput, astranetwork, astranetwork1)
						if addon. getSetting('hispasat') == 'true':
							tools.weteksat(wdvbs1, enableinput, hispanetwork, hispanetwork1)
					if '/dev/dvb/adapter0' in open(wdvbs2).read():
						if addon.getSetting('astra') == 'true':
							tools.weteksat(wdvbs2, enableinput, astranetwork, astranetwork1)
						if addon. getSetting('hispasat') == 'true':
							tools.weteksat(wdvbs2, enableinput, hispanetwork, hispanetwork1)

	### K1 PLUS COMBO ###
	if addon.getSetting('k1plusenable') == 'true':

		###DVB-S ###
		if addon.getSetting('k1plusdvbs') == 'true':
			k1tuner = os.listdir(addontvhtuners)[0]
			k1dvbs = "%s%s" % (addontvhtuners, k1tuner)
			if '"enabled": true' in open(k1dvbs).read():
				dialog.notification(addonname, langString(5065), xbmcgui.NOTIFICATION_WARNING, 2000)
			else:
				if addon.getSetting('astra') == 'true':
					tools.k1sat(k1dvbs, enableinput, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.k1sat(k1dvbs, enableinput, hispanetwork, hispanetwork1)

	### GENERIC ###
	if addon.getSetting('rpigenable') == 'true':
		### ONE INPUT ###
		if addon.getSetting('dvbnumber') == '0':
			tuner1 = os.listdir(addontvhtuners)[0]
			dvbtuner1 = "%s%s" % (addontvhtuners, tuner1)
			if '"enabled": true' in open(dvbtuner1).read():
				dialog.notification(addonname, langString(5065), xbmcgui.NOTIFICATION_WARNING, 2000)
			else:
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)

		### TWO INPUTS ###
		if addon.getSetting('dvbnumber') == '1':
			tuner1 = os.listdir(addontvhtuners)[0]
			dvbtuner1 = "%s%s" % (addontvhtuners, tuner1)
			if '"enabled": true' in open(dvbtuner1).read():
				dialog.notification(addonname, langString(5065), xbmcgui.NOTIFICATION_WARNING, 2000)
			else:
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				tuner2 = os.listdir(addontvhtuners)[1]
				dvbtuner2 = "%s%s" % (addontvhtuners, tuner2)
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				
		### THREE INPUTS ###
		if addon.getSetting('dvbnumber') == '2':
			tuner1 = os.listdir(addontvhtuners)[0]
			dvbtuner1 = "%s%s" % (addontvhtuners, tuner1)
			if '"enabled": true' in open(dvbtuner1).read():
				dialog.notification(addonname, langString(5065), xbmcgui.NOTIFICATION_WARNING, 2000)
			else:
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				tuner2 = os.listdir(addontvhtuners)[1]
				dvbtuner2 = "%s%s" % (addontvhtuners, tuner2)
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				tuner3 = os.listdir(addontvhtuners)[2]
				dvbtuner3 = "%s%s" % (addontvhtuners, tuner3)
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)

		### FOUR INPUTS ###
		if addon.getSetting('dvbnumber') == '3':
			tuner1 = os.listdir(addontvhtuners)[0]
			dvbtuner1 = "%s%s" % (addontvhtuners, tuner1)
			if '"enabled": true' in open(dvbtuner1).read():
				dialog.notification(addonname, langString(5065), xbmcgui.NOTIFICATION_WARNING, 2000)
			else:
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				tuner2 = os.listdir(addontvhtuners)[1]
				dvbtuner2 = "%s%s" % (addontvhtuners, tuner2)
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				tuner3 = os.listdir(addontvhtuners)[2]
				dvbtuner3 = "%s%s" % (addontvhtuners, tuner3)
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				tuner4 = os.listdir(addontvhtuners)[3]
				dvbtuner4 = "%s%s" % (addontvhtuners, tuner4)
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				
		### FIVE INPUTS ###
		if addon.getSetting('dvbnumber') == '4':
			tuner1 = os.listdir(addontvhtuners)[0]
			dvbtuner1 = "%s%s" % (addontvhtuners, tuner1)
			if '"enabled": true' in open(dvbtuner1).read():
				dialog.notification(addonname, langString(5065), xbmcgui.NOTIFICATION_WARNING, 2000)
			else:
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner1, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				tuner2 = os.listdir(addontvhtuners)[1]
				dvbtuner2 = "%s%s" % (addontvhtuners, tuner2)
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner2, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				tuner3 = os.listdir(addontvhtuners)[2]
				dvbtuner3 = "%s%s" % (addontvhtuners, tuner3)
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner3, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				tuner4 = os.listdir(addontvhtuners)[3]
				dvbtuner4 = "%s%s" % (addontvhtuners, tuner4)
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner4, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				tuner5 = os.listdir(addontvhtuners)[4]
				dvbtuner5 = "%s%s" % (addontvhtuners, tuner5)
				if addon.getSetting('lisbon') == 'true':
					tools.generic(dvbtuner5, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('porto') == 'true':
					tools.generic(dvbtuner5, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('aveiro') == 'true':
					tools.generic(dvbtuner5, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('leiria') == 'true':
					tools.generic(dvbtuner5, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon.getSetting('astra') == 'true':
					tools.generic(dvbtuner5, enableinput, dvbcnetwork, astranetwork, astranetwork1)
				if addon. getSetting('hispasat') == 'true':
					tools.generic(dvbtuner5, enableinput, dvbcnetwork, hispanetwork, hispanetwork1)
				
##### USERS #####

def tvh_users():
	userdefault = os.listdir(addontvhacontrol)[0]
	defaultuser = "%s%s" % (addontvhacontrol, userdefault)
	if not 'Default access entry' in open(defaultuser).read():
		dialog.notification(addonname, langString(5069), xbmcgui.NOTIFICATION_WARNING, 5000)
	else:
		# Create administrator user with password
		if addon.getSetting('logadmin') == 'true':
			# Disable Default access entry
			disablemaster = {'"enabled": true,':'"enabled": false,','"index": 1,':'"index": 2,'}
			tools.change_words(defaultuser, disablemaster)

			# Create user admin 
			filenameuser = "%s%s" % (addontvhacontrol, "90989e141bf7c77bcaecaef8da1e0054")
			createuser = open(filenameuser, 'a')
			createuser.write("{\n")
			createuser.write('	"index": 1,\n')
			createuser.write('	"enabled": true,\n')
			createuser.write('	"username": "%s",\n' % adminuser)
			createuser.write('	"prefix": "0.0.0.0/0,::/0",\n')
			createuser.write('	"change": [\n')
			createuser.write('		"change_rights"\n')
			createuser.write('	],\n')
			createuser.write('	"uilevel": 2,\n')
			createuser.write('	"uilevel_nochange": -1,\n')
			createuser.write('	"streaming": [\n')
			createuser.write('		"basic",\n')
			createuser.write('		"advanced",\n')
			createuser.write('		"htsp"\n')
			createuser.write('	],\n')
			createuser.write('	"profile": [\n')
			createuser.write('	],\n')
			createuser.write('	"dvr": [\n')
			createuser.write('		"basic",\n')
			createuser.write('		"htsp",\n')
			createuser.write('		"all",\n')
			createuser.write('		"all_rw",\n')
			createuser.write('		"failed"\n')
			createuser.write('	],\n')
			createuser.write('	"htsp_anonymize": false,\n')
			createuser.write('	"dvr_config": [\n')
			createuser.write('	],\n')
			createuser.write('	"webui": true,\n')
			createuser.write('	"admin": true,\n')
			createuser.write('	"conn_limit_type": 0,\n')
			createuser.write('	"conn_limit": 0,\n')
			createuser.write('	"channel_min": 0,\n')
			createuser.write('	"channel_max": 0,\n')
			createuser.write('	"channel_tag_exclude": false,\n')
			createuser.write('	"channel_tag": [\n')
			createuser.write('	],\n')
			createuser.write('	"comment": "Administrator",\n')
			createuser.write('	"wizard": false\n')
			createuser.write('}\n')
			createuser.close()

			# Create Admin Password
			newpath = addontvhpass
			if not os.path.exists(newpath):
				os.makedirs(newpath)
			
			#enconde pass
			encoded = base64.b64encode(adminpass)
			tvhpass = "VFZIZWFkZW5kLUhpZGUt"
			passenconded = "%s%s" % (tvhpass, encoded)
			
			#create pass
			filenamepass = "%s%s" % (addontvhpass, "cb77ac54d4e6d859c1890b770f9fbe3a")
			createpass = open(filenamepass, 'a')
			createpass.write("{\n")
			createpass.write('	"enabled": true,\n')
			createpass.write('	"username": "%s",\n' % adminuser)
			createpass.write('	"password2": "%s",\n' % passenconded)
			createpass.write('	"comment": "Pass of Adminstrator",\n')
			createpass.write('	"wizard": false\n')
			createpass.write('}\n')
			createpass.close()

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
				filenamepass = "%s%s" % (addontvhpass, "8597d99ed41fe710bff95567a24372ba")
				createpass = open(filenamepass, 'a')
				createpass.write("{\n")
				createpass.write('	"enabled": true,\n')
				createpass.write('	"username": "%s",\n' % clientuser)
				createpass.write('	"password2": "%s",\n' % passenconded)
				createpass.write('	"comment": "Pass of Client",\n')
				createpass.write('	"wizard": false\n')
				createpass.write('}\n')
				createpass.close()

			# Create user client
			filenameclient = "%s%s" % (addontvhacontrol, "95275ba5e99a33a72b5081c870e179d8")
			createuser = open(filenameclient, 'a')
			createuser.write("{\n")
			createuser.write('	"index": 2,\n')
			createuser.write('	"enabled": true,\n')
			createuser.write('	"username": "%s",\n' % userclient)
			createuser.write('	"prefix": "0.0.0.0/0",\n')
			createuser.write('	"change": [\n')
			createuser.write('		"change_rights"\n')
			createuser.write('	],\n')
			createuser.write('	"uilevel": -1,\n')
			createuser.write('	"uilevel_nochange": -1,\n')
			createuser.write('	"streaming": [\n')
			createuser.write('		"htsp"\n')
			createuser.write('	],\n')
			createuser.write('	"profile": [\n')
			createuser.write('	],\n')
			createuser.write('	"dvr": [\n')
			createuser.write('		"basic",\n')
			createuser.write('		"htsp",\n')
			createuser.write('		"all",\n')
			createuser.write('		"failed"\n')
			createuser.write('	],\n')
			createuser.write('	"htsp_anonymize": false,\n')
			createuser.write('	"dvr_config": [\n')
			createuser.write('	],\n')
			createuser.write('	"webui": false,\n')
			createuser.write('	"admin": false,\n')
			createuser.write('	"conn_limit_type": 0,\n')
			createuser.write('	"conn_limit": 0,\n')
			createuser.write('	"channel_min": 0,\n')
			createuser.write('	"channel_max": 0,\n')
			createuser.write('	"channel_tag_exclude": false,\n')
			createuser.write('	"channel_tag": [\n')
			createuser.write('	],\n')
			createuser.write('	"comment": "Client",\n')
			createuser.write('	"wizard": false\n')
			createuser.write('}\n')
			createuser.close()

##### Recording #####

def tvh_recording():
	if 'tndsdvr' in open(addontvhdefaultdvr).read():
		dialog.notification(addonname, langString(5070), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		tndsdvr = '    "tndsdvr": true,\n'
		tools.insert_words(addontvhdefaultdvr, 13, tndsdvr)
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
				recording = '		"42c91dae1ea94fbc2a46d456491b4179"\n'
				adminuser = "%s%s" % (addontvhacontrol, "90989e141bf7c77bcaecaef8da1e0054")
				tools.insert_words(adminuser, 26, recording)
			if addon.getSetting('logclient') == 'true':
				recording = '		"42c91dae1ea94fbc2a46d456491b4179"\n'
				clientuser = "%s%s" % (addontvhacontrol, "95275ba5e99a33a72b5081c870e179d8")
				tools.insert_words(clientuser, 23, recording)
				
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
				recording = '		"42c91dae1ea94fbc2a46d456491b4179"\n'
				adminuser = "%s%s" % (addontvhacontrol, "90989e141bf7c77bcaecaef8da1e0054")
				tools.insert_words(adminuser, 26, recording)
			if addon.getSetting('logclient') == 'true':
				recording = '		"42c91dae1ea94fbc2a46d456491b4179"\n'
				clientuser = "%s%s" % (addontvhacontrol, "95275ba5e99a33a72b5081c870e179d8")
				tools.insert_words(clientuser, 22, recording)
					
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
				recording = '		"42c91dae1ea94fbc2a46d456491b4179"\n'
				adminuser = "%s%s" % (addontvhacontrol, "90989e141bf7c77bcaecaef8da1e0054")
				tools.insert_words(adminuser, 26, recording)
			if addon.getSetting('logclient') == 'true':
				recording = '		"42c91dae1ea94fbc2a46d456491b4179"\n'
				clientuser = "%s%s" % (addontvhacontrol, "95275ba5e99a33a72b5081c870e179d8")
				tools.insert_words(clientuser, 22, recording)

		elif addon.getSetting('recordprofile') == '3':
			defaultline = {'/storage/recordings':recordingpath}
			tools.change_words(addontvhdefaultdvr, defaultline)
	
##### PVR Config #####

def tvh_pvr():
	if os.path.exists(addonpvrtvhdata):
		if '"epg_async" value="true"' in open(addonpvrtvhsettings).read():
			dialog.notification(addonname, langString(5071), xbmcgui.NOTIFICATION_WARNING, 2000)
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
		dialog.notification(addonname, langString(5072), xbmcgui.NOTIFICATION_WARNING, 2000)
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
	
##### TIMESHIFT Config #####

def tvh_timeshift():
	if '"enabled": true,' in open(addontvhtimeconf).read():
		dialog.notification(addonname, langString(5073), xbmcgui.NOTIFICATION_WARNING, 2000)
	else:
		if os.path.exists(addontvhtime):
			shutil.rmtree(addontvhtime)
			os.makedirs(addontvhtime)
			createtime = open(addontvhtimeconf, 'a')
			createtime.write("{\n")
			createtime.write('	"enabled": true,\n')
			createtime.write('	"ondemand": false,\n')
			createtime.write('	"path": "/storage/.kodi/userdata/addon_data/service.tvheadend42/cache/timeshift",\n')
			createtime.write('	"max_period": 60,\n')
			createtime.write('	"unlimited_period": false,\n')
			createtime.write('	"max_size": 3072,\n')
			createtime.write('	"ram_size": 0,\n')
			createtime.write('	"unlimited_size": false,\n')
			createtime.write('	"ram_only": false,\n')
			createtime.write('	"ram_fit": true\n')
			createtime.write('}\n')
			createtime.close()

