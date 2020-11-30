from Utils import *
from Env_Agents import *
from Env_Objects import *
from Robot import *
from Robot2 import *
import random
import numpy as np


class Enviroment:
    def __init__(self,n:int,m:int,t:int,pcfilthy:int,pcobstacles:int,children:int, cycles:int = 100):
        self.n = n
        self.m = m
        self.t = t
        self.grid = None
        self.cycles = cycles
        self.children = children
        self.rollers = children
        self.robot = Robot(True,self)
        self.filthy = int(pcfilthy*(n*m))
        self.xfilthy = self.filthy
        self.obstacles = int(pcobstacles*(n*m))
        if self.filthy/(self.n*self.m - self.children - self.rollers - self.obstacles - 1) >= 0.6:
            print("Initial configuration cannot be an end state.")
        if self.filthy==0 and self.children==0:
            print("Initial configuration cannot be an end state.")
        total = n*m
        if total*(pcfilthy + pcobstacles) + children*2 + 1 > total:
            print("Invalid initial configuration.")
        
    
    def variate(self):
        total = self.n*self.m
        n = self.n
        m = self.m
        self.grid = []
        for i in range(n):
            self.grid.append([])
            for j in range(m):
                self.grid[i].append(Empty())
        lrandom = [x for x in range(total)]
        random.shuffle(lrandom)

        if self.rollers !=0:
            fstroller = lrandom.pop()
            i,j = (fstroller//m,fstroller%m)
            rollers_pos = []
            rollers_pos.append((i,j))
            self.grid[i][j] = Roller()
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            while len(rollers_pos) != self.rollers:
                x,y = random.choice(rollers_pos)
                neighbors = []
                for xdir,ydir in dirs:
                    if safe_index(self,x+xdir,y+ydir):
                        if self.grid[x+xdir][y+ydir].tag is Tags.Empty:
                            neighbors.append((x+xdir,y+ydir))
                if len(neighbors) == 0:
                    continue
                nx, ny = random.choice(neighbors)
                rollers_pos.append((nx,ny))
                self.grid[nx][ny] = Roller()
                lrandom.remove((nx*m)+ny)
            loaded = self.rollers-self.children
            for i in range(loaded):
                nx, ny = random.choice(rollers_pos)
                self.grid[nx][ny] = Loaded_Roller()
                rollers_pos.remove((nx,ny))

        filthy = self.filthy
        obstacles =self.obstacles
        children = self.children
        if not self.robot.child is None:
            children = children-1
        for i in range(filthy + obstacles + children):
            ran = lrandom[i]
            x = ran//m
            y = ran%m
            if i < filthy:
                self.grid[x][y] = Dirty()
            elif i < filthy + obstacles:
                self.grid[x][y] = Obstacle()
            elif i < filthy + obstacles + children:
                self.grid[x][y] = Child(True,self)
                self.grid[x][y].set_pos(x,y)
        possible = [(x,y) for x in range(self.n) for y in range(self.m) if self.grid[x][y].tag == self.robot.saved.tag]
        rx,ry = random.choice(possible)
        self.grid[rx][ry]=self.robot
        self.grid[rx][ry].set_pos(rx,ry)
    
    def change_robot(self,robot):
        robot.child = self.robot.child
        robot.saved = self.robot.saved
        self.robot = robot
        if self.grid:
            for x in range(self.n):
                for y in range(self.m):
                    if self.grid[x][y].tag is Tags.Robot:
                        self.grid[x][y] = self.robot
                        self.grid[x][y].set_pos(x,y)

    def paint(self):
        for x in range(self.n):
            string = ""
            for y in range(self.m):
                grid = self.grid
                if grid[x][y].tag is Tags.Robot:
                    string = string + "A"
                elif grid[x][y].tag is Tags.Child:
                    string = string + "B"
                elif grid[x][y].tag is Tags.Empty:
                    string = string + "-"
                elif grid[x][y].tag is Tags.Obstacle:
                    string = string + "O"
                elif grid[x][y].tag is Tags.Roller:
                    string = string + "R"
                elif grid[x][y].tag is Tags.Loaded_Roller:
                    string = string + "L"
                elif grid[x][y].tag is Tags.Dirty:
                    string = string + "D"
                string = string + " "
            print(string)
        print("-"*self.m*2)

    def simulate(self):
        dirty = 0
        self.children = self.rollers
        self.filthy = self.xfilthy
        self.robot.reset()
        self.variate()
        # self.paint()
        for i in range(1,self.t*self.cycles+1):
            for x in range(self.n):
                if self.robot.i < i:
                    self.robot.action()
                    self.robot.i = i
                for y in range(self.m):
                    elem = self.grid[x][y]
                    if elem.tag is Tags.Child:
                        if elem.i < i:
                            elem.i = i
                            elem.action()
            # self.paint()
            if i!=0 and i%self.t == 0:
                self.variate()
            dirty = dirty + (self.filthy/(self.n*self.m))
            if (self.n*self.m - self.children - self.rollers - self.obstacles - 1) != 0 and self.filthy/(self.n*self.m - self.children - self.rollers - self.obstacles - 1)>= 0.6:
                return (False,True,dirty,i)
            if self.filthy == 0 and self.children == 0:
                return (True,False,dirty,i)
        return (False,False,dirty,(self.t*self.cycles))
