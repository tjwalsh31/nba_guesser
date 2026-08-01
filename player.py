from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
import random
import pandas as pd
from getplayer import get_info



class Player:
    def __init__(self):
        d = get_info()
        self.name = d["Name"]
        self.position = d["Position"]
        self.height = d["Height"]
        self.jersey = d["Jersey"]
        self.team = d["Team"]
        self.age = d["Age"]

    def __str__(self):
        return f"Name: {self.name}, Position: {self.position}, Height: {self.height}, Jersey: {self.jersey}, Team: {self.team}"


player = Player()
print(player)