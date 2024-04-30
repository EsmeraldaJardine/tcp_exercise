import sys
import socket
from common_methods import handle_request_client

print("Make sure this is ran as python client.py <hostname> <port> put <filename>")
server_addr = (sys.argv[1], int(sys.argv[2])) 
request_type = sys.argv[3]
request_type_str = str(sys.argv[3])
file_name = sys.argv[4]
file_name_str = str(sys.argv[4])

server_addr_str = str(server_addr)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print("Connecting to " + server_addr_str + "... ")
    client_socket.connect(server_addr)
except Exception as e:
    print(e)
    exit(1)
    
    
try:
    while True:  
        bytes_sent = handle_request_client(request_type_str, file_name_str, client_socket)
        if bytes_sent == 0:
            print("User-requested exit.")
            break
         
finally:
    client_socket.close()
         