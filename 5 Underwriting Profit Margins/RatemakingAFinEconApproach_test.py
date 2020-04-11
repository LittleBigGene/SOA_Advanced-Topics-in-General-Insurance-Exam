
import unittest
from RatemakingAFinEconApproach import Ratemaking_A_FinEcon_Approach as CAPM

class test_RatemakingAFinEconApproach(unittest.TestCase):
    def test_spring_19_7(self):
        targetModel = CAPM()

        targetModel.RiskFreeRate = .02
        targetModel.Beta = 1.5
        targetModel.MarketRiskPremium = .06
        targetModel.Premium = 850000
        targetModel.Equity = 500000
        targetModel.InvestableAsset = 1200000
        targetModel.InvestmentReturn = .07
        #a
        self.assertAlmostEqual(.11, targetModel.CAPM_Total_Return()) 
        #b
        self.assertAlmostEqual(-.0341, targetModel.UW_Profit_Margin(), 4) 


    def test_fall_16_7(self):
        targetModel = CAPM()
        targetModel.RiskFreeRate = .01
        targetModel.Beta = -.2
        targetModel.MarketRiskPremium = .05

        # a
        k = .4 * 3 / 12 + .4 * 6 / 12 + .2 * 9 / 12
        self.assertAlmostEqual(0.45, k)

        # b
        uw_beta = targetModel.Beta * -k
        self.assertAlmostEqual(0.09, uw_beta)

        # c
        upm = -k * targetModel.RiskFreeRate + uw_beta * targetModel.MarketRiskPremium
        self.assertAlmostEqual(0, upm)

        # e) Provide two criticisms of models that apply the Capital Asset Pricing Model to insurance.
        # The model only covers risk that varies with market returns. As such, it ignores unique insurance risks such as catastrophe.
        # The insurance market cannot simply be appended to the stock market.
        

    def test_spring_16_5(self):

        pvL = 70 / 2 / 0.94 + 70 / 2 / 0.94 / 0.94
        pvE = 20

        p = 99.7

        pvTUW = (p-20) * 0.4 / 1.01 - 70 * 0.4 / 0.94
        pvTII = (p+100-20) * 0.01 * .4 /1.01 + (p + 50 - 20 - 35) * 0.01 * 0.4 / 1.01**2

        #a       
        self.assertAlmostEqual(p, pvL + pvE + pvTUW + pvTII , 2)

        #b) You are also considering using the Target Total Rate of Return Model. 
        #   You need to decide whether to use statutory surplus or the company’s actual equity to derive the required underwriting profit margin.

        # Actual equity should be used, because using statutory surplus has the following issues:
        #  It is usually lower than actual equity and thus will lead to a lower profit margin, which may lead to investment in risky assets.
        #  It ignores the time value of money.
        #  It excludes tangible assets and some reinsurance.
        #  It does not value bonds and real estate at market value.

        #c) Explain the adjustment to the Capital Asset Pricing Model (CAPM) needed to reflect increased risk.
        
        # The absolute value of beta should be increased.

if __name__ == '__main__':
    unittest.main()
