import sys
import socket
from common_methods import get_path, handle_request_client, write_to_file

print("Make sure this is ran as python client.py <hostname> <port> put <filename>")
server_addr = (sys.argv[1], int(sys.argv[2])) 
request_type_str = str(sys.argv[3])
if len(sys.argv) == 5:
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
        if request_type_str != "list":
            filename_length = "0x"+format(len(filename_str), "02x")
            if request_type_str == "put":
                client_socket.send(filename_length.encode())
                client_socket.sendall(filename_str.encode())
                bytes_sent = handle_request_client(request_type_str, filename_str, client_socket)
                print("file sent successfully. Exiting...")
            elif request_type_str == "get":
                client_socket.send(filename_str.encode())
                response = client_socket.recv(50).decode()
                contents = str(response)
                print(filename_str)
                file_path = get_path(filename_str, "client_data", True) + "/" + filename_str
                # print(file_path)
                new_file = write_to_file(file_path, contents)
                client_socket.send("File received".encode())
                exit(0)
            break
        else:
            response = client_socket.recv(1024).decode().strip()
            break

finally:
    client_socket.close()
exit(0)
         