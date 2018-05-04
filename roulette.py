import random

ip = ""
port = str(random.randint(1024,65535))

for i in range(4):
	ip = ip + str(random.randint(0,255)) + "."

ip = ip[:-1]

print "ip and port - {0}:{1} ".format(ip,port)


