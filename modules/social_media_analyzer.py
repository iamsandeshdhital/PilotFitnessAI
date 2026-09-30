"""
Social Media Behavior Analysis Module
Analyzes pilot social media posts for risk indicators, sentiment, and behavioral patterns.
"""

import re
from datetime import datetime, timedelta


class SocialMediaAnalyzer:
    """Analyzes social media content for safety and security risks"""
    
    def __init__(self):
        # Risk keyword dictionaries
        self.profanity_patterns = [
            r'\b(damn|hell|shit|fuck|bitch|bastard|ass|crap|piss)\b',
        ]
        
        self.violence_patterns = [
            r'\b(kill|murder|shoot|stab|bomb|attack|fight|punch|weapon|gun|knife)\b',
            r'\b(threat|revenge|destroy|hurt|harm)\b',
        ]
        
        self.extremist_patterns = [
            r'\b(jihad|isis|al-qaeda|terrorist|radical|extremist|martyr)\b',
            r'\b(white power|neo-nazi|supremacist|ethnic cleansing)\b',
            r'\b(overthrow|revolution|insurgent|militia)\b',
        ]
        
        self.discriminatory_patterns = [
            r'\b(racist|sexist|homophobic|xenophobic|nazi|fascist)\b',
            r'\b(slur|offensive term)\b',
            r'\b(hate|inferior|subhuman)\b',
        ]
        
        self.alcohol_drug_patterns = [
            r'\b(drunk|wasted|high|stoned|beer|vodka|whiskey|cocaine|weed|marijuana)\b',
            r'\b(party|bar hop|hangover|binge drink)\b',
        ]
        
        self.confidential_patterns = [
            r'\b(confidential|classified|internal only|do not share|secret)\b',
            r'\b(flight plan|security protocol|passenger manifest|crew schedule)\b',
        ]
        
        self.risk_indicator_patterns = [
            r'\b(hate my job|quit flying|done with this|can\'t take it)\b',
            r'\b(stressed|depressed|anxious|overwhelmed|burnout|exhausted)\b',
            r'\b(fired|terminated|suspended|grounded|in trouble)\b',
            r'\b(lawsuit|legal action|lawyer|sue)\b',
            r'\b(divorce|relationship problems|family issues)\b',
            r'\b(debt|broke|can\'t afford|financial problems)\b',
            r'\b(sick|tired|not feeling well|medical)\b',
        ]
        
        self.negative_sentiment_words = [
            'hate', 'angry', 'furious', 'disgusted', 'terrible', 'awful',
            'worst', 'horrible', 'disappointed', 'frustrated', 'annoyed',
            'sad', 'depressed', 'anxious', 'worried', 'stressed', 'upset',
            'disgusting', 'pathetic', 'useless', 'stupid', 'idiot', 'dumb',
        ]
        
        self.positive_sentiment_words = [
            'love', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'best', 'awesome', 'brilliant', 'outstanding', 'superb', 'perfect',
            'happy', 'joy', 'excited', 'grateful', 'blessed', 'proud',
        ]
    
    def assess(self, pilot, social_posts):
        """Run complete social media assessment"""
        if not social_posts:
            return {
                'score': 50,  # Neutral - no data
                'status': 'NO_DATA',
                'findings': ['No social media data available for analysis'],
                'recommendations': ['Monitor social media presence'],
                'risk_factors': ['Unknown social media behavior'],
                'total_posts_analyzed': 0,
                'flagged_posts': 0,
            }
        
        findings = []
        recommendations = []
        risk_factors = []
        
        total_posts = len(social_posts)
        flagged_posts = [p for p in social_posts if p.flagged]
        negative_posts = [p for p in social_posts if p.sentiment_label == 'Negative']
        positive_posts = [p for p in social_posts if p.sentiment_label == 'Positive']
        
        # Calculate base score
        score = 100
        
        # Penalize flagged posts
        if flagged_posts:
            flag_ratio = len(flagged_posts) / total_posts
            score -= flag_ratio * 50
            findings.append(f"{len(flagged_posts)} out of {total_posts} posts flagged for review")
            risk_factors.append(f"{len(flagged_posts)} flagged social media posts")
        
        # Analyze sentiment distribution
        if negative_posts:
            neg_ratio = len(negative_posts) / total_posts
            if neg_ratio > 0.5:
                score -= 25
                findings.append(f"Predominantly negative sentiment ({len(negative_posts)}/{total_posts} posts)")
                risk_factors.append("Predominantly negative social media presence")
                recommendations.append("Stress management and counseling recommended")
            elif neg_ratio > 0.3:
                score -= 15
                findings.append(f"High negative sentiment ratio ({len(negative_posts)}/{total_posts} posts)")
                recommendations.append("Monitor for signs of stress or dissatisfaction")
        
        # Check for specific risk categories
        violence_posts = [p for p in social_posts if p.contains_violence]
        extremist_posts = [p for p in social_posts if p.contains_extremist_content]
        discriminatory_posts = [p for p in social_posts if p.contains_discriminatory_content]
        confidential_posts = [p for p in social_posts if p.contains_company_confidential]
        alcohol_drug_posts = [p for p in social_posts if p.contains_alcohol_drugs]
        
        if violence_posts:
            score -= 40
            findings.append(f"{len(violence_posts)} posts containing violent content")
            risk_factors.append("Violent content on social media")
            recommendations.append("Anger management evaluation required")
        
        if extremist_posts:
            score -= 80
            findings.append(f"{len(extremist_posts)} posts with extremist content - CRITICAL")
            risk_factors.append("EXTREMIST CONTENT DETECTED - SECURITY RISK")
            recommendations.append("Immediate security review required")
        
        if discriminatory_posts:
            score -= 35
            findings.append(f"{len(discriminatory_posts)} posts with discriminatory content")
            risk_factors.append("Discriminatory content on social media")
            recommendations.append("Diversity and inclusion training required")
        
        if confidential_posts:
            score -= 50
            findings.append(f"{len(confidential_posts)} posts potentially containing confidential information")
            risk_factors.append("Potential information security breach")
            recommendations.append("Security awareness training and investigation required")
        
        if alcohol_drug_posts:
            score -= 20
            findings.append(f"{len(alcohol_drug_posts)} posts referencing alcohol/drugs")
            risk_factors.append("Substance-related social media content")
            recommendations.append("Substance abuse awareness counseling")
        
        # Check posting frequency and timing
        recent_posts = [
            p for p in social_posts
            if p.post_date and (datetime.utcnow() - p.post_date).days <= 7
        ]
        if len(recent_posts) > 20:
            score -= 10
            findings.append(f"Excessive social media activity ({len(recent_posts)} posts in last 7 days)")
        
        # Check for concerning patterns
        concerning_patterns = self._analyze_patterns(social_posts)
        if concerning_patterns:
            score -= len(concerning_patterns) * 10
            findings.extend(concerning_patterns)
        
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
            'total_posts_analyzed': total_posts,
            'flagged_posts': len(flagged_posts),
            'sentiment_distribution': {
                'positive': len(positive_posts),
                'negative': len(negative_posts),
                'neutral': total_posts - len(positive_posts) - len(negative_posts),
            },
        }
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of a text"""
        text_lower = text.lower()
        
        pos_count = sum(1 for word in self.positive_sentiment_words if word in text_lower)
        neg_count = sum(1 for word in self.negative_sentiment_words if word in text_lower)
        
        total = pos_count + neg_count
        if total == 0:
            return 0.0, 'Neutral'
        
        score = (pos_count - neg_count) / total
        
        if score > 0.2:
            return score, 'Positive'
        elif score < -0.2:
            return score, 'Negative'
        else:
            return score, 'Neutral'
    
    def extract_topics(self, text):
        """Extract topics from text"""
        topics = []
        text_lower = text.lower()
        
        topic_keywords = {
            'aviation': ['flight', 'flying', 'aircraft', 'pilot', 'airport', 'airline', 'cockpit'],
            'work': ['job', 'work', 'shift', 'schedule', 'crew', 'colleague', 'boss'],
            'personal_life': ['family', 'wife', 'husband', 'kids', 'children', 'home'],
            'politics': ['government', 'election', 'president', 'policy', 'law', 'vote'],
            'religion': ['god', 'church', 'mosque', 'temple', 'pray', 'faith', 'religion'],
            'health': ['doctor', 'hospital', 'sick', 'health', 'medical', 'medicine'],
            'finance': ['money', 'debt', 'pay', 'salary', 'financial', 'bank'],
            'substances': ['alcohol', 'beer', 'wine', 'drink', 'drug', 'smoke'],
            'travel': ['vacation', 'trip', 'travel', 'holiday', 'destination'],
            'sports': ['game', 'team', 'score', 'win', 'match', 'sport'],
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                topics.append(topic)
        
        return topics
    
    def extract_entities(self, text):
        """Extract named entities from text"""
        entities = []
        
        # Simple pattern matching for common entities
        # Airports
        airport_pattern = r'\b([A-Z]{3})\b'
        potential_airports = re.findall(airport_pattern, text)
        known_airports = ['JFK', 'LAX', 'ORD', 'DFW', 'LHR', 'CDG', 'DXB', 'SIN', 'HKG', 'NRT']
        for airport in potential_airports:
            if airport in known_airports:
                entities.append({'type': 'airport', 'value': airport})
        
        # Aircraft types
        aircraft_pattern = r'\b(B7\d{2}|A3\d{2}|B747|B777|B787|A320|A330|A350|A380|CRJ|ERJ)\b'
        aircraft = re.findall(aircraft_pattern, text)
        for ac in aircraft:
            entities.append({'type': 'aircraft', 'value': ac})
        
        return entities
    
    def check_profanity(self, text):
        """Check for profanity"""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.profanity_patterns)
    
    def check_violence(self, text):
        """Check for violent content"""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.violence_patterns)
    
    def check_political_content(self, text):
        """Check for political content"""
        text_lower = text.lower()
        political_keywords = ['president', 'election', 'government', 'policy', 'law', 'vote', 'party', 'political']
        return any(kw in text_lower for kw in political_keywords)
    
    def check_extremist_content(self, text):
        """Check for extremist content"""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.extremist_patterns)
    
    def check_discriminatory_content(self, text):
        """Check for discriminatory content"""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.discriminatory_patterns)
    
    def check_company_confidential(self, text):
        """Check for potential confidential information"""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.confidential_patterns)
    
    def check_alcohol_drugs(self, text):
        """Check for alcohol/drug references"""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.alcohol_drug_patterns)
    
    def identify_risk_indicators(self, text):
        """Identify risk indicators in text"""
        text_lower = text.lower()
        indicators = []
        
        for pattern in self.risk_indicator_patterns:
            if re.search(pattern, text_lower):
                indicators.append(pattern.replace(r'\b', '').replace('\\', ''))
        
        return indicators
    
    def _analyze_patterns(self, posts):
        """Analyze patterns across multiple posts"""
        patterns = []
        
        # Check for escalating negativity
        sorted_posts = sorted(posts, key=lambda p: p.post_date or datetime.min)
        if len(sorted_posts) >= 3:
            recent_sentiments = [p.sentiment_score or 0 for p in sorted_posts[-3:]]
            if all(s < -0.3 for s in recent_sentiments):
                patterns.append("Escalating negative sentiment in recent posts")
        
        # Check for concerning topic frequency
        all_topics = []
        for post in posts:
            if post.topics:
                import json
                all_topics.extend(json.loads(post.topics))
        
        from collections import Counter
        topic_counts = Counter(all_topics)
        
        if topic_counts.get('substances', 0) > 3:
            patterns.append("Frequent substance-related posts")
        
        if topic_counts.get('politics', 0) > 5:
            patterns.append("Excessive political content")
        
        return patterns
