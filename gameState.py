#!/usr/bin/env python3

from config import *

from screenStuff import ScreenStuff
from sklearn.linear_model import LogisticRegression
import pickle
import cv2
import numpy as np
import skimage.measure
from time import sleep
import random

class GameState:
    def __init__(self):
        print("Initializing Game State!!")
        self.init_game_vars()

        
    def init_game_vars(self):
        self.gold         = 10
        self.prev_lives   = 10
        self.lives        = 10
        self.prev_wins    = 0
        self.wins         = 0
        self.prev_round   = 0
        self.round        = 0

        self.prev_stage_attack = 0
        self.stage_attack      = 0
        self.prev_stage_health = 0
        self.stage_health      = 0 
        self.prev_stage_score  = 0
        self.stage_score       = 0
        self.prev_shop_attack  = 0
        self.shop_attack       = 0
        self.prev_shop_health  = 0
        self.shop_health       = 0
        self.prev_shop_score   = 0
        self.shop_score        = 0


        self.open_stage_spots = [0, 1, 2, 3, 4]
        self.avail_shop_pets  = [0, 1, 2]
        self.sell_idxs        = []
        self.combine_idxs     = []
        self.buy_combine_idxs = []
        self.avail_food       = [6]
        self.stage_pos        = []


        self.result    = None
        self.new_round = True
        self.new_game  = True

        # Take initial screenshot 
        self.screen = ScreenStuff()

        # Load ML Models
        self.numbs_ML_Model   = pickle.load(open(NUMBS_LR_MODEL, 'rb'))
        self.wins_ML_Model    = pickle.load(open(WINS_LR_MODEL, 'rb'))
        self.situ_ML_Model    = pickle.load(open(SITU_LR_MODEL, 'rb'))
        self.anifood_ML_Model = pickle.load(open(ANIFOOD_LR_MODEL, 'rb'))
        self.attack_ML_Model  = pickle.load(open(ATTACK_LR_MODEL, 'rb'))
        self.health_ML_Model  = pickle.load(open(HEALTH_LR_MODEL, 'rb'))

        self.situ_map = {
            0: "loading_screen",
            1: "name_team",
            2: "main_game",
            3: "clickthrough",
            4: "excess_gold"
        }

        self.actions = {
            "roll":             0,
            "buy_pet":          1,
            "buy_combine_pet":  2,
            "sell_pet":         3,
            "freeze_pet":       4,
            "buy_food":         5,
            "move_pet":         6,
            "combine_pet":      7
        }
        self.attack_region_coords = (6, 243, 90, 83)
        self.health_region_coords = (98, 243, 90, 83)

        self.empty_spot = ["empty", "none"]

        self.anifood_map = anifood_map

        self.stage = ["empty"] * 5
        self.shop  = ["empty"] * 7

    def reset(self):
        self.gold         = 10
        self.prev_lives   = 10
        self.lives        = 10
        self.prev_wins    = 0
        self.wins         = 0
        self.prev_round   = 0
        self.round        = 0

        self.prev_stage_attack = 0
        self.stage_attack      = 0
        self.prev_stage_health = 0
        self.stage_health      = 0 
        self.prev_stage_score  = 0
        self.stage_score       = 0
        self.prev_shop_attack  = 0
        self.shop_attack       = 0
        self.prev_shop_health  = 0
        self.shop_health       = 0
        self.prev_shop_score   = 0
        self.shop_score        = 0

        self.open_stage_spots = [0, 1, 2, 3, 4]
        self.avail_shop_pets  = [0, 1, 2]
        self.sell_idxs        = []
        self.combine_idxs     = []
        self.avail_food       = [6]
        self.stage_pos        = []

        self.result    = None
        self.new_round = True

        

        self.stage = ["empty"] * 5
        self.shop  = ["empty"] * 7
    
    def print_game_state(self):
        print(f"Gold:  {self.gold}")
        print(f"Lives: {self.lives}")
        print(f"Wins:  {self.wins}")
        print(f"Round: {self.round}")
        print(f"Open Stage Spots: {self.open_stage_spots}")
        print(f"Stage Pos Taken:  {self.stage_pos}")
        print(f"Avial Shop Pets:  {self.avail_shop_pets}")
        print(f"Avail Shop Food:  {self.avail_food}")
        print(f"Avail Combine Idxs:  {self.combine_idxs}")
        print(f"Avail Buy-Comb Idxs: {self.buy_combine_idxs}")
        print(f"Result of last round: {self.result}")


        print("\nSTAGE:\n")
        for ani in self.stage:
            print(f"{ani:<5}  ", end="") if ani not in self.empty_spot else print("_____  ", end="")
        print(f"\nAttack: {self.stage_attack} | Health: {self.stage_health} | Score: {self.stage_score}")
        print("\n\nSHOP:\n")
        for ani in self.shop:
            print(f"{ani:<5}  ", end="") if ani not in self.empty_spot else print("_____  ", end="")
        print(f"\nAttack: {self.shop_attack} | Health: {self.shop_health} | Score: {self.shop_score}")
        print("\n")

        print("SCORES:")
        print(f"Prev Stage: {self.prev_stage_score}")
        print(f"CURR Stage: {self.stage_score}")
    
    def get_empty_stage_spots(self):
        empty_stage_spots = []
        for i, spot in enumerate(self.stage):
            if spot == "empty":
                empty_stage_spots.append(i)
        return empty_stage_spots
    
    def get_avail_shop_pets(self):
        avail_shop = []
        for i, spot in enumerate(self.shop):
            if i > 4:
                break
            if spot not in self.empty_spot:
                avail_shop.append(i)
        return avail_shop

    def get_avail_food(self):
        offset = 5
        avail_food = []
        for i, spot in enumerate(self.shop[5:]):
            if spot not in self.empty_spot:
                avail_food.append(i + offset)
        return avail_food
    
    def get_stage_positions(self):
        stage_pos = []
        for i, pet in enumerate(self.stage):
            if pet not in self.empty_spot:
                stage_pos.append(i)
        return stage_pos

    def get_results(self):
        if self.new_game == True:
            self.result = None
            return
            
        if self.wins > self.prev_wins:
            self.result = 'won'
            self.prev_wins = self.wins
        elif self.lives < self.prev_lives:
            self.result = "lost"
            self.prev_lives = self.lives
        else:
            self.result = "drew"


    def buy_pet(self):
        print("buying pet!")
        if not self.open_stage_spots:
            print("CANNOT BUY A NEW PET!!! No open spots on stage...")
            #sleep(1)
            return
        elif not self.avail_shop_pets:
            print("CANNOT BUY A NEW PET! No pets in shop!")
            #sleep(1)
            return
        else:
            rand_pet_idx  = random.randint(0, len(self.avail_shop_pets) - 1)
            rand_dest_idx = random.randint(0, len(self.open_stage_spots) - 1)
            rand_pet  = self.avail_shop_pets[rand_pet_idx]
            rand_dest = self.open_stage_spots[rand_dest_idx]
        #sleep(1)
        self.screen.buy_sell_freeze(rand_pet, rand_dest)

    def get_pets_to_sell_indecies(self):
        sell_idxs = []
        for i, pet in enumerate(self.stage):
            if pet not in self.empty_spot:
                sell_idxs.append(i)

        return sell_idxs

    def sell_pet(self):
        print("Selling pet!")
        sell_idxs = self.get_pets_to_sell_indecies()

            # rand_dest = random.randint(0, len(self.open_stage_spots))
        rand_idx  = random.randint(0, len(sell_idxs) - 1)
        rand_pet  = sell_idxs[rand_idx]

        self.screen.buy_sell_freeze(rand_pet, "sell")

    def freeze_pet(self):
        # get random index of pet in shop
        rand_idx = random.randint(0, len(self.avail_shop_pets) - 1)
        rand_pet = self.avail_shop_pets[rand_idx]
        self.screen.buy_sell_freeze(rand_pet, "freeze")

    def buy_food(self):
        # get random index of pet in shop
        try:
            rand_idx  = random.randint(0, len(self.avail_food) - 1)
            rand_food = self.avail_food[rand_idx]
        except:
            print("BUYING FOOD FAILED")
            print("RAND IDX is:", rand_idx)
            sleep(5)
            return

        rand_pet  = random.randint(0, len(self.stage_pos) - 1)
        rand_dest = self.stage_pos[rand_pet] 

        self.screen.buy_sell_freeze(rand_food, rand_dest)

    def move_pet(self):
        rand_idx  = random.randint(0, len(self.stage_pos) - 1)
        rand_pet  = self.stage_pos[rand_idx]
        rand_dest = random.randint(0, 4)
        while self.stage[rand_pet] == self.stage[rand_dest]:
            rand_dest = random.randint(0, 4)

        self.screen.move_pet(rand_pet, rand_dest)

    def combine_pet(self):
        rand_int      = random.randint(0, len(self.combine_idxs) - 1)
        rand_indecies = self.combine_idxs[rand_int]

        self.screen.move_pet(rand_indecies[0], rand_indecies[1])
    
    def get_buy_combine_idxs(self):
        combine_idxs = []
        for shop_idx, pet in enumerate(self.shop):
            if shop_idx > 4:
                break
            if pet not in self.empty_spot:
                for pet_idx, pet2 in enumerate(self.stage):
                    if pet2 not in self.empty_spot:
                        if pet == pet2:
                            combine_idxs.append((shop_idx, pet_idx))
        return combine_idxs

    def get_combine_indxs(self):
        combine_idxs = []
        for idx1, pet in enumerate(self.stage):
            for idx2, pet2 in enumerate(self.stage):
                if idx1 == idx2:
                    continue
                if pet == pet2:
                    combine_idxs.append((idx1, idx2))

    def buy_combine_pet(self):
        # Get number of possible combinations
        num_combines = len(self.buy_combine_idxs)

        # if more than one, pick one at random
        if num_combines > 1:
            idx = random.randint(0, num_combines - 1)
        else:
            idx = 0
        # Get the index of the pet to buy and combine
        buy_pet     = self.buy_combine_idxs[idx][0]
        combine_pet = self.buy_combine_idxs[idx][1]

        # Combine the pets!
        self.screen.buy_sell_freeze(buy_pet, combine_pet)

    def get_possible_actions(self):
        possible_actions = []
        if self.gold > 0:
            possible_actions.append(self.actions["roll"])
        if self.gold > 2:
            if self.avail_shop_pets and self.open_stage_spots:
                possible_actions.append(self.actions["buy_pet"])
            if self.buy_combine_idxs:
                possible_actions.append(self.actions["buy_combine_pet"])
        if self.sell_idxs:
            possible_actions.append(self.actions["sell_pet"])
        if self.avail_shop_pets:
            possible_actions.append(self.actions["freeze_pet"])
        if self.gold > 2 and self.avail_food and self.stage_pos:
            possible_actions.append(self.actions["buy_food"])
        if self.stage_pos:
            possible_actions.append(self.actions["move_pet"])
        if self.combine_idxs:
            possible_actions.append(self.actions["combine_pet"])
        #TODO: Add a no-op
        
        return possible_actions
        
        



    def convert_img(self, img, scale=(2,2)):
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)    # Convert to BGR
        img = np.dot(img, [0.2989, 0.5870, 0.1140])             # Convert to grayscale
        img = skimage.measure.block_reduce(img, scale, np.max)  # Downsample
        img = (img - img.mean()) / np.sqrt(img.var() + 1e-5)    # Rescale
        # cv2.imshow("BLoop", img)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        img = img.flatten()                                     # Make 1D
        return img

    def get_single_value(self, kind, img):
        # Use the appropriate ML model to get value
        if kind == "numbs":
            model = self.numbs_ML_Model
        elif kind == "anifood":
            model = self.anifood_ML_Model
        elif kind == "attack":
            model = self.attack_ML_Model
        elif kind == "health":
            model = self.health_ML_Model
        else:
            model = self.wins_ML_Model

        img   = self.convert_img(img)
        
        value = model.predict(np.array([img]))[0]   # Get ML Prediction

        return value

    def crop_single_region(self, img, coords):
        x = coords[0]
        y = coords[1]
        w = coords[2]
        h = coords[3]

        region = img[y: y + h, x: x + w]

        return region

    def get_attack(self, regions):
        total_attack = 0
        for reg in regions:
            reg = self.crop_single_region(reg, self.attack_region_coords)
            total_attack += self.get_single_value("attack", reg)
        return total_attack

    def get_health(self, regions):
        total_health = 0
        for reg in regions:
            reg = self.crop_single_region(reg, self.health_region_coords)
            total_health += self.get_single_value("health", reg)
        return total_health
    
    def get_total_score(self, regions):
        stage_attack = self.get_attack(regions)
        stage_health = self.get_health(regions)
        stage_score  = stage_attack + stage_health

        return stage_attack, stage_health, stage_score

    def return_prev_state(self):
        return self.prev_stage_attack, self.prev_stage_health, self.prev_stage_score, \
               self.prev_shop_attack, self.prev_shop_health, self.prev_shop_score

    def save_prev_state(self, stage_attack, stage_health, stage_score, shop_attack, shop_health, shop_score):
        self.prev_stage_attack = stage_attack
        self.prev_stage_health = stage_health
        self.prev_stage_score  = stage_score
        self.prev_shop_attack  = shop_attack
        self.prev_shop_health  = shop_health
        self.prev_shop_score   = shop_score

    def update_game_state(self, iteration):
        # Get regions for ML models to classify
        numbs_regions, wins_region  = self.screen.get_game_state_regions()
        stage_regions, shop_regions = self.screen.get_stage_shop_regions()

        # Classify each health and attack of both shop and stage and get values
        self.stage_attack, self.stage_health, self.stage_score = self.get_total_score(stage_regions)
        self.shop_attack,  self.shop_health, self.shop_score   = self.get_total_score(shop_regions)

        # Classify the regions and get values
        self.gold  = self.get_single_value("numbs", numbs_regions[0])
        self.lives = self.get_single_value("numbs", numbs_regions[1])
        self.round = self.get_single_value("numbs", numbs_regions[2])
        self.wins  = self.get_single_value("wins", wins_region[0])
        
        # Figure out if this is a new round or if we are in the middle of one
        if self.prev_round != self.round:
            self.prev_round = self.round
            self.new_round = True
        else:
            self.new_round = False

        # Get result of prev round
        if self.new_round == True:
            self.get_results()

        # Update animals on stage and in shop
        for i in range(len(self.stage)):
            ani_val = self.get_single_value("anifood", stage_regions[i])
            self.stage[i] = self.anifood_map[ani_val]

        for i in range(len(self.shop)):
            ani_val = self.get_single_value("anifood", shop_regions[i])
            self.shop[i] = self.anifood_map[ani_val]

        # Update available shop and stage indecies
        self.sell_idxs        = self.get_pets_to_sell_indecies()
        self.buy_combine_idxs = self.get_buy_combine_idxs()
        self.combine_idxs     = self.get_combine_indxs()
        self.open_stage_spots = self.get_empty_stage_spots()
        self.avail_shop_pets  = self.get_avail_shop_pets()
        self.avail_food       = self.get_avail_food()
        self.stage_pos        = self.get_stage_positions()
        


    def return_game_state(self):
        return self.gold, self.lives, self.wins, self.round, self.result, self.new_round,\
               self.stage_attack, self.stage_health, self.stage_score,\
               self.shop_attack, self.shop_health, self.shop_score


    def get_situation(self):
        curr_img = self.screen.get_curr_img()
        model    = self.situ_ML_Model

        img = self.convert_img(curr_img, scale=(8,8))

        situ = model.predict(np.array([img]))[0]
        prob = model.predict_proba(np.array([img]))

        if max(prob[0]) < 0.9:
            return "unknown"
        else:
            return self.situ_map[int(situ)]


    def update_img(self):
        self.screen.get_img()


    def start_game(self):
        self.new_game = True
        x_y = self.screen.start_game_coords
        self.screen.click_on(x_y[0], x_y[1])


    def pick_team_name(self):
        # find coordinates of random names on screen from first set and
        # second set
        offset = 20
        first_name_coords  = self.screen.get_random_name_coords("first")
        second_name_coords = self.screen.get_random_name_coords("second")

        # Click on the names!
        self.screen.click_on(
            (first_name_coords[0] // 2) + offset,
            (first_name_coords[1] // 2) + offset,
        )

        self.screen.click_on(
            (second_name_coords[0] // 2) + offset,
            (second_name_coords[1] // 2) + offset
        )

    def end_turn(self):
        if self.new_game == True:
            self.new_game = False
        self.gold = 10
        self.screen.end_turn()

    def roll(self):
        self.screen.roll()
    
    def clickthrough(self):
        self.screen.clickthrough()


    






def main():

    print("Hello World!")
    game = GameState()

    # game.pick_team_name()
    game.start_game()
    game.roll()
    game.end_turn()


if __name__ == "__main__":
    main()



