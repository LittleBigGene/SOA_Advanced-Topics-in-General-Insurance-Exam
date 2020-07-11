
import unittest
from sympy import symbols
from RatemakingAFinEconApproach import Ratemaking_A_FinEcon_Approach as FinEconRatemaking

class test_RatemakingAFinEconApproach(unittest.TestCase):
    def test_16_fall_7(self):
        targetModel = FinEconRatemaking()
        
        # a
        k = .4 * 3 / 12 + .4 * 6 / 12 + .2 * 9 / 12
        self.assertAlmostEqual(0.45, k)

        # b
        beta = -.2
        self.assertAlmostEqual(0.09, beta * -k)

        # c
        upm = symbols('upm')
        sol = targetModel.Fairley_CAPM(
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
       
    def test_16_spring_5(self):
        
        p = symbols('p')
        riskFree, riskAdjLoss = 0.01, -0.06

        targetModel = FinEconRatemaking()        
        sol = targetModel.Risk_Adjusted_Discount_Technique( 
            premium = p,                    risk_free = 0.01,            
            losses = [0, 70 / 2, 70 / 2],   risk_adj_loss = -0.06,
            expense = 20,                    uw_loss = -70,
            invest_income = [0, (p + 100 - 20), (p + 50 - 20 - 35)],
            tax = 0.4
        )        

        #a        
        self.assertAlmostEqual(sol, 99.69+0.02 , 2)

        #b) You are also considering using the Target Total Rate of Return Model. 
        #   You need to decide whether to use statutory surplus or the company’s actual equity to derive the required underwriting profit margin.

        # Actual equity should be used, because using statutory surplus has the following issues:
        #  It is usually lower than actual equity and thus will lead to a lower profit margin, which may lead to investment in risky assets.
        #  It ignores the time value of money.
        #  It excludes tangible assets and some reinsurance.
        #  It does not value bonds and real estate at market value.

        #c) Explain the adjustment to the Capital Asset Pricing Model (CAPM) needed to reflect increased risk.
        
        # The absolute value of beta should be increased.

    def test_17_fall_3(self):
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
            losses = [0, 70],   risk_adj_loss = r,
            expense = 26,                 uw_loss = -70,
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

    def test_17_spring_3(self):
        #a) assumptions of the Captial Asset Pricing Model
        #   • Investors are risk averse.
        #   • Investors are price takers.
        #   • Investors have identical expectations.
        #   • Investors have no transaction costs.
        #   • Investors can borrow or invest at the risk-free rate.
        #   • Assets are infinitely divisible.

        #b)
        targetModel = FinEconRatemaking()     

        upm = symbols('upm')
        sol = targetModel.Fairley_CAPM(
            UPM=upm,
            k = 0.75,
            risk_free=0.02,
            uw_beta = 0.5,
            market_risk_premium=.03,
            tax= [0.231,0.35],
            equity_to_premium = 2
        )
        self.assertAlmostEqual(1.15/100, sol, 4)

    def test_18_fall_3(self):
        
        p = symbols('p')        

        targetModel = FinEconRatemaking()        
        sol = targetModel.Risk_Adjusted_Discount_Technique( 
            premium = p,        risk_free = 0.02,            
            losses = [0,80],   risk_adj_loss = -0.02,
            expense = 20,       uw_loss = -80,
            invest_income = [0, (50 + p - 20)],
            tax = 0.2
        )      
        #a)
        self.assertAlmostEqual(101.875 + 0.003, sol, 3 )

        #b) Describe three criticisms of the Risk Adjusted Discounted Technique as applied to insurance models.
        #   Commentary on Question: Any three of the following are sufficient for full credit.
        #   • The risk-free rate may not be the correct rate to use.
        #   • It is not clear how to set the risk-adjusted rate.
        #   • It is difficult to allocate equity to policies.
        #   • It considers only one policy term, not renewal cycles.
        #   • Actual taxes may not be at the corporate rate.
        #   • Expenses may depend on the premium rate.

    def test_18_spring_4(self):
        #a) Explain why owners’ equity is difficult to determine.
        # • Insurers do not set rates in aggregate, but on a by-line and by-state basis. 
        #   However, equity is normally only calculated in aggregate.

        # • Statutory surplus is generally lower than actual equity due to 
        #       ignoring time value of money, 
        #       excluding some assets, and 
        #       valuing some assets at other than market value.

        targetModel = FinEconRatemaking()
        #b       
        upm = symbols('upm')
        step1 = targetModel.Fairley_CAPM(
            UPM=upm,
            k = 1,
            risk_free=.02,
            uw_beta = 1.5,
            market_risk_premium=.04
        )
        self.assertAlmostEqual(0.04, step1)

        p = symbols('p')
        step2 = targetModel.Target_Total_Rate_of_Return_1(
            P=p,
            S=100,
            UPM = step1,
            IA = p-25+100,
            IR = .02,
            TRR = .07
        )

        self.assertAlmostEqual(91.66666666, step2)

        #c 40% quota share
        # before reinsurance
        upm = 0.04
        p = 91.666
        e = 25
        L = (1 - upm) * p - e
        
        # after reinsurance        
        E = e - .35 * .4 * p
        P = 0.6*p      
        L = 0.6*L  
        upm = 1 - L/P - E/P

        self.assertAlmostEqual(0.0915, upm, 4)        

        trr = symbols('trr')        
        sol = targetModel.Target_Total_Rate_of_Return( 
            P = P,
            S = .6 * 100,
            E = E,
            L = L,
            IR = .02,
            TRR = trr
        )        
        self.assertAlmostEqual(0.118, sol, 3)
        
    def test_19_spring_7(self):
        targetModel = FinEconRatemaking()

        exp_r = symbols('r')
        sol = targetModel.CAPM_Total_Return(
            exp_return = exp_r,
            risk_free=.02,
            beta=1.5,
            market_risk_premium=.06            
        )
        #a) CAPM
        self.assertAlmostEqual(.11, sol) 

        #b) TRR
        upm = symbols('upm')
        sol = targetModel.Target_Total_Rate_of_Return_1(
            P=850000,
            S=500000,
            UPM = upm,
            IA = 1200000,
            IR = .07,
            TRR = .11
        )
        self.assertAlmostEqual(-.0341, sol, 4) 

        #c) Explain how the existence of catastrophe risk makes the use of CAPM problematic for insurers.
        # CAPM provides a risk premium only for risks that are systematic with market returns. 
        # Catastrophe risk is not such a risk and hence is not considered by CAPM.

        #d) Explain the relationship between the IRR and NPV when employing discounted cash flow analysis.
        # The IRR is the discount rate such that NPV is zero. 
        # If cash flows change sign more than once, there may be multiple solutions.

if __name__ == '__main__':
    unittest.main()
