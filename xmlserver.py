#!/usr/bin/python
#XML remote connector(version 1.0)-Python based xml server for remote services
# Copyright (C) 2015 Shubham Dubey
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

#Xml based server to serve for many remote tasks


#XMLremote connector use xmlrpclib and SimpleXMLRPCServer
#(apt: python-imaging, web: <http://svn.python.org/projects/python/trunk/Lib/SimpleXMLRPCServer.py>).


from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib
import commands
from Crypto.Cipher import AES
#encryption is used for disguising data
#encoding is used for putting data in a specific format
import base64
import os

#funtion for encrypting the chat send

def encryption(privateInfo):
        #32 bytes = 256 bits
        #16 = 128 bits
        # the block size for cipher obj, can be 16 24 or 32. 16 matches 128 bit.
        BLOCK_SIZE = 16
        # the character used for padding
        # used to ensure that your value is always a multiple of BLOCK_SIZE
        PADDING = '{'
        # function to pad the functions. Lambda
        # is used for abstraction of functions.
        # basically, its a function, and you define it, followed by the param
	# followed by a colon,
        # ex = lambda x: x+5
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
        # encrypt with AES, encode with base64
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        
        secret = 'DS324^&&gghv#@xd'
        # creates the cipher obj using the key
        cipher = AES.new(secret)
        # encodes you private info!
        encoded = EncodeAES(cipher, privateInfo)
        return encoded

#funtion for decrypting the chat recievied

def decryption(encryptedString):
        PADDING = '{'
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        #Key is FROM the printout of 'secret' in encryption
        #below is the encryption.
        encryption = encryptedString
        key = 'DS324^&&gghv#@xd'
        cipher = AES.new(key)
        decoded = DecodeAES(cipher, encryption)
        return decoded


#some testing code
"""def cmd_copyin(data):
	if len(data)!=3:

		a="ERROR!\nExtra argument found!"
		return a
	server_file=data[1]
	client_location=data[2]
	try:
		a=len(os.listdir(server_file))
	except OSError:
		try:
			file_data=open(server_file,'rb')
		except IOError:
            		error_msg='7'
            		return error_msg
        	else:
        		file_data1=file_data.read()
			return file_data1
	else:
        	msg="ERROR!Directory transfer not avaliable!!"
	
        	return msg
"""


#function to copy from client to server
def cmd_copyout(data):
    
	server_file=data[1]
	file_data=''
	
	#data[2] to last will be the content of the data to sent
	for x in range(2,len(data)):
		file_data=file_data+' '+data[x]
	
	#to remove the blank space at starting
	file_data=file_data[1:]
	save_to=open(server_file,'wb')
	save_to.write(file_data)
	save_to.close()
	msg='File Sucessfully copied'
	return msg
	
	
#main connection handler starts here
def connection(x,filename=''):
        
        
        #this is for copyout operation
        if filename!='':
                with open(filename,'wb') as handle:
			handle.write(x.data)
			handle.close()
                
                return True
        
        else:
        
                data=x
                
                #to split the send data into list..ex: send hello-> data[2]=send data[1]=hello
                data=data.split(' ')
                if data[0]=='send':
                        z=data[1]
                        
                        m=decryption(z)
                        print '\033[1mMessage recieved:\033[0m'+m
                        msg=raw_input("Enter your message:")
                        
                        msg=encryption(msg)
                        return xmlrpclib.Binary(msg)
                
                #help text to display
                elif data[0]=='help' and len(data)==1:
                    
                        a='''	Syntax Help:
                                        ->help #to see this dialog
                                        ->send [message] #to send a message
                                        ->copyin dest1 dest2 #dest1(server file/folder),dest2(your system location)
                                        ->copout dest1 dest2 #dest1(your system file/folder),dest2(server's location)
                                        '''
                        
                        return str(a)
                    
                
                #copyin to copy from server to client
                elif data[0]=='copyin':
                        if len(data)!=3:
                            a="Invalid Syntax for copyin\ntry \033[31mhelp\033[0m for correct Syntax."
                            return a
                        
                        #to recieve the data of file
                        with open(data[1],'rb') as handle:
                                
                                return xmlrpclib.Binary(handle.read())
                
                                
                    
                #cd does'nt work with os.system
                elif data[0]=='cd':
                        os.chdir(data[1])
                        return 'Directory changed'	
                
                #connection checker to see if connected to server
                elif data[0]=='chk_conn':
                        print "\033[31mOne conection recieved..\033[0m"
                        
                        return '010'
                
                #to get the output of command entered
                else:
                        cmnd=commands.getoutput(x)
                        return xmlrpclib.Binary(cmnd)
            
def main():
        
        print "\033[1m\033[36mXML remote connector v-1.0\033[0m"
        print 
        print
        port=raw_input ("\033[36mEnter the port to listen on(default=9000):")
        if port=='':
                port=9000
            
	server = SimpleXMLRPCServer(('localhost', int(port)))
	print ("Listening on port %s...\033[0m" %port)
	print


	server.register_function(connection,'connection')
	try:
		print 'Use Ctrl^C to exit'
		server.serve_forever()
		
	#if connection closed
	except KeyboardInterrupt:
		print
		print 'Exiting the chat....BYE<>BYE'


if __name__=='__main__':
	main()
