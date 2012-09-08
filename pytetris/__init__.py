# coding:utf-8
import pygame
from pygame.locals import *
import copy
import time
import numpy as np
from random import *

import view
import model
from const import *
from piece import Piece
import param
                        
def draw():
    map_new = copy.deepcopy(const.map)
    for i in range(len(model.p.shape[0])):
        for j in range (len(model.p.shape[0][i])):
            if model.p.shape[0][i][j]:
                map_new[model.p.y+i][model.p.x+j] = model.p.shape[1]
    view.renderMap(map_new)
    view.renderScore(param.score)
    pygame.display.update()

    
def getBoard():
    map_new = copy.deepcopy(const.map)
    for i in range(len(map_new)):
        for j in range(len(map_new[i])):
            if map_new[i][j] != 0:
                map_new[i][j] = 1
    return map_new

def getScore():
    return param.score

def answer(state_map, state_piece, x, dx, rad):
    map_tmp = copy.deepcopy(const.map)
    for i in range(len(state_map)):
        if state_map[i] != 0:
            map_tmp[state_map[i]][i] = 1

    p_tmp = Piece(state_piece, x)
    p_tmp.updateMap(map_tmp)
    gain = 0

    if dx>0:
        for i in range(dx):
            p_tmp.move('right')
    else:
        for i in range(-dx):
            p_tmp.move('left')
    for i in range(rad):
        p_tmp.rotate('ccw')
    p_tmp.drop()

    for i in range(len(p_tmp.shape[0])):
        for j in range(len(p_tmp.shape[0][i])):
            if p_tmp.shape[0][i][j]:
                map_tmp[p_tmp.y+i][p_tmp.x+j] = p_tmp.shape[1]

    erasable = []
    for i in range(len(map_tmp)-1):
        flag_full = True
        for j in range(1,len(map_tmp[i])-1):
            if map_tmp[i][j] == 0 or map_tmp[i][j] == 8: flag_full = False
        if flag_full:
            erasable.append(i)
    if len(erasable) == 0:
        gain = 0
    else:
        gain = scores[min(len(erasable)-1, 3)]
    for i in erasable:
        for j in range(i-2):
            map_tmp[i-j] = copy.deepcopy(map[i-j-1])

    for i in range(len(map_tmp)):
        for j in range(len(map_tmp[i])):
            if map_tmp[i][j]!=0:
                map_tmp[i][j] = 1
    return [map_tmp, gain]

# def answer(state_map, state_piece, x, dx, rad):
#     map_tmp = copy.deepcopy(state_map)
#     p_tmp = Piece(state_piece, x)
#     p_tmp.updateMap(map_tmp)
#     gain = 0
    
#     if dx>0:
#         for i in range(dx):
#             p_tmp.move('right')
#     else:
#         for i in range(-dx):
#             p_tmp.move('left')
#     for i in range(rad):
#         p_tmp.rotate('ccw')
#     p_tmp.drop()

#     for i in range(len(p_tmp.shape[0])):
#         for j in range(len(p_tmp.shape[0][i])):
#             if p_tmp.shape[0][i][j]:
#                 map_tmp[p_tmp.y+i][p_tmp.x+j] = p_tmp.shape[1]

#     erasable = []
#     for i in range(len(map_tmp)-1):
#         flag_full = True
#         for j in range(1,len(map_tmp[i])-1):
#             if map_tmp[i][j] == 0 or map_tmp[i][j] == 8: flag_full = False
#         if flag_full:
#             erasable.append(i)
#     if len(erasable) == 0:
#         gain = 0
#     else:
#         gain = scores[min(len(erasable)-1, 3)]
#     for i in erasable:
#         for j in range(i-2):
#             map_tmp[i-j] = copy.deepcopy(map[i-j-1])

#     for i in range(len(map_tmp)):
#         for j in range(len(map_tmp[i])):
#             if map_tmp[i][j]!=0:
#                 map_tmp[i][j] = 1
#     return [map_tmp, gain]
    
    
    
    
def init(gravity):
    reload(const)
    reload(param)

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption(u"TETRIS")

    model.p = Piece()
    model.p_next = Piece()

    view.renderNext(model.p_next)
    param.score = 0
    
    clock = pygame.time.Clock()
    param.t['dropped'] = param.t['moved'] = param.t['rotated'] = \
    param.t['stopped_moving'] = param.t['stopped_rotating'] \
        = time.clock()
    param.interval['gravity'] = gravity
    pygame.key.set_repeat(150, 40)

def tick():
    param.t['now'] = time.clock()
    pygame.time.Clock().tick(600)

def alive():
    return not param.flag['gameover']
    
def loop():
    tick()
    if param.flag['erase']:
        model.erase()
        pass
    elif param.flag['update']:
        for i in range(len(model.p.shape[0])):
            for j in range (len(model.p.shape[0][i])):
                if model.p.shape[0][i][j]:
                    const.map[model.p.y+i][model.p.x+j] = model.p.shape[1]
        model.checkErase()
        model.p= copy.deepcopy(model.p_next)
        model.p.updateMap(const.map)
        model.p_next = Piece()
        view.renderNext(model.p_next)
        param.flag['update'] = False
        param.flag['ground'] = False
    elif param.flag['gameover']:
        print('oh no')
    else:
        model.getKey(model.p)
        if (param.t['now']-param.t['dropped'])> param.interval['gravity']:
#            param.t['dropped'] = param.t['now']
            if param.flag['ground']:
                if param.t['now']-param.t['moved'] < param.interval['gravity']\
                or param.t['now']-param.t['rotated'] < param.interval['gravity']:
                    pass
                else:
                    param.flag['update'] = True
            else:
                model.p.move('down')
        else:
            pass

    model.p.checkGround()
    model.checkGameover()
    draw()
    
def quit():        
    pygame.quit()
    
def getPiece():
    return [model.p.shape[1], model.p.shape[0], model.p.x, model.p.y]
def getNextPiece():
    return [model.p_next.shape[1], model.p_next.shape[0], model.p_next.x, model.p_next.y]

def move(dir):
    if(dir=='left'): model.p.move('left')
    elif(dir=='right'): model.p.move('right')
    elif(dir=='down'): model.p.move('down')

def drop():
    model.p.drop()

def rotate(dir):
    if(dir=='cw'): model.p.rotate('cw')
    elif(dir=='ccw'): model.p.rotate('ccw')
            
if __name__ == '__main__':
    init(0.3)
    while alive():
        loop()
    quit()
    
