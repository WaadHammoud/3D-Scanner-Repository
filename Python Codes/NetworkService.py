from socket import *
from time import sleep

class NetworkService:

    # Intialize network object
    def __init__(self, broadcastPort, listenPort): 
        self.hostname = gethostname() # Get hostname (Computer Name)   
        self.address = gethostbyname(self.hostname) # Get Computer IP Address on local network
        
    # Broadcast message on socket for certain time (seconds)
    def Broadcast(self, message, time):
        sock = socket(AF_INET, SOCK_DGRAM) # Create a socket at server/client side using TCP/IP Protocol
        sock.bind(('', 0))
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        
        for i in range(int(time/2)):
            # message (IP...) needs to be encoded from string to bytes
            sock.sendto(message.encode('utf-8'), ('<broadcast>', 50000))
            sleep(2)
    
    # Listen for any message on socket
    def Listen(self):
        sock = socket(AF_INET, SOCK_DGRAM) # Create a socket at server/client side using TCP/IP Protocol
        sock.bind(('', 50000))
        data = ''
        while (data == ''): #While broadcast hasn't been received yet (empty string)
            data, wherefrom = sock.recvfrom(1500, 0)
        
        # data needs to be decoded from bytes into string
        data = data.decode('utf-8')
        address = repr(wherefrom[0])
        return (data, address) #Returns message and IP Address
        
    # Listen for certain message on socket
    def ListenFor(self, message):
        sock = socket(AF_INET, SOCK_DGRAM) # Create a socket at server/client side using TCP/IP Protocol
        sock.bind(('', 50000))
        data = ''
        while (data != message.encode('utf-8')): #While broadcast hasn't been received yet (empty string) or incorrect message
            data, wherefrom = sock.recvfrom(1500, 0)
        
        # data needs to be decoded from bytes into string
        data = data.decode('utf-8')
        address = repr(wherefrom[0])
        return (data, address) #Returns message and IP Address

