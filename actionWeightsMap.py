#!/usr/bin/env python3
import numpy as np
import operator


class ActionWeightsMap:
    def __init__(self):
        #initialize the exploration probability to 1
        self.exploration_proba = 1
        #exploartion decreasing decay for exponential decreasing
        self.exploration_decreasing_decay = 0.001
        # minimum of exploration proba
        self.min_exploration_proba = 0.01
        #discounted factor
        self.gamma = 0.99
        #learning rate
        self.lr = 0.1

        self.iteration = 0

        self.action_weights_map = {}

    def get_map(self):
        return self.action_weights_map
    
    def update_exploration_proba(self):
        self.exploration_proba = max(self.min_exploration_proba, np.exp(-self.exploration_decreasing_decay * self.iteration))
    
    def adjust_action_weight(self, prev_action, reward, round):
        # Adjust the action weight using the Q-Learning equation
        prev_weight = self.action_weights_map[prev_action]
        # best_next_action = self.get_best_action_of_next_round(int(round + 1))
        # new_weight = (1 - self.lr) * prev_weight + self.lr * (reward + self.gamma * best_next_action)
        new_weight = (1 - self.lr) * prev_weight + self.lr * reward
        self.action_weights_map[prev_action] = new_weight

    def add_new_action(self, action):
        self.action_weights_map[action] = 0

    def get_best_action_possible(self, possible_actions):
        act_weight_subset = {key: self.action_weights_map[(key[0], key[1])] for key in possible_actions}
        action = max(act_weight_subset.items(), key=operator.itemgetter(1))[0]
        return action

    def get_best_action_of_next_round(self, next_actions):
        best_action_val = 0
        
        for action in next_actions:
            action_val = self.action_weights_map[action]
            if action_val > best_action_val:
                best_action_val = action_val

        return best_action_val

    def print_map(self):
        for k, v in self.action_weights_map.items():
            print(k, v)
    
    def is_empty(self):
        if self.action_weights_map:
            return False
        return True

def main():
    a = ActionWeightsMap()
    if a.is_empty():
        print("I'm empty")
    else:
        print("I'm not empty")
    a.add_new_action((1,2))
    if a.is_empty():
        print("I'm empty")
    else:
        print("I'm not empty")
    a.print_map()

if __name__ == "__main__":
    main()