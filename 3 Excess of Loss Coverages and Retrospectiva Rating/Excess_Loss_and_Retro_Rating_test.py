import unittest
import numpy as np
from Excess_Loss_and_Retro_Rating import Excess_Loss_and_Retro_Rating

class test_ExcessLossCoverageAndRetroRating(unittest.TestCase):
    def test_19_spring_6(self):
        coverage = Excess_Loss_and_Retro_Rating()
        coverage.Layers = [0,100,200]
        coverage.ExcessAmounts = [100,100,999]
        coverage.Trend = 0.1
        
        coverage.set_losses_probabilities([150, 250], [0.5,0.5])        
        self.assertLess(coverage.TrendFactors[0],coverage.TrendFactors[1])
        self.assertLess(coverage.TrendFactors[1],coverage.TrendFactors[2])

        coverage.set_losses_probabilities([100, 250], [0.9,0.1])        
        self.assertLess(coverage.TrendFactors[0],coverage.TrendFactors[2])
        self.assertLess(coverage.TrendFactors[2],coverage.TrendFactors[1])
        
        coverage.set_losses_probabilities([25, 250], [0.8,0.2])        
        self.assertLess(coverage.TrendFactors[1],coverage.TrendFactors[0])
        self.assertLess(coverage.TrendFactors[0],coverage.TrendFactors[2])

    def test_16_fall_3(self):
        #intergal (1 - 1/10 * x) from 2 to 10 = 3.2
        #intergal (1 - 1/15 * x) from 2 to 10 = 4.8
        pass

    def test_16_spring_6(self):
        retro = Excess_Loss_and_Retro_Rating()

        #a) define Table M in a retro rating plan

        #b
        retro.Loss_Ratios = np.array([.3,.4,.5,.6,.7])

        r = 0
        self.assertAlmostEqual(1,retro.Φ(r))
        self.assertAlmostEqual(0,retro.Ψ(r))

        r = 0.4
        self.assertAlmostEqual(0.6, retro.Φ(r))
        self.assertAlmostEqual(0 , retro.Ψ(r))
        
        r = 0.8
        self.assertAlmostEqual(0.24, retro.Φ(r))
        self.assertAlmostEqual(0.04, retro.Ψ(r))
        
        r = 1
        self.assertAlmostEqual(0.12, retro.Φ(r))
        self.assertAlmostEqual(0.12, retro.Ψ(r))
                
        r = 1.2 
        self.assertAlmostEqual(0.04, retro.Φ(r))
        self.assertAlmostEqual(0.24, retro.Ψ(r))

        r = 1.6
        self.assertAlmostEqual( 0 , retro.Φ(r))
        self.assertAlmostEqual(0.6 , retro.Ψ(r))

        r = 2
        self.assertAlmostEqual( 0 ,retro.Φ(r))
        self.assertAlmostEqual( 1 , retro.Ψ(r))

        #c) Explain how Table L differs from Table M.
        # Table L incorporates a per accident limit on losses.

    def test_17_fall_7(self):
        pass

    def test_17_spring_7(self):
        # a) b + C(E - I) = e + E
        # b) H = b + C * E * r_H 
        # c) G = b + C * E * r_G 
        # d) I = E [φ(r_G) - ψ(r_H)]
        pass
    
    def test_18_fall_7(self):
        retro = Excess_Loss_and_Retro_Rating()

        #a) define Table L in a retro rating plan

        #b
        retro.Loss_Ratios = np.array([.2, .3, .4, .5, .6])

        r = 0.6
        self.assertAlmostEqual(0.44,retro.Φ_Limited(r, 0.2))
        self.assertAlmostEqual(0.04,retro.Ψ_Limited(r, 0.2))

        r = 0.8
        self.assertAlmostEqual(0.32,retro.Φ_Limited(r, 0.2))
        self.assertAlmostEqual(0.12,retro.Ψ_Limited(r, 0.2))
       


if __name__ == '__main__':
    unittest.main()