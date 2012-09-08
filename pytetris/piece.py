import const 
import numpy as np
from random import *
import copy
from var import *
import param

shape = {
    0: [np.array([[0,1],[1,1]]),1],
    1: [np.array([[0,1],[0,1]]),4]#yellow
    }

# shape = {
#     0: [np.array([[0,0,0,0,0],[0,0,0,0,0],[0,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0]]),1], #cyan
#     1: [np.array([[1,1],[1,1]]),2],#yellow
#     2: [np.array([[0,0,0],[1,1,1],[0,1,0]]),3],#'violet
#     3: [np.array([[1,1,0],[0,1,1],[0,0,0]]),4],#'red'
#     4: [np.array([[0,1,1],[1,1,0],[0,0,0]]),5],#'green'
#     5: [np.array([[0,0,0],[1,1,1],[1,0,0]]),6],#'orange'
#     6: [np.array([[0,0,0],[1,1,1],[0,0,1]]),7]#'blue'
#     }

class Piece():
    def __init__(self, state_shape = None, x = None):
        if state_shape is None:
            self.type = randint(0,1)#randint(0,6)
            self.shape = shape[self.type]
        else:
            # detect self.type from state_shape
            tmp = np.array(state_shape)
            for i in range(3):
                for s in range(len(shape)):
                    flag = False
                    if len(shape[s][0])==len(tmp):
                        flag = True
                    for j in range(len(shape[s][0])):
                        flag = flag and (tmp[j]==shape[s][0][j]).all()
                    if flag:
                        self.type = s
                tmp = np.rot90(tmp)
            self.shape = [np.array(state_shape), self.type+1]
                
        self.x = 3 + int(len(self.shape[0]) / (-2)) if x is None else x
        self.y = 2 + int(len(self.shape[0]) / (-2))
        # self.x = 6 + int(len(self.shape[0]) / (-2)) if x is None else x
        # self.y = 3 + int(len(self.shape[0]) / (-2))
        self.map = const.map
#        for i in range(randint(0,4)):
#            self.rotate('cw')

    def updateMap(self, newmap):
        self.map = newmap
        
    def isMovable(self,dir):
        for i in range(len(self.shape[0])):
            for j in range(np.size(self.shape[0][i])):
                if self.shape[0][i][j]:
                    if dir == 'left':
                        if self.map[self.y+i][self.x+j-1] != 0: return False 
                    if dir == 'right':
                        if self.map[self.y+i][self.x+j+1] != 0: return False 
                    if dir == 'down':
                        if self.map[self.y+i+1][self.x+j] != 0: return False 
        return True
    
    def move(self,dir):
        if self.isMovable(dir):
            if dir == 'left': self.x -= 1 
            if dir == 'right': self.x += 1 
            if dir == 'down': self.y += 1
        param.flag['moved'] = True
#        param.flag['update'] = False
            
    def rotate(self,rad):
        if rad == 'ccw':
            tmp = np.rot90(self.shape[0])
        elif rad == 'cw':
            tmp = np.rot90(self.shape[0],3)
        x_tmp = copy.copy(self.x)
        y_tmp = copy.copy(self.y)
        offset = 0
        while offset < 4:
            cleared = True
            for i in range(len(tmp)):
                for j in range(len(tmp[i])):
                    if tmp[i][j]:
                        if y_tmp+i<0:
                            y_tmp += 1
                            cleared = False
                            continue
                        elif y_tmp+i>21:
                            y_tmp -= 1
                            cleared = False
                            continue
                        elif x_tmp+j<0:
                            if offset==0:
                                x_tmp += 1
                                offset = 1
                            cleared = False
                            continue
                        elif x_tmp+j>11:
                            if offset==1:
                                x_tmp -= 1
                                offset = 2
                            cleared = False
                            continue
                        elif self.map[y_tmp+i][x_tmp+j]!=0:
                            if offset == 0:
                                x_tmp+=1
                            elif offset == 1:
                                x_tmp-=2
                            elif offset == 2:
                                x_tmp+=1
                                y_tmp-=1
                            elif offset == 3:
                                y_tmp+=1
                            offset+=1
                            cleared = False
            if cleared:
                self.x = x_tmp
                self.y = y_tmp
                self.shape[0] = tmp
                offset = 100
                param.flag['moved'] = True
#                param.flag['update'] = False

        if param.flag['rotating'] == False: param.flag['rotating'] = True
#        print('hey')

    def drop(self):
        while self.isMovable('down'):
            self.y += 1
        param.flag['moved'] = True
        
    def checkGround(self):
        param.flag['ground'] = False
        for i in range(len(self.shape[0])):
            for j in range(len(self.shape[0][i])):
                if self.shape[0][i][j]:
                    if self.map[self.y+i+1][self.x+j]!=0:
                        param.flag['ground'] = True
                        
