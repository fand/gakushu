# -*- coding:utf-8 -*-
import pytetris as pt
from egreedy import get_reward
from qlearning import add_state
import lists

# updateQ：価値の更新。疑似コード等を参考に
def updateQ(c_state, action, alpha, gamma):

	num_s = add_state(c_state)
	num_a = lists.action_list.index(action)
	reward = 0 #get_reward()
	piece = c_state[1]
	n_board_state, line_reward = pt.answer(c_state[0], piece[1], piece[2], action[0], action[1])
	for i in range(len(n_board_state)):
		for j in range(len(n_board_state[i])):
			if n_board_state[i][j] > 0 and n_board_state[i][j] < 8:	n_board_state[i][j] = 1
	n_state = [n_board_state, pt.getNextPiece()]
	num_sn = add_state(n_state)
	if num_sn:	pass
	else:num_sn = add_state(n_state)
#	else:
#		lists.state_list.append(n_state)
#		num_sn = lists.state_list.index(n_state)
	Q_s_a = get_value(num_s, num_a)
	r_s_a, height = get_reward(c_state, action)
	max_Q = get_max_Qvalue(num_sn)

	value = Q_s_a + alpha * (r_s_a + gamma * max_Q - Q_s_a)
	if len(lists.Qtable)<=num_s:
		for i in range(len(lists.Qtable), num_s+1):
			lists.Qtable.append([])
	if len(lists.Qtable[num_s])<=num_a:
		for i in range(len(lists.Qtable[num_s]), num_a+1):
			lists.Qtable[num_s].append(0)
	lists.Qtable[num_s][num_a] = value
	return 

def gameover_Q(num_s):

	start = len(lists.Qtable[num_s])
	final = len(lists.action_list)
	for i in range(0, start):	lists.Qtable[num_s][i] = -1000
	for i in range(start,final):	lists.Qtable[num_s].append(-1000)
	
	return

#- Q(s,a)の取得
def get_value(num_s, num_a):
        if (len(lists.Qtable)>num_s):
                if (len(lists.Qtable[num_s])>num_a):
                        return lists.Qtable[num_s][num_a]
                else:
                        return 0
        else:
                return 0


#- 状態s'において最大のQ(s',a')を取得
def get_max_Qvalue(num_sn):
	value_list = lists.Qtable[num_sn] if len(lists.Qtable)>num_sn else []
	return max(value_list) if len(value_list)>0 else 0
