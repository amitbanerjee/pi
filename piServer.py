# -*- coding: utf-8 -*-
import socket
import sys
from thread import *
import newPackage
import re

reload(sys)
sys.setdefaultencoding('utf-8')

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8080 # Port Specified
	 
#Function for handling connections. This will be used to create threads
def clientthread(conn, myPacks):
	#infinite loop so that function do not terminate and thread do not end.
	while True:
		#Receiving from client
		try:
			data = conn.recv(4096).encode('utf-8')
		except:
			print "Don't handle non utf-8 chars\n"
			break
		cmds = data.split("|")
		if len(cmds) != 3:
			try:
				conn.sendall("ERROR\n")	
			except:
				print "Dead connection"
				break
			continue

		cmd = cmds[0].strip()
		pkg = cmds[1].strip()
		deps = cmds[2].strip()

		if cmd == "INDEX":
			
			if not bool(re.match('^[.+a-z0-9_-]+$', pkg, re.IGNORECASE)):
				reply = "ERROR\n"
				try:
					conn.sendall(reply)	
				except:
					print "Dead connection"
					break
				print data
				continue
		
			ret = myPacks.index(pkg, deps)	
			reply = ret

		elif cmd == "REMOVE":
			ret = myPacks.remove(pkg)	
			reply = ret

		elif cmd == "QUERY":
			ret = myPacks.query(pkg)	
			reply = ret

		elif cmd == "PRINT":
			myPacks.printPackage()	
			reply = "OK\n"

		else:
			reply = "ERROR\n"


		#Now send the response back
		try:
			conn.sendall(reply)	
		except:
			print "Dead connection"
			break
		
	#came out of loop
	conn.close()

if __name__=='__main__':
	 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Socket created'
	 
	#Bind socket to local host and port
	try:
		s.bind((HOST, PORT))
	except socket.error as msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	     
	print 'Socket bind complete'
	myPacks = newPackage.PackageList() 
	#Start listening on socket
	s.listen(150)
	print 'Socket now listening'
	#now keep talking with the client
	while 1:
		#wait to accept a connection - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])

		#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientthread ,(conn,myPacks,))
	 
	s.close()
