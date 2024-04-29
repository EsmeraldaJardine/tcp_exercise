# Some Hints and Tips for Assessed Exercise 2

The handout has a lot of this information already, so there's some redundancy here. I am highlighthing these points as based on past experience these are more often overlooked.

## The Code
 
+ This is a non-trivial coursework, and among other challenges, there are a few aspects left un-prescribed and open-ended in the handout, but that you are expected to encounter and handle. This actually reflects the nature of real software projects quite well!

+ Problem set 4.2 in B3 (and it's model solution) is your friend! You can use that working client-server application as the starting point, and then work from there. Or, maybe you feel writing code from scratch is cleaner, but keep that solution handy for reference. 

+ Perhaps the trickiest part, and in fact one of the key goals of the "application protocol" is to deal with the recv() and send() functions, which do not return a predictable number of bytes. So you may have to keep calling them repeatedly until you get the expected number of bytes (which means you need to first know how many bytes you are expecting). Sending is easier as in addition to send(), there's a sendall() function as well. 
Here's an article that you might find useful:
http://stupidpythonideas.blogspot.com/2013/05/sockets-are-byte-streams-not-message.html

+ The code will be tested with both small and large (a few GBs) file sizes. One of the most common errors is writing code that is limited to files up to a certain size (e.g. 1024 bytes), with anything larger automatically truncated. Some file limit is inevitable, but it should be some non-arbitrary, reasonable limit (e.g. file size that can be defined in a certain number of bytes). I will test with file sizes of up to 4 GB when marking this.

+ Following on from the previous point, a "sensible" protocol design, well documented, is a key requirement. Using some kind of encoding for commands and errors as part of the application protocol makes a lot of sense.

+ The code will also be tested with transferring binary files, which means they must be opened the right way.

+ Something the keep in mind is that even though you are writing a client-server application, for the purpose of this assessment, they will both be running on the same machine, and we'll be "pretending" they are two separate machines running the client the server respectively. To achieve this pretense, you should create separate "server_data" and "client_data" folders, so that there's no confusion about which file is on which "machine". See handout for more details.

+ Be careful and defibrate about handling folder structures. The "list" command should list the contents of the "server_data" folder as that is the folder of interest in this context. 

+ Related to the previous two points, you should be careful that the pretense of server and client scripts being on separate machines is maintained. This means you should never directly access the "server_data" folder directly from the client.py script (or vice-versa), and any communication between client and server --- including file transfers --- should be strictly over TCP calls (because that is the only way available in real-life when client and server scripts are running on separate machines).

+ Using "with" to open files is good practice.
https://realpython.com/read-write-files-python/
 
+ Helpful and appropriate messages printed on the screen on both sides is good practice.

+ Command line argument handling is an another important focus point. Are you following the API exactly as stated in the handout? Are you checking for correct number/type of arguments? Are you giving appropriate error messages?

+ All socket calls [not just connect()] are best placed inside try blocks for graceful handling of TCP related errors. There is no single scheme for doing this, but you can try (no pun intended) experimenting with nested try blocks.

+ There is enough common functionality encountered on both the server and client side scripts to warrant a shared module capturing all those functions (this is indicated in the handout as well). 

+ Modularity: The code has enough clearly identifiable and differentiated functionalities to warrant modular, structured code, with e.g. separate functions for put, get, list. See the lab B3 solution for some hints.

+ Use block comments at the top of functions to explain what they are doing. The use of "docstrings" may be warranted specially for those functions that are re-used across client and server.

## The Report

+ In your report, don't focus too much on details of the implementation (i.e., the code). What is of primary interest for the report is the _application protocol_. That is, what kind of messages are transferred between client and hosts, and in what sequence? Why did you decide to have those messages? How did you ensure exact number of bytes are sent/received? How do you handle and communicate errors, corner cases? 

+ It's good practice to add comments along the lines of "how to use this" with your submitted code (and/or report). The point is, best not to presume the user of your code knows how to use it already.

+ Don't worry too much about the size of the report. The main thing is whether you've addressed the information expected in the report, as stated in the handout, i.e.:

"a description of the application-level protocol you designed (exact format of the exchanged messages, their fields and semantics, the order in which these messages are expected to be exchanged, etc.) and a discussion of the reasoning behind the design of your protocol and the associated design decisions."

I've seen very good reports written up in a couple of pages, and longer ones with a lot of fluff and lacking essentials.

+ While this is not a requirement, simple diagram(s) to illustrate your application level protocol is a good idea; e.g. maybe a "sequence diagram" showing the sequence of interactions between client and server.