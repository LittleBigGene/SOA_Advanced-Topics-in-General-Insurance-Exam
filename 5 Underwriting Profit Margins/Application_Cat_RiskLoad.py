# CAS Exam 9
# An Application of Game Theory: Property Catastrophe Risk Load
# Donald F. Mango
# Two well known methods for calculating risk load
# Marginal Surplus and Marginal Variance

class Risk_Load:

    #def __init__(self) -> None:

    def Variance_Binomial(self, p, L):
        return p * (1-p) * L**2

    def Marginal_Surplus_Z(self, r = 1 , y = 1, S_1 = 1, S_0 = 0):
        print(f'r = {r}')
        print(f'S_1 - S_0 = {S_1 - S_0}')
        print(f'y / (1+y) = {y / (1+y)}')
        z = r / (S_1 - S_0) / (y / (1+y) )
        return z

    def Marginal_Surplus_R(self, z = 1 , y = 1, S_1 = 1, S_0 = 0):
        print(f'z = {z}')
        print(f'S_1 - S_0 = {S_1 - S_0}')
        print(f'y / (1+y) = {y / (1+y)}')
        r = y * z / (1+y) * (S_1 - S_0)
        return r

    def Standard_Deviation (self, v):
        return v ** 0.5
