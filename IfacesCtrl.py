import os
import re
import subprocess as sp
import time
import netifaces as ni

# for test
import inspect

class IfacesCtrl:


	ifaces = []
	
	def __init__ (self):

		print("=== IfacesCtrl object is created ===\n")

	
	def get_interfaces (self):

		self.func_name()

		process = sp.Popen(['ip', 'addr', 'show'], stdout=sp.PIPE)
		stdout = process.communicate()[0]

		temp = re.split('[ :\n]+',stdout)
		temp = [i for i in temp if i]

		for n, l in enumerate(temp):
			if l[0] == '<':
				self.ifaces.append(temp[n-1])

		self.ifaces.remove('lo')

		print('ifaces = ')
		for i, val in enumerate(self.ifaces):
			print(str(i) + ': ' + str(val))
		

	def get_default (self):
		self.func_name()
	

	def set_default (self):
		self.func_name()
	

	def get_gateway (self):
		self.func_name()

	
	def check_ping (self, dev, amount, wait):

		self.func_name()

		process = sp.Popen(["""ping -I """ + str(dev) + \
			""" -c""" + str(amount) + \
			""" -q -nW""" + str(wait) + \
			""" 8.8.8.8 | grep loss | awk '{print $(NF-4)}' | cut -d"%" -f1"""], \
			stdout=sp.PIPE, shell = True)

		packet_loss = process.communicate()[0]

		print('packet loss = ')
		print(packet_loss)
		return packet_loss

	
	def reboot_network (self):	
		self.func_name()

	
	def up_link (self):
		self.func_name()

	
	def down_link (self):
		self.func_name()

	
	def check_static_ip (self):
		self.func_name()

	
	def arp_request (self):
		self.func_name()

	
	def get_arp_gateway (self):
		self.func_name()

#======================== FOR TEST =================================
	
	def func_name (self):
		print('\n>>> '  +  str(inspect.stack()[1][3]) + '()\n')


# get ip address
# netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']

# gws = netifaces.gateways()
# gws['default'][netifaces.AF_INET]
# netifaces.gateways()['default'][netifaces.AF_INET]
# netifaces.gateways()['default'][netifaces.AF_INET][0] - gateway
# netifaces.gateways()['default'][netifaces.AF_INET][1] - interface name



