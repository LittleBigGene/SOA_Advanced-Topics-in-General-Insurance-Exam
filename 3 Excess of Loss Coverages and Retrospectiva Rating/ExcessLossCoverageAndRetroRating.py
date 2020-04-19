# SOA Exam GIADV
# Lee

class Excess_Loss_Coverage_And_RetroRating:
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

    # 5 Conclusion