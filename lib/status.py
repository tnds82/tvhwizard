#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmcaddon, tools

addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')

newcamdhost = tools.return_data('READERS', 'PROTOCOL', 'newcamd', 3)
newcamdport = tools.return_data('READERS', 'PROTOCOL', 'newcamd', 6)
dvbapip     = tools.return_data('OSCAM', 'PROTOCOL', 'dvbapi', 3)
dvbapiport  = tools.return_data('OSCAM', 'PROTOCOL', 'dvbapi', 4)
pathrecord  = tools.return_data('RECORDS', 'ID', 1, 1)
pvripbox    = tools.return_data('PVR', 'PROGRAM', 'tvh_htsp', 4)
usertvh     = tools.return_data('USERS', 'PROGRAM', 'tvhadmin', 2)
useroscam   = tools.return_data('USERS', 'PROGRAM', 'oscam', 2)


class Status():

    def __init__(self):
        if tools.return_data('TVHWIZARD', 'STRING', 'brasil', 2) == 1:
            addon.setSetting(id='country', value='Brasil')
            self.statusbr()
        if tools.return_data('TVHWIZARD', 'STRING', 'portugal', 2) == 1:
            addon.setSetting(id='country', value='Portugal')
            self.statuspt()
	
    def statusbr(self):
        addon.setSetting(id='tvhip', value=pvripbox)
        addon.setSetting(id='useradmin', value=usertvh)
        addon.setSetting(id='pathrecording', value=pathrecord)
        # Box
        if tools.return_data('TVHWIZARD', 'STRING', 'k1plus', 2) == 1:
            addon.setSetting(id='box', value='KI Plus')
        elif tools.return_data('TVHWIZARD', 'STRING', 'k1pro', 2) == 1:
            addon.setSetting(id='box', value='KI Pro')
        elif tools.return_data('TVHWIZARD', 'STRING', 'k2pro', 2) == 1:
            addon.setSetting(id='box', value='KII Pro')
        elif tools.return_data('TVHWIZARD', 'STRING', 'k3pro', 2) == 1:
            addon.setSetting(id='box', value='KIII Pro')
        elif tools.return_data('TVHWIZARD', 'STRING', 'wetekplay2', 2) == 1:
            addon.setSetting(id='box', value='Wetek Play 2')			
        # Tuner
        if tools.return_data('TVHWIZARD', 'STRING', 'kdvbc', 2) == 1:
            addon.setSetting(id='tuner', value='DVB-C')
        elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbs', 2) == 1:
            addon.setSetting(id='tuner', value='DVB-S')
        # Channels
        if tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
            addon.setSetting(id='channels', value='NET')
        elif tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
            addon.setSetting(id='channels', value='Claro TV')
        addon.setSetting(id='softcam', value='NewCamd')
        addon.setSetting(id='ipdvbapi', value=newcamdhost)
        addon.setSetting(id='portdvbapi', value=newcamdport)
			
    def statuspt(self):
        addon.setSetting(id='tvhip', value=pvripbox)
        addon.setSetting(id='useradmin', value=usertvh)
        addon.setSetting(id='pathrecording', value=pathrecord)
        if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
            # Box
            if tools.return_data('TVHWIZARD', 'STRING', 'wetekplay', 2) == 1:
                addon.setSetting(id='box', value='Wetek Play')
            elif tools.return_data('TVHWIZARD', 'STRING', 'wetekplay2', 2) == 1:
                addon.setSetting(id='box', value='Wetek Play 2')
            elif tools.return_data('TVHWIZARD', 'STRING', 'k1plus', 2) == 1:
                addon.setSetting(id='box', value='KI Plus')
            elif tools.return_data('TVHWIZARD', 'STRING', 'k1pro', 2) == 1:
                addon.setSetting(id='box', value='KI Pro')
            elif tools.return_data('TVHWIZARD', 'STRING', 'k2pro', 2) == 1:
                addon.setSetting(id='box', value='KII Pro')
            elif tools.return_data('TVHWIZARD', 'STRING', 'k3pro', 2) == 1:
                addon.setSetting(id='box', value='KIII Pro')
            elif tools.return_data('TVHWIZARD', 'STRING', 'pcix', 2) == 1:
                addon.setSetting(id='box', value='Generic PCI-x')
            elif tools.return_data('TVHWIZARD', 'STRING', 'usb', 2) == 1:
                addon.setSetting(id='box', value='Generic USB')
            elif tools.return_data('TVHWIZARD', 'STRING', 'kvim2', 2) == 1:
                addon.setSetting(id='box', value='Khadas VIM2')
            # Tuner
            if tools.return_data('TVHWIZARD', 'STRING', 'wdvbc', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-C')
            elif tools.return_data('TVHWIZARD', 'STRING', 'wdvbs', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-S')
            elif tools.return_data('TVHWIZARD', 'STRING', 'wdvbt', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-T')
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbc', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-C')
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbs', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-S')
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbt', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-T')
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbts', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-T/S')
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbcs', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-C/S')
            elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbc', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-C')
            elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbs', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-S')
            elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbt', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-T')
            elif tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbc', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-C')
            elif tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbs', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-S')
            elif tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbt', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-T')				
            # Channels
            if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
                addon.setSetting(id='channels', value='NOS')
            elif tools.return_data('TVHWIZARD', 'STRING', 'madeira', 2) == 1:
                addon.setSetting(id='channels', value='Nos Madeira')
            elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
                addon.setSetting(id='channels', value='Nowo')
            elif tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
                addon.setSetting(id='channels', value='Hispasat')
            elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
                addon.setSetting(id='channels', value='Astra')
            elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
                addon.setSetting(id='channels', value='Hotbird')
            elif tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
                addon.setSetting(id='channels', value='TDT Portugal')
            elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
                addon.setSetting(id='channels', value='Meo')
            elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
                addon.setSetting(id='channels', value='Vodafone')		
            addon.setSetting(id='softcam', value='DVBapi')
            addon.setSetting(id='ipdvbapi', value=dvbapip)
            addon.setSetting(id='portdvbapi', value=dvbapiport)
            addon.setSetting(id='readertype', value='cccam')
            addon.setSetting(id='useroscam', value=useroscam)
            if tools.return_data('TVHWIZARD', 'STRING', 'rfirst', 2) == 1:
                addon.setSetting(id='readerfirst', value='Configured')
            if tools.return_data('TVHWIZARD', 'STRING', 'rsecond', 2) == 1:
                addon.setSetting(id='readersecond', value='Configured')
            if tools.return_data('TVHWIZARD', 'STRING', 'rthird', 2) == 1:
                addon.setSetting(id='readerthird', value='Configured')
            if tools.return_data('TVHWIZARD', 'STRING', 'rfourth', 2) == 1:
                addon.setSetting(id='readerfourth', value='Configured')
            if tools.return_data('TVHWIZARD', 'STRING', 'rfifth', 2) == 1:
                addon.setSetting(id='readerfifth', value='Configured')
        else:
            # Box
            if tools.return_data('TVHWIZARD', 'STRING', 'wetekplay', 2) == 1:
                addon.setSetting(id='box', value='Wetek Play')
            elif tools.return_data('TVHWIZARD', 'STRING', 'wetekplay2', 2) == 1:
                addon.setSetting(id='box', value='Wetek Play 2')
            elif tools.return_data('TVHWIZARD', 'STRING', 'k1plus', 2) == 1:
                addon.setSetting(id='box', value='KI Plus')
            elif tools.return_data('TVHWIZARD', 'STRING', 'k1pro', 2) == 1:
                addon.setSetting(id='box', value='KI Pro')
            elif tools.return_data('TVHWIZARD', 'STRING', 'k2pro', 2) == 1:
                addon.setSetting(id='box', value='KII Pro')
            elif tools.return_data('TVHWIZARD', 'STRING', 'k3pro', 2) == 1:
                addon.setSetting(id='box', value='KIII Pro')
            elif tools.return_data('TVHWIZARD', 'STRING', 'pcix', 2) == 1:
                addon.setSetting(id='box', value='Generic PCI-x')
            elif tools.return_data('TVHWIZARD', 'STRING', 'usb', 2) == 1:
                addon.setSetting(id='box', value='Generic USB')
            # Tuner
            if tools.return_data('TVHWIZARD', 'STRING', 'wdvbc', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-C')
            elif tools.return_data('TVHWIZARD', 'STRING', 'wdvbs', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-S')
            elif tools.return_data('TVHWIZARD', 'STRING', 'wdvbt', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-T')
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbc', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-C')
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbs', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-S')
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbt', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-T')
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbts', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-T/S')
            elif tools.return_data('TVHWIZARD', 'STRING', 'kdvbcs', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-C/S')
            elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbc', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-C')
            elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbs', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-S')
            elif tools.return_data('TVHWIZARD', 'STRING', 'gdvbt', 2) == 1:
                addon.setSetting(id='tuner', value='DVB-T')
            # Channels
            if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
                addon.setSetting(id='channels', value='NOS')
            elif tools.return_data('TVHWIZARD', 'STRING', 'madeira', 2) == 1:
                addon.setSetting(id='channels', value='Nos Madeira')
            elif tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
                addon.setSetting(id='channels', value='Nowo')
            elif tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
                addon.setSetting(id='channels', value='Hispasat')
            elif tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
                addon.setSetting(id='channels', value='Astra')
            elif tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
                addon.setSetting(id='channels', value='Hotbird')
            elif tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
                addon.setSetting(id='channels', value='TDT Portugal')
            elif tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
                addon.setSetting(id='channels', value='Meo')
            elif tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
                addon.setSetting(id='channels', value='Vodafone')