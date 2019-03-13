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

pyxbmct.skin.estuary = True

def langString(id):
	return addon.getLocalizedString(id)

class FinishBR(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(FinishBR, self).__init__(title)
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
        image = pyxbmct.Image(addonfolder+artsfolder+'/finish.png')
        self.placeControl(image, 8, 4, rowspan=2, columnspan=8)
		
		# Finish button
        self.start_button = pyxbmct.Button('FINISH')
        self.placeControl(self.start_button, 11, 7, rowspan=1, columnspan=2)
        self.connect(self.start_button, lambda: self.page())

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.start_button.controlRight(self.close_button)
        self.close_button.controlLeft(self.start_button)
	    # Set initial focus.
        self.setFocus(self.start_button)

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def page(self):
        addon.setSetting(id='pvrconfig', value='true')
        ip_box = self.get_ip_address()
        addon.setSetting(id='ipbox', value=ip_box)
        addon.setSetting(id='kodiconfig', value='true')
        addon.setSetting(id='syncgroup', value='true')
        addon.setSetting(id='syncchannels', value='true')
        addon.setSetting(id='playmax', value='true')
        addon.setSetting(id='video169', value='true')
        addon.setSetting(id='optim', value='true')
        addon.setSetting(id='enableguide', value='true')
        addon.setSetting(id='disableup', value='true')
        addon.setSetting(id='upinterval', value='30')
        import server
        os.system('systemctl stop service.tvheadend42')
        if addon.getSetting('tvhconfig') == 'true':
            server.tvh_config()
        if addon.getSetting('dvbapienable') == 'true':
            server.tvh_dvbapi()
        if addon.getSetting('createusers') == 'true':
            server.tvh_users()
        if addon.getSetting('recording') == 'true':
            server.tvh_recording()
        if addon.getSetting('pvrconfig') == 'true':
            server.tvh_pvr()
        if addon.getSetting('kodiconfig') == 'true':		
            server.kodi_config()
        if addon.getSetting('enableguide') == 'true':
            server.tvh_guide()
        if addon.getSetting('dvbcards') == 'true':
            server.tvh_tunners()
        if addon.getSetting('channelson') == 'true':
            server.tvh_channels()
        os.system('systemctl start service.tvheadend42')
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(5022), 2000, addonicon))
        addon.setSetting(id='tvhstatus', value='Configured')
        addon.setSetting(id='tvh', value='Configured')
        addon.setSetting(id='changeip', value='true')			
        self.close()
        time.sleep(1)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'KODI is restart', 2000, addonicon))
        xbmc.executebuiltin('Reboot')

class Finish(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Finish, self).__init__(title)
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
        image = pyxbmct.Image(addonfolder+artsfolder+'/finish.png')
        self.placeControl(image, 8, 4, rowspan=2, columnspan=8)
		
		# Finish button
        self.start_button = pyxbmct.Button('FINISH')
        self.placeControl(self.start_button, 11, 7, rowspan=1, columnspan=2)
        self.connect(self.start_button, lambda: self.page())

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.start_button.controlRight(self.close_button)
        self.close_button.controlLeft(self.start_button)
	    # Set initial focus.
        self.setFocus(self.start_button)

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def page(self):
        addon.setSetting(id='pvrconfig', value='true')
        ip_box = self.get_ip_address()
        addon.setSetting(id='ipbox', value=ip_box)
        addon.setSetting(id='kodiconfig', value='true')
        addon.setSetting(id='syncgroup', value='true')
        addon.setSetting(id='syncchannels', value='true')
        addon.setSetting(id='playmax', value='true')
        addon.setSetting(id='video169', value='true')
        addon.setSetting(id='optim', value='true')
        addon.setSetting(id='enableguide', value='true')
        addon.setSetting(id='disableup', value='true')
        addon.setSetting(id='upinterval', value='30')
        if addon.getSetting('start') == 'tvhwosc':
            import oscam
            os.system('systemctl stop service.softcam.oscam')
            if addon.getSetting('oscamenable') == 'true':
                oscam.oscam_enable()
            if addon.getSetting ('dvbapioscam') == 'true':
                oscam.dvbapi_enable()
            if addon.getSetting('firstreader') == 'true':
                oscam.oscam_reader('server1', 'first')
            if addon.getSetting('secondreader') == 'true':	
                oscam.oscam_reader('server2', 'second')
            if addon.getSetting('thirdreader') == 'true':
                oscam.oscam_reader('server3', 'third')
            if addon.getSetting('fourthreader') == 'true':
                oscam.oscam_reader('server4', 'fourth')
            if addon.getSetting('fifthreader') == 'true':
                oscam.oscam_reader('server5', 'fifth')
            os.system('systemctl start service.softcam.oscam')
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(5033), 2000, addonicon))
            import server
            os.system('systemctl stop service.tvheadend42')
            if addon.getSetting('tvhconfig') == 'true':
                server.tvh_config()
            if addon.getSetting('dvbapienable') == 'true':
                server.tvh_dvbapi()
            if addon.getSetting('createusers') == 'true':
                server.tvh_users()
            if addon.getSetting('recording') == 'true':
                server.tvh_recording()
            if addon.getSetting('pvrconfig') == 'true':
                server.tvh_pvr()
            if addon.getSetting('kodiconfig') == 'true':		
                server.kodi_config()
            if addon.getSetting('enableguide') == 'true':
                server.tvh_guide()
            if addon.getSetting('dvbcards') == 'true':
                server.tvh_tunners()
            if addon.getSetting('channelson') == 'true':
                server.tvh_channels()
            os.system('systemctl start service.tvheadend42')
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(5022), 2000, addonicon))
            addon.setSetting(id='tvhstatus', value='Configured')
            addon.setSetting(id='tvh', value='Configured')
            addon.setSetting(id='oscam', value='Configured')
            addon.setSetting(id='changeip', value='true')			
        else:
            import server
            os.system('systemctl stop service.tvheadend42')
            if addon.getSetting('tvhconfig') == 'true':
                server.tvh_config()
            if addon.getSetting('dvbapienable') == 'true':
                server.tvh_dvbapi()
            if addon.getSetting('createusers') == 'true':
                server.tvh_users()
            if addon.getSetting('recording') == 'true':
                server.tvh_recording()
            if addon.getSetting('pvrconfig') == 'true':
                server.tvh_pvr()
            if addon.getSetting('kodiconfig') == 'true':		
                server.kodi_config()
            if addon.getSetting('enableguide') == 'true':
                server.tvh_guide()
            if addon.getSetting('dvbcards') == 'true':
                server.tvh_tunners()
            if addon.getSetting('channelson') == 'true':
                server.tvh_channels()
            os.system('systemctl start service.tvheadend42')
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(5022), 2000, addonicon))
            addon.setSetting(id='tvhstatus', value='Configured')
            addon.setSetting(id='tvh', value='Configured')
            addon.setSetting(id='changeip', value='true')			
        self.close()
        time.sleep(1)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'KODI is restart', 2000, addonicon))
        xbmc.executebuiltin('Reboot')

class DVBGeneric(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBGeneric, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/dvb.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)
		
		# DVB-C
        self.dvbc_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbc_button, 10, 1, rowspan=2, columnspan=4)
        self.connect(self.dvbc_button, self.dvbc_button_update)
        if (addon.getSetting('gdvbc') == 'true'):
            self.dvbc_button.setSelected(True)
        else:
            self.dvbc_button.setSelected(False)
        dvbc = pyxbmct.Image(addonfolder+artsfolder+'/dvbc.png')
        self.placeControl(dvbc, 10, 1, rowspan=2, columnspan=4)
        
		# DVB-S
        self.dvbs_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbs_button, 10, 6, rowspan=2, columnspan=4)
        self.connect(self.dvbs_button, self.dvbs_button_update)
        if (addon.getSetting('gdvbs') == 'true'):
            self.dvbs_button.setSelected(True)
        else:
            self.dvbs_button.setSelected(False)
        dvbs = pyxbmct.Image(addonfolder+artsfolder+'/dvbs2.png')
        self.placeControl(dvbs, 10, 6, rowspan=2, columnspan=4)

		# DVB-T
        self.dvbt_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbt_button, 10, 11, rowspan=2, columnspan=4)
        self.connect(self.dvbt_button, self.dvbt_button_update)
        if (addon.getSetting('gdvbt') == 'true'):
            self.dvbt_button.setSelected(True)
        else:
            self.dvbt_button.setSelected(False)
        dvbt = pyxbmct.Image(addonfolder+artsfolder+'/dvbt.png')
        self.placeControl(dvbt, 10, 11, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.dvbc_button)
        self.dvbc_button.controlDown(self.close_button)
        self.dvbc_button.controlRight(self.dvbs_button)
        self.dvbs_button.controlRight(self.dvbt_button)
        self.dvbs_button.controlDown(self.close_button)
        self.dvbt_button.controlLeft(self.dvbs_button)
        self.dvbt_button.controlDown(self.close_button)
        self.dvbs_button.controlLeft(self.dvbc_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def dvbc_button_update(self):
        if self.dvbc_button.isSelected():
            self.close()
            addon.setSetting(id='picons', value='true')
            addon.setSetting(id='gdvbc', value='true')
            DVBC().doModal()
        else:
            addon.setSetting(id='picons', value='false')
            addon.setSetting(id='gdvbc', value='false')

    def dvbs_button_update(self):
        if self.dvbs_button.isSelected():
            self.close()
            addon.setSetting(id='picons', value='true')
            addon.setSetting(id='gdvbs', value='true')
            DVBS().doModal()
        else:
            addon.setSetting(id='picons', value='false')
            addon.setSetting(id='gdvbs', value='false')
             
    def dvbt_button_update(self):
        if self.dvbt_button.isSelected():
            self.close()	
            addon.setSetting(id='picons', value='true')
            addon.setSetting(id='gdvbt', value='true')
            DVBT().doModal()
        else:
            addon.setSetting(id='picons', value='false')
            addon.setSetting(id='gdvbt', value='false')

class DVBKBR(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBKBR, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/kbox.png')
        self.placeControl(image, 0, 0, rowspan=10, columnspan=16)

        # DVBC
        self.kdvbc_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbc_button, 11, 3, rowspan=1, columnspan=3)
        self.connect(self.kdvbc_button, self.kdvbc_button_update)
        if (addon.getSetting('kdvbc') == 'true'):
            self.kdvbc_button.setSelected(True)
        else:
            self.kdvbc_button.setSelected(False)
        lnb1 = pyxbmct.Image(addonfolder+artsfolder+'/dvbc.png')
        self.placeControl(lnb1, 11, 3, rowspan=1, columnspan=3)

        # DVBS2
        self.kdvbs_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbs_button, 11, 10, rowspan=1, columnspan=3)
        self.connect(self.kdvbs_button, self.kdvbs_button_update)
        if (addon.getSetting('kdvbs') == 'true'):
            self.kdvbs_button.setSelected(True)
        else:
            self.kdvbs_button.setSelected(False)
        lnb2 = pyxbmct.Image(addonfolder+artsfolder+'/dvbs2.png')
        self.placeControl(lnb2, 11, 10, rowspan=1, columnspan=3)

        # Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.kdvbc_button)
        self.kdvbc_button.controlRight(self.kdvbs_button)
        self.kdvbs_button.controlLeft(self.kdvbc_button)
        self.kdvbc_button.controlDown(self.close_button)
        self.kdvbs_button.controlDown(self.close_button)

	    # Set initial focus.
        self.setFocus(self.close_button)

    def kdvbc_button_update(self):
        if self.kdvbc_button.isSelected():
            self.close()
            addon.setSetting(id='picons', value='true')
            addon.setSetting(id='kdvbc', value='true')
            DVBCBR().doModal()
        else:
            addon.setSetting(id='picons', value='false')
            addon.setSetting(id='kdvbc', value='false')

    def kdvbs_button_update(self):
        if self.kdvbs_button.isSelected():
            self.close()
            addon.setSetting(id='picons', value='true')
            addon.setSetting(id='kdvbs', value='true')
            DVBSBR().doModal()
        else:
            addon.setSetting(id='picons', value='false')
            addon.setSetting(id='kdvbs', value='false')

class DVBK(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBK, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/kbox.png')
        self.placeControl(image, 0, 0, rowspan=10, columnspan=16)

        # DVBT
        self.kdvbt_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbt_button, 11, 1, rowspan=1, columnspan=3)
        self.connect(self.kdvbt_button, self.kdvbt_button_update)
        if (addon.getSetting('kdvbt') == 'true'):
            self.kdvbt_button.setSelected(True)
        else:
            self.kdvbt_button.setSelected(False)
        lnb1 = pyxbmct.Image(addonfolder+artsfolder+'/dvbt.png')
        self.placeControl(lnb1, 11, 1, rowspan=1, columnspan=3)

        # DVBC
        self.kdvbc_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbc_button, 12, 1, rowspan=1, columnspan=3)
        self.connect(self.kdvbc_button, self.kdvbc_button_update)
        if (addon.getSetting('kdvbc') == 'true'):
            self.kdvbc_button.setSelected(True)
        else:
            self.kdvbc_button.setSelected(False)
        lnb1 = pyxbmct.Image(addonfolder+artsfolder+'/dvbc.png')
        self.placeControl(lnb1, 12, 1, rowspan=1, columnspan=3)

        # DVBS2
        self.kdvbs_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbs_button, 11, 6, rowspan=1, columnspan=3)
        self.connect(self.kdvbs_button, self.kdvbs_button_update)
        if (addon.getSetting('kdvbs') == 'true'):
            self.kdvbs_button.setSelected(True)
        else:
            self.kdvbs_button.setSelected(False)
        lnb2 = pyxbmct.Image(addonfolder+artsfolder+'/dvbs2.png')
        self.placeControl(lnb2, 11, 6, rowspan=1, columnspan=3)

        # DVBT/DVBS2
        self.kdvbts_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbts_button, 11, 11, rowspan=1, columnspan=3)
        self.connect(self.kdvbts_button, self.kdvbts_button_update)
#        if (addon.getSetting('kdvbts') == 'true'):
#            self.kdvbts_button.setSelected(True)
#        else:
#            self.kdvbts_button.setSelected(False)
        both = pyxbmct.Image(addonfolder+artsfolder+'/dvbts2.png')
        self.placeControl(both, 11, 11, rowspan=1, columnspan=3)

        # DVBC/DVBS2
        self.kdvbcs_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbcs_button, 12, 11, rowspan=1, columnspan=3)
        self.connect(self.kdvbcs_button, self.kdvbcs_button_update)
#        if (addon.getSetting('kdvbcs') == 'true'):
#            self.kdvbcs_button.setSelected(True)
#        else:
#            self.kdvbcs_button.setSelected(False)
        both = pyxbmct.Image(addonfolder+artsfolder+'/dvbcs2.png')
        self.placeControl(both, 12, 11, rowspan=1, columnspan=3)

        # Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.kdvbt_button)
        self.close_button.controlLeft(self.kdvbt_button)
        self.kdvbt_button.controlRight(self.kdvbs_button)
        self.kdvbt_button.controlDown(self.kdvbc_button)
        self.kdvbt_button.controlLeft(self.kdvbts_button)
        self.kdvbc_button.controlUp(self.kdvbt_button)
        self.kdvbc_button.controlDown(self.close_button)
        self.kdvbc_button.controlLeft(self.kdvbcs_button)
        self.kdvbc_button.controlRight(self.kdvbcs_button)
        self.kdvbs_button.controlLeft(self.kdvbt_button)
        self.kdvbs_button.controlRight(self.kdvbts_button)
        self.kdvbs_button.controlDown(self.close_button)
        self.kdvbts_button.controlLeft(self.kdvbs_button)
        self.kdvbts_button.controlRight(self.kdvbt_button)
        self.kdvbts_button.controlDown(self.kdvbcs_button)
        self.kdvbcs_button.controlDown(self.close_button)
        self.kdvbcs_button.controlUp(self.kdvbts_button)
        self.kdvbcs_button.controlLeft(self.kdvbc_button)
        self.kdvbcs_button.controlRight(self.kdvbc_button)

	    # Set initial focus.
        self.setFocus(self.close_button)

    def kdvbt_button_update(self):
        if self.kdvbt_button.isSelected():
            self.close()
            addon.setSetting(id='picons', value='true')
            addon.setSetting(id='kdvbt', value='true')
            DVBT().doModal()
        else:
            addon.setSetting(id='picons', value='false')
            addon.setSetting(id='kdvbt', value='false')
			
    def kdvbc_button_update(self):
        if self.kdvbc_button.isSelected():
            self.close()
            addon.setSetting(id='picons', value='true')
            addon.setSetting(id='kdvbc', value='true')
            DVBC().doModal()
        else:
            addon.setSetting(id='picons', value='false')
            addon.setSetting(id='kdvbc', value='false')

    def kdvbs_button_update(self):
        if self.kdvbs_button.isSelected():
            self.close()
            addon.setSetting(id='picons', value='true')
            addon.setSetting(id='kdvbs', value='true')
            DVBS().doModal()
        else:
            addon.setSetting(id='picons', value='false')
            addon.setSetting(id='kdvbs', value='false')

    def kdvbts_button_update(self):
        if self.kdvbts_button.isSelected():
#            self.close()
#            addon.setSetting(id='kdvbts', value='true')
#            DVBTS().doModal()
            xbmcgui.Dialog().ok(addonname, "Comming Soon", "", "")
#        else:
#            addon.setSetting(id='kdvbts', value='false')

    def kdvbcs_button_update(self):
        if self.kdvbcs_button.isSelected():
#            self.close()
#            addon.setSetting(id='kdvbcs', value='true')
#            DVBCS().doModal()
            xbmcgui.Dialog().ok(addonname, "Comming Soon", "", "")
#        else:
#            addon.setSetting(id='kdvbcs', value='false')
			
class WetekPlay(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(WetekPlay, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/wplay.png')
        self.placeControl(image, 0, 0, rowspan=10, columnspan=16)

        # LNB1
        self.wplnb1_button = pyxbmct.RadioButton('')
        self.placeControl(self.wplnb1_button, 11, 1, rowspan=1, columnspan=4)
        self.connect(self.wplnb1_button, self.wplnb1_button_update)
        if (addon.getSetting('wplnb1') == 'true'):
            self.wplnb1_button.setSelected(True)
        else:
            self.wplnb1_button.setSelected(False)
        lnb1 = pyxbmct.Image(addonfolder+artsfolder+'/lnb1.png')
        self.placeControl(lnb1, 11, 1, rowspan=1, columnspan=4)

        # LNB2
        self.wplnb2_button = pyxbmct.RadioButton('')
        self.placeControl(self.wplnb2_button, 11, 6, rowspan=1, columnspan=4)
        self.connect(self.wplnb2_button, self.wplnb2_button_update)
        if (addon.getSetting('wplnb2') == 'true'):
            self.wplnb2_button.setSelected(True)
        else:
            self.wplnb2_button.setSelected(False)
        lnb2 = pyxbmct.Image(addonfolder+artsfolder+'/lnb2.png')
        self.placeControl(lnb2, 11, 6, rowspan=1, columnspan=4)

        # LNB1/LNB2
        self.wplnboth_button = pyxbmct.RadioButton('')
        self.placeControl(self.wplnboth_button, 11, 11, rowspan=1, columnspan=4)
        self.connect(self.wplnboth_button, self.wplnboth_button_update)
        if (addon.getSetting('wplnboth') == 'true'):
            self.wplnboth_button.setSelected(True)
        else:
            self.wplnboth_button.setSelected(False)
        both = pyxbmct.Image(addonfolder+artsfolder+'/both.png')
        self.placeControl(both, 11, 11, rowspan=1, columnspan=4)

        # Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.wplnb1_button)
        self.wplnb1_button.controlRight(self.wplnb2_button)
        self.wplnb2_button.controlRight(self.wplnboth_button)
        self.wplnb1_button.controlDown(self.close_button)
        self.wplnb2_button.controlDown(self.close_button)
        self.wplnboth_button.controlDown(self.close_button)
        self.wplnb1_button.controlLeft(self.wplnboth_button)      
        self.wplnb2_button.controlLeft(self.wplnb1_button)      
        self.wplnboth_button.controlLeft(self.wplnb2_button)
        self.wplnboth_button.controlRight(self.wplnb1_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def wplnb1_button_update(self):
        if self.wplnb1_button.isSelected():
            self.close()
            addon.setSetting(id='wplnb1', value='true')
#            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'Your choice is LNB 1', 2000, addonicon))
            DVBS().doModal()
        else:
            addon.setSetting(id='wplnb1', value='false')

    def wplnb2_button_update(self):
        if self.wplnb2_button.isSelected():
            self.close()
            addon.setSetting(id='wplnb2', value='true')
 #           xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'Your choice is LNB 2', 2000, addonicon))
            DVBS().doModal()
        else:
            addon.setSetting(id='wplnb2', value='false')

    def wplnboth_button_update(self):
        if self.wplnboth_button.isSelected():
            self.close()
            addon.setSetting(id='wplnboth', value='true')
#            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'Your choice is Both', 2000, addonicon))
            DVBS().doModal()
        else:
            addon.setSetting(id='wplnboth', value='false')

class DVBT(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBT, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/mapdvbt.png')
        self.placeControl(image, 0, 0, rowspan=10, columnspan=16)

		# TDT
        self.tdt_button = pyxbmct.RadioButton('')
        self.placeControl(self.tdt_button, 11, 1, rowspan=1, columnspan=4)
        self.connect(self.tdt_button, self.tdt_button_update)
        if (addon.getSetting('tdt') == 'true'):
            self.tdt_button.setSelected(True)
        else:
            self.tdt_button.setSelected(False)
        tdt = pyxbmct.Image(addonfolder+artsfolder+'/tdt.png')
        self.placeControl(tdt, 11, 1, rowspan=1, columnspan=4)
        
		# Meo
        self.meo_button = pyxbmct.RadioButton('')
        self.placeControl(self.meo_button, 11, 6, rowspan=1, columnspan=4)
        self.connect(self.meo_button, self.meo_button_update)
        if (addon.getSetting('meo') == 'true'):
            self.meo_button.setSelected(True)
        else:
            self.meo_button.setSelected(False)
        meo = pyxbmct.Image(addonfolder+artsfolder+'/meo.png')
        self.placeControl(meo, 11, 6, rowspan=1, columnspan=4)

		# Vodafone
        self.vodafone_button = pyxbmct.RadioButton('')
        self.placeControl(self.vodafone_button, 11, 11, rowspan=1, columnspan=4)
        self.connect(self.vodafone_button, self.vodafone_button_update)
        if (addon.getSetting('vodafone') == 'true'):
            self.vodafone_button.setSelected(True)
        else:
            self.vodafone_button.setSelected(False)
        vodafone = pyxbmct.Image(addonfolder+artsfolder+'/vodafone.png')
        self.placeControl(vodafone, 11, 11, rowspan=1, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.tdt_button)
        self.tdt_button.controlDown(self.close_button)
        self.tdt_button.controlRight(self.meo_button)
        self.meo_button.controlRight(self.vodafone_button)
        self.meo_button.controlDown(self.close_button)
        self.vodafone_button.controlLeft(self.meo_button)
        self.vodafone_button.controlDown(self.close_button)
        self.meo_button.controlLeft(self.tdt_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def tdt_button_update(self):
        if self.tdt_button.isSelected():
            self.close()
            addon.setSetting(id='tdt', value='true')
            Finish().doModal()
        else:
            addon.setSetting(id='tdt', value='false')

    def meo_button_update(self):
        if self.meo_button.isSelected():
            self.close()
            addon.setSetting(id='meo', value='true')
            Finish().doModal()
        else:
            addon.setSetting(id='meo', value='false')

    def vodafone_button_update(self):
        if self.vodafone_button.isSelected():
            self.close()
            addon.setSetting(id='vodafone', value='true')
            Finish().doModal()
        else:
            addon.setSetting(id='vodafone', value='false')

class Newcamd(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Newcamd, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=16)

		# Label information
        image = pyxbmct.Image(addonfolder+artsfolder+'/newcamd.png')
        self.placeControl(image, 7, 1, rowspan=1, columnspan=14)
		
		# Hostname input
        image = pyxbmct.Image(addonfolder+artsfolder+'/hostname.png')
        self.placeControl(image, 9, 0, rowspan=1, columnspan=4)
        self.hostname_input = pyxbmct.Edit('')
        self.placeControl(self.hostname_input, 9, 4, rowspan=1, columnspan=4)

		# Port input
        image = pyxbmct.Image(addonfolder+artsfolder+'/port.png')
        self.placeControl(image, 12, 1, rowspan=1, columnspan=3)
        self.port_input = pyxbmct.Edit('')
        self.placeControl(self.port_input, 12, 4, rowspan=1, columnspan=2)

		# Username input
        image = pyxbmct.Image(addonfolder+artsfolder+'/username.png')
        self.placeControl(image, 10, 1, rowspan=1, columnspan=3)
        self.username_input = pyxbmct.Edit('')
        self.placeControl(self.username_input, 10, 4, rowspan=1, columnspan=4)
		
		# Password input
        image = pyxbmct.Image(addonfolder+artsfolder+'/password.png')
        self.placeControl(image, 11, 1, rowspan=1, columnspan=3)
        self.password_input = pyxbmct.Edit('', isPassword=True)
        self.placeControl(self.password_input, 11, 4, rowspan=1, columnspan=4)

		# DES Key
        image = pyxbmct.Image(addonfolder+artsfolder+'/deskey.png')
        self.placeControl(image, 9, 9, rowspan=1, columnspan=3)

		# DESKey1
        self.deskey1_button = pyxbmct.RadioButton('')
        self.placeControl(self.deskey1_button, 10, 9, rowspan=1, columnspan=6)
        self.connect(self.deskey1_button, self.deskey1_button_update)
        if (addon.getSetting('deskey1') == 'true'):
            self.deskey1_button.setSelected(True)
        else:
            self.deskey1_button.setSelected(False)
        deskey1 = pyxbmct.Image(addonfolder+artsfolder+'/deskey1.png')
        self.placeControl(deskey1, 10, 9, rowspan=1, columnspan=6)

		# DESKey2
        self.deskey2_button = pyxbmct.RadioButton('')
        self.placeControl(self.deskey2_button, 11, 9, rowspan=1, columnspan=6)
        self.connect(self.deskey2_button, self.deskey2_button_update)
        if (addon.getSetting('deskey2') == 'true'):
            self.deskey2_button.setSelected(True)
        else:
            self.deskey2_button.setSelected(False)
        deskey2 = pyxbmct.Image(addonfolder+artsfolder+'/deskey2.png')
        self.placeControl(deskey2, 11, 9, rowspan=1, columnspan=6)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)
        
    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlLeft(self.hostname_input)
        self.hostname_input.controlDown(self.username_input)
        self.username_input.controlUp(self.hostname_input)
        self.username_input.controlDown(self.password_input)
        self.password_input.controlUp(self.username_input)
        self.password_input.controlDown(self.port_input)
        self.port_input.controlUp(self.password_input)
        self.port_input.controlDown(self.deskey1_button)
        self.deskey1_button.controlUp(self.port_input)
        self.deskey1_button.controlDown(self.deskey2_button)
        self.deskey2_button.controlUp(self.deskey1_button)
        self.deskey2_button.controlDown(self.close_button)
        # Set initial focus
        self.setFocus(self.close_button)

    def deskey1_button_update(self):
        if self.deskey1_button.isSelected():
            addon.setSetting(id='dvbapienable', value='true')
            addon.setSetting(id='dvbapichoose', value='newcamd')
            addon.setSetting(id='newcamduser', value=self.username_input.getText())
            addon.setSetting(id='newcamdhost', value=self.hostname_input.getText())
            addon.setSetting(id='newcamdport', value=self.port_input.getText())
            addon.setSetting(id='newcamdpass', value=self.password_input.getText())			
            addon.setSetting(id='deskey1', value='true')
            self.close()
            FinishBR().doModal()
        else:
            addon.setSetting(id='deskey1', value='false')

    def deskey2_button_update(self):
        if self.deskey2_button.isSelected():
            addon.setSetting(id='dvbapienable', value='true')
            addon.setSetting(id='dvbapichoose', value='newcamd')
            addon.setSetting(id='newcamduser', value=self.username_input.getText())
            addon.setSetting(id='newcamdhost', value=self.hostname_input.getText())
            addon.setSetting(id='newcamdport', value=self.port_input.getText())
            addon.setSetting(id='newcamdpass', value=self.password_input.getText())			
            addon.setSetting(id='deskey2', value='true')
            self.close()
            FinishBR().doModal()
        else:
            addon.setSetting(id='deskey2', value='false')

class DVBCBR(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBCBR, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/mapdvbc.png')
        self.placeControl(image, 0, 0, rowspan=10, columnspan=16)

		# NET
        self.net_button = pyxbmct.RadioButton('')
        self.placeControl(self.net_button, 11, 6, rowspan=1, columnspan=4)
        self.connect(self.net_button, self.net_button_update)
        if (addon.getSetting('net') == 'true'):
            self.net_button.setSelected(True)
        else:
            self.net_button.setSelected(False)
        net = pyxbmct.Image(addonfolder+artsfolder+'/net.png')
        self.placeControl(net, 11, 6, rowspan=1, columnspan=4)
        
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.net_button)
        self.net_button.controlDown(self.close_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def net_button_update(self):
        if self.net_button.isSelected():
            self.close()
            addon.setSetting(id='net', value='true')
            Newcamd().doModal()
        else:
            addon.setSetting(id='net', value='false')

class DVBSBR(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBSBR, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/mapdvbs.png')
        self.placeControl(image, 0, 0, rowspan=10, columnspan=16)

		# ClaroTV
        self.clarotv_button = pyxbmct.RadioButton('')
        self.placeControl(self.clarotv_button, 11, 6, rowspan=1, columnspan=4)
        self.connect(self.clarotv_button, self.clarotv_button_update)
        if (addon.getSetting('clarotv') == 'true'):
            self.clarotv_button.setSelected(True)
        else:
            self.clarotv_button.setSelected(False)
        clarotv = pyxbmct.Image(addonfolder+artsfolder+'/clarotv.png')
        self.placeControl(clarotv, 11, 6, rowspan=1, columnspan=4)
        
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.clarotv_button)
        self.clarotv_button.controlDown(self.close_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def clarotv_button_update(self):
        if self.clarotv_button.isSelected():
            self.close()
            addon.setSetting(id='clarotv', value='true')
            Newcamd().doModal()
        else:
            addon.setSetting(id='clarotv', value='false')

class DVBS(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBS, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/mapdvbs.png')
        self.placeControl(image, 0, 0, rowspan=10, columnspan=16)

		# Hispasat
        self.hispasat_button = pyxbmct.RadioButton('')
        self.placeControl(self.hispasat_button, 11, 1, rowspan=1, columnspan=4)
        self.connect(self.hispasat_button, self.hispasat_button_update)
        if (addon.getSetting('hispasat') == 'true'):
            self.hispasat_button.setSelected(True)
        else:
            self.hispasat_button.setSelected(False)
        hispasat = pyxbmct.Image(addonfolder+artsfolder+'/hispasat.png')
        self.placeControl(hispasat, 11, 1, rowspan=1, columnspan=4)
        
		# Astra
        self.astra_button = pyxbmct.RadioButton('')
        self.placeControl(self.astra_button, 11, 6, rowspan=1, columnspan=4)
        self.connect(self.astra_button, self.astra_button_update)
#        if (addon.getSetting('astra') == 'true'):
#            self.astra_button.setSelected(True)
#        else:
#            self.astra_button.setSelected(False)
        astra = pyxbmct.Image(addonfolder+artsfolder+'/astra.png')
        self.placeControl(astra, 11, 6, rowspan=1, columnspan=4)

		# Hotbird
        self.hotbird_button = pyxbmct.RadioButton('')
        self.placeControl(self.hotbird_button, 11, 11, rowspan=1, columnspan=4)
        self.connect(self.hotbird_button, self.hotbird_button_update)
#        if (addon.getSetting('hotbird') == 'true'):
#            self.hotbird_button.setSelected(True)
#        else:
#            self.hotbird_button.setSelected(False)
        hotbird = pyxbmct.Image(addonfolder+artsfolder+'/hotbird.png')
        self.placeControl(hotbird, 11, 11, rowspan=1, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.hispasat_button)
        self.hispasat_button.controlDown(self.close_button)
        self.hispasat_button.controlRight(self.astra_button)
        self.astra_button.controlRight(self.hotbird_button)
        self.astra_button.controlDown(self.close_button)
        self.hotbird_button.controlLeft(self.astra_button)
        self.hotbird_button.controlDown(self.close_button)
        self.astra_button.controlLeft(self.hispasat_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def hispasat_button_update(self):
        if self.hispasat_button.isSelected():
            self.close()
            addon.setSetting(id='hispasat', value='true')
            Finish().doModal()
        else:
            addon.setSetting(id='hispasat', value='false')

    def astra_button_update(self):
        if self.astra_button.isSelected():
#            self.close()
#            addon.setSetting(id='astra', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Comming Soon", "", "")
#        else:
#            addon.setSetting(id='astra', value='false')

    def hotbird_button_update(self):
        if self.hotbird_button.isSelected():
#            self.close()
#            addon.setSetting(id='hotbird', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Comming Soon", "", "")
#        else:
#            addon.setSetting(id='hotbird', value='false')

class DVBC(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBC, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/mapdvbc.png')
        self.placeControl(image, 0, 0, rowspan=10, columnspan=16)

		# Nos
        self.nos_button = pyxbmct.RadioButton('')
        self.placeControl(self.nos_button, 11, 3, rowspan=1, columnspan=4)
        self.connect(self.nos_button, self.nos_button_update)
        if (addon.getSetting('nos') == 'true'):
            self.nos_button.setSelected(True)
        else:
            self.nos_button.setSelected(False)
        nos = pyxbmct.Image(addonfolder+artsfolder+'/nos.png')
        self.placeControl(nos, 11, 3, rowspan=1, columnspan=4)
        
		# Nowo
        self.nowo_button = pyxbmct.RadioButton('')
        self.placeControl(self.nowo_button, 11, 9, rowspan=1, columnspan=4)
        self.connect(self.nowo_button, self.nowo_button_update)
        if (addon.getSetting('nowo') == 'true'):
            self.nowo_button.setSelected(True)
        else:
            self.nowo_button.setSelected(False)
        nowo = pyxbmct.Image(addonfolder+artsfolder+'/nowo.png')
        self.placeControl(nowo, 11, 9, rowspan=1, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.nos_button)
        self.nos_button.controlDown(self.close_button)
        self.nos_button.controlRight(self.nowo_button)
        self.nowo_button.controlDown(self.close_button)
        self.nowo_button.controlLeft(self.nos_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def nos_button_update(self):
        if self.nos_button.isSelected():
            self.close()
            addon.setSetting(id='nos', value='true')
            Finish().doModal()
        else:
            addon.setSetting(id='nos', value='false')

    def nowo_button_update(self):
        if self.nowo_button.isSelected():
            self.close()
            addon.setSetting(id='nowo', value='true')
            Finish().doModal()
        else:
            addon.setSetting(id='nowo', value='false')

class DVBCold(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBCold, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/mapdvbc.png')
        self.placeControl(image, 0, 4, rowspan=12, columnspan=8)

        # Porto
        self.porto_button = pyxbmct.RadioButton('Porto / Braga / V. Castelo')
        self.placeControl(self.porto_button, 0, 0, rowspan=2, columnspan=4)
        self.connect(self.porto_button, self.porto_button_update)
#        if (addon.getSetting('porto') == 'true'):
#            self.porto_button.setSelected(True)
#        else:
#            self.porto_button.setSelected(False)

        # Coimbra
        self.coimbra_button = pyxbmct.RadioButton('Coimbra / Aveiro / Viseu')
        self.placeControl(self.coimbra_button, 2, 0, rowspan=2, columnspan=4)
        self.connect(self.coimbra_button, self.coimbra_button_update)
#        if (addon.getSetting('coimbra') == 'true'):
#            self.coimbra_button.setSelected(True)
#        else:
#            self.coimbra_button.setSelected(False)

        # Leiria
        self.leiria_button = pyxbmct.RadioButton('Leiria / T.Novas')
        self.placeControl(self.leiria_button, 4, 0, rowspan=2, columnspan=4)
        self.connect(self.leiria_button, self.leiria_button_update)
#        if (addon.getSetting('leiria') == 'true'):
#            self.leiria_button.setSelected(True)
#        else:
#            self.leiria_button.setSelected(False)

        # Lisboa
        self.lisboa_button = pyxbmct.RadioButton('Grande Lisboa')
        self.placeControl(self.lisboa_button, 6, 0, rowspan=2, columnspan=4)
        self.connect(self.lisboa_button, self.lisboa_button_update)
        if (addon.getSetting('lisboa') == 'true'):
            self.lisboa_button.setSelected(True)
        else:
            self.lisboa_button.setSelected(False)

        # Madeira
        self.madeira_button = pyxbmct.RadioButton('Madeira')
        self.placeControl(self.madeira_button, 8, 0, rowspan=2, columnspan=4)
        self.connect(self.madeira_button, self.madeira_button_update)
#        if (addon.getSetting('madeira') == 'true'):
#            self.madeira_button.setSelected(True)
#        else:
#            self.madeira_button.setSelected(False)

        # Açores
        self.acores_button = pyxbmct.RadioButton('Açores')
        self.placeControl(self.acores_button, 10, 0, rowspan=2, columnspan=4)
        self.connect(self.acores_button, self.acores_button_update)
#        if (addon.getSetting('acores') == 'true'):
#            self.acores_button.setSelected(True)
#        else:
#            self.acores_button.setSelected(False)

        # Mirandela
        self.mirandela_button = pyxbmct.RadioButton('Vila Real / Mirandela')
        self.placeControl(self.mirandela_button, 0, 12, rowspan=2, columnspan=4)
        self.connect(self.mirandela_button, self.mirandela_button_update)
#        if (addon.getSetting('mirandela') == 'true'):
#            self.mirandela_button.setSelected(True)
#        else:
#            self.mirandela_button.setSelected(False)

        # Santarém
        self.santarem_button = pyxbmct.RadioButton('V.F. Xira / Santarém')
        self.placeControl(self.santarem_button, 4, 12, rowspan=2, columnspan=4)
        self.connect(self.santarem_button, self.santarem_button_update)
#        if (addon.getSetting('santarem') == 'true'):
#            self.santarem_button.setSelected(True)
#        else:
#            self.santarem_button.setSelected(False)

        # Sul Tejo
        self.stejo_button = pyxbmct.RadioButton('Sul do Tejo')
        self.placeControl(self.stejo_button, 6, 12, rowspan=2, columnspan=4)
        self.connect(self.stejo_button, self.stejo_button_update)
#        if (addon.getSetting('stejo') == 'true'):
#            self.stejo_button.setSelected(True)
#        else:
#            self.stejo_button.setSelected(False)

        # Évora
        self.evora_button = pyxbmct.RadioButton('Évora')
        self.placeControl(self.evora_button, 8, 12, rowspan=2, columnspan=4)
        self.connect(self.evora_button, self.evora_button_update)
#        if (addon.getSetting('evora') == 'true'):
#            self.evora_button.setSelected(True)
#        else:
#            self.evora_button.setSelected(False)

        # Algarve
        self.algarve_button = pyxbmct.RadioButton('Algarve')
        self.placeControl(self.algarve_button, 10, 12, rowspan=2, columnspan=4)
        self.connect(self.algarve_button, self.algarve_button_update)
#        if (addon.getSetting('algarve') == 'true'):
#            self.algarve_button.setSelected(True)
#        else:
#            self.algarve_button.setSelected(False)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.acores_button)
        self.acores_button.controlUp(self.madeira_button)
        self.acores_button.controlRight(self.algarve_button)
        self.acores_button.controlDown(self.close_button)
        self.algarve_button.controlUp(self.evora_button)
        self.algarve_button.controlLeft(self.acores_button)
        self.algarve_button.controlDown(self.close_button)
        self.madeira_button.controlUp(self.lisboa_button)
        self.madeira_button.controlRight(self.evora_button)
        self.madeira_button.controlDown(self.acores_button)
        self.lisboa_button.controlUp(self.leiria_button)
        self.lisboa_button.controlRight(self.stejo_button)
        self.lisboa_button.controlDown(self.madeira_button)
        self.leiria_button.controlUp(self.coimbra_button)
        self.leiria_button.controlRight(self.santarem_button)
        self.leiria_button.controlDown(self.lisboa_button)
        self.coimbra_button.controlUp(self.porto_button)
        self.coimbra_button.controlDown(self.leiria_button)
        self.porto_button.controlRight(self.mirandela_button)
        self.porto_button.controlDown(self.coimbra_button)
        self.mirandela_button.controlLeft(self.porto_button)
        self.mirandela_button.controlDown(self.santarem_button)
        self.santarem_button.controlUp(self.mirandela_button)
        self.santarem_button.controlLeft(self.leiria_button)
        self.santarem_button.controlDown(self.stejo_button)
        self.stejo_button.controlUp(self.santarem_button)
        self.stejo_button.controlLeft(self.lisboa_button)
        self.stejo_button.controlDown(self.evora_button)
        self.evora_button.controlUp(self.stejo_button)
        self.evora_button.controlLeft(self.madeira_button)
        self.evora_button.controlDown(self.algarve_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def porto_button_update(self):
        if self.porto_button.isSelected():
#            self.close()
#            addon.setSetting(id='porto', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Lista de Canais - Porto / Braga / V. Castelo", "Para adicionar a lista entra em contacto:", "tndsrepo@gmail.com")
#        else:
#            addon.setSetting(id='porto', value='false')

    def coimbra_button_update(self):
        if self.coimbra_button.isSelected():
#            self.close()
#            addon.setSetting(id='coimbra', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Lista de Canais - Coimbra / Aveiro / Viseu", "Para adicionar a lista entra em contacto:", "tndsrepo@gmail.com")
#        else:
#            addon.setSetting(id='coimbra', value='false')

    def leiria_button_update(self):
        if self.leiria_button.isSelected():
#            self.close()
#            addon.setSetting(id='leiria', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Lista de Canais - Leiria / T.Novas", "Para adicionar a lista entra em contacto:", "tndsrepo@gmail.com")
#        else:
#            addon.setSetting(id='leiria', value='false')

    def lisboa_button_update(self):
        if self.lisboa_button.isSelected():
            self.close()
            addon.setSetting(id='lisboa', value='true')
#            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'Lista de Canais - Grande Lisboa', 2000, addonicon))
            Finish().doModal()
        else:
            addon.setSetting(id='lisboa', value='false')

    def madeira_button_update(self):
        if self.madeira_button.isSelected():
#            self.close()
#            addon.setSetting(id='madeira', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Lista de Canais - Madeira", "Para adicionar a lista entra em contacto:", "tndsrepo@gmail.com")
#        else:
#            addon.setSetting(id='madeira', value='false')

    def acores_button_update(self):
        if self.acores_button.isSelected():
#            self.close()
#            addon.setSetting(id='acores', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Lista de Canais - Açores", "Para adicionar a lista entra em contacto:", "tndsrepo@gmail.com")
#        else:
#            addon.setSetting(id='acores', value='false')

    def mirandela_button_update(self):
        if self.mirandela_button.isSelected():
#            self.close()
#            addon.setSetting(id='mirandela', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Lista de Canais - Vila Real / Mirandela", "Para adicionar a lista entra em contacto:", "tndsrepo@gmail.com")
#        else:
#            addon.setSetting(id='mirandela', value='false')

    def santarem_button_update(self):
        if self.santarem_button.isSelected():
#            self.close()
#            addon.setSetting(id='santarem', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Lista de Canais - V.F. Xira / Santarém", "Para adicionar a lista entra em contacto:", "tndsrepo@gmail.com")
#        else:
#            addon.setSetting(id='santarem', value='false')

    def stejo_button_update(self):
        if self.stejo_button.isSelected():
#            self.close()
#            addon.setSetting(id='stejo', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Lista de Canais - Sul do Tejo", "Para adicionar a lista entra em contacto:", "tndsrepo@gmail.com")
#        else:
#            addon.setSetting(id='stejo', value='false')

    def evora_button_update(self):
        if self.evora_button.isSelected():
#            self.close()
#            addon.setSetting(id='evora', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Lista de Canais - Évora", "Para adicionar a lista entra em contacto:", "tndsrepo@gmail.com")
#        else:
#            addon.setSetting(id='evora', value='false')

    def algarve_button_update(self):
        if self.algarve_button.isSelected():
#            self.close()
#            addon.setSetting(id='algarve', value='true')
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Lista de Canais - Algarve", "Para adicionar a lista entra em contacto:", "tndsrepo@gmail.com")
#        else:
#            addon.setSetting(id='algarve', value='false')

class DVBWetek(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBWetek, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/dvb.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)
		
		# DVB-C
        self.dvbc_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbc_button, 10, 1, rowspan=2, columnspan=4)
        self.connect(self.dvbc_button, self.dvbc_button_update)
        if (addon.getSetting('wdvbc') == 'true'):
            self.dvbc_button.setSelected(True)
        else:
            self.dvbc_button.setSelected(False)
        dvbc = pyxbmct.Image(addonfolder+artsfolder+'/dvbc.png')
        self.placeControl(dvbc, 10, 1, rowspan=2, columnspan=4)
        
		# DVB-S
        self.dvbs_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbs_button, 10, 6, rowspan=2, columnspan=4)
        self.connect(self.dvbs_button, self.dvbs_button_update)
        if (addon.getSetting('wdvbs') == 'true'):
            self.dvbs_button.setSelected(True)
        else:
            self.dvbs_button.setSelected(False)
        dvbs = pyxbmct.Image(addonfolder+artsfolder+'/dvbs2.png')
        self.placeControl(dvbs, 10, 6, rowspan=2, columnspan=4)

		# DVB-T
        self.dvbt_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbt_button, 10, 11, rowspan=2, columnspan=4)
        self.connect(self.dvbt_button, self.dvbt_button_update)
        if (addon.getSetting('wdvbt') == 'true'):
            self.dvbt_button.setSelected(True)
        else:
            self.dvbt_button.setSelected(False)
        dvbt = pyxbmct.Image(addonfolder+artsfolder+'/dvbt.png')
        self.placeControl(dvbt, 10, 11, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.dvbc_button)
        self.dvbc_button.controlDown(self.close_button)
        self.dvbc_button.controlRight(self.dvbs_button)
        self.dvbs_button.controlRight(self.dvbt_button)
        self.dvbs_button.controlDown(self.close_button)
        self.dvbt_button.controlLeft(self.dvbs_button)
        self.dvbt_button.controlDown(self.close_button)
        self.dvbs_button.controlLeft(self.dvbc_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def dvbc_button_update(self):
        if self.dvbc_button.isSelected():
            self.close()
            addon.setSetting(id='picons', value='true')
            addon.setSetting(id='wdvbc', value='true')
            DVBC().doModal()
        else:
            addon.setSetting(id='picons', value='false')
            addon.setSetting(id='wdvbc', value='false')

    def dvbs_button_update(self):
        if self.dvbs_button.isSelected():
            self.close()
            addon.setSetting(id='picons', value='true')
            addon.setSetting(id='wdvbs', value='true')
            if addon.getSetting('wetekplay') == 'true':
			    WetekPlay().doModal()
            else:
                DVBS().doModal()
        else:
            addon.setSetting(id='picons', value='false')
            addon.setSetting(id='wdvbs', value='false')
             
    def dvbt_button_update(self):
        if self.dvbt_button.isSelected():
            self.close()
            addon.setSetting(id='picons', value='true')
            addon.setSetting(id='wdvbt', value='true')
            DVBT().doModal()
        else:
            addon.setSetting(id='picons', value='false')
            addon.setSetting(id='wdvbt', value='false')

class Generic(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Generic, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/generic.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# USB
        self.usb_button = pyxbmct.RadioButton('')
        self.placeControl(self.usb_button, 9, 3, rowspan=2, columnspan=4)
        self.connect(self.usb_button, self.usb_button_update)
        if (addon.getSetting('usb') == 'true'):
            self.usb_button.setSelected(True)
        else:
            self.usb_button.setSelected(False)
        usb = pyxbmct.Image(addonfolder+artsfolder+'/usb.png')
        self.placeControl(usb, 9, 3, rowspan=2, columnspan=4)

		# PCI-X
        self.pcix_button = pyxbmct.RadioButton('')
        self.placeControl(self.pcix_button, 9, 9, rowspan=2, columnspan=4)
        self.connect(self.pcix_button, self.pcix_button_update)
        if (addon.getSetting('pcix') == 'true'):
            self.pcix_button.setSelected(True)
        else:
            self.pcix_button.setSelected(False)
        pcix = pyxbmct.Image(addonfolder+artsfolder+'/pcix.png')
        self.placeControl(pcix, 9, 9, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.usb_button)
        self.usb_button.controlDown(self.close_button)
        self.usb_button.controlRight(self.pcix_button)
        self.pcix_button.controlDown(self.close_button)
        self.pcix_button.controlLeft(self.usb_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def usb_button_update(self):
        if self.usb_button.isSelected():
            self.close()
            addon.setSetting(id='usb', value='true')
            DVBGeneric().doModal()
        else:
            addon.setSetting(id='usb', value='false')

    def pcix_button_update(self):
        if self.pcix_button.isSelected():
            self.close()
            addon.setSetting(id='pcix', value='true')
            DVBGeneric().doModal()
        else:
            addon.setSetting(id='pcix', value='false')

class KBR(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(KBR, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/k.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# KI Plus
        self.k1plus_button = pyxbmct.RadioButton('')
        self.placeControl(self.k1plus_button, 8, 1, rowspan=2, columnspan=4)
        self.connect(self.k1plus_button, self.k1plus_button_update)
        if (addon.getSetting('k1plus') == 'true'):
            self.k1plus_button.setSelected(True)
        else:
            self.k1plus_button.setSelected(False)
        k1plus = pyxbmct.Image(addonfolder+artsfolder+'/k1plus.png')
        self.placeControl(k1plus, 8, 1, rowspan=2, columnspan=4)

		# KI Pro
        self.k1pro_button = pyxbmct.RadioButton('')
        self.placeControl(self.k1pro_button, 11, 6, rowspan=2, columnspan=4)
        self.connect(self.k1pro_button, self.k1pro_button_update)
        if (addon.getSetting('k1pro') == 'true'):
            self.k1pro_button.setSelected(True)
        else:
            self.k1pro_button.setSelected(False)
        k1pro = pyxbmct.Image(addonfolder+artsfolder+'/k1pro.png')
        self.placeControl(k1pro, 11, 6, rowspan=2, columnspan=4)

		# KII Pro
        self.k2pro_button = pyxbmct.RadioButton('')
        self.placeControl(self.k2pro_button, 8, 6, rowspan=2, columnspan=4)
        self.connect(self.k2pro_button, self.k2pro_button_update)
        if (addon.getSetting('k2pro') == 'true'):
            self.k2pro_button.setSelected(True)
        else:
            self.k2pro_button.setSelected(False)
        k2pro = pyxbmct.Image(addonfolder+artsfolder+'/k2pro.png')
        self.placeControl(k2pro, 8, 6, rowspan=2, columnspan=4)

		# KIII Pro
        self.k3pro_button = pyxbmct.RadioButton('')
        self.placeControl(self.k3pro_button, 8, 11, rowspan=2, columnspan=4)
        self.connect(self.k3pro_button, self.k3pro_button_update)
        if (addon.getSetting('k3pro') == 'true'):
            self.k3pro_button.setSelected(True)
        else:
            self.k3pro_button.setSelected(False)
        k3pro = pyxbmct.Image(addonfolder+artsfolder+'/k3pro.png')
        self.placeControl(k3pro, 8, 11, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.k1plus_button)
        self.k1plus_button.controlDown(self.k1pro_button)
        self.k1pro_button.controlDown(self.close_button)
        self.k2pro_button.controlDown(self.k1pro_button)
        self.k3pro_button.controlDown(self.k1pro_button)
        self.k1pro_button.controlUp(self.k2pro_button)
        self.k1plus_button.controlRight(self.k2pro_button)
        self.k2pro_button.controlRight(self.k3pro_button)
        self.k3pro_button.controlLeft(self.k2pro_button)
        self.k3pro_button.controlRight(self.k1pro_button)
        self.k2pro_button.controlLeft(self.k1plus_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def k1plus_button_update(self):
        if self.k1plus_button.isSelected():
            self.close()
            import tools
            addon.setSetting(id='dvbcards', value='true')
            addon.setSetting(id='k1plus', value='true')
            tools.set_addon('driver.dvb.crazycat', True)
            DVBKBR().doModal()
        else:
            addon.setSetting(id='k1plus', value='false')

    def k1pro_button_update(self):
        if self.k1pro_button.isSelected():
            self.close()
            import tools
            addon.setSetting(id='dvbcards', value='true')
            addon.setSetting(id='k1pro', value='true')
            tools.set_addon('driver.dvb.crazycat', True)
            DVBKBR().doModal()
        else:
            addon.setSetting(id='k1pro', value='false')

    def k2pro_button_update(self):
        if self.k2pro_button.isSelected():
            self.close()
            import tools
            addon.setSetting(id='dvbcards', value='true')
            addon.setSetting(id='k2pro', value='true')
            tools.set_addon('driver.dvb.crazycat', True)
            DVBKBR().doModal()
        else:
            addon.setSetting(id='k2pro', value='false')

    def k3pro_button_update(self):
        if self.k3pro_button.isSelected():
            self.close()
            import tools
            addon.setSetting(id='dvbcards', value='true')
            addon.setSetting(id='k3pro', value='true')
            tools.set_addon('driver.dvb.crazycat', True)
            DVBKBR().doModal()
        else:
            addon.setSetting(id='k3pro', value='false')

class K(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(K, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/k.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# KI Plus
        self.k1plus_button = pyxbmct.RadioButton('')
        self.placeControl(self.k1plus_button, 8, 1, rowspan=2, columnspan=4)
        self.connect(self.k1plus_button, self.k1plus_button_update)
        if (addon.getSetting('k1plus') == 'true'):
            self.k1plus_button.setSelected(True)
        else:
            self.k1plus_button.setSelected(False)
        k1plus = pyxbmct.Image(addonfolder+artsfolder+'/k1plus.png')
        self.placeControl(k1plus, 8, 1, rowspan=2, columnspan=4)

		# KI Pro
        self.k1pro_button = pyxbmct.RadioButton('')
        self.placeControl(self.k1pro_button, 11, 6, rowspan=2, columnspan=4)
        self.connect(self.k1pro_button, self.k1pro_button_update)
        if (addon.getSetting('k1pro') == 'true'):
            self.k1pro_button.setSelected(True)
        else:
            self.k1pro_button.setSelected(False)
        k1pro = pyxbmct.Image(addonfolder+artsfolder+'/k1pro.png')
        self.placeControl(k1pro, 11, 6, rowspan=2, columnspan=4)

		# KII Pro
        self.k2pro_button = pyxbmct.RadioButton('')
        self.placeControl(self.k2pro_button, 8, 6, rowspan=2, columnspan=4)
        self.connect(self.k2pro_button, self.k2pro_button_update)
        if (addon.getSetting('k2pro') == 'true'):
            self.k2pro_button.setSelected(True)
        else:
            self.k2pro_button.setSelected(False)
        k2pro = pyxbmct.Image(addonfolder+artsfolder+'/k2pro.png')
        self.placeControl(k2pro, 8, 6, rowspan=2, columnspan=4)

		# KIII Pro
        self.k3pro_button = pyxbmct.RadioButton('')
        self.placeControl(self.k3pro_button, 8, 11, rowspan=2, columnspan=4)
        self.connect(self.k3pro_button, self.k3pro_button_update)
        if (addon.getSetting('k3pro') == 'true'):
            self.k3pro_button.setSelected(True)
        else:
            self.k3pro_button.setSelected(False)
        k3pro = pyxbmct.Image(addonfolder+artsfolder+'/k3pro.png')
        self.placeControl(k3pro, 8, 11, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.k1plus_button)
        self.k1plus_button.controlDown(self.k1pro_button)
        self.k1pro_button.controlDown(self.close_button)
        self.k2pro_button.controlDown(self.k1pro_button)
        self.k3pro_button.controlDown(self.k1pro_button)
        self.k1pro_button.controlUp(self.k2pro_button)
        self.k1plus_button.controlRight(self.k2pro_button)
        self.k2pro_button.controlRight(self.k3pro_button)
        self.k3pro_button.controlLeft(self.k2pro_button)
        self.k3pro_button.controlRight(self.k1pro_button)
        self.k2pro_button.controlLeft(self.k1plus_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def k1plus_button_update(self):
        if self.k1plus_button.isSelected():
            self.close()
            addon.setSetting(id='k1plus', value='true')
            DVBK().doModal()
        else:
            addon.setSetting(id='k1plus', value='false')

    def k1pro_button_update(self):
        if self.k1pro_button.isSelected():
            self.close()
            addon.setSetting(id='k1pro', value='true')
            DVBK().doModal()
        else:
            addon.setSetting(id='k1pro', value='false')

    def k2pro_button_update(self):
        if self.k2pro_button.isSelected():
            self.close()
            addon.setSetting(id='k2pro', value='true')
            DVBK().doModal()
        else:
            addon.setSetting(id='k2pro', value='false')

    def k3pro_button_update(self):
        if self.k3pro_button.isSelected():
            self.close()
            addon.setSetting(id='k3pro', value='true')
            DVBK().doModal()
        else:
            addon.setSetting(id='k3pro', value='false')

class Wetek(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Wetek, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/wetek.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# WetekPlay
        self.wp_button = pyxbmct.RadioButton('')
        self.placeControl(self.wp_button, 10, 1, rowspan=2, columnspan=4)
        self.connect(self.wp_button, self.wp_button_update)
        if (addon.getSetting('wetekplay') == 'true'):
            self.wp_button.setSelected(True)
        else:
            self.wp_button.setSelected(False)
        wp = pyxbmct.Image(addonfolder+artsfolder+'/wp.png')
        self.placeControl(wp, 10, 1, rowspan=2, columnspan=4)

		# WetekPlay2
        self.wp2_button = pyxbmct.RadioButton('')
        self.placeControl(self.wp2_button, 10, 6, rowspan=2, columnspan=4)
        self.connect(self.wp2_button, self.wp2_button_update)
        if (addon.getSetting('wetekplay2') == 'true'):
            self.wp2_button.setSelected(True)
        else:
            self.wp2_button.setSelected(False)
        wp2 = pyxbmct.Image(addonfolder+artsfolder+'/wp2.png')
        self.placeControl(wp2, 10, 6, rowspan=2, columnspan=4)

		# WetekPlay2S
        self.wp2s_button = pyxbmct.RadioButton('')
        self.placeControl(self.wp2s_button, 10, 11, rowspan=2, columnspan=4)
        self.connect(self.wp2s_button, self.wp2s_button_update)
#        if (addon.getSetting('wetekplay2s') == 'true'):
#            self.wp2s_button.setSelected(True)
#        else:
#            self.wp2s_button.setSelected(False)
        wp2s = pyxbmct.Image(addonfolder+artsfolder+'/wp2s.png')
        self.placeControl(wp2s, 10, 11, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.wp_button)
        self.wp_button.controlDown(self.close_button)
        self.wp_button.controlRight(self.wp2_button)
        self.wp2_button.controlRight(self.wp2s_button)
        self.wp2_button.controlDown(self.close_button)
        self.wp2s_button.controlLeft(self.wp2_button)
        self.wp2s_button.controlDown(self.close_button)
        self.wp2_button.controlLeft(self.wp_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def wp_button_update(self):
        if self.wp_button.isSelected():
            self.close()
            addon.setSetting(id='wetekplay', value='true')
            DVBWetek().doModal()
        else:
            addon.setSetting(id='wetekplay', value='false')

    def wp2_button_update(self):
        if self.wp2_button.isSelected():
            self.close()
            addon.setSetting(id='wetekplay2', value='true')
            DVBWetek().doModal()
        else:
            addon.setSetting(id='wetekplay2', value='false')

    def wp2s_button_update(self):
        if self.wp2s_button.isSelected():
#            addon.setSetting(id='wetekplay2s', value='true')
#            DVBWetek().doModal()
            xbmcgui.Dialog().ok(addonname, "Comming Soon", "", "")
#        else:
#            addon.setSetting(id='wetekplay2s', value='false')

class Inputs(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Inputs, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# Wetek Button
        self.wetek_button = pyxbmct.RadioButton('')
        self.placeControl(self.wetek_button, 9, 1, rowspan=3, columnspan=3)
        self.connect(self.wetek_button, self.wetek_button_update)
        if (addon.getSetting('wetek') == 'true'):
            self.wetek_button.setSelected(True)
        else:
            self.wetek_button.setSelected(False)
        wetek = pyxbmct.Image(addonfolder+artsfolder+'/weteksmall.png')
        self.placeControl(wetek, 9, 1, rowspan=3, columnspan=3)

		# K Button
        self.k_button = pyxbmct.RadioButton('')
        self.placeControl(self.k_button, 9, 6, rowspan=3, columnspan=3)
        self.connect(self.k_button, self.k_button_update)
        if (addon.getSetting('k') == 'true'):
            self.k_button.setSelected(True)
        else:
            self.k_button.setSelected(False)
        k = pyxbmct.Image(addonfolder+artsfolder+'/ksmall.png')
        self.placeControl(k, 9, 6, rowspan=3, columnspan=3)

		# Generic Button
        self.generic_button = pyxbmct.RadioButton('')
        self.placeControl(self.generic_button, 9, 11, rowspan=3, columnspan=3)
        self.connect(self.generic_button, self.generic_button_update)
        if (addon.getSetting('generic') == 'true'):
            self.generic_button.setSelected(True)
        else:
            self.generic_button.setSelected(False)
        generic = pyxbmct.Image(addonfolder+artsfolder+'/genericsmall.png')
        self.placeControl(generic, 9, 11, rowspan=3, columnspan=3)
		
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.wetek_button)
        self.wetek_button.controlDown(self.close_button)
        self.wetek_button.controlRight(self.k_button)
        self.k_button.controlRight(self.generic_button)
        self.k_button.controlDown(self.close_button)
        self.generic_button.controlLeft(self.k_button)
        self.generic_button.controlDown(self.close_button)
        self.k_button.controlLeft(self.wetek_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def wetek_button_update(self):
        if self.wetek_button.isSelected():
            self.close()
            addon.setSetting(id='dvbcards', value='true')
            addon.setSetting(id='wetek', value='true')
            Wetek().doModal()
        else:
            addon.setSetting(id='dvbcards', value='false')
            addon.setSetting(id='wetek', value='false')

    def k_button_update(self):
        if self.k_button.isSelected():
            self.close()
            import tools
            addon.setSetting(id='dvbcards', value='true')			
            addon.setSetting(id='k', value='true')
            tools.set_addon('driver.dvb.crazycat', True)
            K().doModal()
        else:
            addon.setSetting(id='dvbcards', value='false')
            addon.setSetting(id='k', value='false')

    def generic_button_update(self):
        if self.generic_button.isSelected():
            self.close()
            addon.setSetting(id='dvbcards', value='true')
            addon.setSetting(id='generic', value='true')
            Generic().doModal()
        else:
            addon.setSetting(id='dvbcards', value='false')
            addon.setSetting(id='generic', value='false')

class ReaderCccam(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(ReaderCccam, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/osc.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=16)

		# Label information
        image = pyxbmct.Image(addonfolder+artsfolder+'/readers.png')
        self.placeControl(image, 7, 1, rowspan=1, columnspan=14)
		
		# Hostname input
        image = pyxbmct.Image(addonfolder+artsfolder+'/hostname.png')
        self.placeControl(image, 9, 0, rowspan=1, columnspan=4)
        self.hostname_input = pyxbmct.Edit('')
        self.placeControl(self.hostname_input, 9, 4, rowspan=1, columnspan=5)

		# Port input
        image = pyxbmct.Image(addonfolder+artsfolder+'/port.png')
        self.placeControl(image, 12, 1, rowspan=1, columnspan=3)
        self.port_input = pyxbmct.Edit('')
        self.placeControl(self.port_input, 12, 4, rowspan=1, columnspan=2)

		# Username input
        image = pyxbmct.Image(addonfolder+artsfolder+'/username.png')
        self.placeControl(image, 10, 1, rowspan=1, columnspan=3)
        self.username_input = pyxbmct.Edit('')
        self.placeControl(self.username_input, 10, 4, rowspan=1, columnspan=4)
		
		# Password input
        image = pyxbmct.Image(addonfolder+artsfolder+'/password.png')
        self.placeControl(image, 11, 1, rowspan=1, columnspan=3)
        self.password_input = pyxbmct.Edit('', isPassword=True)
        self.placeControl(self.password_input, 11, 4, rowspan=1, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.page(Readers))
        
    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlLeft(self.hostname_input)
        self.hostname_input.controlDown(self.username_input)
        self.username_input.controlUp(self.hostname_input)
        self.username_input.controlDown(self.password_input)
        self.password_input.controlUp(self.username_input)
        self.password_input.controlDown(self.port_input)
        self.port_input.controlUp(self.password_input)
        self.port_input.controlDown(self.close_button)
        # Set initial focus
        self.setFocus(self.close_button)

    def page(self, page):
        if addon.getSetting('reader') == 'first':
            addon.setSetting(id='firstreader', value='true')
            addon.setSetting(id='protocolfirstreader', value='cccam')
            addon.setSetting(id='namefirstreader', value=self.username_input.getText())
            addon.setSetting(id='ipfirstreader', value=self.hostname_input.getText())
            addon.setSetting(id='portfirstreader', value=self.port_input.getText())
            addon.setSetting(id='userfirstreader', value=self.username_input.getText())
            addon.setSetting(id='passfirstreader', value=self.password_input.getText())
        elif addon.getSetting('reader') == 'second':
            addon.setSetting(id='secondreader', value='true')
            addon.setSetting(id='protocolsecondreader', value='cccam')
            addon.setSetting(id='namesecondreader', value=self.username_input.getText())
            addon.setSetting(id='ipsecondreader', value=self.hostname_input.getText())
            addon.setSetting(id='portsecondreader', value=self.port_input.getText())
            addon.setSetting(id='usersecondreader', value=self.username_input.getText())
            addon.setSetting(id='passsecondreader', value=self.password_input.getText())
        elif addon.getSetting('reader') == 'third':
            addon.setSetting(id='thirdreader', value='true')
            addon.setSetting(id='protocolthirdreader', value='cccam')
            addon.setSetting(id='namethirdreader', value=self.username_input.getText())
            addon.setSetting(id='ipthirdreader', value=self.hostname_input.getText())
            addon.setSetting(id='portthirdreader', value=self.port_input.getText())
            addon.setSetting(id='userthirdreader', value=self.username_input.getText())
            addon.setSetting(id='passthirdreader', value=self.password_input.getText())
        elif addon.getSetting('reader') == 'fourth':
            addon.setSetting(id='fourthreader', value='true')
            addon.setSetting(id='protocolfourthreader', value='cccam')
            addon.setSetting(id='namefourthreader', value=self.username_input.getText())
            addon.setSetting(id='ipfourthreader', value=self.hostname_input.getText())
            addon.setSetting(id='portfourthreader', value=self.port_input.getText())
            addon.setSetting(id='userfourthreader', value=self.username_input.getText())
            addon.setSetting(id='passfourthreader', value=self.password_input.getText())
        elif addon.getSetting('reader') == 'fifth':
            addon.setSetting(id='fifthreader', value='true')
            addon.setSetting(id='protocolfifthreader', value='cccam')
            addon.setSetting(id='namefifthreader', value=self.username_input.getText())
            addon.setSetting(id='ipfifthreader', value=self.hostname_input.getText())
            addon.setSetting(id='portfifthreader', value=self.port_input.getText())
            addon.setSetting(id='userfifthreader', value=self.username_input.getText())
            addon.setSetting(id='passfifthreader', value=self.password_input.getText())
        self.close()
        page().doModal()

class Readers(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        
        """Class constructor"""
        super(Readers, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/osc.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# Label information
        image = pyxbmct.Image(addonfolder+artsfolder+'/readers.png')
        self.placeControl(image, 8, 1, rowspan=1, columnspan=14)

		# Reader 1
        if addon.getSetting('firstreader') == 'true':
            color1 = '0xFF00FF00'
        else:
            color1 = '0xFFFF0000'
        self.reader1_button = pyxbmct.Button('READER 1', textColor=color1)
        self.placeControl(self.reader1_button, 10, 1, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.reader1_button, lambda: self.reader(ReaderCccam, 'first'))
		
		# Reader 2
        if addon.getSetting('secondreader') == 'true':
            color2 = '0xFF00FF00'
        else:
            color2 = '0xFFFF0000'
        self.reader2_button = pyxbmct.Button('READER 2', textColor=color2)
        self.placeControl(self.reader2_button, 10, 4, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.reader2_button, lambda: self.reader(ReaderCccam, 'second'))

		# Reader 3
        if addon.getSetting('thirdreader') == 'true':
            color3 = '0xFF00FF00'
        else:
            color3 = '0xFFFF0000'
        self.reader3_button = pyxbmct.Button('READER 3', textColor=color3)
        self.placeControl(self.reader3_button, 10, 7, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.reader3_button, lambda: self.reader(ReaderCccam, 'third'))

		# Reader 4
        if addon.getSetting('fourthreader') == 'true':
            color4 = '0xFF00FF00'
        else:
            color4 = '0xFFFF0000'
        self.reader4_button = pyxbmct.Button('READER 4', textColor=color4)
        self.placeControl(self.reader4_button, 10, 10, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.reader4_button, lambda: self.reader(ReaderCccam, 'fourth'))

		# Reader 5
        if addon.getSetting('fifthreader') == 'true':
            color5 = '0xFF00FF00'
        else:
            color5 = '0xFFFF0000'
        self.reader5_button = pyxbmct.Button('READER 5', textColor=color5)
        self.placeControl(self.reader5_button, 10, 13, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.reader5_button, lambda: self.reader(ReaderCccam, 'fifth'))
		
		# Next button
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 13, 14, rowspan=1, columnspan=1)
        self.connect(self.next_button, lambda: self.page(Tvheadend))
		
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.reader1_button)
        self.close_button.controlLeft(self.next_button)
        self.reader1_button.controlRight(self.reader2_button)
        self.reader2_button.controlRight(self.reader3_button)
        self.reader3_button.controlRight(self.reader4_button)
        self.reader4_button.controlRight(self.reader5_button)
        self.reader1_button.controlDown(self.next_button)
        self.reader2_button.controlDown(self.next_button)
        self.reader3_button.controlDown(self.next_button)
        self.reader4_button.controlDown(self.next_button)
        self.reader5_button.controlDown(self.next_button)
        self.next_button.controlUp(self.reader5_button)
        self.next_button.controlRight(self.close_button)
        self.reader5_button.controlLeft(self.reader4_button)
        self.reader4_button.controlLeft(self.reader3_button)
        self.reader3_button.controlLeft(self.reader2_button)
        self.reader2_button.controlLeft(self.reader1_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def reader(self, page, reader):
        addon.setSetting(id='reader', value=reader)
        self.close()
        page().doModal()

    def page(self, page):
        self.close()
        page().doModal()

class UsersOscam(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(UsersOscam, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/osc.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# Label information
        image = pyxbmct.Image(addonfolder+artsfolder+'/users.png')
        self.placeControl(image, 8, 1, rowspan=1, columnspan=14)
		
		# Username input
        image = pyxbmct.Image(addonfolder+artsfolder+'/username.png')
        self.placeControl(image, 10, 1, rowspan=1, columnspan=3)
        self.username_input = pyxbmct.Edit('')
        self.placeControl(self.username_input, 10, 4, rowspan=1, columnspan=4)
        self.username_input.setText('oscam')
		
		# Password input
        image = pyxbmct.Image(addonfolder+artsfolder+'/password.png')
        self.placeControl(image, 11, 1, rowspan=1, columnspan=3)
        self.password_input = pyxbmct.Edit('', isPassword=True)
        self.placeControl(self.password_input, 11, 4, rowspan=1, columnspan=4)
        self.password_input.setText('oscam')
		
		# Port input
        image = pyxbmct.Image(addonfolder+artsfolder+'/port.png')
        self.placeControl(image, 12, 1, rowspan=1, columnspan=3)
        self.port_input = pyxbmct.Edit('')
        self.placeControl(self.port_input, 12, 4, rowspan=1, columnspan=4)
        self.port_input.setText('8888')
		
		# Next button
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 13, 14, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.next_button, lambda: self.page())
		
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.username_input)
        self.close_button.controlLeft(self.username_input)
        self.username_input.controlDown(self.password_input)
        self.password_input.controlUp(self.username_input)
        self.password_input.controlDown(self.port_input)
        self.port_input.controlUp(self.password_input)
        self.port_input.controlRight(self.next_button)
        self.port_input.controlDown(self.next_button)
        self.next_button.controlUp(self.port_input)
        self.password_input.controlRight(self.next_button)
        self.next_button.controlRight(self.close_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def page(self):
        addon.setSetting(id='useroscam', value=self.username_input.getText())
        addon.setSetting(id='passoscam', value=self.password_input.getText())
        addon.setSetting(id='portoscam', value=self.port_input.getText())
        addon.setSetting(id='dvbapioscam', value='true')
        addon.setSetting(id='portdvbapipc', value='9002')		
        addon.setSetting(id='boxtype', value='pc')
        self.close()
        Readers().doModal()

class RecordingBR(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(RecordingBR, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# Label information
        image = pyxbmct.Image(addonfolder+artsfolder+'/recording.png')
        self.placeControl(image, 8, 1, rowspan=1, columnspan=14)
		
		# Browse information
        self.browse_label = pyxbmct.Edit('')
        self.placeControl(self.browse_label, 11, 2, rowspan=1, columnspan=6)
        if addon.getSetting('pathrecording') == '':
            self.browse_label.setText('')
        else:
            path = addon.getSetting('pathrecording')
            self.browse_label.setText(path)
			
		# Browse input
        self.browse_button = pyxbmct.Button('Browse')
        self.placeControl(self.browse_button, 11, 6, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.browse_button, lambda: self.browse())

		# Next button
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 13, 14, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.next_button, lambda: self.page())
		
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.browse_button)
        self.browse_button.controlDown(self.next_button)
        self.browse_button.controlRight(self.next_button)
        self.next_button.controlRight(self.close_button)
        self.next_button.controlLeft(self.browse_button)
        self.close_button.controlLeft(self.next_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def browse(self):
        browsepath = xbmcgui.Dialog().browse(3, 'Recording path', 'files', '', False, False, '/storage')
        addon.setSetting(id='pathrecording', value=browsepath)
        self.close()
        RecordingBR().doModal()

    def page(self):
        if addon.getSetting('pathrecording') == '':
            self.close()
            KBR().doModal()
        else:
            addon.setSetting(id='recording', value='true')
            addon.setSetting(id='recordprofile', value='0')
            self.close()
            KBR().doModal()

class Recording(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Recording, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# Label information
        image = pyxbmct.Image(addonfolder+artsfolder+'/recording.png')
        self.placeControl(image, 8, 1, rowspan=1, columnspan=14)
		
		# Browse information
        self.browse_label = pyxbmct.Edit('')
        self.placeControl(self.browse_label, 11, 2, rowspan=1, columnspan=6)
        if addon.getSetting('pathrecording') == '':
            self.browse_label.setText('')
        else:
            path = addon.getSetting('pathrecording')
            self.browse_label.setText(path)
			
		# Browse input
        self.browse_button = pyxbmct.Button('Browse')
        self.placeControl(self.browse_button, 11, 6, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.browse_button, lambda: self.browse())

		# Next button
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 13, 14, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.next_button, lambda: self.page())
		
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.browse_button)
        self.browse_button.controlDown(self.next_button)
        self.browse_button.controlRight(self.next_button)
        self.next_button.controlRight(self.close_button)
        self.next_button.controlLeft(self.browse_button)
        self.close_button.controlLeft(self.next_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def browse(self):
        browsepath = xbmcgui.Dialog().browse(3, 'Recording path', 'files', '', False, False, '/storage')
        addon.setSetting(id='pathrecording', value=browsepath)
        self.close()
        Recording().doModal()

    def page(self):
        if addon.getSetting('pathrecording') == '':
            self.close()
            Inputs().doModal()
        else:
            addon.setSetting(id='recording', value='true')
            addon.setSetting(id='recordprofile', value='0')
            self.close()
            Inputs().doModal()

class UsersBR(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(UsersBR, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# Label information
        image = pyxbmct.Image(addonfolder+artsfolder+'/users.png')
        self.placeControl(image, 8, 1, rowspan=1, columnspan=14)
		
		# Username input
        image = pyxbmct.Image(addonfolder+artsfolder+'/username.png')
        self.placeControl(image, 10, 1, rowspan=1, columnspan=3)
        self.username_input = pyxbmct.Edit('')
        self.placeControl(self.username_input, 10, 4, rowspan=1, columnspan=4)

		# Password input
        image = pyxbmct.Image(addonfolder+artsfolder+'/password.png')
        self.placeControl(image, 11, 1, rowspan=1, columnspan=3)
        self.password_input = pyxbmct.Edit('', isPassword=True)
        self.placeControl(self.password_input, 11, 4, rowspan=1, columnspan=4)

		# Next button
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 13, 14, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.next_button, lambda: self.page())
		
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.username_input)
        self.close_button.controlLeft(self.next_button)
        self.next_button.controlLeft(self.username_input)
        self.username_input.controlDown(self.password_input)
        self.password_input.controlUp(self.username_input)
        self.password_input.controlRight(self.next_button)
        self.next_button.controlRight(self.close_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def page(self):
        if self.username_input.getText() == '' :
            self.close()
            RecordingBR().doModal()
        else:
            addon.setSetting(id='createusers', value='true')
            addon.setSetting(id='logadmin', value='true')
            addon.setSetting(id='useradmin', value=self.username_input.getText())
            addon.setSetting(id='passadmin', value=self.password_input.getText())
            addon.setSetting(id='logclient', value='true')
            addon.setSetting(id='userclient', value='tvh')
            addon.setSetting(id='passclient', value='tvh')
            addon.setSetting(id='recordingpath', value='')
            self.close()
            RecordingBR().doModal()
		
class Users(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Users, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)

		# Label information
        image = pyxbmct.Image(addonfolder+artsfolder+'/users.png')
        self.placeControl(image, 8, 1, rowspan=1, columnspan=14)
		
		# Username input
        image = pyxbmct.Image(addonfolder+artsfolder+'/username.png')
        self.placeControl(image, 10, 1, rowspan=1, columnspan=3)
        self.username_input = pyxbmct.Edit('')
        self.placeControl(self.username_input, 10, 4, rowspan=1, columnspan=4)

		# Password input
        image = pyxbmct.Image(addonfolder+artsfolder+'/password.png')
        self.placeControl(image, 11, 1, rowspan=1, columnspan=3)
        self.password_input = pyxbmct.Edit('', isPassword=True)
        self.placeControl(self.password_input, 11, 4, rowspan=1, columnspan=4)

		# Next button
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 13, 14, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.next_button, lambda: self.page())
		
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.username_input)
        self.close_button.controlLeft(self.next_button)
        self.next_button.controlLeft(self.username_input)
        self.username_input.controlDown(self.password_input)
        self.password_input.controlUp(self.username_input)
        self.password_input.controlRight(self.next_button)
        self.next_button.controlRight(self.close_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def page(self):
        if self.username_input.getText() == '' :
            self.close()
            Recording().doModal()
        else:
            addon.setSetting(id='createusers', value='true')
            addon.setSetting(id='logadmin', value='true')
            addon.setSetting(id='useradmin', value=self.username_input.getText())
            addon.setSetting(id='passadmin', value=self.password_input.getText())
            addon.setSetting(id='logclient', value='true')
            addon.setSetting(id='userclient', value='tvh')
            addon.setSetting(id='passclient', value='tvh')
            addon.setSetting(id='recordingpath', value='')
            self.close()
            Recording().doModal()

class OSCam(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(OSCam, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/osc.png')
        self.placeControl(image, 0, 0, rowspan=9, columnspan=16)

        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/installaddons.png')
        self.placeControl(image, 8, 6, rowspan=4, columnspan=4)

		# OSCam button
        self.osc_button = pyxbmct.Button('OSCAM')
        self.placeControl(self.osc_button, 10, 2, rowspan=1, columnspan=3)
        self.connect(self.osc_button, lambda: self.installaddons('service.softcam.oscam'))

		# Start button
        self.start_button = pyxbmct.Button('START')
        self.placeControl(self.start_button, 12, 7, rowspan=1, columnspan=2)
        self.connect(self.start_button, lambda: self.page('service.softcam.oscam'))

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.start_button.controlUp(self.osc_button)
        self.start_button.controlLeft(self.osc_button)
        self.osc_button.controlDown(self.start_button)
        self.osc_button.controlRight(self.start_button)
        self.start_button.controlDown(self.close_button)
        self.close_button.controlLeft(self.start_button)
	    # Set initial focus.
        self.setFocus(self.start_button)

    def installaddons(self, id):
        if os.path.exists(xbmc.translatePath('special://home/addons/') + id):
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'Addon was alredy installed', 2000, addonicon))
        else:
            xbmc.executebuiltin('InstallAddon(%s)'%(id))

    def page(self, id1):
        if not os.path.exists(xbmc.translatePath('special://home/addons/') + id1):
            xbmc.executebuiltin(xbmcgui.Dialog().ok("OSCam Config", "The addons are not installed. Please install them to continue"))
        else:
            self.close()
            addon.setSetting(id='oscamenable', value='true')
            UsersOscam().doModal()

class TvheadendBR(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(TvheadendBR, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh.png')
        self.placeControl(image, 0, 0, rowspan=9, columnspan=16)

        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/installaddons.png')
        self.placeControl(image, 8, 6, rowspan=4, columnspan=4)

		# Tvheadend button
        self.tvh_button = pyxbmct.Button('TVHEADEND')
        self.placeControl(self.tvh_button, 10, 11, rowspan=1, columnspan=3)
        self.connect(self.tvh_button, lambda: self.installaddons('service.tvheadend42'))

		# Tvheadend HTSP Client button
        self.htsp_button = pyxbmct.Button('HTSP CLIENT')
        self.placeControl(self.htsp_button, 10, 2, rowspan=1, columnspan=3)
        self.connect(self.htsp_button, lambda: self.installaddons('pvr.hts'))

		# Start button
        self.start_button = pyxbmct.Button('START')
        self.placeControl(self.start_button, 12, 7, rowspan=1, columnspan=2)
        self.connect(self.start_button, lambda: self.page('service.tvheadend42', 'pvr.hts'))

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.start_button.controlRight(self.close_button)
        self.start_button.controlLeft(self.htsp_button)
        self.start_button.controlUp(self.htsp_button)
        self.htsp_button.controlRight(self.tvh_button)
        self.tvh_button.controlLeft(self.htsp_button)
        self.htsp_button.controlDown(self.start_button)
        self.tvh_button.controlDown(self.start_button)
        self.close_button.controlLeft(self.start_button)
	    # Set initial focus.
        self.setFocus(self.start_button)

    def installaddons(self, id):
        if os.path.exists(xbmc.translatePath('special://home/addons/') + id):
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'Addon was alredy installed', 2000, addonicon))
        else:
            xbmc.executebuiltin('InstallAddon(%s)'%(id))
    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def page(self, id1, id2):
        if not os.path.exists(xbmc.translatePath('special://home/addons/') + id1):
            xbmc.executebuiltin(xbmcgui.Dialog().ok("Tvheadend Config", "The addons are not installed. Please install them to continue"))
        elif not os.path.exists(xbmc.translatePath('special://home/addons/') + id2):
            xbmc.executebuiltin(xbmcgui.Dialog().ok("Tvheadend Config", "The addons are not installed. Please install them to continue"))
        else:
            addon.setSetting(id='tvhconfig', value='true')
            addon.setSetting(id='tvhexpert', value='true')
            addon.setSetting(id='languien', value='true')
            addon.setSetting(id='langepg', value='true')
            addon.setSetting(id='langepgen', value='true')
            addon.setSetting(id='langepgpt', value='true')
            self.close()
            UsersBR().doModal()

class Tvheadend(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Tvheadend, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh.png')
        self.placeControl(image, 0, 0, rowspan=9, columnspan=16)

        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/installaddons.png')
        self.placeControl(image, 8, 6, rowspan=4, columnspan=4)

		# Tvheadend button
        self.tvh_button = pyxbmct.Button('TVHEADEND')
        self.placeControl(self.tvh_button, 10, 11, rowspan=1, columnspan=3)
        self.connect(self.tvh_button, lambda: self.installaddons('service.tvheadend42'))

		# Tvheadend HTSP Client button
        self.htsp_button = pyxbmct.Button('HTSP CLIENT')
        self.placeControl(self.htsp_button, 10, 2, rowspan=1, columnspan=3)
        self.connect(self.htsp_button, lambda: self.installaddons('pvr.hts'))

		# Start button
        self.start_button = pyxbmct.Button('START')
        self.placeControl(self.start_button, 12, 7, rowspan=1, columnspan=2)
        self.connect(self.start_button, lambda: self.page('service.tvheadend42', 'pvr.hts'))

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.start_button.controlRight(self.close_button)
        self.start_button.controlLeft(self.htsp_button)
        self.start_button.controlUp(self.htsp_button)
        self.htsp_button.controlRight(self.tvh_button)
        self.tvh_button.controlLeft(self.htsp_button)
        self.htsp_button.controlDown(self.start_button)
        self.tvh_button.controlDown(self.start_button)
        self.close_button.controlLeft(self.start_button)
	    # Set initial focus.
        self.setFocus(self.start_button)

    def installaddons(self, id):
        if os.path.exists(xbmc.translatePath('special://home/addons/') + id):
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, 'Addon was alredy installed', 2000, addonicon))
        else:
            xbmc.executebuiltin('InstallAddon(%s)'%(id))
    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def page(self, id1, id2):
        if not os.path.exists(xbmc.translatePath('special://home/addons/') + id1):
            xbmc.executebuiltin(xbmcgui.Dialog().ok("Tvheadend Config", "The addons are not installed. Please install them to continue"))
        elif not os.path.exists(xbmc.translatePath('special://home/addons/') + id2):
            xbmc.executebuiltin(xbmcgui.Dialog().ok("Tvheadend Config", "The addons are not installed. Please install them to continue"))
        else:
            addon.setSetting(id='tvhconfig', value='true')
            addon.setSetting(id='tvhexpert', value='true')
            addon.setSetting(id='languien', value='true')
            addon.setSetting(id='langepg', value='true')
            addon.setSetting(id='langepgen', value='true')
            addon.setSetting(id='langepgpt', value='true')
            if addon.getSetting('start') == 'tvhwosc':
                ip_box = self.get_ip_address()
                addon.setSetting(id='dvbapienable', value='true')
                addon.setSetting(id='dvbapichoose', value='pc')
                addon.setSetting(id='ipdvbapi', value=ip_box)
                addon.setSetting(id='portdvbapi', value='9002')				
                self.close()
            else:
                self.close()
            Users().doModal()
		
class Start(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Start, self).__init__(title)
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
        image = pyxbmct.Image(addonfolder+artsfolder+'/start.png')
        self.placeControl(image, 8, 4, rowspan=2, columnspan=8)
		
		# YES button
        self.yes_button = pyxbmct.Button('YES')
        self.placeControl(self.yes_button, 11, 6, rowspan=1, columnspan=2)
        self.connect(self.yes_button, lambda: self.page(OSCam))

		# NO button
        self.no_button = pyxbmct.Button('NO')
        self.placeControl(self.no_button, 11, 8, rowspan=1, columnspan=2)
        self.connect(self.no_button, lambda: self.page(Tvheadend))

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.no_button.controlLeft(self.yes_button)
        self.no_button.controlRight(self.close_button)
        self.close_button.controlUp(self.no_button)
        self.yes_button.controlRight(self.no_button)
        self.yes_button.controlDown(self.close_button)
	    # Set initial focus.
        self.setFocus(self.no_button)

    def page(self, page):
        if page == OSCam:
            addon.setSetting(id='start', value='tvhwosc')
        else:
            addon.setSetting(id='start', value='tvh')
        self.close()
        page().doModal()

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
        if (addon.getSetting('portugal') == 'true'):
            self.portugal_button.setSelected(True)
        else:
            self.portugal_button.setSelected(False)
        portugal = pyxbmct.Image(addonfolder+artsfolder+'/portugal.png')
        self.placeControl(portugal, 9, 3, rowspan=2, columnspan=4)

		# Brasil
        self.brasil_button = pyxbmct.RadioButton('')
        self.placeControl(self.brasil_button, 9, 9, rowspan=2, columnspan=4)
        self.connect(self.brasil_button, self.brasil_button_update)
        if (addon.getSetting('brasil') == 'true'):
            self.brasil_button.setSelected(True)
        else:
            self.brasil_button.setSelected(False)
        brasil = pyxbmct.Image(addonfolder+artsfolder+'/brasil.png')
        self.placeControl(brasil, 9, 9, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        # Connect close button
        self.connect(self.close_button, self.close)

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
            addon.setSetting(id='portugal', value='true')
            Start().doModal()
        else:
            addon.setSetting(id='portugal', value='false')

    def brasil_button_update(self):
        if self.brasil_button.isSelected():
            self.close()
            addon.setSetting(id='brasil', value='true')
            TvheadendBR().doModal()
        else:
            addon.setSetting(id='brasil', value='false')

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
        # Connect close button
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.start_button.controlRight(self.close_button)
        self.close_button.controlLeft(self.start_button)
	    # Set initial focus.
        self.setFocus(self.start_button)

    def page(self):
        self.close()
        import tools
        Country().doModal()
		
if __name__ == '__main__':
    tvhwizard = TvhWizard('TvhWizard')
    tvhwizard.doModal()
    del tvhwizard
