import unittest
from sympy import symbols, solve
from AssessingRiskMargins import AssessingRiskMargins

class test_AssessingRiskMargins(unittest.TestCase):

    def test_16_fall_2(self):
        #a) using quantitative methods based on historical data to estimate the correlation among these sources of risk

        # Any three of the following is sufficient to earn full credit.
        #  Commonly used methods are complex and require a lot of data. The benefits may not outweigh the costs.
        #  Correlations are heavily influenced by correlations in past data and may not accurately reflect the true values.
        #  It is difficult to separate past results into independent and systemic components.
        #  Internal systemic risk cannot be modeled using standard correlation modeling techniques.

        #b) propose a numerical value for high correlation
        # 0.5 < pick < 1, author used 0.75

        #c
        ocl, pl = 15/50*8.5, 35/50*6
        cv2_int = ocl**2 + pl**2 + 2*.75*ocl*pl
        self.assertAlmostEqual(cv2_int, 40.2075,4)

        #d) Describe two implications of differing lengths of claim run-off when performing internal benchmarking of independent risk.

        # For outstanding claim liabilities, longer run-off implies higher volatility and hence a higher coefficient of variation. 
        # This is due to more time for random effects to have an impact. 
        # For premium liabilities, long tails imply a higher coefficient of variation relative to outstanding claim liabilities. 
        # This is due to smaller volume.

    def test_16_spring_7(self):
        arm = AssessingRiskMargins()

        sources = [0.06, 0.08, 0.16]
        
        #a        
        combined_coefficient = arm.combined_coefficient_of_variation(sources)
        self.assertAlmostEqual(.1887, combined_coefficient, 4)

        #b
        riskMargin = arm.risk_margin(combined_coefficient, 216 * 10**6 )
        self.assertAlmostEqual(27468734, riskMargin, 0)

        #c) Describe two areas of additional analysis that you may conduct to provide further comfort regarding the outcomes from the deployment of this framework.
        #  Sensitivity testing: Vary each assumption to see the effect on risk margins.
        #  Scenario testing: Tie outcomes to a set of valuation outcomes.
        #  Internal benchmarking: For each source of uncertainty compare the coefficients of variation between classes for various liabilities.
        #  External benchmarking: Review differences between benchmarks and the claim portfolio being analyzed.
        #  Hindsight analysis: Compare past estimates against the latest view of the equivalent liabilities.

        #d) Identify four approaches that can be used to analyze independent sources of risk.
        #  Mack method
        #  Bootstrapping
        #  Stochastic chain ladder
        #  Generalized linear models
        #  Bayesian

        #e  One of the attractions of this framework is that each of the sources of uncertainty being
        #   analyzed can be aligned with the central estimate analysis and appropriate decisions around volatility made in the context of that analysis.
        #   Your actuarial student proposes analyzing risk margins at the same granular level as used for central estimate valuation purposes.

        # Evaluate your student’s proposal.
        # Commentary on Question:
        # Three of the following four statements are sufficient to earn full credit.
        #  May not be possible to work at the granular level
        #  Information may not be credible
        #  May be costly to work at the granular level
        #  Extra detail may not provide material improvement

    def test_17_fall_2(self):
        #a) Describe each of the following sources of risk:
        # Parameter selection error for internal systemic risk
        # Random component of parameter risk

        #b
        arm = AssessingRiskMargins()       
        claim_liabilities = [7500,4000]

        independent_risk = [0.07, 0.1]
        ind_risk_coeff = arm.risk_coefficient_of_variation(independent_risk, claim_liabilities)        
        self.assertAlmostEqual(0.057, ind_risk_coeff, 3)

        internal_systemic_risk = [.06, .09]
        internal_systemic_risk_coeff = arm.risk_coefficient_of_variation(internal_systemic_risk, claim_liabilities, 0.25)        
        self.assertAlmostEqual(0.056, internal_systemic_risk_coeff, 3)

        aggregate = arm.combined_coefficient_of_variation([ind_risk_coeff,internal_systemic_risk_coeff,0.032])

        rm = arm.risk_margin(aggregate, sum(claim_liabilities))
        self.assertAlmostEqual(667+2, rm, 0)

        #c) Your manager also asked you to provide an estimate of the risk margin at the 99.5% adequacy level on the same portfolio.
        #   Explain why using the approach of part (b) may not be appropriate.

        #   Any two of the following were sufficient for full credit.
        #   • The normal distribution may not be appropriate for an extreme percentile.
        #   • The internal systemic risk correlation in the extreme tails may be more than 25%.
        #   • There may be other risk drivers than those used.

    def test_17_spring_2(self):
        # The major challenge for candidates was matching risk indicators to sources of internal systemic risk.
        # Specification error – Risk Indicators 1 and 3 
        # Parameter selection error – Risk Indicators 2 and 6 
        # Data error – Risk Indicators 4 and 5

        Motor_score = 0.3*(3+2)/2 + 0.5*(5+3)/2 + 0.2*(4+7)/2 # 3.85
        Home_score = 0.3*(5+3)/2 + 0.5*(3+4)/2 + 0.2*(4+6)/2 # 3.95
        #Both scores are in the range 3-4 and hence CoV = 8.5% for each.
        CV_m, CV_h = 8.5, 8.5

        CV2 = (2/5*CV_m)**2 + (3/5*CV_h)**2 + 2*0.5*(2/5*CV_m)*(3/5*CV_h)
         
        self.assertAlmostEqual(CV2**.5, 7.41, 2)

    def test_18_fall_6(self):
        pass

    def test_18_spring_3(self):
        CV2_ext = (3/10)**2 * (2**2 + 1**2 + 3**2) + (7/10)**2 * (2**2 + 1**2 + 1**2)
        self.assertAlmostEqual(CV2_ext, 4.2)
        
        CV2, CV2_ind  = 9.6**2, 8**2
        CV2_int = CV2 - CV2_ind -  CV2_ext        
        self.assertAlmostEqual(CV2_int, 23.96)

        v = symbols('v')
        sol = solve((0.7*v)**2 + (.3*3)**2 + 2 * 0.75 * (0.7*v) * (0.3*3) - CV2_int)
        self.assertAlmostEqual(sol[1], 5.9765172)

        #b) approach if external systemic risk are partally correlated
        #c) hindsight analysis
        #d) hindsight analysis for short-tail vs long-tail


    def test_CAS7_19_spring_9(self):
        pass

if __name__ == '__main__':
    unittest.main()
