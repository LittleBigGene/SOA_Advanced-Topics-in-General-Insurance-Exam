# CAS Exam 7
# Clark

import math

class Stochastic_Reserving:    

    # 1 Expected Loss Emergence

    def __init__(self):
        self.α = 0
        self.θ = 0
        self.ω = 0

    def pareto(self, x):
        return 1 - (self.θ / (x + self.θ)) ** self.α

    def loglogistic(self, x):
        return x ** self.ω / (x ** self.ω + self.θ  ** self.ω)

    def exponential(self, x):
        return 1 - math.exp(-x/self.θ)

    def weibull(self, x):
        return 1 - math.exp( - (x/self.θ)**self.ω )

    # 2 The Distribution of Actual Loss Emergence and Maximum Likelihood

    def total_standard_deviation(self, variance, amount, sd):
        return (variance * amount + sd ** 2) ** 0.5


    def estimate_variance(self, increments, ULTs, Gs, dof):        
        variance = 0 
        for actual, ult, g in zip(increments, ULTs, Gs):
            estimate = ult * g
            variance += (actual - estimate) ** 2 / estimate

        return  variance / dof

    # 3 Key Assumptions of this Model
    #   Incremental losses are independent and identically distributed(iid)
    #   The Variance / Mean Scale Parameter σ^2 is fixed and known
    #   Variance estimates are based on an approximation to the Rao-Cramer lowerbound.

    # 4 A Practical Example



    # 5 Comments and Conclusion


    # Appendix A: Derivatives of the Loglikelihood Function

    # Appendix B: Adjustments for Different Exposure Periods

    #   Calculate the average accident date of the period that is earned
    def average_age(self, year):
        if year <= 1:
            return year*12/2
        else:
            return self.average_age(year - 1) + 12