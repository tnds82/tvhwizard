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
        if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
            if tools.return_data('USERS', 'ID', 2, 1) == 'tvhadmin':
                tools.update_data('PVR', 'IP', self.get_ip_address(), 'ID', 1)
            else:
                tools.insert_pvr('tvh_htsp', '', '', self.get_ip_address())
				
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50033), 2000, addonicon))

            import oscam
            os.system('systemctl stop service.softcam.oscam')
            oscam.Oscam()
            os.system('systemctl start service.softcam.oscam')
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50033), 2000, addonicon))

            import tvheadend
            os.system('systemctl stop service.tvheadend42')
            tvheadend.Tvheadend()
            os.system('systemctl start service.tvheadend42')
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50022), 2000, addonicon))
            addon.setSetting(id='tvhstatus', value='Configured')
            addon.setSetting(id='tvh', value='Configured')
            addon.setSetting(id='oscam', value='Configured')
        else:
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
        tools.delete_tempfolder()
        self.close()
        time.sleep(1)
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(50023), 2000, addonicon))
        subprocess.call(['systemctl', 'restart', 'kodi'])

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
            self.tdt_button.setSelected(True)
        else:
            self.tdt_button.setSelected(False)
        tdt = pyxbmct.Image(addonfolder+artsfolder+'/tdt.png')
        self.placeControl(tdt, 11, 1, rowspan=1, columnspan=4)
        
		# Meo
        self.meo_button = pyxbmct.RadioButton('')
        self.placeControl(self.meo_button, 11, 6, rowspan=1, columnspan=4)
        self.connect(self.meo_button, self.meo_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
            self.meo_button.setSelected(True)
        else:
            self.meo_button.setSelected(False)
        meo = pyxbmct.Image(addonfolder+artsfolder+'/meo.png')
        self.placeControl(meo, 11, 6, rowspan=1, columnspan=4)

		# Vodafone
        self.vodafone_button = pyxbmct.RadioButton('')
        self.placeControl(self.vodafone_button, 11, 11, rowspan=1, columnspan=4)
        self.connect(self.vodafone_button, self.vodafone_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
            self.vodafone_button.setSelected(True)
        else:
            self.vodafone_button.setSelected(False)
        vodafone = pyxbmct.Image(addonfolder+artsfolder+'/vodafone.png')
        self.placeControl(vodafone, 11, 11, rowspan=1, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('tdt', 1)
            Finish().doModal()
        else:
            tools.insert_tvhwizard('tdt', 0)

    def meo_button_update(self):
        if self.meo_button.isSelected():
            self.close()
            tools.insert_tvhwizard('meo', 1)
            Finish().doModal()
        else:
            tools.insert_tvhwizard('meo', 0)

    def vodafone_button_update(self):
        if self.vodafone_button.isSelected():
            self.close()
            tools.insert_tvhwizard('vodafone', 1)
            Finish().doModal()
        else:
            tools.insert_tvhwizard('vodafone', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
            self.hispasat_button.setSelected(True)
        else:
            self.hispasat_button.setSelected(False)
        hispasat = pyxbmct.Image(addonfolder+artsfolder+'/hispasat.png')
        self.placeControl(hispasat, 11, 1, rowspan=1, columnspan=4)
        
		# Astra
        self.astra_button = pyxbmct.RadioButton('')
        self.placeControl(self.astra_button, 11, 6, rowspan=1, columnspan=4)
        self.connect(self.astra_button, self.astra_button_update)
#        if tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
#            self.astra_button.setSelected(True)
#        else:
#            self.astra_button.setSelected(False)
        astra = pyxbmct.Image(addonfolder+artsfolder+'/astra.png')
        self.placeControl(astra, 11, 6, rowspan=1, columnspan=4)

		# Hotbird
        self.hotbird_button = pyxbmct.RadioButton('')
        self.placeControl(self.hotbird_button, 11, 11, rowspan=1, columnspan=4)
        self.connect(self.hotbird_button, self.hotbird_button_update)
#        if tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
#            self.hotbird_button.setSelected(True)
#        else:
#            self.hotbird_button.setSelected(False)
        hotbird = pyxbmct.Image(addonfolder+artsfolder+'/hotbird.png')
        self.placeControl(hotbird, 11, 11, rowspan=1, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('hispasat', 1)
            Finish().doModal()
        else:
            tools.insert_tvhwizard('hispasat', 0)

    def astra_button_update(self):
        if self.astra_button.isSelected():
#            self.close()
#            tools.insert_tvhwizard('astra', 1)
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Comming Soon", "", "")
#        else:
#            tools.insert_tvhwizard('astra', 0)

    def hotbird_button_update(self):
        if self.hotbird_button.isSelected():
#            self.close()
#            tools.insert_tvhwizard('hotbird', 1)
#            Finish().doModal()
            xbmcgui.Dialog().ok(addonname, "Comming Soon", "", "")
#        else:
#            tools.insert_tvhwizard('hotbird', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
            self.nos_button.setSelected(True)
        else:
            self.nos_button.setSelected(False)
        nos = pyxbmct.Image(addonfolder+artsfolder+'/nos.png')
        self.placeControl(nos, 11, 3, rowspan=1, columnspan=4)
        
		# Nowo
        self.nowo_button = pyxbmct.RadioButton('')
        self.placeControl(self.nowo_button, 11, 9, rowspan=1, columnspan=4)
        self.connect(self.nowo_button, self.nowo_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
            self.nowo_button.setSelected(True)
        else:
            self.nowo_button.setSelected(False)
        nowo = pyxbmct.Image(addonfolder+artsfolder+'/nowo.png')
        self.placeControl(nowo, 11, 9, rowspan=1, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('nos', 1)
            Finish().doModal()
        else:
            tools.insert_tvhwizard('nos', 0)

    def nowo_button_update(self):
        if self.nowo_button.isSelected():
            self.close()
            tools.insert_tvhwizard('nowo', 1)
            Finish().doModal()
        else:
            tools.insert_tvhwizard('nowo', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'gdvbc', 2) == 1:
            self.dvbc_button.setSelected(True)
        else:
            self.dvbc_button.setSelected(False)
        dvbc = pyxbmct.Image(addonfolder+artsfolder+'/dvbc.png')
        self.placeControl(dvbc, 10, 1, rowspan=2, columnspan=4)
        
		# DVB-S
        self.dvbs_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbs_button, 10, 6, rowspan=2, columnspan=4)
        self.connect(self.dvbs_button, self.dvbs_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'gdvbs', 2) == 1:
            self.dvbs_button.setSelected(True)
        else:
            self.dvbs_button.setSelected(False)
        dvbs = pyxbmct.Image(addonfolder+artsfolder+'/dvbs2.png')
        self.placeControl(dvbs, 10, 6, rowspan=2, columnspan=4)

		# DVB-T
        self.dvbt_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbt_button, 10, 11, rowspan=2, columnspan=4)
        self.connect(self.dvbt_button, self.dvbt_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'gdvbt', 2) == 1:
            self.dvbt_button.setSelected(True)
        else:
            self.dvbt_button.setSelected(False)
        dvbt = pyxbmct.Image(addonfolder+artsfolder+'/dvbt.png')
        self.placeControl(dvbt, 10, 11, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('gdvbc', 1)
            DVBC().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('gdvbc', 0)

    def dvbs_button_update(self):
        if self.dvbs_button.isSelected():
            self.close()
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('gdvbs', 1)
            DVBS().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('gdvbs', 0)
             
    def dvbt_button_update(self):
        if self.dvbt_button.isSelected():
            self.close()	
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('gdvbt', 1)
            DVBT().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('gdvbt', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'usb', 2) == 1:
            self.usb_button.setSelected(True)
        else:
            self.usb_button.setSelected(False)
        usb = pyxbmct.Image(addonfolder+artsfolder+'/usb.png')
        self.placeControl(usb, 9, 3, rowspan=2, columnspan=4)

		# PCI-X
        self.pcix_button = pyxbmct.RadioButton('')
        self.placeControl(self.pcix_button, 9, 9, rowspan=2, columnspan=4)
        self.connect(self.pcix_button, self.pcix_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'pcix', 2) == 1:
            self.pcix_button.setSelected(True)
        else:
            self.pcix_button.setSelected(False)
        pcix = pyxbmct.Image(addonfolder+artsfolder+'/pcix.png')
        self.placeControl(pcix, 9, 9, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('usb', 1)
            DVBGeneric().doModal()
        else:
            tools.insert_tvhwizard('usb', 0)

    def pcix_button_update(self):
        if self.pcix_button.isSelected():
            self.close()
            tools.insert_tvhwizard('pcix', 1)
            DVBGeneric().doModal()
        else:
            tools.insert_tvhwizard('pcix', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

class DVBKhadas(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(DVBKhadas, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/khadasdvb.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=16)
		
		# DVB-C
        self.dvbc_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbc_button, 10, 1, rowspan=2, columnspan=4)
        self.connect(self.dvbc_button, self.dvbc_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbc', 2) == 1:
            self.dvbc_button.setSelected(True)
        else:
            self.dvbc_button.setSelected(False)
        dvbc = pyxbmct.Image(addonfolder+artsfolder+'/dvbc.png')
        self.placeControl(dvbc, 10, 1, rowspan=2, columnspan=4)
        
		# DVB-S
        self.dvbs_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbs_button, 10, 6, rowspan=2, columnspan=4)
        self.connect(self.dvbs_button, self.dvbs_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbs', 2) == 1:
            self.dvbs_button.setSelected(True)
        else:
            self.dvbs_button.setSelected(False)
        dvbs = pyxbmct.Image(addonfolder+artsfolder+'/dvbs2.png')
        self.placeControl(dvbs, 10, 6, rowspan=2, columnspan=4)

		# DVB-T
        self.dvbt_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbt_button, 10, 11, rowspan=2, columnspan=4)
        self.connect(self.dvbt_button, self.dvbt_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'khadasdvbt', 2) == 1:
            self.dvbt_button.setSelected(True)
        else:
            self.dvbt_button.setSelected(False)
        dvbt = pyxbmct.Image(addonfolder+artsfolder+'/dvbt.png')
        self.placeControl(dvbt, 10, 11, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('khadasdvbc', 1)
            DVBC().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('khadasdvbc', 0)

    def dvbs_button_update(self):
        if self.dvbs_button.isSelected():
            self.close()
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('khadasdvbs', 1)
            DVBS().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('khadasdvbs', 0)
             
    def dvbt_button_update(self):
        if self.dvbt_button.isSelected():
            self.close()	
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('khadasdvbt', 1)
            DVBT().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('khadasdvbt', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

class Khadas(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Khadas, self).__init__(title)
        self.setGeometry(1200, 680, 14, 16)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/khadas.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=16)

		# KHADAS VTV
        kvtv = pyxbmct.Image(addonfolder+artsfolder+'/kvtv.png')
        self.placeControl(kvtv, 8, 2, rowspan=5, columnspan=4)

		# KHADAS VIM 2
        kvim = pyxbmct.Image(addonfolder+artsfolder+'/kvim.png')
        self.placeControl(kvim, 8, 11, rowspan=5, columnspan=4)


		# KHADAS KVIM2 & VTV
        self.kvimvtv_button = pyxbmct.RadioButton('')
        self.placeControl(self.kvimvtv_button, 10, 7, rowspan=2, columnspan=3)
        self.connect(self.kvimvtv_button, self.kvimvtv_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'kvim2', 2) == 1:
            self.kvimvtv_button.setSelected(True)
        else:
            self.kvimvtv_button.setSelected(False)
        kvimvtv = pyxbmct.Image(addonfolder+artsfolder+'/kvimvtv.png')
        self.placeControl(kvimvtv, 10, 7, rowspan=2, columnspan=3)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.kvimvtv_button)
        self.kvimvtv_button.controlDown(self.close_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		

    def kvimvtv_button_update(self):
        if self.kvimvtv_button.isSelected():
            self.close()
            tools.insert_tvhwizard('kvim2', 1)
            DVBKhadas().doModal()
        else:
            tools.insert_tvhwizard('kvim2', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'kdvbt', 2) == 1:
            self.kdvbt_button.setSelected(True)
        else:
            self.kdvbt_button.setSelected(False)
        lnb1 = pyxbmct.Image(addonfolder+artsfolder+'/dvbt.png')
        self.placeControl(lnb1, 11, 1, rowspan=1, columnspan=3)

        # DVBC
        self.kdvbc_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbc_button, 12, 1, rowspan=1, columnspan=3)
        self.connect(self.kdvbc_button, self.kdvbc_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'kdvbc', 2) == 1:
            self.kdvbc_button.setSelected(True)
        else:
            self.kdvbc_button.setSelected(False)
        lnb1 = pyxbmct.Image(addonfolder+artsfolder+'/dvbc.png')
        self.placeControl(lnb1, 12, 1, rowspan=1, columnspan=3)

        # DVBS2
        self.kdvbs_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbs_button, 11, 6, rowspan=1, columnspan=3)
        self.connect(self.kdvbs_button, self.kdvbs_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'kdvbs', 2) == 1:
            self.kdvbs_button.setSelected(True)
        else:
            self.kdvbs_button.setSelected(False)
        lnb2 = pyxbmct.Image(addonfolder+artsfolder+'/dvbs2.png')
        self.placeControl(lnb2, 11, 6, rowspan=1, columnspan=3)

        # DVBT/DVBS2
        self.kdvbts_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbts_button, 11, 11, rowspan=1, columnspan=3)
        self.connect(self.kdvbts_button, self.kdvbts_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'kdvbts', 2) == 1:
            self.kdvbts_button.setSelected(True)
        else:
            self.kdvbts_button.setSelected(False)
        both = pyxbmct.Image(addonfolder+artsfolder+'/dvbts2.png')
        self.placeControl(both, 11, 11, rowspan=1, columnspan=3)

        # DVBC/DVBS2
        self.kdvbcs_button = pyxbmct.RadioButton('')
        self.placeControl(self.kdvbcs_button, 12, 11, rowspan=1, columnspan=3)
        self.connect(self.kdvbcs_button, self.kdvbcs_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'kdvbcs', 2) == 1:
            self.kdvbcs_button.setSelected(True)
        else:
            self.kdvbcs_button.setSelected(False)
        both = pyxbmct.Image(addonfolder+artsfolder+'/dvbcs2.png')
        self.placeControl(both, 12, 11, rowspan=1, columnspan=3)

        # Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('kdvbt', 1)
            DVBT().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('kdvbt', 0)
			
    def kdvbc_button_update(self):
        if self.kdvbc_button.isSelected():
            self.close()
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('kdvbc', 1)
            DVBC().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('kdvbc', 0)

    def kdvbs_button_update(self):
        if self.kdvbs_button.isSelected():
            self.close()
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('kdvbs', 1)
            DVBS().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('kdvbs', 0)

    def kdvbts_button_update(self):
        if self.kdvbts_button.isSelected():
#            self.close()
#            tools.insert_tvhwizard('picons', 1)
#            tools.insert_tvhwizard('kdvbts', 1)
#            DVBTS().doModal()
            xbmcgui.Dialog().ok(addonname, "Comming Soon", "", "")
#        else:
#            tools.insert_tvhwizard('picons', 0)
#            tools.insert_tvhwizard('kdvbts', 0)

    def kdvbcs_button_update(self):
        if self.kdvbcs_button.isSelected():
#            self.close()
#            tools.insert_tvhwizard('picons', 1)
#            tools.insert_tvhwizard('kdvbcs', 1)
#            DVBCS().doModal()
            xbmcgui.Dialog().ok(addonname, "Comming Soon", "", "")
#        else:
#            tools.insert_tvhwizard('picons', 0)
#            tools.insert_tvhwizard('kdvbcs', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
            DVBK().doModal()
        else:
            tools.insert_tvhwizard('k1plus', 0)

    def k1pro_button_update(self):
        if self.k1pro_button.isSelected():
            self.close()
            tools.insert_tvhwizard('k1pro', 1)
            DVBK().doModal()
        else:
            tools.insert_tvhwizard('k1pro', 0)

    def k2pro_button_update(self):
        if self.k2pro_button.isSelected():
            self.close()
            tools.insert_tvhwizard('k2pro', 1)
            DVBK().doModal()
        else:
            tools.insert_tvhwizard('k2pro', 0)

    def k3pro_button_update(self):
        if self.k3pro_button.isSelected():
            self.close()
            tools.insert_tvhwizard('k3pro', 1)
            DVBK().doModal()
        else:
            tools.insert_tvhwizard('k3pro', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'wplnb1', 2) == 1:
            self.wplnb1_button.setSelected(True)
        else:
            self.wplnb1_button.setSelected(False)
        lnb1 = pyxbmct.Image(addonfolder+artsfolder+'/lnb1.png')
        self.placeControl(lnb1, 11, 1, rowspan=1, columnspan=4)

        # LNB2
        self.wplnb2_button = pyxbmct.RadioButton('')
        self.placeControl(self.wplnb2_button, 11, 6, rowspan=1, columnspan=4)
        self.connect(self.wplnb2_button, self.wplnb2_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'wplnb2', 2) == 1:
            self.wplnb2_button.setSelected(True)
        else:
            self.wplnb2_button.setSelected(False)
        lnb2 = pyxbmct.Image(addonfolder+artsfolder+'/lnb2.png')
        self.placeControl(lnb2, 11, 6, rowspan=1, columnspan=4)

        # LNB1/LNB2
        self.wplnboth_button = pyxbmct.RadioButton('')
        self.placeControl(self.wplnboth_button, 11, 11, rowspan=1, columnspan=4)
        self.connect(self.wplnboth_button, self.wplnboth_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'wplnboth', 2) == 1:
            self.wplnboth_button.setSelected(True)
        else:
            self.wplnboth_button.setSelected(False)
        both = pyxbmct.Image(addonfolder+artsfolder+'/both.png')
        self.placeControl(both, 11, 11, rowspan=1, columnspan=4)

        # Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('wplnb1', 1)
            DVBS().doModal()
        else:
            tools.insert_tvhwizard('wplnb1', 0)
 
    def wplnb2_button_update(self):
        if self.wplnb2_button.isSelected():
            self.close()
            tools.insert_tvhwizard('wplnb2', 1)
            DVBS().doModal()
        else:
            tools.insert_tvhwizard('wplnb2', 0)
            addon.setSetting(id='wplnb2', value='false')

    def wplnboth_button_update(self):
        if self.wplnboth_button.isSelected():
            self.close()
            tools.insert_tvhwizard('wplnboth', 1)
            DVBS().doModal()
        else:
            tools.insert_tvhwizard('wplnboth', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'wdvbc', 2) == 1:
            self.dvbc_button.setSelected(True)
        else:
            self.dvbc_button.setSelected(False)
        dvbc = pyxbmct.Image(addonfolder+artsfolder+'/dvbc.png')
        self.placeControl(dvbc, 10, 1, rowspan=2, columnspan=4)
        
		# DVB-S
        self.dvbs_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbs_button, 10, 6, rowspan=2, columnspan=4)
        self.connect(self.dvbs_button, self.dvbs_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'wdvbs', 2) == 1:
            self.dvbs_button.setSelected(True)
        else:
            self.dvbs_button.setSelected(False)
        dvbs = pyxbmct.Image(addonfolder+artsfolder+'/dvbs2.png')
        self.placeControl(dvbs, 10, 6, rowspan=2, columnspan=4)

		# DVB-T
        self.dvbt_button = pyxbmct.RadioButton('')
        self.placeControl(self.dvbt_button, 10, 11, rowspan=2, columnspan=4)
        self.connect(self.dvbt_button, self.dvbt_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'wdvbt', 2) == 1:
            self.dvbt_button.setSelected(True)
        else:
            self.dvbt_button.setSelected(False)
        dvbt = pyxbmct.Image(addonfolder+artsfolder+'/dvbt.png')
        self.placeControl(dvbt, 10, 11, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('wdvbc', 1)
            DVBC().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('wdvbc', 0)

    def dvbs_button_update(self):
        if self.dvbs_button.isSelected():
            self.close()
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('wdvbs', 1)
            if tools.return_data('TVHWIZARD', 'STRING', 'wetekplay', 2) == 1:
			    WetekPlay().doModal()
            else:
                DVBS().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('wdvbs', 0)
             
    def dvbt_button_update(self):
        if self.dvbt_button.isSelected():
            self.close()
            tools.insert_tvhwizard('picons', 1)
            tools.insert_tvhwizard('wdvbt', 1)
            DVBT().doModal()
        else:
            tools.insert_tvhwizard('picons', 0)
            tools.insert_tvhwizard('wdvbt', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        self.placeControl(self.wp_button, 10, 3, rowspan=2, columnspan=4)
        self.connect(self.wp_button, self.wp_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'wetekplay', 2) == 1:
            self.wp_button.setSelected(True)
        else:
            self.wp_button.setSelected(False)
        wp = pyxbmct.Image(addonfolder+artsfolder+'/wp.png')
        self.placeControl(wp, 10, 3, rowspan=2, columnspan=4)

		# WetekPlay2
        self.wp2_button = pyxbmct.RadioButton('')
        self.placeControl(self.wp2_button, 10, 9, rowspan=2, columnspan=4)
        self.connect(self.wp2_button, self.wp2_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'wetekplay2', 2) == 1:
            self.wp2_button.setSelected(True)
        else:
            self.wp2_button.setSelected(False)
        wp2 = pyxbmct.Image(addonfolder+artsfolder+'/wp2.png')
        self.placeControl(wp2, 10, 9, rowspan=2, columnspan=4)

		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.wp_button)
        self.wp_button.controlDown(self.close_button)
        self.wp_button.controlRight(self.wp2_button)
        self.wp2_button.controlDown(self.close_button)
        self.wp2_button.controlLeft(self.wp_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def wp_button_update(self):
        if self.wp_button.isSelected():
            self.close()
            tools.insert_tvhwizard('wetekplay', 1)
            DVBWetek().doModal()
        else:
            tools.insert_tvhwizard('wetekplay', 0)

    def wp2_button_update(self):
        if self.wp2_button.isSelected():
            self.close()
            tools.insert_tvhwizard('wetekplay2', 1)
            DVBWetek().doModal()
        else:
            tools.insert_tvhwizard('wetekplay2', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

class Inputs(pyxbmct.AddonFullWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Inputs, self).__init__(title)
        self.setGeometry(1200, 680, 14, 17)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        # Image control
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh.png')
        self.placeControl(image, 0, 0, rowspan=8, columnspan=17)

		# Wetek Button
        self.wetek_button = pyxbmct.RadioButton('')
        self.placeControl(self.wetek_button, 9, 1, rowspan=3, columnspan=3)
        self.connect(self.wetek_button, self.wetek_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'wetek', 2) == 1:
            self.wetek_button.setSelected(True)
        else:
            self.wetek_button.setSelected(False)
        wetek = pyxbmct.Image(addonfolder+artsfolder+'/weteksmall.png')
        self.placeControl(wetek, 9, 1, rowspan=3, columnspan=3)

		# K Button
        self.k_button = pyxbmct.RadioButton('')
        self.placeControl(self.k_button, 9, 5, rowspan=3, columnspan=3)
        self.connect(self.k_button, self.k_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'k', 2) == 1:
            self.k_button.setSelected(True)
        else:
            self.k_button.setSelected(False)
        k = pyxbmct.Image(addonfolder+artsfolder+'/ksmall.png')
        self.placeControl(k, 9, 5, rowspan=3, columnspan=3)

		# Khadas Button
        self.khadas_button = pyxbmct.RadioButton('')
        self.placeControl(self.khadas_button, 9, 9, rowspan=3, columnspan=3)
        self.connect(self.khadas_button, self.khadas_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'khadas', 2) == 1:
            self.khadas_button.setSelected(True)
        else:
            self.khadas_button.setSelected(False)
        khadas = pyxbmct.Image(addonfolder+artsfolder+'/khadasmall.png')
        self.placeControl(khadas, 9, 9, rowspan=3, columnspan=3)

		# Generic Button
        self.generic_button = pyxbmct.RadioButton('')
        self.placeControl(self.generic_button, 9, 13, rowspan=3, columnspan=3)
        self.connect(self.generic_button, self.generic_button_update)
        if tools.return_data('TVHWIZARD', 'STRING', 'generic', 2) == 1:
            self.generic_button.setSelected(True)
        else:
            self.generic_button.setSelected(False)
        generic = pyxbmct.Image(addonfolder+artsfolder+'/genericsmall.png')
        self.placeControl(generic, 9, 13, rowspan=3, columnspan=3)
		
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 16, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.wetek_button)
        self.wetek_button.controlDown(self.close_button)
        self.wetek_button.controlRight(self.k_button)
        self.k_button.controlRight(self.khadas_button)
        self.k_button.controlDown(self.close_button)
        self.khadas_button.controlRight(self.generic_button)
        self.khadas_button.controlDown(self.close_button)
        self.generic_button.controlLeft(self.khadas_button)
        self.generic_button.controlDown(self.close_button)
        self.k_button.controlLeft(self.wetek_button)
        self.khadas_button.controlLeft(self.k_button)
	    # Set initial focus.
        self.setFocus(self.close_button)
		
    def wetek_button_update(self):
        if self.wetek_button.isSelected():
            self.close()
            tools.insert_tvhwizard('dvbcards', 1)
            tools.insert_tvhwizard('wetek', 1)
            Wetek().doModal()
        else:
            tools.insert_tvhwizard('dvbcards', 0)
            tools.insert_tvhwizard('wetek', 0)

    def k_button_update(self):
        if self.k_button.isSelected():
            self.close()
            tools.insert_tvhwizard('dvbcards', 1)
            tools.insert_tvhwizard('k', 1)
            tools.set_addon('driver.dvb.crazycat', True)
            K().doModal()
        else:
            tools.insert_tvhwizard('dvbcards', 0)
            tools.insert_tvhwizard('k', 0)

    def generic_button_update(self):
        if self.generic_button.isSelected():
            self.close()
            tools.insert_tvhwizard('dvbcards', 1)
            tools.insert_tvhwizard('generic', 1)
            Generic().doModal()
        else:
            tools.insert_tvhwizard('dvbcards', 0)
            tools.insert_tvhwizard('generic', 0)

    def khadas_button_update(self):
        if self.khadas_button.isSelected():
            self.close()
            tools.insert_tvhwizard('dvbcards', 1)
            tools.insert_tvhwizard('khadas', 1)
            tools.set_addon('driver.dvb.crazycat', True)
            Khadas().doModal()
        else:
            tools.insert_tvhwizard('dvbcards', 0)
            tools.insert_tvhwizard('khadas', 0)

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('RECORDS', 'ID', 1, 1) == '':
            self.browse_label.setText('')
        else:
            path = tools.return_data('RECORDS', 'ID', 1, 1)
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
        Recording().doModal()

    def page(self):
        tools.insert_tvhwizard('recording', 1)
        tools.insert_tvhwizard('mkvprofile', 1)
        self.close()
        Inputs().doModal()

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))
		
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
            Recording().doModal()
        else:
            tools.insert_tvhwizard('createusers', 1)
            tools.insert_users('tvhadmin', self.username_input.getText(), self.password_input.getText(), '')
            tools.insert_users('tvhclient', 'tvh', 'tvh', '')
            tools.insert_pvr('tvh_htsp', 'tvh', 'tvh', '')
            tools.insert_records('')
            self.close()
            Recording().doModal()

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
            tools.insert_tvhwizard('tvhconfig', 1)
            if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
                tools.insert_oscam('dvbapi', 'pc', self.get_ip_address(), '9002')
                self.close()
            else:
                self.close()
            Users().doModal()

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        if tools.return_data('TVHWIZARD', 'STRING', 'rfifth', 2) == 1:
            tools.insert_readers('cccam', 'reader5', self.hostname_input.getText(), self.username_input.getText(), self.password_input.getText(), self.port_input.getText(), '')
        elif tools.return_data('TVHWIZARD', 'STRING', 'rfourth', 2) == 1:
            tools.insert_readers('cccam', 'reader4', self.hostname_input.getText(), self.username_input.getText(), self.password_input.getText(), self.port_input.getText(), '')
        elif tools.return_data('TVHWIZARD', 'STRING', 'rthird', 2) == 1:
            tools.insert_readers('cccam', 'reader3', self.hostname_input.getText(), self.username_input.getText(), self.password_input.getText(), self.port_input.getText(), '')
        elif tools.return_data('TVHWIZARD', 'STRING', 'rsecond', 2) == 1:
            tools.insert_readers('cccam', 'reader2', self.hostname_input.getText(), self.username_input.getText(), self.password_input.getText(), self.port_input.getText(), '')
        elif tools.return_data('TVHWIZARD', 'STRING', 'rfirst', 2) == 1:
            tools.insert_readers('cccam', 'reader1', self.hostname_input.getText(), self.username_input.getText(), self.password_input.getText(), self.port_input.getText(), '')
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
        if tools.return_data('TVHWIZARD', 'STRING', 'rfirst', 2) == 1:
            color1 = '0xFF00FF00'
        else:
            color1 = '0xFFFF0000'
        self.reader1_button = pyxbmct.Button('READER 1', textColor=color1)
        self.placeControl(self.reader1_button, 10, 1, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.reader1_button, lambda: self.reader(ReaderCccam, 'rfirst', 1))
		
		# Reader 2
        if tools.return_data('TVHWIZARD', 'STRING', 'rsecond', 2) == 1:
            color2 = '0xFF00FF00'
        else:
            color2 = '0xFFFF0000'
        self.reader2_button = pyxbmct.Button('READER 2', textColor=color2)
        self.placeControl(self.reader2_button, 10, 4, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.reader2_button, lambda: self.reader(ReaderCccam, 'rsecond', 1))

		# Reader 3
        if tools.return_data('TVHWIZARD', 'STRING', 'rthird', 2) == 1:
            color3 = '0xFF00FF00'
        else:
            color3 = '0xFFFF0000'
        self.reader3_button = pyxbmct.Button('READER 3', textColor=color3)
        self.placeControl(self.reader3_button, 10, 7, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.reader3_button, lambda: self.reader(ReaderCccam, 'rthird', 1))

		# Reader 4
        if tools.return_data('TVHWIZARD', 'STRING', 'rfourth', 2) == 1:
            color4 = '0xFF00FF00'
        else:
            color4 = '0xFFFF0000'
        self.reader4_button = pyxbmct.Button('READER 4', textColor=color4)
        self.placeControl(self.reader4_button, 10, 10, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.reader4_button, lambda: self.reader(ReaderCccam, 'rfourth', 1))

		# Reader 5
        if tools.return_data('TVHWIZARD', 'STRING', 'rfifth', 2) == 1:
            color5 = '0xFF00FF00'
        else:
            color5 = '0xFFFF0000'
        self.reader5_button = pyxbmct.Button('READER 5', textColor=color5)
        self.placeControl(self.reader5_button, 10, 13, rowspan=1, columnspan=2)
        # Connect close button
        self.connect(self.reader5_button, lambda: self.reader(ReaderCccam, 'rfifth', 1))
		
		# Next button
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 13, 14, rowspan=1, columnspan=1)
        self.connect(self.next_button, lambda: self.page(Tvheadend))
		
		# Close button
        self.close_button = pyxbmct.Button('Exit')
        self.placeControl(self.close_button, 13, 15, rowspan=1, columnspan=1)
        self.connect(self.close_button, lambda: self.closepage())

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

    def reader(self, page, reader, choice):
        tools.insert_tvhwizard(reader, choice)
        self.close()
        page().doModal()

    def page(self, page):
        self.close()
        page().doModal()

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        self.connect(self.close_button, lambda: self.closepage())

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
        tools.insert_users('oscam',self.username_input.getText(),self.password_input.getText(),self.port_input.getText())
        tools.insert_tvhwizard('dvbapioscam', 1)
        self.close()
        Readers().doModal()

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))
		
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
        self.connect(self.close_button, lambda: self.closepage())

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
            UsersOscam().doModal()

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

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
        self.connect(self.close_button, lambda: self.closepage())

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
            tools.insert_tvhwizard('tvhwosc', 1)
        else:
            tools.insert_tvhwizard('tvhwosc', 0)
        self.close()
        page().doModal()

    def closepage(self):
        self.close()
        subprocess_cmd('%s %s' % ('rm -r', database))

