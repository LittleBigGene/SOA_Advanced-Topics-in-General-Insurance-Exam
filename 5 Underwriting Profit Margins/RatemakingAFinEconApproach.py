# SOA Exam GIADV

class Ratemaking_A_FinEcon_Approach:
    def __init__(self):
        self.RiskFreeRate = 0
        self.Beta = 0
        self.MarketRiskPremium = 0
        self.Premium = 0
        self.Equity = 0
        self.InvestableAsset = 0
        self.InvestmentReturn = 0

    def CAPM_Total_Return(self):
        return self.RiskFreeRate + self.Beta * self.MarketRiskPremium

    def UW_Profit_Margin(self):
        S = self.Equity
        P = self.Premium 
        TRR = self.CAPM_Total_Return() 
        IA = self.InvestableAsset 
        IR = self.InvestmentReturn
               
        return S / P * (TRR - IA / S * IR)

