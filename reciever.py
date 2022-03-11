from curses import baudrate
import os
import serial
import sys
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



fileName = input("Enter File Name: ")
fileExt = input("Enter File Extension: ")
fileSize = -1
print("Recieving || Waiting")
fp = open(fileName + "-new." + fileExt, "wb")
ser = serial.Serial(comPort, baudrate=230400, timeout=0.1)
count = 0
recvData = ""
bitList = []
while ser.in_waiting or 1:
    val = ser.read(3).decode().strip("\n")
    # print(val)
    if val:
        bitList.append(str(val))
        # print(bitList)
    if(len(bitList) >= 8):
        
        #Generate Bits
        for i in bitList:
            recvData += (i.strip("\r"))
        # print(recvData, end=" ")
        
        bitList.clear()
        
        if(fileSize == -1):
            fileSize = int(recvData, 2)
            # print(fileSize)
            print("\n\n##### Recieving || Started #####")
        else:
            byteData = bytes(int(recvData[i : i + 8], 2) for i in range(0, len(recvData), 8))
            
            fp.write(byteData)
        count += 1
        
        if(count > fileSize):
            ser.write("^".encode())
            ser.flushInput()
            ser.flushOutput()
            break
        # print(recvData)
        recvData = ""
        

fp.close()
ser.close()
    # sleep(0.01)

print("\n\n##### File Recieving Successfully #####")
print("File saved as", fileName + "-new." + fileExt)

