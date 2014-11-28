"""DropBoxer

Usage: 
	dropboxcli.py <file> [, <file>]... [--folder=""]

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

app_key = 'xb7jnmhd5inuxcc'
app_secret = '6q11qbkg3vd2z8l'

class DropBoxCli():
	def __init__(self):
		''' guide for getting an authorize url '''
		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
		authorize_url = flow.start()
		
		''' guide for getting an authorize url '''
		sys.stdout.write("1. Go to: " + authorize_url + "\n")
		sys.stdout.write("2. Click 'Allow' (you might have to log in first) \n")
		sys.stdout.write("3. Copy the authorization code. \n")
		code = input("Enter the authorization code here: \n").strip()
		
		access_token, user_id = flow.finish(code)

		self.client = dropbox.client.DropboxClient(access_token)

		sys.stdout.write('linked account: \n')

		print(self.client.account_info())
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
	print(arguments)
	if arguments['<file>']:
		cli = DropBoxCli()
		cli.send_files(arguments['<file>'])

