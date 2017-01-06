#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
############# BIBLIOTECAS A IMPORTAR E DEFINICOES ###################
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,os,shutil,xbmcvfs,re,tools,urllib2,time

dialog = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()

	##### ADDON TVH WIZARD by Tnds #####
addon             = xbmcaddon.Addon(id='script.tvhwizard.tnds')
addonname         = addon.getAddonInfo('name')
addonfolder       = addon.getAddonInfo('path')
addonicon        = os.path.join(addonfolder, 'icon.png')

	##### ADDON SERVICE TVHEADEND #####
addontvh         = xbmcaddon.Addon(id='service.tvheadend42')
addontvhname     = addontvh.getAddonInfo('name')
addontvhfolder   = addontvh.getAddonInfo('path')

	##### DESTINATION #####
addontvhdest     = xbmc.translatePath(addontvh.getAddonInfo('profile'))
addontvhchannel  = os.path.join(addontvhdest, 'channel/')
addontvhdvb      = os.path.join(addontvhdest, 'input/dvb')
addontvhimgcache = os.path.join(addontvhdest, 'imagecache/')
addontvhimgmeta  = os.path.join(addontvhdest, 'imagecache/meta')
tndsdown         = os.path.join('/storage/.kodi/tnds82')
zonelisbon       = os.path.join(tndsdown, 'lisbon')
zoneporto        = os.path.join(tndsdown, 'porto')
zonehispasat     = os.path.join(tndsdown, 'hispasat')
zoneastra        = os.path.join(tndsdown, 'astra')
zoneaveiro       = os.path.join(tndsdown, 'aveiro')
zoneleiria       = os.path.join(tndsdown, 'leiria')

   ##### CHANNEL'S VERSION'S #####
channelver = "%s%s" % (addontvhchannel, 'version')

def langString(id):
	return addon.getLocalizedString(id)
	
def zone_channels():
	#Cabo Lisboa
	if addon.getSetting('uplisbon') == 'true':
		version_url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/lisbonversion"
		url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/lisbon.zip"
		urlpicon = "http://tnds82.xyz/tvhwizard/picons/dvbc/portugal/picons.zip"
		check = urllib2.urlopen(version_url)
		check1 = open(channelver, "r")
		for line1 in check:
			for line2 in check1:
					if line1==line2:
						print "There is no update of Channels"
					else:
						updatechannels = dialog.yesno(addonname, langString(5077))
						if updatechannels == 0:
							print "Your answer was no"
						else:
							update_channels(url, zonelisbon, urlpicon)
	#Cabo Porto
	if addon.getSetting('upporto') == 'true':
		version_url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/portoversion"
		url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/porto.zip"
		urlpicon = "http://tnds82.xyz/tvhwizard/picons/dvbc/portugal/picons.zip"
		check = urllib2.urlopen(version_url)
		check1 = open(channelver, "r")
		for line1 in check:
			for line2 in check1:
					if line1==line2:
						print "There is no update of Channels"
					else:
						updatechannels = dialog.yesno(addonname, langString(5077))
						if updatechannels == 0:
							print "Your answer was no"
						else:
							update_channels(url, zoneporto, urlpicon)

	#Sat Hispasat
	if addon.getSetting('uphispasat') == 'true':
		version_url = "http://tnds82.xyz/tvhwizard/channels/dvbs/hispasatversion"
		url = "http://tnds82.xyz/tvhwizard/channels/dvbs/hispasat.zip"
		urlpicon = "http://tnds82.xyz/tvhwizard/picons/dvbs/hispasat.zip"
		check = urllib2.urlopen(version_url)
		check1 = open(channelver, "r")
		for line1 in check:
			for line2 in check1:
					if line1==line2:
						print "There is no update of Channels"
					else:
						updatechannels = dialog.yesno(addonname, langString(5077))
						if updatechannels == 0:
							print "Your answer was no"
						else:
							update_channels(url, zonehispasat, urlpicon)

	#Sat Astra
	if addon.getSetting('upastra') == 'true':
		version_url = "http://tnds82.xyz/tvhwizard/channels/dvbs/astraversion"
		url = "http://tnds82.xyz/tvhwizard/channels/dvbs/astra.zip"
		urlpicon = "http://tnds82.xyz/tvhwizard/picons/dvbs/astra.zip"
		check = urllib2.urlopen(version_url)
		check1 = open(channelver, "r")
		for line1 in check:
			for line2 in check1:
					if line1==line2:
						print "There is no update of Channels"
					else:
						updatechannels = dialog.yesno(addonname, langString(5077))
						if updatechannels == 0:
							print "Your answer was no"
						else:
							update_channels(url, zoneastra, urlpicon)

	#Cabo Aveiro
	if addon.getSetting('upaveiro') == 'true':
		version_url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/aveiroversion"
		url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/aveiro.zip"
		urlpicon = "http://tnds82.xyz/tvhwizard/picons/dvbc/portugal/picons.zip"
		check = urllib2.urlopen(version_url)
		check1 = open(channelver, "r")
		for line1 in check:
			for line2 in check1:
					if line1==line2:
						print "There is no update of Channels"
					else:
						updatechannels = dialog.yesno(addonname, langString(5077))
						if updatechannels == 0:
							print "Your answer was no"
						else:
							update_channels(url, zoneaveiro, urlpicon)

	#Cabo Leiria
	if addon.getSetting('upleiria') == 'true':
		version_url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/leiriaversion"
		url = "http://tnds82.xyz/tvhwizard/channels/dvbc/portugal/leiria.zip"
		urlpicon = "http://tnds82.xyz/tvhwizard/picons/dvbc/portugal/picons.zip"
		check = urllib2.urlopen(version_url)
		check1 = open(channelver, "r")
		for line1 in check:
			for line2 in check1:
					if line1==line2:
						print "There is no update of Channels"
					else:
						updatechannels = dialog.yesno(addonname, langString(5077))
						if updatechannels == 0:
							print "Your answer was no"
						else:
							update_channels(url, zoneleiria, urlpicon)
						

def update_channels(url, zone, urlpicon):
	os.system("systemctl stop service.tvheadend42")
	channelsFile = os.path.join(zone , 'channel.zip')
	networkFile  = os.path.join(zone , 'networks.zip')
	imgcacheFile = os.path.join(zone , 'meta.zip')
	header = "Channels"
	header1 = "Networks"
	header2 = "Image Cache"
	## Channels ##
	if os.path.exists(tndsdown):
		shutil.rmtree(tndsdown)
	tools.channels(url)
	if os.path.exists(addontvhchannel):
		shutil.rmtree(addontvhchannel)
		os.makedirs(addontvhchannel)
	tools.extract(channelsFile,addontvhdest,dp,header)
	if os.path.exists(addontvhdvb):
		shutil.rmtree(addontvhdvb)
		os.makedirs(addontvhdvb)
	tools.extract(networkFile,addontvhdvb,dp,header1)
	## Picons ##
	tools.picons(urlpicon)
	## Img Cache ##
	if os.path.exists(addontvhimgmeta):
		shutil.rmtree(addontvhimgmeta)
		os.makedirs(addontvhimgmeta)
	tools.extract(imgcacheFile,addontvhimgcache,dp,header2)
	os.system("systemctl stop service.tvheadend42")
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(5078), 5000, addonicon))
	time.sleep(1)
	os.system("reboot")

