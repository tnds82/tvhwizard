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

import xbmcaddon

addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')

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
		if addon.getSetting('porto') == 'true':
			addon.setSetting(id='channels', value='NOS Porto')
		elif addon.getSetting('coimbra') == 'true':
			addon.setSetting(id='channels', value='NOS Coimbra')
		elif addon.getSetting('leiria') == 'true':
			addon.setSetting(id='channels', value='NOS Leiria')
		elif addon.getSetting('lisboa') == 'true':
			addon.setSetting(id='channels', value='NOS Lisboa')
		elif addon.getSetting('madeira') == 'true':
			addon.setSetting(id='channels', value='NOS Madeira')
		elif addon.getSetting('acores') == 'true':
			addon.setSetting(id='channels', value='NOS Açores')
		elif addon.getSetting('mirandela') == 'true':
			addon.setSetting(id='channels', value='NOS Mirandela')
		elif addon.getSetting('santarem') == 'true':
			addon.setSetting(id='channels', value='NOS Santarem')
		elif addon.getSetting('stejo') == 'true':
			addon.setSetting(id='channels', value='NOS Sul Tejo')
		elif addon.getSetting('evora') == 'true':
			addon.setSetting(id='channels', value='NOS Évora')
		elif addon.getSetting('algarve') == 'true':
			addon.setSetting(id='channels', value='NOS Algarve')
		elif addon.getSetting('hispasat') == 'true':
			addon.setSetting(id='channels', value='Hispasat')
		elif addon.getSetting('astra') == 'true':
			addon.setSetting(id='channels', value='Astra')
		elif addon.getSetting('hotbird') == 'true':
			addon.setSetting(id='channels', value='Hotbird')
		elif addon.getSetting('tdt') == 'true':
			addon.setSetting(id='channels', value='TDT Portugal')
		elif addon.getSetting('meo') == 'true':
			addon.setSetting(id='channels', value='TDT Meo')
		elif addon.getSetting('vodafone') == 'true':
			addon.setSetting(id='channels', value='TDT Vodafone')		
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
		if addon.getSetting('porto') == 'true':
			addon.setSetting(id='channels', value='NOS Porto')
		elif addon.getSetting('coimbra') == 'true':
			addon.setSetting(id='channels', value='NOS Coimbra')
		elif addon.getSetting('leiria') == 'true':
			addon.setSetting(id='channels', value='NOS Leiria')
		elif addon.getSetting('lisboa') == 'true':
			addon.setSetting(id='channels', value='NOS Lisboa')
		elif addon.getSetting('madeira') == 'true':
			addon.setSetting(id='channels', value='NOS Madeira')
		elif addon.getSetting('acores') == 'true':
			addon.setSetting(id='channels', value='NOS Açores')
		elif addon.getSetting('mirandela') == 'true':
			addon.setSetting(id='channels', value='NOS Mirandela')
		elif addon.getSetting('santarem') == 'true':
			addon.setSetting(id='channels', value='NOS Santarem')
		elif addon.getSetting('stejo') == 'true':
			addon.setSetting(id='channels', value='NOS Sul Tejo')
		elif addon.getSetting('evora') == 'true':
			addon.setSetting(id='channels', value='NOS Évora')
		elif addon.getSetting('algarve') == 'true':
			addon.setSetting(id='channels', value='NOS Algarve')
		elif addon.getSetting('hispasat') == 'true':
			addon.setSetting(id='channels', value='Hispasat')
		elif addon.getSetting('astra') == 'true':
			addon.setSetting(id='channels', value='Astra')
		elif addon.getSetting('hotbird') == 'true':
			addon.setSetting(id='channels', value='Hotbird')
		elif addon.getSetting('tdt') == 'true':
			addon.setSetting(id='channels', value='TDT Portugal')
		elif addon.getSetting('meo') == 'true':
			addon.setSetting(id='channels', value='TDT Meo')
		elif addon.getSetting('vodafone') == 'true':
			addon.setSetting(id='channels', value='TDT Vodafone')		

