"""DropBoxer

Usage: 
	dropboxcli.py <file> [, <file>]... [--db-folder=""] [--config=""]

Options:
	<file> The path to the file you want to send to DropBox
	--user=<id>	User ID
	--password=<pwd> User Password
"""

from docopt import docopt, DocoptExit
import sys
import cmd
import os
import dropbox
import json

class DropBoxCli():
	def __init__(self, configPath):
		# configPath =  if configPath is None else configPath
		self.setConfigFilePath()
		self.startOAuth()

	def setConfigFilePath(self, path = None):
		''' Sets the path for config '''
		self.configPath = os.path.expanduser('~') + '/.dropBoxCliConfig'

	def checkConfigExists(self):
		''' Checks to see if the config is set and reads the config if it exists '''
		return True if os.path.isfile(self.configPath) else False

	def readConfigFile(self):
		try:
			f = open(self.configPath).read()
			configJSON = json.loads(f)
			if configJSON:
				return configJSON
			else:
				return False
		except IOError as ex:
			sys.stdout.write('There was a problem reading your config file...')
			return False

	def writeConfig(self, config):
		''' writes to the config if it isnt there '''
		try:
			f = open(self.configPath, 'w')
			f.write(config)
			f.close()
		except IOError as ex:
			sys.stdout.write('There was a problem writing your config...') 	
		return

	def createConfigFile(self):
		sys.stdout.write('To use this cli you must register an app. \n Go To: https://www.dropbox.com/developers/apps/create and create a Dropbox API app \n')
		self.app_key = input("Paste your app key here: \n").strip()
		self.app_secret = input("Paste your app secret here: \n").strip()
		
		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)
		authorize_url = flow.start()

		''' guide for getting an authorize url '''
		sys.stdout.write("1. Go to: " + authorize_url + "\n")
		sys.stdout.write("2. Click 'Allow' (you might have to log in first) \n")
		sys.stdout.write("3. Copy the authorization code. \n")
		
		''' get authorization code '''
		code = input("Enter the authorization code here: \n").strip()
		self.access_token, self.user_id = flow.finish(code)

		config = {
			'app_key': self.app_key,
			'app_secret': self.app_secret,
			'access_token': self.access_token,
			'user_id': self.user_id
		}
		
		config = json.dumps(config)
		self.writeConfig(config)
		return

	def startOAuth(self):
		if self.checkConfigExists() is False:
			config = self.createConfigFile()
		else:
			config = self.readConfigFile()
		''' get a client from config '''
		self.client = dropbox.client.DropboxClient(config['access_token'])

	def send_files(self, files):
		if isinstance(files, list):
			for file in files:
				f = open(file, 'rb')
				''' get the file name '''
				file_name = file.split('/')[-1]
				response = self.client.put_file('/' + file_name, f)	
				sys.stdout.write("file uploaded")
				sys.stdout.write(response)

		return


if __name__ == '__main__':
	arguments = docopt(__doc__, version='DropBoxer 1.0')
	cli = DropBoxCli(arguments['--config'])
	if arguments['<file>']:
		cli.send_files(arguments['<file>'])
