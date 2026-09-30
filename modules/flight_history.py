"""
Flight History Analysis Module
Analyzes pilot flight logs, patterns, and performance indicators.
"""

from datetime import datetime, timedelta
from collections import Counter


class FlightHistoryAnalyzer:
    """Analyzes flight history for fitness assessment"""
    
    def __init__(self):
        self.max_daily_flight_hours = 14  # Regulatory limit
        self.max_weekly_flight_hours = 60
        self.max_monthly_flight_hours = 100
    
    def assess(self, pilot, flight_logs):
        """Run flight history assessment"""
        if not flight_logs:
            return {
                'score': 50,
                'status': 'NO_DATA',
                'findings': ['No flight logs available'],
                'recommendations': ['Verify flight history records'],
                'risk_factors': ['Unknown flight history'],
            }
        
        findings = []
        recommendations = []
        risk_factors = []
        score = 100
        
        # Check total flight hours vs claimed
        logged_hours = sum(
            (log.flight_duration_minutes or 0) / 60
            for log in flight_logs
        )
        
        if pilot.total_flight_hours > 0:
            discrepancy = abs(pilot.total_flight_hours - logged_hours)
            if discrepancy > pilot.total_flight_hours * 0.2:
                score -= 20
                findings.append(f"Flight hour discrepancy: claimed {pilot.total_flight_hours}, logged {logged_hours:.0f}")
                risk_factors.append("Flight log discrepancy")
                recommendations.append("Audit flight logs for accuracy")
        
        # Analyze flight patterns
        daily_hours = self._calculate_daily_hours(flight_logs)
        for date, hours in daily_hours.items():
            if hours > self.max_daily_flight_hours:
                score -= 15
                findings.append(f"Excessive flight hours on {date}: {hours:.1f} hours")
                risk_factors.append("Flight time limitation violation")
                recommendations.append("Review flight time compliance")
                break
        
        # Check for fatigue indicators
        fatigue_indicators = self._check_fatigue_indicators(flight_logs)
        if fatigue_indicators:
            score -= fatigue_indicators * 10
            findings.append(f"{fatigue_indicators} potential fatigue indicators in flight schedule")
            risk_factors.append("Fatigue risk indicators")
            recommendations.append("Fatigue risk management training")
        
        # Check for incidents in flight logs
        incident_logs = [log for log in flight_logs if log.incidents and log.incidents != 'None']
        if incident_logs:
            score -= len(incident_logs) * 10
            findings.append(f"{len(incident_logs)} flights with reported incidents")
            risk_factors.append("Multiple flight incidents")
            recommendations.append("Review incident patterns and provide additional training")
        
        # Check recency of flying
        if flight_logs:
            latest_flight = max(log.flight_date for log in flight_logs if log.flight_date)
            days_since_flight = (datetime.now().date() - latest_flight).days
            
            if days_since_flight > 90:
                score -= 25
                findings.append(f"No flights in {days_since_flight} days - skill degradation risk")
                risk_factors.append("Extended flight inactivity")
                recommendations.append("Recency training and check ride required")
            elif days_since_flight > 30:
                score -= 10
                findings.append(f"Last flight was {days_since_flight} days ago")
                recommendations.append("Ensure recent flight experience")
        
        # Check aircraft type diversity
        aircraft_types = set(log.aircraft_type for log in flight_logs if log.aircraft_type)
        if len(aircraft_types) == 1 and len(flight_logs) > 20:
            score -= 5
            findings.append("Limited aircraft type experience")
        
        # Check for night flying currency
        night_flights = [log for log in flight_logs if log.night_flight]
        if len(night_flights) < 3 and len(flight_logs) > 20:
            score -= 5
            findings.append("Limited night flying experience")
        
        # Check for instrument currency
        instrument_flights = [log for log in flight_logs if (log.instrument_time or 0) > 0]
        if len(instrument_flights) < 5 and len(flight_logs) > 20:
            score -= 10
            findings.append("Limited instrument flight experience")
            recommendations.append("Instrument proficiency check recommended")
        
        # Analyze route familiarity
        routes = Counter()
        for log in flight_logs:
            if log.departure_airport and log.arrival_airport:
                route = f"{log.departure_airport}-{log.arrival_airport}"
                routes[route] += 1
        
        if routes and routes.most_common(1)[0][1] > len(flight_logs) * 0.8:
            score -= 5
            findings.append("Limited route diversity")
        
        # Check for weather-related concerns
        imc_flights = [log for log in flight_logs if log.weather_conditions and 'IMC' in log.weather_conditions]
        if len(imc_flights) < 3 and len(flight_logs) > 30:
            score -= 5
            findings.append("Limited IMC experience")
        
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
            'total_logged_hours': round(logged_hours, 1),
            'flight_count': len(flight_logs),
            'aircraft_types': list(aircraft_types),
            'night_flights': len(night_flights),
            'instrument_flights': len(instrument_flights),
            'incident_count': len(incident_logs),
        }
    
    def _calculate_daily_hours(self, flight_logs):
        """Calculate flight hours per day"""
        daily = {}
        for log in flight_logs:
            if log.flight_date and log.flight_duration_minutes:
                date_str = log.flight_date.isoformat()
                daily[date_str] = daily.get(date_str, 0) + (log.flight_duration_minutes / 60)
        return daily
    
    def _check_fight_fatigue_indicators(self, flight_logs):
        """Check for fatigue indicators in flight schedule"""
        indicators = 0
        
        # Sort by date
        sorted_logs = sorted(
            [l for l in flight_logs if l.flight_date],
            key=lambda x: x.flight_date
        )
        
        for i in range(1, len(sorted_logs)):
            prev = sorted_logs[i-1]
            curr = sorted_logs[i]
            
            # Check for consecutive long flights
            if (prev.flight_duration_minutes or 0) > 360 and (curr.flight_duration_minutes or 0) > 360:
                days_between = (curr.flight_date - prev.flight_date).days
                if days_between < 1:
                    indicators += 1
            
            # Check for rapid timezone changes (simplified)
            if prev.arrival_airport and curr.departure_airport:
                if prev.arrival_airport != curr.departure_airport:
                    days_between = (curr.flight_date - prev.flight_date).days
                    if days_between < 1:
                        indicators += 1
        
        return indicators
