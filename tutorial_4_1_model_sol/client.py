import sys
import socket
from common_methods import handle_request, send_one_message, get_path, write_to_file, recv_one_message

print("Make sure this is ran as python client.py <hostname> <port> put <filename>")
server_addr = (sys.argv[1], int(sys.argv[2])) 
request_type_str = str(sys.argv[3])
server_addr_str = str(server_addr)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handshake(socket):
    send_one_message(socket, "syn")
    response = recv_one_message(socket).decode()
    if response == "syn/ack":
        send_one_message(socket, "ack")
        print("Handhsake successful...continuing...")
        return
    else:
        print("Handshake failed...")
        socket.close()
        exit(0)
try:
    print("Connecting to " + server_addr_str + "... ")
    client_socket.connect(server_addr)
except Exception as e:
    print(e)
    socket.close()
    exit(1)
    
    
try:
    while True:
        handshake(client_socket)
        request_type_sent = send_one_message(client_socket, request_type_str)


        if request_type_str == "list":
            files = recv_one_message(client_socket).decode()
            print("files: ", files)
            break
            

        else:
            filename_str = str(sys.argv[4])
            filename_sent = send_one_message(client_socket, filename_str) 
            if request_type_str == "put":  
                file_path = get_path("client_data", True) + "/" + filename_str
                data_sent = handle_request(request_type_str, file_path, client_socket)
                print("file sent successfully. Exiting...")
                break

            elif request_type_str == "get":
                content = recv_one_message(client_socket).decode()
                print("file name: ", filename_str)
                file_path = get_path("client_data", True) + "/" + filename_str
                print("file path: ", file_path)
                new_file = write_to_file(file_path, content)
                break



            

finally:
    client_socket.close()
exit(0)
         
