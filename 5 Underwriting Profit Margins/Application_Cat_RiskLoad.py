# CAS Exam 9
# An Application of Game Theory: Property Catastrophe Risk Load
# Donald F. Mango
# Two well known methods for calculating risk load
# Marginal Surplus and Marginal Variance

import math
import numpy
from sympy import solve

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
    def marginal_surplus(self, r=1, z=1, y=1, SD_L1 = 1, SD_L0 = 0):
        
        # y, the required return

        sol = solve(y * z / (1+y) * (SD_L1 - SD_L0) - r)
        return sol[0] 

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

    def covariance_share(self, loss_x, loss_y, λ = 1, show=False):
        loss_xy = [x + y for x, y in zip(loss_x, loss_y)]
        x, y = sum(self.var_x), sum(self.var_y)
        if show:
            print(f'var_x={x} var_y={y}')

        for i in range(2):
            weight_x = loss_x[i]/loss_xy[i] 
            weight_y = loss_y[i]/loss_xy[i] 
            total_cov = self.var_xy[i] - self.var_x[i] - self.var_y[i]
            
            x += weight_x * total_cov
            y += weight_y * total_cov
            if show:
                print(f'event {i+1} total cov = {round(total_cov)} \t var_x={x} \t weight_x={round(weight_x,4)} \t var_y={y} \t weight_y={round(weight_y,4)}')

            
        return [ x * λ, y * λ ]

    #   TABLE 7 Building up X and Y: Shapley Value Method
    #   TABLE 8 Building up X and Y: Covariance Share Method

    #11 Appliping the Shapley and CS methods to the example
    
    #   TABLE 9 Renewing X and Y: Shapley Value Method
    #   TABLE 10 Renewing X and Y: Covariance Share Method

    #12 Conclusion