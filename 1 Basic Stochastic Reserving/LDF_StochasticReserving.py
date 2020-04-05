import numpy as np

class Stochastic_Reserving:    

    def __init__(self):
        self.Alpha = 0
        self.Theta = 0

    def pareto(self, x):
        return 1 - (self.Theta / (x + self.Theta)) ** self.Alpha
    
    def exponential(self, x):
        return 1 - np.exp(-x/self.Theta)