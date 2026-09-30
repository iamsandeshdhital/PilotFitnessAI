"""
Training & Certification Validation Module
Validates pilot training records, certifications, and currency requirements.
"""

from datetime import datetime, timedelta


class TrainingCertificationValidator:
    """Validates training records and certification status"""
    
    def __init__(self):
        self.required_training_types = [
            'Type Rating',
            'CRM Recurrent',
            'Upset Recovery',
            'Emergency Procedures',
            'Dangerous Goods',
            'Security Training',
        ]
    
    def assess(self, pilot, training_records):
        """Run training and certification assessment"""
        findings = []
        recommendations = []
        risk_factors = []
        score = 100
        
        # Check license validity
        if pilot.license_expiry_date:
            days_to_expiry = (pilot.license_expiry_date - datetime.now().date()).days
            if days_to_expiry < 0:
                score = 0
                findings.append(f"License EXPIRED {abs(days_to_expiry)} days ago")
                risk_factors.append("Flying with expired license")
                recommendations.append("Immediate license renewal required")
            elif days_to_expiry < 30:
                score -= 30
                findings.append(f"License expires in {days_to_expiry} days")
                recommendations.append("Renew license immediately")
            elif days_to_expiry < 90:
                score -= 10
                findings.append(f"License expires in {days_to_expiry} days")
                recommendations.append("Plan license renewal")
        
        # Check medical certificate
        if pilot.medical_expiry:
            days_to_expiry = (pilot.medical_expiry - datetime.now().date()).days
            if days_to_expiry < 0:
                score = 0
                findings.append(f"Medical certificate EXPIRED {abs(days_to_expiry)} days ago")
                risk_factors.append("Flying with expired medical certificate")
            elif days_to_expiry < 30:
                score -= 20
                findings.append(f"Medical certificate expires in {days_to_expiry} days")
        
        if not training_records:
            score -= 30
            findings.append("No training records available")
            risk_factors.append("Unknown training status")
            recommendations.append("Verify all training records")
        else:
            # Check for required training types
            completed_types = set(t.training_type for t in training_records if t.result == 'PASS')
            
            for required in self.required_training_types:
                if not any(required.lower() in ct.lower() for ct in completed_types):
                    score -= 10
                    findings.append(f"Missing required training: {required}")
                    recommendations.append(f"Complete {required} training")
            
            # Check for expired training
            expired_training = []
            for record in training_records:
                if record.expiry_date and record.expiry_date < datetime.now().date():
                    expired_training.append(record)
                    score -= 15
                    findings.append(f"Expired training: {record.training_type} (expired {record.expiry_date})")
                    risk_factors.append(f"Expired {record.training_type} certification")
                    recommendations.append(f"Renew {record.training_type} training immediately")
            
            # Check for failed training
            failed_training = [t for t in training_records if t.result == 'FAIL']
            if failed_training:
                score -= len(failed_training) * 20
                findings.append(f"{len(failed_training)} failed training attempt(s)")
                risk_factors.append("Training failure history")
                recommendations.append("Remedial training and re-evaluation required")
            
            # Check for incomplete remedial
            incomplete_remedial = [t for t in training_records if t.remedial_required and not t.remedial_completed]
            if incomplete_remedial:
                score -= 15
                findings.append(f"{len(incomplete_remedial)} incomplete remedial training(s)")
                risk_factors.append("Incomplete remedial training")
                recommendations.append("Complete all remedial training")
            
            # Check training recency
            latest_training = max((t.training_date for t in training_records if t.training_date), default=None)
            if latest_training:
                days_since = (datetime.now().date() - latest_training).days
                if days_since > 365:
                    score -= 15
                    findings.append(f"Last training was {days_since} days ago")
                    recommendations.append("Schedule recurrent training")
            
            # Check training scores
            low_scores = [t for t in training_records if t.score and t.score < 70]
            if low_scores:
                score -= len(low_scores) * 10
                findings.append(f"{len(low_scores)} training(s) with low scores")
                recommendations.append("Additional study and practice recommended")
        
        # Check type ratings match aircraft
        if pilot.aircraft_type_ratings:
            import json
            try:
                rated_aircraft = json.loads(pilot.aircraft_type_ratings)
                type_rating_training = [t for t in training_records if 'Type Rating' in (t.training_type or '')]
                for aircraft in rated_aircraft:
                    if not any(aircraft in (t.training_type or '') for t in type_rating_training):
                        score -= 10
                        findings.append(f"No type rating training found for {aircraft}")
                        risk_factors.append(f"Unverified type rating: {aircraft}")
            except (json.JSONDecodeError, TypeError):
                pass
        
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
            'training_count': len(training_records),
            'expired_training_count': len(expired_training) if training_records else 0,
            'failed_training_count': len(failed_training) if training_records else 0,
            'license_valid': pilot.license_expiry_date and pilot.license_expiry_date > datetime.now().date(),
            'medical_valid': pilot.medical_expiry and pilot.medical_expiry > datetime.now().date(),
        }
