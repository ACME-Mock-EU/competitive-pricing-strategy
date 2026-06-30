# Pricing Approval Workflow & Governance
# Multi-level approval routing and pricing decision governance

import pandas as pd
from datetime import datetime, timedelta

class PricingApprovalWorkflow:
    def __init__(self):
        self.approvers = {
            'Sofia Nguyen': {'level': 1, 'title': 'Pricing Manager'},
            'Morgan Alvarez': {'level': 2, 'title': 'Pricing Director'},
            'Priya Desai': {'level': 3, 'title': 'VP Revenue'},
            'Renee Caldwell': {'level': 4, 'title': 'CFO/Executive'}
        }
        self.approval_thresholds = {
            'level_1': 50,      # < 50 price points
            'level_2': 150,     # 50-150 price points
            'level_3': 500,     # 150-500 price points
            'level_4': float('inf')  # > 500 price points
        }
    
    def route_for_approval(self, pricing_decision):
        '''Route pricing decision to appropriate approval level'''
        price = pricing_decision['Q3-PriceAlign-2026']
        cost_move = pricing_decision['Cost Move,']
        margin_impact_pct = (cost_move / price) * 100 if price > 0 else 0
        
        # Determine approval level based on price and margin impact
        if price < self.approval_thresholds['level_1'] and abs(margin_impact_pct) < 5:
            approval_level = 1
        elif price < self.approval_thresholds['level_2'] and abs(margin_impact_pct) < 10:
            approval_level = 2
        elif price < self.approval_thresholds['level_3'] and abs(margin_impact_pct) < 15:
            approval_level = 3
        else:
            approval_level = 4
        
        # Find appropriate approver
        approvers_list = sorted(self.approvers.items(), key=lambda x: x[1]['level'])
        selected_approver = [a for a in approvers_list if a[1]['level'] >= approval_level][0]
        
        return {
            'pricing_decision': pricing_decision,
            'approval_level': approval_level,
            'assigned_to': selected_approver[0],
            'approver_title': selected_approver[1]['title'],
            'reason_code': pricing_decision.get('Reason Code', 'UNKNOWN'),
            'status': 'Pending Approval',
            'created_at': datetime.now().isoformat(),
            'due_date': (datetime.now() + timedelta(days=2)).isoformat()
        }
    
    def track_approval_status(self, approval_request, status, notes=None):
        '''Track approval status updates'''
        approval_update = {
            'approval_id': approval_request.get('approval_id'),
            'pricing_id': approval_request['pricing_decision'].get('Distributor A Quote'),
            'assigned_to': approval_request['assigned_to'],
            'status': status,  # Pending, Approved, Denied, Needs Review
            'notes': notes,
            'updated_at': datetime.now().isoformat()
        }
        return approval_update
    
    def approval_analytics(self, approval_history):
        '''Generate approval workflow analytics'''
        total = len(approval_history)
        approved = len([a for a in approval_history if a['status'] == 'Approved'])
        denied = len([a for a in approval_history if a['status'] == 'Denied'])
        pending = len([a for a in approval_history if a['status'] == 'Pending Approval'])
        
        analytics = {
            'total_decisions': total,
            'approved': approved,
            'denied': denied,
            'pending': pending,
            'approval_rate': (approved / total * 100) if total > 0 else 0,
            'denial_rate': (denied / total * 100) if total > 0 else 0,
            'approvers_distribution': {}
        }
        
        for approver in self.approvers:
            approver_decisions = [a for a in approval_history if a['assigned_to'] == approver]
            analytics['approvers_distribution'][approver] = len(approver_decisions)
        
        return analytics
    
    def reason_code_routing(self, reason_code):
        '''Route based on reason code for additional context'''
        routing_rules = {
            'PRC': {'priority': 'medium', 'escalate_if': 'cost_move > 20'},
            'SKU': {'priority': 'low', 'escalate_if': 'margin_impact > 10'},
            'CMP': {'priority': 'medium', 'escalate_if': 'campaign_conflict'},
            'MAP': {'priority': 'high', 'escalate_if': 'violation_risk'},
            'CST': {'priority': 'medium', 'escalate_if': 'cost_change > 15'}
        }
        return routing_rules.get(reason_code, {'priority': 'medium', 'escalate_if': 'none'})

if __name__ == "__main__":
    workflow = PricingApprovalWorkflow()
    print("Pricing Approval Workflow v1.0 initialized")
    print("Approvers: 4-level governance | Auto-routing: Enabled")
