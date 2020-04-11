import unittest
from ExcessLossCoverageAndRetroRating import Excess_Loss_Coverage_And_RetroRating

class test_ExcessLossCoverageAndRetroRating(unittest.TestCase):
    def test_spring_19_6(self):
        coverage = Excess_Loss_Coverage_And_RetroRating()
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

    def test_fall_16_3(self):
        pass

    def test_spring_16_6(self):
        retro = Excess_Loss_Coverage_And_RetroRating()

        #a) define Table M in a retro rating plan

        #b
        retro.Table_M_Loss_Ratios = [.3,.4,.5,.6,.7]

        r = 0
        self.assertAlmostEqual(1,retro.Φ(r))
        self.assertAlmostEqual(0,retro.Ψ(r))

        r = 0.4
        self.assertAlmostEqual(0.6, retro.Φ(r))
        self.assertAlmostEqual(0 , retro.Ψ(r))
        
        r = 0.8
        self.assertAlmostEqual(0.24, retro.Φ(r))
        self.assertAlmostEqual(0.04, retro.Ψ(r))
        
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

        
if __name__ == '__main__':
    unittest.main()