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

class Clientpage4(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Client Instructions (Page 4)'):
        """Class constructor"""
        super(Clientpage4, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/client4.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Guide: Permite escolher como o guide faz o update no Kodi\n"
                             "Activar o Config Guide, já vem pré configurado, mas pode sempre ser modificado o intervalo de tempo\n"
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Clientpage3()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=4)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.previous_button)
        self.previous_button.controlDown(self.close_button)
        self.setFocus(self.previous_button)

    def page(self, page):
        self.close()
        page.doModal()

class Clientpage3(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Client Instructions (Page 3)'):
        """Class constructor"""
        super(Clientpage3, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/client3.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Kodi: Permite activar um serie de funções no Kodi\n"
                             "Activar o Config Kodi, as funções já se encontram pré activadas, mas podem desactivar as que não desejarem\n"
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Clientpage2()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Clientpage4()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=4)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.previous_button)
        self.previous_button.controlDown(self.close_button)
        self.previous_button.controlRight(self.next_button)
        self.next_button.controlLeft(self.previous_button)
        self.next_button.controlDown(self.close_button)		
        self.setFocus(self.next_button)

    def page(self, page):
        self.close()
        page.doModal()
		
class Clientpage2(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Client Instructions (Page 2)'):
        """Class constructor"""
        super(Clientpage2, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/client2.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("PVR: Configuração do HTSP Client Tvheadend\n"
                             "Activar a Configuração do Client PVR e preencher os dados\n"
                             "Hostname/IP: Preencher com o IP do equipamento que tem o Tvheadend Server\n"
							 "Username: Colocar o username de acesso do Tvheadend Sever\n"
                             "Password: Colocar a password de acesso do username")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Clientpage1()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Clientpage3()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=4)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.previous_button)
        self.previous_button.controlDown(self.close_button)
        self.previous_button.controlRight(self.next_button)
        self.next_button.controlLeft(self.previous_button)
        self.next_button.controlDown(self.close_button)		
        self.setFocus(self.next_button)

    def page(self, page):
        self.close()
        page.doModal()
		
class Clientpage1(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Client Instructions (Page 1)'):
        """Class constructor"""
        super(Clientpage1, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/client1.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Addons: Addons necessários a configuração do Tvheadend Client\n"
                             "Clicar para poder instalar o addon necessário\n"
							 "\n"
                             "[COLOR red]Nota:[/COLOR] Caso os addon já tenham sido instalados não clicar para instalar o addon")
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Clientpage2()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=4)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.next_button)
        self.next_button.controlDown(self.close_button)
        self.setFocus(self.next_button)

    def page(self, page):
        self.close()
        page.doModal()

if __name__ == '__main__':
    if sys.argv[1] == 'page1':
        Clientpage1().doModal()

