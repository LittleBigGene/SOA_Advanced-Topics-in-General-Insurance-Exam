# SOA Exam GIADV
# Lee
from sympy import symbols, solve
import numpy as np
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
        self.Loss_Ratios = np.array
    
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
        expected_excess = r * self.Loss_Ratios.mean()
        excess = (self.Loss_Ratios - expected_excess).clip(0,1)            
        return excess.mean() / self.Loss_Ratios.mean()

    # Table M saving: The average amount by which a risk’s actual loss falls short of r times its expected loss, divided by its expected loss
    def Ψ(self, r):               
        expected_excess = r * self.Loss_Ratios.mean()
        saving = (expected_excess - self.Loss_Ratios).clip(0,1)            
        return saving.mean() / self.Loss_Ratios.mean()

    # Table L charge: The average amount by which a risk’s actual limited loss exceeds r times its expected loss, divided by its expected loss
    def Φ_Limited(self, r, loss_elimination_ratio):
        avg_loss_ratio = self.Loss_Ratios.mean() / (1 - loss_elimination_ratio)
        expected_excess = r * avg_loss_ratio

        excess = (self.Loss_Ratios - expected_excess).clip(0,1)               
        return excess.mean() / avg_loss_ratio + loss_elimination_ratio

    # Table L saving: The average amount by which a risk’s actual limited loss falls short of r times its expected loss, divided by its expected loss
    def Ψ_Limited(self, r, loss_elimination_ratio):
        avg_loss_ratio = self.Loss_Ratios.mean() / (1 - loss_elimination_ratio  )
        expected_excess = r * avg_loss_ratio

        saving = (expected_excess - self.Loss_Ratios).clip(0,1)              
        return saving.mean() / avg_loss_ratio 

    
    def workers_compensation_retro_rating(self):
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