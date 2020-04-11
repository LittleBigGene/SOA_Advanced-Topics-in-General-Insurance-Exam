# CAS Exam 7
# Measuring the Variability of Chain Ladder Reserve Estimates
# Thomas Mack 1994

class Chain_Ladder:    
    # 1 Introduction and Overview
    def __init__(self, triangle):
        self.Triangle = triangle
        self.Dimension = max(triangle.keys()) // 10
        
        self.AgeToAgeFactors = []
        self.AgeToUltimateFactors = []

        for dev in range(1, self.Dimension):
            currTotal, nextTotal = 0, 0           
            for acc in range(1, self.Dimension - dev + 1):
                currTotal += triangle[ acc * 10 + dev    ]
                nextTotal += triangle[ acc * 10 + dev + 1]
        
            self.AgeToAgeFactors.append(nextTotal / currTotal)            

        cumulativeFactor = 1
        for ageFactor in reversed(self.AgeToAgeFactors):            
            cumulativeFactor = round(cumulativeFactor * ageFactor, 8)
            self.AgeToUltimateFactors.insert(0, cumulativeFactor)          
         
        # print(f'AgeToAgeFactor {self.AgeToAgeFactors}')            
        # print(f'AgeToUltFactor {self.AgeToUltimateFactors}')

    # 2 Notations and First Analysis of the Chain Ladder Method
    #   C_i_k
    #   f_k

    # 3 Analysis of the Age-to-Age Factor Formula: the Key to Measuring the Variability

    #   (1) The expected value is the previous value times a constant that depends only on the development year. 
    #       This assumption does not prevent values from decreasing because it only relates to the expected, not the actual value. 
    #       Alternatively, the constant can be less than one, which implies an expected decrease.
    #   (2) The variance is the previous value times a factor that depends only on the development year. 
    #       This assumption does not prevent values from decreasing because with variability in outcomes, that could extend to decreasing values.
    #   (3) Values from different accident years are independent. 
    #       This assumption makes no statement about the magnitude of the values and so allows for decreasing values.


    # 4 Quantifying the Variability of the Ultimate Claims Amount
    # a^2_k
    def a_proportionality_constant(self, a):
        f0 = self.AgeToAgeFactors[a-1]        
        meanSquareError = 0       
        for j in range(1, self.Dimension - a + 1):
            c0 = self.Triangle[ j * 10 + a] 
            c1 = self.Triangle[ j * 10 + a + 1] 
            meanSquareError += c0 * ((c1 / c0 - f0) ** 2)
            #print(f'MeanSquareError c1={c1} c2={c2} f={self.AgeToAgeFactors[a-1]}' )
        
        if (self.Dimension - a - 1) > 0:
            return meanSquareError / (self.Dimension - a - 1)
        else:
            a_less_1 = self.a_proportionality_constant(a-1)
            a_less_2 = self.a_proportionality_constant(a-2)
            return  a_less_1 ** 2 / a_less_2             

    def standard_error(self, ay):    
        dy = self.Dimension - ay + 1   
        error = 0
        if dy >= self.Dimension:
            return error

        for d in range(dy, self.Dimension):
            
            a2 = self.a_proportionality_constant(d)
            f = self.AgeToAgeFactors[d-1]

            k = d
            c = self.Triangle[ ay * 10 + dy] 
            while k > dy:  
                k = k - 1                                              
                c = c * self.AgeToAgeFactors[k - 1]

            s = 0
            for r in range(1, self.Dimension - d + 1):
                s += self.Triangle[r * 10 + d ]
            
            error += a2 / f**2 * (1/s + 1/c)                     

        ult = self.Triangle[ ay * 10 + dy  ] * self.AgeToUltimateFactors[dy-1] 
        error = ult ** 2 * error
        return error ** 0.5


    # 5 Checking the Chain Ladder Assumptions Against the Data
    # 6 Numerical Example
    # 7 Final Remark

    # Appendix A: Unbiasedness of Age-to-Age Factors
    # Appendix B: Minimizing the Variance of Independent Estimators
    # Appendix C: Unbiasedness of the Estimated Ultimate Claims Amount
    # Appendix D: Calculation of the Standard Error of C_iI
    # Appendix E: Unbiasedness of the Estimator a^2_k
    # Appendix F: The Standard Error of the Overall Reserve Estimate
    # Appendix G: Testing for Correlations between Subsequent Development Factors
    # Appendix H: Testing for Calendar Year Effects


    def natural_starting_values(self, f):
        if (f == 1):                
            result = 1 / self.AgeToUltimateFactors[f - 1]            
        else:
            result = (self.AgeToAgeFactors[f-2] - 1) / self.AgeToUltimateFactors[f - 2]
        
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
    
    
        
