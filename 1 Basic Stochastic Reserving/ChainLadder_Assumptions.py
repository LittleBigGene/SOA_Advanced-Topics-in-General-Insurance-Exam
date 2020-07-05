# CAS Exam 7
import math
from ChainLadder_Measure_Variability import Chain_Ladder_Mack

class Chain_Ladder_Venter(Chain_Ladder_Mack):

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

    def natural_starting_values(self, f, show=False):
        i = f-1
        if (f == 1):      
            if show:
                print(f'f({f}) = 1/{self.AgeToUltimateFactors[i]}')                      
            result = 1 / self.AgeToUltimateFactors[i]            
        else:            
            if show:
                print(f'f({f}) = ({self.AgeToAgeFactors[i-1]} - 1 ) / {self.AgeToUltimateFactors[i-1]}')
                        
            result = (self.AgeToAgeFactors[i-1] - 1 ) / self.AgeToUltimateFactors[i-1]
        

        return result

    def starting_values (self, h): 
        cumulative = []  
        for (key, value) in self.Triangle.items():
            if (key // 10 == h):
                cumulative.append(value)        
        
        incremental = []
        incremental.append(cumulative[0])
        if len(cumulative) > 1 :
            
            numerator, denominator = 0, 0
            for dev in range(1, len(cumulative)):
                incremental.append(cumulative[dev] - cumulative[dev - 1])

            for dev in range(1, len(incremental) + 1):                                               
                nsv = self.natural_starting_values(dev)
                numerator += nsv * incremental[dev - 1]
                denominator += nsv ** 2
        else:
            nsv = self.natural_starting_values(1)
            numerator = nsv * cumulative[0]
            denominator = nsv ** 2

        # print(f'Incremental {incremental}')

        return numerator / denominator   