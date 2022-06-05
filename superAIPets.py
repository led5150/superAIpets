#!/usr/bin/env python3

from config import *
from gameState import GameState
import sys
from time import sleep
import random



class superAIPet:
    def __init__(self, game=None):
        self.game = game
        if self.game is None:
            self.game = GameState()
        else:
            self.game = game

        self.curr_state = None

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
    
    def main_game(self):
        print("ON Main Game Screen!")
        print("Updating Game State...")
        self.game.update_game_state()
        
        
        print("\n~~~ GAME STATE ~~~")
        self.game.print_game_state()

        print("Returning Game State...")
        gold, lives, wins, round, result, new_round = self.game.return_game_state()

        # Next round if gold is zero
        if gold == 0:
            self.game.end_turn()
            return

        #TODO: Update weights according to value of result!
        if new_round == True:
            self.update_weights(result)
        else:
            print("We are in the middle of the same round!!")

        # Find possible actions
        actions = self.game.get_possible_actions()
        print("Possible Actions: ", end="")
        for act in actions:
            print(f"{self.action_strs[act]}, ", end="")
        print("")


        # Perform some random action...
        rand_idx = random.randint(0, len(actions) - 1)
        print(f"DOING ACTION: {self.action_strs[actions[rand_idx]]}")
        self.action_map[actions[rand_idx]]()
        # self.action_map[5]()
        
        
    
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
            print("\033c") # Clear Terminal
            print(f"Game Situation: {situ.upper()}")

            # Execute the proper function
            self.execute_situation(situ)
            
            
            
            



def run_AI():

    AI = superAIPet()
    AI.run()





if __name__ == "__main__":
    run_AI()
