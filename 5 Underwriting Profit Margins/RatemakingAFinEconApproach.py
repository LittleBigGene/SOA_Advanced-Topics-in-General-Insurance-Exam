# SOA Exam GIADV

from sympy import solve

class Ratemaking_A_FinEcon_Approach:
    # 1 Introduction to Financial Economics
    def CAPM_Total_Return(self, exp_return, risk_free, beta, market_risk_premium):
        # beta of security i = Cov(R_i, R_m) / Var(R_m)

        sol = solve(risk_free + beta * market_risk_premium - exp_return)
        return sol[0] 

    # 2 Target Total Rate of Return Model
        
    # P Premium, S Equity, L Losses, E Expenses    
    # IA Investable Asset, IR Investment Return
    # TRR Target Total Rate of Return
    # UPM Underwriting Profit Margin

    def Target_Total_Rate_of_Return(self, P, S, E, L, IR, TRR, showWork = False):
        IA = (P + S - E)
        UPM = (P - E - L) / P

        if showWork:
            print(f'P {P} \n UPM {UPM} \n S {S} \n IA {IA} \n Ex {E}')
        
        return self.Target_Total_Rate_of_Return_1(P, S, UPM, IA, IR, TRR)

    def Target_Total_Rate_of_Return_1(self, P, S, UPM, IA, IR, TRR):        
        # TRR =      (IA / S) * IR + (P / S) * UPM        
        sol = solve((IA / S) * IR + (P / S) * UPM - TRR)
        return sol[0] 


    # 3 Capital Asset Pricing Model

    #   Two      Asset Allocation Case - simply a weighted average of each asset's expected return
    #   Multiple Asset Allocation Case

    #   Efficient Frontier

    #   Some cautions about using the CAPM must be mentioned
    #   The model requires theuse of the market risk premium and past market portfolio returns and individual asset returns to arrive at beta estimatesfor individual assets
    #   This assumesthat such relationshipsare stable, when in fact they are likely to changeover time. 


    # 4 Application of the CAPM to Insurance
    # k, the funds generating coefficient estimate
    def CAPM_UPM(self, UPM, k, risk_free, uw_beta, market_risk_premium):

        sol = solve(-k * risk_free + uw_beta * market_risk_premium - UPM)
        return sol[0] 

    # 5 Discounted Cash Flow Analysis

    # 6 Discounted Cash Flow Models Applied to Insurance

    def Risk_Adjusted_Discount_Technique(self, premium, risk_free, losses, risk_adj_loss, expense, uw_pl, invest_income, tax):                
        asset_discount = 1 /(1 + risk_free)
        loss_discount = 1 /( 1 + risk_adj_loss)

        #  L  Losses and LAE
        pv_L, n = 0, 0
        for loss in losses:
            pv_L += loss * loss_discount  ** n
            n += 1

        #   E   Underwriting Expenses        
        pv_E = expense

        #  TII Taxes on Investment Income
        pv_TII, n = 0, 0
        for income in invest_income:
            pv_TII += income * risk_free * tax * asset_discount ** n
            n += 1
        
        #  TUW Taxes on Underwriting Profit or Loss
        pv_TUW = (premium - expense) * tax * asset_discount - uw_pl * tax * loss_discount

        #print(f'Premium {premium} \n pv_L {pv_L} \n pv_E {pv_E} \n pv_TUW {pv_TUW} \n pv_TII {pv_TII}')
        # premium =  pv_L + pv_E + pv_TUW + pv_TII                
        sol = solve(pv_L + pv_E + pv_TUW + pv_TII - premium)
        return sol[0] 
    # 7 Option Pricing

    # 8 Application of Option Pricing Models to Pricing Insurance

    # 9 Conclusion