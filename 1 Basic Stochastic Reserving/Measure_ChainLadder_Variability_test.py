import pandas as pd
import unittest
from Measure_ChainLadder_Variability import Chain_Ladder
from Venter_Factors import Venter_Factors, ChainLadderHelper

class test_ChainLadder(unittest.TestCase):
    def test_spring_19_4(self):
        paidClaims = { 11: 8000, 12:15000, 13:21000, 14:23100,
                       21:10000, 22:15000, 23:18000,
                       31:12000, 32:15000,
                       41:14000 }
        
        paidTriangle = Chain_Ladder(paidClaims)
        paidTriangle.calc_AgeToAgeFactors()       

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
        paidTriangle.calc_AgeToAgeFactors()  

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
        paidTriangle.calc_AgeToAgeFactors()               
        
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

        # f) Venter proposes investigating models other than the standard chain ladder 
        #   (where each value is multiplied by a factor that depends only on the development year).
        #   Describe one such alternative model, using words, not formulas.

    def test_fall_17_4(self):        
        rawPaid = [9146,12176,17670,18546,18128,18517,18888,
                  10834,15902,20884,23304,22887,23371,23839,
                  11946,15697,20478,22854,20718,21159,21583,
                  12414,19333,38991,42905,40935,41806,42644,
                  14284,20888,25210,27675,26405,26967,27507,
                  15648,17240,25293,27767,26492,27056,27598,
                  17221,23473,34438,37806,36070,36838,37576]

        helper = ChainLadderHelper()
        paidClaims = helper.convert_2_triangle(rawPaid, 7)
        paidTriangle = Chain_Ladder(paidClaims)
        paidTriangle.calc_AgeToAgeFactors()  

        #a
        self.assertAlmostEqual(1761, paidTriangle.standard_error(4), 0)
        
        #b
        self.assertAlmostEqual(0.011, paidTriangle.square_of_SE_of_overall(2), 3)

        #c) explain why the estimators are dependent?

        #d)
        ay, dy = 4, 3
        f = paidTriangle.AgeToAgeFactors[(dy-1) -1]
        actual_ = paidTriangle.Triangle[ay*10 + dy-1]

        expected = actual_ * f        
        actual = paidTriangle.Triangle[ay*10 + dy]

        self.assertAlmostEqual(76.43, (actual - expected) / (actual_ ** 0.5),2 )

        #e
        n, p = 6*(6+1)/2, 6
        
        #f 
        SSE = 184086659
        venter = Venter_Factors()
        self.assertAlmostEqual(818163, venter.adjusted_SSE(SSE, n, p), 0)
        self.assertAlmostEqual(325979727, venter.adjusted_SSE_AIC(SSE, n, p), 0)
        self.assertAlmostEqual(439338494, venter.adjusted_SSE_BIC(SSE, n, p), 0)

    def test_spring_17_4(self):   
        rawPaid = [ 20587, 29243, 33208, 35957, 36328, 37131, 37871,
                    21399, 23109, 30971, 36752, 38103, 38877, 39652,
                    22259, 31780, 42282, 45157, 48759, 49792, 50784,
                    23191, 33060, 46113, 48668, 50866, 51944, 52979,
                    25065, 29536, 38140, 41630, 43510, 44432, 45317,
                    25024, 40688, 52885, 57724, 60332, 61610, 62838,
                    25387, 34597, 44968, 49083, 51300, 52387, 53431]                    
        helper = ChainLadderHelper()
        paidClaims = helper.convert_2_triangle(rawPaid, 7)
        paidTriangle = Chain_Ladder(paidClaims)
        paidTriangle.calc_AgeToAgeFactors()  

        #a
        self.assertAlmostEqual(50.162, paidTriangle.a_proportionality_constant(4),2)

        #b
        self.assertAlmostEqual(3157, paidTriangle.standard_error(5),0)

        #c d e f) Indicate whether or not this observation provides support for the underlying assumptions of Mack’s model. Justify your response.
        #c) No, Mack assumes that expected development is a multiple of the previous value. It does not assume that the factor is greater than one.
        #d) No, Mack makes no assumption about the observed ratios, only about their expected values and variances.
        #e) The results cannot confirm that the assumptions hold because there may be other tests that would reveal ways in which the assumptions do not hold.
        #f) The results cannot confirm that the assumptions do not hold. 
        #   When conducting multiple tests in an environment where the assumptions do hold, 
        #   it is possible that due to chance a few of the tests may yield an adverse result.
        
    def test_fall_18_4(self):
        #a,b) Mack's three assumptions
        
        age_to_age_factors = {11: 1.3313, 12: 1.4512, 13: 1.0496, 14: 0.9775, 15: 1.0215, 16:1.0200,
                              21: 1.4678, 22: 1.3133, 23: 1.1159, 24: 0.9821, 25: 1.0211,
                              31: 1.3140, 32: 1.3046, 33: 1.1160, 34: 0.9065,
                              41: 1.5574, 42: 2.0168, 43: 1.1004,
                              51: 1.4623, 52: 1.2069,
                              61: 1.1017}
        
        target = Chain_Ladder(age_to_age_factors)
        target.spearman_rank()        

        self.assertAlmostEqual(-.24, target.T)

        self.assertAlmostEqual(-0.76, target.T / target.Var_T**0.5, 2)

    def test_CAS7_spring_18_7(self):
        # variance assumptions
        assert 1 == 1

    def test_CAS7_spring_18_8(self):
        age_to_age_factors = {11: 1.7, 12: 1.35, 13: 1.10, 14: 1.05,
                              21: 2.5, 22: 1.55, 23: 1.08,
                              31: 2.0, 32: 1.40,
                              41: 1.8}
                              
        target = Chain_Ladder(age_to_age_factors)
        target.spearman_rank()    

        self.assertAlmostEqual(0.3333, target.T, 4)
        
        self.assertAlmostEqual(0.3333, target.Var_T,4)

    def test_spring_18_5(self):
        paidClaims = { 11: 9146, 12:12176, 13:17670, 14:18546, 15:18128, 16:18517, 17:18888,
                       21:10834, 22:15902, 23:20884, 24:23304, 25:22887, 26:23371, 
                       31:11946, 32:15697, 33:20478, 34:22854, 35:20718,
                       41:12414, 42:19333, 43:38991, 44:42905,
                       51:14284, 52:20888, 53:25210, 
                       61:15648, 62:17240,
                       71:17221}

        paidTriangle = Chain_Ladder(paidClaims)
        paidTriangle.calc_AgeToAgeFactors()       

        #a
        self.assertAlmostEqual(40.0504, paidTriangle.a_proportionality_constant(4),4)

        self.assertAlmostEqual(1761, paidTriangle.standard_error(4), 0)
        self.assertAlmostEqual(1514, paidTriangle.standard_error(5), 0)

        print(sum(paidTriangle.AgeToAgeFactors) / 6)

if __name__ == '__main__':
    unittest.main()