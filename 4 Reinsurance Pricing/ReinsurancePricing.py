# CAS Exam 8
# Basics of Reinsurance Pricing
# David R. Clark

class Reinsurance_Pricing:
    IncreasedLimitsFactor = {}

    def __init__(self, ilf = None) -> None:
        self.IncreasedLimitsFactor = ilf

    def exposure_rating(self, underlyingLimit, policyLimit, IncreasedLimitsFactor, excessAmt = 1):

        reinsuranceCoverage = IncreasedLimitsFactor[policyLimit + underlyingLimit] - IncreasedLimitsFactor[underlyingLimit + excessAmt]
        #print(f'Reinsurance Coverage diff = {reinsuranceCoverage}')
         
        policy = IncreasedLimitsFactor[policyLimit + underlyingLimit] - IncreasedLimitsFactor[underlyingLimit]
        #print(f'policy difference         = {policy}')
      
        return  reinsuranceCoverage / policy
    
    def swing_plan (self, maxPremium, minPremium, retro, premium):
        retroPremium = retro * premium

        if (retroPremium > maxPremium):
            return maxPremium
        if (retroPremium < minPremium):
            return minPremium
        
        return retroPremium

    def additional_prem(self, precentage, loss, margin, annualPrem ):
        return max(0, precentage * (loss + margin - annualPrem))

    def profit_commission(self, precentage, loss, margin, annualPrem):
        return max(0, precentage * (annualPrem - margin - loss))

    def loss_cost_rate(self, standard_premium_x, standard_premium_y, expected_loss_ratio_x, expected_loss_ratio_y, allocation_x, allocation_y, layer_x, layer_y):

        return (standard_premium_x * expected_loss_ratio_x + standard_premium_y * expected_loss_ratio_y) * (allocation_x * layer_x + allocation_y * layer_y ) 
        