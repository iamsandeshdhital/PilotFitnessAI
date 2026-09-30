"""
Fatigue & Lifestyle Assessment Module
Evaluates pilot fatigue risk, sleep patterns, and lifestyle factors.
"""

from datetime import datetime, timedelta


class FatigueLifestyleAnalyzer:
    """Assesses fatigue risk and lifestyle factors"""
    
    def __init__(self):
        self.max_weekly_hours = 60
        self.max_monthly_hours = 100
        self.min_rest_hours = 10  # Minimum rest between shifts
    
    def assess(self, pilot, flight_logs, medical_records):
        """Run fatigue and lifestyle assessment"""
        findings = []
        recommendations = []
        risk_factors = []
        score = 100
        
        # Analyze flight schedule for fatigue risk
        if flight_logs:
            fatigue_score = self._analyze_flight_fatigue(flight_logs, findings, recommendations, risk_factors)
            score = min(score, fatigue_score)
        
        # Analyze medical records for lifestyle factors
        if medical_records:
            lifestyle_score = self._analyze_lifestyle_factors(medical_records, findings, recommendations, risk_factors)
            score = min(score, lifestyle_score)
        
        # Check for sleep disorder indicators
        sleep_score = self._check_sleep_disorders(medical_records, findings, recommendations, risk_factors)
        score = min(score, sleep_score)
        
        # Check for exercise and fitness indicators
        fitness_score = self._check_physical_fitness(medical_records, findings, recommendations, risk_factors)
        score = min(score, fitness_score)
        
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
        }
    
    def _analyze_flight_fatigue(self, flight_logs, findings, recommendations, risk_factors):
        """Analyze flight logs for fatigue indicators"""
        score = 100
        
        # Sort by date
        sorted_logs = sorted(
            [l for l in flight_logs if l.flight_date],
            key=lambda x: x.flight_date
        )
        
        # Check for consecutive duty days
        consecutive_days = 0
        max_consecutive = 0
        prev_date = None
        
        for log in sorted_logs:
            if prev_date:
                days_between = (log.flight_date - prev_date).days
                if days_between <= 1:
                    consecutive_days += 1
                else:
                    max_consecutive = max(max_consecutive, consecutive_days)
                    consecutive_days = 1
            else:
                consecutive_days = 1
            prev_date = log.flight_date
        
        max_consecutive = max(max_consecutive, consecutive_days)
        
        if max_consecutive > 10:
            score -= 25
            findings.append(f"Worked {max_consecutive} consecutive days - fatigue risk")
            risk_factors.append("Excessive consecutive duty days")
            recommendations.append("Implement mandatory rest periods")
        elif max_consecutive > 7:
            score -= 15
            findings.append(f"Worked {max_consecutive} consecutive days")
            recommendations.append("Monitor duty day limits")
        
        # Check for short rest periods
        for i in range(1, len(sorted_logs)):
            prev = sorted_logs[i-1]
            curr = sorted_logs[i]
            
            days_between = (curr.flight_date - prev.flight_date).days
            if days_between == 0:
                # Same day flights - check total hours
                total_minutes = (prev.flight_duration_minutes or 0) + (curr.flight_duration_minutes or 0)
                if total_minutes > 600:  # 10 hours
                    score -= 15
                    findings.append(f"Excessive same-day flight time: {total_minutes/60:.1f} hours")
                    risk_factors.append("Daily flight time limit exceeded")
                    break
        
        # Check for night flight frequency
        night_flights = [l for l in sorted_logs if l.night_flight]
        if len(night_flights) > len(sorted_logs) * 0.5:
            score -= 10
            findings.append("High proportion of night flights")
            risk_factors.append("Circadian rhythm disruption risk")
            recommendations.append("Monitor for fatigue from night operations")
        
        # Check for long-haul frequency
        long_haul = [l for l in sorted_logs if (l.flight_duration_minutes or 0) > 480]
        if len(long_haul) > len(sorted_logs) * 0.4:
            score -= 10
            findings.append("High proportion of long-haul flights")
            risk_factors.append("Jet lag and fatigue accumulation")
        
        return max(0, score)
    
    def _analyze_lifestyle_factors(self, medical_records, findings, recommendations, risk_factors):
        """Analyze lifestyle factors from medical records"""
        score = 100
        
        if not medical_records:
            return score
        
        latest = medical_records[0]
        
        # Alcohol consumption
        if latest.alcohol_consumption:
            if latest.alcohol_consumption == 'Heavy':
                score -= 30
                findings.append("Heavy alcohol consumption reported")
                risk_factors.append("Heavy alcohol use")
                recommendations.append("Alcohol reduction program required")
            elif latest.alcohol_consumption == 'Moderate':
                score -= 10
                findings.append("Moderate alcohol consumption")
        
        # Tobacco use
        if latest.tobacco_use == 'Current':
            score -= 15
            findings.append("Current tobacco use")
            recommendations.append("Smoking cessation program")
        
        # BMI and fitness
        if latest.bmi:
            if latest.bmi > 30:
                score -= 15
                findings.append(f"Obesity (BMI: {latest.bmi:.1f})")
                risk_factors.append("Obesity - health and fatigue risk")
                recommendations.append("Weight management program")
            elif latest.bmi > 25:
                score -= 5
                findings.append(f"Overweight (BMI: {latest.bmi:.1f})")
        
        return max(0, score)
    
    def _check_sleep_disorders(self, medical_records, findings, recommendations, risk_factors):
        """Check for sleep disorder indicators"""
        score = 100
        
        if not medical_records:
            return score
        
        latest = medical_records[0]
        
        # Check for sleep-related conditions in medical notes
        notes = (latest.notes or '').lower()
        conditions = (latest.neurological_conditions or '').lower()
        
        sleep_keywords = ['sleep apnea', 'insomnia', 'narcolepsy', 'sleep disorder', 'restless leg']
        
        for keyword in sleep_keywords:
            if keyword in notes or keyword in conditions:
                score -= 30
                findings.append(f"Sleep disorder indicator: {keyword}")
                risk_factors.append(f"Sleep disorder: {keyword}")
                recommendations.append("Sleep study and treatment required")
        
        return max(0, score)
    
    def _check_physical_fitness(self, medical_records, findings, recommendations, risk_factors):
        """Check physical fitness indicators"""
        score = 100
        
        if not medical_records:
            return score
        
        latest = medical_records[0]
        
        # Cardiovascular fitness indicators
        if latest.blood_pressure_systolic and latest.blood_pressure_diastolic:
            if latest.blood_pressure_systolic > 140 or latest.blood_pressure_diastolic > 90:
                score -= 15
                findings.append("Hypertension - cardiovascular fitness concern")
                risk_factors.append("Cardiovascular fitness concern")
        
        if latest.heart_rate and latest.heart_rate > 100:
            score -= 10
            findings.append(f"Elevated resting heart rate: {latest.heart_rate} bpm")
        
        # Mobility
        if latest.mobility_issues:
            score -= 15
            findings.append(f"Mobility issues: {latest.mobility_issues}")
            risk_factors.append("Physical mobility limitations")
        
        return max(0, score)
