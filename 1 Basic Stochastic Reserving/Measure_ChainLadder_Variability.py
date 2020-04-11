# CAS Exam 7
# Measuring the Variability of Chain Ladder Reserve Estimates
# Thomas Mack 1994

class Chain_Ladder:    
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
    
    # Mack's method
    def proportionality_constants(self, a):
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
            a_less_1 = self.proportionality_constants(a-1)
            a_less_2 = self.proportionality_constants(a-2)
            return  a_less_1 ** 2 / a_less_2             
        
    def standard_error(self, ay):    
        dy = self.Dimension - ay + 1   
        error = 0
        if dy >= self.Dimension:
            return error

        for d in range(dy, self.Dimension):
            
            a2 = self.proportionality_constants(d)
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
