import sys
import socket
import os



def socket_to_memory(socket, socket_address):
    print(socket_address + ": ", end="", flush=True)
    data = bytearray(1)
    bytes_read = 0
    while len(data) > 0:
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
            download_file(file_name_str, socket)
        case "EXIT":
            return 0

def send_file(file_name_str, socket):
    file_path = get_path(file_name_str, "client_data", True)
    bytes_sent = 0
    try:
        with open(file_path, 'r') as reader:
                print("...sending data...")
                data = reader.read(4096)
                socket.sendall(str.encode((data)))
                bytes_sent += len(data)
                return bytes_sent               
    except Exception as e:
        print("Error while sending file:", e)
        return 0

def download_file(file_name_str, socket): #write to a file stuff
    file_path = get_path(file_name_str, "server_data", False)
    try:
        with open(file_path, 'r') as reader:
                print("...sending data...")
                data = reader.read(4096)
                socket.sendall(str.encode((data)))
    except Exception as e:
        print("Error while sending file:", e)
        return 0

def get_path(file_name_str, dir_name, parent):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if parent == True:
        relative_path = os.path.join("..", dir_name)
    else:
        relative_path = os.path.join(dir_name)
    absolute_path = os.path.normpath(os.path.join(current_dir, relative_path))
    
    if os.path.exists(absolute_path):
        return absolute_path 
    else:
        print(f"The file '{file_name_str}' does not exist in directory '{os.path.dirname(absolute_path)}'")
        return None #error statement is only for sending files, not for receiving them
            

def write_to_file(file_name_str, content):
    try:
        with open(file_name_str, 'w') as writer:
            writer.write(content)
            return True
    except Exception as e:
        print("Error while writing to file:", e)
        return False
            


    