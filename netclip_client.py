#!/usr/bin/python3.5

import socket, sys, time, os
from subprocess import call, Popen, PIPE

_CLP = ''

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
		print("Error sending Ping")
		return (0, s)
	
	reply = s.recv(1024).decode()
	if not reply == "Pong":
		return (0, s)
	else:
		print(time.strftime("%d.%m.%y %H:%M:%S ") + "Connected: " + host + ":" + port)
		data = "Ok"
		try:
			s.send(data.encode("iso-8859-1"))
			return (1, s)
		except socket.error as msg:
			print("Error sending Ok")
			return (0, s)
		
	
def readclb_linux():
	clb = Popen(["xclip", "-selection", "c", "-o"], stdout=PIPE)
	stdout, stderr = clb.communicate()
	return bytes.decode(stdout)	 

def pasteclb_linux(text):
    clb = Popen(['xclip', '-selection', 'c'], stdin=PIPE)
    try:
        clb.communicate(input=bytes(text, 'utf-8'))
    except TypeError:
        clb.communicate(input=bytes(text))   

def ifexist(clb):
	if not _CLP == clb:
		return 1
	else:
		return 0

def wglobal(gl):
	global _CLP
	_CLP = gl	

def sendclb(clb, sock):
	try:
		sock.send(clb.encode())
		return 1
	except socket.error as msg:
		print("Error sending Clibboard")
		return 0 

def main(argv):
	wglobal(readclb_linux())
	r, sock = cstart(sys.argv [1], sys.argv[2])
	if not r:	
		print("Not connected!")
		sys.exit()
	while 1:
		if ifexist(readclb_linux()): 
			print("n vorhanden")
			sendclb(readclb_linux(), sock)
			wglobal(readclb_linux())
		else:
			print("vorhanden")
	sock.close()
	sys.exit()	
if __name__ == "__main__":
	main(sys.argv[1:])
