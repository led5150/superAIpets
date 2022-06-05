import os

HERE           = os.path.dirname(os.path.abspath(__file__))
IMG_DIR        = os.path.join(HERE, "images")
BASE_IMGS      = os.path.join(IMG_DIR, "base_imgs")
SIT_IMG_DIR    = os.path.join(IMG_DIR, "situation_imgs")
ACTION_IMG_DIR = os.path.join(IMG_DIR, "action_imgs")
MODELS_DIR     = os.path.join(HERE, "models")


NAME_TEAM_IMG = os.path.join(BASE_IMGS, "name_team.png")

TEAM_NAME_1ST_SEARCH = os.path.join(ACTION_IMG_DIR, "team_name_1st_search.png")
TEAM_NAME_2ND_SEARCH = os.path.join(ACTION_IMG_DIR, "team_name_2nd_search.png")


# ML Model Paths
NUMBS_LR_MODEL = os.path.join(MODELS_DIR, "numbs_LogReg_model.03")
NUMBS_MLP_MODEL = os.path.join(MODELS_DIR, "numbs_MLP_model.01")
WINS_LR_MODEL  = os.path.join(MODELS_DIR, "wins_LogReg_model.02")
SITU_LR_MODEL  = os.path.join(MODELS_DIR, "situ_LogReg_model.01")
SITU_MLP_MODEL  = os.path.join(MODELS_DIR, "situ_MLP_model.01")
ANIFOOD_LR_MODEL = os.path.join(MODELS_DIR, "anifood_LogReg_model.01")
ATTACK_LR_MODEL = os.path.join(MODELS_DIR, "attack_LogReg_model.01")
HEALTH_LR_MODEL = os.path.join(MODELS_DIR, "health_LogReg_model.01")

anifoods = [
"none",
"empty",
"ant",
"apple",
"badgr",
"beavr",
"bfish",
"bison",
"boar",
"camel",
"can",
"cat",
"ccake",
"chili",
"choco",
"cow",
"crab",
"crikt",
"croc",
"deer",
"dlphn",
"dodo",
"dog",
"dragn",
"duck",
"elpht",
"fish",
"fly",
"garlc",
"goril",
"grafe",
"hghog",
"hippo",
"honey",
"horse",
"kanga",
"leprd",
"mamth",
"meat",
"melon",
"milk",
"mingo",
"monky",
"mosqt",
"mushm",
"otter",
"ox",
"parrt",
"pcock",
"pear",
"pguin",
"pig",
"pill",
"pizza",
"rabit",
"rat",
"rhino",
"roost",
"salad",
"scorp",
"seal",
"shark",
"sheep",
"shrmp",
"skunk",
"snail",
"snake",
"spidr",
"sqrrl",
"steak",
"sushi",
"swan",
"tiger",
"turky",
"turtl",
"whale",
"worm"
]

values = range(-1, len(anifoods))

anifood_map = dict(zip(values, anifoods))

