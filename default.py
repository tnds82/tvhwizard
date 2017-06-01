#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds82
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,xbmcplugin,xbmcgui,xbmcaddon,os,time,subprocess

from resources.lib import lock

addon             = xbmcaddon.Addon(id='script.tvhwizard')
addonname         = addon.getAddonInfo('name')
addonfolder       = addon.getAddonInfo('path')
addonicon         = os.path.join(addonfolder, 'resources/icon.png')

addondata         = xbmc.translatePath(addon.getAddonInfo('profile'))
addonsettings     = os.path.join(addonfolder, 'resources/settings.xml')
addonresources    = os.path.join(addonfolder, 'resources/')
addonsubsettings  = os.path.join(addonfolder, 'resources/lib/subsettings/')
addoninstructions = os.path.join(addonfolder, 'resources/lib/tutorials/')

addondatasettings = os.path.join(addondata, 'settings.xml')

artsfolder        = '/resources/img/'
fanart            = addonfolder+artsfolder+'/fanart.jpg'
dialog            = xbmcgui.Dialog()
dialogok          = dialog.ok
dialogyesno       = dialog.yesno

################################################## 
#MENUS
def CATEGORIES():
	addDir(langString(5013),1,addonfolder+artsfolder+'/oscam.png')
	addDir(langString(5014),2,addonfolder+artsfolder+'/tvh.png')
	addDir(langString(5015),3,addonfolder+artsfolder+'/reboot.png')
	addDir(langString(5016),4,addonfolder+artsfolder+'/lock.png',True)
	addDir(langString(5017),5,addonfolder+artsfolder+'/channels.png')
	addDir(langString(5018),6,addonfolder+artsfolder+'/groups.png')
	addDir(langString(5019),7,addonfolder+artsfolder+'/update.png')
	addDir(langString(5083),10,addonfolder+artsfolder+'/instructions.png')
	thumbnail()
	
def lock_menu():
	addDir(langString(5020),8,addonfolder+artsfolder+'/addonlock.png')
	addDir(langString(5021),9,addonfolder+artsfolder+'/parental.png')
	thumbnail()
	
##################################################
#FUNCOES
def langString(id):
	return addon.getLocalizedString(id)

def back():
	xbmc.executebuiltin('Action(Back)')
	
def thumbnail():
	skin_used = xbmc.getSkinDir()
	if skin_used == 'skin.confluence':
		xbmc.executebuiltin('Container.SetViewMode(500)')
	elif skin_used == 'skin.aeon.nox':
		xbmc.executebuiltin('Container.SetViewMode(512)')
	elif skin_used == 'skin.aeon.nox.silvo':
		xbmc.executebuiltin('Container.SetViewMode(500)')
	elif skin_used == 'skin.estuary':
		xbmc.executebuiltin('Container.SetViewMode(500)')	
	elif skin_used == 'skin.amber':
		xbmc.executebuiltin('Container.SetViewMode(53)')
	elif skin_used == 'skin.arctic.zephyr':
		xbmc.executebuiltin('Container.SetViewMode(500)')
	elif skin_used == 'skin.mimic':
		xbmc.executebuiltin('Container.SetViewMode(52)')
	elif skin_used == 'skin.titan':
		xbmc.executebuiltin('Container.SetViewMode(509)')

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout

def server():
	from resources.lib.subsettings import serverset
	subprocess_cmd('%s %s%s %s' % ('ln -b', addonsubsettings, 'server.xml', addonsettings))
	serverset.settings()
	subprocess_cmd('%s %s%s %s' % ('cp', addonresources, 'default-settings.xml', addonsettings))
	
	from resources.lib import server

	os.system('systemctl stop service.tvheadend42')
	if addon.getSetting('dvbcards') == 'true':
		if addon.getSetting('wetekpdvbs') == 'true':
			server.tvh_wetekspecial()
			server.tvh_tunners()
			back()
		else: 
			server.tvh_tunners()
	if addon.getSetting('tvhconfig') == 'true':
		server.tvh_config()
	if addon.getSetting('dvbapienable') == 'true':
		server.tvh_dvbapi()
	if addon.getSetting('channelson') == 'true':
		server.tvh_channels()
	if addon.getSetting('picons')  == 'true':
		server.tvh_picons()
	if addon.getSetting('createusers') == 'true':
		server.tvh_users()
	if addon.getSetting('recording') == 'true':
		server.tvh_recording()
	if addon.getSetting('pvrconfig') == 'true':
		server.tvh_pvr()
	if addon.getSetting('kodiconfig') == 'true':		
		server.kodi_config()
	if addon.getSetting('enableguide') == 'true':
		server.tvh_guide()
	if addon.getSetting('timeshift') == 'true':
		server.tvh_timeshift()

	os.system('systemctl start service.tvheadend42')
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(5022), 5000, addonicon))

def client():
	from resources.lib.subsettings import clientset
	subprocess_cmd('%s %s%s %s' % ('ln -b', addonsubsettings, 'client.xml', addonsettings))
	clientset.settings()
	subprocess_cmd('%s %s%s %s' % ('cp', addonresources, 'default-settings.xml', addonsettings))

	from resources.lib import client

	if addon.getSetting('pvrconfig') == 'true':
		client.pvr_config()
	if addon.getSetting ('kodiconfig') == 'true':
		client.kodi_config()
	if addon.getSetting('enableguide') == 'true':
		client.tvh_guide()
	
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(5023), 5000, addonicon))

def instructions():
	from resources.lib.tutorials import instructions
	instructions.Tvwpage1().doModal()

def update():
	if not os.path.exists(xbmcaddon.Addon(id='service.tvheadend42').getAddonInfo('path')):
		dialogok(addonname, langString(5024), langString(5025), langString(5026))
	else:
		if not 'updatetvh' in open(addonsettings).read():
			from resources.lib.subsettings import updateset
			subprocess_cmd('%s %s%s %s' % ('ln -b', addonsubsettings, 'update.xml', addonsettings))
			updateset.settings()
			subprocess_cmd('%s %s%s %s' % ('cp', addonresources, 'default-settings.xml', addonsettings))
		else:
			upsett = dialogyesno(addonname, langString(5027), langString(5028), langString(5029), langString(5030), langString(5031))
			if upsett == 0:
				if addon.getSetting('updatetvh') == 'true':
					from resources.lib import update
					update.zone_channels()
				else:
					xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(5032), 5000, addonicon))
			if upsett == 1:
				from resources.lib.subsettings import updateset
				subprocess_cmd('%s %s%s %s' % ('ln -b', addonsubsettings, 'update.xml', addonsettings))
				updateset.settings()
				subprocess_cmd('%s %s%s %s' % ('cp', addonresources, 'default-settings.xml', addonsettings))

def manage_channels():
	xbmc.executebuiltin('ActivateWindow(pvrchannelmanager)')

def manage_groups():
	xbmc.executebuiltin('ActivateWindow(pvrgroupmanager)')
	
def adlock():
	from resources.lib.subsettings import lockset
	subprocess_cmd('%s %s%s %s' % ('ln -b', addonsubsettings, 'lock.xml', addonsettings))

	lock.run()
	
	subprocess_cmd('%s %s%s %s' % ('cp', addonresources, 'default-settings.xml', addonsettings))
	
def channel_lock():
	from resources.lib.subsettings import lockset
	subprocess_cmd('%s %s%s %s' % ('ln -b', addonsubsettings, 'lock.xml', addonsettings))

	lock.parental_control()

	subprocess_cmd('%s %s%s %s' % ('cp', addonresources, 'default-settings.xml', addonsettings))

def oscam():
	from resources.lib.subsettings import oscamset
	subprocess_cmd('%s %s%s %s' % ('ln -b', addonsubsettings, 'oscam.xml', addonsettings))
	oscamset.settings()
	subprocess_cmd('%s %s%s %s' % ('cp', addonresources, 'default-settings.xml', addonsettings))

	from resources.lib import oscam
	
	os.system('systemctl stop service.softcam.oscam')
	if addon.getSetting('oscamenable') == 'true':
		oscam.oscam_enable()
	if addon.getSetting ('dvbapioscam') == 'true':
		oscam.dvbapi_enable()
	if addon.getSetting ('cccamenable') == 'true':
		oscam.cccam_enable()
	if addon.getSetting('firstreader') == 'true':
		oscam.oscam_reader('server1', 'first')
	if addon.getSetting('secondreader') == 'true':	
		oscam.oscam_reader('server2', 'second')
	if addon.getSetting('thirdreader') == 'true':
		oscam.oscam_reader('server3', 'third')
	if addon.getSetting('fourthreader') == 'true':
		oscam.oscam_reader('server4', 'fourth')
	if addon.getSetting('fifthreader') == 'true':
		oscam.oscam_reader('server5', 'fifth')
	if addon.getSetting('firstuser') == 'true':
		oscam.oscam_user('user1', 'first')
	if addon.getSetting('seconduser') == 'true':
		oscam.oscam_user('user2', 'second')
	if addon.getSetting('thirduser') == 'true':
		oscam.oscam_user('user3', 'third')
	if addon.getSetting('fourthuser') == 'true':
		oscam.oscam_user('user4', 'fourth')
	if addon.getSetting('fifthuser') == 'true':
		oscam.oscam_user('user5', 'fifth')
	os.system('systemctl start service.softcam.oscam')
	
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(5033), 5000, addonicon))
	
def reboot():
	time.sleep(1)
	os.system("reboot")
	
######################################################FUNCOES JÁ FEITAS
def addDir(name,mode,iconimage,pasta=False,folderDel=None):
        if sys.argv[0] < 0: sys.argv[0] = 1
        u=sys.argv[0]+"?folderDel="+str(folderDel)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',addonfolder+'/fanart.jpg')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
        return ok
		
###############################GET PARAMS
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
        return param
      
params=get_params()
folderDel=None
name=None
mode=None
iconimage=None

try: folderDel=urllib.unquote_plus(params["folderDel"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Mode: "+str(mode)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "folderDel: "+str(folderDel)

#################################
#MODOS

if mode==None:
	if not os.path.exists(addondata):
		os.makedirs(addondata)
		
		addon.setSetting(id='parentalcfg', value='false')
		addon.setSetting(id='addonpin', value='')

	if '<setting id="parentalcfg" value="false" />' in open(addondatasettings).read():
		CATEGORIES()
	else:
		password = addon.getSetting('addonpin')
		unlock = dialog.input(langString(5034), type=xbmcgui.INPUT_PASSWORD, option=xbmcgui.PASSWORD_VERIFY);
		if unlock == password:
			CATEGORIES()
		else:
			dialogok(addonname, langString(5035))

elif mode==1:
	oscam()
elif mode==2:
	tvhconfig = dialog.yesno(addonname, langString(5036), langString(5037), langString(5038), langString(5039), langString(5040))
	if tvhconfig == 0:
		server()
	if tvhconfig == 1:
		client()
elif mode==3: 
	reboot()
elif mode==4: 
	lock_menu()
elif mode==5: 
	manage_channels()
elif mode==6: 
	manage_groups()
elif mode==7: 
	update()
elif mode==8:
	adlock()
elif mode==9:
	channel_lock()
elif mode==10:
	instructions()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
