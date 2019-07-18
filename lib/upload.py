#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2018-present Tnds82 (https://addons.tnds82.xyz)

import xbmc, xbmcgui, xbmcaddon, os, shutil
import subprocess, zipfile, tools, smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders


dialog = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()

	##### ADDON TVH WIZARD by Tnds #####
addon       = xbmcaddon.Addon(id='script.tvhwizard')
addonname   = addon.getAddonInfo('name')
addonfolder = addon.getAddonInfo('path')
addonicon   = os.path.join(addonfolder, 'resources/icon.png')
addondata   = xbmc.translatePath(addon.getAddonInfo('profile'))
addonupload = os.path.join(addondata, 'upload/')

	##### ADDON SERVICE TVHEADEND #####
addontvh         = xbmcaddon.Addon(id='service.tvheadend42')
addontvhname     = addontvh.getAddonInfo('name')
addontvhfolder   = addontvh.getAddonInfo('path')
addontvhdata     = xbmc.translatePath(addontvh.getAddonInfo('profile'))
addontvhchannels = os.path.join(addontvhdata, 'channel')
addontvhnetworks = os.path.join(addontvhdata, 'input/dvb/networks')
addontvhpicons   = os.path.join("/storage/picons/vdr")

def langString(id):
	return addon.getLocalizedString(id)

def writeLog(message, level=xbmc.LOGDEBUG):
    xbmc.log('[%s %s] %s' % (xbmcaddon.Addon().getAddonInfo('id'),
                             xbmcaddon.Addon().getAddonInfo('version'),
                             message), level)

class Upload():

	def __init__(self):
		if os.path.exists(addonupload):
			shutil.rmtree(addonupload)
		if not os.path.exists(addonupload):
			os.makedirs(addonupload)
		self.compress_channels('%s%s' % (addonupload, 'channel.zip'), addontvhchannels)
		self.compress_channels('%s%s' % (addonupload, 'networks.zip'), addontvhnetworks)
		self.compress_channels('%s%s' % (addonupload, 'picons.zip'), addontvhpicons)
		self.send_mail()

	def compress_channels(self, zipname, path):
			zipf = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
			tools.compress(path, zipf)
			zipf.close()

	def send_mail(self):
		#Set up crap for the attachments
		filenames = [os.path.join(addonupload, f) for f in os.listdir(addonupload)]

		#Set up users for email
		recipients = ['addons@tnds82.xyz']

		#send it
		if tools.return_data('TVHWIZARD', 'STRING', 'nos', 2) == 1:
			if tools.return_data('TVHWIZARD', 'STRING', 'tvhwosc', 2) == 1:
				self.mail(recipients, "Lista de Canais Nos", "Lista de Canais Nos", filenames)
				self.finish(50042)
			else:
				self.mail(recipients, "Lista de Canais Nos(free)", "Lista de Canais Nos(free)", filenames)
				self.finish(50042)
		if tools.return_data('TVHWIZARD', 'STRING', 'nowo', 2) == 1:
			self.mail(recipients, "Lista de Canais Nowo", "Lista de Canais Nowo", filenames)
			self.finish(50043)
		if tools.return_data('TVHWIZARD', 'STRING', 'hispasat', 2) == 1:
			self.mail(recipients, "Lista de Canais Hispasat", "Lista de Canais Hispasat", filenames)
			self.finish(50044)
		if tools.return_data('TVHWIZARD', 'STRING', 'astra', 2) == 1:
			self.mail(recipients, "Lista de Canais Astra", "Lista de Canais Astra", filenames)
			self.finish(50045)
		if tools.return_data('TVHWIZARD', 'STRING', 'hotbird', 2) == 1:
			self.mail(recipients, "Lista de Canais Hotbird", "Lista de Canais Hotbird", filenames)
			self.finish(50046)
		if tools.return_data('TVHWIZARD', 'STRING', 'tdt', 2) == 1:
			self.mail(recipients, "Lista de Canais Tdt", "Lista de Canais Tdt", filenames)
			self.finish(50047)
		if tools.return_data('TVHWIZARD', 'STRING', 'meo', 2) == 1:
			self.mail(recipients, "Lista de Canais Meo", "Lista de Canais Meo", filenames)
			self.finish(50048)
		if tools.return_data('TVHWIZARD', 'STRING', 'vodafone', 2) == 1:
			self.mail(recipients, "Lista de Canais Vodafone", "Lista de Canais Vodafone", filenames)
			self.finish(50049)
		if tools.return_data('TVHWIZARD', 'STRING', 'net', 2) == 1:
			self.mail(recipients, "Lista de Canais Net", "Lista de Canais Net", filenames)
			self.finish(50050)
		if tools.return_data('TVHWIZARD', 'STRING', 'clarotv', 2) == 1:
			self.mail(recipients, "Lista de Canais Clarotv", "Lista de Canais Clarotv", filenames)
			self.finish(50051)

	#Create Module
	def mail(self, to, subject, text, attach):
		#Set up users for email
		gmail_user = "tndsrepo@gmail.com"
		gmail_pwd = "svigqlyqmqqurqav"

		msg = MIMEMultipart()
		msg['From'] = gmail_user
		msg['To'] = ", ".join(to)
		msg['Subject'] = subject

		msg.attach(MIMEText(text))

		#get all the attachments
		for file in attach:
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(open(file, 'rb').read())
			Encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
			msg.attach(part)

		mailServer = smtplib.SMTP("smtp.gmail.com", 587)
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(gmail_user, gmail_pwd)
		mailServer.sendmail(gmail_user, to, msg.as_string())
		# Should be mailServer.quit(), but that crashes...
		mailServer.close()

	def finish(self, list):
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, langString(list), 5000, addonicon))
		writeLog("Email successfully sent", xbmc.LOGNOTICE)