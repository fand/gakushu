flag = {
    'waiting': True,
    'moved': False,
    'ground': False,
    'gameover': False,
    'moving': False,
    'rotating': False,
    'update': False,
    'erase':False
    }
t = {
    'now':0,
    'dropped': 0,
    'moved': 0,
    'rotated': 0,
    'stopped_moving':0,
    'stopped_rotating':0,
    'input': 0
    }
interval = {
    'move':0.3,
    'rotate':0.3,
    'gravity':0.5
    }
signal = {
    'left': False,
    'right': False,
    'down': False,
    'cw': False,
    'ccw': False
    }


score = 0
