#!/usr/bin/python3
import socket
from array import array
from struct import unpack, pack
from math import ceil
import rsa
import pickle

__all__ = ["client", 'fc']

PORT = 502
BUFF = 1024

# rsa encryption process
def RsaEncrypt(strArray):
    (PubKey, PrivateKey) = rsa.newkeys(128)
    Encrypt_Str_Array = []
    for data in strArray:
        content = str(data).encode('utf8')
        # Encryption of plaintext with public key
        Encrypt_Str = rsa.encrypt(content, PubKey)
        Encrypt_Str_Array.append(Encrypt_Str)
    # Return the encrypted content and private key
    return (Encrypt_Str_Array, PrivateKey)

# rsa decryption process
def RsaDecrypt(strArray, pk):
    Decrypt_Str_Array = []
    for data in strArray:
        content = rsa.decrypt(data, pk)
        content = content.decode('utf8')
        content = int(content)
        Decrypt_Str_Array.append(content)
    return array('B', Decrypt_Str_Array)
    
def fc():
    print("Supported Function Codes:\n\
	1 = Read Coils or Digital Outputs\n\
	2 = Read Digital Inputs\n\
	3 = Read Holding Registers\n\
	4 = Read Input Registers\n\
	5 = Write Single Coil\n\
	6 = Write Single Register\n\
	15 = Write Coils or Digital Outputs\n\
	16 = Write Holding Registers")


class client:
    def __init__(self, host='localhost', unit=1):
        self.host = host
        self.unit = unit
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, PORT))
        self.TID = 0

    def read(self, FC=4, ADR=0, LEN=10):  # Default Read: Input Registers
        if FC not in [1, 2, 3, 4]:
            return(fc())
        lADR = ADR & 0x00FF
        mADR = ADR >> 8
        lLEN = LEN & 0x00FF
        mLEN = LEN >> 8
        if (FC < 3):
            BYT = ceil(LEN / 8)  # Round off the no. of bytes
        else:
            BYT = LEN * 2
        if self.TID < 255:
            self.TID = self.TID + 1
        else:
            self.TID = 1
        cmd = array('B', [0, self.TID, 0, 0, 0, 6,
                          self.unit, FC, mADR, lADR, mLEN, lLEN])
        (encryptdata, PrivateKey) = RsaEncrypt(cmd)
        Message = pickle.dumps([encryptdata, PrivateKey]) 
        self.sock.send(Message)   
        
        Received_Message = self.sock.recv(BUFF)
        if Received_Message:
            (recvdata, PrivateKey) = pickle.loads(Received_Message)
        else:
            return 
        buf = RsaDecrypt(recvdata, PrivateKey)

        if (FC > 2):
            return unpack('>' + 'H' * LEN, buf[9:(9 + BYT)])
        else:
            return unpack('B' * BYT, buf[9:(9 + BYT)])

    def write(self, *DAT, FC=16, ADR=0):  # Default Write: Holding Registers
        if FC not in [5, 6, 15, 16]:
            return(fc())
        lADR = ADR & 0x00FF
        mADR = ADR >> 8
        VAL = b''
        for i in DAT:
            VAL = VAL + pack('>H', i)
        if FC == 5 or FC == 6:
            VAL = VAL[0:2]
        if FC == 5 or FC == 15:
            LEN = len(VAL) * 8
        else:
            LEN = len(VAL) // 2
        lLEN = LEN & 0x00FF
        mLEN = LEN >> 8
        if self.TID < 255:
            self.TID = self.TID + 1
        else:
            self.TID = 1
        if FC == 6:
            cmd = array('B', [0, self.TID, 0, 0, 0,
                        6, self.unit, FC, mADR, lADR])
        else:
            cmd = array('B', [0, self.TID, 0, 0, 0, 7 + len(VAL),
                        self.unit, FC, mADR, lADR, mLEN, lLEN, len(VAL)])
        cmd.extend(VAL)
        print("Sent", cmd)

        (encryptdata, PrivateKey) = RsaEncrypt(cmd)
        Message = pickle.dumps([encryptdata, PrivateKey]) 
        self.sock.send(Message) 

        Received_Message = self.sock.recv(BUFF)
        # 如果接收到的内容非空
        if Received_Message:
            (recvdata, PrivateKey) = pickle.loads(Received_Message)
        else:
            return 
        buffer = RsaDecrypt(recvdata, PrivateKey)

