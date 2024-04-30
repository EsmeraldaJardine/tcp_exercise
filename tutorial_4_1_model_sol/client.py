import sys
import socket
from common_methods import handle_request_client

print("Make sure this is ran as python client.py <hostname> <port> put <filename>")
server_addr = (sys.argv[1], int(sys.argv[2])) 
request_type_str = str(sys.argv[3])
filename_str = str(sys.argv[4])

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
        client_socket.sendall(request_type_str.encode())
        print("request type: ", request_type_str)
        filename_length = "0x"+format(len(filename_str), "02x")
        client_socket.send(filename_length.encode())
        client_socket.sendall(filename_str.encode())
        print("file name: ", filename_str) 
        bytes_sent = handle_request_client(request_type_str, filename_str, client_socket)
        print("file sent successfully. Exiting...")
        break

finally:
    client_socket.close()
exit(0)
         