#!/usr/bin/env python3
import math
import numpy as np
import tqdm
import matplotlib.pyplot as plt


discount = 0.9
lam_A_req = 3
lam_B_req = 4
lam_A_ret = 3
lam_B_ret = 2
rental_reward = 10
cost = -2
max_cars = 20
max_cars_to_move = 5
random_upper_bound = 11


# Poisson probabilities for given n and lambda
def poisson_prob(n, lam):
    return lam**n/math.factorial(n)*np.exp(-lam)


# Poisson probabilities
prob = dict()
for lam in [lam_A_req, lam_B_req, lam_A_ret, lam_B_ret]:
    for n in range(random_upper_bound):
        key = n*10 + lam
        if key not in prob.keys():
            prob[key] = poisson_prob(n, lam)


# All possible states
states = np.zeros(((max_cars+1)**2, 2), dtype=np.int)
for i in range(max_cars+1):
    for j in range(max_cars+1):
        states[i*(max_cars+1)+j, 0] = i
        states[i*(max_cars+1)+j, 1] = j
# Initial values of the states
V = np.zeros((max_cars+1, max_cars+1))
# Policy
policy = np.zeros((max_cars+1, max_cars+1))


def value_iteration():
    global states
    global V
    global policy
    # Value iteration
    for state in tqdm.tqdm(states):
        # All available actions for a state (from A perspective)
        actions = range(-min(max_cars_to_move, state[0]), min(max_cars_to_move, state[1]+1))
        new_vals = np.zeros(len(actions))
        # For each possible action
        for ind, action in enumerate(actions):
            new_state_after_action = [min(state[0] + action, max_cars), 
                                      min(state[1] - action, max_cars)] 
            new_vals[ind] += abs(action)*cost
            # Requests
            for A_req in range(random_upper_bound):
                for B_req in range(random_upper_bound):
                    p = prob[A_req*10+lam_A_req]*prob[B_req*10+lam_B_req]
                    new_state = [new_state_after_action[0] - min(A_req, new_state_after_action[0]), 
                                 new_state_after_action[1] - min(B_req, new_state_after_action[1])]
                    # Returns
                    for A_ret in range(random_upper_bound):
                        for B_ret in range(random_upper_bound):
                            p_ = prob[A_ret*10+lam_A_ret]*prob[B_ret*10+lam_B_ret]
                            final_state = [min(new_state[0] + A_ret, max_cars),
                                           min(new_state[1] + B_ret, max_cars)]
                            new_vals[ind] += p*p_*(rental_reward*(A_req+B_req) + \
                                                   discount*V[final_state[0], final_state[1]])
        # Choose value for a state
        V[state[0], state[1]] = np.max(new_vals)
        policy[state[0], state[1]] = actions[np.argmax(new_vals)]

if __name__ == '__main__':
    for i in range(20):
        value_iteration()   

print(V)
               






