#!/usr/bin/python

from IfacesCtrl import IfacesCtrl


ifaces = IfacesCtrl()


ifaces.set_gateway('enp9s0')
ifaces.set_gateway('wlp8s0')

ifaces.get_default()

#ifaces.get_interfaces()

print('iface = ')
for i, val in enumerate(ifaces.iface):
	print(str(i) + ': ' + str(val))
	


packet_loss = ifaces.check_ping(ifaces.iface[1], 1, 1)

print('packet_loss = ', str(packet_loss))




#ifaces.down_link(ifaces.iface[1])
#
#ifaces.up_link(ifaces.iface[1])
#
#
#ifaces.add_default(ifaces.iface[1], '192.168.1.1')
#
#ifaces.restart_network()

gw_default = ifaces.get_gateway()

print(gw_default)

gw = ifaces.set_gateway('eth')

print(gw)

