
import unittest
from sympy import symbols
from RatemakingAFinEconApproach import Ratemaking_A_FinEcon_Approach as FinEconRatemaking

class test_RatemakingAFinEconApproach(unittest.TestCase):
    def test_spring_19_7(self):
        targetModel = FinEconRatemaking()

        exp_r = symbols('r')
        sol = targetModel.CAPM_Total_Return(
            exp_return = exp_r,
            risk_free=.02,
            beta=1.5,
            market_risk_premium=.06            
        )
        #a
        self.assertAlmostEqual(.11, sol) 

        upm = symbols('upm')
        sol = targetModel.Target_Total_Rate_of_Return_1(
            P=850000,
            S=500000,
            UPM = upm,
            IA = 1200000,
            IR = .07,
            TRR = .11
        )
        
        #b
        self.assertAlmostEqual(-.0341, sol, 4) 

    def test_fall_16_7(self):
        targetModel = FinEconRatemaking()
        
        # a
        k = .4 * 3 / 12 + .4 * 6 / 12 + .2 * 9 / 12
        self.assertAlmostEqual(0.45, k)

        # b
        beta = -.2
        self.assertAlmostEqual(0.09, beta * -k)

        # c
        upm = symbols('upm')
        sol = targetModel.CAPM_UPM(
            UPM=upm,
            k = k,
            risk_free=.01,
            uw_beta = beta * -k,
            market_risk_premium=.05
        )

        self.assertAlmostEqual(0, sol)

        # e) Provide two criticisms of models that apply the Capital Asset Pricing Model to insurance.
        # The model only covers risk that varies with market returns. As such, it ignores unique insurance risks such as catastrophe.
        # The insurance market cannot simply be appended to the stock market.
       
    def test_spring_16_5(self):
        
        p = symbols('p')
        riskFree, riskAdjLoss = 0.01, -0.06

        targetModel = FinEconRatemaking()        
        sol = targetModel.Risk_Adjusted_Discount_Technique( 
            premium = p,                    risk_free = 0.01,            
            losses = [0, 70 / 2, 70 / 2],   risk_adj_loss = -0.06,
            expense = 20,                    uw_pl = 70,
            invest_income = [0, (p + 100 - 20), (p + 50 - 20 - 35)],
            tax = 0.4
        )        

        #a       
        self.assertAlmostEqual(sol, 99.69 + 0.02 , 2)

        #b) You are also considering using the Target Total Rate of Return Model. 
        #   You need to decide whether to use statutory surplus or the company’s actual equity to derive the required underwriting profit margin.

        # Actual equity should be used, because using statutory surplus has the following issues:
        #  It is usually lower than actual equity and thus will lead to a lower profit margin, which may lead to investment in risky assets.
        #  It ignores the time value of money.
        #  It excludes tangible assets and some reinsurance.
        #  It does not value bonds and real estate at market value.

        #c) Explain the adjustment to the Capital Asset Pricing Model (CAPM) needed to reflect increased risk.
        
        # The absolute value of beta should be increased.

    def test_fall_17_3(self):
        targetModel = FinEconRatemaking()        

        #a
        p = symbols('p')        
        riskFree = 0.0175
        sol = targetModel.Target_Total_Rate_of_Return( 
            P = symbols('p'),
            S = 0.5 * p,
            E = 26,
            L = 70,
            IR = riskFree,
            TRR = 0.15
        )        
        self.assertAlmostEqual(sol, 101.40, 2)

        #b  
        p = 101.40
        r = symbols('r')        
        sol = targetModel.Risk_Adjusted_Discount_Technique( 
            premium = p,                  risk_free = 0.0175,            
            losses = [0, 70 * (1-.35)],   risk_adj_loss = r,
            expense = 26,                 uw_pl = 0,
            invest_income = [ (p + p/2 - 26) ],
            tax = 0.35
        )    
        self.assertAlmostEqual(sol, -0.066, 3)

        #c
        pct_ceded = .6
        re_A = targetModel.Target_Total_Rate_of_Return( 
            P = p * (1-pct_ceded) ,
            S = p/2 * (1-pct_ceded) ,
            E = 26 * (1-pct_ceded) ,
            L = 70 * (1-pct_ceded) ,
            IR = riskFree,
            TRR = r
        )        
        self.assertAlmostEqual( re_A , .15, 3)

        pct_ceded = .4
        commission = .3
        re_B = targetModel.Target_Total_Rate_of_Return( 
            P = p * (1-pct_ceded)  ,
            S = p/2 * (1-pct_ceded) ,
            E = 26 - commission * pct_ceded * p,
            L = 70 * (1-pct_ceded) ,
            IR = riskFree,
            TRR = r
        )        
        self.assertAlmostEqual(re_B, .209, 3)


if __name__ == '__main__':
    unittest.main()
