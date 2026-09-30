"""
Background Check & Security Assessment Module
Evaluates criminal history, incident reports, and security risk factors.
"""

from datetime import datetime


class BackgroundChecker:
    """Performs background and security risk assessment"""
    
    def __init__(self):
        self.critical_offenses = [
            'terrorism', 'treason', 'espionage', 'hijacking',
            'murder', 'manslaughter', 'kidnapping', 'bombing',
        ]
        
        self.serious_offenses = [
            'assault', 'battery', 'robbery', 'burglary',
            'fraud', 'embezzlement', 'drug trafficking', 'dui',
        ]
        
        self.moderate_offenses = [
            'theft', 'vandalism', 'disorderly conduct', 'trespassing',
            'reckless driving', 'domestic violence',
        ]
    
    def assess(self, pilot, incidents):
        """Run background check assessment"""
        findings = []
        recommendations = []
        risk_factors = []
        score = 100
        
        if not incidents:
            return {
                'score': 80,  # Good - no incidents
                'status': 'FIT',
                'findings': ['No incident reports on record'],
                'recommendations': ['Continue routine monitoring'],
                'risk_factors': [],
                'incident_count': 0,
            }
        
        # Analyze incidents
        critical_incidents = []
        serious_incidents = []
        moderate_incidents = []
        pilot_at_fault_count = 0
        
        for incident in incidents:
            incident_type = (incident.incident_type or '').lower()
            severity = (incident.severity or '').lower()
            
            # Categorize by severity
            if severity == 'critical' or any(offense in incident_type for offense in self.critical_offenses):
                critical_incidents.append(incident)
            elif severity == 'high' or any(offense in incident_type for offense in self.serious_offenses):
                serious_incidents.append(incident)
            elif severity == 'medium' or any(offense in incident_type for offense in self.moderate_offenses):
                moderate_incidents.append(incident)
            else:
                moderate_incidents.append(incident)  # Default to moderate
            
            if incident.pilot_at_fault:
                pilot_at_fault_count += 1
        
        # Score based on incidents
        if critical_incidents:
            score -= 80
            findings.append(f"{len(critical_incidents)} CRITICAL incident(s) on record")
            risk_factors.append("Critical incident history")
            recommendations.append("Comprehensive security review required")
        
        if serious_incidents:
            score -= len(serious_incidents) * 25
            findings.append(f"{len(serious_incidents)} serious incident(s) on record")
            risk_factors.append("Serious incident history")
            recommendations.append("Detailed incident review and corrective action plan")
        
        if moderate_incidents:
            score -= len(moderate_incidents) * 10
            findings.append(f"{len(moderate_incidents)} moderate incident(s) on record")
        
        # Check pilot fault rate
        if incidents:
            fault_rate = pilot_at_fault_count / len(incidents)
            if fault_rate > 0.5:
                score -= 20
                findings.append(f"Pilot at fault in {pilot_at_fault_count}/{len(incidents)} incidents")
                risk_factors.append("High incident fault rate")
                recommendations.append("Performance improvement plan required")
            elif fault_rate > 0.3:
                score -= 10
                findings.append(f"Pilot at fault in {pilot_at_fault_count}/{len(incidents)} incidents")
        
        # Check for open incidents
        open_incidents = [i for i in incidents if i.status == 'Open']
        if open_incidents:
            score -= 15
            findings.append(f"{len(open_incidents)} open incident(s) under investigation")
            risk_factors.append("Open incident investigations")
            recommendations.append("Resolve open incidents before clearance")
        
        # Check incident recency
        recent_incidents = [
            i for i in incidents
            if i.incident_date and (datetime.now().date() - i.incident_date).days <= 365
        ]
        if recent_incidents:
            score -= 10
            findings.append(f"{len(recent_incidents)} incident(s) in the last 12 months")
            risk_factors.append("Recent incident activity")
        
        # Check for patterns
        incident_types = [i.incident_type for i in incidents]
        from collections import Counter
        type_counts = Counter(incident_types)
        
        for inc_type, count in type_counts.items():
            if count >= 3:
                score -= 15
                findings.append(f"Pattern of {inc_type} incidents ({count} occurrences)")
                risk_factors.append(f"Recurring {inc_type} incidents")
                recommendations.append(f"Targeted training for {inc_type} prevention")
        
        # Check investigation findings
        for incident in incidents:
            if incident.investigation_findings:
                findings.append(f"Investigation finding ({incident.incident_date}): {incident.investigation_findings[:100]}")
        
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
            'incident_count': len(incidents),
            'critical_incidents': len(critical_incidents),
            'serious_incidents': len(serious_incidents),
            'moderate_incidents': len(moderate_incidents),
            'pilot_at_fault_count': pilot_at_fault_count,
            'open_incidents': len(open_incidents),
        }
