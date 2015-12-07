This first commit is a primarily working, though still rough commit
It offers the ability to communicate with the Echo server, but still needs work on the ability to run all as one process, right now requiring two processes simultaneously, one running the receiver, one running the send messages.
The Commenting is in need of well, any sort of being explained, and testing has been haphazard to this point, only communication with the Echo Server is achieved, though they seem to be successful.  The Encryption has been tested on only a few standard inputs, though feeding the encryption output
as the first argument of Decryption gets the correct results.  Also, the test of the 'Al Dakota guts' input with the specified key and IV worked as listed
on the testing page.  This is a rough initial commit, though mostly working.  Also, termination of the program is only offered through externally killing the idle window, not from within the program itself...
