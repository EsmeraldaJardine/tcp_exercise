( Esmeralda Jardine ; 2391491j )
( Dannielle Spears : 2959195s )

*** STATUS REPORT ***

[+] Program runs successfully
[+] All instructions (list, put, get) implemented
[+] Common errors handled, prints error message and closes connection both sides
[-] Files unable to be handled in pythons native file open() cannot be sent!
[BUG] Occasionally issue with connection closing properly, rerunning server with another port will close the initial port
To make program as close to how protocol works in real life, we implemented a 3-way handshake to initiate server-client connection
Client initializes connection by sending "syn" message, server checks receipt of syn, sends "syn/ack", client checks receipt of "ack"
Failure of handshake will result in closing connection with "Handshake failed" message

Connection is closed automatically on both ends after request has been handled
    (due to hardware limitations during development associated with long-running server loop)

Successful handshake will result in:
 + Client input arguments are checked to ensure correctness
 + Client sends request type (and filename if put/get) to server as per cli arg
 + File names are checked on start to ensure less than 100 characters
 + Server uses this to determine what action to perform (list, get, put)
 + list requests send equivalent of 'ls server_data' to client to be printed to user
 + if server received 'get' request, server handles it as 'put' for use in common_methods.py's methods
 + get/put requests are checked on sender end to ensure to sending of 0byte files

STABILITY / SECURITY FEATURES
 + Initial handshake
 + cli arg input errors
 + get/put requests will check on recipient end if filename exists in save dir and ensure saved filename is appended with unique number
   to prevent overwrites
 + attempting to send file types not natively handled will exit with appropriate error message

 DESIGN

 We tried to abstract many common methods (found in common_methods.py).
 Handshake was implemented in simplistic fashion due to time constraints - priority was to merely ensure adequate connection
 To mimic realistic protocol, we are sending in packets of fixed length (4) so that they can be unpacked correctly on receipt
    This also enables the recipient to know when datastream has finished and stop listening