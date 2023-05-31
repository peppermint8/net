#!/usr/bin/env python
#! -*- coding: utf-8 -*-

"""
https://realpython.com/python-sockets/

Beavis & Butthead server

- connect
- recv: {"p1": (x,y), "p2": (x,y)}
- send: {"p1": (x,y), "p2": (x,y)}
- close


"""

import socket
import sys
import bson


host = "127.0.0.1"
host = "" # everyone
port = 8002
exit_flag = False
data_size = 1024

cnt = 0

print("Starting game server: {}:{}".format(host, port))

p1 = {"x": -1, "y": -1} # Beavis
p2 = {"x": -1, "y": -1} # Butthead


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

        print("- received: {}".format(data_json))

        #g = int(data_json.get("guess", -1))
        if data_json.get("p1-x", -1) > -1:
            p1['x'] = data_json.get("p1-x", -1)
        if data_json.get("p1-y", -1) > -1:
            p1['y'] = data_json.get("p1-y", -1)
        
        if data_json.get("p2-x", -1) > -1:
            p2['x'] = data_json.get("p2-x", -1)
        if data_json.get("p2-y", -1) > -1:
            p2['y'] = data_json.get("p2-y", -1)

        send_json = {"p1-x": p1['x'], "p1-y": p1['y'], "p2-x": p2['x'], "p2-y": p2['y']}

        # thinking
        #time.sleep(1)

        conn.sendall(bson.encode(send_json))


    conn.close()

    print("Closing connection to {}".format(addr))
    #if cnt >= 5:
    #    exit_flag = True


s.close()

print("Server closed")

sys.exit(0)