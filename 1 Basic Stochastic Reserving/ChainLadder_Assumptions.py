# CAS Exam 7

import math
    
class Chain_Ladder_Venter():

    def convert_2_triangle(self, rawTable, size):
        triangle = {}
        cursor = 0
        for ay in range(1, size + 1):
            for dy in range(1, size + 1):   
                triangle[ay*10 + dy] = rawTable[cursor]
                cursor += 1
        return triangle


    # Describe two other approaches that Venter proposes for comparing or evaluating different models.
    # Commentary on Question:
    # Any two of the following are sufficient for full credit.
    #  Test the significance of the estimated factors.
    #  Examine the residuals to determine if the model is linear in the specified manner.
    #  Examine the residuals over time to determine if there are any patterns.


    # Implication 2: Superiority to Alternative Emergence Patterns

    def adjusted_SSE(self, SSE, n, p):
        return SSE / (n-p)**2

    def adjusted_SSE_AIC(self, SSE, n, p):
        return SSE * math.exp(2 * p / n)

    def adjusted_SSE_BIC(self, SSE, n, p):
        return SSE * n ** (p/n)

    # Venter proposes investigating models other than the standard chain ladder 
    #   (1) Add a constant after multiplying by the chain ladder development factor.
    #   (2) Multiplication of factors representing the accident year and development year. 
    #       This can also be described as a parameterized version of the Bornhuetter Ferguson method.
    #   (3) As in number (2) but add a factor for calendar year.

