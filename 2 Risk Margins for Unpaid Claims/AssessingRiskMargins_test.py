import unittest
from AssessingRiskMargins import AssessingRiskMargins

class test_AssessingRiskMargins(unittest.TestCase):

    def test_fall_16_2(self):
        pass

    def test_spring_16_7(self):
        arm = AssessingRiskMargins()

        sources = [0.06, 0.08, 0.16]
        
        #a        
        combined_coefficient = arm.combined_coefficient_of_variation(sources)
        self.assertAlmostEqual(.1887, combined_coefficient, 4)

        #b
        riskMargin = arm.risk_margin(combined_coefficient, 216 * 10**6 )
        self.assertAlmostEqual(27468734, riskMargin, 0)

        #c) Describe two areas of additional analysis that you may conduct to provide further comfort regarding the outcomes from the deployment of this framework.

        #d) Identify four approaches that can be used to analyze independent sources of risk.

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

    def test_fall_17_2(self):
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

    def test_spring_17_2(self):
        pass


if __name__ == '__main__':
    unittest.main()
