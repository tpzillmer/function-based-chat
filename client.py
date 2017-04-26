def client(server, port):
    
    #Create a client communicator object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, int(port)))

    #Create threads to handle sendMsg and recvMsg functions
    threading.Thread(target=sendMsg, args=[sock]).start()
    threading.Thread(target=recvMsg, args=[sock]).start()

def sendMsg(sock):
    #Handle the sending of message from the client
    while True:
        
        #Allows the user to input a message
        print("You: ", end="")
        sys.stdout.flush()
        msg = sys.stdin.readline()
        
        #Leaves the loop if the message length is zero
        if not msg:
            break
        
        #Tries to send a message
        try:
            sock.send(msg.encode())
            
        #If there is an error, exit
        except:
            sys.exit()
            
    #Attempt to close the socket
    try: 
        sock.shutdown(socket.SHUT_WR)
        sock.close()
    except:
        pass
    
def recvMsg(sock):
    #Handles the receiving of messages
    
    while True:
        
        #Tries to send a message
        try:
            recvMsg = sock.recv(1024)
            print("\nOther: " + recvMsg.decode()+"You: ", end="")
            
        #If no message can be sent, the server has closed or client socket has closed
        except:
            print("\nYou have left the conversation.")
            sock.close()
            break
            

if __name__ == "__main__":
    import getopt
    import sys
    import threading
    import socket

    #gets command line arguments
    opts, args = getopt.getopt(sys.argv[1:], "")
    
    client(args[1], args[0])
