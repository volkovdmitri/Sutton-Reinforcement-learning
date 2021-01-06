#!/usr/bin/env python3
import numpy as np
import tqdm
import matplotlib.pyplot as plt

# Class for one blackjack hand
class Blackjack_hand:

    def __init__(self):
        
        self.deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        self.hand = []
        self.is_bust = False


    def draw_card(self):

        self.hand.append(np.random.choice(self.deck))


    def draw_hand(self):

        return [self.draw_card(), self.draw_card()]

    
    def usable_ace(self):

        return 1 in self.hand and sum(self.hand)+10 <= 21


    def compute_score(self):
        
        if self.usable_ace():
            return sum(self.hand)+10 
        else:
            return sum(self.hand)


    def check_if_bust(self):

        if self.compute_score() > 21:
            self.is_bust = True


# Class for one blackjack episode
class Blackjack_game():

    def __init__(self, player_policy):
        
        self.win_reward = 1
        self.lose_reward = -1 
        self.draw_reward = 0

        self.player = Blackjack_hand()
        self.dealer = Blackjack_hand()
        
        self.player.draw_hand()
        self.dealer.draw_hand()
        
        # log of states during an episode
        self.player_score_list = []
        self.player_usable_ace_list = []

        # policy shape - (10 - score of player's hand, 10 - first dealer's card, 2 - is ace usable) 
        # 1 - hits, 0 - sticks
        self.player_policy = player_policy


    def player_turn(self):
        
        self.player_score = self.player.compute_score()
        self.dealer_first_card = self.dealer.hand[0]

        while not self.player.is_bust:
            
            # save logs
            self.player_score_list.append(self.player_score)
            self.player_usable_ace_list.append(int(self.player.usable_ace()))

            # player's policy
            if self.player_score <= 11:
                action = 1
            else:
                action = self.player_policy[self.player_score-12, self.dealer_first_card-1, 
                                            int(self.player.usable_ace())]
            
            # act according to the policy 
            if action == 1:
                self.player.draw_card()
                self.player.check_if_bust()
                self.player_score = self.player.compute_score()
            else:
                break


    def dealer_turn(self):

        self.dealer_score = self.dealer.compute_score()
        while self.dealer_score < 17 and not self.dealer.is_bust:
            self.dealer.draw_card()
            self.dealer.check_if_bust()
            self.dealer_score = self.dealer.compute_score()


    def results(self):

        if self.player.is_bust:
            return self.lose_reward
        elif self.dealer.is_bust:
            return self.win_reward
        else:
            if self.player_score > self.dealer_score:
                return self.win_reward
            elif self.player_score < self.dealer_score:
                return self.lose_reward
            else:
                return self.draw_reward


    def play(self):

        self.player_turn()
        self.dealer_turn()


# the policy that sticks if the player’s sum is 20 or 21, and otherwise hits
policy = np.zeros((10, 10, 2)) + 1
policy[8:10, :, :] = 0


def monte_carlo(policy, runs):

    # initial values
    V = np.zeros((10, 10, 2))
    N = np.zeros((10, 10, 2))
    
    for _ in tqdm.tqdm(range(runs)):
        game = Blackjack_game(policy)
        game.play()
        reward = game.results()

        states_log = []
        for i in range(len(game.player_score_list)):
            state = (game.player_score_list[i], game.dealer_first_card, 
                     game.player_usable_ace_list[i])   
            # update value of a state
            if state[0] >= 12 and state not in states_log:
                N[state[0]-12, state[1]-1, state[2]] += 1 
                V[state[0]-12, state[1]-1, state[2]] += 1/N[state[0]-12, state[1]-1, state[2]]*\
                                                       (reward - V[state[0]-12, state[1]-1, state[2]])
                states_log.append(state)

    return V

V = monte_carlo(policy, 500000)

# Plot
fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.arange(1, 11)
Y = np.arange(12, 22)
X, Y = np.meshgrid(X, Y)

surf = ax.plot_surface(X, Y, V[:,:,0])
plt.show()


