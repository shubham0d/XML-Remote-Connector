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

'''Xml based server to serve for many purpose 


XMLremote connector use xmlrpclib and SimpleXMLRPCServer
(apt: python-imaging, web: <http://svn.python.org/projects/python/trunk/Lib/SimpleXMLRPCServer.py>).
'''























import xmlrpclib



from time import sleep
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



        # generate a randomized secret key with urandom
        secret = 'DS324^&&gghv#@xd'


        # creates the cipher obj using the key
        cipher = AES.new(secret)

        # encodes you private info!
        encoded = EncodeAES(cipher, privateInfo)
        return encoded





#function to decrypt the chat recieved
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


#funtion to check if connected to the server
def check_it(s):
        try:
                status=s.connection('chk_conn')

        #if nothing recieved and program exited 
        except:
                print
                
                print "\033[31m........!!!"
                sleep(3)
                print "\033[31mUnable to connect to server..\nEither connection not avaliable or Connection refuse..!!!\033[0m"
                exit()
        
        
        else:
                print "...."
                sleep(2)
                print "\033[35mConnection established!!"
                print "\033[35mhelp-> to get help text\033[0m"
                print
            
            
#main function to handle all request
def connection(s):
    while True:
            try:
                    msg=raw_input('\033[1m\033[31mEnter the command:\033[0m')
                    k=msg.split(' ')
                    
                    #'send msg' is entered as cmd
                    if k[0]=='send':
                            
                            #to combine the message to send
                            z=''
                            for x in range(1,len(k)):
                                    z=z+' '+k[x]
                            new_msg='send '+encryption(z)

                            
                            try:
                                    encrypted_msg=s.connection(new_msg).data
                            
                            
                            except xmlrpclib.Fault as err:
                                    print ("A fault occurred.Unable to display reply")
                                    print ("Fault code:%d" %err.faultCode)
                                    print ("Fault string:%s" %err.faultString)
                                    exit()
                            
                            except  xmlrpclib.ProtocolError as err:
                                    print ("Error Occured")
                                    print ("Unhandled Connection.Unable to fufill request")
                                    print ("Error message: %s" %err.errmsg)
                                    exit()



                            except:
                                    print "Unable to Complete request...Connection Closed"
                                    exit()


                            else:
                                    print "Msg send!"
                                    print "Waiting for reply.!!"
                                    pure_msg=decryption(encrypted_msg)
                                    print ("\033[1m\033[34mMessage recieved:\033[0m"+pure_msg)
                    
                    #to recieve help text
                    elif k[0]=='help' and len(k)==1:
                            print '\033[36m'+s.connection(msg)+'\033[0m'
                    
                    
                    #command start with copyin
                    elif k[0]=='copyin':

                            """file_data=s.connection(msg)
                            if file_data=='7':
                                    print "ERROR:File/Dir not found!"
                                    exit()
                            if file_data=='ERROR!Directory transfer not avaliable!!':
                                    print file_data
                                    exit
                            else:
                                    client_file=open(k[2],'wb')
                                    client_file.write(file_data)
                                    client_file.close()"""
                                    
                            #if extra argument given
                            if len(k)!=3:
                                    print "Invalid Syntax! Try \033[31mhelp\033[0m to see help message."
                                    print 
                                    
                            else:
                                    try:
                                            with open(k[2],'wb') as handle:
                                        
                                                    a=handle.write(s.connection(msg).data)
                                    
                                    except xmlrpclib.Fault as err:
                                            print ("A fault occurred.Unable to Complete request...!!")
                                            #print ("Fault code:%d" %err.faultCode)
                                            print ("Fault string:%s" %err.faultString)
                                            exit()
                                            
                                            
                                    except IOError:
                                            print "Unable to complete request...Path not exists...!!!"
                                            exit()
                                            
                                    else:    
                                            print "File Successfully Send!"
                                            exit()
                    
                    
                    #command start with copout
                    elif k[0]=='copyout':
                        
                            if len(k)!=3:
                                    print "Invalid Syntax! Try \033[31mhelp\033[0m to see help message."
                                    print
                            else:
                                
                                    '''my_file=k[1]
                                    server_file=k[2]
                                    file=open(my_file,'rb')
                                    file_data=file.read()
                                    file_data='copyout '+server_file+' '+file_data
                                    recieved=s.connection(file_data)
                                    print recieved'''
                                    with open(k[1],'rb') as handle:
                                            data=xmlrpclib.Binary(handle.read())
                                    
                                    
                                    #everything=k[0]+' '+k[2]+' '+data
                                    result=s.connection(data,k[2])
                                    if result==True:
                                            print "File Successfully Transfered!"

                    
                    
                    else:
                            print s.connection(msg)

            except KeyboardInterrupt:
                    print
                    print 'Exiting the chat....BYE<>BYE'
                    exit()








def main():
    
    print "\033[1m\033[36mXML remote connector v-1.0\033[0m"
    print 
    print
    
    ip=raw_input("\033[36mEnter the ip address of the server:")
    if ip=='':
	print "\033[31mPlese enter the valid IP address\nQuitting...\n \033[0m"
	quit()
    port=raw_input("Enter the listener port(default=9000):\033[0m")
    
    if port=='':
        port=9000
        
    s=xmlrpclib.ServerProxy('http://'+str(ip)+':'+str(port))
    check_it(s)
    connection(s)
    
    
    
if __name__=='__main__':
    main()
