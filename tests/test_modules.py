"""
Unit tests for Pilot Fitness Assessment modules
"""

import unittest
from datetime import datetime, timedelta
from modules.medical_assessment import MedicalAssessment
from modules.psychological_assessment import PsychologicalAssessment
from modules.social_media_analyzer import SocialMediaAnalyzer
from modules.substance_abuse import SubstanceAbuseScreening
from modules.financial_stability import FinancialStabilityChecker
from modules.radicalization_detection import RadicalizationDetector
from modules.digital_footprint import DigitalFootprintAnalyzer
from modules.travel_history import TravelHistoryAnalyzer
from modules.behavior_pattern import BehaviorPatternAnalyzer


class TestMedicalAssessment(unittest.TestCase):
    def setUp(self):
        self.assessor = MedicalAssessment()
    
    def test_no_data(self):
        result = self.assessor.assess(None, [])
        self.assertEqual(result['status'], 'NO_DATA')
        self.assertEqual(result['score'], 0)
    
    def test_vision_assessment(self):
        # Mock record with perfect vision
        class MockRecord:
            vision_left_eye = '20/20'
            vision_right_eye = '20/20'
            color_vision = 'Normal'
            corrective_lenses_required = False
            hearing_left_ear = 'Normal'
            hearing_right_ear = 'Normal'
            hearing_aid_required = False
            blood_pressure_systolic = 120
            blood_pressure_diastolic = 80
            heart_rate = 70
            ecg_result = 'Normal'
            cholesterol_total = 180
            cholesterol_ldl = 100
            cholesterol_hdl = 60
            lung_function_fev1 = 4.0
            lung_function_fvc = 5.0
            respiratory_conditions = ''
            height_cm = 175
            weight_kg = 70
            bmi = 22.9
            mobility_issues = ''
            neurological_conditions = 'None'
            seizure_history = False
            epilepsy = False
            psychiatric_conditions = 'None'
            current_medications = 'None'
            medication_side_effects = 'None'
            alcohol_consumption = 'Occasional'
            tobacco_use = 'Never'
            drug_use_history = 'None'
            blood_test_result = 'Normal'
            urine_test_result = 'Normal'
            drug_screen_result = 'NEGATIVE'
            alcohol_test_result = 'NEGATIVE'
            exam_date = datetime.now().date()
        
        result = self.assessor.assess(None, [MockRecord()])
        self.assertGreater(result['score'], 80)
        self.assertEqual(result['status'], 'FIT')


class TestPsychologicalAssessment(unittest.TestCase):
    def setUp(self):
        self.assessor = PsychologicalAssessment()
    
    def test_no_data(self):
        result = self.assessor.assess(None, [])
        self.assertEqual(result['status'], 'NO_DATA')


class TestSocialMediaAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = SocialMediaAnalyzer()
    
    def test_sentiment_positive(self):
        score, label = self.analyzer.analyze_sentiment("I love flying! Best job ever!")
        self.assertGreater(score, 0)
        self.assertEqual(label, 'Positive')
    
    def test_sentiment_negative(self):
        score, label = self.analyzer.analyze_sentiment("I hate this job, it's terrible and awful")
        self.assertLess(score, 0)
        self.assertEqual(label, 'Negative')
    
    def test_profanity_detection(self):
        self.assertTrue(self.analyzer.check_profanity("This is shit"))
        self.assertFalse(self.analyzer.check_profanity("This is great"))
    
    def test_violence_detection(self):
        self.assertTrue(self.analyzer.check_violence("I will kill them"))
        self.assertFalse(self.analyzer.check_violence("I will help them"))
    
    def test_extremist_detection(self):
        self.assertTrue(self.analyzer.check_extremist_content("jihad is the answer"))
        self.assertFalse(self.analyzer.check_extremist_content("peace is the answer"))


class TestSubstanceAbuseScreening(unittest.TestCase):
    def setUp(self):
        self.screener = SubstanceAbuseScreening()
    
    def test_no_data(self):
        result = self.screener.assess(None, [])
        self.assertEqual(result['status'], 'NO_DATA')


class TestFinancialStability(unittest.TestCase):
    def setUp(self):
        self.checker = FinancialStabilityChecker()
    
    def test_no_data(self):
        result = self.checker.assess(None, [])
        self.assertEqual(result['status'], 'NO_DATA')


class TestRadicalizationDetector(unittest.TestCase):
    def setUp(self):
        self.detector = RadicalizationDetector()
    
    def test_no_data(self):
        result = self.detector.assess(None, [], [], [], [], [])
        self.assertEqual(result['radicalization_risk'], 'NONE')


class TestDigitalFootprintAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = DigitalFootprintAnalyzer()
    
    def test_no_data(self):
        result = self.analyzer.assess(None, [], [], [], [], [], [])
        self.assertEqual(result['status'], 'NO_DATA')


class TestTravelHistoryAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TravelHistoryAnalyzer()
    
    def test_no_data(self):
        result = self.analyzer.assess(None, [])
        self.assertEqual(result['status'], 'NO_DATA')


class TestBehaviorPatternAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = BehaviorPatternAnalyzer()
    
    def test_no_data(self):
        result = self.analyzer.assess(None, [], [], [], [])
        self.assertEqual(result['status'], 'NO_DATA')


if __name__ == '__main__':
    unittest.main()
