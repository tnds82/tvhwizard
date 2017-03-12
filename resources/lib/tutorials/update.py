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

class Updatepage3(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Update Channels / IP Instructions (Page 3)'):
        """Class constructor"""
        super(Updatepage3, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/update3.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Update IP: Serve para quem muda a box de casa ou não usa ip fixo e por vezes o ip da box é alterado\n"
                             "Activando esta função sempre que a box é reiniciada é efectuada uma verificação do IP, caso seja diferente o addon altera o que necessita para que tudo possa voltar a funcionar e reinicia a box\n"
							 "[COLOR red]Nota:[/COLOR] Caso mudem a box de casa e seja ligação wi-fi devem primeiro configurar a ligação e depois reiniciar a box para que funcione")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Updatepage2()))
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
		
class Updatepage2(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Update Channels / IP Instructions (Page 2)'):
        """Class constructor"""
        super(Updatepage2, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/update2.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("DVB-S: Lista de Canais Satélite\n"
                             "\n"
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Updatepage1()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Updatepage3()))
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
		
class Updatepage1(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Update Channels / IP Instructions (Page 1)'):
        """Class constructor"""
        super(Updatepage1, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/update1.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Update Channels: Serve para actualizar as listas de canais e dos picons respectivos\n"
                             "Activar o update channels and picons. Sempre que reiniciam o equipamento o addon irá fazer uma verificação se existe uma lista nova. Se existir pergunta se querem fazer update\n"
							 "Escolher a lista que configuraram no Config Tvheadend Server\n"
                             "DVB-C: Lista de canais Cabo")
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Updatepage2()))
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
        Updatepage1().doModal()

