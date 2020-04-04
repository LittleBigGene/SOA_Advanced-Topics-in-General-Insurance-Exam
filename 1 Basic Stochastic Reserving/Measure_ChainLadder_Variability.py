# Measuring the Variability of Chain Ladder Reserve Estimates
# Thomas Mack

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
        meanSquareError = 0        
        for acc in range(1, self.Dimension - a + 1):
            c1 = self.Triangle[ acc * 10 + a] 
            c2 = self.Triangle[ acc * 10 + a + 1] 
            meanSquareError += c1 * ((c2 / c1 - self.AgeToAgeFactors[a-1]) ** 2)
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

if __name__ == "__main__":
    paidClaims = { 11: 9659, 12:15468, 13:17887, 14:18236, 15:18910, 16:19262, 17:19644,
                   21:10731, 22:17668, 23:22333, 24:24701, 25:24827, 26:25331,
                   31:11715, 32:11037, 33:14503, 34:14707, 35:16414,                                        
                   41:12450, 42:15686, 43:19069, 44:23888,
                   51:13574, 52:15924, 53:17706, 
                   61:14717, 62:20165,
                   71:16100 }

    paidTriangle = Chain_Ladder(paidClaims)
    #print(f'Standard Error 1 {paidTriangle.standard_error(1)}')
    print(f'Standard Error 2 {paidTriangle.standard_error(2)}')
    # print(f'Standard Error 3 {paidTriangle.standard_error(3)}')
    print(f'Standard Error 4 {paidTriangle.standard_error(4)}')
    # print(f'Standard Error 5 {paidTriangle.standard_error(5)}')
    print(f'Standard Error 6 {paidTriangle.standard_error(6)}')
    #print(f'Standard Error 7 {paidTriangle.standard_error(7)}')
    