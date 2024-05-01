import sys
import socket
import os
import struct



def socket_to_memory(socket, socket_address):
    print(socket_address + ": ", end="", flush=True)
    data = bytearray(1)
    bytes_read = 0
    while len(data) > 0:
        data = socket.recv(4096)
        print(data.decode(), end="") 
        bytes_read += len(data)
    return bytes_read

 
    


def handle_request_client(request_type_str, file_path, socket):
    match request_type_str:
        case "put":
            send_one_data_message(file_path, socket)
        case "get":
           # file_path = get_path(file_name_str, "server_data", False) + "/" + file_name_str
           # download_file(file_path, socket)
            print("file downloaded")
        case "list":
            view_files()
        case "EXIT":
            return 0


def send_one_message(socket, data):
    length = len(data)
    socket.sendall(struct.pack('!I', length))
    socket.sendall(str.encode((data)))

def send_one_data_message(file_path, socket):
    data = open_file(file_path)
    print("data: ", data)
    length = len(data)
    print("length: ", length)
    socket.sendall(struct.pack('!I', length))
    print(struct.pack('!I', length))
    socket.sendall(str.encode((data)))

def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def download_file(file_path, socket): #write to a file stuff
    print("file path: ", file_path)
    content = recv_one_message(socket).decode()
    print("content: ", content)
    downloaded_file = write_to_file(file_path, content)
    if downloaded_file:
        print(f"File '{file_name}' downloaded successfully")
    else:
        print(f"Error downloading file '{file_name}'")

def view_files(): #not sure yet
    return 0


def get_path(file_name_str, dir_name, parent):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if parent == True:
        relative_path = os.path.join("..", dir_name, file_name_str)
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
            
def open_file(file_name):
    try:
        with open(file_name, 'r') as reader:
            data = reader.read()
            return data
    except Exception as e:
        print("Error while opening file:", e)
        return None