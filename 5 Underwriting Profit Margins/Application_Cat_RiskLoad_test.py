
import unittest
from Application_Cat_RiskLoad import Risk_Load

class test_RiskLoad(unittest.TestCase):

    def setUp(self):
        self.account = Risk_Load()

    def test_spring_19_1(self):        
        account = self.account

        a = 0.0002 * (account.binomial_variance(0.01, 1000) + account.binomial_variance(0.02, 3000) + account.binomial_variance(0.03, 5000))
        self.assertAlmostEqual(a, 182.76)

        combined_variance = account.binomial_variance(0.01, 1000 + 200) + account.binomial_variance(0.02, 3000 + 500) + account.binomial_variance(0.03, 5000)        
        b = 0.0002 * combined_variance - a
        self.assertAlmostEqual(b, 13.61, 2)

        new_account_variance = account.binomial_variance(0.01, 200) + account.binomial_variance(0.02, 500) + account.binomial_variance(0.03, 0)
        new_account_risk_load = 0.0002 * new_account_variance        
        self.assertNotEqual(b, new_account_risk_load)

        S1 = (combined_variance) ** 0.5
        S0 = (a / 0.0002) ** 0.5

        d = account.marginal_surplus_Z(y = 0.15, r = b, S_1 = S1, S_0 = S0 )
        self.assertAlmostEqual(d, 2.985, 3)

    def test_fall_16_6(self):

        account = self.account

        var_x = [17640000, 2227500]
        var_y = [78400   , 22275]
        var_xy = [20070400, 2695275]

        # a
        # var(x+y) = var(x) + 2cov(x+y) + var(y)
        cov_xy = (sum(var_xy) - sum(var_x) - sum(var_y)) / 2

        x_riskLoad = account.shapley(sum(var_x), cov_xy)
        y_riskLoad = account.shapley(sum(var_y), cov_xy)

        self.assertAlmostEqual(532, x_riskLoad*.000025, 0)
        self.assertAlmostEqual(37, y_riskLoad*.000025, 0)

        # b
        loss_x = [30000, 15000]
        loss_y = [2000 , 1500]
        loss_xy= [32000, 16500]

        cov_share = account.covariance_share(loss_x, loss_y, loss_xy, var_x, var_y, var_xy)
        
        self.assertAlmostEqual(562, cov_share[0]*.000025, 0)
        self.assertAlmostEqual(7, cov_share[1]*.000025, 0) 

        # c) Evaluate which method is more likely to produce appropriate risk loads to be used in pricing.
        # The covariance share method is more appropriate because it allocates less of the covariance to smaller accounts, which should have lower risk.

    def test_spring_16_2(self):
        account = self.account

        p = [.01, .02, .03]
        L = [100, 200, 400]        
        varE = account.binomial_variances(p,L)

        p = [.02, .04, .06, .07]
        L = [500, 400, 200, 100]        
        varH = account.binomial_variances(p,L)

        corr = 0.2
        cov = corr * ((varE * varH)**0.5)
        var = varE + varH + 2 * cov

        # a
        self.assertAlmostEqual(25 * 23006.24, 25* var, 0)

        # b 
        e = account.shapley(varE, cov)
        self.assertAlmostEqual(182428, e * 25, 0)
        h = account.shapley(varH, cov)
        self.assertAlmostEqual(392728, h * 25, 0)

        # d
        self.assertAlmostEqual(436681, 25 * (var - varE), 0)        
        self.assertAlmostEqual(226381, 25 * (var - varH), 0)

if __name__ == '__main__':
    unittest.main()
