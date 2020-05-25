# CAS Exam 7
# Marshall et al.
import numpy as np
class AssessingRiskMargins():

    # 1 Introduction

    #   1.2 Current approaches to assessing risk margins
    #       Coefficients of variation
    #       correlation matrix

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


    # 2 The proposed framework

    #   2.2 Sources of uncertainty

        #   Random component of parameter risk
            #       The random component of parameter risk is the extent to which the randomness associated 
            #       with the insurance process compromises the ability to select appropriate parameters.

    #       The random component of parameter risk, 
    #           representing the extent to which the randomness associated with the insurance process 
    #           compromises the ability to select appropriate parameters in the valuation models. 

    #       The random component of process risk 
    #           being the pure effect of the randomness associated with the insurance process. 
    #           Even if the valuation model was perfectly calibrated to reflect expected future outcomes, 
    #           the volatility associated with the insurance process

    #   2.4 Analysing independent risk sources

    #       Approaches that can be used to analyze independent sources of risk.

    #       Mack method
    #       Bootstrapping
    #       Stochastic Chain Ladder
    #       GLM
    #       Bayesian


    #   2.5 Analysing systemic risk sources
    #       Internal systemic risk
    #           Specification Error
    #           Parameter selection error
    #           Data error

    #       External systemic risk
    #           Economic and social risks
    #           Legislative, political risk and claim inflation risks
    #           Claim management process change risk 
    #           Expense risk
    #           Event risk
    #           Latent claim risk
    #           Recovery risk 

    #       Correlation effects
    #           Independent risk 
    #           Internal systemic risk
    #           External systemic risk

    #   2.7. Additional analysis
    
    #       Areas of additional analysis that you may conduct to provide further comfort regarding the outcomes from the deployment of this framework.
                
    #       Sensitivity testing: Vary each assumption to see the effect on risk margins.
    #       Scenario testing: Tie outcomes to a set of valuation outcomes.

    #       Internal benchmarking: For each source of uncertainty compare the coefficients of variation between classes for various liabilities.
    #       External benchmarking: Review differences between benchmarks and the claim portfolio being analyzed.

    #       Hindsight analysis: Compare past estimates against the latest view of the equivalent liabilities.


    # 3 Independent risk assessment


    # 4 Systemic risk assessment

    # 4.1 Internal systemic risk

    #       Specification error - the error that can arise from an inability to build a model that is fully representative of the underlying insurance process. 
    #       
    #       Parameter selection error - the error that can arise because the model is unable to measure all predictors of claim cost outcomes or trends in these predictors.
    #     
    #       Parameter selection error for internal systemic risk
    #           The parameter selection error for internal systemic risk is the error from the model 
    #           being unable to adequately measure all predictors of claim cost outcomes or trends.
            
    #       Data error - the error that can arise due to poor data, unavailability of data and/or inadequate knowledge of the portfolio being analysed.