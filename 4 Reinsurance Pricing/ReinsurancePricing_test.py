import unittest
from ReinsurancePricing import Reinsurance_Pricing as rp

class test_ReinsurancePricing(unittest.TestCase):

    def setUp(self):
        pass

    def test_spring19_2(self):        
        IncreasedLimitsFactor = {0:0, 1:1, 2:1.16 , 3:1.28 , 4:1.38 }
        ExpectedLoss = rp(IncreasedLimitsFactor)

        #a
        a1 = ExpectedLoss.exposure_rating(0, 1, IncreasedLimitsFactor)
        self.assertAlmostEqual(a1, 0)

        a2 = ExpectedLoss.exposure_rating(0, 2, IncreasedLimitsFactor)
        self.assertAlmostEqual( a2, 0.138, 3)

        a3 = ExpectedLoss.exposure_rating(0, 3, IncreasedLimitsFactor)
        self.assertAlmostEqual( a3, 0.219, 3)

        a4 = ExpectedLoss.exposure_rating(1, 2, IncreasedLimitsFactor)
        self.assertAlmostEqual( a4, 0.429, 3)
        
        a5 = ExpectedLoss.exposure_rating(1, 3, IncreasedLimitsFactor)
        self.assertAlmostEqual(a5, 0.579, 3)

        a = .6*(3 * a1 + 4 * a2 + 5 * a3 + 8 * a4 + 9 * a5)
        self.assertAlmostEqual(a, 6.17, 2)
     
        #b
        averageLossCost = 0.1 * 0.04 + 0.75 * 0.19 + 0.15 * 0.44
        self.assertAlmostEqual(averageLossCost, .2125)

        loadedLossCost =  0.1 * ExpectedLoss.swing_plan(0.375,.125,100/80,0.04) + 0.75 * ExpectedLoss.swing_plan(0.375,.125,100/80,0.19) + 0.15 * ExpectedLoss.swing_plan(0.375,.125,100/80,0.44)
        self.assertAlmostEqual( loadedLossCost, .2469, 4)
    
    def test_spring19_8(self):
        annualPrem = 50
        margin = .1 * annualPrem
        OccurrenceLimit = 200         
        
        specialist = rp()

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

    def test_fall16_1(self):
        treaty = rp()
                       
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
        
if __name__ == '__main__':
    unittest.main()
