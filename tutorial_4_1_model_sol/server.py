import os
import sys
import socket
from common_methods import handle_request, get_path, send_one_message, write_to_file, recv_one_message

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
    
def handshake(socket):
    response = recv_one_message(socket).decode()
    if response == "syn":
        send_one_message(socket, "syn/ack")
        ack_response = recv_one_message(socket).decode()
        if ack_response == "ack":
            print("Handshake successful, continuing..")
        else:
            print("Handshake failed on ack...")
            socket.close()
            exit()
        
    else:
        print("Handshake failed on syn...")
        socket.close()
        exit(0)
    
try:
    while True:
        print("Waiting for new client... ")
        client_socket, client_address = server_socket.accept()
        cli_addr_str = str(client_address) 
        print("Client " + cli_addr_str + " connected. Now chatting...")
        handshake(client_socket)

        request_type_str = recv_one_message(client_socket).decode()

        if request_type_str == "list":
            print("Sending file list...")
            file_path = get_path("server_data", False)
            sent_data = handle_request(request_type_str, file_path, client_socket)
            client_socket.close()
            exit(0)
        
        else:
            second_message = recv_one_message(client_socket).decode()

        if request_type_str == "put":
            print("Server receiving file...")
            filename_str = second_message
            content = recv_one_message(client_socket).decode()
            if "ERR" in content:
                    print(content[3:])
                    break
            file_path = get_path("server_data", False) + "/" + filename_str
            if os.path.exists(file_path):
                for cnt in range(1, 100):
                    if not os.path.exists(file_path[:-4]+"("+str(cnt)+")"+file_path[-4:]):
                        file_path=file_path[:-4]+"("+str(cnt)+")"+file_path[-4:]
                        filename_str = filename_str[:-4]+"("+str(cnt)+")"+filename_str[-4:]
                        break
            new_file = write_to_file(file_path, content)
            success_msg = "put successful! Saved on server as: " + filename_str
            print(success_msg)
            send_one_message(client_socket, success_msg)
            client_socket.close()
            exit(0)
            
        
        elif request_type_str == "get":
            print("Server sending file...")
            filename_str = second_message
            request_type_str = "put"
            file_path = get_path("server_data", False) + "/" + filename_str
            if os.path.exists(file_path):
                sent_data = handle_request(request_type_str, file_path, client_socket)
                success_msg = "get successful! Exiting..."
                print(success_msg)
                send_one_message(client_socket, success_msg)
            else:
                error = "No such file exists!"
                print(error)
                send_one_message(client_socket, "ERR"+error)
            print(recv_one_message(client_socket).decode())
            client_socket.close()
            exit(0)

except Exception as e:
    print("Error message: ", e, " occurred. Exiting...")
    exit(0)  
