"""
Behavior Pattern Change Detection Module
Detects changes in pilot behavior over time that may indicate risk factors.
"""

from datetime import datetime, timedelta
from collections import defaultdict


class BehaviorPatternAnalyzer:
    """Analyzes behavior patterns and detects changes over time"""
    
    def __init__(self):
        self.change_threshold = 0.3  # 30% change threshold
        self.significant_change_threshold = 0.5  # 50% change is significant
    
    def assess(self, pilot, flight_logs, staff_feedback, social_posts, medical_records):
        """Run behavior pattern change assessment"""
        findings = []
        recommendations = []
        risk_factors = []
        score = 100
        
        if not any([flight_logs, staff_feedback, social_posts, medical_records]):
            return {
                'score': 50,
                'status': 'NO_DATA',
                'findings': ['Insufficient data for behavior pattern analysis'],
                'recommendations': ['Collect comprehensive behavioral data'],
                'risk_factors': ['Unknown behavior patterns'],
            }
        
        # Analyze flight performance trends
        if flight_logs and len(flight_logs) >= 5:
            flight_trend = self._analyze_flight_trends(flight_logs, findings, recommendations, risk_factors)
            score -= flight_trend
        
        # Analyze staff feedback trends
        if staff_feedback and len(staff_feedback) >= 3:
            feedback_trend = self._analyze_feedback_trends(staff_feedback, findings, recommendations, risk_factors)
            score -= feedback_trend
        
        # Analyze social media behavior changes
        if social_posts and len(social_posts) >= 5:
            social_trend = self._analyze_social_trends(social_posts, findings, recommendations, risk_factors)
            score -= social_trend
        
        # Analyze medical/health trends
        if medical_records and len(medical_records) >= 2:
            health_trend = self._analyze_health_trends(medical_records, findings, recommendations, risk_factors)
            score -= health_trend
        
        # Check for sudden changes
        sudden_changes = self._detect_sudden_changes(flight_logs, staff_feedback, social_posts)
        if sudden_changes:
            score -= len(sudden_changes) * 15
            findings.extend(sudden_changes)
            risk_factors.append("Sudden behavior changes detected")
            recommendations.append("Investigate causes of behavior changes")
        
        # Check for gradual decline
        decline_indicators = self._detect_gradual_decline(flight_logs, staff_feedback, medical_records)
        if decline_indicators:
            score -= len(decline_indicators) * 10
            findings.extend(decline_indicators)
            risk_factors.append("Gradual performance/behavior decline")
            recommendations.append("Comprehensive evaluation recommended")
        
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
            'changes_detected': len(sudden_changes) + len(decline_indicators),
        }
    
    def _analyze_flight_trends(self, flight_logs, findings, recommendations, risk_factors):
        """Analyze flight performance trends over time"""
        penalty = 0
        
        # Sort by date
        sorted_logs = sorted(
            [l for l in flight_logs if l.flight_date],
            key=lambda x: x.flight_date
        )
        
        if len(sorted_logs) < 5:
            return penalty
        
        # Split into early and recent periods
        mid_point = len(sorted_logs) // 2
        early_logs = sorted_logs[:mid_point]
        recent_logs = sorted_logs[mid_point:]
        
        # Compare flight duration patterns
        early_avg = sum(l.flight_duration_minutes or 0 for l in early_logs) / len(early_logs)
        recent_avg = sum(l.flight_duration_minutes or 0 for l in recent_logs) / len(recent_logs)
        
        if recent_avg < early_avg * 0.6:
            penalty += 15
            findings.append("Significant decrease in flight activity")
            risk_factors.append("Reduced flight activity - possible disengagement")
        
        # Compare incident rates
        early_incidents = len([l for l in early_logs if l.incidents and l.incidents != 'None'])
        recent_incidents = len([l for l in recent_logs if l.incidents and l.incidents != 'None'])
        
        if recent_incidents > early_incidents * 2 and recent_incidents > 1:
            penalty += 20
            findings.append("Increase in flight incidents")
            risk_factors.append("Rising incident rate")
            recommendations.append("Performance review and additional training")
        
        # Check for route changes
        early_routes = set(f"{l.departure_airport}-{l.arrival_airport}" for l in early_logs)
        recent_routes = set(f"{l.departure_airport}-{l.arrival_airport}" for l in recent_logs)
        
        if len(recent_routes - early_routes) > len(early_routes) * 0.5:
            penalty += 10
            findings.append("Significant route changes detected")
        
        return penalty
    
    def _analyze_feedback_trends(self, staff_feedback, findings, recommendations, risk_factors):
        """Analyze staff feedback trends over time"""
        penalty = 0
        
        # Sort by date
        sorted_feedback = sorted(
            [f for f in staff_feedback if f.feedback_date],
            key=lambda x: x.feedback_date
        )
        
        if len(sorted_feedback) < 3:
            return penalty
        
        # Split into early and recent
        mid_point = len(sorted_feedback) // 2
        early_fb = sorted_feedback[:mid_point]
        recent_fb = sorted_feedback[mid_point:]
        
        # Compare average ratings
        early_ratings = [f.overall_rating for f in early_fb if f.overall_rating]
        recent_ratings = [f.overall_rating for f in recent_fb if f.overall_rating]
        
        if early_ratings and recent_ratings:
            early_avg = sum(early_ratings) / len(early_ratings)
            recent_avg = sum(recent_ratings) / len(recent_ratings)
            
            if recent_avg < early_avg - 1:
                penalty += 20
                findings.append(f"Staff feedback declined from {early_avg:.1f} to {recent_avg:.1f}")
                risk_factors.append("Declining staff perception")
                recommendations.append("Interpersonal skills training recommended")
            elif recent_avg < early_avg - 0.5:
                penalty += 10
                findings.append(f"Staff feedback slightly declined from {early_avg:.1f} to {recent_avg:.1f}")
        
        # Check for new behavioral flags
        early_flags = set()
        recent_flags = set()
        
        for fb in early_fb:
            for flag in ['signs_of_stress', 'signs_of_fatigue', 'signs_of_aggression', 'signs_of_depression']:
                if getattr(fb, flag):
                    early_flags.add(flag)
        
        for fb in recent_fb:
            for flag in ['signs_of_stress', 'signs_of_fatigue', 'signs_of_aggression', 'signs_of_depression']:
                if getattr(fb, flag):
                    recent_flags.add(flag)
        
        new_flags = recent_flags - early_flags
        if new_flags:
            penalty += len(new_flags) * 15
            flag_names = [f.replace('signs_of_', '').replace('_', ' ') for f in new_flags]
            findings.append(f"New behavioral concerns: {', '.join(flag_names)}")
            risk_factors.append("Emerging behavioral issues")
            recommendations.append("Counseling and support services recommended")
        
        return penalty
    
    def _analyze_social_trends(self, social_posts, findings, recommendations, risk_factors):
        """Analyze social media behavior changes over time"""
        penalty = 0
        
        # Sort by date
        sorted_posts = sorted(
            [p for p in social_posts if p.post_date],
            key=lambda x: x.post_date
        )
        
        if len(sorted_posts) < 5:
            return penalty
        
        # Split into early and recent
        mid_point = len(sorted_posts) // 2
        early_posts = sorted_posts[:mid_point]
        recent_posts = sorted_posts[mid_point:]
        
        # Compare sentiment
        early_sentiments = [p.sentiment_score or 0 for p in early_posts]
        recent_sentiments = [p.sentiment_score or 0 for p in recent_posts]
        
        early_avg = sum(early_sentiments) / len(early_sentiments) if early_sentiments else 0
        recent_avg = sum(recent_sentiments) / len(recent_sentiments) if recent_sentiments else 0
        
        if recent_avg < early_avg - 0.3:
            penalty += 20
            findings.append(f"Social media sentiment declined significantly")
            risk_factors.append("Negative sentiment shift on social media")
            recommendations.append("Mental health check-in recommended")
        
        # Check for posting frequency changes
        if len(recent_posts) > len(early_posts) * 2:
            penalty += 10
            findings.append("Significant increase in social media activity")
            risk_factors.append("Changed social media behavior")
        
        # Check for new risk indicators
        early_risks = set()
        recent_risks = set()
        
        for post in early_posts:
            if post.risk_indicators:
                import json
                try:
                    early_risks.update(json.loads(post.risk_indicators))
                except (json.JSONDecodeError, TypeError):
                    pass
        
        for post in recent_posts:
            if post.risk_indicators:
                import json
                try:
                    recent_risks.update(json.loads(post.risk_indicators))
                except (json.JSONDecodeError, TypeError):
                    pass
        
        new_risks = recent_risks - early_risks
        if new_risks:
            penalty += len(new_risks) * 10
            findings.append(f"New risk indicators in social media: {', '.join(new_risks)}")
            risk_factors.append("Emerging social media risk indicators")
        
        return penalty
    
    def _analyze_health_trends(self, medical_records, findings, recommendations, risk_factors):
        """Analyze health trends over time"""
        penalty = 0
        
        # Sort by date
        sorted_records = sorted(
            [r for r in medical_records if r.exam_date],
            key=lambda x: x.exam_date
        )
        
        if len(sorted_records) < 2:
            return penalty
        
        # Compare BMI changes
        bmi_records = [r for r in sorted_records if r.bmi]
        if len(bmi_records) >= 2:
            early_bmi = bmi_records[0].bmi
            recent_bmi = bmi_records[-1].bmi
            
            if recent_bmi and early_bmi:
                bmi_change = recent_bmi - early_bmi
                if bmi_change > 3:
                    penalty += 15
                    findings.append(f"Significant weight gain: BMI {early_bmi:.1f} -> {recent_bmi:.1f}")
                    risk_factors.append("Significant weight change")
                    recommendations.append("Health and wellness program recommended")
                elif bmi_change < -3:
                    penalty += 10
                    findings.append(f"Significant weight loss: BMI {early_bmi:.1f} -> {recent_bmi:.1f}")
                    risk_factors.append("Significant weight loss")
        
        # Compare blood pressure trends
        bp_records = [r for r in sorted_records if r.blood_pressure_systolic and r.blood_pressure_diastolic]
        if len(bp_records) >= 2:
            early_sys = bp_records[0].blood_pressure_systolic
            recent_sys = bp_records[-1].blood_pressure_systolic
            
            if recent_sys and early_sys:
                if recent_sys > early_sys + 15:
                    penalty += 15
                    findings.append(f"Blood pressure increased: {early_sys} -> {recent_sys}")
                    risk_factors.append("Worsening blood pressure")
                    recommendations.append("Cardiovascular health management required")
        
        # Check for new medical conditions
        early_conditions = set()
        recent_conditions = set()
        
        for record in sorted_records[:-1]:
            if record.neurological_conditions and record.neurological_conditions != 'None':
                early_conditions.add(record.neurological_conditions)
            if record.psychiatric_conditions and record.psychiatric_conditions != 'None':
                early_conditions.add(record.psychiatric_conditions)
        
        latest = sorted_records[-1]
        if latest.neurological_conditions and latest.neurological_conditions != 'None':
            recent_conditions.add(latest.neurological_conditions)
        if latest.psychiatric_conditions and latest.psychiatric_conditions != 'None':
            recent_conditions.add(latest.psychiatric_conditions)
        
        new_conditions = recent_conditions - early_conditions
        if new_conditions:
            penalty += 20
            findings.append(f"New medical conditions: {', '.join(new_conditions)}")
            risk_factors.append("New medical conditions detected")
            recommendations.append("Medical follow-up required")
        
        return penalty
    
    def _detect_sudden_changes(self, flight_logs, staff_feedback, social_posts):
        """Detect sudden behavior changes"""
        changes = []
        
        # Check for sudden stop in flying
        if flight_logs:
            sorted_logs = sorted(
                [l for l in flight_logs if l.flight_date],
                key=lambda x: x.flight_date,
                reverse=True
            )
            if sorted_logs:
                latest = sorted_logs[0].flight_date
                days_since = (datetime.now().date() - latest).days
                if days_since > 60 and len(flight_logs) > 10:
                    changes.append(f"Sudden stop in flying activity ({days_since} days ago)")
        
        # Check for sudden negative feedback
        if staff_feedback:
            recent_fb = [
                f for f in staff_feedback
                if f.feedback_date and (datetime.utcnow().date() - f.feedback_date).days <= 30
            ]
            if recent_fb:
                avg_recent = sum(f.overall_rating or 3 for f in recent_fb) / len(recent_fb)
                if avg_recent < 2.5:
                    changes.append("Sudden drop in staff feedback ratings")
        
        # Check for sudden social media changes
        if social_posts:
            recent_posts = [
                p for p in social_posts
                if p.post_date and (datetime.utcnow() - p.post_date).days <= 7
            ]
            if len(recent_posts) > 10:
                changes.append("Sudden increase in social media activity")
        
        return changes
    
    def _detect_gradual_decline(self, flight_logs, staff_feedback, medical_records):
        """Detect gradual performance or behavior decline"""
        indicators = []
        
        # Check for gradual decline in flight hours
        if flight_logs and len(flight_logs) >= 10:
            sorted_logs = sorted(
                [l for l in flight_logs if l.flight_date],
                key=lambda x: x.flight_date
            )
            
            # Compare first third to last third
            third = len(sorted_logs) // 3
            early = sorted_logs[:third]
            recent = sorted_logs[-third:]
            
            early_hours = sum(l.flight_duration_minutes or 0 for l in early) / len(early) if early else 0
            recent_hours = sum(l.flight_duration_minutes or 0 for l in recent) / len(recent) if recent else 0
            
            if recent_hours < early_hours * 0.7:
                indicators.append("Gradual decline in flight activity")
        
        # Check for gradual health decline
        if medical_records and len(medical_records) >= 3:
            sorted_records = sorted(
                [r for r in medical_records if r.exam_date],
                key=lambda x: x.exam_date
            )
            
            # Check for declining health indicators
            bmi_trend = [r.bmi for r in sorted_records if r.bmi]
            if len(bmi_trend) >= 3:
                if all(bmi_trend[i] <= bmi_trend[i+1] for i in range(len(bmi_trend)-1)):
                    if bmi_trend[-1] - bmi_trend[0] > 2:
                        indicators.append("Gradual weight gain trend")
        
        return indicators
