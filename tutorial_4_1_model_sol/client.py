import sys
import socket
from common_methods import handle_request_client, send_one_message

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
        request_type_sent = send_one_message(client_socket, request_type_str)
        filename_sent = send_one_message(client_socket, filename_str) 
        data_sent = handle_request_client(request_type_str, filename_str, client_socket)
        print("file sent successfully. Exiting...")
        break

finally:
    client_socket.close()
exit(0)
         