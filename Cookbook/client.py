#! /usr/bin/python3

# -*- coding: utf-8 -*-



from socket import *

from select import *

import sys

from time import ctime



HOST = '127.0.0.1'

PORT = 10000

BUFSIZE = 1024

ADDR = (HOST,PORT)



clientSocket = socket(AF_INET, SOCK_STREAM)#1 서버에 접속하기 위한 소켓을 생성한다.



try:

        clientSocket.connect(ADDR)#2. 서버에 접속을 시도한다.

except  Exception as e:

        print('%s:%s'%ADDR)

        sys.exit()

print('connect is success')
