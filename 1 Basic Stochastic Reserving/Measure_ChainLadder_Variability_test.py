import unittest
from Measure_ChainLadder_Variability import Chain_Ladder

class test_ChainLadder(unittest.TestCase):
    def test_spring_19_4(self):
        paidClaims = { 11: 8000, 12:15000, 13:21000, 14:23100,
                       21:10000, 22:15000, 23:18000,
                       31:12000, 32:15000,
                       41:14000 }
        
        paidTriangle = Chain_Ladder(paidClaims)
        
        #a
        self.assertAlmostEqual(0.46620, paidTriangle.natural_starting_values(1),5)
        self.assertAlmostEqual(0.23310, paidTriangle.natural_starting_values(2),5)
        self.assertAlmostEqual(0.20979, paidTriangle.natural_starting_values(3),5)
        self.assertAlmostEqual(0.09091, paidTriangle.natural_starting_values(4),5)
        #b
        self.assertAlmostEqual(21024, paidTriangle.starting_values(1),0)
        self.assertAlmostEqual(20453, paidTriangle.starting_values(2),0)
        self.assertAlmostEqual(23166, paidTriangle.starting_values(3),0)
        self.assertAlmostEqual(30030, paidTriangle.starting_values(4),0)

        #f
        self.assertAlmostEqual(937.5, paidTriangle.proportionality_constants(1),1)
        self.assertAlmostEqual(300, paidTriangle.proportionality_constants(2),0)
        self.assertAlmostEqual(96, paidTriangle.proportionality_constants(3),0)
 
    def setUp(self):    
        self.paidClaims = { 11: 9659, 12:15468, 13:17887, 14:18236, 15:18910, 16:19262, 17:19644,
                       21:10731, 22:17668, 23:22333, 24:24701, 25:24827, 26:25331,
                       31:11715, 32:11037, 33:14503, 34:14707, 35:16414,                                        
                       41:12450, 42:15686, 43:19069, 44:23888,
                       51:13574, 52:15924, 53:17706, 
                       61:14717, 62:20165,
                       71:16100 }

        self.paidTriangle = Chain_Ladder(self.paidClaims)

    def test_fall_16_4(self):
        # a
        self.assertAlmostEqual(0.0305, self.paidTriangle.proportionality_constants(5), 4)       

        # b     
        self.assertAlmostEqual(0, self.paidTriangle.standard_error(1),0)
        self.assertAlmostEqual(1, self.paidTriangle.standard_error(2),0)    
        self.assertAlmostEqual(27, self.paidTriangle.standard_error(3),0)   
        self.assertAlmostEqual(1448, self.paidTriangle.standard_error(4),0)
        self.assertAlmostEqual(2715, self.paidTriangle.standard_error(5),0)
        self.assertAlmostEqual(3782, self.paidTriangle.standard_error(6),0)                
        self.assertAlmostEqual(6915, self.paidTriangle.standard_error(7),0)
    
        # c) Normal approximation 
        # d) Lognormal 
        # e) why weighted regression
        # f) Venter

if __name__ == '__main__':
    unittest.main()