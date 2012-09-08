# coding:utf-8

import pytetris as pt

import numpy
import random
import lists

# ε-greedy：テキストを参考に
def eGreedy(state):
	e = 1.0 #- εの値。繰り返しの回数に従って段々小さくする
	p = 0.0 #- 疑似乱数用変数。εを超えたら搾取
	proposed_actions = [] #- 行動パターンを格納するリスト

	#- 行動探査
	random.seed()
	while p < e:
		p = random.random()
		e *= 0.999
		a = make_action(state[1])
		proposed_actions.append(a)

	#- 行動の搾取
	a,val_a = pruning_action(state, proposed_actions)
	b,val_b = search_action(state)

	if b and val_b > val_a:
		return b
	else:
		return a

#- 行動の作成
def make_action(piece):
	#- lateral_times:	横移動回数
	#- rotate_times:	回転の回数

	random.seed()
	rotate_times = random.randint(0,3)
#	if rotate_times % 2:	min, max = -piece[2], piece[2]
#	else:	min, max = - piece[2] * 3 / 2, piece[2] * 3 / 2
#	if rotate_times % 2:	min, max = -4,4
	min, max = -2,2#-4,5
	lateral_times = random.randint(min,max)

	return [lateral_times, rotate_times]

#- rewardに応じてactionの枝刈り
def pruning_action(state, proposed_actions):
	#- board_state:	現在の盤面の状態
	#- max_r:	最大のreward
	#- max_a:	max_rを得る時のaction

	flag = 0
	actions = []

	for action in proposed_actions:
		reward, height = get_reward(state, action)
		if flag == 0:	max_r, min_h, flag = reward, height, 1
		if max_r < reward:
			max_r, min_h, actions = reward, height, [action]
		elif max_r == reward:
			if min_h == height:	actions.append(action)
			elif min_h < height:	actions, min_h = [action], height
	action = random.choice(actions)
	return action, max_r

#- rewardの取得
def get_reward(c_state, action):
	#- c_board_state:	現在の盤面の状態
	#- scores = [40, 100, 300, 1200]
	#- index: action_listの中でQを最大化するactionを示す番号
	c_board_state,piece = c_state
	n_board_state, line_reward = pt.answer(c_board_state, piece[1], piece[2], action[0], action[1])
	erace_line = line(line_reward)	#-	消したライン数
	block_reward = reward = 0
##	for i in range(0,len(n_board_state)):
##		for j in range(0,len(n_board_state[i])):
##			if n_board_state[i][j] != 0 and n_board_state[i][j] != 8:	n_board_state[i][j] = 1
	
	#- 一番下の空きスペースを埋めた分だけrewardを与える．隙間を作ったら減点
##	trans_c = zip(*c_board_state)
##	trans_n = zip(*n_board_state)
	max_h = 7#21

##	for width in range(1, 5):#11
##		r = 0

#		if trans_c[width][:22 - erace_line] != trans_n[width][erace_line:22]:
##                if trans_c[width][:8 - erace_line] != trans_n[width][erace_line:8]:
##			r = 3
#			l = [num for num in list(trans_n[width]) if num > 0]
#			max_1 = l[0]
#			start = list(trans_n[width]).index(max_1)
#			if l.count(0) + 2 <= len(l): max_2 = l[1]
#			else:	max_2 = 8
#			if max_2 == max_1:
#				max_2 = [num for num in list(trans_n[width]) if num != max_1 and num > 0][0]
#				print "max_1:",max_1,"max_2:",max_2
#			start = list(trans_n[width]).index(max_1)
#			final = list(trans_n[width]).index(max_2)

##			if [num for num in list(trans_n[width]) if num == 1] != []:
##				start = list(trans_n[width]).index(1)

##				r -= list(trans_n[width])[erace_line + start:].count(0)
##			else:	start = 8#22
##			r -= 6 - start#20
##			if max_h > start:
##				max_h = start
##		block_reward += r


        block_reward = 100/(numpy.max(c_board_state) - numpy.min(c_board_state))
        
	reward = block_reward + line_reward
	return reward, max_h

def line(line_reward):
	if line_reward == 0: return 0
	elif line_reward == 40: return 1
	elif line_reward == 100: return 2
	elif line_reward == 300: return 3
	elif line_reward == 1200: return 4
	else: print("erase_line error")

#- 履歴を参照し，最大のQとactionを返す
def search_action(state):
	max_q = -10
	max_a = []
	
	for i in lists.state_list:
		if i[0] == state[0]:
			i[1][1] = numpy.array(i[1][1])
			s = lists.state_list.index(i)
			if s + 1 <= len(lists.Qtable) and len(lists.Qtable[s])>0:
				max_q = max(lists.Qtable[s])
				a = lists.Qtable[s].index(max_q)
				if a <= len(lists.Qtable[s]):
					max_a = lists.action_list[a]

	return max_a, max_q
