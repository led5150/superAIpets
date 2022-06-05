#!/usr/bin/env python3

from config import *
from gameState import GameState
import sys
from time import sleep
import random
import numpy as np
import operator



class superAIPet:
    def __init__(self, game=None):
        self.game = game
        if self.game is None:
            self.game = GameState()
        else:
            self.game = game

        self.curr_state  = None
        self.prev_action = None
        self.iteration   = 0

        self.func_map = {
            "loading_screen":   self.load_game,
            "name_team":        self.name_team,
            "main_game":        self.main_game,
            "clickthrough":     self.clickthrough,
            "excess_gold":      self.excess_gold,
            "unknown":          self.unknown_situation,
        }

        self.action_map = {
            0: self.game.roll,
            1: self.game.buy_pet,
            2: self.game.buy_combine_pet,
            3: self.game.sell_pet,
            4: self.game.freeze_pet,    
            5: self.game.buy_food,      
            6: self.game.move_pet,      
            7: self.game.combine_pet    
        }

        self.action_strs = {
            0: "roll",
            1: "buy_pet",
            2: "buy_combine_pet",
            3: "sell_pet",
            4: "freeze_pet",    
            5: "buy_food",      
            6: "move_pet",      
            7: "combine_pet"    
        }

        self.action_weights_map = {}

        #initialize the exploration probability to 1
        self.exploration_proba = 1

        #exploartion decreasing decay for exponential decreasing
        # self.exploration_decreasing_decay = 0.001
        self.exploration_decreasing_decay = 0.05


        # minimum of exploration proba
        self.min_exploration_proba = 0.01

        #discounted factor
        self.gamma = 0.99

        #learning rate
        self.lr = 0.1

    # Situation functions:

    def load_game(self):
        print("ON LOADING SCREEN!!")
        self.game.reset()
        self.game.start_game()
    
    def excess_gold(self):
        print("ON EXXESSSS GOLLLSSSSSS")
        print("TOOOO")
        print("Dooooooooooo")

    def name_team(self):
        print("IN Name Team!!")
        self.game.pick_team_name()
        self.game.end_turn()
    
    def adjust_action_weight(self, prev_weight, reward, next_action ):
        new_weight = (1 - self.lr) * prev_weight + self.lr * (reward + self.gamma * self.action_weights_map[next_action])
        return new_weight

    def determine_reward(self, prev_stage_attack, prev_stage_health, prev_stage_score,
                         prev_shop_attack, prev_shop_health, prev_shop_score,
                         stage_attack, stage_health, stage_score,
                         shop_attack, shop_health, shop_score):
        if prev_stage_score > stage_score:
            return -1
        if prev_stage_score == stage_score:
            return 0
        if prev_stage_score < stage_score:
            return 1

    def pretty_print_action_map(self):
        for k, v in self.action_weights_map.items():
            print(f"{self.action_strs[k]}: {v} | ", end="")
        print("\n")

    def main_game(self):
        print("\033c") # Clear Terminal
        print("ACTION WEIGHTS!")
        self.pretty_print_action_map()
        prev_stage_attack, prev_stage_health, prev_stage_score, \
        prev_shop_attack, prev_shop_health, prev_shop_score = self.game.return_prev_state()
        self.game.update_game_state(self.iteration)
        
        
        print("\n~~~ GAME STATE ~~~")
        self.game.print_game_state()
        # sleep(3)

        print("Returning Game State...")
        gold, lives, wins, round, result, new_round,  \
        stage_attack, stage_health, stage_score,      \
        shop_attack, shop_health, shop_score  = self.game.return_game_state()

        self.game.save_prev_state(stage_attack, stage_health, stage_score, shop_attack, shop_health, shop_score)

        reward = self.determine_reward(prev_stage_attack, prev_stage_health, prev_stage_score,
                         prev_shop_attack, prev_shop_health, prev_shop_score,
                         stage_attack, stage_health, stage_score,
                         shop_attack, shop_health, shop_score)



        # Next round if gold is zero
        if gold == 0:
            self.game.end_turn()
            return

        #TODO: Update weights according to value of result!
        if new_round == True:
            self.update_weights(result)
            self.exploration_proba = max(self.min_exploration_proba, np.exp(-self.exploration_decreasing_decay * round))
        else:
            print("We are in the middle of the same round!!")

        # Find possible actions
        actions = self.game.get_possible_actions()

        # If we have never seen this action before, add it to the map
        for action in actions:
            if action not in self.action_weights_map:
                self.action_weights_map[action] = 0

        print("Possible Actions: ", end="")
        for act in actions:
            print(f"{self.action_strs[act]}, ", end="")
        print("")


        # Perform some random action, or choose the best action available
        if np.random.uniform(0,1) < self.exploration_proba:
            rand_idx = random.randint(0, len(actions) - 1)
            print(f"RANDOM ACTION: {self.action_strs[actions[rand_idx]]}")
            action = actions[rand_idx]
        else:
            action = self.get_best_action_possible(actions)
            print(f"DOING BEST ACTION!!!! {self.action_strs[action]}")

        # Update the weights of the previous action based on the strength of team
        if self.prev_action is not None:
            print("UPDATING ACTION WEIGHT")
            prev_weight = self.action_weights_map[self.prev_action]
            self.action_weights_map[self.prev_action] = self.adjust_action_weight(prev_weight, reward, action)
        self.prev_action = action
        self.action_map[action]()
        
        
            
    def get_best_action_possible(self, possible_actions):
        act_weight_subset = {key: self.action_weights_map[key] for key in possible_actions}
        action = max(act_weight_subset.items(), key=operator.itemgetter(1))[0]
        return action

    def update_weights(self, result):
        if result == None:
            print("THIS IS A NEW GAME")
        elif result == "won":
            print("WE WON!!!, Positive update in weights....")
        elif result == "lost":
            print("We lost... Negative update here....")
        else:
            print("We Drew!!  Update anything??? maybe a little less positive???")
        # sleep(3)
            

    def clickthrough(self):
        print("Clicking Through...")
        self.game.clickthrough()


    def unknown_situation(self):
        print("Unknown Situation...clicking through...")
        # self.game.clickthrough()
    

    def execute_situation(self, situation):
        self.func_map[situation]()

    def print_game_state(self):
        self.game.print_game_state()
    
    def update_img(self):
        self.game.update_img()

    def run(self):
        while True:
            self.update_img()
            situ = self.game.get_situation()
            
            print(f"Game Situation: {situ.upper()}")

            # Execute the proper function
            self.execute_situation(situ)
            
            
            
            



def run_AI():

    AI = superAIPet()
    AI.run()





if __name__ == "__main__":
    run_AI()
