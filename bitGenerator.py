from base64 import encode
from curses import baudrate
import os
from socket import timeout
import serial
import time
import serial.tools.list_ports

comPort = ""
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    if "CH3" in desc:
        comPort = port
        break

if(comPort == ""):
    print("Li-Fi Module not available.")
    exit();


ser = serial.Serial(comPort, 115200, timeout=0.1)
filename = input("Enter file name: ")
fileExt = input("Enter file extension: ")
ser.write("^".encode())
data = ser.readline()
filesize = os.path.getsize(filename + "." + fileExt)
ser.write(filesize.to_bytes(1, byteorder='big'))
data = ser.readline().decode().strip("\n")
fp = open(filename + "-temp.txt", "w")
with open(filename + "." + fileExt, "rb") as f:
    byteRead = f.read(1)
    d = ""
    while byteRead:
        bits = bin(ord(byteRead))[2:].rjust(8, '0')
        
        #Writing to File
        fp.write(bits)
        fp.write("\n")
        
        #Transmit Data
        ser.write(byteRead);
        
        #Read The Data From Port
        time.sleep(0.2)
        

        #Read Data from File
        byteRead = f.read(1)

        data = ser.readline().decode().strip("\n")
        print(data)
        

ser.close()
f.close()
fp.close()