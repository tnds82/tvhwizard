#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds82
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib, os, re, urllib2, xbmc, xbmcgui, xbmcaddon, zipfile

addon         = xbmcaddon.Addon(id='script.tvhwizard')
addonname     = addon.getAddonInfo('name')

dp = xbmcgui.DialogProgress()

def langString(id):
	return addon.getLocalizedString(id)

def downloader(url,dest, header):
    
    dp.create(header, langString(5075), langString(5080))
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        print percent
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled():
        d = xbmcgui.Dialog()
        print "DOWNLOAD CANCELLED" # need to get this part working
        d.notification(addonname, langString(5074), xbmcgui.NOTIFICATION_INFO, 1000)
        dp.close()

def extract(_in, _out, dp, header):
    dp.create(header, langString(5076), langString(5080))

    zin = zipfile.ZipFile(_in,  'r')

    nFiles = float(len(zin.infolist()))
    count  = 0

    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dp.update(int(update))
            zin.extract(item, _out)
    except Exception, e:
        print str(e)
        return False

    return True
	
def channels(url):
	tndsDir = os.path.join('/storage/.kodi/tnds82')
	packageFile = os.path.join('/storage/.kodi/tnds82', 'channels.zip')
	header = 'Channels for Tvheadend'
	dp = xbmcgui.DialogProgress()
	if not os.path.exists(tndsDir):
		os.makedirs(tndsDir)
	downloader(url,packageFile,header)
	extract(packageFile,tndsDir,dp,header)
	
def picons(url):
	piconsDir = os.path.join('/storage/.kodi/userdata/picons')
	packageFile = os.path.join('/storage/.kodi/tnds82', 'picons.zip')
	header = 'Picons for Tvheadend'
	dp = xbmcgui.DialogProgress()
	if not os.path.exists(piconsDir):
		os.makedirs(piconsDir)
	downloader(url,packageFile,header)
	extract(packageFile,piconsDir,dp,header)

   ##### NETWORKS #####
dvbctuner        = '"type": "DVB-C"'
dvbstuner        = '"type": "DVB-S"'

def wetek2cable(tuner, enable, cable):
	wdvbcinput = open(tuner, 'r')
	contents = wdvbcinput.readlines()
	wdvbcinput.close()
	del contents[11]
	contents.insert(11, enable)
	contents.insert(21, cable)
	wdvbcinput = open(tuner, 'w')
	contents = "".join(contents)
	wdvbcinput.write(contents)
	wdvbcinput.close()

def wetek2sat(tuner, enable, sat, sat1):
	wdvbsinput = open(tuner, 'r')
	contents = wdvbsinput.readlines()
	wdvbsinput.close()
	del contents[11]
	contents.insert(11, enable)
	contents.insert(21, sat)
	contents.insert(37, sat1)
	wdvbsinput = open(tuner, 'w')
	contents = "".join(contents)
	wdvbsinput.write(contents)
	wdvbsinput.close()

def wetekcable(tuner, enable, cable):
	wdvbcinput = open(tuner, 'r')
	contents = wdvbcinput.readlines()
	wdvbcinput.close()
	del contents[35]
	contents.insert(35, enable)
	contents.insert(45, cable)
	wdvbcinput = open(tuner, 'w')
	contents = "".join(contents)
	wdvbcinput.write(contents)
	wdvbcinput.close()

def weteksat(tuner, enable, sat, sat1):
	wdvbsinput = open(tuner, 'r')
	contents = wdvbsinput.readlines()
	wdvbsinput.close()
	del contents[11]
	contents.insert(11, enable)
	contents.insert(21, sat)
	contents.insert(37, sat1)
	wdvbsinput = open(tuner, 'w')
	contents = "".join(contents)
	wdvbsinput.write(contents)
	wdvbsinput.close()

def k1sat(tuner, enable, sat, sat1):
	wdvbsinput = open(tuner, 'r')
	contents = wdvbsinput.readlines()
	wdvbsinput.close()
	del contents[56]
	contents.insert(56, enable)
	contents.insert(65, sat)
	contents.insert(81, sat1)
	wdvbsinput = open(tuner, 'w')
	contents = "".join(contents)
	wdvbsinput.write(contents)
	wdvbsinput.close()
	
def generic(tuner, enable, cable, sat, sat1):
	arquivo = open(tuner, 'r')
	linhas = arquivo.readlines()
	arquivo.close()
	for linha in linhas:
		if dvbctuner in linha:
			input = open(tuner, 'r')
			contents = input.readlines()
			input.close()
			del contents[11]
			contents.insert(11, enable)
			contents.insert(21, cable)
			input = open(tuner, 'w')
			contents = "".join(contents)
			input.write(contents)
			input.close()
		if dvbstuner in linha:
			input = open(tuner, 'r')
			contents = input.readlines()
			input.close()
			del contents[11]
			contents.insert(11, enable)
			contents.insert(21, sat)
			contents.insert(37, sat1)
			input = open(tuner, 'w')
			contents = "".join(contents)
			input.write(contents)
			input.close()

def check_mkvprofile(number, source):
	profilepathname = os.listdir(source)[number]
	profilepath     = "%s%s" % (source, profilepathname)
	if '"profile-matroska"' in  open(profilepath).read():
		return profilepathname
	else:
		None
		
def check_passprofile(number, source):
	profilepathname = os.listdir(source)[number]
	profilepath     = "%s%s" % (source, profilepathname)
	if '"profile-mpegts"' in  open(profilepath).read():
		return profilepathname
	else:
		None

def check_htspprofile(number, source):
	profilepathname = os.listdir(source)[number]
	profilepath     = "%s%s" % (source, profilepathname)
	if '"profile-htsp"' in  open(profilepath).read():
		return profilepathname
	else:
		None
			
def recording_profile(profile, recordingpath, source, name):
	filenamedvr = "%s%s" % (source, "42c91dae1ea94fbc2a46d456491b4179")
	recordingprofile = open(filenamedvr, 'a')
	recordingprofile.write('{\n')
	recordingprofile.write('	"enabled": true,\n')
	recordingprofile.write('	"name": "%s",\n' % name)
	recordingprofile.write('	"comment": "Recording Profile",\n')
	recordingprofile.write('	"profile": "%s",\n' % profile)
	recordingprofile.write('	"cache": 2,\n')
	recordingprofile.write('	"retention-days": 31,\n')
	recordingprofile.write('	"removal-days": 0,\n')
	recordingprofile.write('	"clone": true,\n')
	recordingprofile.write('	"rerecord-errors": 0,\n')
	recordingprofile.write('	"warm-time": 30,\n')
	recordingprofile.write('	"pre-extra-time": 0,\n')
	recordingprofile.write('	"post-extra-time": 0,\n')
	recordingprofile.write('	"epg-update-window": 86400,\n')
	recordingprofile.write('	"epg-running": false,\n')
	recordingprofile.write('	"autorec-maxcount": 0,\n')
	recordingprofile.write('	"autorec-maxsched": 0,\n')
	recordingprofile.write('	"storage": "%s",\n' % recordingpath)
	recordingprofile.write('	"storage-mfree": 1000,\n')
	recordingprofile.write('	"storage-mused": 0,\n')
	recordingprofile.write('	"file-permissions": "0664",\n')
	recordingprofile.write('	"charset": "UTF-8",\n')
	recordingprofile.write('	"tag-files": true,\n')
	recordingprofile.write('	"skip-commercials": true,\n')
	recordingprofile.write('	"pathname": "%F/$c/$t$-c$n.$x",\n')
	recordingprofile.write('	"directory-permissions": "0775",\n')
	recordingprofile.write('	"day-dir": true,\n')
	recordingprofile.write('	"channel-dir": true,\n')
	recordingprofile.write('	"title-dir": false,\n')
	recordingprofile.write('	"channel-in-title": true,\n')
	recordingprofile.write('	"date-in-title": false,\n')
	recordingprofile.write('	"time-in-title": false,\n')
	recordingprofile.write('	"episode-in-title": false,\n')
	recordingprofile.write('	"subtitle-in-title": false,\n')
	recordingprofile.write('	"omit-title": false,\n')
	recordingprofile.write('	"clean-title": false,\n')
	recordingprofile.write('	"whitespace-in-title": false,\n')
	recordingprofile.write('	"windows-compatible-filenames": false\n')
	recordingprofile.write('}\n')
	recordingprofile.close()
			
def wetekexample():
	url = "http://tnds82.xyz/tvhwizard/channels/wetek.png"
	xbmc.executebuiltin("ShowPicture(%s)"%url)

def advancedsettings_jarvis(dest):
	optprofile = open(dest, 'a')
	optprofile.write('<!-- Created using Config Tvheadend addon by tnds82 -->\n')
	optprofile.write('<advancedsettings>\n')
	optprofile.write('    <network>\n')
	optprofile.write('        <cachemembuffersize>0</cachemembuffersize>\n')
	optprofile.write('        <readbufferfactor>20</readbufferfactor>\n')
	optprofile.write('    </network>\n')
	optprofile.write('    <videoscanner>\n')
	optprofile.write('        <ignoreerrors>true</ignoreerrors>\n')
	optprofile.write('    </videoscanner>\n')
	optprofile.write('    <gui>\n')
	optprofile.write('        <algorithmdirtyregions>3</algorithmdirtyregions>\n')
	optprofile.write('        <nofliptimeout>0</nofliptimeout>\n')
	optprofile.write('    </gui>\n')
	optprofile.write('    <lookandfeel>\n')
	optprofile.write('        <enablerssfeeds>false</enablerssfeeds>\n')
	optprofile.write('    </lookandfeel>\n')
	optprofile.write('    <splash>false</splash>\n')
	optprofile.write('    <pvr>\n')
	optprofile.write('        <minvideocachelevel>0</minvideocachelevel>\n')
	optprofile.write('        <minaudiocachelevel>0</minaudiocachelevel>\n')
	optprofile.write('        <maxvideocachelevel>0</maxvideocachelevel>\n')
	optprofile.write('        <maxaudiocachelevel>0</maxaudiocachelevel>\n')
	optprofile.write('        <cacheindvdplayer>false</cacheindvdplayer>\n')
	optprofile.write('    </pvr>\n')
	optprofile.write('    <musiclibrary>\n')
	optprofile.write('        <backgroundupdate>true</backgroundupdate>\n')
	optprofile.write('    </musiclibrary>\n')
	optprofile.write('</advancedsettings>\n')
	optprofile.close()

def advancedsettings_krypton(dest):
	optprofile = open(dest, 'a')
	optprofile.write('<!-- Created using Config Tvheadend addon by tnds82 -->\n')
	optprofile.write('<advancedsettings>\n')
	optprofile.write('    <cache>\n')
	optprofile.write('        <memorysize>419430400</memorysize>\n')
	optprofile.write('        <readfactor>20</readfactor>\n')
	optprofile.write('    </cache>\n')
	optprofile.write('    <videoscanner>\n')
	optprofile.write('        <ignoreerrors>true</ignoreerrors>\n')
	optprofile.write('    </videoscanner>\n')
	optprofile.write('    <gui>\n')
	optprofile.write('        <algorithmdirtyregions>3</algorithmdirtyregions>\n')
	optprofile.write('        <nofliptimeout>0</nofliptimeout>\n')
	optprofile.write('    </gui>\n')
	optprofile.write('    <lookandfeel>\n')
	optprofile.write('        <enablerssfeeds>false</enablerssfeeds>\n')
	optprofile.write('    </lookandfeel>\n')
	optprofile.write('    <splash>false</splash>\n')
	optprofile.write('    <pvr>\n')
	optprofile.write('        <minvideocachelevel>0</minvideocachelevel>\n')
	optprofile.write('        <minaudiocachelevel>0</minaudiocachelevel>\n')
	optprofile.write('        <maxvideocachelevel>0</maxvideocachelevel>\n')
	optprofile.write('        <maxaudiocachelevel>0</maxaudiocachelevel>\n')
	optprofile.write('        <cacheindvdplayer>false</cacheindvdplayer>\n')
	optprofile.write('    </pvr>\n')
	optprofile.write('    <musiclibrary>\n')
	optprofile.write('        <backgroundupdate>true</backgroundupdate>\n')
	optprofile.write('    </musiclibrary>\n')
	optprofile.write('</advancedsettings>\n')
	optprofile.close()

def change_words(file, words):
	lines = []
	with open(file) as infile:
		for line in infile:
			for src, target in words.iteritems():
				line = line.replace(src, target)
			lines.append(line)
	with open(file, 'w') as outfile:
		for line in lines:
			outfile.write(line)

def remove_words(file, liner):
	insert = open(file, 'r')
	contents = insert.readlines()
	insert.close()
	del contents[liner]
	insert = open(file, "w")
	contents = "".join(contents)
	insert.write(contents)
	insert.close()
			
def insert_words(file, line, words):
	insert = open(file, 'r')
	contents = insert.readlines()
	insert.close()
	contents.insert(line, words)
	insert = open(file, "w")
	contents = "".join(contents)
	insert.write(contents)
	insert.close()
	
def removeinsert_words(file, liner, line, words):
	insert = open(file, 'r')
	contents = insert.readlines()
	insert.close()
	del contents[liner]
	contents.insert(line, words)
	insert = open(file, "w")
	contents = "".join(contents)
	insert.write(contents)
	insert.close()

def removeinsert_2words(file, liner1, liner2, line, words):
	insert = open(file, 'r')
	contents = insert.readlines()
	insert.close()
	del contents[liner1]
	del contents[liner2]
	contents.insert(line, words)
	insert = open(file, "w")
	contents = "".join(contents)
	insert.write(contents)
	insert.close()

def pvrsettings(dest, hostname, password, username):
	createsett = open(dest, 'a')
	createsett.write("<settings>\n")
	createsett.write('    <setting id="autorec_approxtime" value="0" />\n')
	createsett.write('    <setting id="autorec_maxdiff" value="15" />\n')
	createsett.write('    <setting id="connect_timeout" value="10" />\n')
	createsett.write('    <setting id="dvr_dubdetect" value="0" />\n')
	createsett.write('    <setting id="dvr_lifetime" value="8" />\n')
	createsett.write('    <setting id="dvr_priority" value="2" />\n')
	createsett.write('    <setting id="epg_async" value="true" />\n')
	createsett.write('    <setting id="host" value="%s" />\n' % hostname)
	createsett.write('    <setting id="htsp_port" value="9982" />\n')
	createsett.write('    <setting id="http_port" value="9981" />\n')
	createsett.write('    <setting id="pass" value="%s" />\n' % password)
	createsett.write('    <setting id="pretuner_closedelay" value="5" />\n')
	createsett.write('    <setting id="pretuner_enabled" value="false" />\n')
	createsett.write('    <setting id="response_timeout" value="5" />\n')
	createsett.write('    <setting id="streaming_profile" value="" />\n')
	createsett.write('    <setting id="total_tuners" value="10" />\n')
	createsett.write('    <setting id="trace_debug" value="false" />\n')
	createsett.write('    <setting id="user" value="%s" />\n' % username)
	createsett.write('</settings>\n')
	createsett.close()	
	
def readercccam(dest, nome, hostname, port, username, passw, description):
	createreader = open(dest, 'a')
	createreader.write("[reader]\n")
	createreader.write("label                         = %s\n" % nome)
	createreader.write("description                   = %s\n" % description)
	createreader.write("enable                        = 1\n")
	createreader.write("protocol                      = cccam\n")
	createreader.write("device                        = %s,%s\n" % (hostname, port))
	createreader.write("user                          = %s\n" % username)
	createreader.write("password                      = %s\n" % passw)
	createreader.write("inactivitytimeout             = 30\n")
	createreader.write("group                         = 1\n")
	createreader.write("cccversion                    = 2.3.0\n")
	createreader.write("ccckeepalive                  = 1\n")
	createreader.write("cccreshare                    = 2\n")
	createreader.write("\n")
	createreader.close()
			
def readernewcamd(dest, nome, username, passw, description):
	createreader = open(dest, 'a')
	createreader.write("[reader]\n")
	createreader.write("label                         = %s\n" % nome)
	createreader.write("description                   = %s\n" % description)
	createreader.write("enable                        = 1\n")
	createreader.write("protocol                      = newcamd\n")
	createreader.write("key                           = 0102030405060708091011121314\n")
	createreader.write("user                          = %s\n" % username)
	createreader.write("password                      = %s\n" % passw)
	createreader.write("connectoninit                 = 1\n")
	createreader.write("fallback                      = 1\n")
	createreader.write("group                         = 1\n")
	createreader.write("\n")
	createreader.close()
			
def readercs357x(dest, nome, hostname, port, username, passw, description):
	createreader = open(dest, 'a')
	createreader.write("[reader]\n")
	createreader.write("label                         = %s\n" % nome)
	createreader.write("description                   = %s\n" % description)
	createreader.write("enable                        = 1\n")
	createreader.write("protocol                      = cs357x\n")
	createreader.write("device                        = %s,%s\n" % (hostname, port))
	createreader.write("user                          = %s\n" % username)
	createreader.write("password                      = %s\n" % passw)
	createreader.write("fallback                      = 1\n")
	createreader.write("group                         = 1\n")
	createreader.write("\n")
	createreader.close()
	
def usercccam(dest, username, passw, description):
	createuser = open(dest, 'a')
	createuser.write("[account]\n")
	createuser.write("disabled                      = 0\n")
	createuser.write("description                   = %s\n" % description)
	createuser.write("user                          = %s\n" % username)
	createuser.write("pwd                           = %s\n" % passw)
	createuser.write("keepalive                     = 1\n")
	createuser.write("au                            = 1\n")
	createuser.write("group                         = 1\n")
	createuser.write("\n")
	createuser.close()

