from Agent import Agent
from Utils import *
from Env_Objects import *
import random

class Child(Agent):
    def __init__(self,active, enviroment):
        super().__init__(active, enviroment)
        self.tag = Tags.Child
        self.saved = Empty()
        self.i=-1
    
    def action(self):
        def push(env,xdir,ydir,x,y):
            
            if not safe_index(env,x+xdir,y+ydir):
                return False
            if env.grid[x+xdir][y+ydir].tag is Tags.Obstacle:
                if push(env,xdir,ydir,x+xdir,y+ydir):
                    env.grid[x+xdir][y+ydir] = env.grid[x][y]
                    return True
            elif env.grid[x+xdir][y+ydir].tag is Tags.Empty:
                env.grid[x+xdir][y+ydir] = env.grid[x][y]
                return True
            return False

        if not self.active:
            return
        xdir, ydir = random.choice(DIRECTIONS)
        if random.random() < 0.20:
            xdir,ydir = (0,0)
        x,y = self.position
        env = self.enviroment
        if not safe_index(env,x+xdir,y+ydir):
            return
        elif xdir == 0 and ydir == 0:
            pass
        elif env.grid[x+xdir][y+ydir].tag is Tags.Obstacle:
            if push(env,xdir,ydir,x+xdir,y+ydir):
                env.grid[x][y] = self.saved
                self.saved = env.grid[x+xdir][y+ydir]
                env.grid[x+xdir][y+ydir] = self
                self.set_pos(x+xdir,y+ydir)
        elif env.grid[x+xdir][y+ydir].tag is Tags.Empty:
            env.grid[x][y] = self.saved
            self.saved = env.grid[x+xdir][y+ydir]
            env.grid[x+xdir][y+ydir] = self
            self.set_pos(x+xdir,y+ydir)
    
        neighbors = []
        for xdir, ydir in ALL:
            if safe_index(env,x+xdir,y+ydir):
                neighbors.append((x+xdir,y+ydir))
        empty = [(x,y) for (x,y) in neighbors if env.grid[x][y].tag is Tags.Empty]
        childs = len([(x,y) for (x,y) in neighbors if env.grid[x][y].tag is Tags.Child])
        dirty = 1
        if childs == 2:
            dirty = 3
        elif childs > 2:
            dirty = 6
        amount = random.randint(0,min(len(empty),dirty))
        for x,y in random.sample(empty,amount):
            env.grid[x][y]=Dirty()
            env.filthy+=1

        

