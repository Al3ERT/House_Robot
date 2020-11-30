class Agent:
    def __init__(self, active, enviroment):
        self.tag = None
        self.active = active
        self.enviroment = enviroment
    
    def action(self):
        pass

    def set_pos(self,x,y):
        self.position = (x,y)
    
    def activate(self):
        self.active = True
    
    def lock(self):
        self.active = False