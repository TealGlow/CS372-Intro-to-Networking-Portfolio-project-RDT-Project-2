# Networking-RDT-Project-2

Not the best but it simulates client sending data to a server using RDT.

<strong>Alyssa Comstock
<br/>
CS372 - Intro to Computer Networking
<br/>
Project 2 - RDT Layer</strong>
<br/>

Notes:
- Developed in PyCharm Community Edition.
- Using Python 3.9 Interpreter.
- By default it is set so that all the options are turned on and the largest text is being sent.

How it works:
- Sends a number of packages within its window (window size of 4 packages)
- Waits for server ack back
- If no ack is received within a frame of a few iterations the window of 4 packages is sent again.
- If the ack does not match the expected ack, then the entire window is sent again.
- If the expected ack matches the ack we receive, then we advance the window and send the new window.
- Items are added to the server data variable with their sequence number attached in an array for easy sorting in the end so that out of order and delayed packages are not as much of a problem.
