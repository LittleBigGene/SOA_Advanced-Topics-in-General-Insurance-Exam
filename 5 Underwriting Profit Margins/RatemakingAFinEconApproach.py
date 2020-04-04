class Ratemaking_A_FinEcon_Approach:
    RiskFreeRate = 0
    Beta = 0
    MarketRiskPremium =0 
    Premium=0
    Equity=0
    InvestableAsset=0
    InvestmentReturn=0

    def __init__(self, RiskFreeRate, Beta, MarketRiskPremium, Premium, Equity, InvestableAsset, InvestmentReturn):
        self.RiskFreeRate = RiskFreeRate
        self.Beta = Beta
        self.MarketRiskPremium = MarketRiskPremium
        self.Premium = Premium
        self.Equity = Equity
        self.InvestableAsset = InvestableAsset
        self.InvestmentReturn = InvestmentReturn

    def CAPM_Total_Return(self):
        return self.RiskFreeRate + self.Beta * self.MarketRiskPremium

    def UW_Profit_Margin(self):
        S = self.Equity
        P = self.Premium 
        TRR = self.CAPM_Total_Return() 
        IA = self.InvestableAsset 
        IR = self.InvestmentReturn
               
        return S/P*(TRR-IA/S*IR)

