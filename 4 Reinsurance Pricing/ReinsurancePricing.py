# CAS Exam 8
# Basics of Reinsurance Pricing
# David R. Clark

import numpy as np

class Reinsurance_Pricing:    

    def __init__(self) -> None:
        #IncreasedLimitsFactor
        self.ILF = {}

    # 1. Proportional Treaties
    # Quota Share, Surplus Share

    # 1B a)Slicing Scale Commission      
    def technical_ratio(self, loss_ratio_range, commission_ratio_min, commission_ratio_max, reassume = 1, sliding = 0):        
        tech = []        
        for loss in range(loss_ratio_range[0],loss_ratio_range[1]+1,1):            

            if loss <= commission_ratio_max[1]:
                comm = commission_ratio_max[0]
            elif loss > commission_ratio_min[1] - sliding:
                comm = commission_ratio_min[0]                
            else:
                comm = commission_ratio_min[0] + sliding * (loss - commission_ratio_max[1])
                loss = commission_ratio_max[1] + reassume * (loss - commission_ratio_max[1])

            tech.append( loss + comm)
        # print(tech)
        # print(sum(tech) / len(tech))
        return tech

    # b)Profit Commission
    def profit_commission(self, precentage, loss, margin, annualPrem):
        return max(0, precentage * (annualPrem - margin - loss))

    # c)Loss Corridors
    # The ceding company reassumes a portion of the liability if the loss ratio exceeds a certain amount.

    

    # 2. Property Per Risk Excess Treaties
    # a) Experience Rating
    # b) Exposure Rating
    def risk_exposure_rating(self, limit, retention, insured_value):
            # layer 400 excess of 100 -> limit, retention = 400, 100             
        return self.exposure_curve( (limit + retention) / insured_value ) - self.exposure_curve( retention / insured_value )
        
    def exposure_curve(self, x):
        x = np.clip(x, 0, 1.2)
        return 1 - (1 - x/1.2)**2
        
    # 2B. Other Issues On Property Per Risk Treaties
    # a) Free Cover


    # 3. Casualty Per Occurrence Excess Treaties
    # a) Experience Rating
    # b) Exposure Rating
    def occurrence_exposure_rating(self, underlyingLimit, policyLimit, excessAmt = 1):

        reinsuranceCoverage = self.ILF[policyLimit + underlyingLimit] - self.ILF[underlyingLimit + excessAmt]
        #print(f'Reinsurance Coverage diff = {reinsuranceCoverage}')
         
        policy = self.ILF[policyLimit + underlyingLimit] - self.ILF[underlyingLimit]
        #print(f'policy difference         = {policy}')
      
        return  reinsuranceCoverage / policy
    

    # 3B Special Problems on Casualty Excess Treaties
    # a) Including Umbrella Policies
    # b) Loss Sensitive Features
    def swing_plan (self, maxPremium, minPremium, retro, premium):            
        retroPremium = retro * premium
        if (retroPremium > maxPremium):
            return maxPremium
        if (retroPremium < minPremium):
            return minPremium        
        return retroPremium

    def loss_cost_rate(self, standard_premium_x, standard_premium_y, expected_loss_ratio_x, expected_loss_ratio_y, allocation_x, allocation_y, layer_x, layer_y):

        return (standard_premium_x * expected_loss_ratio_x + standard_premium_y * expected_loss_ratio_y) * (allocation_x * layer_x + allocation_y * layer_y ) 


    # c) Workers Compensation Experience Rating

    # 4. Aggregate Distribution Models
    # a) Empirical Distribution
    # b) Single Distribution Model
    # c) Recursive Calculation of Aggregate Distribution
    # d) Other Collective Risk Models

    # 5. Property Catastrophe Covers
    # 5A. Traditional Products and Methods
    # That is, other reinsurance inures to the benefit of the catastrophe cover.
    
    # 5B. Alternative Risk Products
    def additional_prem(self, precentage, loss, margin, annualPrem ):
        return max(0, precentage * (loss + margin - annualPrem))

    # 6. Calculating the Final Price


if __name__=='__main__':
    treaty = Reinsurance_Pricing()
    treaty.risk_exposure_rating()