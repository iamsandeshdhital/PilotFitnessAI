"""
Financial Stability Assessment Module
Evaluates pilot's financial health and economic risk factors.
"""

from datetime import datetime


class FinancialStabilityChecker:
    """Assesses financial stability and economic risk factors"""
    
    def __init__(self):
        self.credit_score_excellent = 750
        self.credit_score_good = 670
        self.credit_score_fair = 580
        self.credit_score_poor = 300
        
        self.debt_to_income_warning = 0.4
        self.debt_to_income_critical = 0.6
    
    def assess(self, pilot, financial_records):
        """Run financial stability assessment"""
        if not financial_records:
            return {
                'score': 50,
                'status': 'NO_DATA',
                'findings': ['No financial records available'],
                'recommendations': ['Conduct financial background check'],
                'risk_factors': ['Unknown financial status'],
            }
        
        latest = financial_records[0]
        findings = []
        recommendations = []
        risk_factors = []
        score = 100
        
        # Credit Score Assessment
        if latest.credit_score:
            if latest.credit_score >= self.credit_score_excellent:
                pass  # Excellent
            elif latest.credit_score >= self.credit_score_good:
                score -= 5
                findings.append(f"Good credit score: {latest.credit_score}")
            elif latest.credit_score >= self.credit_score_fair:
                score -= 20
                findings.append(f"Fair credit score: {latest.credit_score}")
                risk_factors.append("Fair credit score - financial stress indicator")
                recommendations.append("Financial counseling recommended")
            elif latest.credit_score >= self.credit_score_poor:
                score -= 40
                findings.append(f"Poor credit score: {latest.credit_score}")
                risk_factors.append("Poor credit score - significant financial stress")
                recommendations.append("Mandatory financial counseling required")
            else:
                score -= 60
                findings.append(f"Very poor credit score: {latest.credit_score}")
                risk_factors.append("Very poor credit score - high risk")
                recommendations.append("Intensive financial management program required")
        
        # Debt-to-Income Ratio
        if latest.annual_income and latest.total_debt:
            dti_ratio = latest.total_debt / latest.annual_income if latest.annual_income > 0 else 1
            
            if dti_ratio > self.debt_to_income_critical:
                score -= 35
                findings.append(f"Critical debt-to-income ratio: {dti_ratio:.1%}")
                risk_factors.append("Critical debt burden")
                recommendations.append("Debt management program required")
            elif dti_ratio > self.debt_to_income_warning:
                score -= 20
                findings.append(f"High debt-to-income ratio: {dti_ratio:.1%}")
                risk_factors.append("High debt burden")
                recommendations.append("Financial planning assistance recommended")
        
        # Bankruptcy History
        if latest.bankruptcy_history:
            score -= 40
            findings.append("Bankruptcy history detected")
            risk_factors.append("Previous bankruptcy")
            recommendations.append("Financial stability monitoring required")
        
        # Payment Delinquencies
        if latest.payment_delinquencies:
            if latest.payment_delinquencies > 5:
                score -= 30
                findings.append(f"Multiple payment delinquencies: {latest.payment_delinquencies}")
                risk_factors.append("Pattern of payment delinquencies")
            elif latest.payment_delinquencies > 2:
                score -= 15
                findings.append(f"Several payment delinquencies: {latest.payment_delinquencies}")
                risk_factors.append("Payment delinquency history")
            elif latest.payment_delinquencies > 0:
                score -= 5
                findings.append(f"Payment delinquencies: {latest.payment_delinquencies}")
        
        # Gambling Concerns
        if latest.gambling_concerns:
            score -= 35
            findings.append("Gambling concerns identified")
            risk_factors.append("Gambling - potential financial and security risk")
            recommendations.append("Gambling addiction screening required")
        
        # Financial Stress Indicators
        if latest.financial_stress_indicators:
            score -= 15
            findings.append(f"Financial stress indicators: {latest.financial_stress_indicators}")
            risk_factors.append("Financial stress reported")
        
        # Source of Wealth Verification
        if not latest.source_of_wealth_verified:
            score -= 10
            findings.append("Source of wealth not verified")
            recommendations.append("Complete source of wealth verification")
        
        # Income Stability
        if latest.annual_income:
            if latest.annual_income < 50000:
                score -= 10
                findings.append(f"Low income level: ${latest.annual_income:,.0f}")
                risk_factors.append("Low income - potential financial stress")
        
        # Check record recency
        if latest.record_date:
            days_since = (datetime.now().date() - latest.record_date).days
            if days_since > 365:
                score -= 10
                findings.append(f"Financial record is {days_since} days old")
                recommendations.append("Update financial records")
        
        # Determine status
        if score >= 80 and not risk_factors:
            status = 'FIT'
        elif score >= 60:
            status = 'CONDITIONAL'
        else:
            status = 'UNFIT'
        
        return {
            'score': round(max(0, score), 1),
            'status': status,
            'findings': findings,
            'recommendations': recommendations,
            'risk_factors': risk_factors,
            'credit_score': latest.credit_score,
            'debt_to_income': round(latest.total_debt / latest.annual_income, 2) if latest.annual_income and latest.total_debt else None,
            'bankruptcy_history': latest.bankruptcy_history,
            'gambling_concerns': latest.gambling_concerns,
        }
