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

import sys
import xbmcaddon


from lib import tvhwizard
from lib import tndstvh

addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')

if addon.getSetting('tvhstatus') == 'Configured':
	tndstvh.TndsTvh().doModal()
else:
	tvhwizard.TvhWizard().doModal()