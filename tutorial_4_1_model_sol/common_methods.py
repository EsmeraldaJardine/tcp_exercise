import sys
import socket
import os



def socket_to_memory(socket, socket_address):
    print(socket_address + ": ", end="", flush=True)
    data = bytearray(1)
    bytes_read = 0
    
    while len(data) > 0 and "\n" not in data.decode():
        data = socket.recv(4096)
        print(data.decode(), end="") 
        bytes_read += len(data)
    return bytes_read

 
def device_to_socket(socket):
    print("You: ", end="", flush=True) 
    user_request = input("send, download or view the server files (type EXIT to exit)")
    # if client socket
    handle_request_client(user_request, socket)
    # else: handle_request_server
    


def handle_request_client(request_type_str, file_name_str, socket):
    match request_type_str:
        case "put":
            send_file(file_name_str, socket)
        case "get":
            download_file()
        case "list":
            view_files()
        case "EXIT":
            return 0

def send_file(file_name_str, socket):
    file_path = get_path(file_name_str)
    data = open_file(file_path)
    bytes_sent = socket.sendall(str.encode(data)) # will need to be revised
    return bytes_sent

def download_file(): #write to a file stuff
    return 0

def view_files(): #not sure yet
    return 0


def get_path(file_name_str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    relative_path = os.path.join("..", "client_data", file_name_str)
    print(relative_path)
    absolute_path = os.path.normpath(os.path.join(current_dir, relative_path))
    print(absolute_path)
    if os.path.exists(absolute_path):
        return absolute_path #this is bugged
    else:
        print(f"The file '{file_name_str}' does not exist in directory '{os.path.dirname(absolute_path)}'")
        return None
    
def open_file(file_path):
    with open(file_path, 'r') as reader:
        data = reader.read()
        return data
            