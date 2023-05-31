#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import random
import pygame
import math

CZ = 3 * math.pi / 4 # to adjust for screen
# rotate(r, 100, cx, cy)
# r = radians

def rotate(r, size, cxy):
    r0 = r - CZ
    
    x = math.cos(r0) * size - math.sin(r0) * size + cxy[0]
    y = math.sin(r0) * size + math.cos(r0) * size + cxy[1]

    x = int(x)
    y = int(y)
    return (x,y)


def convert_color(color_str):
    clr = (0, 0, 0)
    if not color_str:
        return get_rgb()

    if not color_str.startswith("#"):
        color_str = "#" + color_str
    
    clr = pygame.Color(color_str)

    return clr


def get_coco_rgb():
    """
TRS-80 Color Computer colors
black text = 183018
green      = 00ff00 cls(1)
yellow     = ffff44 cls(2)
blue       = 2211bb cls(3)
red        = bb0022 cls(4)
white      = ffffff cls(5)
cyan       = 00dd66 cls(6)
pink       = ff11ff cls(7)
orange     = ff4400 cls(8)

    """

    rgb = random.choice(["#000000", "#00ff00", "#ffff44", "#2211bb", "#bb0022", "#ffffff", "#00dd66", "#ff11ff", "#ff4400"])

    return convert_color(rgb)

def get_rgb():
    rgb = (random.randint(1,255), random.randint(1,255), random.randint(1,255))
    return rgb 



