# Network (sockets) 

Testing sending data across a network (localhost)
- could be more complicated across the internet

https://realpython.com/python-sockets/
https://docs.python.org/3/howto/sockets.html


Using python 3.10 & pygame & bson & sockets

## N1 & N2

Pick a number server (n1) and client (n2)
- the old pick a number between 1 & 100, the server answers "higher", "lower" or "correct"

$ ./n1.py - listens on port 8002
- receives bson data on the guess
- returns bson data on the result 
- shuts down after 5 connects

$ ./n2.py - connects to n1
- sets up a new game 
- sends the guesses until we get a correct guess

## MyNet

Uses pygame to move pngs around the screen with the mouse.
- each instance sends the position of the player to the "BB" server
- BB server returns the positions
- the "mynet" game moves the other player into the new position

3 shells:
1$ ./bb.py # listens on port 8002
2$ ./mynet.py beavis.yaml # starts game as Beavis
3$ ./mynet.py butthead.yaml # starts game as Butthead

moving the mouse around to move Beavis or Butthead will move them in the other window also

Some config options in beavis.yaml and butthead.yaml

