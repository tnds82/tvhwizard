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
import xbmcgui
import xbmc
import pyxbmct, os, time, socket

addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addondata   = xbmc.translatePath(addon.getAddonInfo('profile'))
addonicon   = os.path.join(addonfolder, 'resources/icon.png')
artsfolder  = '/resources/img/tvhwizard'

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
        self.placeControl(self.cmanager_button, 8, 2, rowspan=3, columnspan=3)
        self.connect(self.cmanager_button, self.cmanager_button_update)
        cmanager = pyxbmct.Image(addonfolder+artsfolder+'/cmanager.png')
        self.placeControl(cmanager, 8, 2, rowspan=3, columnspan=3)

		# Group Manager
        self.gmanager_button = pyxbmct.Button('')
        self.placeControl(self.gmanager_button, 8, 11, rowspan=3, columnspan=3)
        self.connect(self.gmanager_button, self.gmanager_button_update)
        gmanager = pyxbmct.Image(addonfolder+artsfolder+'/gmanager.png')
        self.placeControl(gmanager, 8, 11, rowspan=3, columnspan=3)
		
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
        self.cmanager_button.controlDown(self.close_button)
        self.gmanager_button.controlDown(self.close_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def gmanager_button_update(self):
        xbmc.executebuiltin('ActivateWindow(pvrgroupmanager)')
		
    def cmanager_button_update(self):
        xbmc.executebuiltin('ActivateWindow(pvrchannelmanager)')		

if __name__ == '__main__':
    tndstvh = TndsTvh('TvhWizard')
    tndstvh.doModal()
    del tndstvh