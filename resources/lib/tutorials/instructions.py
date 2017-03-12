#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Tnds82
# email: tndsrepo@gmail.com
# This program is free software: GNU General Public License
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import xbmcaddon, xbmcgui, xbmc, pyxbmct, os

addon             = xbmcaddon.Addon(id='script.tvhwizard')
addonname         = addon.getAddonInfo('name')
addonfolder       = addon.getAddonInfo('path')
artsfolder        = '/resources/img/tutorials'

pyxbmct.skin.estuary = True

class Tvwpage11(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Instructions (Page 8)'):
        """Class constructor"""
        super(Tvwpage11, self).__init__(title)
        self.setGeometry(1000, 680, 10, 5)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhwizard11.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=5)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 5)
        self.textbox.setText("[COLOR FF2a7a95]Addon Instructions:[/COLOR] Acesso às instruções do Addon\n"
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvwpage10()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=5)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.previous_button)
        self.previous_button.controlDown(self.close_button)
        self.setFocus(self.previous_button)

    def page(self, page):
        self.close()
        page.doModal()
		
class Tvwpage10(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Instructions (Page 7)'):
        """Class constructor"""
        super(Tvwpage10, self).__init__(title)
        self.setGeometry(1000, 680, 10, 5)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhwizard10.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=5)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 5)
        self.textbox.setText("[COLOR FF2a7a95]Update Channels /IP:[/COLOR] Permite activar a função de actualização das listas de canais e do IP\n"
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvwpage9()))
        self.instructions_button = pyxbmct.Button('Instructions')
        self.placeControl(self.instructions_button, 8, 2)
        self.connect(self.instructions_button, lambda: self.update())
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 4)
        self.connect(self.next_button, lambda: self.page(Tvwpage11()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=5)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.instructions_button)
        self.next_button.controlLeft(self.instructions_button)
        self.next_button.controlDown(self.close_button)
        self.previous_button.controlRight(self.instructions_button)
        self.previous_button.controlDown(self.close_button)
        self.instructions_button.controlDown(self.close_button)
        self.instructions_button.controlLeft(self.previous_button)
        self.instructions_button.controlRight(self.next_button)		
        self.setFocus(self.instructions_button)

    def page(self, page):
        self.close()
        page.doModal()
		
    def update(self):
        from update import Updatepage1
        Updatepage1().doModal()

class Tvwpage9(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Instructions (Page 6)'):
        """Class constructor"""
        super(Tvwpage9, self).__init__(title)
        self.setGeometry(1000, 680, 10, 5)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhwizard9.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=5)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 5)
        self.textbox.setText("[COLOR FF2a7a95]Manage Groups:[/COLOR] Permite fazer a gestão de grupos de canais no Kodi\n"
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvwpage8()))
        self.instructions_button = pyxbmct.Button('Instructions')
        self.placeControl(self.instructions_button, 8, 2)
        self.connect(self.instructions_button, lambda: self.gmanager())
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 4)
        self.connect(self.next_button, lambda: self.page(Tvwpage10()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=5)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.instructions_button)
        self.next_button.controlLeft(self.instructions_button)
        self.next_button.controlDown(self.close_button)
        self.previous_button.controlRight(self.instructions_button)
        self.previous_button.controlDown(self.close_button)
        self.instructions_button.controlDown(self.close_button)
        self.instructions_button.controlLeft(self.previous_button)
        self.instructions_button.controlRight(self.next_button)		
        self.setFocus(self.instructions_button)

    def page(self, page):
        self.close()
        page.doModal()

    def gmanager(self):
        from gmanager import Gmanager1
        Gmanager1().doModal()

class Tvwpage8(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Instructions (Page 5)'):
        """Class constructor"""
        super(Tvwpage8, self).__init__(title)
        self.setGeometry(1000, 680, 10, 5)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhwizard8.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=5)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 5)
        self.textbox.setText("[COLOR FF2a7a95]Manage Channels:[/COLOR] Permite fazer a gestão de canais no Kodi\n"
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvwpage5()))
        self.instructions_button = pyxbmct.Button('Instructions')
        self.placeControl(self.instructions_button, 8, 2)
        self.connect(self.instructions_button, lambda: self.cmanager())
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 4)
        self.connect(self.next_button, lambda: self.page(Tvwpage9()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=5)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.instructions_button)
        self.next_button.controlLeft(self.instructions_button)
        self.next_button.controlDown(self.close_button)
        self.previous_button.controlRight(self.instructions_button)
        self.previous_button.controlDown(self.close_button)
        self.instructions_button.controlDown(self.close_button)
        self.instructions_button.controlLeft(self.previous_button)
        self.instructions_button.controlRight(self.next_button)		
        self.setFocus(self.instructions_button)

    def page(self, page):
        self.close()
        page.doModal()

    def cmanager(self):
        from cmanager import Cmanager1
        Cmanager1().doModal()

class Tvwpage7(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Instructions Parental Lock Menu (Page 1)'):
        """Class constructor"""
        super(Tvwpage7, self).__init__(title)
        self.setGeometry(1000, 680, 10, 5)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhwizard7.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=5)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 5)
        self.textbox.setText("[COLOR FF2a7a95]Channels Lock:[/COLOR] Permite criar um pin lock de acesso a canais que posteriormente serão activados o controlo parental no Channel Manager\n"
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvwpage6()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=5)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.previous_button)
        self.previous_button.controlDown(self.close_button)
        self.setFocus(self.previous_button)

    def page(self, page):
        self.close()
        page.doModal()

class Tvwpage6(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Instructions Parental Lock Menu (Page 1)'):
        """Class constructor"""
        super(Tvwpage6, self).__init__(title)
        self.setGeometry(1000, 680, 10, 5)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhwizard6.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=5)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 5)
        self.textbox.setText("[COLOR FF2a7a95]Addon Lock:[/COLOR] Permite criar uma password de acesso ao addon Tvhwizard, para quem não quiser que o addon seja alterado por terceiros\n"
                             "\n"
							 "\n"
                             "")
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 4)
        self.connect(self.next_button, lambda: self.page(Tvwpage7()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=5)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.next_button)
        self.next_button.controlDown(self.close_button)		
        self.setFocus(self.next_button)

    def page(self, page):
        self.close()
        page.doModal()

class Tvwpage5(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Instructions (Page 4)'):
        """Class constructor"""
        super(Tvwpage5, self).__init__(title)
        self.setGeometry(1000, 680, 10, 5)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhwizard5.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=5)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 5)
        self.textbox.setText("[COLOR FF2a7a95]Parental Lock Menu:[/COLOR] Acesso ao menu de bloqueio parental, onde teremos dois tipos de Lock\n"
                             "Bloqueio de acesso ao Addon Tvhwizard e Bloqueio Parental de acesso a canais que posteriormente se activa\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvwpage4()))
        self.lock_button = pyxbmct.Button('Menu Lock')
        self.placeControl(self.lock_button, 8, 2)
        self.connect(self.lock_button, lambda: self.lock(Tvwpage6()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 4)
        self.connect(self.next_button, lambda: self.page(Tvwpage8()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=5)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.lock_button)
        self.next_button.controlLeft(self.lock_button)
        self.next_button.controlDown(self.close_button)
        self.previous_button.controlRight(self.lock_button)
        self.previous_button.controlDown(self.close_button)
        self.lock_button.controlDown(self.close_button)
        self.lock_button.controlLeft(self.previous_button)
        self.lock_button.controlRight(self.next_button)		
        self.setFocus(self.lock_button)

    def page(self, page):
        self.close()
        page.doModal()

    def lock(self, page):
        page.doModal()

class Tvwpage4(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Instructions (Page 3)'):
        """Class constructor"""
        super(Tvwpage4, self).__init__(title)
        self.setGeometry(1000, 680, 10, 5)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhwizard4.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=5)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 5)
        self.textbox.setText("[COLOR FF2a7a95]Reboot System:[/COLOR] Atalho para reiniciar o LibreELEC, aconselhado ao finalizar o Config OSCam e o Config TvHeadend\n"
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvwpage2()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 4)
        self.connect(self.next_button, lambda: self.page(Tvwpage5()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=5)
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

class Tvwpage3(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Instructions Tvh Client or Server'):
        """Class constructor"""
        super(Tvwpage3, self).__init__(title)
        self.setGeometry(1000, 680, 10, 5)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhwizard3.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=5)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 5)
        self.textbox.setText("[COLOR FF2a7a95]Config Tvheadend:[/COLOR] Vamos escolher se é para configurar o Cliente ou o Servidor\n"
                             "Cliente: Serve apenas para configurar o Kodi como cliente em uma box sem tuner ((ex: Wetek Core)\n"
							 "Servidor: Serve para configurar o Tvheadend e o Cliente numa box com tuner (ex: Wetek Play)\n"
                             "")
        self.client_button = pyxbmct.Button('Client')
        self.placeControl(self.client_button, 8, 1)
        self.connect(self.client_button, lambda: self.client())
        self.server_button = pyxbmct.Button('Server')
        self.placeControl(self.server_button, 8, 3)
        self.connect(self.server_button, lambda: self.server())
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=5)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.server_button)
        self.client_button.controlDown(self.close_button)
        self.client_button.controlRight(self.server_button)
        self.server_button.controlLeft(self.client_button)
        self.server_button.controlDown(self.close_button)		
        self.setFocus(self.server_button)

    def client(self):
        from client import Clientpage1
        Clientpage1().doModal()

    def server(self):
        from tvh import Tvhpage1
        Tvhpage1().doModal()

class Tvwpage2(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Instructions (Page 2)'):
        """Class constructor"""
        super(Tvwpage2, self).__init__(title)
        self.setGeometry(1000, 680, 10, 5)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhwizard2.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=5)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 5)
        self.textbox.setText("[COLOR FF2a7a95]Config Tvheadend:[/COLOR] Permite configurar o Tvheadend\n"
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvwpage1()))
        self.instructions_button = pyxbmct.Button('Instructions')
        self.placeControl(self.instructions_button, 8, 2)
        self.connect(self.instructions_button, lambda: self.tvh(Tvwpage3()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 4)
        self.connect(self.next_button, lambda: self.page(Tvwpage4()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=5)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.instructions_button)
        self.next_button.controlLeft(self.instructions_button)
        self.next_button.controlDown(self.close_button)
        self.previous_button.controlRight(self.instructions_button)
        self.previous_button.controlDown(self.close_button)
        self.instructions_button.controlDown(self.close_button)
        self.instructions_button.controlLeft(self.previous_button)
        self.instructions_button.controlRight(self.next_button)		
        self.setFocus(self.instructions_button)

    def page(self, page):
        self.close()
        page.doModal()

    def tvh(self, page):
        page.doModal()

class Tvwpage1(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Instructions (Page 1)'):
        """Class constructor"""
        super(Tvwpage1, self).__init__(title)
        self.setGeometry(1000, 680, 10, 5)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvhwizard1.png')
        self.placeControl(image, 0, 0, rowspan=7, columnspan=5)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 7, 0, 10, 5)
        self.textbox.setText("[COLOR FF2a7a95]Config OSCam:[/COLOR] Permite configurar o OSCam\n"
                             "\n"
							 "\n"
                             "")
        self.instructions_button = pyxbmct.Button('Instructions')
        self.placeControl(self.instructions_button, 8, 2)
        self.connect(self.instructions_button, lambda: self.oscam())
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 4)
        self.connect(self.next_button, lambda: self.page(Tvwpage2()))
        self.close_button = pyxbmct.Button('Close')
        self.placeControl(self.close_button, 9, 0, rowspan=1, columnspan=5)
        self.connect(self.close_button, self.close)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""
        self.close_button.controlUp(self.instructions_button)
        self.next_button.controlLeft(self.instructions_button)
        self.next_button.controlDown(self.close_button)
        self.instructions_button.controlDown(self.close_button)
        self.instructions_button.controlRight(self.next_button)		
        self.setFocus(self.instructions_button)

    def page(self, page):
        self.close()
        page.doModal()

    def oscam(self):
        from oscam import OSCampage1
        OSCampage1().doModal()

if __name__ == '__main__':
    if sys.argv[1] == 'page1':
        Tvwpage1().doModal()

