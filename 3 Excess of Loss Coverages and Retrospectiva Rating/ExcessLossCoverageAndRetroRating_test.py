import unittest
from ExcessLossCoverageAndRetroRating import Excess_Loss_Coverage_And_RetroRating

class test_ExcessLossCoverageAndRetroRating(unittest.TestCase):
    def test_spring_19_6(self):
        coverage = Excess_Loss_Coverage_And_RetroRating([0,100,200], [100,100,999], 0.1)
        
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

if __name__ == '__main__':
    unittest.main()