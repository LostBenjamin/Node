#!/usr/bin/python

import krbV
import os
import socket
import shutil
import sys

def kadmin_local(command):
	ret = os.system("/usr/kerberos/sbin/kadmin.local -q '" + command + "'")
	if ret != 0:
		raise

def get_ip(hostname):
	return socket.gethostbyname(hostname)

if len(sys.argv) != 2:
	print "Usage: add_host_principal.py <hostname>"
	sys.exit(1)


default_realm = krbV.Context().default_realm

ipaddr = get_ip(sys.argv[1])

libvirt_princ = 'libvirt/' + sys.argv[1] + '@' + default_realm
outname = '/usr/share/ipa/html/' + ipaddr + '-libvirt.tab'

# here, generate the libvirt/ principle for this machine, necessary
# for taskomatic and host-browser
kadmin_local('addprinc -randkey +requires_preauth ' + libvirt_princ)
kadmin_local('ktadd -k ' + outname + ' ' + libvirt_princ)
