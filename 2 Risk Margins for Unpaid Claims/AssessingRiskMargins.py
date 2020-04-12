# CAS Exam 7
# Marshall et al.
import numpy as np
class AssessingRiskMargins():

    def risk_margin(self, coefficient_of_variation, claim_liabilities, z_75th = 0.674 ):
        return coefficient_of_variation * claim_liabilities * z_75th

    def combined_coefficient_of_variation(self, sources):
        combined = 0
        for source in sources:
            combined += source ** 2
        
        return combined ** 0.5

    def risk_coefficient_of_variation(self, risks, claim_liabilities, corr = 0):
        combined = 0
        total_liab = sum(claim_liabilities)
        for risk, liab in zip(risks, claim_liabilities):
            combined += (risk * liab / total_liab) ** 2
        
        # covariance
        combined += 2 * corr * np.prod(risks) * np.prod(claim_liabilities) / (total_liab ** 2)
        
        return combined ** .5

    # two areas of additional analysis that you may conduct to provide further comfort regarding the outcomes from the deployment of this framework.
                
        #  Sensitivity testing: Vary each assumption to see the effect on risk margins.
        #  Scenario testing: Tie outcomes to a set of valuation outcomes.
        #  Internal benchmarking: For each source of uncertainty compare the coefficients of variation between classes for various liabilities.
        #  External benchmarking: Review differences between benchmarks and the claim portfolio being analyzed.
        #  Hindsight analysis: Compare past estimates against the latest view of the equivalent liabilities.

    #four approaches that can be used to analyze independent sources of risk.
                
        #  Mack method
        #  Bootstrapping
        #  Stochastic chain ladder
        #  Generalized linear models
        #  Bayesian

    # Parameter selection error for internal systemic risk
    #   The parameter selection error for internal systemic risk is the error from the model 
    #   being unable to adequately measure all predictors of claim cost outcomes or trends.
    
    # Random component of parameter risk
    #   The random component of parameter risk is the extent to which the randomness associated 
    #   with the insurance process compromises the ability to select appropriate parameters.