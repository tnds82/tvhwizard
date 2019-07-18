#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import sys
import xbmcaddon


from lib import tvhwizard

addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')

if addon.getSetting('tvhstatus') == 'Configured':
	from lib import tndstvh
	tndstvh.Status().doModal()
else:
	tvhwizard.TvhWizard().doModal()