#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
#########################################################################
import xbmc, xbmcaddon, xbmcgui, os, tools, socket

addon     = xbmcaddon.Addon(id='script.tvhwizard')
addonname = addon.getAddonInfo('name')
release   = "/etc/os-release"

def langString(id):
	return addon.getLocalizedString(id)
	
def install_service(header, url, addonid, addonserv, addonname):
	addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
	packageFile = os.path.join(addonsDir, 'packages', addonid)
	header = header
	dp = xbmcgui.DialogProgress()
	tools.downloader(url,packageFile,header)
	tools.extract(packageFile,addonsDir,dp,header)
	xbmc.executebuiltin("UpdateLocalAddons")
	xbmc.executebuiltin("UpdateAddonRepos")
	icon = os.path.join(addonsDir, addonid, 'icon.png')
	line1 = "Add-on enabled"
	time = 5000 #in miliseconds
	src = os.path.join(addonsDir, addonid, 'system.d', addonserv)
	dst = "%s%s" % ('/storage/.config/system.d/',addonserv)
	dst1 = "%s%s" %('/storage/.config/system.d/kodi.target.wants/',addonserv)
	kodiconf = "/storage/.config/system.d/kodi.target.wants"
	if not os.path.exists(kodiconf):
		os.makedirs(kodiconf)
	os.symlink(src, dst)
	os.symlink(src, dst1)
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,line1, time, icon))

def install_addon(header, url, addonid, addonname):
	addonsDir = xbmc.translatePath(os.path.join('special://home', 'addons')).decode("utf-8")
	packageFile = os.path.join(addonsDir, 'packages', addonid)
	header = header
	dp = xbmcgui.DialogProgress()
	tools.downloader(url,packageFile,header)
	tools.extract(packageFile,addonsDir,dp,header)
	xbmc.executebuiltin("UpdateLocalAddons")
	xbmc.executebuiltin("UpdateAddonRepos")
	icon = os.path.join(addonsDir, addonid, 'icon.png')
	line1 = "Add-on enabled"
	time = 5000 #in miliseconds
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname,line1, time, icon))

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def ip_box():
	ip_box = get_ip_address()
	xbmcgui.Dialog().ok(addonname, langString(5079), ip_box, "")

def service_oscam():
	if 'VERSION_ID="7.0"' in open(release).read():
		if 'Generic' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/generic/service.softcam.oscam.zip'
			install_service('Addon Oscam', url, 'service.softcam.oscam', 'service.softcam.oscam.service', 'oscam')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.softcam.oscam')
		elif 'Virtual' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/generic/service.softcam.oscam.zip'
			install_service('Addon Oscam', url, 'service.softcam.oscam', 'service.softcam.oscam.service', 'oscam')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.softcam.oscam')
		elif 'RPi2' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/rpi/service.softcam.oscam.zip'
			install_service('Addon Oscam', url, 'service.softcam.oscam', 'service.softcam.oscam.service', 'oscam')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.softcam.oscam')
		elif 'WeTek_Core' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/wetekcore/service.softcam.oscam.zip'
			install_service('Addon Oscam', url, 'service.softcam.oscam', 'service.softcam.oscam.service', 'oscam')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.softcam.oscam')
		elif 'WeTek_Play.arm' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/wetekplay/service.softcam.oscam.zip'
			install_service('Addon Oscam', url, 'service.softcam.oscam', 'service.softcam.oscam.service', 'oscam')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.softcam.oscam')
		elif 'WeTek_Play_2.aarch64' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/wetekplay2/service.softcam.oscam.zip'		
			install_service('Addon Oscam', url, 'service.softcam.oscam', 'service.softcam.oscam.service', 'oscam')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.softcam.oscam')
		else:
			xbmcgui.Dialog().ok(addonname, langString(5081), "", "")

	if 'VERSION_ID="8.0"' in open(release).read():
		xbmc.executebuiltin("InstallAddon(service.softcam.oscam)")
	
def service_tvheadend():
	if 'VERSION_ID="7.0"' in open(release).read():
		if 'Generic' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/generic/service.tvheadend42.zip'
			install_service('Addon Tvheadend HTSP Client', url, 'service.tvheadend42', 'service.tvheadend42.service', 'Tvheadend 4.2')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.tvheadend42')
		elif 'Virtual' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/generic/service.tvheadend42.zip'
			install_service('Addon Tvheadend HTSP Client', url, 'service.tvheadend42', 'service.tvheadend42.service', 'Tvheadend 4.2')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.tvheadend42')
		elif 'RPi2' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/rpi/service.tvheadend42.zip'
			install_service('Addon Tvheadend HTSP Client', url, 'service.tvheadend42', 'service.tvheadend42.service', 'Tvheadend 4.2')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.tvheadend42')
		elif 'WeTek_Core' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/wetekcore/service.tvheadend42.zip'
			install_service('Addon Tvheadend HTSP Client', url, 'service.tvheadend42', 'service.tvheadend42.service', 'Tvheadend 4.2')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.tvheadend42')
		elif 'WeTek_Play.arm' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/wetekplay/service.tvheadend42.zip'
			install_service('Addon Tvheadend HTSP Client', url, 'service.tvheadend42', 'service.tvheadend42.service', 'Tvheadend 4.2')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.tvheadend42')
		elif 'WeTek_Play_2.aarch64' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/wetekplay2/service.tvheadend42.zip'		
			install_service('Addon Tvheadend HTSP Client', url, 'service.tvheadend42', 'service.tvheadend42.service', 'Tvheadend 4.2')
			os.system('systemctl daemon-reload')
			os.system('systemctl start service.tvheadend42')
		else:
			xbmcgui.Dialog().ok(addonname, langString(5081), "", "")
			
	if 'VERSION_ID="8.0"' in open(release).read():
		xbmc.executebuiltin("InstallAddon(service.tvheadend42)")

def pvr_tvheadend():
	if 'VERSION_ID="7.0"' in open(release).read():
		if 'Generic' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/generic/pvr.hts.zip'
			install_addon('Addon Tvheadend 4.2', url, 'pvr.hts', 'Tvheadend HTSP Client')
		elif 'Virtual' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/generic/pvr.hts.zip'
			install_addon('Addon Tvheadend 4.2', url, 'pvr.hts', 'Tvheadend HTSP Client')
		elif 'RPi2' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/rpi/pvr.hts.zip'
			install_addon('Addon Tvheadend 4.2', url, 'pvr.hts', 'Tvheadend HTSP Client')
		elif 'WeTek_Core' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/wetekcore/pvr.hts.zip'
			install_addon('Addon Tvheadend 4.2', url, 'pvr.hts', 'Tvheadend HTSP Client')
		elif 'WeTek_Play.arm' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/wetekplay/pvr.hts.zip'
			install_addon('Addon Tvheadend 4.2', url, 'pvr.hts', 'Tvheadend HTSP Client')
		elif 'WeTek_Play_2.aarch64' in open(release).read():
			url ='http://tnds82.xyz/tvhwizard/libreelec/wetekplay2/pvr.hts.zip'		
			install_addon('Addon Tvheadend 4.2', url, 'pvr.hts', 'Tvheadend HTSP Client')
		else:
			xbmcgui.Dialog().ok(addonname, langString(5082), "", "")
			
	if 'VERSION_ID="8.0"' in open(release).read():
		xbmc.executebuiltin("InstallAddon(pvr.hts)")

if __name__ == '__main__':
	if sys.argv[1] == 'oscam':
		service_oscam()
	elif sys.argv[1] == 'tvheadend':
		service_tvheadend()
	elif sys.argv[1] == 'pvr.tvh':
		pvr_tvheadend()
	elif sys.argv[1] == 'ip':
		ip_box()
