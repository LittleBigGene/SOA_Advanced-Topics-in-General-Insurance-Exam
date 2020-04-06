# CAS Exam 8
# Basics of Reinsurance Pricing
# David R. Clark

class Reinsurance_Pricing:    

    def __init__(self) -> None:
        #IncreasedLimitsFactor
        self.ILF = {}

    def exposure_rating(self, underlyingLimit, policyLimit, excessAmt = 1):

        reinsuranceCoverage = self.ILF[policyLimit + underlyingLimit] - self.ILF[underlyingLimit + excessAmt]
        #print(f'Reinsurance Coverage diff = {reinsuranceCoverage}')
         
        policy = self.ILF[policyLimit + underlyingLimit] - self.ILF[underlyingLimit]
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

if __name__=='__main__':
    treaty = Reinsurance_Pricing()