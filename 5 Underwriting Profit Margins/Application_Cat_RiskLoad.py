# CAS Exam 9
# An Application of Game Theory: Property Catastrophe Risk Load
# Donald F. Mango
# Two well known methods for calculating risk load
# Marginal Surplus and Marginal Variance

import math
import numpy

class Risk_Load:
    # 1 Introduction
    def __init__(self) -> None:
        self.p = [0,0]
        self.var_x = [0,0]
        self.var_y = [0,0]
        self.var_xy = [0,0]

    # 2 The catastrophe occurrence size-of-loss ditribution

    def binomial_variances(self, Loss):
        result = []
        for p, L in zip(self.p, Loss):
            result.append(self.binomial_variance(p, L))
        return result
        
    def binomial_variance(self, prob, Loss):
        return prob * (1-prob) * Loss**2


    # 3 The marginal surplus (MS) method

    def marginal_surplus_Z(self, r = 1 , y = 1, S_1 = 1, S_0 = 0):
        # print(f'r = {r}')
        # print(f'S_1 - S_0 = {S_1 - S_0}')
        # print(f'y / (1+y) = {y / (1+y)}')
        z = r / (S_1 - S_0) / (y / (1+y) )
        return z

    def marginal_surplus(self, z = 1 , y = 1, S_1 = 1, S_0 = 0):
        # print(f'z = {z}')
        # print(f'S_1 - S_0 = {S_1 - S_0}')
        # print(f'y / (1+y) = {y / (1+y)}')
        r = y * z / (1+y) * (S_1 - S_0)
        return r

    # 4 The marginal variance (MV) method

    def marginal_variance(self, variance, covariance, λ = 1):
        return λ * (variance + 2 * covariance )
    
    #   where λ is a multiplier similar to yz/(1+y) from the MS method
    #   although dimensioned to apply to variance rather than standard deviation.


    # 5 Building up a portfolio of two accounts
    #   TABLE 1 Building X and Y: MS method
    #   TABLE 2 Building X and Y: MV method

    # 6 Renewing the portfolio of two accounts
    #   TABLE 3 Renewing X and Y: MS method
    #   TABLE 4 Renewing X and Y: MV method

    def mv_renewal_risk_load(self, L_x, L_y, λ):
        L_xy = [x + y for x, y in zip(L_x, L_y)]

        sol_x = (sum(self.var_xy) - sum(self.var_y) ) * λ
        sol_y = (sum(self.var_xy) - sum(self.var_x) ) * λ
        
        return [sol_x, sol_y]

    # 7 Exploring the differences between new and renewal

    #   Build-Up Δ Std Dev(X) = Std Dev (X)
    #   Renewal  Δ Std Dev(X) = Std Dev (X + Y) - Std Dev (Y)        

    #   recall square root operator is sub-additive: the sq root of a sum < the sum of sq roots
    #   therefore, one would expect renewal < build-up when MS method is applied

    #   Build-Up Δ Var(X) = Var (X)
    #   Renewal  Δ Var(X) = Var (X + Y) - Var (Y) 
    #                     = [Var(X) + 2Cov(X,Y) + Var(Y)] - Var(Y)     
    #                     = Var(X) + 2Cov(X,Y)
    #   therefore, one would expect renewal > build-up when MV method is applied

    # 8 A new concept: renewal additivity
    # 9 A new approach from game theory
    #   characteristic function v()
    #   sub-additive:
    #       v(S) + v(T) > v(S ⋃ T) ∀ disjoint S & T
    #   super-additive:
    #       v(S) + v(T) < v(S ⋃ T) ∀ disjoint S & T

    #   TABLE 6, the Shapley value is the straight average of MV, over six permutations
    #   Shapley Value = Var(n) + Cov(L, n); where L = existing portfolio, n = new account
    def shapley(self, variance, covariance, λ = 1):
        return λ * (variance + covariance)


    #10 Sharing the covariance

    def covariance_share(self, loss_x, loss_y, λ = 1):
        loss_xy = [x + y for x, y in zip(loss_x, loss_y)]

        x, y = sum(self.var_x), sum(self.var_y)

        for i in range(2):
            weight_x = loss_x[i]/loss_xy[i] 
            weight_y = loss_y[i]/loss_xy[i] 
            cov = self.var_xy[i] - self.var_x[i] - self.var_y[i]

            x += weight_x * cov
            y += weight_y * cov
            
        return [ x * λ, y * λ ]

    #   TABLE 7 Building up X and Y: Shapley Value Method
    #   TABLE 8 Building up X and Y: Covariance Share Method

    #11 Appliping the Shapley and CS methods to the example
    
    #   TABLE 9 Renewing X and Y: Shapley Value Method
    #   TABLE 10 Renewing X and Y: Covariance Share Method

    #12 Conclusion