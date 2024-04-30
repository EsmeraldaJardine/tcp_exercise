import os

def find_absolute_path(filename):
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    # Construct the relative path to the file
    relative_path = os.path.join("client_data", filename)
    print(relative_path)
    # Join the current directory with the relative path to get the absolute path
    absolute_path = os.path.normpath(os.path.join(current_dir, relative_path))
    # Check if the file exists
    if os.path.exists(absolute_path):
        return absolute_path
    else:
        print(f"The file '{filename}' does not exist in directory '{os.path.dirname(absolute_path)}'")
        return None
    
def open_file(file_path):
    with open(file_path, 'r') as reader:
        data = reader.read()
        return data
        encoded_data = str.encode(data)
        
            

filename = "message.txt"
absolute_path = find_absolute_path(filename)
if absolute_path:
    print("Absolute path:", absolute_path)
open_file(absolute_path)
    



# client ttd:
# 1. ask client to upload, download or list the files to/in the server (switch-case)
# and send request to the appropriate handler (welcome message giving 
# the instructions on how to run the program)
#   1.1 obtain request_type and file_name from args
#   1.2 make a switch-case for handling different requests, send file_name to 
#       the appropriate function
# 
#
# 2. Handle uploading files ("put" request):
#   2.1 take the file_name and match it to the file in the client_data
#       2.1.1 find the absolute path of the client_data
#       2.1.2 iterate though the files in this directory
#       2.1.3 if file_name matches a file set this as the upload_file
#   2.2 encode the upload_file 
#       2.2.1 
#
#   2.3 send the encoded upload_file



# server ttd:
# 1. Handle the client connection and obtain the request type:
#   1.1  how does the server process the request-type argument from the client? .accept()?
#      
#   1.1 create a byte array to store the data??
#   1.2  recover the sent data .recv()
#   1.2 obtain the request type and request arguments from 
#
