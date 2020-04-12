import unittest
from AssessingRiskMargins import AssessingRiskMargins

class test_AssessingRiskMargins(unittest.TestCase):

    def test_fall_16_2(self):
        pass

    def test_spring_16_7(self):
        uncertainties = [0.06, 0.08, 0.16]

        #a        
        combined = 0
        for source in uncertainties:
            combined += source ** 2
        
        combined_coefficient = combined ** 0.5
        self.assertAlmostEqual(.1887, combined_coefficient, 4)

        #b
        riskMargin = combined_coefficient * 216 * 10**6 * .674
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

if __name__ == '__main__':
    unittest.main()
