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

class Tvhpage13(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 13)'):
        """Class constructor"""
        super(Tvhpage13, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh13.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Timeshift: Permite activar o timeshift no Tvheadend\n"
		                     "Serve para fazer pausa na transmissão e continuar a ver a mesma\n"
                             "\n"
							 "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvhpage12()))
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

class Tvhpage12(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 12)'):
        """Class constructor"""
        super(Tvhpage12, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh12.png')
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
        self.connect(self.previous_button, lambda: self.page(Tvhpage11()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage13()))
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

class Tvhpage11(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 11)'):
        """Class constructor"""
        super(Tvhpage11, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh11.png')
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
        self.connect(self.previous_button, lambda: self.page(Tvhpage10()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage12()))
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
		
class Tvhpage10(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 10)'):
        """Class constructor"""
        super(Tvhpage10, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh10.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("PVR: Onde vamos configurar o cliente HTSP Tvheadend do Kodi\n"
                             'Activar o mesmo e colcoar o ip da box, podemos verificar o mesmo em [COLOR orange]"Click to see your IP"[/COLOR]\n'
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvhpage9()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage11()))
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
		
class Tvhpage9(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 9)'):
        """Class constructor"""
        super(Tvhpage9, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh9.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Recordings - Menu de configuração das gravaçoes\n"
                             "Activar caso desejem efectuar gravações de canais\n"
                             "Escolher o profile desejado. Profiles disponiveis [COLOR lightblue]Matroska(mkv)[/COLOR] - [COLOR lightblue]Pass-thru(pass)[/COLOR] - [COLOR lightblue]HTSP(htsp)[/COLOR]\n"
							 "Escolher o caminho onde desejam que sejam colocadas as gravações\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvhpage8()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage10()))
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

class Tvhpage8(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 8)'):
        """Class constructor"""
        super(Tvhpage8, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh8.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Softcam: Serve para permitir a ligação do Tvheadend ao OSCam\n"
                             "Activar o DVBapi, e de seguida muito importante escolher o Modo\n"
                             "Escolher o modo o conforme o que foi escolhido no OSCam Config, no modo pc colcoar o ip (podem verificar abaixo) e a porta ( porta escolhida no OSCam Config)\n"
                             "Caso o oscam esteja noutro equipamento o modo deverá ser o pc")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvhpage7()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage9()))
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

class Tvhpage7(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 7)'):
        """Class constructor"""
        super(Tvhpage7, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh7.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("DVB Inputs: Serve para activar as placas conforme o equipamento e o tipo de tuner (DVB-S e DVB-C)\n"
							 'Activar "Enable Adapters" e escolher o equipamento que tem, de seguida escolher o tuner conforme a lista de canais anteriormente escolhida\n'
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvhpage6()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage8()))
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

class Tvhpage6(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 6)'):
        """Class constructor"""
        super(Tvhpage6, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh6.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Picons: Activar para que sejam colocados os picons dos canais conforme a lista\n"
                             "Image Cache: Activar permite fazer o cache dos picons para serem mais rápidos\n"
                             "\n"
							 "\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvhpage5()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage7()))
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

class Tvhpage5(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 5)'):
        """Class constructor"""
        super(Tvhpage5, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh5.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("DVB-S: Escolher a lista de Satelite pretendida\n"
                             "\n"
                             "\n"
							 "[COLOR red]Nota:[/COLOR] São listas pré feitas e organizadas\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvhpage4()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage6()))
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

class Tvhpage4(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 4)'):
        """Class constructor"""
        super(Tvhpage4, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh4.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Channels: Deverão activar os canais para poderem escolher a lista pretendida\n"
                             "DVB-C: Escolher a lista de Cabo pretendida\n"
                             "\n"
							 "[COLOR red]Nota:[/COLOR] São listas pré feitas e organizadas\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvhpage3()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage5()))
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

class Tvhpage3(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 3)'):
        """Class constructor"""
        super(Tvhpage3, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh3.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("User: Permite criar um utilizador Admin e um Cliente (recomendado: caso tenham acesso externo)\n"
                             "Administrator: Escolher um username e uma password. (Acesso total à Interface Web\n"
							 "Client: Sempre que for criado um Admin este user deverá ficar [COLOR green]activado[/COLOR], não sendo obrigatório criar username nem password. (Apenas tem acesso a stream, sem acesso ao Interface Web. Será o login usado pelo Kodi)\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvhpage2()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage4()))
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

class Tvhpage2(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 2)'):
        """Class constructor"""
        super(Tvhpage2, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh2.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Configuration: Activar para se iniciar a configuração do Tvheadend 4.2\n"
                             "Activate Expert Mode: Activa o Expert Mode no Interface Web para se poder ver os CAs (opcional)\n"
                             "Web Interface Language: Serve para escolher qual a lingua do Interface Web (opcional)\n"
							 "EPG Language: Escolha da prioridade da linguagem do EPG, opções EN e PT. (opcional: podem ser escolhida uma ou as duas)\n"
                             "")
        self.previous_button = pyxbmct.Button('Previous')
        self.placeControl(self.previous_button, 8, 0)
        self.connect(self.previous_button, lambda: self.page(Tvhpage1()))
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage3()))
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
		
class Tvhpage1(pyxbmct.AddonDialogWindow):

    def __init__(self, title='Tvh Wizard by Tnds - Tvheadend Server Instructions (Page 1)'):
        """Class constructor"""
        super(Tvhpage1, self).__init__(title)
        self.setGeometry(1000, 680, 10, 4)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
		
    def set_controls(self):
        """Set up UI controls"""
        image = pyxbmct.Image(addonfolder+artsfolder+'/tvh1.png')
        self.placeControl(image, 0, 0, rowspan=6, columnspan=4)
        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 6, 0, 10, 4)
        self.textbox.setText("Addons: Addons necessários a configuração do Tvheadend Server.\n"
                             "Clicar para poder instalar o addon necessário\n"
							 "\n"
                             "[COLOR red]Nota:[/COLOR] Caso os addon já tenham sido instalados não clicar para instalar o addon")
        self.next_button = pyxbmct.Button('Next')
        self.placeControl(self.next_button, 8, 3)
        self.connect(self.next_button, lambda: self.page(Tvhpage2()))
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
        Tvhpage1().doModal()

