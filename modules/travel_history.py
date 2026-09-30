"""
Travel History Analysis Module
Analyzes pilot travel patterns for security risks, unusual movements, and risk indicators.
"""

from datetime import datetime, timedelta
from collections import Counter


class TravelHistoryAnalyzer:
    """Analyzes travel history for security and fitness risk assessment"""
    
    def __init__(self):
        # High-risk countries/regions (simplified example)
        self.high_risk_destinations = [
            'SYR', 'IRQ', 'AFG', 'SOM', 'YEM', 'LBY', 'PRK', 'IRN',
        ]
        
        self.medium_risk_destinations = [
            'PAK', 'NGA', 'COL', 'VEN', 'MMR', 'RUS', 'BLR',
        ]
        
        # Concerning travel patterns
        self.concerning_patterns = {
            'frequent_high_risk': 'Frequent travel to high-risk destinations',
            'unusual_routes': 'Unusual travel routes detected',
            'last_minute': 'Frequent last-minute bookings',
            'cash_payments': 'Cash payments for travel',
            'one_way': 'One-way ticket patterns',
            'extended_stays': 'Extended stays in foreign countries',
        }
    
    def assess(self, pilot, travel_records):
        """Run travel history assessment"""
        if not travel_records:
            return {
                'score': 70,
                'status': 'NO_DATA',
                'findings': ['No travel history records available'],
                'recommendations': ['Collect travel history data'],
                'risk_factors': ['Unknown travel patterns'],
                'total_trips': 0,
            }
        
        findings = []
        recommendations = []
        risk_factors = []
        score = 100
        
        total_trips = len(travel_records)
        
        # Analyze destinations
        destinations = [t.destination for t in travel_records if t.destination]
        destination_counts = Counter(destinations)
        
        # Check for high-risk destinations
        high_risk_trips = [t for t in travel_records if t.destination in self.high_risk_destinations]
        if high_risk_trips:
            score -= 30
            findings.append(f"{len(high_risk_trips)} trip(s) to high-risk destinations")
            risk_factors.append("Travel to high-risk destinations")
            recommendations.append("Security review of high-risk travel required")
            recommendations.append("Verify purpose of travel to high-risk areas")
        
        # Check for medium-risk destinations
        medium_risk_trips = [t for t in travel_records if t.destination in self.medium_risk_destinations]
        if medium_risk_trips:
            score -= 15
            findings.append(f"{len(medium_risk_trips)} trip(s) to medium-risk destinations")
            recommendations.append("Review medium-risk travel patterns")
        
        # Check for frequent travel to same non-standard destination
        for dest, count in destination_counts.items():
            if count > 3 and dest not in ['USA', 'CAN', 'GBR', 'AUS', 'DEU', 'FRA']:
                score -= 10
                findings.append(f"Frequent travel to {dest}: {count} trips")
                risk_factors.append(f"Unusual travel pattern: {dest}")
                recommendations.append(f"Verify reasons for frequent travel to {dest}")
        
        # Check for unusual travel patterns
        pattern_score = self._analyze_travel_patterns(travel_records, findings, recommendations, risk_factors)
        score -= pattern_score
        
        # Check for travel documentation issues
        for trip in travel_records:
            if trip.visa_status and trip.visa_status == 'Expired':
                score -= 20
                findings.append(f"Travel with expired visa to {trip.destination}")
                risk_factors.append("Immigration violation")
        
        # Check for recent travel
        recent_trips = [
            t for t in travel_records
            if t.return_date and (datetime.now().date() - t.return_date).days <= 30
        ]
        if len(recent_trips) > 2:
            score -= 10
            findings.append(f"{len(recent_trips)} trips in the last 30 days")
            risk_factors.append("Excessive recent travel")
            recommendations.append("Monitor for fatigue from frequent travel")
        
        # Check for solo travel patterns
        solo_trips = [t for t in travel_records if t.companion == 'Solo']
        if len(solo_trips) > total_trips * 0.8:
            score -= 5
            findings.append("Predominantly solo travel")
        
        # Check for travel gaps (potential undisclosed travel)
        if total_trips >= 2:
            sorted_trips = sorted(travel_records, key=lambda t: t.departure_date or datetime.min.date())
            for i in range(1, len(sorted_trips)):
                prev_return = sorted_trips[i-1].return_date
                curr_departure = sorted_trips[i].departure_date
                if prev_return and curr_departure:
                    gap_days = (curr_departure - prev_return).days
                    if gap_days > 180:
                        score -= 5
                        findings.append(f"Large gap in travel records: {gap_days} days")
        
        # Check for contact with foreign nationals
        foreign_contacts = [t for t in travel_records if t.foreign_contacts]
        if foreign_contacts:
            score -= 10
            findings.append(f"{len(foreign_contacts)} trips with foreign national contacts")
            risk_factors.append("Foreign contacts reported")
            recommendations.append("Verify nature of foreign contacts")
        
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
            'total_trips': total_trips,
            'high_risk_trips': len(high_risk_trips),
            'medium_risk_trips': len(medium_risk_trips),
            'unique_destinations': len(destination_counts),
            'destinations': list(destination_counts.keys()),
        }
    
    def _analyze_travel_patterns(self, travel_records, findings, recommendations, risk_factors):
        """Analyze travel patterns for anomalies"""
        penalty = 0
        
        # Check for last-minute bookings
        last_minute_count = 0
        for trip in travel_records:
            if trip.booking_date and trip.departure_date:
                days_in_advance = (trip.departure_date - trip.booking_date).days
                if days_in_advance < 2:
                    last_minute_count += 1
        
        if last_minute_count > len(travel_records) * 0.3:
            penalty += 15
            findings.append(f"{last_minute_count} last-minute bookings detected")
            risk_factors.append("Frequent last-minute travel bookings")
        
        # Check for one-way patterns
        one_way_count = len([t for t in travel_records if t.trip_type == 'One-way'])
        if one_way_count > len(travel_records) * 0.3:
            penalty += 15
            findings.append(f"{one_way_count} one-way trips detected")
            risk_factors.append("One-way ticket pattern")
            recommendations.append("Verify return travel arrangements")
        
        # Check for extended stays
        extended_stays = []
        for trip in travel_records:
            if trip.departure_date and trip.return_date:
                duration = (trip.return_date - trip.departure_date).days
                if duration > 30:
                    extended_stays.append(trip)
        
        if extended_stays:
            penalty += 10
            findings.append(f"{len(extended_stays)} extended stay(s) (>30 days)")
            risk_factors.append("Extended foreign stays")
            recommendations.append("Verify purpose of extended stays")
        
        # Check for unusual routes (simplified)
        # In real implementation, this would use geographic analysis
        unusual_routes = self._detect_unusual_routes(travel_records)
        if unusual_routes:
            penalty += 10
            findings.append(f"{len(unusual_routes)} unusual travel route(s) detected")
            risk_factors.append("Unusual travel routes")
        
        return penalty
    
    def _detect_unusual_routes(self, travel_records):
        """Detect unusual travel routes"""
        unusual = []
        
        # Simplified: check for travel to destinations that don't match
        # the pilot's known residence or airline base
        for trip in travel_records:
            if trip.destination in self.high_risk_destinations:
                unusual.append(trip)
        
        return unusual
