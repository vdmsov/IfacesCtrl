#!/usr/bin/python

from IfacesCtrl import IfacesCtrl


ifaces = IfacesCtrl()



ifaces.get_interfaces()

print('iface = ')
for i, val in enumerate(ifaces.iface):
	print(str(i) + ': ' + str(val))
	


packet_loss = ifaces.check_ping(ifaces.iface[1], 1, 1)

print('packet_loss = ', str(packet_loss))



default = ifaces.get_default(ifaces.iface[1])

print('default: ', ifaces.iface[1], default)



ifaces.down_link(ifaces.iface[1])

ifaces.up_link(ifaces.iface[1])

