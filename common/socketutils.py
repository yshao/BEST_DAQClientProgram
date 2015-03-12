__author__ = 'Ping'

import socket
from socket import *

class Socket:
    def __init__(self):
        ""

    def connect(self,hostname,port=27015):
        self._hostname=hostname
        self._port=port
        print hostname, port

        ###TODO: try handle
        # s = socket()
        conn=socket.create_connection((hostname,port))
        self._conn=conn

    def send_command(self,command):
        self._conn.send(command)


GETDATA= 0x5A
STOPDATA= 0x4B
SETSYSTIME= 0x6C
MOTOR_FWD= 0x2A
MOTOR_REV= 0x2A
MOTOR_HALT= 0x2B
MOTOR_HOME= 0x2A

class SocketMessage:
  def build(self,command,param):
    cmd = {
      'GETDATA' : GETDATA,
      'STOPDATA' : STOPDATA,
      'MOTORFWD' : MOTOR_FWD,
      'MOTORHALT' : MOTOR_HALT,
      'MOTORREV' : MOTOR_REV,
      'MOTORHOME' : MOTOR_HOME


    }[command]

    par = {
      ''

    }
    self._message = cmd
    return self._message

def send(command):
    sm = SocketMessage()
    message=sm.build(command)
    socket.send(message)