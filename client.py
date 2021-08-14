import sys
import socket

serverIP, serverPort = sys.argv[1], sys.argv[2] # The arguments: serverIP and serverPort
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Protocol

''' Asking the server queries '''
while True:
    siteAddress = bytes(input().encode()) # The website that the user asks for its IP
    s.sendto(siteAddress, (serverIP, int(serverPort))) # Send to the server the input message
    data, addr = s.recvfrom(1024) # The data that we have recieved from the server
    print(data.decode("utf-8").split(",")[1]) #print the relevent data to the client

s.close() # Close the socket