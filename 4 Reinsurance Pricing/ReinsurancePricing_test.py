import unittest
import numpy as np
from ReinsurancePricing import Reinsurance_Pricing

class test_ReinsurancePricing(unittest.TestCase):

    def setUp(self):
        pass

    def test_spring_19_2(self):        
        ExpectedLoss = Reinsurance_Pricing()
        ExpectedLoss.ILF = {0:0, 1:1, 2:1.16 , 3:1.28 , 4:1.38 }
        
        #a
        a1 = ExpectedLoss.occurrence_exposure_rating(0, 1)
        self.assertAlmostEqual(a1, 0)

        a2 = ExpectedLoss.occurrence_exposure_rating(0, 2)
        self.assertAlmostEqual( a2, 0.138, 3)

        a3 = ExpectedLoss.occurrence_exposure_rating(0, 3)
        self.assertAlmostEqual( a3, 0.219, 3)

        a4 = ExpectedLoss.occurrence_exposure_rating(1, 2)
        self.assertAlmostEqual( a4, 0.429, 3)
        
        a5 = ExpectedLoss.occurrence_exposure_rating(1, 3)
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

        self.assertAlmostEqual(1020833, expo * 0.6 * 1000000, 0)

if __name__ == '__main__':
    unittest.main()
