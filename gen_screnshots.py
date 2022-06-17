#!/usr/bin/env python3

from ast import Num
from cmath import pi
import os
import sys
from select import select
from webbrowser import get 
import pyautogui as pg
import skimage.measure
import numpy as np
import cv2
from mss.darwin import MSS as mss

# TODO: STill need these attack and health numbers
# ATTACK DICT:
# Picture Stats:
#    47: 0
#    49: 0
#    50: 0

# HEALTH DICT:
# Picture Stats:
#    45: 0



# output_dir = "situation_training"
# output_dir = "training_base"
# output_dir = "numbs_training"
# output_dir = "anifood_training"

attack_output_dir = "attack_training"
health_output_dir = "health_training"

# pic_types = ["loading", "name_team", "main_game", "clickthrough", "excess_gold"]

# pic_types = ["lives_9of10"]

# pic_types = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

# pic_types = [
#     "none",
#     "empty",
#     "ant",
#     "beavr",
#     "crikt",
#     "duck",
#     "fish",
#     "horse",
#     "mosqt",
#     "otter",
#     "pig",
#     "apple",
#     "honey",
#     "crab",
#     "dodo",
#     "turtl",
#     "elpht",
#     "mingo",
#     "hghog",
#     "pcock",
#     "rat",
#     "shrmp",
#     "spidr",
#     "swan",
#     "ccake",
#     "meat",
#     "pill",
#     "badgr",
#     "bfish",
#     "camel",
#     "dog",
#     "grafe",
#     "kanga",
#     "ox",
#     "rabit",
#     "sheep",
#     "snail",
#     "garlc",
#     "salad",
#     "bison",
#     "deer",
#     "dlphn",
#     "hippo",
#     "parrt",
#     "pguin",
#     "roost",
#     "skunk",
#     "sqrrl",
#     "whale",
#     "worm",
#     "can",
#     "pear",
#     "cow",
#     "croc",
#     "monky",
#     "rhino",
#     "scorp",
#     "seal",
#     "shark",
#     "turky",
#     "chili",
#     "choco",
#     "sushi",
#     "boar",
#     "cat",
#     "fly",
#     "dragn",
#     "goril",
#     "leprd",
#     "mamth",
#     "snake",
#     "tiger",
#     "melon",
#     "mushm",
#     "pizza",
#     "steak",
#     "milk",
#     "s"
# ]

pic_types = [x for x in range(51)]
pic_types.append("s")
print(pic_types)


# ONES I HAVE...
# ant, beaver, ccake, cricket, duck, fish, honey, horse, meat, mosqt, otter, pig
# 

# already_have = ["ant", "beavr", "ccake", "crikt", "duck", "fish", "honey", 
#                 "horse", "meat", "mosqt", "otter", "pig", "apple", "pill",
#                 "turtl", ]

TOTAL_TAKEN = 0

NUM_CROP_W = 82
NUM_CROP_H = 86

ROUND_CROP_W = 154
ROUND_CROP_H = 86

numbs_coords = {
    0: {"x": 122, "y": 116, "w": NUM_CROP_W, "h": NUM_CROP_H},
    1: {"x": 338, "y": 116, "w": NUM_CROP_W, "h": NUM_CROP_H},
    2: {"x": 865, "y": 116, "w": NUM_CROP_W, "h": NUM_CROP_H},
}

wins_coords ={
    0: {"x": 552, "y": 116, "w": ROUND_CROP_W, "h": ROUND_CROP_H},
}

# Stage Locations
pad_X   = [607, 799, 991, 1183, 1375, 1567, 1759]
pad_W   = 192
pad_H   = 330
stage_Y = 458
shop_Y  = 843

stage_coords = {
    0: {"x": pad_X[0], "y": stage_Y, "w": pad_W, "h": pad_H},
    1: {"x": pad_X[1], "y": stage_Y, "w": pad_W, "h": pad_H},
    2: {"x": pad_X[2], "y": stage_Y, "w": pad_W, "h": pad_H},
    3: {"x": pad_X[3], "y": stage_Y, "w": pad_W, "h": pad_H},
    4: {"x": pad_X[4], "y": stage_Y, "w": pad_W, "h": pad_H},
}

shop_ani_coords = {
    0: {"x": pad_X[0], "y": shop_Y, "w": pad_W, "h": pad_H},
    1: {"x": pad_X[1], "y": shop_Y, "w": pad_W, "h": pad_H},
    2: {"x": pad_X[2], "y": shop_Y, "w": pad_W, "h": pad_H},
    3: {"x": pad_X[3], "y": shop_Y, "w": pad_W, "h": pad_H},
    4: {"x": pad_X[4], "y": shop_Y, "w": pad_W, "h": pad_H},
}


shop_coords = {
    0: {"x": pad_X[0], "y": shop_Y, "w": pad_W, "h": pad_H},
    1: {"x": pad_X[1], "y": shop_Y, "w": pad_W, "h": pad_H},
    2: {"x": pad_X[2], "y": shop_Y, "w": pad_W, "h": pad_H},
    3: {"x": pad_X[3], "y": shop_Y, "w": pad_W, "h": pad_H},
    4: {"x": pad_X[4], "y": shop_Y, "w": pad_W, "h": pad_H},
    5: {"x": pad_X[5], "y": shop_Y, "w": pad_W, "h": pad_H},
    6: {"x": pad_X[6], "y": shop_Y, "w": pad_W, "h": pad_H},
}

FULLSCREEN = {"top": 0, "left": 0, "width": 1280, "height": 800}


attack_region = (6, 243, 90, 83)
health_region = (98, 243, 90, 83)



def show_cv2_img(window_name, img):
    cv2.imshow(window_name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()

def get_regions(img, coords):
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

def get_single_region(img, coords):
    x = coords[0]
    y = coords[1]
    w = coords[2]
    h = coords[3]

    region = img[y: y + h, x: x + w]

    return region

def rescale_regions(regions):
    re_scaled = []
    for img in regions:
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)    # Convert to BGR
        img = np.dot(img, [0.2989, 0.5870, 0.1140])             # Convert to grayscale
        img = skimage.measure.block_reduce(img, (2,2), np.max)  # Downsample
        img = (img - img.mean()) / np.sqrt(img.var() + 1e-5)    # Rescale
        re_scaled.append(img)
    return re_scaled

def get_img(coords):
    try:
        with mss() as sct:
            img_array = np.array(sct.grab(coords))
        curr_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(e)
        print("Could not load image from screen!")
    return curr_img



def take_batch_of_screenshots(num_taken, pic_dict, pic_names, coords):
    global TOTAL_TAKEN
    
    try:
        stop_at = int(input("How Many? "))
    except ValueError as e:
        print(e)
        print("Need an int dummy!")
        return
    cmd = ""

    base_img = get_img(FULLSCREEN)

    if isinstance(coords, dict):
        regions = get_regions(base_img, coords)
    else:
        regions = get_regions(base_img, coords[0])
        regions.extend(get_regions(base_img, coords[1]))

    while cmd != "q":
        for i, pic in enumerate(pic_names):
            for shot in range(stop_at):
                if pic == "s":
                    print("SKIPPING!!!!!")
                    continue
                if shot == 0:
                    print(f"Taking shots for pic_type: {pic}")
                print(f"Taking sshot #: {shot + 1}...")
                TOTAL_TAKEN += 1
                filename = f"{pic}_numbs_train_{TOTAL_TAKEN}.png"
                cv2.imwrite(os.path.join(output_dir, filename), regions[i])
                num_taken[0] += 1

            pic_dict[pic] += stop_at
        pretty_print(pic_dict)
        cmd = input("Take another batch? type q to stop. ")



def take_batch_of_screenshots2(num_taken, attack_pic_dict, health_pic_dict, pic_names, coords):
    global TOTAL_TAKEN
    
    try:
        stop_at = int(input("How Many? "))
    except ValueError as e:
        print(e)
        print("Need an int dummy!")
        return
    cmd = ""

    base_img = get_img(FULLSCREEN)

    if isinstance(coords, dict):
        regions = get_regions(base_img, coords)
    else:
        ani_regions = get_regions(base_img, coords[0])
        ani_regions.extend(get_regions(base_img, coords[1]))
        attack_regions = []
        health_regions = []
        for i, reg in enumerate(ani_regions):
            attack_regions.append(get_single_region(reg, attack_region))
            health_regions.append(get_single_region(reg, health_region))
        

    attack_regions.extend(health_regions)

    all_regions = attack_regions


    while cmd != "q":
        for i, pic in enumerate(pic_names):
            for shot in range(stop_at):
                if pic == "s":
                    print("SKIPPING!!!!!")
                    continue
                if shot == 0:
                    print(f"Taking shots for pic_type: {pic}")
                print(f"Taking sshot #: {shot + 1}...")
                TOTAL_TAKEN += 1
                if i < 10:
                    filename = f"{pic}_attack_train_{TOTAL_TAKEN}.png"
                    cv2.imwrite(os.path.join(attack_output_dir, filename), all_regions[i])
                else:
                    filename = f"{pic}_health_train_{TOTAL_TAKEN}.png"
                    cv2.imwrite(os.path.join(health_output_dir, filename), all_regions[i])
                num_taken[0] += 1
            if i < 9:
                if pic != "s":
                    attack_pic_dict[pic] += stop_at
            else:
                if pic != "s":
                    health_pic_dict[pic] += stop_at
        print("ATTACK DICT:")
        pretty_print(attack_pic_dict)
        print("\nHEALTH DICT:")
        pretty_print(health_pic_dict)
        cmd = input("Take another batch? type q to stop. ")

def load_anifood_dict():
    anifood = {}
    for ani in pic_types:
        anifood[ani] = 0
    for base, dirs, files in os.walk(output_dir):
        for f in files:
            ani = f.split("_")[0]
            print(ani)
            if ani not in anifood:
                anifood[ani] = 1
            else:
                anifood[ani] += 1
    return anifood


def pretty_print(d):
    print("\nPicture Stats:")
    for k, v in sorted(d.items(), key=lambda x: x[0]):
        if v < 100:
            print(f"{k:>5}: {v}")
    print("")
        
def check_pic_names(pic_names):
    if len(pic_names) != 20:
        print(f"Wrong len for pic names: {len(pic_names)}! Must be len == 20")
        return False
    for pname in pic_names:
        if pname == "s":
            continue
        if int(pname) not in pic_types:
            print(f"ERROR! No pic type {pname}")
            return False
    return True

def main():
    # pic_dict = load_anifood_dict()
    attack_pic_dict = {}
    health_pic_dict = {}
    for i in range(51):
        attack_pic_dict[i] = 0
        health_pic_dict[i] = 0
    rlist = [sys.stdin]
    wlist = []
    xlist = []
    while True:
        print("PAUSED!")
        print("Enter Picture Values: ")
        read, write, x = select(rlist, wlist, xlist)
        if read:
            num_taken = [0]
            pic_name = input()
            if pic_name == "q":
                exit()
            else:
                pic_names = []
                for x in pic_name.split():
                    if x != "s":
                        pic_names.append(int(x))
                    else:
                        pic_names.append(x)
                if not check_pic_names(pic_names):
                    continue
                else:
                    while True:
                        try:
                            print("Hello.....")
                            take_batch_of_screenshots2(num_taken,attack_pic_dict,health_pic_dict,pic_names,[stage_coords, shop_ani_coords])
                            break

                        except Exception as e:
                            print(e)
                            break
                        except KeyboardInterrupt:
                            break
                            # print("Paused!")


        









if __name__ == "__main__":
    main()