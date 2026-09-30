"""
Substance Abuse Screening Module
Evaluates drug and alcohol test results and substance use patterns.
"""

from datetime import datetime, timedelta


class SubstanceAbuseScreening:
    """Screens for substance abuse risks"""
    
    def __init__(self):
        self.drug_tests = [
            'amphetamines', 'cocaine', 'opiates', 'cannabis',
            'benzodiazepines', 'pcp'
        ]
    
    def assess(self, pilot, substance_tests):
        """Run substance abuse screening assessment"""
        if not substance_tests:
            return {
                'score': 50,
                'status': 'NO_DATA',
                'findings': ['No substance test records available'],
                'recommendations': ['Conduct immediate substance screening'],
                'risk_factors': ['Unknown substance use status'],
            }
        
        findings = []
        recommendations = []
        risk_factors = []
        score = 100
        
        # Check for positive tests
        positive_tests = [t for t in substance_tests if t.overall_result == 'POSITIVE']
        if positive_tests:
            score -= 80
            findings.append(f"{len(positive_tests)} POSITIVE substance test(s)")
            risk_factors.append("Positive substance test results")
            recommendations.append("Immediate grounding and substance abuse evaluation required")
            recommendations.append("Mandatory rehabilitation program")
        
        # Check individual drug results
        for test in substance_tests:
            for drug in self.drug_tests:
                result = getattr(test, drug, None)
                if result and result == 'POSITIVE':
                    score -= 60
                    findings.append(f"POSITIVE {drug} test on {test.test_date}")
                    risk_factors.append(f"Positive {drug} test")
        
        # Check alcohol results
        positive_alcohol = [t for t in substance_tests if t.alcohol_result == 'POSITIVE']
        if positive_alcohol:
            score -= 70
            findings.append(f"{len(positive_alcohol)} positive alcohol test(s)")
            risk_factors.append("Positive alcohol test results")
            recommendations.append("Alcohol rehabilitation program required")
        
        # Check alcohol levels
        for test in substance_tests:
            if test.alcohol_level and test.alcohol_level > 0.0:
                if test.alcohol_level > 0.04:  # FAA limit
                    score -= 50
                    findings.append(f"Alcohol level {test.alcohol_level:.3f} exceeds limit on {test.test_date}")
                    risk_factors.append("Alcohol level above regulatory limit")
        
        # Check test frequency
        if len(substance_tests) < 2:
            score -= 10
            findings.append("Limited substance test history")
            recommendations.append("Increase random testing frequency")
        
        # Check test recency
        latest_test = max((t.test_date for t in substance_tests if t.test_date), default=None)
        if latest_test:
            days_since = (datetime.now().date() - latest_test).days
            if days_since > 180:
                score -= 15
                findings.append(f"Last substance test was {days_since} days ago")
                recommendations.append("Schedule substance test immediately")
            elif days_since > 90:
                score -= 5
                findings.append(f"Last substance test was {days_since} days ago")
        
        # Check test types
        test_types = set(t.test_type for t in substance_tests)
        if 'Random' not in test_types:
            score -= 10
            findings.append("No random substance tests on record")
            recommendations.append("Implement random testing program")
        
        # Check for reasonable suspicion tests
        suspicion_tests = [t for t in substance_tests if t.test_type == 'Reasonable Suspicion']
        if suspicion_tests:
            score -= 20
            findings.append(f"{len(suspicion_tests)} reasonable suspicion test(s) conducted")
            risk_factors.append("Reasonable suspicion testing triggered")
            recommendations.append("Investigate circumstances of suspicion tests")
        
        # Check verification status
        unverified = [t for t in substance_tests if not t.verified]
        if unverified:
            score -= 10
            findings.append(f"{len(unverified)} unverified test results")
            recommendations.append("Verify all test results with MRO")
        
        # Analyze patterns
        if len(substance_tests) >= 3:
            # Check for escalating pattern
            recent_tests = sorted(substance_tests, key=lambda t: t.test_date or datetime.min.date(), reverse=True)[:3]
            positive_recent = [t for t in recent_tests if t.overall_result == 'POSITIVE']
            if len(positive_recent) >= 2:
                score -= 30
                findings.append("Pattern of positive tests detected")
                risk_factors.append("Escalating substance use pattern")
        
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
            'total_tests': len(substance_tests),
            'positive_tests': len(positive_tests),
            'last_test_date': latest_test.isoformat() if latest_test else None,
            'test_types': list(test_types),
        }
