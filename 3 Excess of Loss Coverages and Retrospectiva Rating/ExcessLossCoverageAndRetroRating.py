# SOA Exam GIADV
# Lee

class Excess_Loss_Coverage_And_RetroRating:
    Layers = []
    ExcessAmounts = []
    Trend = 0
    TrendFactors = []

    def __init__(self, layers, excessAmts, trend):
        self.Layers = layers
        self.ExcessAmounts = excessAmts
        self.Trend = trend
    
    def set_losses_probabilities(self, losses, probabilities):        
        self.TrendFactors = []
        for layer, excess in zip(self.Layers, self.ExcessAmounts):                       
            layerExcessLoss = 0
            trendedLayerExcessLoss = 0
            for loss, prob in zip(losses, probabilities):
                layerExcessLoss += prob * min(max(loss - layer, 0), excess)    
                trendedLayerExcessLoss += prob * min(max(loss * (1 + self.Trend) - layer,0), excess)    
            print(f'Trend Factor {trendedLayerExcessLoss / layerExcessLoss}')
            self.TrendFactors.append(trendedLayerExcessLoss / layerExcessLoss)    
