import unittest
from LDF_StochasticReserving import Stochastic_Reserving

class test_StochasticReserving(unittest.TestCase):
    def setUp(self):
        self.clark = Stochastic_Reserving()

    def test_spring_19_5(self):
        claims = { 11: 5000, 12: 7500, 13: 8000, 14: 8500,
                   21: 6000, 22: 9000, 23: 8500,
                   31: 7000, 32:10000,
                   41: 8000 }

        clark = self.clark                
        clark.Alpha = 4.3335
        clark.Theta = 21.897

        #c
        AY2017 = clark.pareto(18)
        self.assertAlmostEqual(0.92572, AY2017, 5)
        
        ULT2017 = 10000 / AY2017
        self.assertAlmostEqual(10802, ULT2017, 0)

        #d
        G30 = clark.pareto(30)
        G6 = clark.pareto(6)

        self.assertAlmostEqual(622, 8000*(G30 - AY2017)/G6, 0 )

    def test_fall_16_5(self):
        claims = { 11: 4000, 12: 7000, 13: 8000,
                   21: 5000, 22: 7000, 
                   31: 6000}
        clark = self.clark   

        on_level_premium = 12000

        # a) Clark's method key assumptions
        #  Incremental losses are independent and identically distributed.
        #  The scale parameter is constant.
        #  Variance estimates are based on the Rao-Cramer lower bound.

        # b        
        ELR = 71.15/100
        clark.Theta = 7.293
        
        reserve = on_level_premium * (1 - clark.exponential(6)) * ELR
        est_ult_losses = claims[31] + reserve
        self.assertAlmostEqual(9750, est_ult_losses, 0)

        # c
        est_variance = 273

        sd = (est_variance * reserve) ** 0.5
        self.assertAlmostEqual(1012, sd, 0) 

        # d
        est_sd = 852

        total_sd = clark.total_standard_deviation(variance=est_variance, amount=reserve, sd=est_sd)
        cv = total_sd / reserve
        self.assertAlmostEqual(0.35, cv, 2)

        # e
        expected_pmt = on_level_premium * ELR * (clark.exponential(18) - clark.exponential(6))
        self.assertAlmostEqual(3027, expected_pmt, 0)

        # f
        est_sd = 512
        total_sd = clark.total_standard_deviation(variance=est_variance, amount=expected_pmt, sd=est_sd)
        self.assertAlmostEqual(1043, total_sd, 0) 

        # g 
        actual_pmt = 3800        
        self.assertLessEqual(actual_pmt - expected_pmt, total_sd)
    
    def test_spring_16_3(self):
        #(a) (1.5 points) State two advantages and one disadvantage of using a parametric
        #    cumulative distribution function to model loss development.

        # Three advantages are 
        #   (1) it provides smoothing, 
        #   (2) there are a small number of parameters to estimate, and 
        #   (3) it does not require equal spacing of data points. 
        # Disadvantage is that 
        #   only increasing development patterns can be modeled.

        # b
        clark = self.clark 
        clark.Theta = 7.804

        ULT_2013 = 7250 / clark.exponential(clark.average_age(2016 - 2013))
        self.assertAlmostEqual(7409, ULT_2013, 0)

        # c
        X = ULT_2013 * clark.exponential(clark.average_age(1))
        self.assertAlmostEqual(3974, X, 0)

        Y = ULT_2013 * clark.exponential(clark.average_age(2))
        self.assertAlmostEqual(6671, Y, 0)
        
        # d) identify the number of degress fo freedom
        σ2 = 47
        # e
        reserve = ULT_2013 - 7250
        self.assertAlmostEqual(86, (reserve * σ2) ** 0.5, 0) 


if __name__ == '__main__':
    unittest.main()