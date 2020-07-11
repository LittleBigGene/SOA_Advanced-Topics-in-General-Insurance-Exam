
import unittest
import numpy as np
from sympy import symbols
from Application_Cat_RiskLoad import Risk_Load

class test_RiskLoad(unittest.TestCase):
    def test_16_fall_6(self):
        account = Risk_Load()
        
        account.var_x = [17640000, 2227500]
        account.var_y = [78400   , 22275]
        account.var_xy = [20070400, 2695275]

        # a
        # var(x+y) = var(x) + 2cov(x+y) + var(y)
        cov_xy = (sum(account.var_xy) - sum(account.var_x) - sum(account.var_y)) / 2

        x_riskLoad = account.shapley(sum(account.var_x), cov_xy, .000025)
        y_riskLoad = account.shapley(sum(account.var_y), cov_xy, .000025)

        self.assertAlmostEqual(532, x_riskLoad, 0)
        self.assertAlmostEqual(37, y_riskLoad, 0)

        # b
        loss_x = [30000, 15000]
        loss_y = [2000 , 1500]

        cov_share = account.covariance_share(loss_x, loss_y, .000025)
        
        self.assertAlmostEqual(562, cov_share[0], 0)
        self.assertAlmostEqual(7, cov_share[1], 0) 

        # c) Evaluate which method is more likely to produce appropriate risk loads to be used in pricing.
        # The covariance share method is more appropriate because it allocates less of the covariance to smaller accounts, which should have lower risk.

    def test_16_spring_2(self):
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

    def test_17_fall_6(self):
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
        
    def test_17_spring_6(self):
        account = Risk_Load()

        sd_x = 0.3 * 2000
        sd_y = 0.4 * 450
        cov_xy = 0.2*sd_x*sd_y
        var_xy = sd_x**2 + sd_y**2 + 2 * cov_xy

        #a
        risk_load = account.marginal_surplus(z=2.33, r=symbols('r'), y=0.1, SD_L1=var_xy**0.5)
        self.assertAlmostEqual(139.8, risk_load, 1)

        #b
        renewal_x = account.marginal_surplus(z=2.33, r=symbols('r'), y=0.1, SD_L1=var_xy**0.5, SD_L0=sd_y)
        self.assertAlmostEqual(102, renewal_x, 0)
        renewal_y = account.marginal_surplus(z=2.33, r=symbols('r'), y=0.1, SD_L1=var_xy**0.5, SD_L0=sd_x)
        self.assertAlmostEqual(13, renewal_y, 0)

        #c) State a problem with using the Marginal Surplus method to calculate renewal risk loads.
        #   Individual risk loads will add to less than the total risk load.

        #d
        x = account.shapley(sd_x**2, cov_xy, risk_load/var_xy)        
        self.assertAlmostEqual(123-1, x, 0)
        y = account.shapley(sd_y**2, cov_xy, risk_load/var_xy)
        self.assertAlmostEqual(17,y,0)


    def test_18_fall_2(self):
        prob = np.asarray([.9, .05, .03, .02])
        x = np.asarray([0,500,2000,0])
        y = np.asarray([0,1000,0,3000])
        λ = 0.0001

        #a
        m1 = sum(prob * (x+y))
        m2 = sum(prob * (x+y)**2)
        combined_variance = (m2 - m1**2)
        risk_load = λ*combined_variance
        self.assertAlmostEqual(37.45, risk_load, 2)

        #b
        var_x = sum(prob * x**2) - sum(prob * x)**2
        var_y = sum(prob * y**2) - sum(prob * y)**2

        renewal_risk_load_x = risk_load - λ*var_y
        renewal_risk_load_y = risk_load - λ*var_x

        self.assertAlmostEqual(15.66, renewal_risk_load_x,2)
        self.assertAlmostEqual(24.92, renewal_risk_load_y,2)

        #c
        account = Risk_Load()
        covariance = (combined_variance - var_x - var_y) / 2

        self.assertAlmostEqual(14.09, account.shapley(var_x, covariance, λ) ,2)
        self.assertAlmostEqual(23.36, account.shapley(var_y, covariance, λ), 2)

    def test_18_spring_1(self):
        p = 0.001
        L_1 = 1000000
        L_2 =  500000
        λ_s = 0.025

        #a) build-up risk load
        var_1 = p*(1-p)* L_1**2
        self.assertAlmostEqual(790, var_1**0.5 * λ_s, 0 )

        #b) marginal surplus
        var = p*(1-p)* (L_1 + L_2)**2
        self.assertAlmostEqual(395, var**0.5 * λ_s - 790, 0 )

        #c) variance risk load multiplier
        λ_v = λ_s / var**0.5
        self.assertAlmostEqual(0.5273, λ_v*10**6, 4)

        #d) marginal variance risk load for each contract
        self.assertAlmostEqual(527, λ_v * var_1, 0)
        self.assertAlmostEqual(1185, λ_v * var, 0 )
        self.assertAlmostEqual(658, λ_v * (var - var_1), 0 )

        #e) renewal risk load for each contract
        var_2 = p*(1-p)* L_2**2
        self.assertAlmostEqual(1053+1, λ_v * (var - var_2), 0 )
        self.assertAlmostEqual( 658  , λ_v * (var - var_1), 0 )


    def test_19_spring_1(self):        
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

        d = account.marginal_surplus(z=symbols('z'), y = 0.15, r = b, SD_L1 = S1, SD_L0 = S0 )
        self.assertAlmostEqual(2.985, d, 3)

if __name__ == '__main__':
    unittest.main()
