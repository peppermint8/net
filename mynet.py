#!/usr/bin/env python
#! -*- coding: utf-8 -*-

"""
multi-player game in python
- experimenting with sockets & networks 

open 3 shells:
- run ./bb.py first (server that stores positions) in the first shell
- run ./mynet.py beavis.yaml in the second shell
- run ./mynet.py butthead.yaml in the third shell

Beavis or Butthead moves around in both windows because each "mynet" 
opens a socket to bb.py, sends the position of the player and then receives the 
position of the players

I don't like opening & closing the socket many times.  
- to do - work on server that accepts multiple connections

"""

import sys
import os
import yaml
import pygame
import socket
import bson

from pygame.locals import *

from player import Player
from common import get_rgb, convert_color, get_coco_rgb, rotate


def init_screen():
    max_x = game_config.get("window_x", 800)
    max_y = game_config.get("window_y", 600)
    
    # init screen - should do this all before this
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    
    pygame.init()
    screen = pygame.display.set_mode((max_x, max_y))

    #game_icon = pygame.image.load(os.path.join(img_path, "101664.png"))
    #pygame.display.set_icon(game_icon)
    pygame.display.set_caption(game_config.get("title"))

    #pygame.mouse.set_visible(False)
    #pygame.event.set_grab(True) 
    
    return screen


def net_game(screen, pid):

    max_x = game_config.get("window_x", 600)
    max_y = game_config.get("window_y", 600)
    
    clock_tick = 15
    #pygame.key.set_repeat(1, 500)

    screen_top_left_px = (0,10)
    screen_bottom_right_px = (max_x, max_y-25)

    
    clock = pygame.time.Clock()

    bg = pygame.Surface(screen.get_size())
    bg = bg.convert()

    background_color = convert_color(game_config.get("background_color", "#000000"))
    bg.fill(background_color)

    p1_pos = (max_x // 4, max_y // 2)
    p1 = Player(p1_pos, screen_top_left_px, screen_bottom_right_px)
    p1.velocity = game_config.get("player", {}).get("velocity", 30)
    p1.img = "resources/beavis.png"
    p1.sound = "resources/beavis.mp3"

    p1.pygame_img = pygame.image.load(p1.img)
    p1.pygame_img = pygame.transform.scale(p1.pygame_img, (43,80))
    p1.pygame_snd = pygame.mixer.Sound(p1.sound)

    p2_pos = (3*max_x // 4, max_y // 2)
    p2 = Player(p2_pos, screen_top_left_px, screen_bottom_right_px)
    
    #p2 = Player(p1_pos, screen_top_left_px, screen_bottom_right_px)
    p2.velocity = game_config.get("player", {}).get("velocity", 30)
    p2.img = "resources/butthead.png"
    p2.sound = "resources/butthead.mp3"

    p2.pygame_img = pygame.image.load(p2.img)
    p2.pygame_img = pygame.transform.scale(p2.pygame_img, (43,80))
    p2.pygame_snd = pygame.mixer.Sound(p2.sound)



    done = False
    loop_cnt = 0

    data_size = 1024
    my_host = "127.0.0.1"
    my_port = 8002


    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    while not done:

        loop_cnt += 1

        bg.fill(background_color)

        
        p1.move()
        p2.move()


        # draw beavis
        bg.blit(p1.pygame_img, p1.px) 
        # draw butthead
        bg.blit(p2.pygame_img, p2.px) 

        screen.blit(bg, (0, 0))
        pygame.display.flip()

        clock.tick(clock_tick) 

     
        # connect to bb server, send p1 or p2 position
        # get position of players
        # set new position of other player   
        s_flag = False
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((my_host, my_port))
            s_flag = True
        except ConnectionRefusedError:
            print("Cannot connect to: {}:{}".format(my_host, my_port))

        if s_flag:
            if pid == 1:
                d = {"p1-x": p1.px[0], "p1-y": p1.px[1]}
            else:
                d = {"p2-x": p2.px[0], "p2-y": p2.px[1] }
        
            
            s.sendall(bson.encode(d))
            data = s.recv(data_size)
            data_json = {}
            if data:
                data_json = bson.decode(data)
                #print(data_json)
                if pid == 1:
                    p2.netmove(data_json.get("p2-x", -1), data_json.get("p2-y", -1))
                else:
                    p1.netmove(data_json.get("p1-x", -1), data_json.get("p1-y", -1))
            s.close()


        for event in pygame.event.get():
            mm = pygame.mouse.get_pos()
            if pid == 2:
                p2.movement(mm)
            else:
                p1.movement(mm)


            if event.type == pygame.MOUSEBUTTONUP:
                mpos = pygame.mouse.get_pos()     
                

                # 7 = top button, 6 = bottom button

                # 3 = right, 2 = scroll wheel
                if event.button == 1:
                    if pid == 2:
                        pygame.mixer.Sound.play(p2.pygame_snd)
                    else:
                        pygame.mixer.Sound.play(p1.pygame_snd)
                if event.button == 3:
                    pass

            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True

    
    del p1
    del p2





if __name__ == '__main__':

    config_file = "beavis.yaml"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    print("Loading game config: {}".format(config_file))
    # option to load another config from sys.arg[1]

    if not os.path.isfile(config_file):
        print("Cannot find config: {}".format(config_file))
        sys.exit(1)
    
    with open(config_file, "r", encoding="utf-8") as fh:
        try:
            game_config = yaml.load(fh, Loader=yaml.FullLoader)
        except yaml.scanner.ScannerError as err: 
            print("Config file error: {}".format(err))
            sys.exit(1)

    # pid = player id
    pid = game_config.get("pid", 1)    

    screen = init_screen()
    net_game(screen, pid)

    sys.exit(0)