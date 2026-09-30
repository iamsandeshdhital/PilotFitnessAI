"""
Radicalization Detection Module
Detects signs of radicalization, extremist views, and ideological extremism
in pilot's communications, social media, and behavior patterns.
"""

import re
from datetime import datetime
from collections import Counter


class RadicalizationDetector:
    """Detects radicalization indicators and extremist tendencies"""
    
    def __init__(self):
        # Extremist ideology indicators
        self.extremist_indicators = {
            'religious_extremism': [
                r'\b(jihad|sharia|caliphate|infidel|kafir|mushrik)\b',
                r'\b(islamic state|isis|isil|al-qaeda|taliban|boko haram)\b',
                r'\b(martyrdom|martyr operation|suicide mission)\b',
            ],
            'political_extremism': [
                r'\b(white power|white genocide|14 words|blood and soil)\b',
                r'\b(neo-nazi|nazi|hitler|third reich|aryan)\b',
                r'\b(communist revolution|overthrow the government|armed struggle)\b',
                r'\b(ethnicity cleansing|race war|racial holy war)\b',
            ],
            'violent_extremism': [
                r'\b(kill them all|death to|eliminate|exterminate)\b',
                r'\b(armed resistance|violent revolution|by any means necessary)\b',
                r'\b(target|attack|bomb|shoot|stab).{0,20}(them|enemy|oppressor)\b',
            ],
            'conspiracy_theories': [
                r'\b(new world order|illuminati|deep state|zionist occupation)\b',
                r'\b(false flag|inside job|crisis actor|hoax)\b',
                r'\b(genocide|depopulation|great replacement)\b',
            ],
        }
        
        # Radicalization stage indicators
        self.radicalization_stages = {
            'stage1_personal_grievance': [
                r'\b(unfair|treated like|discriminated|oppressed|marginalized)\b',
                r'\b(they hate us|against my people|my group is)\b',
            ],
            'stage2_us_vs_them': [
                r'\b(us vs them|us versus them|the enemy|the other)\b',
                r'\b(they want to|trying to destroy|take over|replace us)\b',
            ],
            'stage3_justification': [
                r'\b(they deserve|had it coming|justified|necessary evil)\b',
                r'\b(collateral damage|acceptable losses|for the greater good)\b',
            ],
            'stage4_action': [
                r'\b(take action|do something|fight back|rise up)\b',
                r'\b(time to act|can\'t wait anymore|enough is enough)\b',
            ],
        }
        
        # Concerning behavioral changes
        self.behavioral_changes = {
            'social_isolation': 'Increasing social isolation',
            'new_associations': 'New concerning associations',
            'ideological_shift': 'Sudden ideological shift',
            'increased_secrecy': 'Increased secrecy behavior',
            'weapon_interest': 'Unusual interest in weapons',
        }
        
        # Online activity indicators
        self.online_indicators = {
            'extremist_forums': 'Access to extremist forums',
            'encrypted_comms': 'Shift to encrypted communications',
            'radical_content': 'Consumption of radical content',
            'recruitment': 'Possible recruitment activity',
        }
    
    def assess(self, pilot, social_posts, message_records, browsing_history, 
               email_records, staff_feedback):
        """Run radicalization detection assessment"""
        findings = []
        recommendations = []
        risk_factors = []
        score = 100
        
        # Analyze social media content
        if social_posts:
            social_result = self._analyze_social_media(social_posts, findings, recommendations, risk_factors)
            score -= social_result
        
        # Analyze messages
        if message_records:
            message_result = self._analyze_messages(message_records, findings, recommendations, risk_factors)
            score -= message_result
        
        # Analyze browsing history
        if browsing_history:
            browsing_result = self._analyze_browsing(browsing_history, findings, recommendations, risk_factors)
            score -= browsing_result
        
        # Analyze emails
        if email_records:
            email_result = self._analyze_emails(email_records, findings, recommendations, risk_factors)
            score -= email_result
        
        # Analyze staff feedback for behavioral changes
        if staff_feedback:
            behavior_result = self._analyze_behavioral_indicators(staff_feedback, findings, recommendations, risk_factors)
            score -= behavior_result
        
        # Determine radicalization risk level
        risk_level = self._determine_risk_level(findings, risk_factors)
        
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
            'radicalization_risk': risk_level,
            'indicators_detected': len(risk_factors),
        }
    
    def _analyze_social_media(self, social_posts, findings, recommendations, risk_factors):
        """Analyze social media content for radicalization indicators"""
        penalty = 0
        
        for post in social_posts:
            content = (post.post_content or '').lower()
            
            # Check for extremist content
            for category, patterns in self.extremist_indicators.items():
                for pattern in patterns:
                    if re.search(pattern, content):
                        penalty += 30
                        findings.append(f"Extremist content detected ({category})")
                        risk_factors.append(f"Extremist ideology indicator: {category}")
                        recommendations.append("Immediate security review required")
                        break
            
            # Check for radicalization stage indicators
            for stage, patterns in self.radicalization_stages.items():
                for pattern in patterns:
                    if re.search(pattern, content):
                        penalty += 15
                        findings.append(f"Radicalization indicator: {stage}")
                        risk_factors.append(f"Radicalization stage indicator: {stage}")
                        break
        
        # Check for patterns across posts
        all_content = ' '.join((p.post_content or '').lower() for p in social_posts)
        
        # Count extremist terms
        extremist_term_count = 0
        for category, patterns in self.extremist_indicators.items():
            for pattern in patterns:
                extremist_term_count += len(re.findall(pattern, all_content))
        
        if extremist_term_count > 5:
            penalty += 20
            findings.append("Pattern of extremist content across multiple posts")
            risk_factors.append("Consistent extremist content")
        
        return min(penalty, 80)
    
    def _analyze_messages(self, message_records, findings, recommendations, risk_factors):
        """Analyze messages for radicalization indicators"""
        penalty = 0
        
        for message in message_records:
            content = (message.content or '').lower()
            
            for category, patterns in self.extremist_indicators.items():
                for pattern in patterns:
                    if re.search(pattern, content):
                        penalty += 35
                        findings.append(f"Extremist content in messages ({category})")
                        risk_factors.append(f"Extremist ideology in messages: {category}")
                        recommendations.append("Security investigation required")
                        break
        
        return min(penalty, 60)
    
    def _analyze_browsing(self, browsing_history, findings, recommendations, risk_factors):
        """Analyze browsing history for radicalization indicators"""
        penalty = 0
        
        for record in browsing_history:
            url = (record.url or '').lower()
            category = (record.category or '').lower()
            
            # Check for extremist content
            extremist_terms = ['extremist', 'radical', 'jihad', 'neo-nazi', 'terrorist', 'militia']
            for term in extremist_terms:
                if term in url or term in category:
                    penalty += 25
                    findings.append(f"Extremist content access: {term}")
                    risk_factors.append(f"Extremist content browsing: {term}")
                    break
            
            # Check for weapons/weapons manufacturing
            weapon_terms = ['bomb making', 'explosives', 'weapon build', 'ammunition purchase']
            for term in weapon_terms:
                if term in url or term in category:
                    penalty += 40
                    findings.append(f"Weapons-related content access: {term}")
                    risk_factors.append(f"Weapons content: {term}")
                    recommendations.append("Immediate security intervention required")
                    break
        
        return min(penalty, 70)
    
    def _analyze_emails(self, email_records, findings, recommendations, risk_factors):
        """Analyze emails for radicalization indicators"""
        penalty = 0
        
        for email in email_records:
            content = (email.subject + ' ' + (email.body or '')).lower()
            
            for category, patterns in self.extremist_indicators.items():
                for pattern in patterns:
                    if re.search(pattern, content):
                        penalty += 30
                        findings.append(f"Extremist content in email ({category})")
                        risk_factors.append(f"Extremist ideology in email: {category}")
                        break
        
        return min(penalty, 50)
    
    def _analyze_behavioral_indicators(self, staff_feedback, findings, recommendations, risk_factors):
        """Analyze staff feedback for behavioral changes"""
        penalty = 0
        
        # Check for reported behavioral changes
        for feedback in staff_feedback:
            concerns = (feedback.concerns or '').lower()
            comments = (feedback.additional_comments or '').lower()
            all_text = concerns + ' ' + comments
            
            # Check for concerning behavioral indicators
            concerning_terms = {
                'withdrawn': 'Pilot becoming withdrawn',
                'isolated': 'Pilot isolating from others',
                'aggressive': 'Increased aggression',
                'paranoid': 'Paranoid behavior',
                'secretive': 'Increased secrecy',
                'different': 'Noticeable personality change',
                'extreme': 'Extreme views expressed',
                'radical': 'Radical statements',
            }
            
            for term, message in concerning_terms.items():
                if term in all_text:
                    penalty += 15
                    findings.append(f"Staff reported: {message}")
                    risk_factors.append(f"Behavioral concern: {message}")
        
        return min(penalty, 40)
    
    def _determine_risk_level(self, findings, risk_factors):
        """Determine overall radicalization risk level"""
        if not risk_factors:
            return 'NONE'
        
        critical_indicators = [
            'Extremist ideology indicator',
            'Extremist content in messages',
            'Weapons content',
            'Immediate security',
        ]
        
        critical_count = sum(
            1 for rf in risk_factors
            if any(ci in rf for ci in critical_indicators)
        )
        
        if critical_count >= 2:
            return 'CRITICAL'
        elif critical_count >= 1:
            return 'HIGH'
        elif len(risk_factors) >= 3:
            return 'MEDIUM'
        else:
            return 'LOW'
