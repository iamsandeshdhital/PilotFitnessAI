"""
Overall Scoring Engine
Combines all module scores into a comprehensive fitness assessment.
"""


class OverallScoringEngine:
    """Calculates overall fitness score from all module results"""
    
    def __init__(self):
        # Module weights (must sum to 1.0)
        self.module_weights = {
            'medical': 0.15,
            'psychological': 0.12,
            'social_media': 0.08,
            'socio_political_economic': 0.06,
            'staff_feedback': 0.10,
            'flight_history': 0.10,
            'substance_abuse': 0.10,
            'financial_stability': 0.06,
            'background_check': 0.08,
            'fatigue_lifestyle': 0.05,
            'training_certification': 0.10,
        }
        
        # Critical modules - failure in these is automatic unfit
        self.critical_modules = ['medical', 'psychological', 'substance_abuse', 'training_certification']
        
        # Risk level thresholds
        self.risk_thresholds = {
            'LOW': 80,
            'MEDIUM': 60,
            'HIGH': 40,
            'CRITICAL': 0,
        }
    
    def calculate(self, module_results):
        """Calculate overall fitness score and status"""
        # Calculate weighted score
        weighted_sum = 0
        total_weight = 0
        
        for module_name, weight in self.module_weights.items():
            if module_name in module_results:
                module_score = module_results[module_name].get('score', 0)
                weighted_sum += module_score * weight
                total_weight += weight
        
        overall_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Collect all risk factors
        all_risk_factors = []
        all_recommendations = []
        all_conditions = []
        
        for module_name, result in module_results.items():
            all_risk_factors.extend(result.get('risk_factors', []))
            all_recommendations.extend(result.get('recommendations', []))
        
        # Check for critical module failures
        critical_failures = []
        for module_name in self.critical_modules:
            if module_name in module_results:
                module_status = module_results[module_name].get('status', '')
                if module_status == 'UNFIT':
                    critical_failures.append(module_name)
                    overall_score = min(overall_score, 30)
        
        # Determine fitness status
        if critical_failures:
            fitness_status = 'UNFIT'
            all_risk_factors.append(f"Critical module failure: {', '.join(critical_failures)}")
        elif overall_score >= 80 and not all_risk_factors:
            fitness_status = 'FIT'
        elif overall_score >= 60:
            fitness_status = 'CONDITIONAL'
            # Generate conditions for conditional fitness
            all_conditions = self._generate_conditions(module_results)
        else:
            fitness_status = 'UNFIT'
        
        # Determine risk level
        risk_level = self._determine_risk_level(overall_score, all_risk_factors)
        
        # Add critical failures to risk factors
        if critical_failures:
            all_risk_factors.insert(0, f"CRITICAL: Failed {', '.join(critical_failures)}")
        
        return {
            'overall_score': round(overall_score, 1),
            'fitness_status': fitness_status,
            'risk_level': risk_level,
            'red_flags': all_risk_factors,
            'recommendations': list(set(all_recommendations)),  # Remove duplicates
            'conditions': all_conditions,
            'critical_failures': critical_failures,
            'module_scores': {
                name: result.get('score', 0)
                for name, result in module_results.items()
            },
        }
    
    def _determine_risk_level(self, score, risk_factors):
        """Determine risk level based on score and risk factors"""
        # Count severity of risk factors
        critical_count = sum(1 for rf in risk_factors if 'CRITICAL' in rf or 'EXTREMIST' in rf)
        high_count = sum(1 for rf in risk_factors if 'HIGH' in rf or 'Severe' in rf)
        
        if critical_count > 0 or score < 20:
            return 'CRITICAL'
        elif high_count > 0 or score < 40:
            return 'HIGH'
        elif score < 60 or len(risk_factors) > 3:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _generate_conditions(self, module_results):
        """Generate conditions for conditional fitness"""
        conditions = []
        
        for module_name, result in module_results.items():
            if result.get('status') == 'CONDITIONAL':
                conditions.append({
                    'module': module_name,
                    'condition': f"Improve {module_name} score above 80",
                    'deadline_days': 90,
                })
            
            # Add specific conditions based on findings
            for rec in result.get('recommendations', []):
                if 'immediate' in rec.lower() or 'required' in rec.lower():
                    conditions.append({
                        'module': module_name,
                        'condition': rec,
                        'deadline_days': 30,
                    })
        
        return conditions
