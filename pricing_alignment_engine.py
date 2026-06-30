# Q3 Pricing Alignment Engine
# Competitive pricing strategy and alignment optimization

import pandas as pd
import numpy as np
from datetime import datetime

class PricingAlignmentEngine:
    def __init__(self):
        self.q3_price_min = 4.29
        self.q3_price_max = 389.95
        self.q3_price_avg = 85.40
        self.tier_gap_target = 0.20  # 20% target gap between tiers
    
    def load_pricing_data(self, filepath):
        '''Load Q3 pricing alignment data'''
        df = pd.read_excel(filepath)
        return df
    
    def normalize_q3_pricing(self, pricing_data):
        '''Normalize Q3-PriceAlign-2026 values for consistency'''
        pricing_data['q3_normalized'] = (pricing_data['Q3-PriceAlign-2026'] - self.q3_price_min) / (self.q3_price_max - self.q3_price_min)
        return pricing_data
    
    def calculate_cost_impact(self, pricing_data):
        '''Calculate cost move impact on pricing'''
        pricing_data['cost_impact_pct'] = (pricing_data['Cost Move,'] / pricing_data['Q3-PriceAlign-2026']) * 100
        return pricing_data
    
    def analyze_tier_gaps(self, pricing_data):
        '''Analyze price gaps between tiers (Good/Better/Best)'''
        tier_analysis = {}
        for tier in pricing_data['Good/better/best'].unique():
            tier_prices = pricing_data[pricing_data['Good/better/best'] == tier]['Q3-PriceAlign-2026']
            tier_analysis[tier] = {
                'avg_price': tier_prices.mean(),
                'min_price': tier_prices.min(),
                'max_price': tier_prices.max(),
                'count': len(tier_prices)
            }
        return tier_analysis
    
    def optimize_tier_positioning(self, tier_analysis):
        '''Optimize tier positioning with target gaps'''
        optimized = {}
        tiers_sorted = sorted(tier_analysis.items(), key=lambda x: x[1]['avg_price'])
        
        for i, (tier, data) in enumerate(tiers_sorted):
            if i == 0:
                optimized[tier] = {'target_price': data['avg_price'], 'position': 'Entry'}
            elif i == 1:
                base_price = tiers_sorted[0][1]['avg_price']
                optimized[tier] = {
                    'target_price': base_price * (1 + self.tier_gap_target),
                    'position': 'Mid-tier'
                }
            else:
                base_price = tiers_sorted[0][1]['avg_price']
                optimized[tier] = {
                    'target_price': base_price * (1 + 2 * self.tier_gap_target),
                    'position': 'Premium'
                }
        
        return optimized
    
    def calculate_margin_impact(self, original_price, new_price, cost_basis=0.40):
        '''Calculate margin impact of price change'''
        original_margin = (original_price - (original_price * cost_basis)) / original_price
        new_margin = (new_price - (new_price * cost_basis)) / new_price
        margin_change = ((new_margin - original_margin) / original_margin) * 100
        return {'original_margin_pct': original_margin * 100, 'new_margin_pct': new_margin * 100, 'change_pct': margin_change}
    
    def alignment_quality_score(self, pricing_data):
        '''Score pricing alignment quality (0-100)'''
        tier_gaps = self.analyze_tier_gaps(pricing_data)
        gap_variance = 0
        for tier_data in tier_gaps.values():
            gap_variance += abs((tier_data['avg_price'] - self.q3_price_avg) / self.q3_price_avg)
        
        # 0-100 score (lower variance = higher score)
        score = max(0, 100 - (gap_variance * 50))
        return round(score, 1)

if __name__ == "__main__":
    engine = PricingAlignmentEngine()
    print("Q3 Pricing Alignment Engine v1.0 initialized")
    print("Q3 Price Range: 4.29-389.95 | Tier Gap Target: 20%")
