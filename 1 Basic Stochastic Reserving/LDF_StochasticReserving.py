# CAS Exam 7
# Clark


import math

class Stochastic_Reserving:    

    def __init__(self):
        self.Alpha = 0
        self.Theta = 0

    def pareto(self, x):
        return 1 - (self.Theta / (x + self.Theta)) ** self.Alpha
    
    def exponential(self, x):
        return 1 - math.exp(-x/self.Theta)

    def total_standard_deviation(self, variance, amount, sd):
        return (variance * amount + sd ** 2) ** 0.5

    def average_age(self, year):
        if year <= 1:
            return 6
        else:
            return self.average_age(year - 1) + 12