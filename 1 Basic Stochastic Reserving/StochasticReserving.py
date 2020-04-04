
class Stochastic_Reserving:
    Pareto_Alpha = 0
    Pareto_Theta = 0

    def __init__(self, alpha, theta):
        self.Pareto_Alpha = alpha
        self.Pareto_Theta = theta

    def pareto(self, x):
        return 1 - (self.Pareto_Theta / (x + self.Pareto_Theta)) ** self.Pareto_Alpha
        