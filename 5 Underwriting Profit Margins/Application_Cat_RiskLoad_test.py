
import unittest
from Application_Cat_RiskLoad import Risk_Load

class test_RiskLoad(unittest.TestCase):

    def test_spring_19_1(self):        
        account = Risk_Load()

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
        account = Risk_Load()

        account.var_x = [17640000, 2227500]
        account.var_y = [78400   , 22275]
        account.var_xy = [20070400, 2695275]

        # a
        # var(x+y) = var(x) + 2cov(x+y) + var(y)
        cov_xy = (sum(account.var_xy) - sum(account.var_x) - sum(account.var_y)) / 2

        x_riskLoad = account.shapley(sum(account.var_x), cov_xy)
        y_riskLoad = account.shapley(sum(account.var_y), cov_xy)

        self.assertAlmostEqual(532, x_riskLoad*.000025, 0)
        self.assertAlmostEqual(37, y_riskLoad*.000025, 0)

        # b
        loss_x = [30000, 15000]
        loss_y = [2000 , 1500]

        cov_share = account.covariance_share(loss_x, loss_y)
        
        self.assertAlmostEqual(562, cov_share[0]*.000025, 0)
        self.assertAlmostEqual(7, cov_share[1]*.000025, 0) 

        # c) Evaluate which method is more likely to produce appropriate risk loads to be used in pricing.
        # The covariance share method is more appropriate because it allocates less of the covariance to smaller accounts, which should have lower risk.

    def test_spring_16_2(self):
        account = Risk_Load()

        account.p = [.01, .02, .03]        
        varE = sum(account.binomial_variances([100, 200, 400]))

        account.p = [.02, .04, .06, .07]
        varH = sum(account.binomial_variances([500, 400, 200, 100]))

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

    def test_fall_17_6(self):
        account = Risk_Load()
        
        account.p = [.01, .02]
        L_x = [ 20000,  10000]        
        L_y = [  4000,   6000]   
        λ = 0.000024     
        L_xy = [x + y for x, y in zip(L_x, L_y)]

        account.var_x = account.binomial_variances(L_x)
        account.var_y = account.binomial_variances(L_y)
        account.var_xy = account.binomial_variances(L_xy)

        #a
        sol = account.mv_renewal_risk_load(L_x, L_y, λ)
        
        self.assertAlmostEqual(236.544, sol[0])
        self.assertAlmostEqual(115.2  , sol[1])

        # #b
        assert sum(sol) > sum(account.var_xy) * λ

        # #c        
        sol = account.covariance_share(L_x, L_y, λ)
        self.assertAlmostEqual(209.04, sol[0])
        self.assertAlmostEqual( 48.24, sol[1])
        

if __name__ == '__main__':
    unittest.main()
