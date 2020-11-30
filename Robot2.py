from Agent import Agent
from Utils import *
from Env_Objects import *
import random

class Robot2(Agent):
    def __init__(self,active, enviroment):
        super().__init__(active, enviroment)
        self.tag = Tags.Robot
        self.child = None
        self.saved = Empty()
        self.i = -1
        self.path = []

    def search_closest(self,env, tag, x ,y):
        visited={}
        visited[(x,y)]=[]
        neighbors = [(x,y)]
        while len(neighbors) != 0:
            nx, ny = neighbors.pop(0)
            if not self.child is None:
                if env.grid[nx][ny].tag is Tags.Child:
                    continue
            if env.grid[nx][ny].tag is Tags.Obstacle or env.grid[nx][ny].tag is Tags.Loaded_Roller:
                continue
            if env.grid[nx][ny].tag is tag:
                return  [*visited[(nx,ny)],(nx+xdir,ny+ydir)]
            for xdir, ydir in DIRECTIONS:
                if safe_index(env,nx+xdir,ny+ydir) and not (nx+xdir,ny+ydir) in visited:
                    neighbors.append((nx+xdir,ny+ydir))
                    visited[((nx+xdir,ny+ydir))] = [*visited[(nx,ny)],(nx+xdir,ny+ydir)]
        return []

    def reset(self):
        self.child = None
        self.saved = Empty()
        self.i = -1
        self.path = []

    def find_path(self):
        x, y = self.position
        env = self.enviroment 
        
        if  self.enviroment.children == 0:
            self.path = self.search_closest(env,Tags.Dirty,x,y)
        elif self.child is None:
            self.path = self.search_closest(env,Tags.Child,x,y)
        else:
            self.path = self.search_closest(env,Tags.Roller,x,y)

    def step(self):
        x,y = self.position
        if not self.path:
            self.find_path()
        if not self.path:
            return
        nx,ny = self.path.pop(0)
        env = self.enviroment
        if env.grid[nx][ny].tag is Tags.Obstacle or env.grid[nx][ny].tag is Tags.Loaded_Roller or (not self.child is None and env.grid[nx][ny].tag is Tags.Child):
            self.find_path()
            if not self.path:
                return
            nx,ny = self.path.pop(0)
        if abs(x-nx)+(y-ny) != 1:
            self.find_path()
            if not self.path:
                return
            nx,ny = self.path.pop(0)
        if self.child is None:
            if env.grid[nx][ny].tag is Tags.Child:
                self.child = env.grid[nx][ny]
                env.grid[nx][ny] = self
                env.grid[x][y] = self.saved
                self.saved = Empty()
                self.set_pos(nx,ny)
                self.path = []
            else:
                env.grid[x][y] = self.saved
                self.saved = env.grid[nx][ny]
                env.grid[nx][ny] = self
                self.set_pos(nx,ny)
        else:
            if env.grid[nx][ny].tag is Tags.Roller:
                env.grid[x][y] = self.saved
                self.saved = Loaded_Roller()
                self.child = None
                env.children = env.children - 1 
                env.grid[nx][ny] = self
                self.set_pos(nx,ny)
                self.path = []
            else:
                env.grid[x][y] = self.saved
                self.saved = env.grid[nx][ny]
                env.grid[nx][ny] = self
                self.set_pos(nx,ny)

    def action(self):
        if not self.active:
            return
        if self.enviroment.children == 0 and self.saved.tag is Tags.Dirty:
                self.saved = Empty()
                self.enviroment.filthy = self.enviroment.filthy - 1
                self.path = []
        elif self.child is None:
            self.step()
        else:
            self.step()
            if not self.saved.tag is Tags.Loaded_Roller:
                self.step()