#Initilize global variable so it can be accessed by multiple funcitons
#Keeps track of current clients
clientList = []

def server(port):
    #Creates a server communicator object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #Binds to available interfaces
    serversocket.bind(('', int(port)))

    #Listens for conncetions and accept
    serversocket.listen(5)
    
    #Continously checks for a client and accepts their connection
    #Add client to list to be recognized
    #Creates a thread to handle client
    while True:
        sock, addr = serversocket.accept()
        clientList.append(sock)
        threading.Thread(target=recvMessage, args=[sock]).start()

def recvMessage(sock):
    #Handles the receiving of message for the server
    while True:
        
        #Tries ccepts a message
        try:
            msg = sock.recv(1024)
            
        #Exit if fails
        except:
            sys.exit()
            
        #Checks if message is greather than length 0
        if len(msg):
            #Iterates through avaliable clients and sends to each client that is not the originator
            for client in clientList:
                if client != sock:
                    client.send(msg)
                    
        #Message length is 0
        else:
            
            #Remove client from the client list
            #Alert users other client has left
            #Close socket
            print('No bytes received; closing socket')
            clientList.remove(sock)
            userLeftMsg = "\nA user has left the conversation.\n"
            if len(clientList) > 0:
                for client in clientList:
                    client.send(userLeftMsg.encode())
            sock.close()
            break
        
if __name__ == "__main__":
    import getopt
    import sys
    import threading
    import socket
    
    #gets command line arguments
    opts, args = getopt.getopt(sys.argv[1:], "")
    
    server(args[0])

