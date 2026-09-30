"""
Psychological Assessment Module
Evaluates pilot psychological fitness using standardized test results.
"""

from datetime import datetime


class PsychologicalAssessment:
    """Comprehensive psychological fitness evaluation"""
    
    def __init__(self):
        self.weights = {
            'mmpi2': 25,
            'big5': 20,
            'emotional_stability': 20,
            'cognitive_function': 20,
            'behavioral_risk': 15,
        }
    
    def assess(self, pilot, psych_evals):
        """Run complete psychological assessment"""
        if not psych_evals:
            return {
                'score': 0,
                'status': 'NO_DATA',
                'findings': ['No psychological evaluation records available'],
                'recommendations': ['Schedule psychological evaluation immediately'],
                'risk_factors': ['Unknown psychological status'],
            }
        
        latest = psych_evals[0]
        findings = []
        recommendations = []
        risk_factors = []
        scores = {}
        
        # MMPI-2 Assessment
        mmpi_score = self._assess_mmpi2(latest, findings, recommendations, risk_factors)
        scores['mmpi2'] = mmpi_score
        
        # Big Five Personality Assessment
        big5_score = self._assess_big5(latest, findings, recommendations, risk_factors)
        scores['big5'] = big5_score
        
        # Emotional Stability
        emotional_score = self._assess_emotional_stability(latest, findings, recommendations, risk_factors)
        scores['emotional_stability'] = emotional_score
        
        # Cognitive Function
        cognitive_score = self._assess_cognitive_function(latest, findings, recommendations, risk_factors)
        scores['cognitive_function'] = cognitive_score
        
        # Behavioral Risk
        behavioral_score = self._assess_behavioral_risk(latest, findings, recommendations, risk_factors)
        scores['behavioral_risk'] = behavioral_score
        
        # Calculate weighted score
        total_weight = sum(self.weights.values())
        weighted_sum = sum(
            scores.get(key, 0) * self.weights.get(key, 0)
            for key in self.weights
        )
        overall_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Check eval recency
        if latest.eval_date:
            days_since = (datetime.now().date() - latest.eval_date).days
            if days_since > 365:
                overall_score *= 0.7
                findings.append(f"Last psychological eval was {days_since} days ago")
                risk_factors.append("Outdated psychological evaluation")
                recommendations.append("Schedule annual psychological evaluation")
            elif days_since > 180:
                overall_score *= 0.9
                findings.append(f"Last psychological eval was {days_since} days ago")
        
        # Determine status
        if overall_score >= 80 and not risk_factors:
            status = 'FIT'
        elif overall_score >= 60:
            status = 'CONDITIONAL'
        else:
            status = 'UNFIT'
        
        # Critical overrides
        if latest.psychological_fitness == 'UNFIT':
            status = 'UNFIT'
            overall_score = min(overall_score, 20)
            findings.append("CRITICAL: Evaluator determined pilot UNFIT")
        
        return {
            'score': round(overall_score, 1),
            'status': status,
            'findings': findings,
            'recommendations': recommendations,
            'risk_factors': risk_factors,
            'sub_scores': scores,
            'eval_date': latest.eval_date.isoformat() if latest.eval_date else None,
            'evaluator': latest.evaluator_name,
        }
    
    def _assess_mmpi2(self, record, findings, recommendations, risk_factors):
        """Assess MMPI-2 results"""
        score = 100
        
        # Check validity
        if record.mmpi2_validity and 'Valid' not in record.mmpi2_validity:
            score -= 30
            findings.append(f"MMPI-2 validity concern: {record.mmpi2_validity}")
            risk_factors.append("Psychological test validity issues")
        
        # Clinical scales (T-scores, >65 is clinically significant)
        scales = {
            'hs': ('Hypochondriasis', record.mmpi2_hs),
            'd': ('Depression', record.mmpi2_d),
            'hy': ('Hysteria', record.mmpi2_hy),
            'pd': ('Psychopathic Deviate', record.mmpi2_pd),
            'mf': ('Masculinity-Femininity', record.mmpi2_mf),
            'pa': ('Paranoia', record.mmpi2_pa),
            'pt': ('Psychasthenia', record.mmpi2_pt),
            'sc': ('Schizophrenia', record.mmpi2_sc),
            'ma': ('Hypomania', record.mmpi2_ma),
            'si': ('Social Introversion', record.mmpi2_si),
        }
        
        elevated_scales = []
        for key, (name, value) in scales.items():
            if value and value > 65:
                elevated_scales.append(f"{name} (T={value:.0f})")
                if value > 75:
                    score -= 15
                else:
                    score -= 8
        
        if elevated_scales:
            findings.append(f"Elevated MMPI-2 scales: {', '.join(elevated_scales)}")
            if len(elevated_scales) >= 3:
                risk_factors.append("Multiple elevated MMPI-2 scales")
                recommendations.append("Comprehensive psychological evaluation recommended")
        
        # Specific concerns
        if record.mmpi2_d and record.mmpi2_d > 70:
            risk_factors.append("Significant depression indicators")
            recommendations.append("Depression screening and treatment")
        
        if record.mmpi2_pa and record.mmpi2_pa > 70:
            risk_factors.append("Paranoia indicators")
        
        if record.mmpi2_si and record.mmpi2_si > 70:
            score -= 10
            findings.append("High social introversion - may affect CRM")
        
        return max(0, score)
    
    def _assess_big5(self, record, findings, recommendations, risk_factors):
        """Assess Big Five personality traits"""
        score = 100
        
        # Conscientiousness is most important for pilots
        if record.big5_conscientiousness:
            if record.big5_conscientiousness >= 70:
                pass  # Good
            elif record.big5_conscientiousness >= 50:
                score -= 10
                findings.append("Average conscientiousness")
            else:
                score -= 30
                findings.append("LOW conscientiousness - concerning for pilot")
                risk_factors.append("Low conscientiousness - safety concern")
                recommendations.append("Personality development program")
        
        # Neuroticism (emotional stability) - lower is better
        if record.big5_neuroticism:
            if record.big5_neuroticism <= 40:
                pass  # Good
            elif record.big5_neuroticism <= 60:
                score -= 10
                findings.append("Average neuroticism")
            else:
                score -= 30
                findings.append("HIGH neuroticism - emotional instability risk")
                risk_factors.append("High neuroticism - stress vulnerability")
                recommendations.append("Stress management training recommended")
        
        # Agreeableness
        if record.big5_agreeableness:
            if record.big5_agreeableness >= 60:
                pass
            elif record.big5_agreeableness >= 40:
                score -= 5
            else:
                score -= 15
                findings.append("Low agreeableness - CRM concerns")
                recommendations.append("Teamwork and communication training")
        
        # Openness
        if record.big5_openness:
            if 40 <= record.big5_openness <= 70:
                pass
            else:
                score -= 5
                findings.append("Unusual openness score")
        
        return max(0, score)
    
    def _assess_emotional_stability(self, record, findings, recommendations, risk_factors):
        """Assess emotional stability indicators"""
        score = 100
        
        levels = {
            'anxiety': (record.anxiety_level, 'Anxiety'),
            'depression': (record.depression_level, 'Depression'),
            'stress': (record.stress_level, 'Stress'),
            'aggression': (record.aggression_level, 'Aggression'),
        }
        
        for key, (level, name) in levels.items():
            if level == 'None' or not level:
                continue
            elif level == 'Mild':
                score -= 10
                findings.append(f"Mild {name.lower()} reported")
            elif level == 'Moderate':
                score -= 25
                findings.append(f"Moderate {name.lower()} reported")
                risk_factors.append(f"Moderate {name.lower()}")
                recommendations.append(f"{name} management counseling recommended")
            elif level == 'Severe':
                score -= 50
                findings.append(f"SEVERE {name.lower()} reported")
                risk_factors.append(f"Severe {name.lower()} - grounding concern")
                recommendations.append(f"Immediate {name.lower()} treatment required")
        
        return max(0, score)
    
    def _assess_cognitive_function(self, record, findings, recommendations, risk_factors):
        """Assess cognitive function"""
        score = 100
        
        functions = {
            'cognitive': (record.cognitive_function, 'Cognitive function'),
            'memory': (record.memory_function, 'Memory function'),
            'attention': (record.attention_function, 'Attention function'),
            'decision': (record.decision_making_quality, 'Decision making'),
        }
        
        for key, (value, name) in functions.items():
            if not value or value == 'Normal':
                continue
            elif value == 'Mild Impairment':
                score -= 20
                findings.append(f"Mild {name.lower()} impairment")
                recommendations.append(f"{name} assessment recommended")
            elif value == 'Moderate Impairment':
                score -= 40
                findings.append(f"Moderate {name.lower()} impairment")
                risk_factors.append(f"Moderate {name.lower()} impairment")
            elif value == 'Severe Impairment':
                score -= 70
                findings.append(f"SEVERE {name.lower()} impairment")
                risk_factors.append(f"Severe {name.lower()} impairment - grounding")
        
        return max(0, score)
    
    def _assess_behavioral_risk(self, record, findings, recommendations, risk_factors):
        """Assess behavioral risk factors"""
        score = 100
        
        # Impulsivity
        if record.impulsivity_level:
            if record.impulsivity_level == 'Low':
                pass
            elif record.impulsivity_level == 'Moderate':
                score -= 15
                findings.append("Moderate impulsivity")
                recommendations.append("Impulse control training")
            elif record.impulsivity_level == 'High':
                score -= 40
                findings.append("HIGH impulsivity")
                risk_factors.append("High impulsivity - safety risk")
                recommendations.append("Behavioral modification program required")
        
        # Risk-taking tendency
        if record.risk_taking_tendency:
            if record.risk_taking_tendency == 'Low':
                pass
            elif record.risk_taking_tendency == 'Moderate':
                score -= 10
                findings.append("Moderate risk-taking tendency")
            elif record.risk_taking_tendency == 'High':
                score -= 35
                findings.append("HIGH risk-taking tendency")
                risk_factors.append("High risk-taking tendency - safety concern")
                recommendations.append("Risk awareness training required")
        
        return max(0, score)
