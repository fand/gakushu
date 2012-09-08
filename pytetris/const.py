# coding:utf-8
import pygame
from pygame.locals import *
import copy
import time
import numpy as np
from random import *

WIDTH = 4;#10
HEIGHT = 6;#20
SCREEN_SIZE = (420,420)

map = [[8,0,0,0,0,8],
       [8,0,0,0,0,8],
       [8,0,0,0,0,8],
       [8,0,0,0,0,8],
       [8,0,0,0,0,8],
       [8,0,0,0,0,8],
       [8,0,0,0,0,8],
       [8,0,0,0,0,8],
       [8,8,8,8,8,8]]


# map = [[8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,0,0,0,0,0,0,0,0,0,0,8],
#        [8,8,8,8,8,8,8,8,8,8,8,8]]

shape = {
    0: [np.array([[0,0,0,0,0],[0,0,0,0,0],[0,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0]]),1], #cyan
    1: [np.array([[1,1],[1,1]]),2],#yellow
    2: [np.array([[0,0,0],[1,1,1],[0,1,0]]),3],#'violet
    3: [np.array([[1,1,0],[0,1,1],[0,0,0]]),4],#'red'
    4: [np.array([[0,1,1],[1,1,0],[0,0,0]]),5],#'green'
    5: [np.array([[0,0,0],[1,1,1],[1,0,0]]),6],#'orange'
    6: [np.array([[0,0,0],[1,1,1],[0,0,1]]),7]#'blue'
    }

colors = []
black = pygame.Surface([18,18])
black.fill([0,0,0])
colors.append(black)
cyan = pygame.Surface([18,18])
cyan.fill([190,190,255])
colors.append(cyan)
yellow = pygame.Surface([18,18])
yellow.fill([255,155,128])
colors.append(yellow)
violet = pygame.Surface([18,18])
violet.fill([255,128,200])
colors.append(violet)
red = pygame.Surface([18,18])
red.fill([255,128,128])
colors.append(red)
green = pygame.Surface([18,18])
green.fill([128,255,128])
colors.append(green)
orange = pygame.Surface([18,18])
orange.fill([255,200,128])
colors.append(orange)
blue = pygame.Surface([18,18])
blue.fill([128,128,255])
colors.append(blue)
gray = pygame.Surface([18,18])
gray.fill([100,100,100])
colors.append(gray)
white = pygame.Surface([18,18])
white.fill([40,40,40])
colors.append(white)

scores = [40,100,300,1200]
