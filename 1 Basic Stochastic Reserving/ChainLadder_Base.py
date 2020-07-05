class Chain_Ladder():
    # 1 Introduction and Overview
    def __init__(self):
        self.AgeToAgeFactors , self.AgeToUltimateFactors = [], []     
        self.AgaToAgeFactorsTriangle = {}

    def load_triangle(self, triangle):
        self.Triangle = triangle
        self.Dimension = max(triangle.keys()) // 10

    def convert_2_triangle(self, rawTable, size):
        triangle = {}
        cursor = 0
        for ay in range(1, size + 1):
            for dy in range(1, size + 1):   
                triangle[ay*10 + dy] = rawTable[cursor]
                cursor += 1
        self.Triangle = triangle
        self.Dimension = max(triangle.keys()) // 10

    def calc_AgeToAgeFactors(self):         

        for dev in range(1, self.Dimension):
            currTotal, nextTotal = 0, 0           
            for acc in range(1, self.Dimension - dev + 1):
                currTotal += self.Triangle[ acc * 10 + dev    ]
                nextTotal += self.Triangle[ acc * 10 + dev + 1]

                self.AgaToAgeFactorsTriangle[acc*10 + dev] = self.Triangle[ acc * 10 + dev +1] / self.Triangle[ acc * 10 + dev] 

            self.AgeToAgeFactors.append(nextTotal / currTotal)            

        cumulativeFactor = 1
        for ageFactor in reversed(self.AgeToAgeFactors):            
            cumulativeFactor = round(cumulativeFactor * ageFactor, 8)
            self.AgeToUltimateFactors.insert(0, cumulativeFactor)     

        # print(f'AgeToAgeFactor {self.AgeToAgeFactors}')            
        # print(f'AgeToUltFactor {self.AgeToUltimateFactors}')