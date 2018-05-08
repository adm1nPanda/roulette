import random
import dns.reversename
import argparse
import nmap
import socket
import threading
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# print bcolors.WARNING + + bcolors.ENDC

def generate_ip_port(static_port):
	ip = ""
	if static_port == None:
		port = str(random.randint(1024,65535))
	else:
		port = static_port

	for i in range(4):
		ip = ip + str(random.randint(0,255)) + "."
	ip = ip[:-1]

	return ip,port

def get_dns(ip):
	n = dns.reversename.from_address(ip)
	if  n != None:
		print bcolors.OKGREEN + "DNS Result : {0}".format(n) + bcolors.ENDC
	else:
		print bcolors.WARNING + "DNS Failed" + bcolors.ENDC

def check_tcp(ip, p):
	nm = nmap.PortScanner()
	nm.scan(hosts=ip, arguments='-n -sS -p'+p)
	
	for x in nm.all_hosts():
		if nm[x]['status']['state'] == "up" :
			return True
		else:
			return False


def thread(args,n):

	ip,port = generate_ip_port(args.port)
	print n

	if args.dns:
		dns = get_dns(ip)

	succ = check_tcp(ip, port)
	if args.open == True:
		if succ == True:
			print "{0}[:{1}]".format(ip,port) 
			print "TCP connection status - " + bcolors.OKGREEN + "Success" + bcolors.ENDC
	else:
		print "{0}[:{1}]".format(ip,port) 
		if succ == True:
			print "TCP connection status - " + bcolors.OKGREEN + "Success" + bcolors.ENDC
		else:
			print "TCP connection status - " + bcolors.FAIL + "FAIL" + bcolors.ENDC

	if succ == True and args.communicate == True:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(5.0)
		try:
			s.connect((ip, int(port)))
			data = s.recv(1024)
			if data != None:
				print "Recieved data - {0}".format(repr(data))
			s.close()
		except:
			print bcolors.OKBLUE + "Unable to connect using python sockets" + bcolors.ENDC


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Identify services on the internet.')
	parser.add_argument('--dns', action='store_const', const=True, help='resolve DNS query')
	parser.add_argument('--port', metavar='p', type=str, nargs='?', help='set static ip')
	parser.add_argument('--open', action='store_const', const=True, help='print only if port is OPEN')
	parser.add_argument('--loop', metavar='lp', type=int, nargs='?', default=1, help='Loop n times')
	parser.add_argument('--communicate', action='store_const', const=True, help='try to communicate with port if OPEN')

	args = parser.parse_args()

	for n in xrange(args.loop):
		threading.Thread(target=thread(args,n)).start()
