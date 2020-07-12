# CAS Exam 8
# Basics of Reinsurance Pricing
# David R. Clark

import numpy as np
import pandas as pd

class Reinsurance_Pricing:    

    def __init__(self) -> None:
        #IncreasedLimitsFactor
        self.ILF = {}
        self.mean = 0
        self.variance = 0
        self.AP = 0
        self.Limit = 0
    # 1. Proportional Treaties
    # Quota Share, Surplus Share

    def surplus_share(self, insuredValue, loss, retained, limit):
        surplus = (insuredValue - retained).clip(0, limit)
        cededPct = surplus / insuredValue
        cededLoss = cededPct * loss
        return cededLoss

    # 1B a)Slicing Scale Commission      
    def technical_ratio(self, loss_ratio_range, commission_ratio_min, commission_ratio_max, reassume = 1, sliding = 0, carryforward = 0, show=False):        
        tech = []        
        for loss in range(loss_ratio_range[0]     + carryforward
                        , loss_ratio_range[1] + 1 + carryforward , 1 ):            

            if loss <= commission_ratio_max[1]:
                comm = commission_ratio_max[0]
            elif loss > commission_ratio_min[1] - sliding:
                comm = commission_ratio_min[0]                
            else:
                comm = commission_ratio_max[0] - sliding * (loss - commission_ratio_max[1])
                loss = commission_ratio_max[1] + reassume * (loss - commission_ratio_max[1])

            if show:
                print(f'loss:{loss} comm:{comm}')

            tech.append( loss + comm)
        # print(tech)
        # print(sum(tech) / len(tech))
        return tech
    
    # b)Profit Commission
    def profit_commission(self, percentage, loss, margin, annualPrem):
        return max(0, percentage * (annualPrem - margin - loss))

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

    def occurrence_experience_rating(self, experience, layer, excessOf, trend, policeLimit, valYear):        
        pd.options.display.max_columns = None        
        exp = pd.DataFrame(data=experience)

        exp['Trended Loss'] = exp['Untrended Loss'] * trend**(valYear-exp['Accident Date'])
        exp['Trended ALAE'] = exp['Untrended ALAE'] * trend**(valYear-exp['Accident Date'])
        exp['Trended Loss'] = np.where(exp['Trended Loss']>policeLimit, policeLimit, exp['Trended Loss'])
        
        exp['Layer Loss'] = np.where(exp['Trended Loss']>excessOf, exp['Trended Loss']-excessOf , 0)
        exp['Layer Loss'] = np.where(exp['Layer Loss'] >layer, layer, exp['Layer Loss'] )

        exp['Layer ALAE'] = exp['Trended ALAE'] / exp['Trended Loss'] * exp['Layer Loss'] 
        exp['Layer Loss+ALAE'] = exp['Layer ALAE'] + exp['Layer Loss']

        return exp[exp['Layer Loss']>0]



    # b) Exposure Rating
    def occurrence_exposure_rating(self, underlyingLimit, policyLimit, ϕ = 0 , show = False):
        ul         = self.ILF[underlyingLimit]
        ul_pl      = self.ILF[underlyingLimit + policyLimit]        
        ul_ap      = self.ILF[underlyingLimit + self.AP ]
        ul_ap_lim  = self.ILF[underlyingLimit + self.AP + self.Limit  ]

        reinsurance = (min(ul_pl,ul_ap_lim) - min(ul_pl,ul_ap)) * (1-ϕ)
        underlying  = (ul_pl - ul) * (1-ϕ)

        pl = self.ILF[policyLimit]     
        UL_less_Excess = 0
        if ϕ > 0 :
            UL_less_Excess = self.ILF[underlyingLimit - self.AP]
            reinsurance += (ul - UL_less_Excess) * ϕ
            underlying  += (pl - 0             ) * ϕ

        if show:
            print(f'({min(ul_pl,ul_ap_lim)}-{min(ul_pl,ul_ap)})({1-ϕ}) + ({ul} - {UL_less_Excess})({ϕ})')
            print(f'over ({ul_pl}-{ul})({1-ϕ}) + ({pl} - {0})({ϕ})')
        return  reinsurance / underlying
    

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
   

    # c) Workers Compensation Experience Rating

    # 4. Aggregate Distribution Models
    # a) Empirical Distribution
    # b) Single Distribution Model
    # c) Recursive Calculation of Aggregate Distribution
    def aggregate_loss_probability(self, S, A, k, show=False):

        a = 0        
        for i in range(1, min(len(S), k+1)):                        
            a += self.mean / k * i * A[k-i] * S[i]
            if show:
                print(f'i {i} k {k}; {self.mean} / {k} * {i} * {A[k-i]} * {S[i]}')
            
        return a 

        # Text Book Example
        # treaty = Reinsurance_Pricing()
        # treaty.mean = 3
        # S = [0, .4, .15, .1, .35]
        # A = [.05, 0.06, 0.059, 0.057, 0.096, 0.094]
        # p = treaty.aggregate_loss_probability(S,A,6, show=True)
        # print(p)

    def moment_of_loss(self, loss_size_probability):
        first_m, second_m = 0,0
        for s in range(1,len(loss_size_probability)):
            first_m  += loss_size_probability[s] * s 
            second_m += loss_size_probability[s] * s**2
        return [first_m, second_m]
    
    # d) Other Collective Risk Models

    # 5. Property Catastrophe Covers
    # 5A. Traditional Products and Methods
    # That is, other reinsurance inures to the benefit of the catastrophe cover.
    


    # 5B. Alternative Risk Products
    def additional_prem(self, percentage, loss, margin, annualPrem ):
        return max(0, percentage * (loss + margin - annualPrem))

    # 6. Calculating the Final Price

if __name__=='__main__':
    pass

