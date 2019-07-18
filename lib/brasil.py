#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmcaddon
import xbmcgui
import xbmc
import pyxbmct, os, time, socket, subprocess
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
        self.connect(self.close_button, lambda: self.closepage())

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
        if tools.return_data('USERS', 'ID', 1, 1) == 'tvhadmin':
            tools.update_data('PVR', 'IP', self.get_ip_address(), 'ID', 1)
        else:
            tools.insert_pvr('tvh_htsp', '', '', self.get_ip_address())
        import tvheadend
        os.system('systemctl stop service.tvheadend42')
        tvheadend.Tvheadend()
        os.system('systemctl start service.tvheadend42')
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50022), 2000, addonicon))
        addon.setSetting(id='tvhstatus', value='Configured')
        addon.setSetting(id='tvh', value='Configured')
        pvripbox = tools.return_data('PVR', 'PROGRAM', 'tvh_htsp', 4)
        addon.setSetting(id='tvhip', value=pvripbox)
        tools.insert_tvhwizard('changeip', 1)
        self.close()
        time.sleep(1)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50023), 2000, addonicon))
        tools.delete_tempfolder()
        subprocess.call(['systemctl', 'restart', 'kodi'])

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'deskey1', 2) == 1:
            self.deskey1_button.setSelected(True)
        else:
            self.deskey1_button.setSelected(False)
        deskey1 = pyxbmct.Image(addonfolder+artsfolder+'/deskey1.png')
        self.placeControl(deskey1, 10, 9, rowspan=1, columnspan=6)

		# DESKey2
        self.deskey2_button = pyxbmct.RadioButton('')
        self.placeControl(self.deskey2_button, 11, 9, rowspan=1, columnspan=6)
        self.connect(self.deskey2_button, self.deskey2_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'deskey2', 2) == 1:
            self.deskey2_button.setSelected(True)
        else:
            self.deskey2_button.setSelected(False)
        deskey2 = pyxbmct.Image(addonfolder+artsfolder+'/deskey2.png')
        self.placeControl(deskey2, 11, 9, rowspan=1, columnspan=6)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())
        
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
            tools.insert_tvhwizard('deskey1', 1)
            tools.insert_tvhwizard('dvbapioscam', 1)
            tools.insert_readers('newcamd', 'deskey1', self.hostname_input.getText(), self.username_input.getText(), self.password_input.getText(), self.port_input.getText(), '01:02:03:04:05:06:07:08:09:10:11:12:13:14')
            self.close()
            FinishBR().doModal()
        else:
            tools.insert_tvhwizard('deskey1', 0)

    def deskey2_button_update(self):
        if self.deskey2_button.isSelected():
            tools.insert_tvhwizard('deskey2', 1)
            tools.insert_tvhwizard('dvbapioscam', 1)
            tools.insert_readers('newcamd', 'deskey2', self.hostname_input.getText(), self.username_input.getText(), self.password_input.getText(), self.port_input.getText(), '10:10:10:10:10:10:10:10:10:10:11:12:13:14')
            self.close()
            FinishBR().doModal()
        else:
            tools.insert_tvhwizard('deskey2', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
            self.clarotv_button.setSelected(True)
        else:
            self.clarotv_button.setSelected(False)
        clarotv = pyxbmct.Image(addonfolder+artsfolder+'/clarotv.png')
        self.placeControl(clarotv, 11, 6, rowspan=1, columnspan=4)
        
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.clarotv_button)
        self.clarotv_button.controlDown(self.close_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def clarotv_button_update(self):
        if self.clarotv_button.isSelected():
            self.close()
            tools.insert_tvhwizard('clarotv', 1)
            Newcamd().doModal()
        else:
            tools.insert_tvhwizard('clarotv', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
            self.net_button.setSelected(True)
        else:
            self.net_button.setSelected(False)
        net = pyxbmct.Image(addonfolder+artsfolder+'/net.png')
        self.placeControl(net, 11, 6, rowspan=1, columnspan=4)
        
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.net_button)
        self.net_button.controlDown(self.close_button)
	    # Set initial focus.
        self.setFocus(self.close_button)

    def net_button_update(self):
        if self.net_button.isSelected():
            self.close()
            tools.insert_tvhwizard('net', 1)
            Newcamd().doModal()
        else:
            tools.insert_tvhwizard('net', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'kdvbc', 2) == 1:
            self.kdvbc_button.setSelected(True)
        else:
            self.kdvbc_button.setSelected(False)
        lnb1 = pyxbmct.Image(addonfolder+artsfolder+'/dvbc.png')
        self.placeControl(lnb1, 11, 3, rowspan=1, columnspan=3)

        # DVBS2
        self.kdvbs_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbs_button, 11, 10, rowspan=1, columnspan=3)
        self.connect(self.kdvbs_button, self.kdvbs_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'kdvbs', 2) == 1:
            self.kdvbs_button.setSelected(True)
        else:
            self.kdvbs_button.setSelected(False)
        lnb2 = pyxbmct.Image(addonfolder+artsfolder+'/dvbs2.png')
        self.placeControl(lnb2, 11, 10, rowspan=1, columnspan=3)

        # Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('kdvbc', 1)
            DVBCBR().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('kdvbc', 0)

    def kdvbs_button_update(self):
        if self.kdvbs_button.isSelected():
            self.close()
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('kdvbs', 1)
            DVBSBR().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('kdvbs', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'k1plus', 2) == 1:
            self.k1plus_button.setSelected(True)
        else:
            self.k1plus_button.setSelected(False)
        k1plus = pyxbmct.Image(addonfolder+artsfolder+'/k1plus.png')
        self.placeControl(k1plus, 8, 1, rowspan=2, columnspan=4)

		# KI Pro
        self.k1pro_button = pyxbmct.RadioButton('')
        self.placeControl(self.k1pro_button, 11, 6, rowspan=2, columnspan=4)
        self.connect(self.k1pro_button, self.k1pro_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'k1pro', 2) == 1:
            self.k1pro_button.setSelected(True)
        else:
            self.k1pro_button.setSelected(False)
        k1pro = pyxbmct.Image(addonfolder+artsfolder+'/k1pro.png')
        self.placeControl(k1pro, 11, 6, rowspan=2, columnspan=4)

		# KII Pro
        self.k2pro_button = pyxbmct.RadioButton('')
        self.placeControl(self.k2pro_button, 8, 6, rowspan=2, columnspan=4)
        self.connect(self.k2pro_button, self.k2pro_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'k2pro', 2) == 1:
            self.k2pro_button.setSelected(True)
        else:
            self.k2pro_button.setSelected(False)
        k2pro = pyxbmct.Image(addonfolder+artsfolder+'/k2pro.png')
        self.placeControl(k2pro, 8, 6, rowspan=2, columnspan=4)

		# KIII Pro
        self.k3pro_button = pyxbmct.RadioButton('')
        self.placeControl(self.k3pro_button, 8, 11, rowspan=2, columnspan=4)
        self.connect(self.k3pro_button, self.k3pro_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'k3pro', 2) == 1:
            self.k3pro_button.setSelected(True)
        else:
            self.k3pro_button.setSelected(False)
        k3pro = pyxbmct.Image(addonfolder+artsfolder+'/k3pro.png')
        self.placeControl(k3pro, 8, 11, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('k1plus', 1)
            DVBKBR().doModal()
        else:
            tools.insert_tvhwizard('k1plus', 0)

    def k1pro_button_update(self):
        if self.k1pro_button.isSelected():
            self.close()
            tools.insert_tvhwizard('k1pro', 1)
            DVBKBR().doModal()
        else:
            tools.insert_tvhwizard('k1pro', 0)

    def k2pro_button_update(self):
        if self.k2pro_button.isSelected():
            self.close()
            tools.insert_tvhwizard('k2pro', 1)
            DVBKBR().doModal()
        else:
            tools.insert_tvhwizard('k2pro', 0)

    def k3pro_button_update(self):
        if self.k3pro_button.isSelected():
            self.close()
            tools.insert_tvhwizard('k3pro', 1)
            DVBKBR().doModal()
        else:
            tools.insert_tvhwizard('k3pro', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

class DVBWetekBR(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBWetekBR, self).__init__(title)
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
        self.placeControl(self.dvbc_button, 9, 3, rowspan=2, columnspan=4)
        self.connect(self.dvbc_button, self.dvbc_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'wdvbc', 2) == 1:
            self.dvbc_button.setSelected(True)
        else:
            self.dvbc_button.setSelected(False)
        dvbc = pyxbmct.Image(addonfolder+artsfolder+'/dvbc.png')
        self.placeControl(dvbc, 9, 3, rowspan=2, columnspan=4)
        
		# DVB-S
        self.dvbs_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbs_button, 9, 10, rowspan=2, columnspan=4)
        self.connect(self.dvbs_button, self.dvbs_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'wdvbs', 2) == 1:
            self.dvbs_button.setSelected(True)
        else:
            self.dvbs_button.setSelected(False)
        dvbs = pyxbmct.Image(addonfolder+artsfolder+'/dvbs2.png')
        self.placeControl(dvbs, 9, 10, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.dvbc_button)
        self.dvbc_button.controlDown(self.close_button)
        self.dvbc_button.controlRight(self.dvbs_button)
        self.dvbs_button.controlDown(self.close_button)
        self.dvbs_button.controlLeft(self.dvbc_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def dvbc_button_update(self):
        if self.dvbc_button.isSelected():
            self.close()
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('wdvbc', 1)
            DVBCBR().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('wdvbc', 0)

    def dvbs_button_update(self):
        if self.dvbs_button.isSelected():
            self.close()
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('wdvbs', 1)
            DVBSBR().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('wdvbs', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

class WetekBR(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(WetekBR, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/wetek.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)


		# WetekPlay2
        self.wp2_button = pyxbmct.RadioButton('')
        self.placeControl(self.wp2_button, 9, 6, rowspan=2, columnspan=4)
        self.connect(self.wp2_button, self.wp2_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'wetekplay2', 2) == 1:
            self.wp2_button.setSelected(True)
        else:
            self.wp2_button.setSelected(False)
        wp2 = pyxbmct.Image(addonfolder+artsfolder+'/wp2.png')
        self.placeControl(wp2, 9, 6, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.wp2_button)
        self.wp2_button.controlDown(self.close_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def wp2_button_update(self):
        if self.wp2_button.isSelected():
            self.close()
            tools.insert_tvhwizard('wetekplay2', 1)
            DVBWetekBR().doModal()
        else:
            tools.insert_tvhwizard('wetekplay2', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

class InputsBR(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(InputsBR, self).__init__(title)
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
        self.placeControl(self.wetek_button, 9, 3, rowspan=3, columnspan=3)
        self.connect(self.wetek_button, self.wetek_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'wetek', 2) == 1:
            self.wetek_button.setSelected(True)
        else:
            self.wetek_button.setSelected(False)
        wetek = pyxbmct.Image(addonfolder+artsfolder+'/weteksmall.png')
        self.placeControl(wetek, 9, 3, rowspan=3, columnspan=3)

		# K Button
        self.k_button = pyxbmct.RadioButton('')
        self.placeControl(self.k_button, 9, 10, rowspan=3, columnspan=3)
        self.connect(self.k_button, self.k_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'k', 2) == 1:
            self.k_button.setSelected(True)
        else:
            self.k_button.setSelected(False)
        k = pyxbmct.Image(addonfolder+artsfolder+'/ksmall.png')
        self.placeControl(k, 9, 10, rowspan=3, columnspan=3)
		
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.wetek_button)
        self.wetek_button.controlDown(self.close_button)
        self.wetek_button.controlRight(self.k_button)
        self.k_button.controlDown(self.close_button)
        self.k_button.controlLeft(self.wetek_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def wetek_button_update(self):
        if self.wetek_button.isSelected():
            self.close()
            tools.insert_tvhwizard('dvbcards', 1)
            tools.insert_tvhwizard('wetek', 1)
            WetekBR().doModal()
        else:
            tools.insert_tvhwizard('dvbcards', 0)
            tools.insert_tvhwizard('wetek', 0)

    def k_button_update(self):
        if self.k_button.isSelected():
            self.close()
            tools.insert_tvhwizard('dvbcards', 1)
            tools.insert_tvhwizard('k', 1)
            tools.set_addon('driver.dvb.crazycat', True)
            KBR().doModal()
        else:
            tools.insert_tvhwizard('dvbcards', 0)
            tools.insert_tvhwizard('k', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('RECORDS', 'ID', 1, 1) == '':
            self.browse_label.setText('')
        else:
            path = tools.return_data('RECORDS', 'ID', 1, 1)
            self.browse_label.setText(path)
			
		# Browse input
        self.browse_button = pyxbmct.Button('Browse')
        self.placeControl(self.browse_button, 11, 6, rowspan=1, columnspan=2)
        self.connect(self.browse_button, lambda: self.browse())

		# Next button
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 13, 14, rowspan=1, columnspan=1)
        self.connect(self.next_button, lambda: self.page())
		
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
        tools.update_data('RECORDS', 'CAMINHO', browsepath, 'ID', 1)
        self.close()
        RecordingBR().doModal()

    def page(self):
        tools.insert_tvhwizard('recording', 1)
        tools.insert_tvhwizard('mkvprofile', 1)
        self.close()
        InputsBR().doModal()

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_records('')
            self.close()
            RecordingBR().doModal()
        else:
            tools.insert_tvhwizard('createusers', 1)
            tools.insert_users('tvhadmin', self.username_input.getText(), self.password_input.getText(), '')
            tools.insert_users('tvhclient', 'tvh', 'tvh', '')
            tools.insert_pvr('tvh_htsp', 'tvh', 'tvh', '')
            tools.insert_records('')
            self.close()
            RecordingBR().doModal()

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))
		
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
        self.connect(self.close_button, lambda: self.closepage())

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

    def page(self, id1, id2):
        if not os.path.exists(xbmc.translatePath('special://home/addons/') + id1):
            xbmc.executebuiltin(xbmcgui.Dialog().ok("Tvheadend Config", "The addons are not installed. Please install them to continue"))
        elif not os.path.exists(xbmc.translatePath('special://home/addons/') + id2):
            xbmc.executebuiltin(xbmcgui.Dialog().ok("Tvheadend Config", "The addons are not installed. Please install them to continue"))
        else:
            tools.insert_tvhwizard('tvhconfig', 1)
            self.close()
            UsersBR().doModal()

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))
		
