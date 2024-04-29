import sys
import socket

def parse_port_arg():
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python server.py <port number>")
        sys.exit(1)

    # Get the port number from the command line argument
    port_num = int(sys.argv[1])

    # Check if the port number is within the valid range
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
    #