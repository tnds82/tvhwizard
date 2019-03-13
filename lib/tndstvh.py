#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmcaddon
import xbmcgui
import xbmc
import pyxbmct, os, time, socket

addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addondata   = xbmc.translatePath(addon.getAddonInfo('profile'))
addonicon   = os.path.join(addonfolder, 'resources/icon.png')
artsfolder  = '/resources/img/tvhwizard'

dialog      = xbmcgui.Dialog()
dialogyesno = dialog.yesno


pyxbmct.skin.estuary = True

class TndsTvh(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(TndsTvh, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image tnds
        image = pyxbmct.Image(addonfolder+artsfolder+'/tnds82.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=16)

		# Channel Manager
        self.cmanager_button = pyxbmct.Button('')
        self.placeControl(self.cmanager_button, 6, 1, rowspan=3, columnspan=3)
        self.connect(self.cmanager_button, self.cmanager_button_update)
        cmanager = pyxbmct.Image(addonfolder+artsfolder+'/cmanager.png')
        self.placeControl(cmanager, 6, 1, rowspan=3, columnspan=3)

		# Group Manager
        self.gmanager_button = pyxbmct.Button('')
        self.placeControl(self.gmanager_button, 6, 12, rowspan=3, columnspan=3)
        self.connect(self.gmanager_button, self.gmanager_button_update)
        gmanager = pyxbmct.Image(addonfolder+artsfolder+'/gmanager.png')
        self.placeControl(gmanager, 6, 12, rowspan=3, columnspan=3)
		
		# Fix Picons
        self.fixpicons_button = pyxbmct.Button('')
        self.placeControl(self.fixpicons_button, 9, 6, rowspan=4, columnspan=4)
        self.connect(self.fixpicons_button, self.fixpicons_button_update)
        gmanager = pyxbmct.Image(addonfolder+artsfolder+'/fixpicons.png')
        self.placeControl(gmanager, 9, 6, rowspan=4, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.cmanager_button)
        self.cmanager_button.controlRight(self.gmanager_button)
        self.gmanager_button.controlLeft(self.cmanager_button)
        self.cmanager_button.controlDown(self.fixpicons_button)
        self.gmanager_button.controlDown(self.fixpicons_button)
        self.fixpicons_button.controlDown(self.close_button)
        self.fixpicons_button.controlUp(self.cmanager_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def gmanager_button_update(self):
        xbmc.executebuiltin('ActivateWindow(pvrgroupmanager)')
		
    def cmanager_button_update(self):
        xbmc.executebuiltin('ActivateWindow(pvrchannelmanager)')

    def fixpicons_button_update(self):
        fp = dialogyesno(addonname, "Attention:", "If skin backgrounds are * .png files, they may need to be replaced","Do you want to continue?")
        if fp :
            self.close()
            import tools
            tools.fixpicons()
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'Fix picons OK', 2000, addonicon))
            time.sleep(2)
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'KODI is restart', 2000, addonicon))
            xbmc.executebuiltin('Reboot')
            
        else :
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'You chose No', 2000, addonicon))		

if __name__ == '__main__':
    tndstvh = TndsTvh('TvhWizard')
    tndstvh.doModal()
    del tndstvh