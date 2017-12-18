#!/bin/env python

from scapy.all import *
import sys, os, Queue, threading, signal, random

conf.verb = 0

def ip_printer(p):
	fp.write(p[IP].src + "\n")
	fp.flush()

def sig_handler(signum = signal.SIGUSR1, e = 0) :
	sys.exit()

class ScanThread(threading.Thread) :
	def run(self) :
		global queue
		ip_b = queue.get()
		for ip_c in range(0, 256) :
			for ip_d in range(0, 256) :
				target = "%s.%s.%s" % (ip_b, ip_c, ip_d)
				packet = (IP(dst = target)/TCP(sport = s_port, dport = d_port, flags="S"))
				send(packet)
		queue.task_done()

if __name__ == "__main__":
	ip_a = 10
	iface = "wlan0"
	d_port = 22
	#parse the input
	for i in range(1,len(sys.argv)):
		l = sys.argv[i].split('=')
		if l[0] == '-a':
			ip_a = l[1]
		elif l[0] == '-i':
			iface = l[1]
		elif l[0] == '-p' :
			d_port = (int)(l[1])

	target = ''
	s_port = random.randint(1025, 65536)
	print s_port

	fp = open("%s_%d_syn_list.txt" % (ip_a, d_port), "a")
	pid = os.fork()
	if pid == 0 :
		signal.signal(signal.SIGUSR1, sig_handler)
		sniff(iface=iface, filter='(tcp[tcpflags]=0x12) and (src port %s) and (dst port %d)' % (d_port, s_port), prn=ip_printer)
	else :	
		time.sleep(1)
		queue = Queue.Queue()
		target = []
		for ip_b in range(0, 256) :
			target.append('%s.%s' % (ip_a, ip_b))
		for ip_b in target :
			queue.put(ip_b)
		for p in range(len(target)) :
			ScanThread().start()

		queue.join()
		time.sleep(1)
		os.kill(pid, signal.SIGUSR1)
		fp.close()
		sys.exit()
