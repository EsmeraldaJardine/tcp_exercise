 
---
linkcolor: blue
---
# Assessed Exercise 2: Networking


The aim of this exercise is to have students use the knowledge they’ve acquired in this second part of the course, in the context of building a networked application. You will be using the *Python socket library* to create a simple, yet powerful, file service application. Your application will consist of two Python scripts: (a) a "server" that receives and serves client requests for files stored in a local directory, and (b) a "client" that allows the user to upload/download files from the server, as well as list the files currently stored on the server side.

## Python Sockets

An Internet socket is an abstract representation for the local endpoint of a network connection. Berkeley sockets is an API for Internet sockets, coined after the first implementation of sockets appeared in 4.2BSD (circa 1983). Over time, Berkeley sockets evolved to what is now known as POSIX sockets – an IEEE standard defined with the aim of maintaining compatibility and providing interoperability between operating systems. POSIX sockets can be used to communicate using a number of protocols, including (but not limited to) TCP, UDP, ICMP, SCTP and others.

The basic workflow for setting up a TCP connection to a remote host using POSIX sockets was outlined in the course lectures and in the last tutorial exercise (tutorial B3); please consult the lecture slides/recordings and lab handouts. For this assessed exercise you can use all methods provided by the basic Python socket library (`Lib/socket.py`). You are not allowed to use any other networking libraries that act as wrappers for socket.py (e.g., `Lib/socketserver.py`, `Lib/http/server.py`, `Lib/http/client.py`, `Lib/ftplib.py`, etc.). If you are thinking about using a Python library other than `Lib/socket.py`, `Lib/sys.py` or `Lib/os.py`, please *ask me first*!

## Server

The server will be a Python script, named `server.py`, executed through the command line interface. The current working directory of the server (i.e., the directory from where the server.py script is executed) will be used as the directory where files will be stored and served from. As your program needs to have write access to said directory, please make sure that, in your Windows command prompt window, you first change directory to someplace where you can store files, then execute your python script from there.

Your server should receive, as its single command line argument, its port number; that is, the server should be executed like so:

    python server.py <port number>

For example, assuming that M: is a drive where you have full write access:

    C:\Users\me> M: M:\> cd some_dir
    M:\some_dir> python server.py 6789

On startup, your server should create a TCP server socket, bind it to the user-defined port number (for the hostname use either "0.0.0.0" or an empty string, so as to bind to all available network interfaces on your host), report success (i.e., print a single-line message with its IP address and port number on the console and the text "`server up and running`"), and wait for client connections. For every incoming connection (as returned by `socket.accept()`) it should read and parse the request from the client, serve it accordingly, close the connection, report on its outcome (more on this shortly), and loop back to waiting for the next client connection.

Your server should be able to handle three types of requests:
	
1. *Uploading a file*: The client request should include, as a minimum, the request type and the filename to be used on the server side, and the data of the file. The server should then create the file (in <u>exclusive creation, binary mode</u>) and copy the data sent by the client from the socket to the file. To avoid accidents, the server should <u>deny overwriting existing files</u>.
	
2. *Downloading a file*: The client request should include, as a minimum, the request type and the filename of the file to be downloaded. The server should then open the file (in <u>binary mode</u>) and copy its data to the client through the socket.
	
3. *Listing of 1st-level directory contents*: The client request should indicate the request type. The server should then construct a list of the names of files/directories at the top level of its current working directory (e.g., using `os.listdir()`) and return it to the client over the socket. For the needs of this project, your server should not need to handle subdirectories; i.e., all files served and/or entries returned by `os.listdir()` should be those at the top level of the server’s current working directory.

In every case, the server should report (i.e., print on the console) information for every request <u>after its processing is over</u>. This report should be a <u>single line</u> including, at the very least, the IP address and port number of the client, information on the request itself (type and filename, as appropriate) and its status (success/failure). For failures, the report should also include an informative message indicating the type of error. Last, the server should also print informative messages for any other types of errors encountered throughout its execution (again, please only print a <u>single line</u> per error).

## Client

The client will be a Python script, named `client.py`, executed through the command line interface and receiving its arguments as command line arguments. The
first argument should be the address of the server (hostname or IP address) and the second argument should be the server’s port number. The next argument should be one of "`put`", "`get`" or "`list`"; these signify that the client wishes to send or receive a file, or request a directory listing, respectively. For "`put`" and "`get`" there should then be one more argument with the name of the file to upload/download respectively. That is, the client should be executed like so:

    python client.py <hostname> <port> <put filename|get filename|list>

For example:

    M:\some_dir> python client.py localhost 6789 put test1.txt 
    M:\some_dir> python client.py localhost 6789 get test2.txt
    M:\some_dir> python client.py localhost 6789 list

The client should parse its command line arguments and decide what operation is requested. It should then create a client socket, connect to the server defined in the command line, construct and send an appropriate request message, receive the server’s response, process it, and finally close the connection. The processing of requests will depend on the request type:
	
* Upload ("`put`") request: The client should, at the very least, open (in binary mode) the local file defined on the command line, read its data, send it to the server through the socket, and finally close the connection.
	
* Download ("`get`") request: The client should, at the very least, create the local file defined on the command line (in exclusive binary mode), read the data sent by the server, store it in the file, and finally close the connection. To avoid accidents, the client should deny overwriting existing files.
	
* Listing ("`list`") request: the client should, at the very least, send an appropriate request message, receive the listing from the server, print it on the screen one file per line, and finally close the connection.

In every case, the client should report information for every request; this report should be a <u>single line</u> of text including, at the very least, the IP and port number of the server, information on the request itself (type and filename, as appropriate), and its status (success/failure). For failures, the report should also include an informative message indicating the type of error (within the same single line).

## Miscellanea

Your client request and server response messages *may need to include additional fields to those outlined above*. The design of the *application-level protocol* (i.e., the types and formats of exchanged messages, and the exact semantics and order in which these messages are exchanged, and most importantly, *how errors are handled*) is left up to you and is an important component in the marking scheme of this assessed exercise.

As several pieces of the logic will be shared between client and server, you should try to abstract out the common pieces -- i.e., *define functions in a shared module, imported and used by both client and server*. For example:
	* `send_file(socket, filename)`: Opens the file with the given filename and sends its data over the network through the provided socket.
	* `recv_file(socket, filename)`: Creates the file with the given filename and stores into it data received from the provided socket.
	* `send_listing(socket)`: Generates and sends the directory listing from the server to the client via the provided socket.
	* `recv_listing(socket)`: Receives the listing from the server via the provided socket and prints it on screen.

These functions could then be used by both sides; e.g., for a "`put`" request, the client will use `send_file(…)` while the server will use `recv_file(…)`; vice-versa for a "`get`" request; the functions for the listings could internally also make use of the file functions; etc. Please make sure that your code is *well formatted and documented*, and that an *appropriate function/variable naming scheme* has been used. You won’t be assessed on the quality of your Python code per se, but a well written implementation is surely easier to debug (and mark).

## Folder management
You will be running both "client" and "server" on the same machine for this exercise. Since they will be using functions from a shared module, it’s probably easiest to place the client, server, and the shared module file in the same folder. However, both server and client will need to retain separate versions of their *data* files (that is, the files they are exchanging), even though they may have exactly same names. You can manage this by creating a sub-folder for client and server data files. Thus the suggested folder structure would be something like this:

    <project_folder>/
        server.py
        client.py
        common_utilitities.py
        server_data/
            ... data files on the server
    client_data/
            ... data files on the client


## What to submit

For this assessed exercise, *you can work on your own, or groups of two*. Submit a zip file `CANS2024-AE2-`*your-student-id*`.zip` via [the GA Workbook Moodle page](https://moodle.gla.ac.uk/mod/assign/view.php?id=4013663) with your Python source code files and your report as a README. The report should have a heading stating the full name(s) and matriculation number(s) of the team member(s), and include a detailed description of the application-level protocol you designed (exact format of the exchanged messages, their fields and semantics, the order in which these messages are expected to be exchanged, etc.) and a discussion of the reasoning behind the design of your protocol and the associated design decisions. Only *ONE (1)* submission should be done per team. Any one of the team members can upload the submission via their Moodle account. *Please make sure your submission clearly states the names of both students if you are submitting as a team of two.*

## How Exercise 2 will be marked

Following timely submission on Moodle, the exercise will be given a numerical mark, between 0 (no submission) and 100 (perfect in every way). These numerical marks will then be converted to a band (A1, A2, etc.). The marking scheme is given below:

* 70 marks for the implementation:
    * 15 marks for the implementation of the "list" request type and 25 marks for each of "put"/"get" request types, broken down as follows:
        * All request types:
            * 9 marks for handling the intricacies of TCP communication – i.e., that data is streamed from the source to the destination and hence data sent via a single `send()/sendall()` call may be fragmented and received across several sequential `recv()` calls, or data sent via multiple `send()/sendall()` calls may be collated and returned through a single `recv()` call. 
            * 3 marks for handling of connection failures mid-way through the protocol.
            * 2 marks for appropriate logging/reporting. 
            * 1 mark for parsing of command line arguments.
        * Only for "`put`"/"`get`" requests: 
            * 5 marks for correct handling/transferring of binary data (binary transfer, byte ordering, etc.). 
            * 5 marks for support for stability/security features such as very large files, 0-sized files, no overwriting of existing files, very long filenames, etc.
	* 5 marks for appropriate structure of your code (functions, minimal repetition of code, informative but not excessive comments, etc.).
* 30 marks for the report:
    * 20 marks for the quality of the design of the application-level protocol.
    * 10 marks for the discussion of the reasoning/design decisions.
