#!/usr/bin/env python
#! -*- coding: utf-8 -*-

"""
https://realpython.com/python-sockets/
guess a number server
netstat -an

question, answer
- chat

BrokenPipeError


"""

import socket
import random
import time
import sys
import bson


host = "127.0.0.1"
host = "" # everyone
port = 8002
exit_flag = False
data_size = 1024

cnt = 0

print("Starting game server: {}:{}".format(host, port))

xmin = 1
xmax = 100
r = random.randint(xmin, xmax)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

while not exit_flag:

    s.listen()
    print("... waiting for connection ...")
    conn, addr = s.accept()
    cnt += 1

    print("{}: Connected to: {}".format(cnt, addr))

    done = False
    while not done:
        
        data = conn.recv(data_size)
        #print(data, type(data))
        
        data_json = {}
        if data:
            try:
            
                #data_json = bson.BSON.decode(data, codec_options=options)
                data_json = bson.decode(data)
            except bson.errors.InvalidBSON:
                # eoo error??
                print("- error: bad data = {}".format(data, type(data)))
                
        else:
            done = True

        #print("- received: {}".format(data_json))

        g = int(data_json.get("guess", -1))

        answer = ""
        send_json = {}

        
        

        if data_json.get("xmin", 0) > 0 or data_json.get("xmax", 0) > 0:
            xmin = data_json.get("xmin", 1)
            xmax = data_json.get("xmax", 100)
            
            r = random.randint(xmin, xmax)
            print("new game:  [{} .. {}], answer = {}".format(xmin, xmax, r))
            send_json = {"new_game": True}
        

        if g > -1:
            
            if g > r:
                answer = "lower"
            elif g < r:
                answer = "higher"
            else:
                answer = "correct"
            send_json = {"answer": answer}        

            print("guess: {}".format(g, answer))
        
        

        # thinking
        #time.sleep(1)

        conn.sendall(bson.encode(send_json))


    conn.close()

    print("Closing connection to {}".format(addr))
    if cnt >= 5:
        exit_flag = True


s.close()

print("Server closed")

sys.exit(0)