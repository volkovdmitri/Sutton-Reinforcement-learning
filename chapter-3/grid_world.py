import numpy as np

size = 5
table = np.zeros((size, size))
actions = ['N', 'S', 'W', 'E']
prob = {'N':1/4, 'S':1/4, 'W':1/4, 'E':1/4}
discount = 0.9


def reward(action, x, y):
    '''
    actions from ['N', 'S', 'W', 'E']
    x, y - initial position
    return: reward and new position
    '''
    # Point A
    if x==0 and y==1:
        return 10, (4, 1)
    # Point B
    if x==0 and y==3:
        return 5, (2, 3)
    # Other points
    if action=='N':
        if x==0:
            return -1, (x, y)
        else:
            return 0, (x-1, y)

    elif action=='S':
        if x==size-1:
            return -1, (x, y)
        else:
            return 0, (x+1, y)

    elif action=='W':
        if y==0:
            return -1, (x, y)
        else:
            return 0, (x, y-1)

    elif action =='E':
        if y==size-1:
            return -1, (x, y)
        else:
            return 0, (x, y+1)


def epoch(run_type='Random'):
    
    global table
    if run_type=='Random':
        for i in range(size):
            for j in range(size):
                r = np.zeros(len(actions))
                v = np.zeros(len(actions))
                for ind, a in enumerate(actions):
                    r[ind], new_loc = reward(a, i, j)
                    v[ind] = table[new_loc[0], new_loc[1]]
                # Bellman equation
                p = np.array(list(prob.values()))
                table[i, j] = np.dot(p, (r + discount*v).T)
    
    elif run_type=='Optimal':
        for i in range(size):
            for j in range(size):
                r = np.zeros(len(actions))
                v = np.zeros(len(actions))
                for ind, a in enumerate(actions):
                    r[ind], new_loc = reward(a, i, j)
                    v[ind] = table[new_loc[0], new_loc[1]]
                # Bellman equation
                table[i, j] = np.max(r + discount*v)


for e in range(10000):
    epoch(run_type='Random')
print(np.round(table, 1))

for e in range(10000):
    epoch(run_type='Optimal')
print(np.round(table, 1))







