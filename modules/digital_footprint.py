"""
Digital Footprint Analysis Module
Analyzes pilot's digital activities including:
- Phone usage and call patterns
- Laptop and device activity
- Email communications
- Browsing history
- Text messages and communications
- App usage
- Location data from devices
- Social media interactions
"""

import re
from datetime import datetime, timedelta
from collections import Counter


class DigitalFootprintAnalyzer:
    """Analyzes digital footprint for security and fitness risks"""
    
    def __init__(self):
        # Risk keywords for communications
        self.concerning_keywords = {
            'suicide': 'Suicidal ideation detected',
            'kill myself': 'Suicidal ideation detected',
            'end it all': 'Suicidal ideation detected',
            'no reason to live': 'Depression indicator',
            'hopeless': 'Depression indicator',
            'worthless': 'Depression indicator',
            'better off dead': 'Suicidal ideation detected',
        }
        
        self.security_keywords = {
            'hack': 'Hacking-related content',
            'exploit': 'Exploit-related content',
            'bypass security': 'Security bypass intent',
            'disable camera': 'Surveillance avoidance',
            'cover tracks': 'Concealment behavior',
            'delete evidence': 'Evidence destruction intent',
            'leak': 'Information leaking concern',
            'whistleblower': 'Whistleblower indicators',
        }
        
        self.substance_keywords = {
            'buy drugs': 'Drug purchase inquiry',
            'sell drugs': 'Drug distribution',
            'high': 'Drug use reference',
            'dealer': 'Drug dealer contact',
            'pills': 'Drug reference',
        }
        
        self.financial_fraud_keywords = {
            'money laundering': 'Money laundering reference',
            'offshore account': 'Offshore account reference',
            'tax evasion': 'Tax evasion reference',
            'fake invoice': 'Fraud indicator',
            'embezzle': 'Embezzlement reference',
        }
        
        # Concerning browsing categories
        self.concerning_browsing = {
            'suicide_methods': 'Suicide method research',
            'weapon_purchase': 'Weapon purchase research',
            'bomb_making': 'Explosive research',
            'hacking_tutorials': 'Hacking tutorial access',
            'dark_web': 'Dark web access',
            'extremist_content': 'Extremist content access',
            'drug_markets': 'Drug market access',
        }
        
        # Unusual calling patterns
        self.suspicious_contacts = {
            'known_criminal': 'Contact with known criminal',
            'foreign_agent': 'Suspected foreign agent contact',
            'extremist': 'Extremist group contact',
        }
    
    def assess(self, pilot, phone_records, email_records, browsing_history, 
               message_records, device_records, location_data):
        """Run comprehensive digital footprint assessment"""
        findings = []
        recommendations = []
        risk_factors = []
        score = 100
        
        # Analyze phone records
        if phone_records:
            phone_score = self._analyze_phone_records(phone_records, findings, recommendations, risk_factors)
            score = min(score, phone_score)
        
        # Analyze email records
        if email_records:
            email_score = self._analyze_email_records(email_records, findings, recommendations, risk_factors)
            score = min(score, email_score)
        
        # Analyze browsing history
        if browsing_history:
            browsing_score = self._analyze_browsing_history(browsing_history, findings, recommendations, risk_factors)
            score = min(score, browsing_score)
        
        # Analyze message records
        if message_records:
            message_score = self._analyze_message_records(message_records, findings, recommendations, risk_factors)
            score = min(score, message_score)
        
        # Analyze device records
        if device_records:
            device_score = self._analyze_device_records(device_records, findings, recommendations, risk_factors)
            score = min(score, device_score)
        
        # Analyze location data
        if location_data:
            location_score = self._analyze_location_data(location_data, findings, recommendations, risk_factors)
            score = min(score, location_score)
        
        # Cross-reference analysis
        cross_ref_score = self._cross_reference_analysis(
            phone_records, email_records, browsing_history, message_records,
            findings, recommendations, risk_factors
        )
        score -= cross_ref_score
        
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
            'modules_analyzed': sum([
                bool(phone_records), bool(email_records), bool(browsing_history),
                bool(message_records), bool(device_records), bool(location_data)
            ]),
        }
    
    def _analyze_phone_records(self, phone_records, findings, recommendations, risk_factors):
        """Analyze phone call records"""
        score = 100
        
        # Check for calls to suspicious numbers
        suspicious_calls = []
        for record in phone_records:
            if record.contact_type in self.suspicious_contacts:
                suspicious_calls.append(record)
                risk_factors.append(self.suspicious_contacts[record.contact_type])
        
        if suspicious_calls:
            score -= 30
            findings.append(f"{len(suspicious_calls)} calls to suspicious contacts")
        
        # Check for unusual calling patterns
        late_night_calls = [
            r for r in phone_records
            if r.call_time and (r.call_time.hour >= 0 and r.call_time.hour <= 5)
        ]
        if len(late_night_calls) > len(phone_records) * 0.3:
            score -= 15
            findings.append("Frequent late-night calls")
            risk_factors.append("Unusual calling hours")
        
        # Check for calls to unknown international numbers
        intl_calls = [r for r in phone_records if r.is_international]
        if len(intl_calls) > len(phone_records) * 0.2:
            score -= 10
            findings.append(f"{len(intl_calls)} international calls")
            recommendations.append("Verify international contacts")
        
        # Check for very short calls (possible dead drops)
        short_calls = [r for r in phone_records if r.duration_seconds and r.duration_seconds < 10]
        if len(short_calls) > len(phone_records) * 0.1:
            score -= 15
            findings.append("Pattern of very short calls")
            risk_factors.append("Suspicious call pattern")
        
        # Check for calls to/from known associates
        associate_calls = [r for r in phone_records if r.is_known_associate]
        if len(associate_calls) > len(phone_records) * 0.5:
            score -= 10
            findings.append("High volume of calls to known associates")
        
        # Check for burner phone indicators
        prepaid_calls = [r for r in phone_records if r.is_prepaid]
        if prepaid_calls:
            score -= 20
            findings.append("Calls to/from prepaid numbers")
            risk_factors.append("Prepaid phone contact")
        
        return max(0, score)
    
    def _analyze_email_records(self, email_records, findings, recommendations, risk_factors):
        """Analyze email communications"""
        score = 100
        
        # Check for concerning content
        for email in email_records:
            content = (email.subject + ' ' + (email.body or '')).lower()
            
            for keyword, message in self.concerning_keywords.items():
                if keyword in content:
                    score -= 40
                    findings.append(f"Concerning email content: {message}")
                    risk_factors.append(message)
                    recommendations.append("Mental health evaluation required")
            
            for keyword, message in self.security_keywords.items():
                if keyword in content:
                    score -= 30
                    findings.append(f"Security concern in email: {message}")
                    risk_factors.append(message)
            
            for keyword, message in self.financial_fraud_keywords.items():
                if keyword in content:
                    score -= 35
                    findings.append(f"Financial fraud indicator: {message}")
                    risk_factors.append(message)
        
        # Check for external communications
        external_emails = [e for e in email_records if not e.is_internal]
        if len(external_emails) > len(email_records) * 0.5:
            score -= 10
            findings.append("High volume of external email communications")
        
        # Check for encrypted emails
        encrypted_emails = [e for e in email_records if e.is_encrypted]
        if len(encrypted_emails) > len(email_records) * 0.3:
            score -= 15
            findings.append("Frequent use of encrypted email")
            risk_factors.append("Encrypted communications")
        
        # Check for large attachments
        large_attachments = [e for e in email_records if e.has_large_attachment]
        if large_attachments:
            score -= 10
            findings.append(f"{len(large_attachments)} emails with large attachments")
            risk_factors.append("Potential data exfiltration")
        
        # Check for emails to personal accounts
        personal_emails = [e for e in email_records if e.to_personal_account]
        if personal_emails:
            score -= 15
            findings.append("Work emails sent to personal accounts")
            risk_factors.append("Data handling concern")
        
        return max(0, score)
    
    def _analyze_browsing_history(self, browsing_history, findings, recommendations, risk_factors):
        """Analyze web browsing history"""
        score = 100
        
        # Check for concerning content
        for record in browsing_history:
            url = (record.url or '').lower()
            category = (record.category or '').lower()
            
            for key, message in self.concerning_browsing.items():
                if key in category or key.replace('_', ' ') in url:
                    score -= 40
                    findings.append(f"Concerning browsing: {message}")
                    risk_factors.append(message)
            
            # Check for dark web access
            if 'tor' in url or 'onion' in url or 'darkweb' in url:
                score -= 50
                findings.append("Dark web access detected")
                risk_factors.append("Dark web access")
                recommendations.append("Immediate security review required")
            
            # Check for extremist content
            if any(term in url for term in ['extremist', 'radical', 'jihad', 'neo-nazi']):
                score -= 50
                findings.append("Extremist content access detected")
                risk_factors.append("Extremist content access")
        
        # Check for excessive browsing during work hours
        work_hours_browsing = [
            r for r in browsing_history
            if r.access_time and 9 <= r.access_time.hour <= 17
            and r.is_non_work_related
        ]
        if len(work_hours_browsing) > len(browsing_history) * 0.5:
            score -= 10
            findings.append("Excessive non-work browsing during work hours")
        
        # Check for news/political content
        political_browsing = [r for r in browsing_history if r.is_political_content]
        if len(political_browsing) > len(browsing_history) * 0.3:
            score -= 5
            findings.append("High volume of political content browsing")
        
        # Check for job search activity
        job_search = [r for r in browsing_history if r.is_job_search]
        if job_search:
            score -= 10
            findings.append("Job search activity detected")
            risk_factors.append("Potential disengagement from current role")
        
        # Check for financial stress indicators
        financial_stress = [r for r in browsing_history if r.is_financial_stress]
        if financial_stress:
            score -= 10
            findings.append("Financial stress-related browsing")
            risk_factors.append("Financial stress indicators")
        
        return max(0, score)
    
    def _analyze_message_records(self, message_records, findings, recommendations, risk_factors):
        """Analyze text messages and chat records"""
        score = 100
        
        for message in message_records:
            content = (message.content or '').lower()
            
            # Check for concerning content
            for keyword, message_text in self.concerning_keywords.items():
                if keyword in content:
                    score -= 40
                    findings.append(f"Concerning message: {message_text}")
                    risk_factors.append(message_text)
            
            # Check for substance-related content
            for keyword, message_text in self.substance_keywords.items():
                if keyword in content:
                    score -= 25
                    findings.append(f"Substance-related message: {message_text}")
                    risk_factors.append(message_text)
            
            # Check for security concerns
            for keyword, message_text in self.security_keywords.items():
                if keyword in content:
                    score -= 30
                    findings.append(f"Security concern in message: {message_text}")
                    risk_factors.append(message_text)
        
        # Check for messages to unknown contacts
        unknown_contacts = [m for m in message_records if m.is_unknown_contact]
        if len(unknown_contacts) > len(message_records) * 0.3:
            score -= 15
            findings.append("Messages to unknown contacts")
            risk_factors.append("Unknown contacts in messages")
        
        # Check for deleted messages
        deleted_messages = [m for m in message_records if m.is_deleted]
        if len(deleted_messages) > len(message_records) * 0.1:
            score -= 15
            findings.append("Pattern of deleted messages")
            risk_factors.append("Message deletion behavior")
        
        # Check for encrypted messaging apps
        encrypted_apps = [m for m in message_records if m.is_encrypted_app]
        if encrypted_apps:
            score -= 10
            findings.append("Use of encrypted messaging apps")
        
        # Check for late-night messaging
        late_night_msgs = [
            m for m in message_records
            if m.message_time and (m.message_time.hour >= 0 and m.message_time.hour <= 5)
        ]
        if len(late_night_msgs) > len(message_records) * 0.2:
            score -= 10
            findings.append("Frequent late-night messaging")
        
        return max(0, score)
    
    def _analyze_device_records(self, device_records, findings, recommendations, risk_factors):
        """Analyze device usage records"""
        score = 100
        
        # Check for unauthorized devices
        unauthorized = [d for d in device_records if not d.is_authorized]
        if unauthorized:
            score -= 25
            findings.append(f"{len(unauthorized)} unauthorized device(s) detected")
            risk_factors.append("Unauthorized device usage")
        
        # Check for device tampering
        tampered = [d for d in device_records if d.is_tampered]
        if tampered:
            score -= 40
            findings.append("Device tampering detected")
            risk_factors.append("Device tampering")
            recommendations.append("Security investigation required")
        
        # Check for VPN usage
        vpn_usage = [d for d in device_records if d.uses_vpn]
        if vpn_usage:
            score -= 15
            findings.append("VPN usage detected")
            risk_factors.append("VPN usage - possible concealment")
        
        # Check for factory resets
        factory_resets = [d for d in device_records if d.has_factory_reset]
        if factory_resets:
            score -= 20
            findings.append("Factory reset detected on device")
            risk_factors.append("Device reset - possible data destruction")
        
        # Check for multiple devices
        unique_devices = set(d.device_id for d in device_records)
        if len(unique_devices) > 3:
            score -= 10
            findings.append(f"Multiple devices detected: {len(unique_devices)}")
        
        # Check for device sharing
        shared_devices = [d for d in device_records if d.is_shared]
        if shared_devices:
            score -= 15
            findings.append("Device sharing detected")
            risk_factors.append("Shared device usage")
        
        # Check for outdated security
        outdated_security = [d for d in device_records if d.has_outdated_security]
        if outdated_security:
            score -= 10
            findings.append("Outdated security software on devices")
        
        return max(0, score)
    
    def _analyze_location_data(self, location_data, findings, recommendations, risk_factors):
        """Analyze location data from devices"""
        score = 100
        
        # Check for unusual locations
        unusual_locations = [l for l in location_data if l.is_unusual]
        if unusual_locations:
            score -= 20
            findings.append(f"{len(unusual_locations)} unusual location(s) detected")
            risk_factors.append("Unusual location patterns")
        
        # Check for high-risk area visits
        high_risk_visits = [l for l in location_data if l.is_high_risk_area]
        if high_risk_visits:
            score -= 30
            findings.append(f"{len(high_risk_visits)} visit(s) to high-risk areas")
            risk_factors.append("High-risk area visits")
        
        # Check for location spoofing
        spoofed = [l for l in location_data if l.is_spoofed]
        if spoofed:
            score -= 50
            findings.append("Location spoofing detected")
            risk_factors.append("Location spoofing")
            recommendations.append("Immediate security investigation required")
        
        # Check for missing location data (possible disable)
        missing_data = [l for l in location_data if l.has_gap]
        if missing_data:
            score -= 15
            findings.append("Gaps in location data")
            risk_factors.append("Location data gaps")
        
        # Check for border crossings
        border_crossings = [l for l in location_data if l.is_border_crossing]
        if border_crossings:
            score -= 10
            findings.append(f"{len(border_crossings)} border crossing(s) detected")
        
        # Check for consistent location patterns
        if location_data:
            locations = [l.location for l in location_data if l.location]
            location_counts = Counter(locations)
            if location_counts.most_common(1)[0][1] > len(location_data) * 0.8:
                score -= 5
                findings.append("Very limited location diversity")
        
        return max(0, score)
    
    def _cross_reference_analysis(self, phone_records, email_records, browsing_history,
                                   message_records, findings, recommendations, risk_factors):
        """Cross-reference data from multiple sources"""
        penalty = 0
        
        # Check for coordinated concerning activity
        concerning_timestamps = []
        
        for record in (phone_records or []):
            if record.contact_type in self.suspicious_contacts:
                concerning_timestamps.append(record.call_time)
        
        for record in (message_records or []):
            content = (record.content or '').lower()
            if any(kw in content for kw in self.concerning_keywords):
                concerning_timestamps.append(record.message_time)
        
        # Check for clustered concerning activity
        if len(concerning_timestamps) >= 3:
            concerning_timestamps.sort()
            for i in range(len(concerning_timestamps) - 2):
                time_diff = concerning_timestamps[i+2] - concerning_timestamps[i]
                if time_diff <= timedelta(hours=24):
                    penalty += 20
                    findings.append("Clustered concerning digital activity detected")
                    risk_factors.append("Coordinated concerning behavior")
                    break
        
        # Check for attempts to conceal digital activity
        deletion_indicators = 0
        for record in (message_records or []):
            if record.is_deleted:
                deletion_indicators += 1
        for record in (browsing_history or []):
            if record.is_cleared:
                deletion_indicators += 1
        
        if deletion_indicators > 5:
            penalty += 15
            findings.append("Pattern of clearing digital activity")
            risk_factors.append("Digital concealment behavior")
        
        return penalty
