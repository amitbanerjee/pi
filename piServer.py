# -*- coding: utf-8 -*-
import socket
import sys
from thread import *
import Packages
import re

reload(sys)
sys.setdefaultencoding('utf-8') 

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8080 # Port Specified
	 
#Function for handling connections. This will be used to create threads
def clientthread(conn, myPacks):
	#Sending message to connected client
	#conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
	#infinite loop so that function do not terminate and thread do not end.
	while True:
		#Receiving from client
		try:
			data = conn.recv(4096).encode('utf-8')
		except:
			print "Don't handle non utf-8 chars"
			break
		cmds = data.split("|")
		if len(cmds) != 3:
			conn.sendall("ERROR\n")	
			print "ERROR in data"
			print data
			continue

		deps = ""
		pkg = ""
		cmd = cmds[0].strip()
		pkg = cmds[1].strip()
		reply = "ERROR\n"
		if len(cmds) == 3:
			deps = cmds[2].strip()
		if cmd == "INDEX":
			
			if not bool(re.match('^[.a-z0-9_-]+[+]*$', pkg, re.IGNORECASE)):
				reply = "ERROR\n"
				conn.sendall(reply)	
				#print pkg
				continue
		
			#print data
			ret = myPacks.index(pkg, deps)	
			if not ret:
				reply = "ERROR\n"
			else:
				reply = ret
		elif cmd == "REMOVE":
			ret = myPacks.remove(pkg)	
			if not ret:
				reply = "ERROR\n"
			else:
				reply = ret
			#print data + "|" + ret
			#myPacks.printPackage()
		elif cmd == "QUERY":
			ret = myPacks.query(pkg)	
			if not ret:
				reply = "ERROR\n"
			else:
				reply = ret
		elif cmd == "PRINT":
			reply = myPacks.printPackage()	
		else:
			reply = "ERROR\n"
		conn.sendall(reply)	
		
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
	myPacks = Packages.PackageList() 
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
