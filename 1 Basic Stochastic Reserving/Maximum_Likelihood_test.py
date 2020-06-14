import pandas as pd
import unittest
from Maximum_Likelihood import Stochastic_Reserving

class test_StochasticReserving(unittest.TestCase):
    def test_spring_19_5(self):
        claims = { 11: 5000, 12: 7500, 13: 8000, 14: 8500,
                   21: 6000, 22: 9000, 23: 8500,
                   31: 7000, 32:10000,
                   41: 8000 }

        clark = Stochastic_Reserving()               
        clark.α = 4.3335
        clark.θ = 21.897

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
        clark = Stochastic_Reserving()  

        on_level_premium = 12000

        # a) Clark's method key assumptions
        #  Incremental losses are independent and identically distributed.
        #  The scale parameter is constant.
        #  Variance estimates are based on the Rao-Cramer lower bound.

        # b        
        ELR = 71.15/100
        clark.θ = 7.293
        
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
        clark = Stochastic_Reserving()
        clark.θ = 7.804

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

    def test_fall_17_5(self):
        cumulative_reported = [8000, 9500, 10000,
                               4000, 6000, 
                               6000]
        clark = Stochastic_Reserving()  

        clark.ω = 1.1736
        clark.θ = 3.0544

        G1 = clark.loglogistic(clark.average_age(1))
        G2 = clark.loglogistic(clark.average_age(2))
        G3 = clark.loglogistic(clark.average_age(3))

        #a
        tail = 1 - G3
        self.assertAlmostEqual(0.064, tail, 3)

        #b         
        ULT = 10000 / G3 + 6000 / G2 + 6000 / G1
        Reported = 10000 + 6000 + 6000
        IBNR = ULT - Reported

        self.assertAlmostEqual(4150, IBNR, 0)

        #c        
        incremental_reported = [8000, 9500 - 8000, 10000 - 9500,
                                4000, 6000 - 4000]
        G = [G1, G2 - G1, G3 - G2,
             G1, G2 - G1]
        ULT = [10000 / G3, 10000 / G3, 10000 / G3,
                6000 / G2,  6000 / G2]
                             
        var_estimator = clark.estimate_variance(incremental_reported, ULT, G)
        self.assertAlmostEqual(647, var_estimator, 0)

        #d
        self.assertAlmostEqual(1639, (IBNR * var_estimator)**0.5, 0)

        #e
        actual = [6000 - 4000]
        ult = [6000 / G2]
        g =  [(G2 - G1)]

        var = clark.estimate_variance(actual, ult, g)
        normalized_residual = (var / var_estimator) ** 0.5
        self.assertAlmostEqual(0.69, normalized_residual, 2)
        
        #f) Assess whether the residuals support the use of the chosen model.
        #   There are two considerations:
        #       1. Are the residuals randomly scattered about zero? 
        #       Yes, the points are about the same amount above and below.
        #       2. Is the variability roughly constant? 
        #       No, it seems to be increasing. The residuals do not support the model.
        #       Or with the small number of points, a trend is hard to establish.
        
    def test_spring_17_5(self):
        #a) State one advantage and one disadvantage of using a parametric distribution function to model loss development.
        #   Advantages:
        #   • Provides smoothing
        #   • Small number of parameters to estimate
        #   • Does not require equal spacing of data points
        #   Disadvantage:
        #   • Development pattern must be increasing

        cumulative_reported = [4000, 6000, 8000,
                               5000, 7000, 
                               6000]
        clark = Stochastic_Reserving()  

        olp = 12000
        elr = 0.7520
        clark.θ = 8.858

        #b        
        G2 = clark.exponential(clark.average_age(2))
        G3 = clark.exponential(clark.average_age(3))
        expected_payment_in_2017 = olp*elr*(G3-G2)
        self.assertAlmostEqual(878, expected_payment_in_2017, 0)

        #c
        G1 = clark.exponential(clark.average_age(1))
        est_ult_loss_ay2016 = 6000 + olp * elr * (1 - G1)
        self.assertAlmostEqual(10584, est_ult_loss_ay2016, 0)
        
        σ2 = 813

        #d
        process_variance = (est_ult_loss_ay2016 - 6000) * σ2 
        self.assertAlmostEqual(1930,  process_variance **0.5, 0)

        #e
        self.assertAlmostEqual(2, len(cumulative_reported) - 4)
        
        #f) Indicate which of the LDF and Cape Cod methods is likely to have a smaller standard deviation of the total reserve. Justify your response.
        #   Cape Cod likely has a smaller standard deviation because of the additional information the exposure base provides.

    def test_fall_18_5(self):

        cumulative_reported = [6000, 5900, 6200,
                               4000, 5500, 
                               3000]
        clark = Stochastic_Reserving()  

        olp = [10000, 8500, 9000]

        clark.θ = 1.8968
        clark.ω = 1.0300

        #b        
        G3 = clark.loglogistic(clark.average_age(3) - 3 )
        G2 = clark.loglogistic(clark.average_age(2) - 3 )
        G1 = clark.loglogistic(clark.average_age( 9/12 ) )
        
        self.assertAlmostEqual(0.9391, G3,4)
        self.assertAlmostEqual(0.8938, G2,4)
        self.assertAlmostEqual(0.7089, G1,4)

        elr = (6200 + 5500 + 3000) / (pd.Series(olp) * pd.Series([G3,G2,G1])).sum()
        self.assertAlmostEqual(0.6291, elr, 4 )

        #c
        reserve = ( 
            pd.Series(olp) * elr * (1 - pd.Series([G3,G2,G1]))
        ).sum()
        self.assertAlmostEqual(2599.6, reserve, 1)

        #d
        g = clark.loglogistic(18) - clark.loglogistic(15) 
        est = 8500 * elr * g
        self.assertAlmostEqual(88.5, est, 1)

        #e) Describe a situation where the Weibull is likely to be more appropriate.
        # The Weibull distribution generally provides a smaller tail factor than the loglogistic.

        #f) Explain why Mack’s formulas are not appropriate in this situation.
        # Mack assumes that for each development age the expected value and variance are a constant multiple of past values with constant independent of accident year. 
        # 3This situation has different development ages by accident year and hence different factors are required.

    def test_spring_18_6(self):
        clark = Stochastic_Reserving()  
        olp = [10000, 8500, 12000]
        clark.θ = 6.689

        #a) example where assumption might not hold

        #b) explan why variance estimates are an approximation

        #c) caluclate MLE of ELR
        G3 = clark.exponential(clark.average_age(3) )
        G2 = clark.exponential(clark.average_age(2) )
        G1 = clark.exponential(clark.average_age(1) )

        reserve = 4369
        ibnr = olp[0]*(1-G3) + olp[1]*(1-G2) + olp[2]*(1-G1)
        self.assertAlmostEqual(0.7826, reserve/ibnr, 4)
     
        #d) expected payment in 2018 for AY2017
        ay17_payment = olp[2] * reserve/ibnr
        self.assertAlmostEqual(3193, ay17_payment * (G2-G1), 0)


if __name__ == '__main__':
    unittest.main()