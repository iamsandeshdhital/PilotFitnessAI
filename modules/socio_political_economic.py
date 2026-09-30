"""
Socio-Political-Economic Risk Analysis Module
Evaluates pilot's socio-political views, economic stability indicators, and social risk factors.
"""

import re
from datetime import datetime


class SocioPoliticalEconomicAnalyzer:
    """Analyzes socio-political and economic risk factors"""
    
    def __init__(self):
        self.political_extremism_patterns = [
            r'\b(fascist|nazi|communist|anarchist|extremist|radical)\b',
            r'\b(white power|black power|ethnic cleansing|race war)\b',
            r'\b(overthrow the government|revolution|armed struggle)\b',
        ]
        
        self.anti_establishment_patterns = [
            r'\b(the system is rigged|deep state|new world order)\b',
            r'\b(don\'t trust the government|they\'re lying to us)\b',
        ]
        
        self.economic_stress_patterns = [
            r'\b(can\'t pay|behind on payments|debt collectors|foreclosure)\b',
            r'\b(broke|no money|can\'t afford|financial ruin)\b',
            r'\b(gambling debt|casino|bet|wager)\b',
        ]
        
        self.social_unrest_patterns = [
            r'\b(protest|riot|demonstration|march|uprising)\b',
            r'\b(police brutality|systemic racism|oppression)\b',
        ]
    
    def assess(self, pilot, social_posts):
        """Run socio-political-economic assessment"""
        findings = []
        recommendations = []
        risk_factors = []
        score = 100
        
        if not social_posts:
            return {
                'score': 50,
                'status': 'NO_DATA',
                'findings': ['No social media data for socio-political-economic analysis'],
                'recommendations': ['Monitor social media for socio-political content'],
                'risk_factors': ['Unknown socio-political profile'],
            }
        
        # Analyze political content
        political_posts = [p for p in social_posts if p.contains_political_content]
        extremist_posts = [p for p in social_posts if p.contains_extremist_content]
        
        # Check for political extremism
        if extremist_posts:
            score -= 60
            findings.append(f"{len(extremist_posts)} posts with extremist political content")
            risk_factors.append("Political extremism indicators")
            recommendations.append("Security review and counseling required")
        
        # Analyze political engagement level
        if len(political_posts) > len(social_posts) * 0.5:
            score -= 15
            findings.append("Excessive political content on social media")
            risk_factors.append("Highly politicized social media presence")
            recommendations.append("Maintain political neutrality on social media")
        
        # Check for anti-establishment views
        anti_establishment_count = 0
        for post in social_posts:
            content = (post.post_content or '').lower()
            if any(re.search(p, content) for p in self.anti_establishment_patterns):
                anti_establishment_count += 1
        
        if anti_establishment_count > 2:
            score -= 20
            findings.append(f"{anti_establishment_count} posts with anti-establishment views")
            risk_factors.append("Anti-establishment sentiment")
        
        # Check for economic stress indicators
        economic_stress_count = 0
        for post in social_posts:
            content = (post.post_content or '').lower()
            if any(re.search(p, content) for p in self.economic_stress_patterns):
                economic_stress_count += 1
        
        if economic_stress_count > 0:
            score -= 15
            findings.append(f"{economic_stress_count} posts indicating economic stress")
            risk_factors.append("Economic stress indicators")
            recommendations.append("Financial counseling recommended")
        
        # Check for social unrest content
        unrest_count = 0
        for post in social_posts:
            content = (post.post_content or '').lower()
            if any(re.search(p, content) for p in self.social_unrest_patterns):
                unrest_count += 1
        
        if unrest_count > 3:
            score -= 10
            findings.append(f"{unrest_count} posts related to social unrest")
        
        # Analyze nationality-based risk
        nationality_risk = self._assess_nationality_risk(pilot.nationality)
        if nationality_risk > 0:
            score -= nationality_risk
            findings.append(f"Nationality-based risk factor: {pilot.nationality}")
        
        # Check for dual loyalty indicators
        dual_loyalty_risk = self._check_dual_loyalty(pilot, social_posts)
        if dual_loyalty_risk > 0:
            score -= dual_loyalty_risk
            risk_factors.append("Potential dual loyalty concerns")
        
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
            'political_posts_count': len(political_posts),
            'extremist_content_detected': len(extremist_posts) > 0,
        }
    
    def _assess_nationality_risk(self, nationality):
        """Assess risk based on nationality (simplified)"""
        # This is a simplified example - real implementation would use
        # comprehensive country risk databases
        high_risk_countries = []  # Would be populated from security database
        medium_risk_countries = []  # Would be populated from security database
        
        if nationality in high_risk_countries:
            return 30
        elif nationality in medium_risk_countries:
            return 15
        return 0
    
    def _check_dual_loyalty(self, pilot, social_posts):
        """Check for potential dual loyalty indicators"""
        risk_score = 0
        
        # Check for strong foreign ties
        foreign_language_posts = 0
        for post in social_posts:
            if post.language and post.language != 'en':
                foreign_language_posts += 1
        
        if foreign_language_posts > len(social_posts) * 0.3:
            risk_score += 10
        
        return risk_score
