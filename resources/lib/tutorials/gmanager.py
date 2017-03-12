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

		
class Gmanager1(pyxbmct.AddonDialogWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(Gmanager1, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/gmanager1.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 4)
        self.textbox.setText("Group Manager: Serve para fazer uma gestão dos grupos. Todas as alterações apenas ficam memorizadas no KODI\n"
                             "Permite criar novos grupos de canais, adicionar ou remover canais de grupos\n"
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
        Gmanager1().doModal()
