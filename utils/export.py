"""
Export utilities for Pilot Fitness Assessment AI Tool
"""

import csv
import json
from datetime import datetime
from io import StringIO


class ReportExporter:
    """Export assessment reports in various formats"""
    
    @staticmethod
    def to_csv(data, filename=None):
        """Export data to CSV format"""
        if not data:
            return ""
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write headers
        if isinstance(data, list) and len(data) > 0:
            headers = data[0].keys()
            writer.writerow(headers)
            
            # Write data
            for row in data:
                writer.writerow([row.get(h, '') for h in headers])
        
        return output.getvalue()
    
    @staticmethod
    def to_json(data, indent=2):
        """Export data to JSON format"""
        return json.dumps(data, indent=indent, default=str)
    
    @staticmethod
    def assessment_to_dict(assessment, pilot, module_results):
        """Convert assessment to dictionary for export"""
        return {
            'assessment_id': assessment.id,
            'assessment_date': assessment.assessment_date.isoformat(),
            'pilot_id': pilot.pilot_id,
            'pilot_name': pilot.full_name,
            'license_number': pilot.license_number,
            'airline': pilot.airline,
            'overall_score': assessment.overall_score,
            'fitness_status': assessment.fitness_status,
            'risk_level': assessment.risk_level,
            'module_scores': {
                'medical': assessment.medical_score,
                'psychological': assessment.psychological_score,
                'social_media': assessment.social_media_score,
                'socio_political_economic': assessment.socio_political_economic_score,
                'staff_feedback': assessment.staff_feedback_score,
                'flight_history': assessment.flight_history_score,
                'substance_abuse': assessment.substance_abuse_score,
                'financial_stability': assessment.financial_stability_score,
                'background_check': assessment.background_check_score,
                'fatigue_lifestyle': assessment.fatigue_lifestyle_score,
                'training_certification': assessment.training_certification_score,
                'travel_history': assessment.travel_history_score,
                'behavior_pattern': assessment.behavior_pattern_score,
                'digital_footprint': assessment.digital_footprint_score,
                'radicalization': assessment.radicalization_score,
            },
            'red_flags': json.loads(assessment.red_flags) if assessment.red_flags else [],
            'recommendations': json.loads(assessment.recommendations) if assessment.recommendations else [],
            'conditions': json.loads(assessment.conditions) if assessment.conditions else [],
            'assessed_by': assessment.assessed_by,
        }
    
    @staticmethod
    def generate_summary_report(assessments):
        """Generate summary report from multiple assessments"""
        if not assessments:
            return {}
        
        total = len(assessments)
        fit_count = sum(1 for a in assessments if a.fitness_status == 'FIT')
        conditional_count = sum(1 for a in assessments if a.fitness_status == 'CONDITIONAL')
        unfit_count = sum(1 for a in assessments if a.fitness_status == 'UNFIT')
        
        avg_score = sum(a.overall_score or 0 for a in assessments) / total
        
        risk_distribution = {
            'LOW': sum(1 for a in assessments if a.risk_level == 'LOW'),
            'MEDIUM': sum(1 for a in assessments if a.risk_level == 'MEDIUM'),
            'HIGH': sum(1 for a in assessments if a.risk_level == 'HIGH'),
            'CRITICAL': sum(1 for a in assessments if a.risk_level == 'CRITICAL'),
        }
        
        return {
            'report_date': datetime.utcnow().isoformat(),
            'total_assessments': total,
            'fitness_distribution': {
                'FIT': fit_count,
                'CONDITIONAL': conditional_count,
                'UNFIT': unfit_count,
            },
            'average_score': round(avg_score, 1),
            'risk_distribution': risk_distribution,
        }
