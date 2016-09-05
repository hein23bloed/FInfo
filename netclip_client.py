#!/usr/bin/python3.5

import socket, sys, time, os
from subprocess import call, Popen, PIPE

def cstart(host, port):
	reply = ""
	data = "Ping" 

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		s.connect((host, int(port)))
	except socket.error as msg:
		print("Connection Error: " + str(msg))

	try:
		s.send(data.encode())
	except socket.error as msg:
		print("Error sending  Ping")
	
	reply = s.recv(1024).decode()
	if not reply in "Pong":
		return 0
	else:
		print(time.strftime("%d.%m.%y %H:%M:%S ") + "Connected: " + host + ":" + port)
		data = "Ok"
		try:
			s.send(data.encode("iso-8859-1"))
		except socket.error as msg:
			print("Error sending  Ping")
		return 1
	s.close

def readclb():
	p = Popen(["xclip", "-selection", "c", "-o"], stdout=PIPE)
	stdout, stderr = p.communicate()
	return bytes.decode(stdout)	            

def main(argv):
	if not cstart(sys.argv [1], sys.argv[2]):
		print("Not connected!")
		sys.exit()
	print(readclb())
		
		
if __name__ == "__main__":
	main(sys.argv[1:])
