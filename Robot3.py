#Currently discontinued
from Agent import Agent
from Utils import *
from Env_Objects import *
import random

class Robot3(Agent):
    def __init__(self,active, enviroment):
        super().__init__(active, enviroment)
        self.tag = Tags.Robot
        self.child = None
        self.saved = Empty()
        self.i = -1
        self.decision = random.randint(0,1)

    def search_closest(self,env, tag, x ,y):
        visited={}
        visited[(x,y)]=(x,y)
        neighbors = []
        for xdir, ydir in DIRECTIONS:
            if safe_index(env,x+xdir,y+ydir):
                neighbors.append((x+xdir,y+ydir))
                visited[((x+xdir,y+ydir))] = (x+xdir,y+ydir)
        while len(neighbors) != 0:
            nx, ny = neighbors.pop(0)
            if not self.child is None:
                if env.grid[nx][ny].tag is Tags.Child:
                    continue
            if env.grid[nx][ny].tag is Tags.Obstacle or env.grid[nx][ny].tag is Tags.Loaded_Roller:
                continue
            if env.grid[nx][ny].tag is tag:
                return visited[(nx,ny)]
            for xdir, ydir in DIRECTIONS:
                if safe_index(env,nx+xdir,ny+ydir) and not (nx+xdir,ny+ydir) in visited:
                    neighbors.append((nx+xdir,ny+ydir))
                    visited[((nx+xdir,ny+ydir))] = visited[(nx,ny)]
        return (-1,-1)

    def step(self):
        x, y = self.position
        env = self.enviroment 
        neighbors = []
        for xdir, ydir in DIRECTIONS:
            if safe_index(env,x+xdir,y+ydir):
                neighbors.append((x+xdir,y+ydir))
        lpos = (-1,-1)
        
        if  self.decision == 1:
            lpos = self.search_closest(env,Tags.Dirty,x,y)
            if lpos == (-1,-1):
                return
            nx, ny = lpos
            env.grid[x][y] = self.saved
            self.saved = env.grid[nx][ny]
            env.grid[nx][ny] = self
            self.set_pos(nx,ny)
        
        else:
            if self.child is None:
                lpos = self.search_closest(env,Tags.Child,x,y)
                if lpos == (-1,-1):
                    return
                nx, ny = lpos
                if env.grid[nx][ny].tag is Tags.Child:
                    self.child = env.grid[nx][ny]
                    env.grid[nx][ny] = self
                    env.grid[x][y] = self.saved
                    self.saved = Empty()
                    self.set_pos(nx,ny)
                else:
                    env.grid[x][y] = self.saved
                    self.saved = env.grid[nx][ny]
                    env.grid[nx][ny] = self
                    self.set_pos(nx,ny)
            
            else:
                lpos = self.search_closest(env,Tags.Roller,x,y)
                if lpos == (-1,-1):
                    return
                nx, ny = lpos
                if env.grid[nx][ny].tag is Tags.Roller:
                    env.grid[x][y] = self.saved
                    self.saved = Loaded_Roller()
                    self.child = None
                    self.decision = random.randint(0,1)
                    env.children = env.children - 1 
                    env.grid[nx][ny] = self
                    self.set_pos(nx,ny)
                else:
                    env.grid[x][y] = self.saved
                    self.saved = env.grid[nx][ny]
                    env.grid[nx][ny] = self
                    self.set_pos(nx,ny)

    def action(self):
        if not self.active:
            return
        if self.enviroment.children == 0:
            self.decision = 1
        if self.enviroment.filthy == 0:
            self.decision = 0
    
        if self.decision == 1:
            if self.saved.tag is Tags.Dirty:
                self.saved = Empty()
                self.enviroment.filthy = self.enviroment.filthy - 1
                self.decision = random.randint(0,1)
            else:
                self.step()
        else:
            if self.child is None:
                self.step()
            else:
                self.step()
                if not self.saved.tag is Tags.Loaded_Roller:
                    self.step()