import unittest
from Measure_ChainLadder_Variability import Chain_Ladder
from Venter_Factors import Venter_Factors

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
        self.assertAlmostEqual(937.5, paidTriangle.a_proportionality_constant(1),1)
        self.assertAlmostEqual(300, paidTriangle.a_proportionality_constant(2),0)
        self.assertAlmostEqual(96, paidTriangle.a_proportionality_constant(3),0)

    def test_fall_16_4(self):
        paidClaims = { 11: 9659, 12:15468, 13:17887, 14:18236, 15:18910, 16:19262, 17:19644,
                       21:10731, 22:17668, 23:22333, 24:24701, 25:24827, 26:25331,
                       31:11715, 32:11037, 33:14503, 34:14707, 35:16414,                                        
                       41:12450, 42:15686, 43:19069, 44:23888,
                       51:13574, 52:15924, 53:17706, 
                       61:14717, 62:20165,
                       71:16100 }

        paidTriangle = Chain_Ladder(paidClaims)

        # a
        self.assertAlmostEqual(0.0305, paidTriangle.a_proportionality_constant(5), 4)       

        # b     
        self.assertAlmostEqual(0,    paidTriangle.standard_error(1),0)
        self.assertAlmostEqual(1,    paidTriangle.standard_error(2),0)    
        self.assertAlmostEqual(27,   paidTriangle.standard_error(3),0)   
        self.assertAlmostEqual(1448, paidTriangle.standard_error(4),0)
        self.assertAlmostEqual(2715, paidTriangle.standard_error(5),0)
        self.assertAlmostEqual(3782, paidTriangle.standard_error(6),0)                
        self.assertAlmostEqual(6915, paidTriangle.standard_error(7),0)
    
        # c) Normal approximation 
        # d) Lognormal 
        # e) why weighted regression
        # f) Venter

    def test_spring_16_4(self):
        paidClaims = { 11: 9791, 12:12431, 13:13033, 14:14212, 15:14486, 16:14867, 17:15155,
                       21:11314, 22:19266, 23:23518, 24:27910, 25:28117, 26:28697,
                       31:12654, 32:14924, 33:18489, 34:22433, 35:24281,
                       41:13305, 42:14234, 43:15293, 44:15900,
                       51:14693, 52:26298, 53:37108,
                       61:16037, 62:18544,
                       71:17360}

        paidTriangle = Chain_Ladder(paidClaims)
        #a
        self.assertAlmostEqual(37.514, paidTriangle.a_proportionality_constant(4), 3)

        #b
        self.assertAlmostEqual(111, paidTriangle.standard_error(3), 0)

        #c
        # Mack's three assumptions

        #d
        n = 21
        p = 6

        #e
        SSE = 126347521
        venter = Venter_Factors()
        self.assertAlmostEqual(561545, venter.adjusted_SSE(SSE, n, p), 0)
        self.assertAlmostEqual(223735552, venter.adjusted_SSE_AIC(SSE, n, p), 0)
        self.assertAlmostEqual(301539122, venter.adjusted_SSE_BIC(SSE, n, p), 0)

        #f) Venter proposes investigating models other than the standard chain ladder 
        #   (where each value is multiplied by a factor that depends only on the development year).
        #   Describe one such alternative model, using words, not formulas.


if __name__ == '__main__':
    unittest.main()