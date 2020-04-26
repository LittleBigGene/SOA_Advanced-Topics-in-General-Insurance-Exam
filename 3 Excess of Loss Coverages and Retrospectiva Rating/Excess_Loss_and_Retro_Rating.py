# SOA Exam GIADV
# Lee
from sympy import symbols, solve

class Excess_Loss_and_Retro_Rating:
    # 1 Introduction
    #   Size and Layer
    #   G(x) = 1 - F(x)

    # 2 Expected Value Premium
    #   Increased Limits Coverage
    #   Excess of Loss Coverage
    #   Losses with Retention and Limit
    
    # 3 Trend
    #   Effect of Inflation

    def __init__(self):       
        self.Layers = []
        self.ExcessAmounts = []    
        self.Trend = 0
        self.TrendFactors = []
        self.Table_M_Loss_Ratios = []
    
    def set_losses_probabilities(self, losses, probabilities):        
        self.TrendFactors = []
        for layer, excess in zip(self.Layers, self.ExcessAmounts):                       
            layerExcessLoss = 0
            trendedLayerExcessLoss = 0
            for loss, prob in zip(losses, probabilities):
                layerExcessLoss += prob * min(max(loss - layer, 0), excess)    
                trendedLayerExcessLoss += prob * min(max(loss * (1 + self.Trend) - layer,0), excess)    
            #print(f'Trend Factor {trendedLayerExcessLoss / layerExcessLoss}')
            self.TrendFactors.append(trendedLayerExcessLoss / layerExcessLoss)    

    # The entry ratio: The multiple of a risk’s expected loss or expected loss ratio


    # 4 Retrospective Rating
    # Table M charge: The average amount by which a risk’s actual loss exceeds r times its expected loss, divided by its expected loss
    def Φ(self, r):
        avg_loss_ratio = sum(self.Table_M_Loss_Ratios) / len(self.Table_M_Loss_Ratios)
        expected_excess = r * avg_loss_ratio

        excess = 0
        for loss in self.Table_M_Loss_Ratios:
            if loss > expected_excess:
                excess += loss - expected_excess
            
        return excess / len(self.Table_M_Loss_Ratios) / avg_loss_ratio

    # Table M saving: The average amount by which a risk’s actual loss falls short of r times its expected loss, divided by its expected loss
    def Ψ(self, r):
        avg_loss_ratio = sum(self.Table_M_Loss_Ratios) / len(self.Table_M_Loss_Ratios)
        expected_excess = r * avg_loss_ratio

        saving = 0
        for loss in self.Table_M_Loss_Ratios:
            if loss < expected_excess:
                saving += expected_excess - loss
            
        return saving / len(self.Table_M_Loss_Ratios) / avg_loss_ratio

    
    def retro_rating(self):
        b = symbols('basic premium')        
        B = symbols('basic premium ratio')
        P = symbols('premium')

        b = B * P
                
        R = symbols('retro rating')
        C = symbols('loss conversion factor (LCF)')
        L = symbols('loss')

        R = b + C * L

        G = symbols('max premium')
        H = symbols('min premium')
        E = symbols('expected loss')
        L_G = symbols('max loss')
        L_H = symbols('min loss')

        G = b + C * L_G
        r_G = L_G / E

        H = b + C * L_H
        r_H = L_H / E

        I = symbols('the net insurance chart of Table M')
        
    
    # 5 Conclusion