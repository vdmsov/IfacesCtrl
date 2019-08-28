#!/usr/bin/python

from IfacesCtrl import IfacesCtrl


ifaces = IfacesCtrl()

ifaces.get_interfaces()

packet_loss = ifaces.check_ping(ifaces.ifaces[1], 1, 1)