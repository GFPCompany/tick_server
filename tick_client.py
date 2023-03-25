import socket
addr=input("SERVER ADDRESS(like xxx.xxx.xxx.xxx:xxxx):")
s=socket.socket()
try:
    s.connect((addr.split(":")[0],int(addr.split(":")[1])))
except socket.gaierror as e:
    if str(e)=="[Errno 11001] getaddrinfo failed":
        print("Invalid address\nclosing...")
        exit(1)
i=0
while True:
    i+=1
    data = s.recv(2048)
    if i==1:
        print("Connected to server")
    if data == b"online?":
        s.sendall(b"yes")