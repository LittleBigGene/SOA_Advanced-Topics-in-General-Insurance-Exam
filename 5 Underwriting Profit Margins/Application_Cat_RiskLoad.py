# CAS Exam 9
# An Application of Game Theory: Property Catastrophe Risk Load
# Donald F. Mango
# Two well known methods for calculating risk load
# Marginal Surplus and Marginal Variance

import math
import numpy

class Risk_Load:

    #def __init__(self) -> None:

    def binomial_variance(self, p, L):
        return p * (1-p) * L**2

    def marginal_surplus_Z(self, r = 1 , y = 1, S_1 = 1, S_0 = 0):
        # print(f'r = {r}')
        # print(f'S_1 - S_0 = {S_1 - S_0}')
        # print(f'y / (1+y) = {y / (1+y)}')
        z = r / (S_1 - S_0) / (y / (1+y) )
        return z

    def marginal_surplus_R(self, z = 1 , y = 1, S_1 = 1, S_0 = 0):
        # print(f'z = {z}')
        # print(f'S_1 - S_0 = {S_1 - S_0}')
        # print(f'y / (1+y) = {y / (1+y)}')
        r = y * z / (1+y) * (S_1 - S_0)
        return r

    def marginal_variance(self, variance, covariance):
        return variance + 2 * covariance
    
    def shapley(self, variance, covariance):
        return variance + covariance

    def covariance_share(self, loss_x, loss_y, loss_xy, 
                                var_x,  var_y,  var_xy):
        x, y = sum(var_x), sum(var_y)

        for i in range(2):
            weight_x = loss_x[i]/loss_xy[i] 
            weight_y = loss_y[i]/loss_xy[i] 
            cov = var_xy[i] - var_x[i] - var_y[i]

            x += weight_x * cov
            y += weight_y * cov
            
        return [x,y]