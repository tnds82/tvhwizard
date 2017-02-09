#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
#########################################################################################
import xbmcaddon


	##### ADDON CONFIG TVHEADEND #####
addon            = xbmcaddon.Addon(id='script.tvhwizard')
addonname        = addon.getAddonInfo('name')
addonfolder      = addon.getAddonInfo('path')

def settings():
	addon.openSettings()
