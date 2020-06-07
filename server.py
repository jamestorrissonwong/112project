import socket
import threading
from queue import Queue

HOST = '127.0.0.1' 
PORT = 50003
BACKLOG = 2

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

def handleClient(client, serverChannel, cID, clientele):
  client.setblocking(1)
  msg = ""
  while True:
    # try:
      msg += client.recv(10).decode()
      
      command = msg.split("\n")
      while (len(command) > 1):
        ship = command[0]
        msg = "\n".join(command[1:])
        serverChannel.put(str(cID) + " " + ship)
        command = msg.split("\n")


def serverThread(clientele, serverChannel):
  while True:
    msg = serverChannel.get(True, None)
    #print("msg recv: ", msg)
    msgList = msg.split(" ")
    senderID = msgList[0]
    details = " ".join(msgList[1:])
    #print("d", details)
    if (details != ""):
      for cID in clientele:
        
          sendMsg = senderID + " " + details + "\n"
          clientele[cID].send(sendMsg.encode())
          #print("> sent to %s:" % cID, sendMsg[:-1])
    #print()
    serverChannel.task_done()

clientele = dict()
playerNum = 0

serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()

names = ["Ship1", "Ship2"]

while True:
  client, address = server.accept()
  myID = names[playerNum]
  #print(myID, playerNum)
  for cID in clientele:
    #print (repr(cID), repr(playerNum))
    clientele[cID].send(("myIDis %s\n" % myID).encode())
    client.send(("myIDis %s\n" % cID).encode())
  clientele[myID] = client
  client.send(("myIDis %s \n" % myID).encode())
  #print("connection recieved from %s" % myID)
  threading.Thread(target = handleClient, args = 
                        (client ,serverChannel, myID, clientele)).start()
  playerNum += 1