import unittest
import numpy as np
import pandas as pd
from ReinsurancePricing import Reinsurance_Pricing

class test_ReinsurancePricing(unittest.TestCase):

    def test_16_fall_1(self):
        
        standard_premium_x, expected_loss_ratio_x = 0.6, 0.6 
        standard_premium_y, expected_loss_ratio_y = 0.4, 0.7
        
        allocation_x, allocation_y = 0.5, 0.5
        
        expected_loss_x = standard_premium_x * expected_loss_ratio_x
        expected_loss_y = standard_premium_y * expected_loss_ratio_y

        layer_x, layer_y = (0.05-0.0125), (0.1-0.025)
        
        self.assertAlmostEqual(0.036, (expected_loss_x + expected_loss_y) * (allocation_x * layer_x + allocation_y * layer_y))

        # For policy limits, because workers compensation insurance does not have policy limits, no adjustment is needed. 
        # For discounting, loss data should be requested on a full undiscounted basis.
        
        # Historical premiums should be adjusted for rate changes and for exposure (payroll) inflation. 
        # Historical losses should be adjusted for trend and for development.
    
    def test_16_fall_8(self):
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

    def test_16_spring_1(self):
        surplus_share_retained_line = 500
        insured_values = np.clip(np.array([100,200,500,1000]), 0, surplus_share_retained_line)

        betaRe = Reinsurance_Pricing()
        
        expo = 0
        for iv in insured_values:
            layer = betaRe.risk_exposure_rating(limit = 400, retention = 100, insured_value = iv)
            expo += layer
        # a
        self.assertAlmostEqual(1020833, expo * 0.6 * 1000000, 0)

        # b) explain free cover
        # no trended losses in the top of the layer

        # c) State whether the property catastrophe cover will typically inure to the benefit of the surplus share reinsurance.
        # The answer is no. The reverse is typically true. 
        # The surplus share reinsurance will inure to the benefit of the property catastrophe cover.

        # d) state whether the property catastrophe cover will typically inure to the benefit of the property per risk excess treaty.
        # The answer is no. The reverse is typically true. 
        # The property per risk excess treaty will inure to the benefit of the property catastrophe cover.

    def test_16_spring_8(self):
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

    def test_17_fall_1(self):
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

        ExpectedLoss.AP = 500
        ExpectedLoss.Limit = 500

        #b
        b1 = ExpectedLoss.occurrence_exposure_rating(1000, 1000, 0.1)
        b2 = ExpectedLoss.occurrence_exposure_rating(1000, 2000, 0.1)

        self.assertAlmostEqual(460 / 1200, b1)
        self.assertAlmostEqual(230 / 785 , b2)

        total_expeced_loss = .6 * (460 + 230) 
        #print(total_expeced_loss)

        #c) clash cover
        
        #d) Describe two ways that a loss on this treaty could occur. 
        #   Any two of the following were sufficient for full credit.
        #   • Multiple policies involved in a single occurrence
        #   • Extra-contractual obligations
        #   • Rulings awarding damages in excess of policy limits
        #   • ALAE being included with losses and the total exceeding policy limits

    def test_17_fall_8(self):
        cat = Reinsurance_Pricing()
        cat.mean, cat.variance = 1, 2 # geometric distribution

        loss_size_probability = [0, .4, .3, .2, .1]
        aggregate_losses_prob = [.5,.1,.095,.084,.0661,.0403,.0311,.0231,.0166,.0119]

        #a
        p = cat.aggregate_loss_probability(a=0.5, b= 0, k=10, S=loss_size_probability, A= aggregate_losses_prob)
        self.assertAlmostEqual(.0087, p, 4)

        #b
        m = cat.moment_of_loss(loss_size_probability)
        
        aggregate_mean = cat.mean * m[0]
        aggregate_var  = cat.variance * m[1]
        cv = aggregate_var**0.5 /aggregate_mean

        self.assertAlmostEqual(1.581, cv, 3)

    def test_cas8_2013_25(self):
        # Recursive Formula - frequency and severity can be analyzed separately. 
        #   being simple to work with and
        #   works well for low frequency scenarios
                
        #   But only a single severity distribution can be used.
        #   and require an evenly spaced severity distribution. 
        pass

    def test_17_spring_1(self):
        cat = Reinsurance_Pricing()

        exp = {
            'Accident Date': [2014,2014,2015,2015,2016,2016],
            'Untrended Loss': [200, 400, 550,1000, 600, 450],
            'Untrended ALAE': [100, 200,   0, 500, 300,   0]
            }
        
        exp = cat.occurrence_experience_rating(exp, 
            layer = 200, excessOf = 400, trend=1.06, policeLimit= 1000, valYear=2018)
        
        undev14 = exp[exp['Accident Date'] == 2014]
        undev15 = exp[exp['Accident Date'] == 2015]
        undev16 = exp[exp['Accident Date'] == 2016]

        dev14 = sum(undev14['Layer Loss+ALAE']) * 1.1
        dev15 = sum(undev15['Layer Loss+ALAE']) * 1.5
        dev16 = sum(undev16['Layer Loss+ALAE']) * 2

        #print(f"({dev14} + {dev15} + {dev16}) ")
        # a
        self.assertAlmostEqual(0.059, (dev14 + dev15 + dev16)/ 30000, 3)

        # b) The ceding company requests alternative quotes on the following two layers:
        #   (i)  200,000 excess of 300,000
        #   (ii) 200,000 excess of 200,000

        # For both cases revised (likely smaller) development factors would be needed
        # For case (ii) information about untrended losses below 200,000 would be needed. 
        #   Assuming the 6% trend factor applies to these losses, untrended losses of 200,000/1.06^4 = 158,419 (likely rounded to 150,000) or larger would be required.

    def test_17_spring_8(self):
        cat = Reinsurance_Pricing()
        cat.mean, cat.variance = 2, 2 # poisson distribution
        loss_size_probability = [0, .4, .3, .2, .1]
        aggregate_losses_prob = [0.1353, 0.1083, 0.1245, 0.1306, 0.1230, 0.0982, 0.0804, 0.0621, 0.0453, 0.0318]
        
        #a
        p = cat.aggregate_loss_probability(a=0, b= 2, k=10, S=loss_size_probability, A= aggregate_losses_prob)
        self.assertAlmostEqual(.0219, p, 4)

        #b
        m = cat.moment_of_loss(loss_size_probability)
        
        aggregate_mean = cat.mean * m[0]
        aggregate_var  = cat.variance * m[1]
        cv = aggregate_var**0.5 /aggregate_mean
        
        self.assertAlmostEqual(0.7906, cv, 4)

        #c) calculate parameters for lognormal distribution          

    def test_18_spring_8(self):
        cat = Reinsurance_Pricing()
        cat.mean, cat.variance = 1, 0.5*0.5 # binomial distribution
        loss_size_probability = [0, .25, .25, .25, .25]
        aggregate_losses_prob = [0.250000, 0.125000, 0.140625, 0.156250,
                                 0.171875, 
                                 0.062500, 0.046875, 0.031250, 
                                 0.015625] # 4,8 unknown
        M, p = 2, 0.5

        #a
        p4 = cat.aggregate_loss_probability(a=p/(p-1), b= (M+1)*p/(1-p), k=4, S=loss_size_probability, A=aggregate_losses_prob)
        self.assertAlmostEqual(.171875, p4)

        p8 = cat.aggregate_loss_probability(a=p/(p-1), b= (M+1)*p/(1-p), k=8, S=loss_size_probability, A=aggregate_losses_prob)
        self.assertAlmostEqual(.015625, p8 )

    def test_18_fall_1(self):        
        tolerant = Reinsurance_Pricing()

        def expected (vector):
            return sum(vector) / len(vector) / 100

        #a
        loss_ratio, commission, expense = .65, .10, .15
        amt_returned = .4

        tech17 = amt_returned * (1 - loss_ratio - commission - expense) + loss_ratio + commission
        self.assertAlmostEqual(0.79, tech17)
        
        #b
        carryover = 65 - 60
        lr = [30, 70]
        comm_min=[10,60]
        comm_max=[20,40]        
        tech18 = tolerant.technical_ratio(lr, comm_min, comm_max, sliding=.5, carryforward = carryover) 
        
        afterReturnToCeding = expected(tech18) + 11*(35-30)/4000 + 8*(55-35)/4000 + 3*(70-55)/4000 - carryover/100

        self.assertAlmostEqual(0.7028, afterReturnToCeding, 4)

        #c) Describe two complications with pricing the effect of carryforward provisions.
        #   • There is no obvious method for reducing the variance of the aggregate distribution.
        #   • It is difficult to take into account the uncertainty about whether the treaty will be renewed.

    def test_18_fall_8(self):
        #a trend and ultimate losses
        #b Define free cover.
        #   Free cover occurs when no losses trend into the highest portion of the layer covered.

        #c Calculate a suitable adjustemnt to the loss cost using those expsore factors to estiamte the cost of free cover

        #d  Using these exposure factors would imply that the factors are scale invariant. 
        #   This is reasonable for homeowners insurance, but not for commercial property.
        pass

    def test_18_spring_2(self):
        pricing = Reinsurance_Pricing()
        insuredValue = pd.Series(data=[2000,20000,8000,12500,4000])
        loss =  pd.Series(data=[400,16000,3200,12500,1200])

        surplusCededLoss = pricing.surplus_share(insuredValue, loss, 2000, 2000*5)
        surplusRetainedLoss = loss - surplusCededLoss

        xsCession = (surplusRetainedLoss - 1000).clip(0,4000)        
        xsRetained = surplusRetainedLoss - xsCession        
            
        assert surplusCededLoss.sum() == 21000
        assert xsCession.sum() == 5500
        assert xsRetained.sum() - 6000 == 800

        #b
        assert 600 * 1.25 * 800 / 8000 == 75

        #c) Discuss whether a reinstatement pro-rata as to time would be appropriate for this type of cover.

        # Reinstatement pro-rata as to time is uncommon and usually inappropriate for windstorm coverage, which is seasonal. 
        # That is, exposure to risk is not uniform over the coverage period.

        #d) Explain with an example why a catastrophe cover is usually written on 
        #   a losses occurring basis rather than on a risks attaching basis.

    def test_19_spring_2(self):        
        ExpectedLoss = Reinsurance_Pricing()
        ExpectedLoss.ILF = {0:0, 1:1, 2:1.16 , 3:1.28 , 4:1.38 }
        ExpectedLoss.AP = 1
        ExpectedLoss.Limit = 2

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
    
    def test_19_spring_8(self):
        P = 50     # Annual Prem
        M = .1 * P # Margin        
        
        #a_i no losses, additional premium is zero
        L, AP = 0, 0         
        C = 0.95*(P - M)
        netPL_i = P - L - C + AP
        self.assertAlmostEqual(7.25, netPL_i)

        #a_ii one or more loss, commission is zero
        L, C = 200, 0
        AP = .6 * (L + M - P)                
        netPL_ii = P - L - C + AP        
        self.assertAlmostEqual(-57, netPL_ii)

        #b the rate on line for an equivalent traditional risk cover
        rateOnLine = netPL_i/(netPL_i-netPL_ii)        
        self.assertAlmostEqual(.113, rateOnLine, 3 )

        #c 
        AP = 108.917
        netPL_ii = P - L - C + AP 
        rateOnLine = netPL_i/(netPL_i-netPL_ii) 
        self.assertAlmostEqual(.15, rateOnLine, 3 )

    def test_cas8_2019_17(self):
        pass

    def test_cas8_2014_23(self):
        pass 



if __name__ == '__main__':
    unittest.main()

    
