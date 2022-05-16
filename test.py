from modbus.client import *
# Change HOSTNAME to Server IP address, defaults to localhost
c = client(host='10.186.50.224')
c.read()                        # To read 10 Input Registers from Address 0
c.read(FC=3, ADR=10, LEN=8)     # To read 8 Holding Registers from Address 10
c.write(11, 22, 333, 4444)         # To write Holding Registers from Address 0
# To write Holding Registers from Address 10
c.write(11, 22, 333, 4444, ADR=10)
c.write(11, 22, FC=15, ADR=10)   # To write Coils from Address 10
fc()                            # To get the supported Function Codes
