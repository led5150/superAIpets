#!/usr/bin/env python3

import re
from config import *
from gameState import GameState
import sys
from time import sleep
import random
import numpy as np
import operator
import pickle
import argparse
from datetime import datetime



class superAIPet:
    def __init__(self, weights_file=None, game=None):
        self.game = game
        if self.game is None:
            self.game = GameState()
        else:
            self.game = game

        self.curr_state  = None
        self.prev_action = None
        self.iteration   = 0

        self.all_round_actions = []

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
            7: self.game.combine_pet,
            8: self.game.freeze_like_pet
        }

        self.action_strs = {
            0: "roll",
            1: "buy_pet",
            2: "buy_combine_pet",
            3: "sell_pet",
            4: "freeze_pet",    
            5: "buy_food",      
            6: "move_pet",      
            7: "combine_pet",
            8: "freeze_like_pet"
        }

        self.MAXITER = 15 

        self.Q_table = [set() for _ in range(30)]


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


        # Initialize new weights dict, or load from file
        if weights_file is None:
            self.action_weights_map = {}
        else:
            with open(weights_file, 'rb') as f:
                # Load weights and previous iteration/exploration values
                self.action_weights_map = pickle.load(f)
                for k, v in self.action_weights_map.items():
                    print(k, v)
                self.iteration          = self.action_weights_map["iteration"]
                self.exploration_proba  = self.action_weights_map["exploration_proba"]
                del self.action_weights_map["iteration"]
                del self.action_weights_map["exploration_proba"]

        
    # Situation functions:

    def load_game(self):
        print("ON LOADING SCREEN!!")
        self.game.reset()
        self.game.start_game()
    
    def excess_gold(self, action):
        print("ON EXXESSSS GOLLLSSSSSS")
        action()

    def name_team(self):
        print("IN Name Team!!")
        self.game.pick_team_name()
        self.game.end_turn()
    
    def get_best_action_of_next_round(self, next_round):
        next_actions = self.Q_table[next_round]
        best_action_val = 0
        
        for action in next_actions:
            action_val = self.action_weights_map[action]
            if action_val > best_action_val:
                best_action_val = action_val

        return best_action_val

    def adjust_action_weight(self, prev_weight, reward, round):
        # Adjust the action weight using the Q-Learning equation
        # best_next_action = self.get_best_action_of_next_round(int(round + 1))
        # new_weight = (1 - self.lr) * prev_weight + self.lr * (reward + self.gamma * best_next_action)
        new_weight = (1 - self.lr) * prev_weight + self.lr * reward

        return new_weight

    def determine_reward(self, prev_stage_attack, prev_stage_health, prev_stage_score,
                         prev_shop_attack, prev_shop_health, prev_shop_score,
                         stage_attack, stage_health, stage_score,
                         shop_attack, shop_health, shop_score):
        reward = 0
        delta_score = (stage_score - prev_stage_score) + 0.2 * (shop_score - prev_shop_score)
        # delta_score = delta_score * 0.1
        print(f"DELTA SCORE: {delta_score}")
        # Stage adjustments
        if prev_stage_score > stage_score:
            reward -= abs(delta_score)
        if prev_stage_score < stage_score:
            reward += delta_score


        # Shop Adjustments
        # if prev_shop_score > shop_score: # bought animal, or rolled and bad animals
        #     reward -= 0.1
        # if prev_shop_score < shop_score: # rolled and good animals, encourage rolling
        #     reward += 1


        # Action Adjustments
        if self.prev_action == 2:   # buy_combine
            reward += 0.3
        if self.prev_action == 7:   # combine_pet: Offset the penalty for decreasing stage score exactly
            reward += abs(delta_score)
        if self.prev_action == 6:   # Move pet
            reward = 0
        if self.prev_action == 8:   # Freeze Like Pet action
            reward += 0.5

        print(f"Total Reward: {reward}")
        return reward




    def pretty_print_action_map(self):
        for k, v in self.action_weights_map.items():
            print(f"{self.action_strs[k]}: {v} | ", end="")
        print("\n")

    def main_game(self):
        
        for _ in range(self.MAXITER):
            # Get previous state of game
            prev_stage_attack, prev_stage_health, prev_stage_score, \
            prev_shop_attack, prev_shop_health, prev_shop_score = self.game.return_prev_state()

            # Update the game state based on what's on the screen
            self.game.update_game_state(self.iteration)
            print("\033c") # Clear Terminal
            print("\n~~~ GAME STATE ~~~")
            # print the action map and weights
            self.pretty_print_action_map()
            print(self.Q_table)
            print(f"Iteration: {self.iteration}\n")
            self.game.print_game_state()
            # sleep(3)

            gold, lives, wins, round, result, new_round,  \
            stage_attack, stage_health, stage_score,      \
            shop_attack, shop_health, shop_score  = self.game.return_game_state()

            self.game.save_prev_state(stage_attack, stage_health, stage_score, shop_attack, shop_health, shop_score)

            reward = self.determine_reward(prev_stage_attack, prev_stage_health, prev_stage_score,
                            prev_shop_attack, prev_shop_health, prev_shop_score,
                            stage_attack, stage_health, stage_score,
                            shop_attack, shop_health, shop_score)

            # Update the weights of the previous action based on the strength of team
            if self.prev_action is not None:
                prev_weight = self.action_weights_map[self.prev_action]
                self.action_weights_map[self.prev_action] = self.adjust_action_weight(prev_weight, reward, round)
            
            # Update the exploration probability factor
            self.exploration_proba = max(self.min_exploration_proba, np.exp(-self.exploration_decreasing_decay * self.iteration))
            print(f"Exploration Proba: {self.exploration_proba}")

            # Next round if gold is zero
            if gold == 0:
                self.game.end_turn()
                return

            #TODO: Update weights according to value of result!
            if new_round == True:
                sleep(2)
                prev_round = int(round - 1)
                self.update_weights(result, self.all_round_actions, prev_round)
                self.Q_table[prev_round].update(self.all_round_actions) # Add list to set
                self.all_round_actions = []
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
                print(f"{self.action_strs[act[0]]}, ", end="")
            print("")


            # Perform some random action, or choose the best action available
            if np.random.uniform(0,1) < self.exploration_proba:
                rand_idx = random.randint(0, len(actions) - 1)
                print(f"RANDOM ACTION: {self.action_strs[actions[rand_idx]]}")
                action = actions[rand_idx]
            else:
                action = self.get_best_action_possible(actions)
                print(f"DOING BEST ACTION!!!! {self.action_strs[action]}")

            
            
            # Do stuff with action and save state
            self.all_round_actions.append(action)
            self.prev_action = action

            # Determine if we have to do anything special for this action
            if action[0] == 1: # Buying pet
                # find position of pet to buy
                buy_idx = None
                for i, ani in enumerate(self.game.shop):
                    if ani.get_name() == self.game.anifood_str_map[action[1]]:
                        buy_idx = i
                        break
                action[1] = buy_idx
            elif action[0] == 2:
                # find position of pet to buy
                buy_idx = None
                for i, ani in enumerate(self.game.shop):
                    if ani.get_name() == self.game.anifood_str_map[action[1]]:
                        buy_idx = i
                        break
                action[1] = buy_idx


            self.action_map[action[0]](action[1])


            # Move mouse over to get pop-ups off screen and allow some time for
            # them to go away if they are.
            self.clickthrough()
            sleep(3)

            self.iteration += 1

            self.update_img()
        
        print("MAX ITERATIONS REACHED!")
        self.game.end_turn()
        sleep(.5)
        self.game.excess_gold_confirm()
        sleep(7) 
        

        
        
        
            
    def get_best_action_possible(self, possible_actions):
        act_weight_subset = {key: self.action_weights_map[key] for key in possible_actions}
        action = max(act_weight_subset.items(), key=operator.itemgetter(1))[0]
        return action

    def update_weights(self, result, prev_actions, prev_round):
        if result == None:
            print("THIS IS A NEW GAME")
        elif result == "won":
            print("WE WON!!!, Positive update in weights....")
            for action in np.unique(prev_actions):
                weight = self.action_weights_map[action]
                self.action_weights_map[action] = self.adjust_action_weight(weight, 5, prev_round)
            
        elif result == "lost":
            print("We LOST!... Negative update in weights....")
            for action in np.unique(prev_actions):
                weight = self.action_weights_map[action]
                self.action_weights_map[action] = self.adjust_action_weight(weight, -5, prev_round)
        else:
            print("We DREW!! Draw, draw, draw....")
            for action in np.unique(prev_actions):
                weight = self.action_weights_map[action]
                self.action_weights_map[action] = self.adjust_action_weight(weight, 1, prev_round)
        sleep(1.5)
            

    def clickthrough(self):
        print("Clicking Through...")
        self.game.clickthrough()


    def unknown_situation(self):
        print("Unknown Situation...clicking through...")
        self.game.clickthrough()
    

    def execute_situation(self, situation):
        if situation == "excess_gold":
            self.func_map[situation](self.game.excess_gold_back)
        else:
            self.func_map[situation]()

    def print_game_state(self):
        self.game.print_game_state()
    
    def update_img(self):
        self.game.update_img()

    def run(self):
        while True:
            try:
                self.update_img()
                situ = self.game.get_situation()
                
                print(f"Game Situation: {situ.upper()}")

                # Execute the proper function
                self.execute_situation(situ)

                # Allow enough time for the game to update the screen so we
                # don't get bad values for the game!
                if situ in ["loading_screen", "name_team", "clickthrough"]:
                    sleep(7)
                


            except KeyboardInterrupt:
                print("PAUSED!")
                if self.get_answer("Would you like to quit? y/n?") == "y":
                    if self.get_answer("Would you like to save the weights and game state? y/n? ") == "y":
                        date     = datetime.today().strftime("%m-%d-%Y_%H:%M:%S")
                        filename = f"saved_action_weights_{date}.pkl"
                        fpath    = os.path.join(ACTION_W_DIR, filename)

                        # Add the game state, i.e. the iteration number and the 
                        # hyperparameters to the dict

                        self.action_weights_map["iteration"] = self.iteration
                        self.action_weights_map["exploration_proba"] = self.exploration_proba

                        with open(fpath, 'wb') as f:
                            pickle.dump(self.action_weights_map, f)
                    else:
                        print("okay! did not save weights!")

                    print("Thanks for playing! Have a Super Auto Day!")
                    exit()
                else:
                    pass
                
            
            
            
    def get_answer(self, msg):
        answer = input(msg)
        while answer not in ["y", "n"]:
            answer = input(msg)
        return answer


def run_AI(load_weights):

    AI = superAIPet(load_weights)
    AI.run()





if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--load_weights', required=False, help="File to load action weights from.")

    run_AI(**vars(parser.parse_args()))
