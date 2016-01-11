XML Remote Connector (ver 1.0)
====================
XML Remote Connector - Copyright (C) 2015-2016 by Shubham Dubey <sdubey504@gmail.com>
    
    
    

    

XML Remote Connector is a remote server client application that can use for doing any simple task in remote server which is listening for some connection.
XML Remote Connector is developed in Python using SimpleXMLRPCServer and xmlrpclib.
The idea behind creating this program is that there is no popular tool that can give remote control on other system for executing commands with transferring file in parallel and also to send message.Although netcat is there for this but is none of them can be done at once and is not very friendly.So,here is this tool through which you can exec commands, send encrypted messages and tranferring file at same.
* Right now it is in  beginning phase but soon be ready to use in any enviorment. 

XML Remote Connector is an open source project and follows the philosophy of open standard, open design, open development and open management.it is born as a complete open source project and intended to build a sustainable ecosystem that benefits all contributors and users.
XML Remote Connector is developed by [Shubham Dubey](https://github.com/shubham0d/).

**Check out [Latest Release](https://github.com/shubham0d/XML_Remote-Connector/releasenotes.md).**


Highlights
-------------
* 1)Can work as replacement of ssh scp or netcat.
* -> Use as a simple chat application
* ->Can be use to copy file from one system to another.
* ->Use to exec remote commands.
* 2)Use AES encryption for sending and recieve messages.
* 3)Multiple connection supports on Server.
* 4)No extra installion required.
* 5)User friendly and simple to run



Requirements
------------
* the SimpleXMLRPCServer module needs to be installed (if not installed)
* the Crypto and xmlrpclib module needs to be present
* and of course python 2 have to be present


Installation
------------
just run 
* $sudo install.sh 

To start
--------
for server type this in your terminal
* $xmlserver 
* $xmlclient(for client)

Quick start
-----------
* Download the [latest stable code](https://github.com/shubham0d/XML-Remote-Connector/master)
* Clone repo `git clone git://github.com/shubham0d/XML-Remote-Connector`.
* GIT usage: [README GIT](README-GIT.md)

Known issues
------------

Please refer to the TODO file that has been shipped with XML Remote Connector.

*Thanks in advance for your feedback and contributions.
