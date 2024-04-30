import os
import sys
import socket
from common_methods import socket_to_memory, get_path, write_to_file

def parse_port_arg():

    if len(sys.argv) != 2:
        print("Usage: python server.py <port number>")
        sys.exit(1)

    port_num = int(sys.argv[1])

    if not (0 < port_num < 65536):
        print("Port number must be between 1 and 65535")
        sys.exit(1)

    return port_num

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind(("0.0.0.0", parse_port_arg()))
    server_socket.listen(5)   
except Exception as e:
    print(e)
    exit(1)
    
    
try:
    while True:
        print("Waiting for new client... ")
        client_socket, client_address = server_socket.accept()
        cli_addr_str = str(client_address) 
        print("Client " + cli_addr_str + " connected. Now chatting...")
        
        while True:
            try:
                request = client_socket.recv(50).decode()
            except Exception as e:
                print("connection was closed by client")
            if request.strip() == "list":
                response = str(os.listdir())
                client_socket.sendall(response.encode())

            elif request.strip()[:3] == "put":
                print("request type: ", request.strip()[:3])
                filename_length = request.strip()[3:7]
                print("filename length: ", filename_length)
                msg_start_index = 7 + int(filename_length, 16)
                filename = str(request.strip()[7:msg_start_index])
                print("filename ", filename)
                contents = str(request.strip()[msg_start_index:])
                print("message : ", request.strip())
                file_path = get_path(filename, "server_data", False) + "/" + filename
                #contents = client_socket.recv(1024).decode("utf-8")
                new_file = write_to_file(file_path, contents)
                #file = open(file_path, "w")
                
				
                #file.write("ok")
                #client_socket.send("File received".encode())
            #bytes_saved = socket_to_memory(client_socket, cli_addr_str)
            #if bytes_saved == 0:
               # print("Client closed connection.")
              #  exit(0)
            
finally:
    client_socket.close()

