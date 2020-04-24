import asyncio
import random
import json
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

clients = []
clientDict = {}
clientDictName={}
channels ={}
clientToChannel ={}
def broadcast(self,clients,payload,isBinary):
    for client in clients:
        if client!=self:
            client.sendMessage(payload,isBinary)

        
class MyServerProtocol(WebSocketServerProtocol):
    

    def onConnect(self, request):
        clients.append((self))
        print("Client connecting: {0}".format(request.peer))
        clientDict[self]=True
        clientDictName[self]=""
        

    def onOpen(self):
        print("WebSocket connection open.")
    
    

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
        #Decoding the json Object
        # if clientDict[self]==False:
        #     message = json.loads(payload.decode('utf8'))
        #     #Creat new channel
        #     if message["channelName"] not in channels:
        #         channels[message["channelName"]] = []
        #     if self not in channels[message["channelName"]]:
        #         channels[message["channelName"]].append(self)
        #     clientToChannel[self]=message["channelName"]
        #     if(message["channelName"]=="ALL"):
        #         broadcast(self,clients,payload,isBinary)
        #     else:
        #         broadcast(self,channels[message["channelName"]],payload,isBinary)
                


        #assign Name 
        if clientDict[self]==True and clientDictName[self]=="":
            clientDictName[self]=payload.decode('utf8')
            clientDict[self]=False
        
        
        try:
            message = json.loads(payload.decode('utf8'))
            #Creat new channel
            payload = (clientDictName[self]+" : " + message["message"]).encode(encoding='UTF-8',errors='strict') 
            if message["channelName"] not in channels:
                channels[message["channelName"]] = []
            if self not in channels[message["channelName"]]:
                channels[message["channelName"]].append(self)
            clientToChannel[self]=message["channelName"]
            if(message["channelName"]=="ALL"):
                broadcast(self,clients,payload,isBinary)
            else:
                broadcast(self,channels[message["channelName"]],payload,isBinary)
        except:
            print("This is for only first time")


    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
    



if __name__ == '__main__':
    factory = WebSocketServerFactory("ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol
    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '0.0.0.0', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()