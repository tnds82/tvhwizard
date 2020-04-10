#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmcaddon
import xbmc
import pyxbmct, os, subprocess, time

import portugal
import brasil
import tools

addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addondata   = xbmc.translatePath(addon.getAddonInfo('profile'))
addonicon   = os.path.join(addonfolder, 'resources/icon.png')
artsfolder  = '/resources/img/tvhwizard'
addonsetts  = os.path.join(addondata, 'settings.xml')
database    = os.path.join(addondata, 'tvhwizard.db')

pyxbmct.skin.estuary = True

def langString(id):
    return addon.getLocalizedString(id)

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout

class Country(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Country, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/tnds82.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

        # Portugal
        self.portugal_button = pyxbmct.RadioButton('')
        self.placeControl(self.portugal_button, 9, 3, rowspan=2, columnspan=4)
        self.connect(self.portugal_button, self.portugal_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
            self.portugal_button.setSelected(True)
        else:
            self.portugal_button.setSelected(False)
        portugal = pyxbmct.Image(addonfolder+artsfolder+'/portugal.png')
        self.placeControl(portugal, 9, 3, rowspan=2, columnspan=4)

        # Brasil
        self.brasil_button = pyxbmct.RadioButton('')
        self.placeControl(self.brasil_button, 9, 9, rowspan=2, columnspan=4)
        self.connect(self.brasil_button, self.brasil_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
            self.brasil_button.setSelected(True)
        else:
            self.brasil_button.setSelected(False)
        brasil = pyxbmct.Image(addonfolder+artsfolder+'/brasil.png')
        self.placeControl(brasil, 9, 9, rowspan=2, columnspan=4)

        # Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.portugal_button)
        self.portugal_button.controlDown(self.close_button)
        self.portugal_button.controlRight(self.brasil_button)
        self.brasil_button.controlDown(self.close_button)
        self.brasil_button.controlLeft(self.portugal_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def portugal_button_update(self):
        if self.portugal_button.isSelected():
            self.close()
            tools.insert_tvhwizard('portugal', 1)
            portugal.Start().doModal()
        else:
            tools.insert_tvhwizard('portugal', 0)

    def brasil_button_update(self):
        if self.brasil_button.isSelected():
            self.close()
            tools.insert_tvhwizard('brasil', 1)
            brasil.TvheadendBR().doModal()
        else:
            tools.insert_tvhwizard('brasil', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

class TvhWizard(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(TvhWizard, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image tnds
        image = pyxbmct.Image(addonfolder+artsfolder+'/tnds82.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# Image Welcome
        image = pyxbmct.Image(addonfolder+artsfolder+'/welcome.png')
        self.placeControl(image, 8, 4, rowspan=2, columnspan=8)
		
		# Start button
        self.start_button = pyxbmct.Button('START')
        self.placeControl(self.start_button, 11, 7, rowspan=1, columnspan=2)
        self.connect(self.start_button, lambda: self.page())

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.start_button.controlRight(self.close_button)
        self.close_button.controlLeft(self.start_button)
	    # Set initial focus.
        self.setFocus(self.start_button)

    def page(self):
        self.close()
        if not os.path.exists(database):
            tools.create_database()
        Country().doModal()

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))