'''

    Python script to send data using bluetooth

'''

import bluetooth
import argparse

# Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument("toSend", help="The text to send using bluetooth")
args = parser.parse_args()

serverMACAddress = '98:D3:32:20:34:32'
port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))
while 1:
    s.send(args.toSend)
    break
s.close()
