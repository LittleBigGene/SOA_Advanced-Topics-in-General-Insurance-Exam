import pandas as pd
import unittest
from ChainLadder_Measure_Variability import Chain_Ladder_Mack
from ChainLadder_Assumptions import Chain_Ladder_Venter

class test_ChainLadder(unittest.TestCase):
    def test_19_spring_4(self):
        paidClaims = { 11: 8000, 12:15000, 13:21000, 14:23100,
                       21:10000, 22:15000, 23:18000,
                       31:12000, 32:15000,
                       41:14000 }
        
        paidTriangle = Chain_Ladder_Venter()
        paidTriangle.load_triangle(paidClaims)
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

    def test_16_fall_4(self):
        paidClaims = { 11: 9659, 12:15468, 13:17887, 14:18236, 15:18910, 16:19262, 17:19644,
                       21:10731, 22:17668, 23:22333, 24:24701, 25:24827, 26:25331,
                       31:11715, 32:11037, 33:14503, 34:14707, 35:16414,                                        
                       41:12450, 42:15686, 43:19069, 44:23888,
                       51:13574, 52:15924, 53:17706, 
                       61:14717, 62:20165,
                       71:16100 }

        paidTriangle = Chain_Ladder_Mack()
        paidTriangle.load_triangle(paidClaims)
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
    
        # c) why normal approximation may not be reasonable ?
        # The normal approximation is symmetric and may allow for more negative movement than is reasonable. 
        # In this case, it can be noted either that the standard deviation is close to half the reserve or that there is a significant probability of negative development.
        
        # d) Recommend and justify an approach that may be superior 
        # A lognormal distribution may be a superior model. 
        # It is right skewed and thus provides a lower probability of downward movement. 
        # The lognormal distribution assigns probability only to positive values.

        # e) why weighted regression ?
        # An unweighted regression assumes a constant variance. 
        # In the Mack model the variance is proportional to the developed value and thus a weighted regression is needed.
        
        # f) Describe two other approaches that Venter proposes for comparing or evaluating different models.
        #  Test the significance of the estimated factors.
        #  Examine the residuals to determine if the model is linear in the specified manner.
        #  Examine the residuals over time to determine if there are any patterns.

    def test_16_spring_4(self):
        paidClaims = { 11: 9791, 12:12431, 13:13033, 14:14212, 15:14486, 16:14867, 17:15155,
                       21:11314, 22:19266, 23:23518, 24:27910, 25:28117, 26:28697,
                       31:12654, 32:14924, 33:18489, 34:22433, 35:24281,
                       41:13305, 42:14234, 43:15293, 44:15900,
                       51:14693, 52:26298, 53:37108,
                       61:16037, 62:18544,
                       71:17360}

        paidTriangle = Chain_Ladder_Venter()
        paidTriangle.load_triangle(paidClaims)
        paidTriangle.calc_AgeToAgeFactors()               
        
        # a
        self.assertAlmostEqual(37.514, paidTriangle.a_proportionality_constant(4), 3)

        # b
        self.assertAlmostEqual(111, paidTriangle.standard_error(3), 0)

        # c) state Mack's three assumptions and 
        # explain why that assumption does or does not prevent the value form decreasing from one development year to the next
        # (1) The expected value is the previous value times a constant that depends only on the development year. 
        #     This assumption does not prevent values from decreasing because it only relates to the expected, not the actual value. 
        #     Alternatively, the constant can be less than one, which implies an expected decrease.
        # (2) The variance is the previous value times a factor that depends only on the development year. 
        #     This assumption does not prevent values from decreasing because with variability in outcomes, that could extend to decreasing values.
        # (3) Values from different accident years are independent. 
        #     This assumption makes no statement about the magnitude of the values and so allows for decreasing values.

        #d
        n = 21
        p = 6

        #e
        SSE = 126347521
        self.assertAlmostEqual(561545,    paidTriangle.adjusted_SSE(SSE, n, p), 0)
        self.assertAlmostEqual(223735552, paidTriangle.adjusted_SSE_AIC(SSE, n, p), 0)
        self.assertAlmostEqual(301539122, paidTriangle.adjusted_SSE_BIC(SSE, n, p), 0)

        # f) Venter proposes investigating models other than the standard chain ladder 
        #   (where each value is multiplied by a factor that depends only on the development year).
        #   Describe one such alternative model, using words, not formulas.

        # (1) Add a constant after multiplying by the chain ladder development factor.
        # (2) Multiplication of factors representing the accident year and development year. 
        #     This can also be described as a parameterized version of the Bornhuetter Ferguson method.
        # (3) As in number (2) but add a factor for calendar year.

    def test_17_fall_4(self):        
        rawPaid = [9146,12176,17670,18546,18128,18517,18888,
                  10834,15902,20884,23304,22887,23371,23839,
                  11946,15697,20478,22854,20718,21159,21583,
                  12414,19333,38991,42905,40935,41806,42644,
                  14284,20888,25210,27675,26405,26967,27507,
                  15648,17240,25293,27767,26492,27056,27598,
                  17221,23473,34438,37806,36070,36838,37576]

        paidTriangle = Chain_Ladder_Venter()
        paidTriangle.convert_2_triangle(rawPaid, 7)        
        paidTriangle.calc_AgeToAgeFactors()  

        #a
        self.assertAlmostEqual(1761, paidTriangle.standard_error(4), 0)
        
        #b
        self.assertAlmostEqual(0.011, paidTriangle.square_of_SE_of_overall(2), 3)

        #c) explain why the estimators are dependent?
        # Each reserve estimate depends on the sequence of development factors. Some factors are used in more than one reserve estimate. 
        # For example, f6 is used for both AY 4 and AY 5 reserve estimates. Any error in this factor will appear in both calculations.

        #d)
        ay, dy = 4, 3
        f = paidTriangle.AgeToAgeFactors[(dy-1) -1]
        actual_ = paidTriangle.Triangle[ay*10 + dy-1] 
        actual = paidTriangle.Triangle[ay*10 + dy]

        self.assertAlmostEqual(76.43, (actual - actual_ * f) / (actual_ ** 0.5),2 )

        #e
        n, p = 6*(6+1)/2, 6
        
        #f 
        SSE = 184086659        
        self.assertAlmostEqual(818163,    paidTriangle.adjusted_SSE(SSE, n, p), 0)
        self.assertAlmostEqual(325979727, paidTriangle.adjusted_SSE_AIC(SSE, n, p), 0)
        self.assertAlmostEqual(439338494, paidTriangle.adjusted_SSE_BIC(SSE, n, p), 0)

    def test_17_spring_4(self):   
        rawPaid = [ 20587, 29243, 33208, 35957, 36328, 37131, 37871,
                    21399, 23109, 30971, 36752, 38103, 38877, 39652,
                    22259, 31780, 42282, 45157, 48759, 49792, 50784,
                    23191, 33060, 46113, 48668, 50866, 51944, 52979,
                    25065, 29536, 38140, 41630, 43510, 44432, 45317,
                    25024, 40688, 52885, 57724, 60332, 61610, 62838,
                    25387, 34597, 44968, 49083, 51300, 52387, 53431]                    
        paidTriangle = Chain_Ladder_Mack()
        paidTriangle.convert_2_triangle(rawPaid, 7)        
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
        
    def test_18_fall_4(self):
        #a,b) Mack's three assumptions
        
        age_to_age_factors = {11: 1.3313, 12: 1.4512, 13: 1.0496, 14: 0.9775, 15: 1.0215, 16:1.0200,
                              21: 1.4678, 22: 1.3133, 23: 1.1159, 24: 0.9821, 25: 1.0211,
                              31: 1.3140, 32: 1.3046, 33: 1.1160, 34: 0.9065,
                              41: 1.5574, 42: 2.0168, 43: 1.1004,
                              51: 1.4623, 52: 1.2069,
                              61: 1.1017}
        
        target = Chain_Ladder_Mack()
        target.load_triangle(age_to_age_factors)        
        target.spearman_rank()        

        # c
        self.assertAlmostEqual(-.24, target.T)

        # d
        self.assertAlmostEqual(-0.76, target.T / target.Var_T**0.5, 2)
        # a value of Tk close to 0 indicates that the development factors between development years are not correlated.
        # any other value indicates that that factors are (positively or negatively) correlated

        # e) describe two alternative models suggested by Venter
        # • Linear with constant
        # • Factor times parameter
        # • Factor times parameter plus a calendar year effect
        # • Bornhuetter Ferguson
        # • Parameterized Bornhuetter Ferguson
        # • Cape Cod
        # • Additive

    def test_18_spring_5(self):
        paidClaims = { 11: 9146, 12:12176, 13:17670, 14:18546, 15:18128, 16:18517, 17:18888,
                       21:10834, 22:15902, 23:20884, 24:23304, 25:22887, 26:23371, 
                       31:11946, 32:15697, 33:20478, 34:22854, 35:20718,
                       41:12414, 42:19333, 43:38991, 44:42905,
                       51:14284, 52:20888, 53:25210, 
                       61:15648, 62:17240,
                       71:17221}

        paidTriangle = Chain_Ladder_Mack()
        paidTriangle.load_triangle(paidClaims)
        paidTriangle.calc_AgeToAgeFactors()       

        #a
        self.assertAlmostEqual(40.0504, paidTriangle.a_proportionality_constant(4),4)

        self.assertAlmostEqual(1761, paidTriangle.standard_error(4), 0)
        self.assertAlmostEqual(1514, paidTriangle.standard_error(5), 0)

        #b) calculate SE of the reserve estimator for AY 4 & 5 combined

        #c)
        r = 0.574
        self.assertAlmostEqual(1.214**2, r**2/(1-r**2) * (7-2-2), 3) 

        # d) Determine whether this correlation is significant.
        # The test statistic has a t distribution with three degrees of freedom. 
        # At any reasonable significance level the null hypothesis of no correlation is not rejected. 
        # There is no evidence of significant correlation.

        # e)                
        paidTriangle.calendar_year_effect_statistic()
        assert 'SSSSS*' == paidTriangle.CYE_statistic_triangle[6+1]

        # f)
        # The test statistic is (1 – 4.875)/1.196 = –3.24 standard deviations below the mean. 
        # It is significant at any reasonable significance level and thus there is a significant calendar year effect. 
        # The chain ladder method may not be appropriate.


    def test_cas7_2015_4(self):
        age_to_age_factors = {11: 7.0, 12: 2.55, 13: 1.6, 14: 1.3, 15: 1.2, 16: 1.05,
                              21: 6.0, 22: 2.60, 23: 1.4, 24: 1.5, 25: 1.1,
                              31: 5.0, 32: 2.50, 33: 1.8, 34: 1.2,
                              41: 5.5, 42: 2.80, 43: 1.5,                            
                              51: 8.0, 52: 2.40,
                              61: 7.0}

        target = Chain_Ladder_Mack()
        target.Dimension = 6+1
        target.AgaToAgeFactorsTriangle = age_to_age_factors
        target.calendar_year_effect_statistic()
        assert 'LSSSS*' == target.CYE_statistic_triangle[6+1]

    def test_cas7_2016_5(self):
        age_to_age_factors = {11: 1.324, 12: 1.127, 13: 1.065, 14: 1.025, 15: 1.012,
                              21: 1.313, 22: 1.127, 23: 1.058, 24: 1.027,
                              31: 1.344, 32: 1.135, 33: 1.070,
                              41: 1.340, 42: 1.134, 
                              51: 1.344}

        target = Chain_Ladder_Mack()
        target.Dimension = 5+1
        target.AgaToAgeFactorsTriangle = age_to_age_factors
        target.calendar_year_effect_statistic()
        assert 'LLLL*' == target.CYE_statistic_triangle[5+1]

    def test_cas7_2018_7(self):
        # variance assumptions
        pass

    def test_cas7_2018_8(self):
        age_to_age_factors = {11: 1.7, 12: 1.35, 13: 1.10, 14: 1.05,
                              21: 2.5, 22: 1.55, 23: 1.08,
                              31: 2.0, 32: 1.40,
                              41: 1.8}
                              
        target = Chain_Ladder_Mack()
        target.load_triangle(age_to_age_factors)
        target.spearman_rank()    

        self.assertAlmostEqual(0.3333, target.T, 4)
        
        self.assertAlmostEqual(0.3333, target.Var_T,4)

if __name__ == '__main__':
    unittest.main()