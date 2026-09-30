"""
Staff Feedback Analysis Module
Analyzes feedback from colleagues, crew members, and staff.
"""

from datetime import datetime


class StaffFeedbackAnalyzer:
    """Analyzes staff and crew feedback for pilot fitness assessment"""
    
    def __init__(self):
        self.rating_categories = [
            'professionalism_rating',
            'communication_rating',
            'teamwork_rating',
            'decision_making_rating',
            'stress_management_rating',
            'punctuality_rating',
            'technical_knowledge_rating',
            'situational_awareness_rating',
            'leadership_rating',
        ]
        
        self.behavioral_flags = [
            'signs_of_stress',
            'signs_of_fatigue',
            'signs_of_substance_use',
            'signs_of_aggression',
            'signs_of_depression',
            'signs_of_financial_stress',
        ]
    
    def assess(self, pilot, feedback_list):
        """Run staff feedback assessment"""
        if not feedback_list:
            return {
                'score': 50,
                'status': 'NO_DATA',
                'findings': ['No staff feedback available'],
                'recommendations': ['Collect feedback from colleagues and crew'],
                'risk_factors': ['Unknown staff perception'],
            }
        
        findings = []
        recommendations = []
        risk_factors = []
        
        # Calculate average ratings
        avg_ratings = {}
        for category in self.rating_categories:
            ratings = [getattr(f, category) for f in feedback_list if getattr(f, category) is not None]
            if ratings:
                avg_ratings[category] = sum(ratings) / len(ratings)
        
        # Overall average
        overall_ratings = [f.overall_rating for f in feedback_list if f.overall_rating is not None]
        avg_overall = sum(overall_ratings) / len(overall_ratings) if overall_ratings else 3
        
        # Calculate base score from ratings (1-5 scale -> 0-100)
        score = (avg_overall / 5) * 100
        
        # Analyze individual categories
        for category, avg in avg_ratings.items():
            category_name = category.replace('_rating', '').replace('_', ' ').title()
            if avg < 3:
                score -= 10
                findings.append(f"Low {category_name} rating: {avg:.1f}/5")
                risk_factors.append(f"Low {category_name.lower()} scores from staff")
                recommendations.append(f"{category_name} improvement training recommended")
            elif avg < 4:
                score -= 5
                findings.append(f"Below average {category_name} rating: {avg:.1f}/5")
        
        # Check "would fly with again" responses
        would_not_fly = [f for f in feedback_list if f.would_fly_with_again == 'NO']
        if would_not_fly:
            score -= 30
            findings.append(f"{len(would_not_fly)} staff members would NOT fly with this pilot again")
            risk_factors.append("Staff unwilling to fly with pilot")
            recommendations.append("Immediate review and counseling required")
        
        unsure_count = len([f for f in feedback_list if f.would_fly_with_again == 'UNSURE'])
        if unsure_count > len(feedback_list) * 0.3:
            score -= 15
            findings.append(f"{unsure_count} staff members unsure about flying with this pilot")
        
        # Check behavioral flags
        for flag in self.behavioral_flags:
            flagged = [f for f in feedback_list if getattr(f, flag)]
            if flagged:
                flag_name = flag.replace('signs_of_', '').replace('_', ' ').title()
                score -= 15
                findings.append(f"{len(flagged)} reports of {flag_name.lower()} from staff")
                risk_factors.append(f"Staff reported signs of {flag_name.lower()}")
                
                if flag == 'signs_of_substance_use':
                    recommendations.append("Immediate substance abuse evaluation required")
                elif flag == 'signs_of_aggression':
                    recommendations.append("Anger management evaluation required")
                elif flag == 'signs_of_depression':
                    recommendations.append("Mental health evaluation required")
                elif flag == 'signs_of_financial_stress':
                    recommendations.append("Financial counseling recommended")
                else:
                    recommendations.append(f"{flag_name} assessment recommended")
        
        # Check feedback recency
        recent_feedback = [
            f for f in feedback_list
            if f.feedback_date and (datetime.utcnow().date() - f.feedback_date).days <= 180
        ]
        if len(recent_feedback) < 2:
            score -= 10
            findings.append("Limited recent feedback available")
            recommendations.append("Collect more recent feedback from crew members")
        
        # Check feedback diversity (multiple sources)
        providers = set(f.feedback_provider_name for f in feedback_list)
        if len(providers) < 3:
            score -= 5
            findings.append("Limited feedback sources")
            recommendations.append("Collect feedback from diverse sources")
        
        # Analyze qualitative feedback
        all_concerns = ' '.join([f.concerns or '' for f in feedback_list]).lower()
        concern_keywords = {
            'drinking': 'Alcohol concern raised by staff',
            'drugs': 'Drug concern raised by staff',
            'angry': 'Anger issues noted by staff',
            'rude': 'Rudeness reported by staff',
            'careless': 'Carelessness reported by staff',
            'dangerous': 'Dangerous behavior reported by staff',
            'unstable': 'Instability reported by staff',
        }
        
        for keyword, message in concern_keywords.items():
            if keyword in all_concerns:
                score -= 20
                findings.append(message)
                risk_factors.append(message)
        
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
            'feedback_count': len(feedback_list),
            'average_rating': round(avg_overall, 2),
            'average_ratings': {k: round(v, 2) for k, v in avg_ratings.items()},
            'behavioral_flags': {
                flag: len([f for f in feedback_list if getattr(f, flag)])
                for flag in self.behavioral_flags
            },
        }
