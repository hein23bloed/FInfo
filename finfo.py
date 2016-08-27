#!/usr/bin/python3.5

import os, sys, time, errno, getopt, pwd, grp
from stat import * 

_version = "v0.03"

def read_write(fn):
	if os.access(fn, os.R_OK):
		print ("read: \t ok")
	else:
		print ("read: \t no")
	if os.access(fn, os.W_OK):
		print ("write: \t ok")
	else:
		print ("write: \t no")

def fsize(filesize):
	if filesize < 1000:
		result = (str(filesize) + "Bytes")
		return result	
	elif filesize <= 1000000:
		result = (str(round(float(filesize) / 1024, 2)) + "KB")
		return result
	elif filesize <= 1000000000:
		result = (str(round(float(filesize) / (1024*1024), 2)) + "MB")
		return result
	elif filesize <= 1000000000000:
		result = (str(round(float(filesize) / (1024*1024*1024), 2)) + "GB")
		return result
	elif filesize <= 1000000000000000:
		result = (str(round(float(filesize) / (1024*1024*1024*1024), 2)) + "TB")
		return result
	
def finfo(fn, fp):
	print ("\n")
	print ("path: \t", os.path.dirname(os.path.abspath(fn)))
	(p, f) = os.path.split(fn)
	print ("name: \t", f)	
	print ("size: \t", fsize(fp[ST_SIZE]))
	print ("owner: \t", pwd.getpwuid(fp[ST_UID]).pw_name)
	print ("group: \t", grp.getgrgid(fp[ST_GID]).gr_name)
	read_write(fn)	
	print ("access: ", time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(fp[ST_ATIME])))
	print ("changed:", time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(fp[ST_MTIME])))
	print ("meta: \t", time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(fp[ST_CTIME])))
	print ("\n")

def exist(filename):
	try:
		fp = os.stat(filename)
	except IOError as e:
		print ("********************************************")
		print ("* I/O-Error({0}): {1} *".format(e.errno, e.strerror))
		print ("********************************************")
		sys.exit()
	else:
		return fp

def usage():
	print ("Usage: finfo [-vh] <file/directory> <file/directory>")
			

def main(argv):
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hv", ["help", "version"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print (str(err)) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	if len(sys.argv)<=1:
		usage()
		sys.exit()
	elif len(sys.argv)==2:
		usage()
		sys.exit()
	elif len(sys.argv)>4:
		usage()
		sys.exit(2)
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-v", "--version"):
			print (_version)
			sys.exit()
	else:
		finfo(sys.argv[1], exist(sys.argv[1]))	
		
if __name__ == "__main__":
	main(sys.argv[1:])
