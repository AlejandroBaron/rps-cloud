import itertools


MOVES = ["R","P","S"]
OUTCOMES = ["W","T","L"]

RULES = {("R","R"):"T",
        ("R","P"):"L",
        ("R","S"):"W",
        ("P","R"):"W",
        ("P","P"):"T",
        ("P","S"):"L",
        ("S","R"):"L",
        ("S","P"):"W",
        ("S","S"):"T",}

WINNING_MOVE = {"P":"S",
                "R":"P",
                "S":"R"}


 

