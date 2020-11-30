from Utils import *
from Env_Agents import *
from Env_Objects import *
from Enviroment import *
from Robot import *
from Robot2 import *
import copy
import random
import numpy as np

envnum = 10
repnum = 30
i = 0
ambientes = [(0.05,0.02,0.01),(0.2,0.02,0.02),(0.06,0.08,0.01),(0.05,0.2,0.02),(0.05,0.02,0.03),(0.05,0.02,0.04),(0.05,0.2,0.04),(0.12,0.3,0.04),(0.12,0.3,0.03),(0.24,0.3,0.04)]
while i<envnum:
    t = random.randint(8,12)
    n = random.randint(8,12)
    m = random.randint(8,12)
    total = n*m
    dirty, obstacles ,children = ambientes[i]
    children = int(total*children)
    env = Enviroment(n=n,m=m,t=t,pcfilthy=dirty,pcobstacles=obstacles,children=children, cycles = 100)
    newenv2 = copy.deepcopy(env)
    robot = Robot2(True,newenv2)
    newenv2.change_robot(robot)
    print("New Enviroment: n="+str(env.n)+"  m="+str(env.m)+"  t="+str(env.t)+" dirty="+str(dirty*100)+"%"+"  obstacles="+str(obstacles*100)+"%"+"   children="+str(env.children))
    j=0
    canterm = 0
    cantdespedido = 0
    sumdirty = 0
    sumturns = 0
    canterm2 = 0
    cantdespedido2 = 0
    sumdirty2 = 0
    sumturns2 = 0
    while j < repnum:
        newenv =  env
        clean, fired, filthy, turns = newenv.simulate()
        clean2, fired2, filthy2, turns2 = newenv2.simulate()
        if clean:
            canterm += 1
        if fired:
            cantdespedido += 1
        sumdirty += filthy
        sumturns += turns
        if clean2:
            canterm2 += 1
        if fired2:
            cantdespedido2 += 1
        sumdirty2 += filthy2
        sumturns2 += turns2 
        # print("Finished a simulation"+"   Clean end:"+str(clean)+"   Robot fired:"+str(fired)+"   Filthy="+str(filthy/turns)+"%")
        j = j + 1
    print("Finished an enviroment:")
    # print("Robots | All Clean |  Fired  | Mean of dirty  ")
    # print("Robot1 | "+str(canterm)+"  | "+str(cantdespedido)+"   | "+str(sumdirty/sumturns)+"%")
    # print("Robot2 |"+str(canterm2)+"  | "+str(cantdespedido2)+"  | "+str(sumdirty2/sumturns2)+"%")
    print("Robot1 results =   Totally clean end states:"+str(canterm)+"   Robots fired:"+str(cantdespedido)+"   Filthy percent mean="+str(sumdirty/sumturns)+"%")
    print("Robot2 results =   Totally clean end states:"+str(canterm2)+"   Robots fired:"+str(cantdespedido2)+"   Filthy percent mean="+str(sumdirty2/sumturns2)+"%")
    print("-----------------------------------------------------------------------------------")
    i = i + 1