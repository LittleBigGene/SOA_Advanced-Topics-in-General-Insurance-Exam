
import unittest
from RatemakingAFinEconApproach import Ratemaking_A_FinEcon_Approach as rfe

class test_RatemakingAFinEconApproach(unittest.TestCase):
    def test_spring_19_7(self):
        targetModel = rfe(RiskFreeRate=.02, Beta=1.5, MarketRiskPremium=.06, Premium=850000, Equity=500000, InvestableAsset=1200000, InvestmentReturn=.07)
        #a
        self.assertAlmostEqual(.11, targetModel.CAPM_Total_Return()) 
        #b
        self.assertAlmostEqual(-.0341, targetModel.UW_Profit_Margin(), 4) 


if __name__ == '__main__':
    unittest.main()
