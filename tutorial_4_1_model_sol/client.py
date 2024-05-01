import os
import sys
import socket
from common_methods import close_conn, handle_request, send_one_message, get_path, write_to_file, recv_one_message

if len(sys.argv) > 3:
    server_addr = (sys.argv[1], int(sys.argv[2])) 
    request_type_str = str(sys.argv[3])
    server_addr_str = str(server_addr)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if len(sys.argv) == 4 and request_type_str != "list":
        print("Make sure this is ran as python client.py <hostname> <port> <put filename|get filename|list>")
        exit(0)
    if len(sys.argv) == 5 and (request_type_str == "get" or request_type_str == "put"):
        filename_str = str(sys.argv[4])
    else:
        print("Make sure this is ran as python client.py <hostname> <port> <put filename|get filename|list>")
        exit(0)
else:
    print("Make sure this is ran as python client.py <hostname> <port> <put filename|get filename|list>")
    exit(0)

def handshake(socket):
    send_one_message(socket, "syn")
    response = recv_one_message(socket).decode()
    if response == "syn/ack":
        send_one_message(socket, "ack")
        print("Handhsake successful...continuing...")
        return
    else:
        print("Handshake failed...")
        close_conn(socket)
try:
    print("Connecting to " + server_addr_str + "... ")
    client_socket.connect(server_addr)
except Exception as e:
    print(e)
    client_socket.close()
    exit(1)
  
while True:
    handshake(client_socket)
    request_type_sent = send_one_message(client_socket, request_type_str)


    if request_type_str == "list":
        files = recv_one_message(client_socket).decode()
        print("files: ", files)
        close_conn(client_socket)
        

    else:
        filename_str = str(sys.argv[4])
        filename_sent = send_one_message(client_socket, filename_str) 
        if request_type_str == "put":  
            file_path = get_path("client_data", True) + "/" + filename_str
            if os.path.exists(file_path):
                data_sent = handle_request(request_type_str, file_path, client_socket)
                print("file sent successfully. Exiting...")
            else:
                error = "No such file exists!"
                print(error)
                send_one_message(client_socket, "ERR"+error)
            print(recv_one_message(client_socket).decode())
            close_conn(client_socket)

        elif request_type_str == "get":
            content = recv_one_message(client_socket).decode()
            if "ERR" in content:
                print(content[3:])
                client_socket.close()
                exit(0)
            print("file name: ", filename_str)
            file_path = get_path("client_data", True) + "/" + filename_str
            if os.path.exists(file_path):
                for cnt in range(1, 100):
                    if not os.path.exists(file_path[:-4]+"("+str(cnt)+")"+file_path[-4:]):
                        file_path=file_path[:-4]+"("+str(cnt)+")"+file_path[-4:]
                        filename_str = filename_str[:-4]+"("+str(cnt)+")"+filename_str[-4:]
                        break
            new_file = write_to_file(file_path, content)
            success_msg = "put successful! Saved on client as: " + filename_str
            print(success_msg)
            send_one_message(client_socket, success_msg)
            close_conn(client_socket)