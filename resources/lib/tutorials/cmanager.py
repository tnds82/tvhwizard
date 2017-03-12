#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds82
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import xbmcaddon, xbmcgui, xbmc, pyxbmct

addon             = xbmcaddon.Addon(id='script.tvhwizard')
addonname         = addon.getAddonInfo('name')
addonfolder       = addon.getAddonInfo('path')
artsfolder        = '/resources/img/tutorials'

pyxbmct.skin.estuary = True

		
class Cmanager1(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Manage Channels Instructions'):
        """Class constructor"""
        super(Cmanager1, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/cmanager1.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 4)
        self.textbox.setText("Channel Manager: Serve para fazer uma gestão do canais. Todas as alterações apenas ficam memorizadas no KODI\n"
                             "Permite activar e desactivar canais, alterar ou adicionar picon, activar e desactivar guia, alterar a ordem de algum canal. Activar o controlo parental caso tenha sido activada password\n"
							 "\n"
                             "")
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=4)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.setFocus(self.close_button)

if __name__ == '__main__':
    if sys.argv[1] == 'page1':
        Cmanager1().doModal()

