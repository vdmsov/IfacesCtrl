import os
import re
import subprocess as sp
import time
import netifaces as ni

# for test
import inspect

#-------------------------------------------------------------------------------

class IfacesCtrl:


	iface = []

#-------------------------------------------------------------------------------

	def __init__ (self):

		print("=== IfacesCtrl object is created ===\n")

#-------------------------------------------------------------------------------

	def get_interfaces (self):

		self.func_name()

		process = sp.Popen(['ip addr show'], stdout=sp.PIPE, shell = True)
		stdout = process.communicate()[0]

		temp = re.split('[ :\n]+',stdout)
		temp = [i for i in temp if i]

		for n, l in enumerate(temp):
			if l[0] == '<':
				self.iface.append(temp[n-1])

		self.iface.remove('lo')
		
#-------------------------------------------------------------------------------

	def get_default (self, iface_name):
		self.func_name()
		
		process = sp.Popen(['ip route show | grep default | grep ' + str(iface_name)], \
			stdout=sp.PIPE, shell = True)

		stdout = process.communicate()[0]

		temp = re.split('[ ]+',stdout)


		if temp[0] == 'default':
			return True
		else:
			return False

#-------------------------------------------------------------------------------

	def set_default (self):
		self.func_name()
	
#-------------------------------------------------------------------------------

	def get_gateway (self):
		self.func_name()

#-------------------------------------------------------------------------------
	
	def check_ping (self, iface_name, amount, wait):

		self.func_name()

		process = sp.Popen(["""ping -I """ + str(iface_name) + \
			""" -c""" + str(amount) + \
			""" -q -nW""" + str(wait) + \
			""" 8.8.8.8 | grep loss | awk '{print $(NF-4)}' | cut -d"%" -f1"""], \
			stdout=sp.PIPE, shell = True)

		packet_loss = process.communicate()[0]

		if packet_loss >= 0:
			return packet_loss
		else:
			return 100		

#-------------------------------------------------------------------------------
	
	def reboot_network (self):	
		self.func_name()

#-------------------------------------------------------------------------------
	
	def up_link (self, iface_name):
		self.func_name()

		sp.Popen(['ip link set ' + str(iface_name) + ' up'], \
			stdout=sp.PIPE, shell = True)

		print('Interface is Up', iface_name)

#-------------------------------------------------------------------------------

	def down_link (self, iface_name):
		self.func_name()

		sp.Popen(['ip link set ' + str(iface_name) + ' down'], \
			stdout=sp.PIPE, shell = True)

		print('Interface is Down', iface_name)

#-------------------------------------------------------------------------------

	def check_static_ip (self):
		self.func_name()

#-------------------------------------------------------------------------------
	
	def arp_request (self):
		self.func_name()

#-------------------------------------------------------------------------------
	
	def get_arp_gateway (self):
		self.func_name()

#-------------------------------------------------------------------------------

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



