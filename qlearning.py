# -*- coding:utf-8 -*-

import csv
import numpy
import pygame

import pytetris as pt

import egreedy
#import softmax
import updateQ

import lists 

# qLearning：Q-learningの大枠。一つの試行で一度動かす疑似コードを参考に
def qLearning(maxsteps = 10000, rate_a = 0.6, rate_g = 0.3):
	#- state = [board_state, tetrimino]:	盤面の状態, テトリミノ
	#- steps, maxsteps:	エピソード数
	#- state_list:	状態リスト．盤面の状態と落ちてきている駒
	#- action_list:	行動リスト．[横移動回数，回転の回数]を保持
	#- Qtable:	Q値を格納する二次元配列

	steps = 0
	flag = 0

	while steps < maxsteps:
		rate = change_rate(steps/maxsteps, rate_a, rate_g)
		alpha, gamma = rate_a * rate, rate_g * rate
		#state_list = []
		pt.init(0.5)
		alive = 1
		old_board = board = []
		
		print "step:", steps, "start"
		while alive: #- ゲームオーバーになるまで
			if flag == 0:
				board = pt.getBoard()
                                row_heights = len(board)*[0]
				if old_board != board:
					for i in range(len(board[0])):
                                                for j in range(len(board)):
                                                        if board[j][i]:
                                                                row_heights[i] = j
                                                                break
					piece = pt.getPiece()
					state = [row_heights, piece]

					#- 行動の探査・搾取
					action = egreedy.eGreedy(state) # softmaxでもよいが、今はとりあえず

					#- state_list, action_list, Qtableの更新
					if action not in lists.action_list:
						lists.action_list.append(action)
					add_state(state)
					updateQ.updateQ(state, action, alpha, gamma)

					#- actionの実行
					old_board = board
					flag = 1

			#次の状態を準備
			if flag == 1:
				step = 0
				while flag != 2:
					flag = doaction(action, piece)
					step += 1
					if step % 100 == 0:
						flag = 2

			elif flag == 2:
				pt.loop()
				pt.drop()
				if pt.param.flag['update']:
					pt.loop()
					flag = 0
				if pt.param.flag['gameover']:
					num_s = add_state(state)
					updateQ.gameover_Q(num_s)
					alive = flag = 0

		steps += 1
		reset()
		check = 1
#		if len(lists.Qtable) != len(lists.state_list):	print "check"
		while check:
			if [] in lists.Qtable:	lists.Qtable.remove([])
			else:	check = 0
#		if len(lists.Qtable) != len(lists.state_list):	print len(lists.state_list),len(lists.Qtable)
#		flag = steps / maxsteps

	return lists.state_list, lists.action_list, lists.Qtable

#- 学習率を変化させる
def change_rate(flag, alpha, gamma):
	if flag < 0.3: return 1#alpha
	elif flag >= 0.3 and flag < 0.5: return 0.5#8
	elif flag >= 0.5 and flag < 0.8: return 0.3#6
	else:
		return 0#.5

#- stateがリストに無ければ追加
def add_state(state):
	for i in lists.state_list:
		if i[0] == state[0]:
			i[1][1] = numpy.array(i[1][1])
			if i in lists.state_list:
				return lists.state_list.index(i)
	lists.state_list.append(state)
	return lists.state_list.index(state)
#	for i in lists.state_list:	print i
#	print "sum:",len(lists.state_list)

#- リセット
def reset():
	pt.init(100)

#- action実行
def doaction(action, piece):
	k = s = old = 0
	goal = piece[2] + action[0]
	r_p = numpy.rot90(piece[1],action[1])
	p = pt.getPiece()
#	if goal < 1:	goal = 1
#	elif goal > 9 and piece[0] == 1 and action[1] % 2:	goal = 9
#	elif goal > 8 and piece[0] == 1 and action[1] % 2 == 0:	goal = 6
#	elif goal > 8 and piece[0] != 1:	goal = 8

	if goal == p[2]:	k = 1

	if action[0] > 0 and goal != p[2]:
		pt.move('right')
	elif action[0] < 0 and goal != p[2]:
		pt.move('left')
	old = p[2]

	for i in range(len(p[1])):
		for j in range(len(p[1][i])):
			if r_p[i][j] != p[1][i][j]:
				s = 2
				break
			if s == 2:	break
		if s == 2:	break
	if s == 2:
		pt.rotate('ccw')
		s = 0
	else: s = 1

	if k == 1 and s == 1:	return 2
	else:
		return 1
		

score = 0

#- 学習結果をゲームに適用
def play_game(state_list, action_list, Qtable):

	step = 0 # 合計ループ数
	old_state = new_state = [] #- state
	flag = 0
	reset()
	pt.init(0.5)

	# メインループ
	while(pt.alive()):

		#########################
		# ループごとの解析、操作をここに書く

		if step % 180 == 0 and flag == 0:
			new_board = pt.getBoard()
                        piece = pt.getPiece()
			new_state = [new_board, piece]

		if new_state != old_state and flag == 0:
			action, value = egreedy.search_action(new_state)
			if action == []:
				action = egreedy.eGreedy(new_state)
			old_state = new_state
			flag = 1

		if step % 10 == 0 and flag == 1:
			flag = doaction(action, piece)
			if step % 100 == 0:	flag = 2

#			print(new_state)

		#########################
	
		# 次のループへ
		pt.loop()
		if flag == 2:
			print pt.param.flag['update']
			pt.move('down')
			if pt.param.flag['update']:
				print "update"
				pt.loop()
				flag = 0
			if pt.param.flag['gameover']:	alive = flag = 0
		step += 1

	# 終了    
	pt.quit()

if __name__ == "__main__":
	#- エピソード数，学習率，割引率を与える
	print "learning_start"
	state_list, action_list, Qtable = qLearning()
	print "learning_finish"

	#- 学習内容をcsvファイルに出力
	write_csv = csv.writer(file('table.csv', 'w'), lineterminator = '\n')
	for values in Qtable:
		s = Qtable.index(values)
		state = state_list[s]
		for value in values:
			a = Qtable[s].index(value)
			action = action_list[a]
			write_csv.writerow(state)

	#- 学習結果を適用
	play_game(state_list, action_list, Qtable)
	
