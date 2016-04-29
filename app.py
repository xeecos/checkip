#!/usr/bin/env python
import socket
import serial
import sys,time
import signal
from time import ctime,sleep
import glob,struct
from multiprocessing import Process,Manager,Array
import threading
def get_my_ip():
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"
def onRead():
    global ser,isExit
    while True:
        if isExit:
            break;
        n = ser.inWaiting()
        if n>0 :
            s = ser.read(n)
            if s.find("M5 OK")>-1:
                ser.write("M5 SIP:"+get_my_ip()+":5000\n")

if __name__ == "__main__":
    print get_my_ip()
    ser = serial.Serial("/dev/ttyAMA0",115200)
    isExit = False
    try:
        th = threading.Thread(target=onRead)
        th.start()
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print "exit"
        isExit = True
    finally:
        ser.close();
    
