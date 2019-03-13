#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmcaddon

addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')

newcamdhost = addon.getSetting('newcamdhost')
newcamdport = addon.getSetting('newcamdport')


def statusbr():
	if addon.getSetting('wetekplay2') == 'true':
		addon.setSetting(id='box', value='Wetek Play 2')
	elif addon.getSetting('k1plus') == 'true':
		addon.setSetting(id='box', value='KI Plus')
	elif addon.getSetting('k1pro') == 'true':
		addon.setSetting(id='box', value='KI Pro')
	elif addon.getSetting('k2pro') == 'true':
		addon.setSetting(id='box', value='KII Pro')
	elif addon.getSetting('k3pro') == 'true':
		addon.setSetting(id='box', value='KIII Pro')
	if addon.getSetting('kdvbc') == 'true':
		addon.setSetting(id='tuner', value='DVB-C')
	elif addon.getSetting('kdvbs') == 'true':
		addon.setSetting(id='tuner', value='DVB-S')
	if addon.getSetting('net') == 'true':
		addon.setSetting(id='channels', value='NET')
	elif addon.getSetting('clarotv') == 'true':
		addon.setSetting(id='channels', value='Claro TV')
	if addon.getSetting('dvbapichoose') == 'newcamd':
		addon.setSetting(id='softcam', value='NewCamd')
		addon.setSetting(id='ipdvbapi', value=newcamdhost)
		addon.setSetting(id='portdvbapi', value=newcamdport)
					

def status():
	if addon.getSetting('start') == 'tvhwosc':
		addon.setSetting(id='softcam', value='dvbapi')
		addon.setSetting(id='readertype', value='cccam')
		if addon.getSetting('firstreader') == 'true':
			addon.setSetting(id='readerfirst', value='Configured')
		if addon.getSetting('secondreader') == 'true':
			addon.setSetting(id='readersecond', value='Configured')
		if addon.getSetting('thirdreader') == 'true':
			addon.setSetting(id='readerthird', value='Configured')
		if addon.getSetting('fourthreader') == 'true':
			addon.setSetting(id='readerfourth', value='Configured')
		if addon.getSetting('fifthreader') == 'true':
			addon.setSetting(id='readerfifth', value='Configured')
		if addon.getSetting('wetekplay') == 'true':
			addon.setSetting(id='box', value='Wetek Play')
		elif addon.getSetting('wetekplay2') == 'true':
			addon.setSetting(id='box', value='Wetek Play 2')
		elif addon.getSetting('wetekplay2s') == 'true':
			addon.setSetting(id='box', value='Wetek Play 2s')
		elif addon.getSetting('k1plus') == 'true':
			addon.setSetting(id='box', value='KI Plus')
		elif addon.getSetting('k1pro') == 'true':
			addon.setSetting(id='box', value='KI Pro')
		elif addon.getSetting('k2pro') == 'true':
			addon.setSetting(id='box', value='KII Pro')
		elif addon.getSetting('k3pro') == 'true':
			addon.setSetting(id='box', value='KIII Pro')
		elif addon.getSetting('pcix') == 'true':
			addon.setSetting(id='box', value='Generic PCI-x')
		elif addon.getSetting('usb') == 'true':
			addon.setSetting(id='box', value='Generic USB')
		if addon.getSetting('wdvbc') == 'true':
			addon.setSetting(id='tuner', value='DVB-C')
		elif addon.getSetting('wdvbs') == 'true':
			addon.setSetting(id='tuner', value='DVB-S')
		elif addon.getSetting('wdvbt') == 'true':
			addon.setSetting(id='tuner', value='DVB-T')
		elif addon.getSetting('kdvbc') == 'true':
			addon.setSetting(id='tuner', value='DVB-C')
		elif addon.getSetting('kdvbs') == 'true':
			addon.setSetting(id='tuner', value='DVB-S')
		elif addon.getSetting('kdvbt') == 'true':
			addon.setSetting(id='tuner', value='DVB-T')
		elif addon.getSetting('kdvbts') == 'true':
			addon.setSetting(id='tuner', value='DVB-T/S')
		elif addon.getSetting('kdvbcs') == 'true':
			addon.setSetting(id='tuner', value='DVB-C/S')
		elif addon.getSetting('gdvbc') == 'true':
			addon.setSetting(id='tuner', value='DVB-C')
		elif addon.getSetting('gdvbs') == 'true':
			addon.setSetting(id='tuner', value='DVB-S')
		elif addon.getSetting('gdvbt') == 'true':
			addon.setSetting(id='tuner', value='DVB-T')
		if addon.getSetting('nos') == 'true':
			addon.setSetting(id='channels', value='NOS')
		elif addon.getSetting('nowo') == 'true':
			addon.setSetting(id='channels', value='Nowo')
		elif addon.getSetting('hispasat') == 'true':
			addon.setSetting(id='channels', value='Hispasat')
		elif addon.getSetting('astra') == 'true':
			addon.setSetting(id='channels', value='Astra')
		elif addon.getSetting('hotbird') == 'true':
			addon.setSetting(id='channels', value='Hotbird')
		elif addon.getSetting('tdt') == 'true':
			addon.setSetting(id='channels', value='TDT Portugal')
		elif addon.getSetting('meo') == 'true':
			addon.setSetting(id='channels', value='Meo')
		elif addon.getSetting('vodafone') == 'true':
			addon.setSetting(id='channels', value='Vodafone')		
	else:
		if addon.getSetting('wetekplay') == 'true':
			addon.setSetting(id='box', value='Wetek Play')
		elif addon.getSetting('wetekplay2') == 'true':
			addon.setSetting(id='box', value='Wetek Play 2')
		elif addon.getSetting('wetekplay2s') == 'true':
			addon.setSetting(id='box', value='Wetek Play 2s')
		elif addon.getSetting('k1plus') == 'true':
			addon.setSetting(id='box', value='KI Plus')
		elif addon.getSetting('k1pro') == 'true':
			addon.setSetting(id='box', value='KI Pro')
		elif addon.getSetting('k2pro') == 'true':
			addon.setSetting(id='box', value='KII Pro')
		elif addon.getSetting('k3pro') == 'true':
			addon.setSetting(id='box', value='KIII Pro')
		elif addon.getSetting('pcix') == 'true':
			addon.setSetting(id='box', value='Generic PCI-x')
		elif addon.getSetting('usb') == 'true':
			addon.setSetting(id='box', value='Generic USB')
		if addon.getSetting('wdvbc') == 'true':
			addon.setSetting(id='tuner', value='DVB-C')
		elif addon.getSetting('wdvbs') == 'true':
			addon.setSetting(id='tuner', value='DVB-S')
		elif addon.getSetting('wdvbt') == 'true':
			addon.setSetting(id='tuner', value='DVB-T')
		elif addon.getSetting('kdvbc') == 'true':
			addon.setSetting(id='tuner', value='DVB-C')
		elif addon.getSetting('kdvbs') == 'true':
			addon.setSetting(id='tuner', value='DVB-S')
		elif addon.getSetting('kdvbt') == 'true':
			addon.setSetting(id='tuner', value='DVB-T')
		elif addon.getSetting('kdvbts') == 'true':
			addon.setSetting(id='tuner', value='DVB-T/S')
		elif addon.getSetting('kdvbcs') == 'true':
			addon.setSetting(id='tuner', value='DVB-C/S')
		elif addon.getSetting('gdvbc') == 'true':
			addon.setSetting(id='tuner', value='DVB-C')
		elif addon.getSetting('gdvbs') == 'true':
			addon.setSetting(id='tuner', value='DVB-S')
		elif addon.getSetting('gdvbt') == 'true':
			addon.setSetting(id='tuner', value='DVB-T')
		if addon.getSetting('nos') == 'true':
			addon.setSetting(id='channels', value='NOS')
		elif addon.getSetting('nowo') == 'true':
			addon.setSetting(id='channels', value='Nowo')
		elif addon.getSetting('hispasat') == 'true':
			addon.setSetting(id='channels', value='Hispasat')
		elif addon.getSetting('astra') == 'true':
			addon.setSetting(id='channels', value='Astra')
		elif addon.getSetting('hotbird') == 'true':
			addon.setSetting(id='channels', value='Hotbird')
		elif addon.getSetting('tdt') == 'true':
			addon.setSetting(id='channels', value='TDT Portugal')
		elif addon.getSetting('meo') == 'true':
			addon.setSetting(id='channels', value='Meo')
		elif addon.getSetting('vodafone') == 'true':
			addon.setSetting(id='channels', value='Vodafone')		

