import unittest
from LDF_StochasticReserving import Stochastic_Reserving as sr

class test_StochasticReserving(unittest.TestCase):
    def test_spring_19_5(self):
        claims = { 11: 5000, 12: 7500, 13: 8000, 14: 8500,
                   21: 6000, 22: 9000, 23: 8500,
                   31: 7000, 32:10000,
                   41: 8000 }
        
        clark = sr(4.3335, 21.897)

        #c
        AY2017 = clark.pareto(18)
        self.assertAlmostEqual(0.92572, AY2017, 5)
        
        ULT2017 = 10000 / AY2017
        self.assertAlmostEqual(10802, ULT2017, 0)

        #d
        G30 = clark.pareto(30)
        G6 = clark.pareto(6)

        self.assertAlmostEqual(622, 8000*(G30 - AY2017)/G6, 0 )

if __name__ == '__main__':
    unittest.main()