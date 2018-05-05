import random
import dns.reversename
import argparse

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
		print "DNS Result : {0}".format(n)
	else:
		print "DNS Failed" 

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Identify services on the internet.')
	parser.add_argument('--dns', action='store_const', const=True, help='resolve DNS query')
	parser.add_argument('--port', metavar='p', type=str, nargs='?', help='set static ip')
	args = parser.parse_args()

	ip,port = generate_ip_port(args.port)
	print "{0}[:{1}]".format(ip,port) 

	if args.dns:
		dns = get_dns(ip)


	