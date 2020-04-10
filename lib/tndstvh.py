#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmcaddon
import xbmcgui
import xbmc, urllib2, inspect
import pyxbmct, os, time, socket, tools, update, reset, upload

addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addondata   = xbmc.translatePath(addon.getAddonInfo('profile'))
addonicon   = os.path.join(addonfolder, 'resources/icon.png')
artsfolder  = '/resources/img/tvhwizard'
channelver  = os.path.join(addondata, 'version')

dialog      = xbmcgui.Dialog()
dialogyesno = dialog.yesno

pathrecord  = tools.return_data('RECORDS', 'ID', 1, 1)
usertvh     = tools.return_data('USERS', 'PROGRAM', 'tvhadmin', 2)
pvripbox    = tools.return_data('PVR', 'PROGRAM', 'tvh_htsp', 4)
newcamdhost = tools.return_data('READERS', 'PROTOCOL', 'newcamd', 3)
newcamdport = tools.return_data('READERS', 'PROTOCOL', 'newcamd', 6)
useroscam   = tools.return_data('USERS', 'PROGRAM', 'oscam', 2)
dvbapip     = tools.return_data('OSCAM', 'PROTOCOL', 'dvbapi', 3)
dvbapiport  = tools.return_data('OSCAM', 'PROTOCOL', 'dvbapi', 4)
channelsversion = tools.version_channels()



pyxbmct.skin.estuary = True

def langString(id):
	return addon.getLocalizedString(id)

class Status(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Status, self).__init__(title)
        self.setGeometry(1200, 680, 20, 24)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image tnds
        image = pyxbmct.Image(addonfolder+artsfolder+'/tnds82.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=24)

        #status
        image = pyxbmct.Image(addonfolder+artsfolder+'/statusmall.png')
        self.placeControl(image, 8, 1, rowspan=2, columnspan=4)
        #tvheadend
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhsmall.png')
        self.placeControl(image, 10, 0, rowspan=1, columnspan=3)
        label = pyxbmct.Label('INSTALLED', textColor='0xFF61B86A')
        self.placeControl(label, 10, 3, columnspan=3)
        #oscam
        image = pyxbmct.Image(addonfolder+artsfolder+'/oscsmall.png')
        self.placeControl(image, 12, 0, rowspan=1, columnspan=3)
        if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
           label = pyxbmct.Label('INSTALLED', textColor='0xFF61B86A')
           self.placeControl(label, 12, 3, columnspan=3)
        else:
           label = pyxbmct.Label('NOT INSTALLED', textColor='0xFFFF4A4A')
           self.placeControl(label, 12, 3, columnspan=4)
        #yourip
        image = pyxbmct.Image(addonfolder+artsfolder+'/yourip.png')
        self.placeControl(image, 14, 0, rowspan=1, columnspan=3)		
        label = pyxbmct.Label(pvripbox, textColor='0xFF009BC2')
        self.placeControl(label, 14, 3, columnspan=4)
        #country
        image = pyxbmct.Image(addonfolder+artsfolder+'/countrysmall.png')
        self.placeControl(image, 16, 0, rowspan=1, columnspan=3)		
        if tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
            label = pyxbmct.Label('BRASIL', textColor='0xFF009BC2')
            self.placeControl(label, 16, 3, columnspan=3)
        elif tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
            label = pyxbmct.Label('PORTUGAL', textColor='0xFF009BC2')
            self.placeControl(label, 16, 3, columnspan=3)
        #MENU TVHEADEND
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvheadendsmall.png')
        self.placeControl(image, 8, 9, rowspan=2, columnspan=4)
        #username
        image = pyxbmct.Image(addonfolder+artsfolder+'/status/username.png')
        self.placeControl(image, 10, 7, rowspan=1, columnspan=3)
        #box
        image = pyxbmct.Image(addonfolder+artsfolder+'/status/box.png')
        self.placeControl(image, 11, 7, rowspan=1, columnspan=3)
        #tunner
        image = pyxbmct.Image(addonfolder+artsfolder+'/status/tuner.png')
        self.placeControl(image, 12, 7, rowspan=1, columnspan=3)
        #channels
        image = pyxbmct.Image(addonfolder+artsfolder+'/status/channels.png')
        self.placeControl(image, 13, 7, rowspan=1, columnspan=3)
        #recpath
        image = pyxbmct.Image(addonfolder+artsfolder+'/status/recpath.png')
        self.placeControl(image, 14, 7, rowspan=1, columnspan=3)
        #channelsversion
        image = pyxbmct.Image(addonfolder+artsfolder+'/status/channelsversion.png')
        self.placeControl(image, 18, 7, rowspan=1, columnspan=3)
        label = pyxbmct.Label(channelsversion, textColor='0xFF009BC2')
        self.placeControl(label, 18, 10, columnspan=4)
        if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
            if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
                self.checkupdate('nos')
            else:
                self.checkupdate('nosfree')
        elif tools.return_data('TVHWIZARD', 'STRING', 'madeira', 2) == 1:
            self.checkupdate('madeira')
        elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
            self.checkupdate('nowo')
        elif tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
            self.checkupdate('hispasat')
        elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
            self.checkupdate('astra')
        elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
            self.checkupdate('hotbird')
        elif tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
            self.checkupdate('tdt')
        elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
            self.checkupdate('meo')
        elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
            self.checkupdate('vodafone')
        elif tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
            self.checkupdate('net')
        elif tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
            self.checkupdate('clarotv')		
        if tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
            #softcam
            image = pyxbmct.Image(addonfolder+artsfolder+'/status/softcam.png')
            self.placeControl(image, 15, 7, rowspan=1, columnspan=3)
            #hostname
            image = pyxbmct.Image(addonfolder+artsfolder+'/status/hostname.png')
            self.placeControl(image, 16, 7, rowspan=1, columnspan=3)
            #port
            image = pyxbmct.Image(addonfolder+artsfolder+'/status/port.png')
            self.placeControl(image, 17, 7, rowspan=1, columnspan=3)
        elif tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
            if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
                #softcam
                image = pyxbmct.Image(addonfolder+artsfolder+'/status/softcam.png')
                self.placeControl(image, 15, 7, rowspan=1, columnspan=3)
                #hostname
                image = pyxbmct.Image(addonfolder+artsfolder+'/status/hostname.png')
                self.placeControl(image, 16, 7, rowspan=1, columnspan=3)
                #port
                image = pyxbmct.Image(addonfolder+artsfolder+'/status/port.png')
                self.placeControl(image, 17, 7, rowspan=1, columnspan=3)
        #MENU OSCAM
        if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
            image = pyxbmct.Image(addonfolder+artsfolder+'/oscamsmall.png')
            self.placeControl(image, 8, 18, rowspan=2, columnspan=4)
            #username
            image = pyxbmct.Image(addonfolder+artsfolder+'/status/username.png')
            self.placeControl(image, 10, 16, rowspan=1, columnspan=3)
            #softcam
            image = pyxbmct.Image(addonfolder+artsfolder+'/status/softcam.png')
            self.placeControl(image, 11, 16, rowspan=1, columnspan=3)
            #readertype
            image = pyxbmct.Image(addonfolder+artsfolder+'/status/readertype.png')
            self.placeControl(image, 12, 16, rowspan=1, columnspan=3)
            #reader1
            if tools.return_data('TVHWIZARD', 'STRING', 'rfirst', 2) == 1:
               image = pyxbmct.Image(addonfolder+artsfolder+'/status/reader1.png')
               self.placeControl(image, 13, 16, rowspan=1, columnspan=3)
            #reader2
            if tools.return_data('TVHWIZARD', 'STRING', 'rsecond', 2) == 1:
               image = pyxbmct.Image(addonfolder+artsfolder+'/status/reader2.png')
               self.placeControl(image, 14, 16, rowspan=1, columnspan=3)
            #reader3
            if tools.return_data('TVHWIZARD', 'STRING', 'rthird', 2) == 1:
               image = pyxbmct.Image(addonfolder+artsfolder+'/status/reader3.png')
               self.placeControl(image, 15, 16, rowspan=1, columnspan=3)
            #reader4
            if tools.return_data('TVHWIZARD', 'STRING', 'rfourth', 2) == 1:
               image = pyxbmct.Image(addonfolder+artsfolder+'/status/reader4.png')
               self.placeControl(image, 16, 16, rowspan=1, columnspan=3)
            #reader5
            if tools.return_data('TVHWIZARD', 'STRING', 'rfifth', 2) == 1:
               image = pyxbmct.Image(addonfolder+artsfolder+'/status/reader5.png')
               self.placeControl(image, 17, 16, rowspan=1, columnspan=3)
        #BRASIL
        if tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
            label = pyxbmct.Label(usertvh, textColor='0xFF009BC2')
            self.placeControl(label, 10, 10, columnspan=4)
            label = pyxbmct.Label(pathrecord, textColor='0xFF009BC2')
            self.placeControl(label, 14, 10, columnspan=6)
            if tools.return_data('TVHWIZARD', 'STRING', 'k1plus', 2) == 1:
                label = pyxbmct.Label('KI Plus', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=2)
            elif tools.return_data('TVHWIZARD', 'STRING', 'k1pro', 2) == 1:
                label = pyxbmct.Label('KI Pro', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=2)
            elif tools.return_data('TVHWIZARD', 'STRING', 'k2pro', 2) == 1:
                label = pyxbmct.Label('KII Pro', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=2)
            elif tools.return_data('TVHWIZARD', 'STRING', 'k3pro', 2) == 1:
                label = pyxbmct.Label('KIII Pro', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=2)
            elif tools.return_data('TVHWIZARD', 'STRING', 'wetekplay2', 2) == 1:
                label = pyxbmct.Label('Wetek Play 2', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=2)
            if tools.return_data('TVHWIZARD', 'STRING', 'kdvbc', 2) == 1:
                label = pyxbmct.Label('DVB-C', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=2)
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbs', 2) == 1:
                label = pyxbmct.Label('DVB-S', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=2)
            if tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
                label = pyxbmct.Label('NET', textColor='0xFF009BC2')
                self.placeControl(label, 13, 10, columnspan=2)
            elif tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
                label = pyxbmct.Label('Claro TV', textColor='0xFF009BC2')
                self.placeControl(label, 13, 10, columnspan=2)
            label = pyxbmct.Label('Newcamd', textColor='0xFF009BC2')
            self.placeControl(label, 15, 10, columnspan=3)
            label = pyxbmct.Label(newcamdhost, textColor='0xFF009BC2')
            self.placeControl(label, 16, 10, columnspan=6)
            label = pyxbmct.Label(newcamdport, textColor='0xFF009BC2')
            self.placeControl(label, 17, 10, columnspan=2)				
        #PORTUGAL
        elif tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
            label = pyxbmct.Label(usertvh, textColor='0xFF009BC2')
            self.placeControl(label, 10, 10, columnspan=6)
            label = pyxbmct.Label(pathrecord, textColor='0xFF009BC2')
            self.placeControl(label, 14, 10, columnspan=6)
            if tools.return_data('TVHWIZARD', 'STRING', 'k1plus', 2) == 1:
                label = pyxbmct.Label('KI Plus', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'k1pro', 2) == 1:
                label = pyxbmct.Label('KI Pro', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'k2pro', 2) == 1:
                label = pyxbmct.Label('KII Pro', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'k3pro', 2) == 1:
                label = pyxbmct.Label('KIII Pro', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'wetekplay2', 2) == 1:
                label = pyxbmct.Label('Wetek Play 2', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=4)
            elif tools.return_data('TVHWIZARD', 'STRING', 'wetekplay', 2) == 1:
                label = pyxbmct.Label('Wetek Play', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=4)
            elif tools.return_data('TVHWIZARD', 'STRING', 'pcix', 2) == 1:
                label = pyxbmct.Label('Generic PCI-x', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=4)
            elif tools.return_data('TVHWIZARD', 'STRING', 'usb', 2) == 1:
                label = pyxbmct.Label('Generic USB', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=4)
            elif tools.return_data('TVHWIZARD', 'STRING', 'kvim2', 2) == 1:
                label = pyxbmct.Label('Khadas VIM2', textColor='0xFF009BC2')
                self.placeControl(label, 11, 10, columnspan=4)
            if tools.return_data('TVHWIZARD', 'STRING', 'wdvbc', 2) == 1:
                label = pyxbmct.Label('DVB-C', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'wdvbs', 2) == 1:
                label = pyxbmct.Label('DVB-S', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'wdvbt', 2) == 1:
                label = pyxbmct.Label('DVB-T', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbc', 2) == 1:
                label = pyxbmct.Label('DVB-C', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbs', 2) == 1:
                label = pyxbmct.Label('DVB-S', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbt', 2) == 1:
                label = pyxbmct.Label('DVB-T', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbts', 2) == 1:
                label = pyxbmct.Label('DVB-T/S', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbcs', 2) == 1:
                label = pyxbmct.Label('DVB-C/S', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbc', 2) == 1:
                label = pyxbmct.Label('DVB-C', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbs', 2) == 1:
                label = pyxbmct.Label('DVB-S', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbt', 2) == 1:
                label = pyxbmct.Label('DVB-T', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbc', 2) == 1:
                label = pyxbmct.Label('DVB-C', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbs', 2) == 1:
                label = pyxbmct.Label('DVB-S', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbt', 2) == 1:
                label = pyxbmct.Label('DVB-T', textColor='0xFF009BC2')
                self.placeControl(label, 12, 10, columnspan=3)
            if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
                label = pyxbmct.Label('NOS', textColor='0xFF009BC2')
                self.placeControl(label, 13, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'madeira', 2) == 1:
                label = pyxbmct.Label('Nos Madeira', textColor='0xFF009BC2')
                self.placeControl(label, 13, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
                label = pyxbmct.Label('Nowo', textColor='0xFF009BC2')
                self.placeControl(label, 13, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
                label = pyxbmct.Label('Hispasat', textColor='0xFF009BC2')
                self.placeControl(label, 13, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
                label = pyxbmct.Label('Astra', textColor='0xFF009BC2')
                self.placeControl(label, 13, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
                label = pyxbmct.Label('Hotbird', textColor='0xFF009BC2')
                self.placeControl(label, 13, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
                label = pyxbmct.Label('TDT Portugal', textColor='0xFF009BC2')
                self.placeControl(label, 13, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
                label = pyxbmct.Label('Meo', textColor='0xFF009BC2')
                self.placeControl(label, 13, 10, columnspan=3)
            elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
                label = pyxbmct.Label('Vodafone', textColor='0xFF009BC2')
                self.placeControl(label, 13, 10, columnspan=3)
            if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
                label = pyxbmct.Label('DVBapi', textColor='0xFF009BC2')
                self.placeControl(label, 15, 10, columnspan=3)
                label = pyxbmct.Label(dvbapip, textColor='0xFF009BC2')
                self.placeControl(label, 16, 10, columnspan=6)
                label = pyxbmct.Label(dvbapiport, textColor='0xFF009BC2')
                self.placeControl(label, 17, 10, columnspan=3)				
                label = pyxbmct.Label(useroscam, textColor='0xFF009BC2')
                self.placeControl(label, 10, 19, columnspan=4)
                label = pyxbmct.Label('DVBapi', textColor='0xFF009BC2')
                self.placeControl(label, 11, 19, columnspan=3)
                label = pyxbmct.Label('CCcam', textColor='0xFF009BC2')
                self.placeControl(label, 12, 19, columnspan=3)
                if tools.return_data('TVHWIZARD', 'STRING', 'rfirst', 2) == 1:
                    label = pyxbmct.Label('Configured', textColor='0xFF009BC2')
                    self.placeControl(label, 13, 19, columnspan=3)
                if tools.return_data('TVHWIZARD', 'STRING', 'rsecond', 2) == 1:
                    label = pyxbmct.Label('Configured', textColor='0xFF009BC2')
                    self.placeControl(label, 14, 19, columnspan=3)
                if tools.return_data('TVHWIZARD', 'STRING', 'rthird', 2) == 1:
                    label = pyxbmct.Label('Configured', textColor='0xFF009BC2')
                    self.placeControl(label, 15, 19, columnspan=3)
                if tools.return_data('TVHWIZARD', 'STRING', 'rfourth', 2) == 1:
                    label = pyxbmct.Label('Configured', textColor='0xFF009BC2')
                    self.placeControl(label, 16, 19, columnspan=3)
                if tools.return_data('TVHWIZARD', 'STRING', 'rfifth', 2) == 1:
                    label = pyxbmct.Label('Configured', textColor='0xFF009BC2')
                    self.placeControl(label, 17, 19, columnspan=3)

		# More Options button
        self.mopts_button = pyxbmct.Button('More Options')
        self.placeControl(self.mopts_button, 19, 18, rowspan=1, columnspan=4)
        self.connect(self.mopts_button, lambda: self.mopts())

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 19, 22, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.close_button, self.close)

    def checkupdate(self, path):
        url_version = '%s%s%s' % ("https://addons.tnds82.xyz/addon/tvhwizard/update/channels/", path, "version")
        check = urllib2.urlopen(url_version)
        check1 = open(channelver, "r")
        for line1 in check:
            for line2 in check1:
                if line1==line2:
                    label = pyxbmct.Label('Updated', textColor='0xFF61B86A')
                    self.placeControl(label, 18, 13, columnspan=4)
                else:
                    label = pyxbmct.Label('Not Updated', textColor='0xFFFF4A4A')
                    self.placeControl(label, 18, 13, columnspan=4)
                    self.update_button = pyxbmct.Button('Update')
                    self.placeControl(self.update_button, 19, 15, rowspan=1, columnspan=3)
                    self.connect(self.update_button, lambda: self.update())


    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlLeft(self.mopts_button)
        self.mopts_button.controlRight(self.close_button)
        if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
            if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
                self.check('nos')
            else:
                self.check('nosfree')
        elif tools.return_data('TVHWIZARD', 'STRING', 'madeira', 2) == 1:
            self.check('madeira')
        elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
            self.check('nowo')
        elif tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
            self.check('hispasat')
        elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
            self.check('astra')
        elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
            self.check('hotbird')
        elif tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
            self.check('tdt')
        elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
            self.check('meo')
        elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
            self.check('vodafone')
        elif tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
            self.check('net')
        elif tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
            self.check('clarotv')		
	    # Set initial focus.
        self.setFocus(self.close_button)

    def check(self, path):
        url_version = '%s%s%s' % ("https://addons.tnds82.xyz/addon/tvhwizard/update/channels/", path, "version")
        check = urllib2.urlopen(url_version)
        check1 = open(channelver, "r")
        for line1 in check:
            for line2 in check1:
                if line1==line2:
                    pass
                else: 
                    self.mopts_button.controlLeft(self.update_button)
                    self.update_button.controlRight(self.mopts_button)

    def mopts(self):
        self.close()
        TndsTvh().doModal()

    def update(self):
        self.close()
        update.Update()

class TndsTvh(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(TndsTvh, self).__init__(title)
        self.setGeometry(1200, 680, 17, 17)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image tnds
        image = pyxbmct.Image(addonfolder+artsfolder+'/tnds82.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=17)

		# Channel Manager
        self.cmanager_button = pyxbmct.Button('')
        self.placeControl(self.cmanager_button, 8, 2, rowspan=3, columnspan=3)
        self.connect(self.cmanager_button, self.cmanager_button_update)
        cmanager = pyxbmct.Image(addonfolder+artsfolder+'/cmanager.png')
        self.placeControl(cmanager, 8, 2, rowspan=3, columnspan=3)

		# Group Manager
        self.gmanager_button = pyxbmct.Button('')
        self.placeControl(self.gmanager_button, 12, 2, rowspan=3, columnspan=3)
        self.connect(self.gmanager_button, self.gmanager_button_update)
        gmanager = pyxbmct.Image(addonfolder+artsfolder+'/gmanager.png')
        self.placeControl(gmanager, 12, 2, rowspan=3, columnspan=3)
		
		# Fix Picons
        self.fixpicons_button = pyxbmct.Button('')
        self.placeControl(self.fixpicons_button, 8, 7, rowspan=3, columnspan=3)
        self.connect(self.fixpicons_button, self.fixpicons_button_update)
        fixpicons = pyxbmct.Image(addonfolder+artsfolder+'/fixpicons.png')
        self.placeControl(fixpicons, 8, 7, rowspan=3, columnspan=3)

        # Check update Channels
        self.upchannels_button = pyxbmct.Button('')
        self.placeControl(self.upchannels_button, 8, 12, rowspan=3, columnspan=3)
        self.connect(self.upchannels_button, self.upchannels_button_update)
        upchannels = pyxbmct.Image(addonfolder+artsfolder+'/upchannels.png')
        self.placeControl(upchannels, 8, 12, rowspan=3, columnspan=3)

		# Reset Config
        self.resetconfig_button = pyxbmct.Button('')
        self.placeControl(self.resetconfig_button, 	12, 7, rowspan=3, columnspan=3)
        self.connect(self.resetconfig_button, self.resetconfig_button_update)
        resetconfig = pyxbmct.Image(addonfolder+artsfolder+'/resetconfig.png')
        self.placeControl(resetconfig, 12, 7, rowspan=3, columnspan=3)

		# Upload Channels
        self.uploadchannels_button = pyxbmct.Button('')
        self.placeControl(self.uploadchannels_button, 12, 12, rowspan=3, columnspan=3)
        self.connect(self.uploadchannels_button, self.uploadchannels_button_update)
        uploadchannels = pyxbmct.Image(addonfolder+artsfolder+'/uploadchannels.png')
        self.placeControl(uploadchannels, 12, 12, rowspan=3, columnspan=3)

		# Back button
        self.back_button = pyxbmct.Button('Back')
        self.placeControl(self.back_button, 16, 13, rowspan=1, columnspan=2)
        self.connect(self.back_button, lambda: self.back())


		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 16, 15, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.cmanager_button)
        self.close_button.controlLeft(self.back_button)
        self.cmanager_button.controlDown(self.gmanager_button)
        self.cmanager_button.controlRight(self.fixpicons_button)
        self.gmanager_button.controlUp(self.cmanager_button)
        self.gmanager_button.controlDown(self.back_button)
        self.gmanager_button.controlRight(self.resetconfig_button)
        self.fixpicons_button.controlDown(self.resetconfig_button)
        self.fixpicons_button.controlRight(self.upchannels_button)
        self.fixpicons_button.controlLeft(self.cmanager_button)
        self.resetconfig_button.controlUp(self.fixpicons_button)
        self.resetconfig_button.controlDown(self.back_button)
        self.resetconfig_button.controlRight(self.uploadchannels_button)
        self.resetconfig_button.controlLeft(self.gmanager_button)
        self.upchannels_button.controlDown(self.uploadchannels_button)
        self.upchannels_button.controlLeft(self.fixpicons_button)
        self.uploadchannels_button.controlUp(self.upchannels_button)
        self.uploadchannels_button.controlDown(self.back_button)
        self.uploadchannels_button.controlLeft(self.resetconfig_button)
        self.back_button.controlRight(self.close_button)
        self.back_button.controlUp(self.cmanager_button)
		
	    # Set initial focus.
        self.setFocus(self.close_button)

    def back(self):
        self.close()
        Status().doModal()

    def gmanager_button_update(self):
        xbmc.executebuiltin('ActivateWindow(pvrgroupmanager)')
		
    def cmanager_button_update(self):
        xbmc.executebuiltin('ActivateWindow(pvrchannelmanager)')

    def fixpicons_button_update(self):
        fp = dialogyesno(addonname, "Attention:", "If skin backgrounds are * .png files, they may need to be replaced","Do you want to continue?")
        if fp :
            self.close()
            tools.fixpicons()
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50020), 2000, addonicon))
            time.sleep(2)
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50023), 2000, addonicon))
            xbmc.executebuiltin('Reboot')
            
        else :
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50021), 2000, addonicon))		

    def upchannels_button_update(self):
        upchannels = dialogyesno(addonname, "CHECK FOR UPDATE CHANNELS", "","Do you want to continue?")
        if upchannels :
            self.close()
            update.Update()
        else :
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50021), 2000, addonicon))		

    def resetconfig_button_update(self):
        self.close()
        reset.Reset()
		
    def uploadchannels_button_update(self):
		self.close()
		upload.Upload()
