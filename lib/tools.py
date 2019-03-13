#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import urllib, os, re, urllib2, xbmc, xbmcgui, xbmcaddon, zipfile
import json, shutil, subprocess
import platform
from collections import OrderedDict

addon         = xbmcaddon.Addon(id='script.tvhwizard')
addonname     = addon.getAddonInfo('name')

# Constants

STRING = 0
BOOL = 1
NUM = 2

dp = xbmcgui.DialogProgress()

def writeLog(message, level=xbmc.LOGDEBUG):
    xbmc.log('[%s %s] %s' % (xbmcaddon.Addon().getAddonInfo('id'),
                             xbmcaddon.Addon().getAddonInfo('version'),
                             message.encode('utf-8')), level)

def langString(id):
	return addon.getLocalizedString(id)

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout

def fixpicons():
	subprocess_cmd("rm $HOME/.kodi/userdata/Thumbnails/*/*.png")
	subprocess_cmd("rm $HOME/.kodi/userdata/Database/Textures13.db")


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
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, "Download cancelled", 1000, addonicon))
        dp.close()
        sys.exit()
		
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

def jsonrpc(query):
    querystring = {"jsonrpc": "2.0", "id": 1}
    querystring.update(query)
    try:
        response = json.loads(xbmc.executeJSONRPC(json.dumps(querystring, encoding='utf-8')))
        if 'result' in response: return response['result']
    except TypeError, e:
        writeLog('Error executing JSON RPC: %s' % (e.message), xbmc.LOGFATAL)
    return None

def changekeyjson(path, stringold, stringnew):
	jsonFile = open(path, "r")
	data = json.load(jsonFile, object_pairs_hook=OrderedDict)
	jsonFile.close()

	tmp = data[stringold]
	data[stringnew] = data[stringold]
	del data[stringold]
	
	jsonFile = open(path, "w+")
	jsonFile.write(json.dumps(data, indent=4))
	jsonFile.close()

def addkeyjson(path, string, value):
	jsonFile = open(path, "r") # Open the JSON file for reading
	data = json.load(jsonFile, object_pairs_hook=OrderedDict) # Read the JSON into the buffer
	jsonFile.close() # Close the JSON file

	data[string] = value
	
	jsonFile = open(path, "w+")
	jsonFile.write(json.dumps(data, indent=4))
	jsonFile.close()

def updateJsonFile(path, string, value):
	jsonFile = open(path, "r") # Open the JSON file for reading
	data = json.load(jsonFile, object_pairs_hook=OrderedDict) # Read the JSON into the buffer
	jsonFile.close() # Close the JSON file

	tmp = data[string]
	data[string] = value
	
	jsonFile = open(path, "w+")
	jsonFile.write(json.dumps(data, indent=4))
	jsonFile.close()

def dvbc(path, network):	
	jsonFile = open(path, "r")
	data = json.load(jsonFile, object_pairs_hook=OrderedDict)
	jsonFile.close()
	
	data['frontends']['DVB-C #0']['enabled'] = True
	data['frontends']['DVB-C #0']['networks'] = [network]
	
	jsonFile = open(path, "w+")
	jsonFile.write(json.dumps(data, indent=4))
	jsonFile.close()

def dvbt(path, network):	
	jsonFile = open(path, "r")
	data = json.load(jsonFile, object_pairs_hook=OrderedDict)
	jsonFile.close()
	
	data['frontends']['DVB-T #0']['enabled'] = True
	data['frontends']['DVB-T #0']['networks'] = [network]
	
	jsonFile = open(path, "w+")
	jsonFile.write(json.dumps(data, indent=4))
	jsonFile.close()

def dvbs(path, network):
	jsonFile = open(path, "r")
	data = json.load(jsonFile, object_pairs_hook=OrderedDict)
	jsonFile.close()
	
	data['frontends']['DVB-S #0']['enabled'] = True
	data['frontends']['DVB-S #0']['networks'] = [network]
	data['frontends']['DVB-S #0']['satconf']['elements'][0]['networks'] = [network]
	
	jsonFile = open(path, "w+")
	jsonFile.write(json.dumps(data, indent=4))
	jsonFile.close()

def channels(url):
	tndsDir = os.path.join('/tmp/tnds82')
	packageFile = os.path.join('/tmp/tnds82', 'channels.zip')
	header = 'Channels for Tvheadend'
	dp = xbmcgui.DialogProgress()
	if not os.path.exists(tndsDir):
		os.makedirs(tndsDir)
	downloader(url,packageFile,header)
	extract(packageFile,tndsDir,dp,header)
	
def picons(url, path):
	piconspath = os.path.join('/storage/picons/')
	piconsDir = os.path.join('/storage/picons/vdr/')
	packageFile = os.path.join('/tmp/tnds82', 'picons.zip')
	header = 'Picons for Tvheadend'
	dp = xbmcgui.DialogProgress()
	if not os.path.exists(piconspath):
		os.makedirs(piconspath)	
	if not os.path.exists(piconsDir):
		os.makedirs(piconsDir)
	downloader(url,packageFile,header)
	extract(packageFile,piconsDir,dp,header)

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
	with open(filenamedvr, "w") as outfile:
		json.dump({'enabled':True, 'name':name, 'comment':'Recording Profile', 'profile':profile,
			'cache':2, 'retention-days':31, 'removal-days':0, 'clone':True, 'rerecord-errors':0,
			'warm-time':0, 'pre-extra-time':0, 'post-extra-time':0, 'epg-update-window':86400, 
			'epg-running':False, 'autorec-maxcount':0, 'autorec-maxsched':0, 'storage':recordingpath,
			'storage-mfree':1000, 'storage-mused':0, 'file-permissions':0644, 'charset':'UTF-8',
			'tag-files':True, 'skip-commercials':True, 'pathname':'%F/$c/$t$-c$n.$x', 'directory-permissions':0755,
			'day-dir':True, 'channel-dir':True, 'title-dir':False, 'channel-in-title':True,
			'date-in-title':False, 'time-in-title':False, 'episode-in-title':False, 'subtitle-in-title':False,
			'omit-title':False, 'clean-title':False, 'whitespace-in-title':False, 'windows-compatible-filenames':False}, outfile, indent=4)
			
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

def pvrsettings(dest, hostname, password, username):
	createsett = open(dest, 'a')
	createsett.write("<settings>\n")
	createsett.write('    <setting id="autorec_approxtime" value="0" />\n')
	createsett.write('    <setting id="autorec_maxdiff" value="15" />\n')
	createsett.write('    <setting id="connect_timeout" value="10" />\n')
	createsett.write('    <setting id="dvr_dubdetect" value="0" />\n')
	createsett.write('    <setting id="dvr_lifetime" value="8" />\n')
	createsett.write('    <setting id="dvr_priority" value="2" />\n')
	createsett.write('    <setting id="epg_async" value="false" />\n')
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

def set_addon(module, enabled):
    query = {"method": "Addons.SetAddonEnabled",
             "params": {"addonid": module, "enabled": enabled}}
    response = jsonrpc(query)
    if response == 'OK':
        writeLog('driver module \'%s\' %s' % (module, 'enabled' if enabled else 'disabled'), xbmc.LOGNOTICE)
        return True
    else:
        writeLog('could not %s driver module \'%s\'' % ('enable' if enabled else 'disable', module), xbmc.LOGERROR)
    return False
