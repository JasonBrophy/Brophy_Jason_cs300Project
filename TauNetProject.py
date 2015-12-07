#Copyright (c) 2015 Jason Brophy
import socket, select, string, sys, threading, random, pickle
from multiprocessing import Process

def main():
    random.seed()
    userName = 'jbrophy'
    userList = ()
    userList = importUserTable(userName, userList)
    if(userList == 0):
        print('You are not in the authorized users')
        return 0
    else:
        for each in range(0, len(userList), 3):
            print(userList[each], end = ', ')
    p1 = Process(sendMessage(userName, userList))
    p1.start()
    p2 = Process(receiveMessage())
    p2.start()
    '''while(1):
        try:
            receiveMessage()                
        except: 
            print('something went wrong, terminating')
            #os.kill(newpid, 9)
     '''       
    return 0

def receiveMessage():
    host = '0.0.0.0'
    port = 6283
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)
        while(1):
            conn, addr = s.accept()
            print('connected to ' + str(addr))
            test = conn.recv(1024)
            decrypted = decrypt(test, 20, 'password')
            if(decrypted != 0):
                for i in range(len(decrypted) - 1):
                    print(decrypted[i], end='')
            
    except:
        s.shutdown()
            
                        
def importUserTable(userName, userList):
    flag = 0
    try:
        userTable = open('taunetUserTable.txt', "r")
    except:
        print('File not found, exiting')
        return
    userList = []
    newList = []
    userList = userTable.readlines()
    userTable.close()
    for each in userList:
        each = each[:len(each)-1]
        newList.append(each)
        if (userName == each):
            flag = 1
    if flag:
        return newList
    return 0

def displayAvailableUsers():
    print('to be implemented')


def sendMessage(userName, userList):
    sendTo = ''
    message = ''
    host = ''
    while True:
        flag = 0
        input('Press enter to begin the message sending process\n\n')
        try:
            while flag != 1:
                sendTo = input('Enter the name of the user to send a message to' + '\n')
                for each in range(0, len(userList), 3):
                    if(sendTo == userList[each]):
                        host = userList[each+1]
                        flag = 1
            message = input('Enter the message' + '\n')
            for each in message:
                if each == '\n':
                    each = '\r\n'
            wholeMessage = packageMessage(userName, sendTo, message)
            encryptedMessage = encrypt(wholeMessage, 20, 'password')
            #sendableMessage = ''.join(encryptedMessage)
            port = 6283
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(bytes(encryptedMessage))
            s.close()
        except socket.error as msg:
            print(msg)
            print('Message stored in failedMessages.dat')
            file_out = open("failedMessages.dat", "ab")
            pickle.dump(wholeMessage, file_out)
            file_out.close()
     
        
def packageMessage(userName, sendTo, message):
    return 'version: 0.2' + '\r\nfrom: ' + userName + '\r\nto: ' + sendTo + '\r\n' + '\r\n' + message
    

def encrypt(message, rounds, key):
    if(sys.getsizeof(key) > 246):
        return -1
    k = []
    iv = []
    n = len(message)
    for each in range(10):
        iv.append(random.randint(0, 255))
    for each in key:
        k.append(ord(each))
    for each in iv:
        k.append(each)    
    keystream = rc4(n, rounds, k)
    ciphertext = []
    for each in range(n+10):
        ciphertext.append(0)
    for i in range(10):
        ciphertext[i] = iv[i]
    for i in range(n):
        ciphertext[i+10] = (ord(message[i]) ^ keystream[i])
    return ciphertext
    
def rc4(keystreamLength, rounds, key):
    l = len(key)
    s = []
    for each in range(256):
        s.append(each)
    keystream = []
    for each in range(keystreamLength):
        keystream.append(0)
    j = 0
    for each in range(rounds):
        for i in range(256):
            j = (j+s[i]+key[i % l]) % 256
            s[i], s[j] = s[j], s[i]
    j = 0
    for i in range(keystreamLength):
        x = (i+1) % 256
        j = (j + s[x]) % 256
        s[x], s[j] = s[j], s[x]
        keystream[i] = s[(s[x] + s[j]) % 256]
    return keystream
        
def decrypt(message, rounds, key):
    if(len(message) == 0):
        return 0
    if(len(key) > 246):
        return -1
    n = len(message)
    iv = []
    for each in range(10):
        iv.append(message[each])
    k = []
    remnantMessage = []
    for each in range(10, len(message)):
        remnantMessage.append(message[each])

    for each in key:
        k.append(ord(each))
    for each in iv:
        k.append(each)
    keystream = rc4(n-10, rounds, k)

    plaintext = []
    for each in range(n-9):
        plaintext.append(0)
    for i in range(n-10):
        plaintext[i]= chr(remnantMessage[i] ^ keystream[i])
    return plaintext
