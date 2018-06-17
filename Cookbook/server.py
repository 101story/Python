#! /usr/bin/python3

# -*- coding: utf-8 -*-



from socket import *

from select import *

import sys

from time import ctime



HOST = ''

PORT = 10000

BUFSIZE = 1024

ADDR = (HOST,PORT)



serverSocket = socket(AF_INET, SOCK_STREAM)#1.소켓을 생성한다.



serverSocket.bind(ADDR) #2.소켓 주소 정보 할당

print('bind')

serverSocket.listen(100) #3.연결 수신 대기 상태

print('listen')

clientSocket, addr_info = serverSocket.accept() #4.연결 수락

print('accept')

clientSocket.close() #소켓 종료

serverSocket.close()

print('close')
