from pathlib import Path


BARRIER_PREFIX = "Barrier_"
MEGA_PREFIX = "Mega_"

STAGE_FLANN_IMAGE_PATH = r"FLANN.png"
LAST_BOARD_IMAGE_PATH = r"last_board.png"
LAST_SCREEN_IMAGE_PATH = r"last_screen.png"
IMAGES_BARRIER_PATH = r"assets\icons_barrier"
IMAGES_EXTRA_PATH = r"assets\icons_extra"
IMAGES_PATH = r"assets\icons_processed"
ASSETS_PATH = r"assets"
BARRIER_TYPE_REAL = "Real"
BARRIER_TYPE_FAKE = "Fake"
RANDOM = "RANDOM"
SURVIVAL_MODE = "SURVIVAL_MODE"
MEOWTH_COIN_MANIA = "MEOWTH COIN MANIA"
GRADING_TOTAL_SCORE = "grading.score"
GRADING_MEGA_PROGRESS = "grading.megaprogress"
GRADING_WEEKEND_MEOWTH = "WeekendMeowth"
GRADING_MEGA_BOOSTED_SCORE = "MegaBoostedScore"
GRADING_DISRUPTION_BOOSTED_SCORE = "disruptionBoostedScore"

move_strategy = {
    "grading.score": "Total Score",
    "grading.totalblocks": "Total Blocks",
    "grading.disruptions": "Disruptions",
    "grading.mindisruptions": "Low Disrupt.",
    "grading.combos": "Combos",
    "grading.noneorall": "None or All",
    "grading.megaprogress": "Mega Progress",
    "grading.coordinate": "Coordinates",
    "WeekendMeowth": "WeekendMeowth",
    "037MeowthEarlyGame": "037MeowthEarlyGame",
    "037MeowthEndGame": "037MeowthEndGame",
    "MegaBoostedScore": "MegaBoostedScore",
    "disruptionBoostedScore": "disruptionBoostedScore"

}

move_stages = {
    "NORMAL": "NORMAL",
    "FIRE": "FIRE",
    "WATER": "WATER",
    "GRASS": "GRASS",
    "ELECTRIC": "ELECTRIC",
    "ICE": "ICE",
    "FIGHTING": "FIGHTING",
    "POISON": "POISON",
    "GROUND": "GROUND",
    "FLYING": "FLYING",
    "PSYCHIC": "PSYCHIC",
    "BUG": "BUG",
    "ROCK": "ROCK",
    "GHOST": "GHOST",
    "DRAGON": "DRAGON",
    "DARK": "DARK",
    "STEEL": "STEEL",
    "FAIRY": "FAIRY",
    "NONE": "NONE",
    "SP_084": MEOWTH_COIN_MANIA,
    "037": "STAGE 37",
    "SURVIVAL_MODE": "SURVIVAL MODE",
    "RANDOM": "RANDOM"
}
downscale_res = (128, 128)

STAGE_TO_IMAGE = {
    "STAGE 37": "052",
    "STAGE 38": "453",
    "STAGE 39": "222",
}

# This is a bad name. These will change from phone to phone
# depending on how big the top status bar is etc.. These are just
# hardcode values for my phones.
RESOLUTIONS = {
    "1440x3120": {
        # Stage Selection
        "StageSelectionArea": (320, 550, 1120, 2600),
        "HeartTimer": (75, 190, 255, 250),
        "Hearts": (355, 190, 480, 250),
        "Continue": (420, 2770, 1020, 2870),
        "Start!": (420, 2770, 1020, 2870),
        "No": (1000, 2390, 1340, 2490),
        "To Map": (420, 2770, 1020, 2870),
        # Stage
        "Board": (20, 1540, 1415, 2935),
        "Stage": (45, 225, 320, 285),
        "Score": (45, 385, 320, 450),
        "MovesLeft": (45, 1285, 390, 1375),
    },
    "1080x2160": {
        # Stage Selection
        "StageSelectionArea": (240, 400, 840, 1800),
        "HeartTimer": (58, 112, 190, 155),
        "Hearts": (265, 112, 357, 155),
        "Continue": (340, 1890, 740, 1970),
        "Start!": (340, 1890, 740, 1970),
        "No": (780, 1690, 990, 1760),
        "To Map": (340, 1890, 740, 1970),
        # Stage
        "Board": (17, 968, 1064, 2015),
        "Stage": (35, 140, 240, 185),
        "Score": (35, 260, 240, 305),
        "MovesLeft": (35, 775, 300, 845),
    },
    "1600x900": {
        "CompleteScreen": (0, 0, 900, 1600),
        "TopScreen": (0, 0, 900, 716),
        "HeartTimer": (44, 62, 158, 103),
        "Hearts": (230, 62, 299, 105),
        "Continue": (271, 1463, 646, 1578),
        "Start!": (271, 1463, 646, 1578),
        "To Map": (271, 1463, 646, 1578),
        "Next": (271, 1463, 646, 1578),
        "No": (153, 646, 742, 826),
        "No2": (681, 1040, 781, 1093), #This No appears when you click no start without hearts on a stage
        "NoOutOfTime": (646, 1343, 816, 1409), #Out of Time to Play
        "Yes": (153, 646, 742, 826),
        "StageMenu": (801, 27, 906, 162),
        "Combo": (602, 46, 813, 136),
        "CoinStage": (153, 646, 742, 826),
        "CoinStageYes": (118, 1041, 225, 1093),
        "Close": (348, 1033, 544, 1096),
        "Close2": (646, 1041, 806, 1093),
        "Close3": (630, 1153, 823, 1232),
        "Angry": (70, 686, 826, 915), #The Grey Angry! text
        "Retry": (385, 1344, 515, 1409), #Retry Text when Connection Problem occurs
        # "EscalationLevel": (558, 434, 841, 623),
        "Pokeball Capture": (320, 1028, 577, 1272),
        "Greatball": (110, 1259, 803, 1308), #Do you want to use 3500 Coins
        "GreatballNo": (691, 1453, 772, 1509),
        "GreatballYes": (123, 1460, 217, 1506),
        "SurvivalModeText": (126, 720, 780, 813),
        # Stage
        "Board": (16, 716, 886, 1586),
        "Stage": (37, 85, 195, 126),
        "StageName": (581, 546, 890, 586),
        "Score": (32, 187, 200, 222),
        "MovesLeft": (39, 551, 240, 620),
        "EndStageScore": (103, 661, 832, 720),
        "EndStageCoins": (511, 627, 607, 673),
        "Drops": (613, 449, 892, 538),
    },
    "1080x2342": {
        "CompleteScreen": (0, 115, 1080, 2255),
        "TopScreen": (0, 115, 1080, 1190),
        "HeartTimer": (53, 198, 190, 253),
        "Hearts": (276, 198, 359, 255),
        "Continue": (325, 2072, 775, 2226),
        "Start!": (325, 2072, 775, 2226),
        "To Map": (325, 2072, 775, 2226),
        "Next": (325, 2072, 775, 2226),
        "No": (184, 979, 890, 1220),
        "No2": (817, 1506, 937, 1577),
        "NoOutOfTime": (775, 1911, 979, 2000),
        "Yes": (184, 979, 890, 1220),
        "StageMenu": (986, 192, 1080, 306),
        "Combo": (722, 177, 976, 297),
        "CoinStage": (184, 979, 890, 1220),
        "CoinStageYes": (142, 1507, 270, 1577),
        "Close": (418, 1497, 653, 1581),
        "Close2": (775, 1507, 967, 1577),
        "Close3": (756, 1657, 988, 1763),
        "Angry": (84, 1033, 991, 1339),
        "Retry": (462, 1913, 618, 2000),
        "Pokeball Capture": (384, 1490, 692, 1816),
        "Greatball": (132, 1799, 964, 1864),
        "GreatballNo": (829, 2058, 926, 2133),
        "GreatballYes": (148, 2068, 260, 2129),
        "SurvivalModeText": (151, 1078, 936, 1202),
        # Stage
        "Board": (17, 1190, 1064, 2237),
        "Stage": (35, 248, 240, 295),
        "StageName": (680, 990, 1068, 1040),
        "Score": (35, 367, 240, 414),
        "MovesLeft": (35, 995, 295, 1092),
        "EndStageScore": (124, 999, 998, 1078),
        "EndStageCoins": (613, 954, 728, 1015),
        "Drops": (736, 716, 1070, 835),
    },
    "2076x2152": {
        "CompleteScreen": (486, 0, 1592, 2072),
        "TopScreen": (486, 0, 1592, 985),
        "HeartTimer": (540, 80, 680, 133),
        "Hearts": (769, 80, 853, 136),
        "Continue": (819, 1895, 1280, 2044),
        "Start!": (819, 1895, 1280, 2044),
        "To Map": (819, 1895, 1280, 2044),
        "Next": (819, 1895, 1280, 2044),
        "No": (674, 837, 1398, 1070),
        "No2": (1323, 1347, 1446, 1415),
        "NoOutOfTime": (1280, 1739, 1489, 1825),
        "Yes": (674, 837, 1398, 1070),
        "StageMenu": (1495, 11, 1590, 128),
        "Combo": (1226, 60, 1485, 176),
        "CoinStage": (674, 837, 1398, 1070),
        "CoinStageYes": (631, 1348, 762, 1415),
        "Close": (914, 1338, 1155, 1419),
        "Close2": (1280, 1348, 1476, 1415),
        "Close3": (1260, 1493, 1497, 1595),
        "Angry": (572, 888, 1501, 1185),
        "Retry": (959, 1740, 1119, 1825),
        "Pokeball Capture": (879, 1331, 1195, 1647),
        "Greatball": (621, 1630, 1473, 1694),
        "GreatballNo": (1335, 1882, 1435, 1954),
        "GreatballYes": (637, 1891, 753, 1950),
        "SurvivalModeText": (641, 932, 1445, 1053),
        # Stage
        "Board": (500, 985, 1576, 2060),
        "Stage": (525, 67, 735, 115),
        "StageName": (1190, 780, 1580, 835),
        "Score": (525, 189, 735, 237),
        "MovesLeft": (525, 790, 790, 886),
        "EndStageScore": (613, 856, 1508, 932),
        "EndStageCoins": (1114, 812, 1232, 872),
        "Drops": (1239, 581, 1582, 697),
    }
}

SURVIVAL_MODE_TXT = r"assets\survival_list.txt"
ADB_IMAGE_FOLDER = r"assets\adb"
MEOWTH_DEBUG_IMAGE_FOLDER = r"debug\meowth"
DEBUG_STAGES_IMAGE_FOLDER = r"debug\complete"
DEBUG_EXTRA_IMAGE_FOLDER = r"debug\extra"
DEBUG_SURVIVAL_IMAGE_FOLDER = r"debug\survival"
CURRENT_STAGE_IMAGE = r"assets\adb\current_stage.png"
MEOWTH_STAGE_IMAGE = r"assets\adb\meowth_037.png"
SURVIVAL_MODE_STAGE_IMAGE = r"assets\adb\survival_mode.png"
INFO_ICON_IMAGE = r"assets\adb\info_icon.png"
COMBO_IMAGE = r"assets\adb\combo.png"
ACTIVE_BOARD_IMAGE = r"assets\adb\active_board.png"
OK_BUTTON_IMAGE = r"assets\adb\ok_button.png"
OK_BUTTON2_IMAGE = r"assets\adb\ok_button2.png"
RETURN_FLAG_IMAGE = r"assets\adb\return_flag1.png"
RETURN_FLAG2_IMAGE = r"assets\adb\return_flag2.png"
ANGRY_ICON_IMAGE = r"assets\adb\angry_1.png"
ANGRY_ICON2_IMAGE = r"assets\adb\angry_2.png"
POKEBALL_CAPTURE_IMAGE = r"assets\adb\pokeball_capture.png"
DROP_IMAGE = r"assets\adb\drop.png"

NON_POKEMON_NAMES_LIST = ["Empty", "Coin", "Metal", "Wood", "Fog", "Air"]
SURVIVAL_TEAM_STRING = '''

TEAM SURVIVAL_MODE Aerodactyl,Air,Banette,Bellsprout,Blitzle,Bronzor,Budew,Buneary,Carbink,Charizard_x,Charmander,Chespin,Chimchar,Chimchar_w,Coin,Croagunk,Deoxys,Doublade,Dratini,Eevee,Espeon,Exploud,Feebas,Flaaffy,Flareon,Floatzel,Fog,Froakie,Galvantula,Gastly,Gogoat,Goomy,Gothita,Gothitelle,Gothorita,Granbull,Grimer,Happiny,Haunter,Hawlucha_s,Honedge,Illumise,Jigglypuff,Joltik,Kirlia,Klang,Klefki,Klinklang,Lickilicky,Lickitung,Lilligant,Litwick,Loudred,Machoke,Machop,Mandibuzz,Medicham,Meditite,Meowstic,Meowstic_f,Metagross_s,Metal,Monferno,Munna,Musharna,Onix,Pancham,Petilil,Probopass,Pupitar,Ralts,Raticate,Rayquaza,Roselia,Roserade_w,Scyther,Shelgon,Shuckle,Skarmory,Skiddo,Skitty,Sliggoo,Slowbro,Slowpoke,Snorlax,Spritzee,Staraptor,Staravia,Starly,Swablu,Sylveon,Taillow,Tangela,Tangrowth,Togekiss,Togepi,Togetic,Treecko,Turtwig_w,Tyranitar,Whismur,Wood,Zorua 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z Charizard_x Aerodactyl,Banette,Bellsprout,Blitzle,Bronzor,Budew,Buneary,Carbink,Charmander,Chespin,Chimchar,Croagunk,Deoxys,Doublade,Dratini,Eevee,Espeon,Exploud,Feebas,Flaaffy,Flareon,Floatzel,Froakie,Galvantula,Gastly,Gogoat,Goomy,Gothita,Gothitelle,Gothorita,Granbull,Grimer,Happiny,Haunter,Honedge,Illumise,Jigglypuff,Joltik,Kirlia,Klang,Klefki,Klinklang,Lickilicky,Lickitung,Lilligant,Litwick,Loudred,Machoke,Machop,Mandibuzz,Medicham,Meditite,Meowstic,Meowstic_f,Monferno,Munna,Musharna,Onix,Pancham,Petilil,Probopass,Pupitar,Ralts,Raticate,Roselia,Scyther,Shelgon,Shuckle,Skarmory,Skiddo,Skitty,Sliggoo,Slowbro,Slowpoke,Snorlax,Spritzee,Staraptor,Staravia,Starly,Swablu,Taillow,Tangela,Tangrowth,Togekiss,Togepi,Togetic,Treecko,Tyranitar,Whismur,Zorua

'''.strip()
