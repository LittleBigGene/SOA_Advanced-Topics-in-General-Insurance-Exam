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

    #   Assumptions of the Captial Asset Pricing Model
    #   • Investors are risk averse diversifiers who try to maximize expected return and minimize risk.
    #   • Investors are price takers, in that they act as if their trades have no effect on asset prices.
    #   • Investors have identical expectations about asset expected returns and standard deviations.
    #   • Investors have no transaction costs or taxes.
    #   • Investors can borrow or invest at the risk-free rate without any limit.
    #   • Assets are infinitely divisible.

    # 4 Application of the CAPM to Insurance
    # k, the funds generating coefficient estimate
    def Fairley_CAPM(self, UPM, k, risk_free, uw_beta, market_risk_premium, tax = [0,0], equity_to_premium = 1):
        sol = solve(
            - k                 * risk_free *(1-tax[0])/(1-tax[1]) 
            + equity_to_premium * risk_free *   tax[0] /(1-tax[1]) 
            + uw_beta * market_risk_premium 
            - UPM
            )
        return sol[0] 

    # 5 Discounted Cash Flow Analysis

    # 6 Discounted Cash Flow Models Applied to Insurance

    def Risk_Adjusted_Discount_Technique(self, premium, risk_free, losses, risk_adj_loss, expense, uw_loss, invest_income, tax, show=False):                
        asset_discount = 1 /(1 + risk_free)
        loss_discount = 1 /( 1 + risk_adj_loss)

        #  L  Losses and LAE
        pv_L, n = 0, 0
        for loss in losses:
            pv_L += loss * loss_discount ** n
            n += 1

        #   E   Underwriting Expenses        
        pv_E = expense

        #  TII Taxes on Investment Income
        pv_TII, n = 0, 0
        for income in invest_income:
            pv_TII += income * risk_free * tax * asset_discount ** n
            n += 1
        
        #  TUW Taxes on Underwriting Profit or Loss
        pv_TUW = (premium - expense) * tax * asset_discount + uw_loss * tax * loss_discount

        if show:
            print(f'Premium {premium} \n pv_L {pv_L} \n pv_E {pv_E} \n pv_TUW {pv_TUW} \n pv_TII {pv_TII}')
        # premium =  pv_L + pv_E + pv_TUW + pv_TII                
        sol = solve(pv_L + pv_E + pv_TUW + pv_TII - premium)
        return sol[0] 

        # Criticisms of the Risk Adjusted Discounted Technique as applied to insurance models.
        
        #   • The risk-free rate may not be the correct rate to use.
        #   • It is not clear how to set the risk-adjusted rate.
        #   • It is difficult to allocate equity to policies.
        #   • It considers only one policy term, not renewal cycles.
        #   • Actual taxes may not be at the corporate rate.
        #   • Expenses may depend on the premium rate.
    
    # Syllabbi Excluds Section 7 & 8
    # 7 Option Pricing
    # 8 Application of Option Pricing Models to Pricing Insurance

    # 9 Conclusion