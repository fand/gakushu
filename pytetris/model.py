# coding:utf-8
import pygame
from pygame.locals import *
import copy
import time
import numpy as np
from random import *

import const
from piece import Piece
import param

p =  Piece(None,None)
p_next = Piece(None,None)


erasable = []


def getKey(p):
    keys = pygame.key.get_pressed()
    flag_noinput = [False,False]
    # 移動のキー
    if (param.t['now'] - param.t['moved']) > param.interval['move']:
        if keys[K_LEFT]:
            p.move('left')
            param.t['moved'] = param.t['now']
            if param.interval['move'] > 0.08: param.interval['move'] *= 0.5
        elif keys[K_RIGHT]:
            p.move('right')
            param.t['moved'] = param.t['now']
            if param.interval['move']>0.08: param.interval['move'] *= 0.5
        elif keys[K_UP]:
            p.drop()
            param.t['moved'] = param.t['now']
            if param.interval['move']>0.08: param.interval['move'] *= 0.5
        elif keys[K_DOWN]:
            p.move('down')
            if param.flag['ground'] == False:
                param.t['moved'] = param.t['now']
            if param.interval['move']>0.08: param.interval['move'] *= 0.5
        else:
            if param.interval['move'] < 0.3: param.t['stopped_moving'] = param.t['now']
            param.interval['move'] = 0.3
            flag_noinput[0] = True
    elif (param.t['now'] - param.t['stopped_moving'])<0.6 and param.interval['move'] == 0.3:
        if keys[K_LEFT]:
            p.move('left')
            param.t['moved'] = param.t['now']
            if(param.interval['move']>0.08): param.interval['move'] *= 0.5
        elif keys[K_RIGHT]:
            p.move('right')
            param.t['moved'] = param.t['now']
            if(param.interval['move']>0.08): param.interval['move'] *= 0.5
        elif keys[K_UP]:
            p.drop()
            param.t['moved'] = param.t['now']
            if param.interval['move']>0.08: param.interval['move'] *= 0.5
        elif keys[K_DOWN]:
            p.move('down')
            if param.flag['ground'] == False:
                param.t['moved'] = param.t['now']
            if(param.interval['move']>0.08): param.interval['move'] *= 0.5
        else:
            if(param.interval['move'] < 0.3): param.t['stopped_moving'] = param.t['now']
            param.interval['move'] = 0.3
            flag_noinput[0] = True
    # 回転のキー
    if (param.t['now'] - param.t['rotated']) > param.interval['rotate']:
        if keys[K_z]:
            p.rotate('ccw')
            param.t['rotated'] = param.t['now']
            if param.interval['rotate'] > 0.08: param.interval['rotate'] *= 0.5
        elif keys[K_x]:
            p.rotate('cw')
            param.t['rotated'] = param.t['now']
            if param.interval['rotate']>0.08: param.interval['rotate'] *= 0.5
        else:
            if param.interval['rotate'] < 0.3: param.t['stopped_moving'] = param.t['now']
            param.interval['rotate'] = 0.3
            flag_noinput[1] = True
    elif (param.t['now'] - param.t['stopped_moving'])<0.6 and param.interval['rotate'] == 0.3:
        if keys[K_z]:
            p.rotate('ccw')
            param.t['rotated'] = param.t['now']
            if(param.interval['rotate']>0.08): param.interval['rotate'] *= 0.5
        elif keys[K_x]:
            p.rotate('cw')
            param.t['rotated'] = param.t['now']
            if(param.interval['rotate']>0.08): param.interval['rotate'] *= 0.5
        else:
            if(param.interval['rotate'] < 0.3): param.t['stopped_moving'] = param.t['now']
            param.interval['rotate'] = 0.3
            flag_noinput[1] = True
    if flag_noinput[0] and flag_noinput[1]:
        param.flag['moved'] = False

def checkErase():
    global erasable
    for i in range(len(const.map)-1):
        flag_full = True
        for j in range(len(const.map[i])):
            if const.map[i][j]==0: flag_full=False
        if flag_full:
            erasable.append(i)
    if len(erasable)!=0:
        param.flag['erase'] = True

def erase():        
    global erasable
    param.score += const.scores[len(erasable)-1]
    for i in erasable:
        for j in range(i-2):
            const.map[i-j] = copy.deepcopy(const.map[i-j-1])
    erasable = []
    param.flag['erase'] = False

def checkGameover():
    f = False
    for i in const.map[3]:
        if i!=0 and i!=8: f = True
    param.flag['gameover'] = True if f else False
