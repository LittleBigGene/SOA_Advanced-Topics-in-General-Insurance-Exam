import unittest
import numpy as np
from ReinsurancePricing import Reinsurance_Pricing

class test_ReinsurancePricing(unittest.TestCase):

    def test_spring_19_2(self):        
        ExpectedLoss = Reinsurance_Pricing()
        ExpectedLoss.ILF = {0:0, 1:1, 2:1.16 , 3:1.28 , 4:1.38 }
        
        #a
        a1 = ExpectedLoss.occurrence_exposure_rating(0, 1, 1)
        self.assertAlmostEqual(a1, 0)

        a2 = ExpectedLoss.occurrence_exposure_rating(0, 2, 1)
        self.assertAlmostEqual( a2, 0.138, 3)

        a3 = ExpectedLoss.occurrence_exposure_rating(0, 3, 1)
        self.assertAlmostEqual( a3, 0.219, 3)

        a4 = ExpectedLoss.occurrence_exposure_rating(1, 2, 1)
        self.assertAlmostEqual( a4, 0.429, 3)
        
        a5 = ExpectedLoss.occurrence_exposure_rating(1, 3, 1)
        self.assertAlmostEqual(a5, 0.579, 3)

        a = .6*(3 * a1 + 4 * a2 + 5 * a3 + 8 * a4 + 9 * a5)
        self.assertAlmostEqual(a, 6.17, 2)
     
        #b
        averageLossCost = 0.1 * 0.04 + 0.75 * 0.19 + 0.15 * 0.44
        self.assertAlmostEqual(averageLossCost, .2125)

        loadedLossCost =  0.1 * ExpectedLoss.swing_plan(0.375,.125,100/80,0.04) + 0.75 * ExpectedLoss.swing_plan(0.375,.125,100/80,0.19) + 0.15 * ExpectedLoss.swing_plan(0.375,.125,100/80,0.44)
        self.assertAlmostEqual( loadedLossCost, .2469, 4)
    
    def test_spring_19_8(self):
        annualPrem = 50
        margin = .1 * annualPrem
        OccurrenceLimit = 200         
        
        specialist = Reinsurance_Pricing()

        #a_i no losses
        loss = 0
        additionalPrem = specialist.additional_prem(0.6, loss, margin, annualPrem)
        profitCommission = specialist.profit_commission(0.95, loss, margin, annualPrem)
        a1Profit = annualPrem - loss - profitCommission + additionalPrem
        self.assertAlmostEqual(7.25, a1Profit)

        #a_ii one or more loss
        loss = OccurrenceLimit
        additionalPrem = specialist.additional_prem(0.6, loss, margin, annualPrem)
        profitCommission = specialist.profit_commission(0.95, loss, margin, annualPrem)
        a2Loss = annualPrem - loss - profitCommission + additionalPrem
        self.assertAlmostEqual(-57, a2Loss)

        #b the rate on line for an equivalent traditional risk cover        
        self.assertAlmostEqual(11.3/100, a1Profit/(a1Profit-a2Loss), 3 )

        #c 
        additionalPrem = 108.917
        a2Loss = annualPrem - loss - profitCommission + additionalPrem
        self.assertAlmostEqual(.15, a1Profit/(a1Profit-a2Loss), 3 )

    def test_fall_16_1(self):
        treaty = Reinsurance_Pricing()
                       
        a = treaty.loss_cost_rate(
            standard_premium_x=0.6, expected_loss_ratio_x=0.6, 
            standard_premium_y=0.4, expected_loss_ratio_y=0.7, 
            allocation_x=0.5, allocation_y=0.5,
            layer_x=(0.05-0.0125), layer_y=(0.1-0.025))
        
        self.assertAlmostEqual(0.036, a )

        # For policy limits, because workers compensation insurance does not have policy limits, no adjustment is needed. 
        # For discounting, loss data should be requested on a full undiscounted basis.
        
        # Historical premiums should be adjusted for rate changes and for exposure (payroll) inflation. 
        # Historical losses should be adjusted for trend and for development.
    
    def test_fall_16_8(self):
        treaty = Reinsurance_Pricing()

        def expected (vector):
            return sum(vector) / len(vector) / 100

        # a) Option 1
        lr = [30, 80]
        comm_min=[20,70]
        comm_max=[30,50]
        # loss ratio 30~50, comm 30
        # loss ratio 50~70, comm 25
        # loss ratio 70~80, comm 20              
        tech1 = treaty.technical_ratio(lr, comm_min, comm_max, sliding = 0.5)    
        self.assertAlmostEqual(0.81, expected(tech1), 2)
       
        # b) Option 2        
        # # loss ratio 30~60, comm 27.5
        # # loss ratio 60~70, comm 27.5
        # # loss ratio 70~80, comm 27.5   
        tech = treaty.technical_ratio([30,60],[27.5,70],[27.5,60])                         
        self.assertAlmostEqual(.725, expected(tech) )

        tech = treaty.technical_ratio([60,70],[27.5,70],[27.5,60], reassume = 0.5)
        self.assertAlmostEqual(.90, expected(tech) )

        tech = treaty.technical_ratio([70,80],[27.5,70],[27.5,60])
        self.assertAlmostEqual(1.025, expected(tech) )
        
        tech2 = treaty.technical_ratio(lr,[27.5,70],[27.5,60], reassume = 0.5)        
        self.assertAlmostEqual(0.82, expected(tech2), 2)

        # c
        #print(f'Option 1 variance = {np.var(tech1)}; Option 2 variance {np.var(tech2)}')
        self.assertLess(np.var(tech1), np.var(tech2) )

        # d) Explain how the loss ratio distribution on the surplus share treaty would 
        #   qualitatively differ from the loss ratio distribution on the quota share treaty.
        
        # A surplus share treaty has a larger share of the larger risks and none of the smaller risks. 
        # This results in a loss ratio distribution with a larger variance than a quota share treaty.

    def test_spring_16_1(self):
        # surplus share with retained line of 500
        insured_values = np.clip(np.array([100,200,500,1000]), 0, 500)

        betaRe = Reinsurance_Pricing()
        
        expo = 0
        for iv in insured_values:
            expo += betaRe.risk_exposure_rating(limit = 400, retention = 100, insured_value = iv)

        # a
        self.assertAlmostEqual(1020833, expo * 0.6 * 1000000, 0)

        # b) explain free cover

        # c) The surplus share reinsurance       will inure to the benefit of the property catastrophe cover.
        # d) The property per risk excess treaty will inure to the benefit of the property catastrophe cover.

    def test_spring_16_8(self):
        #a
        # Sliding scale commission
        # Profit commission
        # Loss corridor 

        #b
        # Empirical distribution
        #   o Does not take into account all possible outcomes
        #   o If volume or mix changes, will not be able to reflect future volatility
        #   o If loss developed used Bornhuetter Ferguson or Cape Cod, 
        #       then historical periods may provide an artificially smooth sequence of loss ratios, 
        #       which will understate future volatility

        # Single distribution model
        #   o There is no provision for a positive probability of zero claims
        #   o Difficult to reflect changes in per-occurrence limits

        # Recursive formula
        #   o Calculation is difficult when the expected frequency is high o Only one severity distribution can be used

        #c
        # Carryforward provisions
        #   Include the carryforward from past years and estimate its effect on the current year only. 
        #   This approach ignores the potential effect on later years.

        #   Look at the long run of the contract and extend the modification, incorporating a reduction in the variance. 
        #   For this method there is no obvious way to reduce the variance and it is possible that the contract will not renew.

        pass

    def test_fall_17_1(self):
        #a
        # The aggregate excess factor is the average amount of loss in excess of the aggregate limit,       divided by the expected loss. 
        # The Table M charge factor   is the average amount of loss in excess of r times the expected loss, divided by the expected loss. 
        # Hence, they measure the same thing, with a slightly different definition of the point above which the excess is calculated.

        ExpectedLoss = Reinsurance_Pricing()
        ExpectedLoss.ILF = { 500:1.00, 
                            1000:1.50, 
                            1500:1.80, 
                            2000:2.00, 
                            2500:2.10,
                            3000:2.15}

        #b
        b1 = ExpectedLoss.occurrence_exposure_rating(1000, 1000, 500, 0.1)
        b2 = ExpectedLoss.occurrence_exposure_rating(1000, 2000, 500, 0.1)

        self.assertAlmostEqual(460 / 1200, b1)
        self.assertAlmostEqual(365 / 785 , b2)

        total_expeced_loss = .6 * (460 + 365) 
        #print(total_expeced_loss)

        #c) clash over
        #d) Describe two ways that a loss on this treaty could occur. 
        #   Any two of the following were sufficient for full credit.
        #   • Multiple policies involved in a single occurrence
        #   • Extra-contractual obligations
        #   • Rulings awarding damages in excess of policy limits
        #   • ALAE being included with losses and the total exceeding policy limits

    def test_fall_17_8(self):
        cat = Reinsurance_Pricing()
        cat.mean, cat.variance = 1, 2 # geometric distribution

        loss_size_probability = [0, .4, .3, .2, .1]
        aggregate_losses_prob = [.5,.1,.095,.084,.0661,.0403,.0311,.0231,.0166,.0119]

        #a
        p = cat.aggregate_loss_probability(loss_size_probability, aggregate_losses_prob, 4)
        self.assertAlmostEqual(.008765, p/10, 4) # SOA Solution 0.0087

        #b
        m = cat.moment_of_loss(loss_size_probability)
        
        aggregate_mean = cat.mean * m[0]
        aggregate_var  = cat.variance * m[1]
        cv = aggregate_var**0.5 /aggregate_mean

        self.assertAlmostEqual(1.581, cv, 3)

    def test_spring_17_8(self):
        cat = Reinsurance_Pricing()
        cat.mean, cat.variance = 2, 2 # poisson distribution
        loss_size_probability = [0, .4, .3, .2, .1]
        aggregate_losses_prob = [0.1353, 0.1083, 0.1245, 0.1306, 0.1230, 0.0982, 0.0804, 0.0621, 0.0453, 0.0318]
        
         #a
        p = cat.aggregate_loss_probability(loss_size_probability, aggregate_losses_prob, 10)
        self.assertAlmostEqual(.0219, p, 4)

        #b
        m = cat.moment_of_loss(loss_size_probability)
        
        aggregate_mean = cat.mean * m[0]
        aggregate_var  = cat.variance * m[1]
        cv = aggregate_var**0.5 /aggregate_mean
        
        self.assertAlmostEqual(0.7906, cv, 4)

        #c) calculate parameters for lognormal distribution          

    def test_spring_18_8(self):
        cat = Reinsurance_Pricing()
        cat.mean, cat.variance = 1, 0.5*0.5 # binomial distribution
        loss_size_probability = [0, .25, .25, .25, .25]
        aggregate_losses_prob = [0.250000, 0.125000, 0.140625, 0.156250,
                                 0.171875, 
                                 0.062500, 0.046875, 0.031250, 
                                 0.015625] # 4,8 unknown
        
        #a
        p = cat.aggregate_loss_probability(loss_size_probability, aggregate_losses_prob, 4)
        self.assertAlmostEqual(.171875, p + 0.05859375)

        p = cat.aggregate_loss_probability(loss_size_probability, aggregate_losses_prob, 8)
        self.assertAlmostEqual(.015625, p/2 )

        

        

     
if __name__ == '__main__':
    unittest.main()
