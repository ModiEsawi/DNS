import socket
import sys
import time

# reading the lines into a dictionary
readIPsFiles = open(sys.argv[4], 'r')
Lines = readIPsFiles.readlines()
addressDictionary = {}
for line in Lines:
    if len(line.strip()) == 0:  # ignoring empty lines
        continue
    line = line.strip()
    currentLine = line.split(",")
    addressDictionary[currentLine[0]] = [currentLine[1], currentLine[2]]
readIPsFiles.close()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(sys.argv[1])))


# if we wont find the given address in our text file then we will ask our gather server for it
def askDad():
    writeIPsFiles = open(sys.argv[4], 'a+')
    secondSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    secondSocket.sendto(data, (sys.argv[2], int(sys.argv[3])))
    fatherData, fatherAddress = secondSocket.recvfrom(1024)
    lineToWrite = "\n" + str(fatherData.decode("utf-8")) + "#" + str(time.time())
    decoded = fatherData.decode("utf-8").split(",")
    addressDictionary[clientsAddress] = [decoded[1], decoded[2] + "#" + str(time.time())]
    writeIPsFiles.write(str(lineToWrite))
    s.sendto(fatherData, addr)
    secondSocket.close()
    writeIPsFiles.close()


# update the TTL for an address that we already have in our text file we wil first delete the old line/
def deleteLine(lineToDelete):
    with open(sys.argv[4], "r") as file:
        lines = file.readlines()
    file.close()
    for currLine in lines:
        if "#" in currLine:
            if lineToDelete == currLine.split(",")[0]:
                lineToDelete = currLine
                break
    with open(sys.argv[4], "w") as file:
        for textLine in lines:
            if textLine not in lineToDelete:
                textLine = textLine.strip("\n")
                textLine = "\n" + textLine
                file.write(textLine)
    file.close()
    with open(sys.argv[4], 'r') as fin:
        finalData = fin.read().splitlines(True)
    fin.close()
    with open(sys.argv[4], 'w') as fout:
        fout.writelines(finalData[1:])
    fout.close()


while True:
    data, addr = s.recvfrom(1024)
    clientsAddress = data.decode("utf-8")
    if clientsAddress in addressDictionary:
        value = addressDictionary.get(clientsAddress)[1]
        #  if we already have this given address we will check to see if its TTL is valid
        if '#' in value:
            ttl = int(value.split("#")[0])
            entranceTime = float(value.split("#")[1])
            if entranceTime + ttl < time.time():  # TTL is not valid so we will ask our father server for the answer
                deleteLine(clientsAddress)
                askDad()
                continue
        # return the answer as we should : address, IP, TTL.
        toSend = clientsAddress + "," + addressDictionary.get(clientsAddress)[0] + "," + \
                 addressDictionary.get(clientsAddress)[1]
        s.sendto(str.encode(toSend), addr)
    else:
        askDad()
