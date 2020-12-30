#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

p_head = 0.4
e = 1e-10
states = range(1, 100)
v = np.zeros(99)
policy = np.zeros(99)
converged = False

# Value iteration
while not converged:
    delta = 0
    for state in states:
        actions = range(1, state+1)
        q_list = np.zeros(len(actions))
        for ind, bet in enumerate(actions):
            if state+bet >= 100:
                if state == bet:
                    q_list[ind] = p_head*1
                else:
                    q_list[ind] = (1-p_head)*v[state-bet-1] + p_head*1
            elif state == bet:
                q_list[ind] = p_head*v[state+bet-1]
            else:
                q_list[ind] = (1-p_head)*v[state-bet-1] + p_head*v[state+bet-1]
        delta = max(delta, abs(v[state-1] - np.max(q_list)))
        v[state-1] = np.max(q_list)
        policy[state-1] = actions[np.argmax(np.round(q_list, 5))]
    if delta < e:
        converged = True


print(v)
print(policy)
plt.plot(policy)
plt.show()
