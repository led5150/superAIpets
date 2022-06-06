#!/usr/bin/env python3

from config import *

import numpy as np
import cv2
import pyautogui as pg
import random
# import mss
from mss.darwin import MSS as mss
from time import sleep


class ScreenStuff:
    def __init__(self, img_dir=IMG_DIR, action_dir=ACTION_IMG_DIR, situ_dir=SIT_IMG_DIR) -> None:
        super().__init__()
        print("Initializing Screen Stuff!!")
        self.img_dir    = img_dir
        self.action_dir = action_dir
        self.situ_dir   = situ_dir
        
        # Load the positions of each team name rectangle to click when 
        # selecting a team name
        self.first_name_pos, self.second_name_pos = self.load_team_name_positions()

        # Hardcode locations of common buttons to avoid wasting time
        self.roll_coords = (100, 700)
        self.end_coords  = (1100, 700)
        self.clickthrough_coords = (1100, 400) # Middle of screen to the right
        self.start_game_coords   = (750, 350)
        self.sell_freeze_coords  = (700, 700)
        self.excess_gold_back_coords = (428, 489)
        self.excess_gold_conf_coords = (847, 489)

        # Set Vars for game state
        self.NUM_CROP_W   = 82
        self.NUM_CROP_H   = 86
        self.ROUND_CROP_W = 154
        self.ROUND_CROP_H = 86

        self.numbs_coords = {
            0: {"x": 122, "y": 116, "w": self.NUM_CROP_W, "h": self.NUM_CROP_H},
            1: {"x": 338, "y": 116, "w": self.NUM_CROP_W, "h": self.NUM_CROP_H},
            2: {"x": 865, "y": 116, "w": self.NUM_CROP_W, "h": self.NUM_CROP_H},
        }

        self.wins_coords = {
            0: {"x": 552, "y": 116, "w": self.ROUND_CROP_W, "h": self.ROUND_CROP_H},
        }

        # Stage Locations
        self.pad_X   = [607, 799, 991, 1183, 1375, 1567, 1759]
        self.pad_W   = 192
        self.pad_H   = 330
        self.stage_Y = 458
        self.shop_Y  = 843

        self.stage_coords = {
            0: {"x": self.pad_X[0], "y": self.stage_Y, "w": self.pad_W, "h": self.pad_H},
            1: {"x": self.pad_X[1], "y": self.stage_Y, "w": self.pad_W, "h": self.pad_H},
            2: {"x": self.pad_X[2], "y": self.stage_Y, "w": self.pad_W, "h": self.pad_H},
            3: {"x": self.pad_X[3], "y": self.stage_Y, "w": self.pad_W, "h": self.pad_H},
            4: {"x": self.pad_X[4], "y": self.stage_Y, "w": self.pad_W, "h": self.pad_H},
        }

        self.shop_coords = {
            0: {"x": self.pad_X[0], "y": self.shop_Y, "w": self.pad_W, "h": self.pad_H},
            1: {"x": self.pad_X[1], "y": self.shop_Y, "w": self.pad_W, "h": self.pad_H},
            2: {"x": self.pad_X[2], "y": self.shop_Y, "w": self.pad_W, "h": self.pad_H},
            3: {"x": self.pad_X[3], "y": self.shop_Y, "w": self.pad_W, "h": self.pad_H},
            4: {"x": self.pad_X[4], "y": self.shop_Y, "w": self.pad_W, "h": self.pad_H},
            5: {"x": self.pad_X[5], "y": self.shop_Y, "w": self.pad_W, "h": self.pad_H},
            6: {"x": self.pad_X[6], "y": self.shop_Y, "w": self.pad_W, "h": self.pad_H},
        }

        # Get initial screenshot
        print("Getting initial IMage!!!")
        self.get_img()
    
    def excess_gold_back(self):
        self.click_on(self.excess_gold_back_coords[0], self.excess_gold_back_coords[1], clicks=1)

    def excess_gold_confirm(self):
        self.click_on(self.excess_gold_conf_coords[0], self.excess_gold_conf_coords[1], clicks=1)

    def load_team_name_positions(self):
        threshold = 0.75
        team_img = cv2.imread(NAME_TEAM_IMG, cv2.COLOR_RGB2BGR)

        first_search = cv2.imread(TEAM_NAME_1ST_SEARCH, cv2.COLOR_RGB2BGR)

        first_search_w = first_search.shape[1]
        first_search_h = first_search.shape[0]

        first_matches = cv2.matchTemplate(team_img, first_search, cv2.TM_CCOEFF_NORMED)

        yloc, xloc = np.where(first_matches >= threshold)

        rectangles = []
        for (x, y) in zip(xloc, yloc):
            rectangles.append([int(x), int(y), int(first_search_w), int(first_search_h)])


        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        # DEBUG HIGHLIGHT
        # for rec in rectangles:
        #     cv2.rectangle(team_img, (rec[0], rec[1]), (rec[0] + rec[2], rec[1] + rec[3]), (0,255,255), 2)
        # cv2.imshow('Farm', team_img)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        first_rectangles = rectangles[:3]
        second_rectangles = rectangles[3:]

        return first_rectangles, second_rectangles

    def get_regions(self, img, coords):
        regions = []
        for k, v in coords.items():
            x = v["x"]
            y = v["y"]
            w = v["w"]
            h = v["h"]

            # Sanity check
            # print(f"(Y: {y}, H: {h})  (X: {x}, W: {w})")
            region = img[y: y + h, x: x + w]
            regions.append(region)
            
            # Sanity check 2
            # img_info(region, gray=1)
        return regions


    def get_game_state_regions(self):
        numbs_regions = self.get_regions(self.curr_img, self.numbs_coords)
        wins_region   = self.get_regions(self.curr_img, self.wins_coords)

        return numbs_regions, wins_region
    
    def get_stage_shop_regions(self):
        stage_regions = self.get_regions(self.curr_img, self.stage_coords)
        shop_regions  = self.get_regions(self.curr_img, self.shop_coords)

        return stage_regions, shop_regions

    def move_pet(self, pet, dest):

        petX = (self.stage_coords[pet]['x'] // 2) + (self.stage_coords[0]['w'] // 4)
        petY = (self.stage_coords[pet]['y'] // 2) + (self.stage_coords[0]['h'] // 4)

        destX = (self.stage_coords[dest]['x'] // 2) + (self.stage_coords[0]['w'] // 4)
        destY = (self.stage_coords[dest]['y'] // 2) + (self.stage_coords[0]['h'] // 4)
        self.click_on(petX, petY, clicks=1)
        self.click_on(destX, destY, clicks=1)
        self.clickthrough()


    def buy_sell_freeze(self, pet, dest):
        if dest == "sell":
            petX = (self.stage_coords[pet]['x'] // 2) + (self.stage_coords[pet]['w'] // 4)
            petY = (self.stage_coords[pet]['y'] // 2) + (self.stage_coords[pet]['h'] // 4)

            destX = self.sell_freeze_coords[0]
            destY = self.sell_freeze_coords[1]
        elif dest == "freeze":
            petX = (self.shop_coords[pet]['x'] // 2) + (self.shop_coords[pet]['w'] // 4)
            petY = (self.shop_coords[pet]['y'] // 2) + (self.shop_coords[pet]['h'] // 4)

            destX = self.sell_freeze_coords[0]
            destY = self.sell_freeze_coords[1]
        else:
            petX = (self.shop_coords[pet]['x'] // 2) + (self.shop_coords[pet]['w'] // 4)
            petY = (self.shop_coords[pet]['y'] // 2) + (self.shop_coords[pet]['h'] // 4)

            destX = (self.stage_coords[dest]['x'] // 2) + (self.stage_coords[dest]['w'] // 4)
            destY = (self.stage_coords[dest]['y'] // 2) + (self.stage_coords[dest]['h'] // 4)
           

        self.click_on(petX, petY, clicks=1)
        self.click_on(destX, destY, clicks=1)
        if isinstance(dest, int) or dest == "sell":
            sleep(0.5)

    def end_turn(self):
        self.click_on(self.end_coords[0], self.end_coords[1])
    
    def roll(self):
        self.click_on(self.roll_coords[0], self.roll_coords[1])
        sleep(0.5)
    
    def clickthrough(self):
        self.click_on(self.clickthrough_coords[0], self.clickthrough_coords[1])

    def get_img(self):
        try:
            print("Getting Screenshot...")
            with mss() as sct:
                monitor = {"top": 0, "left": 0, "width": 1280, "height": 800}
                img_array = np.array(sct.grab(monitor))
            self.curr_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            # print("CURR IMG STATS")
            # print(self.curr_img.shape)
            # print(pg.size())
        except Exception as e:
            print(e)
            print("Could not load image from screen!")


    def get_curr_img(self):
        return self.curr_img


    def click_on(self, x, y, clicks=2, situ=None):
        if pg.onScreen(x, y):
            pg.click(x=x, y=y, clicks=clicks, interval=0.1, button="left")
        else:
            print(f"NOTTTTT ON SCREEN! X is {x}, y is: {y}")
        


    def get_random_name_coords(self, group):
        rand_int = random.randint(0, 2)
        if group == "first":
            return self.first_name_pos[rand_int]
        elif group == "second":
            return self.second_name_pos[rand_int]



    # Debugging functions
    def show(self):
        cv2.imshow("Current Image", self.curr_img)
        cv2.waitKey()
        cv2.destroyAllWindows()




def main():
    # print("Hello World!")

    # screenshot = pg.screenshot()

    # screenshot.show()
    screen = ScreenStuff()

    # print("Best situation")
    # print(screen.get_situation())
    # screen.get_img()
    # screen.show()




if __name__ == "__main__":
    main()