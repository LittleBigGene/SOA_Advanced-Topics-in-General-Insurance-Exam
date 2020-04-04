
import unittest
from Application_Cat_RiskLoad import Risk_Load as rl

class test_RiskLoad(unittest.TestCase):
    def test_spring_19_1(self):
        
        account = rl()

        a = 0.0002 * (account.Variance_Binomial(0.01, 1000) + account.Variance_Binomial(0.02, 3000) + account.Variance_Binomial(0.03, 5000))
        self.assertAlmostEqual(a, 182.76)

        combined_variance = account.Variance_Binomial(0.01, 1000 + 200) + account.Variance_Binomial(0.02, 3000 + 500) + account.Variance_Binomial(0.03, 5000)        
        b = 0.0002 * combined_variance - a
        self.assertAlmostEqual(b, 13.61, 2)

        new_account_variance = account.Variance_Binomial(0.01, 200) + account.Variance_Binomial(0.02, 500) + account.Variance_Binomial(0.03, 0)
        new_account_risk_load = 0.0002 * new_account_variance        
        self.assertNotEqual(b, new_account_risk_load)

        S1 = account.Standard_Deviation(combined_variance)
        S0 = account.Standard_Deviation(a / 0.0002)

        d = account.Marginal_Surplus_Z(y = 0.15, r = b, S_1 = S1, S_0 = S0 )
        self.assertAlmostEqual(d, 2.985, 3)

if __name__ == '__main__':
    unittest.main()
