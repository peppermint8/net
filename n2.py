#!/usr/bin/env python
#! -*- coding: utf-8 -*-

"""
guess the number between xmin and xmax

./n2.py
./n2.py 10.3.70.94


idea:
connect to server, make guess, receive answer, close connection
- allows multiple clients to connect quick and keep running w/o blocking

b & b server, store (char) position:
(char): x, y
where is (char2): x,y
close


"""

import socket
#import random
import sys
import bson
import time

host = "127.0.0.1"
port = 8002

if len(sys.argv) > 1:
    host = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
except ConnectionRefusedError:
    print("Cannot connect to: {}:{}".format(host, port))
    sys.exit(0)
finally:
    # do this regardless of if it worked or not
    print("-")
    
print("connected to: {}:{}".format(host,port))

xmin = 1
xmax = 100_000_000
data_size = 1024

new_game = True


print("Range: {} .. {}".format(xmin, xmax))




done = False
while not done:

    if new_game:
        
        d = {"xmin": xmin, "xmax": xmax}
        
        de = bson.encode(d)
        s.sendall(bson.encode(d))
        #print("send = {}".format(de))

        new_game = False

        # if don't receive, then n1 gets bad (eoo?) data
        data = s.recv(data_size)
        data_json = {}
        if data:
            data_json = bson.decode(data)
        if data_json.get("new_game", False):
            print("- New game!")


    else:


        g = (xmax - xmin) // 2 + xmin
        guess = {"guess": g}
        s.sendall(bson.encode(guess))

        data = s.recv(data_size)
        data_json = {}
        if data:
            data_json = bson.decode(data)
    
    

        answer = data_json.get("answer")

        print("guess: {}, answer: {}  [{}..{}]".format(g, answer, xmin, xmax))
    
    
        if answer == "higher":
            #g = g + 1
            xmin = g
            g = (xmax - xmin) // 2 + xmin
        elif answer == "lower":
            xmax = g
            g = (xmax - xmin) // 2 + xmin
        elif answer == "correct":
            done = True

        time.sleep(1)

s.close()

sys.exit(0)
