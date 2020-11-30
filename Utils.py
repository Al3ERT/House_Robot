from enum import Enum

DIRECTIONS = [(1,0),(0,1),(0,-1),(-1,0)]
ALL = [*DIRECTIONS,(1,1),(1,-1),(-1,1),(-1,-1)]
class Tags(Enum):
    Empty, Child, Robot, Obstacle, Dirty, Roller, Loaded_Roller = range(7)

def safe_index(env,x,y):
    return x < env.n and y < env.m and x >= 0 and y >= 0

