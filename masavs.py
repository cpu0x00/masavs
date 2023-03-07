'''
Author: Karim (github.com/cpu0x00) (twitter.com/fsociety_py00)

a script to create a vpn server on any given machine in 1 minute

(M)ake (A)ny (S)erver (A) (V)pn (S)erver
'''


import argparse
from os import getcwd
from os import system
import re
import paramiko 
import requests
from time import sleep


parser = argparse.ArgumentParser(epilog='(M)ake (A)ny (S)erver (A) (V)pn (S)erver')
parser.add_argument("--ip", required=True, help='the ip of the server')
parser.add_argument('--port', type=int,default=22,help='the port of ssh (defaut=22)')
parser.add_argument('--ssh_user', required=True,help='ssh username to use')
parser.add_argument('--ssh_passwd', help='ssh password to use')
parser.add_argument('--ssh_key', help='ssh private key to use instead of password')
parser.add_argument('--ssh_key_phrase', help='ssh private key passphrase to use with (--ssh_key)')


args = parser.parse_args()

OPENVPN_SETUP_SCRIPT = 'https://raw.githubusercontent.com/cpu0x00/bypassing-udp-vpn-restriction/main/openvpn-automated-install.sh'


def create_openvpn_as(): # creates openvpn access server on the droplet and retrieve the client profile to the local machine
	print('[*] creating openvpn access server on the vps (be patient...)')

	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	if args.ssh_key and args.ssh_key_phrase:
		ssh_idrsa = f'{getcwd()}/{args.ssh_key}' 
		ssh_client.connect(args.ip, port=args.port ,username=args.ssh_user, key_filename=ssh_idrsa, passphrase=args.ssh_key_phrase)

	if args.ssh_key:
		ssh_idrsa = f'{getcwd()}/{args.ssh_key}' 
		ssh_client.connect(args.ip, port=args.port ,username=args.ssh_user, key_filename=ssh_idrsa)

	if args.ssh_passwd:
		ssh_client.connect(args.ip, port=args.port ,username=args.ssh_user,password=args.ssh_passwd)



	stdin, stdout, stderr = ssh_client.exec_command(f'wget {OPENVPN_SETUP_SCRIPT} -O ~/openvpn-automated-install.sh')

	print('[*] downloaded the (openvpn-automated-install.sh) script to the vps')

	while not stdout.readlines() or stderr.readlines():
		sleep(0.2)
		if stdout.readlines() or stderr.readlines():
			break


	stdin, stdout, stderr = ssh_client.exec_command(f'chmod +x ~/openvpn-automated-install.sh')


	while not stdout.readlines() or stderr.readlines():
		sleep(0.1)
		if str(stdout.readlines()) == '[]' or str(stderr.readlines()) == '[]':
			break

	print('[*] executing the setup script in the vps...')

	stdin, stdout, stderr =  ssh_client.exec_command('/bin/bash ~/openvpn-automated-install.sh')


	while not stdout.readlines() or not stderr.readlines():
		sleep(0.1)
		if stdout.readlines() or stderr.readlines():
			break

	sftp_client = ssh_client.open_sftp()

	localpath = f'{getcwd()}/vps-openvpn-client.ovpn'

	if args.ssh_user == 'root':

		remotepath = '/root/vps-openvpn-client.ovpn'
	else:
		remotepath = f'/home/{args.ssh_user}/vps-openvpn-client.ovpn'

	print('[*] retrieving the (vps-openvpn-client.ovpn) client file')

	if sftp_client.get(remotepath,localpath):

		print('[*] done!')
	
	sftp_client.close()
	ssh_client.close()

	print('[INFO] to remove the openvpn-as from the machine run the (~/openvpn-automated-install.sh) on the machine and follow the instructions ')
	print('\n[FLEX] yep its that easy ;)')


create_openvpn_as()