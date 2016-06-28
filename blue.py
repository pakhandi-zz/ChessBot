import bluetooth
import sys

serverMACAddress = '98:D3:32:20:34:32'
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))
while 1:
    s.send(sys.argv[1])
    break
s.close()