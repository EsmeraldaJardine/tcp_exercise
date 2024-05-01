import os
import sys
import socket
from common_methods import handle_request, get_path, write_to_file, recv_one_message

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
        
        try:
            first_message = recv_one_message(client_socket).decode()
            client_socket.sendall(b'ack')
            second_message = recv_one_message(client_socket).decode()
            client_socket.sendall(b'ack')

            print("first message: ", first_message)
            print("second message: ", second_message)
        except Exception as e:
            print("connection was closed by client")
        #if request.strip() == "list":
        #    response = str(os.listdir())
        #    client_socket.sendall(response.encode())
        if first_message == "put":
            request_type_str = first_message
            filename_str = second_message
            content = recv_one_message(client_socket).decode()
            print("message : ", content)
            file_path = get_path(filename_str, "server_data", False) + "/" + filename_str
            new_file = write_to_file(file_path, content)
            print("file saved")
        
        elif first_message == "get":
            filename_str = second_message
            request_type_str = "put"
            file_path = get_path(filename_str, "server_data", False) + "/" + filename_str
            print("file path: ", file_path)
            client_socket.sendall(b'ack')
            sent_data = handle_request(request_type_str, file_path, client_socket)
            exit(0)
        
finally:
    client_socket.close()

