#!/usr/bin/python3.5

import os, sys, time, errno, getopt, pwd, grp
from stat import * 

_version = "v0.01_04"

def rw_access(fn):
	if os.access(fn, os.R_OK):
		print("read: \t ok")
	else:
		print("read: \t no")
	if os.access(fn, os.W_OK):
		print("write: \t ok")
	else:
		print("write: \t no")

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
	
def print_finfo(fn, fp):
	print("\n")
	print("path: \t", os.path.dirname(os.path.abspath(fn)))
	(p, f) = os.path.split(fn)
	print("name: \t", f)	
	print("size: \t", fsize(fp[ST_SIZE]))
	print("owner: \t", pwd.getpwuid(fp[ST_UID]).pw_name)
	print("group: \t", grp.getgrgid(fp[ST_GID]).gr_name)
	rw_access(fn)	
	print("access: ", time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(fp[ST_ATIME])))
	print("changed:", time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(fp[ST_MTIME])))
	print("\n")

def exist(filename):
	try:
		fp = os.stat(filename)
	except IOError as e:
		print("I/O-Error({0}) {2}: {1} ".format(e.errno, e.strerror, filename))
		sys.exit()
	else:
		return fp

def fcomp(fn1, fn2):
	exist(fn1)
	exist(fn2)
	print("compare")

def usage():
	print("Usage: finfo  <file/directory>")
	print("Usage: finfo -c --compare <file/directory> <file/directory>")
	print("Usage: finfo -vh --version --help")

			

def main(argv):
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvc", ["help", "version", "compare"])
	except getopt.GetoptError as err:		
		print (str(err)) 
		usage()
		sys.exit(2)
	if len(sys.argv)==0:
		usage()
		sys.exit()
	else:
		for o, a in opts:
			if o in ("-h", "--help"):
				usage()
				sys.exit()
			elif o in ("-v", "--version"):
				print (_version)
				sys.exit()
			elif o in ("-c", "--compare"):
				if len(sys.argv[3:])==0:
					usage()
					sys.exit()
				else:
					fcomp(sys.argv[2], sys.argv[3])
					sys.exit()
		else:
			if len(sys.argv)>2:
				usage()
			else:
				print_finfo(sys.argv[1], exist(sys.argv[1]))	
		
if __name__ == "__main__":
	main(sys.argv[1:])
