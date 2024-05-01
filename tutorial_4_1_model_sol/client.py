import sys
import socket
from common_methods import handle_request, send_one_message, get_path, write_to_file, recv_one_message

print("Make sure this is ran as python client.py <hostname> <port> put <filename>")
server_addr = (sys.argv[1], int(sys.argv[2])) 
request_type_str = str(sys.argv[3])
server_addr_str = str(server_addr)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def verify_acknowledgement(message, message_type):
    if message.decode() != "ack":
        print("Server did not acknowledge the " + message_type + " message. Exiting...")
        exit(1)
    elif message_type != "content":
        print(message_type + " sent")
    else:
        print(message_type + " received")


try:
    print("Connecting to " + server_addr_str + "... ")
    client_socket.connect(server_addr)
except Exception as e:
    print(e)
    exit(1)
    
    
try:
    while True:
        request_type_sent = send_one_message(client_socket, request_type_str)
        verify_acknowledgement(client_socket.recv(1024), "request-type")


        if request_type_str == "list":
            verify_acknowledgement(client_socket.recv(1024), "files")
            files = recv_one_message(client_socket).decode()
            print("files: ", files)
            break
            

        else:
            filename_str = str(sys.argv[4])
            filename_sent = send_one_message(client_socket, filename_str) 
            verify_acknowledgement(client_socket.recv(1024), "filename")
        if request_type_str == "put":  
            file_path = get_path("client_data", True) + "/" + filename_str
            data_sent = handle_request(request_type_str, file_path, client_socket)
            print("file sent successfully. Exiting...")
            break

        elif request_type_str == "get":
            verify_acknowledgement(client_socket.recv(1024), "content")
            content = recv_one_message(client_socket).decode()
            print("file name: ", filename_str)
            file_path = get_path("client_data", True) + "/" + filename_str
            print("file path: ", file_path)
            new_file = write_to_file(file_path, content)
            break



            

finally:
    client_socket.close()
exit(0)
         
