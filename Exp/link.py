#!/usr/bin/python
import subprocess, re, time, os

process = subprocess.Popen(["ifconfig", "-a"], stdout=subprocess.PIPE)
stdout = process.communicate()[0]
all_link = re.split("[ \n]+",stdout)
all_link = [x for x in all_link if x]

link = []

for n, l in enumerate(all_link):
	if l == "Link": link.append(all_link[n-1])

link.remove('lo')
print link

for l in link:
	subprocess.call(["ip", "link", "set", l, "down"], stdout=subprocess.PIPE)

link_ok = []

for l in link:

	print l
	#print "dhclient"
	#subprocess.call(["dhclient", l], stdout=subprocess.PIPE)
	#print "ip set up"
	subprocess.call(["ip", "link", "set", l, "up"])
	subprocess.call(["dhclient", l], stdout=subprocess.PIPE)
	p = subprocess.call(["ping", "-c", "1", "-nW", "1", "8.8.8.8"])	
	print p
	if p==0:
		link_ok.append(l)

	print '=============================='
	print link_ok
	print '=============================='

if len(link_ok) > 0:
	subprocess.call(["ip", "link", "set", link_ok[0], "up"])
	
	print link_ok[0] + ' is connected'



