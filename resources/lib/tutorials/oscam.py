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


class OSCampage6(pyxbmct.AddonDialogWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(OSCampage6, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/oscam6.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("OSCam User: Serve para adicionar utilizadores a quem vao dar linhas\n"
		                     "Caso tenham activado o cccam, aqui vao criar os users, neste caso as linhas para outros\n"
                             "Users: Equipavale a cada linha que irão criar\n"
							 "Activar cada user e preencher o username e password")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(OSCampage5()))
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

class OSCampage5(pyxbmct.AddonDialogWindow):

    def __init__(self, title=''):
        """Class constructor"""
        super(OSCampage5, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/oscam5.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("OSCam Readers: Serve para adicionar as linhas que tem de acesso\n"
                             "Readers - Cada reader equivale a cada linha podem ser adicionadas até 5 readers\n"
                             "Enable Reader - Activar para adicionar linha\n"
							 "Protocol - Escolher o protocolo da linha, opcções - [COLOR lightblue]cccam[/COLOR] - [COLOR lightblue]newcamd[/COLOR] - [COLOR lightblue]cs357x[/COLOR]\n"
                             "Preencher os restantes dados solicitados")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(OSCampage4()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(OSCampage6()))
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

class OSCampage4(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - OSCam Instructions (Page 4)'):
        """Class constructor"""
        super(OSCampage4, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/oscam4.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("CCCam: Enable cccam - Activar apenas se forem criar utilizadores para usarem linhas criadas por voçes.\n"
                             "Caso activem a função cccam deverão escolher a porta de comunicação que desejarem\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(OSCampage3()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(OSCampage5()))
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

class OSCampage3(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - OSCam Instructions (Page 3)'):
        """Class constructor"""
        super(OSCampage3, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/oscam3.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("DVBapi: Configuração do DVBAPI.\n"
                             "Activar o DVBapi e de seguida escolher o Modo [COLOR red]Importante:[/COLOR] Se o modo não for escolhido não irá existir forma depois do Tvheadend comunicar\n"
                             "Modo pc-nodmx: utilizar caso desejem que a comunicação seja efectuada por camd.socket\n"
							 "Modo pc: utilizar caso desejem que a comunicação seja efectuada por TCP/IP")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(OSCampage2()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(OSCampage4()))
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

class OSCampage2(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - OSCam Instructions (Page 2)'):
        """Class constructor"""
        super(OSCampage2, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/oscam2.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("OSCam: Configuração de acesso ao Interface Web do OSCam.\n"
                             "Dados pré definidos são Username: [COLOR lightblue]oscam[/COLOR] Password: [COLOR lightblue]oscam[/COLOR] Porta: [COLOR lightblue]8888[/COLOR].\n"
                             "Os dados podem ser alterados à vossa escolha")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(OSCampage1()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(OSCampage3()))
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
		
class OSCampage1(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - OSCam Instructions (Page 1)'):
        """Class constructor"""
        super(OSCampage1, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/oscam1.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Addons: Addons necessários a configuração do OSCam.\n"
                             "Clicar para poder instalar o addon necessário\n"
							 "\n"
                             "[COLOR red]Nota:[/COLOR] Caso o addon já tenha sido instalado não clicar para instalar o addon")
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(OSCampage2()))
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
        OSCampage1().doModal()

