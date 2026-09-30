"""
Medical Fitness Assessment Module
Evaluates pilot medical records against ICAO and FAA standards.
"""

from datetime import datetime, timedelta


class MedicalAssessment:
    """Comprehensive medical fitness evaluation"""
    
    def __init__(self):
        self.weights = {
            'vision': 15,
            'hearing': 10,
            'cardiovascular': 20,
            'respiratory': 10,
            'musculoskeletal': 10,
            'neurological': 15,
            'mental_health': 10,
            'substance': 10,
        }
    
    def assess(self, pilot, medical_records):
        """Run complete medical assessment"""
        if not medical_records:
            return {
                'score': 0,
                'status': 'NO_DATA',
                'findings': ['No medical records available'],
                'recommendations': ['Schedule immediate medical examination'],
                'risk_factors': ['Unknown medical status'],
            }
        
        latest = medical_records[0]  # Most recent exam
        findings = []
        recommendations = []
        risk_factors = []
        scores = {}
        
        # Vision Assessment
        vision_score = self._assess_vision(latest, findings, recommendations, risk_factors)
        scores['vision'] = vision_score
        
        # Hearing Assessment
        hearing_score = self._assess_hearing(latest, findings, recommendations, risk_factors)
        scores['hearing'] = hearing_score
        
        # Cardiovascular Assessment
        cardio_score = self._assess_cardiovascular(latest, findings, recommendations, risk_factors)
        scores['cardiovascular'] = cardio_score
        
        # Respiratory Assessment
        resp_score = self._assess_respiratory(latest, findings, recommendations, risk_factors)
        scores['respiratory'] = resp_score
        
        # Musculoskeletal Assessment
        musculo_score = self._assess_musculoskeletal(latest, findings, recommendations, risk_factors)
        scores['musculoskeletal'] = musculo_score
        
        # Neurological Assessment
        neuro_score = self._assess_neurological(latest, findings, recommendations, risk_factors)
        scores['neurological'] = neuro_score
        
        # Mental Health Assessment
        mental_score = self._assess_mental_health(latest, findings, recommendations, risk_factors)
        scores['mental_health'] = mental_score
        
        # Substance Assessment
        substance_score = self._assess_substance(latest, findings, recommendations, risk_factors)
        scores['substance'] = substance_score
        
        # Calculate weighted overall score
        total_weight = sum(self.weights.values())
        weighted_sum = sum(
            scores.get(key, 0) * self.weights.get(key, 0)
            for key in self.weights
        )
        overall_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Check medical certificate validity
        if pilot.medical_expiry:
            days_to_expiry = (pilot.medical_expiry - datetime.now().date()).days
            if days_to_expiry < 0:
                overall_score = 0
                findings.append(f"Medical certificate EXPIRED {abs(days_to_expiry)} days ago")
                risk_factors.append("Flying with expired medical certificate")
                recommendations.append("Immediate medical re-examination required")
            elif days_to_expiry < 30:
                overall_score *= 0.7
                findings.append(f"Medical certificate expires in {days_to_expiry} days")
                recommendations.append("Schedule medical renewal immediately")
            elif days_to_expiry < 90:
                overall_score *= 0.9
                findings.append(f"Medical certificate expires in {days_to_expiry} days")
                recommendations.append("Plan medical renewal soon")
        
        # Check exam recency
        if latest.exam_date:
            days_since_exam = (datetime.now().date() - latest.exam_date).days
            if days_since_exam > 365:
                overall_score *= 0.6
                findings.append(f"Last medical exam was {days_since_exam} days ago")
                risk_factors.append("Outdated medical examination")
                recommendations.append("Schedule annual medical examination")
            elif days_since_exam > 180:
                overall_score *= 0.85
                findings.append(f"Last medical exam was {days_since_exam} days ago")
        
        # Determine status
        if overall_score >= 80 and not risk_factors:
            status = 'FIT'
        elif overall_score >= 60:
            status = 'CONDITIONAL'
        else:
            status = 'UNFIT'
        
        # Check for critical conditions
        critical_conditions = [
            latest.epilepsy,
            latest.seizure_history,
        ]
        if any(critical_conditions):
            status = 'UNFIT'
            overall_score = min(overall_score, 20)
            findings.append("CRITICAL: Seizure history or epilepsy detected")
            risk_factors.append("Grounding condition - seizure risk")
        
        return {
            'score': round(overall_score, 1),
            'status': status,
            'findings': findings,
            'recommendations': recommendations,
            'risk_factors': risk_factors,
            'sub_scores': scores,
            'exam_date': latest.exam_date.isoformat() if latest.exam_date else None,
            'examiner': latest.examiner_name,
        }
    
    def _assess_vision(self, record, findings, recommendations, risk_factors):
        """Assess vision standards"""
        score = 100
        
        left = record.vision_left_eye or ''
        right = record.vision_right_eye or ''
        
        # Check visual acuity
        if '20/20' in left and '20/20' in right:
            pass  # Perfect
        elif '20/20' in left or '20/20' in right:
            score -= 10
            findings.append("One eye has corrected vision only")
        elif '20/40' in left and '20/40' in right:
            score -= 20
            findings.append("Vision correctable to 20/40 - meets minimum standard")
        elif '20/40' in left or '20/40' in right:
            score -= 30
            findings.append("One eye below 20/40 corrected - marginal")
            recommendations.append("Ophthalmology consultation recommended")
        else:
            score -= 50
            findings.append("Vision below acceptable standards")
            risk_factors.append("Visual acuity concerns")
            recommendations.append("Immediate ophthalmology evaluation required")
        
        # Color vision
        if record.color_vision and 'Normal' not in record.color_vision:
            score -= 25
            findings.append(f"Color vision deficiency: {record.color_vision}")
            risk_factors.append("Color vision deficiency - may affect signal light recognition")
            recommendations.append("Operational color vision test required")
        
        # Corrective lenses
        if record.corrective_lenses_required:
            score -= 5
            findings.append("Corrective lenses required - must carry spare")
            recommendations.append("Ensure backup glasses available at all times")
        
        return max(0, score)
    
    def _assess_hearing(self, record, findings, recommendations, risk_factors):
        """Assess hearing standards"""
        score = 100
        
        left = record.hearing_left_ear or ''
        right = record.hearing_right_ear or ''
        
        if 'Normal' in left and 'Normal' in right:
            pass
        elif 'Normal' in left or 'Normal' in right:
            score -= 15
            findings.append("Mild hearing loss in one ear")
        else:
            score -= 35
            findings.append("Hearing impairment in both ears")
            risk_factors.append("Hearing impairment - communication concerns")
            recommendations.append("Audiology evaluation recommended")
        
        if record.hearing_aid_required:
            score -= 20
            findings.append("Hearing aid required")
            recommendations.append("Ensure hearing aid is functional and backup available")
        
        return max(0, score)
    
    def _assess_cardiovascular(self, record, findings, recommendations, risk_factors):
        """Assess cardiovascular health"""
        score = 100
        
        # Blood pressure
        if record.blood_pressure_systolic and record.blood_pressure_diastolic:
            sys = record.blood_pressure_systolic
            dia = record.blood_pressure_diastolic
            
            if sys < 140 and dia < 90:
                pass  # Normal
            elif sys < 160 and dia < 100:
                score -= 15
                findings.append(f"Elevated blood pressure: {sys}/{dia}")
                recommendations.append("Blood pressure monitoring recommended")
            elif sys >= 160 or dia >= 100:
                score -= 40
                findings.append(f"Hypertension: {sys}/{dia}")
                risk_factors.append("Hypertension - cardiovascular risk")
                recommendations.append("Cardiology consultation required")
            else:
                score -= 10
                findings.append(f"Borderline blood pressure: {sys}/{dia}")
        
        # Heart rate
        if record.heart_rate:
            if 60 <= record.heart_rate <= 100:
                pass
            elif 50 <= record.heart_rate < 60 or 100 < record.heart_rate <= 110:
                score -= 10
                findings.append(f"Borderline heart rate: {record.heart_rate} bpm")
            else:
                score -= 25
                findings.append(f"Abnormal heart rate: {record.heart_rate} bpm")
                risk_factors.append("Cardiac rhythm concern")
                recommendations.append("Cardiology evaluation recommended")
        
        # ECG
        if record.ecg_result and 'Normal' not in record.ecg_result:
            score -= 30
            findings.append(f"ECG abnormality: {record.ecg_result}")
            risk_factors.append("ECG abnormality")
            recommendations.append("Cardiology follow-up required")
        
        # Cholesterol
        if record.cholesterol_total:
            if record.cholesterol_total < 200:
                pass
            elif record.cholesterol_total < 240:
                score -= 10
                findings.append(f"Borderline cholesterol: {record.cholesterol_total}")
            else:
                score -= 20
                findings.append(f"High cholesterol: {record.cholesterol_total}")
                risk_factors.append("Hyperlipidemia - cardiovascular risk factor")
                recommendations.append("Dietary counseling and lipid management")
        
        return max(0, score)
    
    def _assess_respiratory(self, record, findings, recommendations, risk_factors):
        """Assess respiratory health"""
        score = 100
        
        if record.lung_function_fev1 and record.lung_function_fvc:
            ratio = record.lung_function_fev1 / record.lung_function_fvc if record.lung_function_fvc > 0 else 0
            if ratio >= 0.7:
                pass
            elif ratio >= 0.6:
                score -= 20
                findings.append(f"Mildly reduced lung function (FEV1/FVC: {ratio:.2f})")
            else:
                score -= 40
                findings.append(f"Significantly reduced lung function (FEV1/FVC: {ratio:.2f})")
                risk_factors.append("Respiratory impairment")
                recommendations.append("Pulmonology evaluation recommended")
        
        if record.respiratory_conditions:
            score -= 25
            findings.append(f"Respiratory conditions: {record.respiratory_conditions}")
            risk_factors.append("Active respiratory condition")
        
        return max(0, score)
    
    def _assess_musculoskeletal(self, record, findings, recommendations, risk_factors):
        """Assess musculoskeletal health"""
        score = 100
        
        # BMI
        if record.bmi:
            if 18.5 <= record.bmi <= 24.9:
                pass
            elif 25 <= record.bmi <= 29.9:
                score -= 10
                findings.append(f"Overweight (BMI: {record.bmi:.1f})")
            elif 30 <= record.bmi <= 34.9:
                score -= 20
                findings.append(f"Obese Class I (BMI: {record.bmi:.1f})")
                risk_factors.append("Obesity - associated health risks")
                recommendations.append("Weight management program recommended")
            elif record.bmi >= 35:
                score -= 35
                findings.append(f"Obese Class II+ (BMI: {record.bmi:.1f})")
                risk_factors.append("Severe obesity - significant health risks")
                recommendations.append("Mandatory weight management program")
            elif record.bmi < 18.5:
                score -= 10
                findings.append(f"Underweight (BMI: {record.bmi:.1f})")
        
        if record.mobility_issues:
            score -= 20
            findings.append(f"Mobility issues: {record.mobility_issues}")
            risk_factors.append("Physical mobility limitations")
        
        return max(0, score)
    
    def _assess_neurological(self, record, findings, recommendations, risk_factors):
        """Assess neurological health"""
        score = 100
        
        if record.neurological_conditions and record.neurological_conditions != 'None':
            score -= 40
            findings.append(f"Neurological conditions: {record.neurological_conditions}")
            risk_factors.append("Active neurological condition")
            recommendations.append("Neurology consultation required")
        
        if record.seizure_history:
            score -= 80
            findings.append("SEIZURE HISTORY - CRITICAL")
            risk_factors.append("Seizure history - grounding condition")
        
        if record.epilepsy:
            score -= 100
            findings.append("EPILEPSY - CRITICAL")
            risk_factors.append("Epilepsy - absolute grounding condition")
        
        return max(0, score)
    
    def _assess_mental_health(self, record, findings, recommendations, risk_factors):
        """Assess mental health from medical perspective"""
        score = 100
        
        if record.psychiatric_conditions and record.psychiatric_conditions != 'None':
            score -= 35
            findings.append(f"Psychiatric conditions: {record.psychiatric_conditions}")
            risk_factors.append("Active psychiatric condition")
            recommendations.append("Psychiatric evaluation required")
        
        if record.current_medications and record.current_medications != 'None':
            score -= 15
            findings.append(f"Current medications: {record.current_medications}")
            recommendations.append("Review medication side effects on flight performance")
        
        if record.medication_side_effects and record.medication_side_effects != 'None':
            score -= 25
            findings.append(f"Medication side effects: {record.medication_side_effects}")
            risk_factors.append("Medication may impair flight performance")
        
        return max(0, score)
    
    def _assess_substance(self, record, findings, recommendations, risk_factors):
        """Assess substance use from medical perspective"""
        score = 100
        
        # Alcohol
        if record.alcohol_consumption:
            if record.alcohol_consumption == 'Never':
                pass
            elif record.alcohol_consumption == 'Occasional':
                score -= 5
            elif record.alcohol_consumption == 'Moderate':
                score -= 15
                findings.append("Moderate alcohol consumption reported")
            elif record.alcohol_consumption == 'Heavy':
                score -= 50
                findings.append("HEAVY alcohol consumption reported")
                risk_factors.append("Potential alcohol abuse")
                recommendations.append("Substance abuse evaluation required")
        
        # Tobacco
        if record.tobacco_use:
            if record.tobacco_use == 'Never':
                pass
            elif record.tobacco_use == 'Former':
                score -= 5
            elif record.tobacco_use == 'Current':
                score -= 15
                findings.append("Current tobacco use")
                recommendations.append("Smoking cessation program recommended")
        
        # Drug history
        if record.drug_use_history and record.drug_use_history != 'None':
            score -= 40
            findings.append(f"Drug use history: {record.drug_use_history}")
            risk_factors.append("History of drug use")
            recommendations.append("Substance abuse counseling recommended")
        
        # Lab results
        if record.drug_screen_result and 'NEGATIVE' not in record.drug_screen_result:
            score -= 80
            findings.append(f"POSITIVE drug screen: {record.drug_screen_result}")
            risk_factors.append("Positive drug test result")
        
        if record.alcohol_test_result and 'NEGATIVE' not in record.alcohol_test_result:
            score -= 80
            findings.append(f"POSITIVE alcohol test: {record.alcohol_test_result}")
            risk_factors.append("Positive alcohol test result")
        
        return max(0, score)
