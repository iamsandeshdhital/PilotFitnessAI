"""
Pilot Fitness Assessment AI Tool
================================
Comprehensive pilot fitness evaluation system assessing:
- Medical fitness
- Psychological evaluation
- Social media behavior analysis
- Socio-political-economic risk factors
- Staff & crew feedback
- Flight history & performance
- Substance abuse screening
- Financial stability
- Criminal background
- Training & certification validity
- Fatigue & lifestyle assessment
- Travel history analysis
- Behavior pattern change detection
- Digital footprint analysis (phone, laptop, devices, email, browsing, messages)
- Radicalization detection
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import json
import hashlib
import re
from functools import wraps

from modules.medical_assessment import MedicalAssessment
from modules.psychological_assessment import PsychologicalAssessment
from modules.social_media_analyzer import SocialMediaAnalyzer
from modules.socio_political_economic import SocioPoliticalEconomicAnalyzer
from modules.staff_feedback import StaffFeedbackAnalyzer
from modules.flight_history import FlightHistoryAnalyzer
from modules.substance_abuse import SubstanceAbuseScreening
from modules.financial_stability import FinancialStabilityChecker
from modules.background_check import BackgroundChecker
from modules.fatigue_lifestyle import FatigueLifestyleAnalyzer
from modules.training_certification import TrainingCertificationValidator
from modules.travel_history import TravelHistoryAnalyzer
from modules.behavior_pattern import BehaviorPatternAnalyzer
from modules.digital_footprint import DigitalFootprintAnalyzer
from modules.radicalization_detection import RadicalizationDetector
from modules.overall_scoring import OverallScoringEngine
from auth import authenticate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'pilot-fitness-ai-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pilot_fitness.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


# Template context processors
@app.context_processor
def inject_now():
    """Make 'now' available in all templates"""
    return {'now': datetime.now().date()}


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 errors"""
    return render_template('404.html'), 403


# ============================================================
# AUTHENTICATION ROUTES
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = authenticate(username, password)
        if user:
            session['user'] = user
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


# ============================================================
# DATABASE MODELS
# ============================================================

class Pilot(db.Model):
    """Core pilot information"""
    __tablename__ = 'pilots'
    
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    nationality = db.Column(db.String(100))
    license_number = db.Column(db.String(50), unique=True)
    license_type = db.Column(db.String(50))
    license_issue_date = db.Column(db.Date)
    license_expiry_date = db.Column(db.Date)
    medical_certificate_class = db.Column(db.String(10))
    medical_expiry = db.Column(db.Date)
    total_flight_hours = db.Column(db.Float, default=0)
    aircraft_type_ratings = db.Column(db.Text)
    airline = db.Column(db.String(200))
    base_airport = db.Column(db.String(10))
    years_experience = db.Column(db.Float, default=0)
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.Text)
    social_media_handles = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assessments = db.relationship('Assessment', backref='pilot', lazy=True, cascade='all, delete-orphan')
    medical_records = db.relationship('MedicalRecord', backref='pilot', lazy=True, cascade='all, delete-orphan')
    flight_logs = db.relationship('FlightLog', backref='pilot', lazy=True, cascade='all, delete-orphan')
    staff_feedback = db.relationship('StaffFeedback', backref='pilot', lazy=True, cascade='all, delete-orphan')
    social_media_posts = db.relationship('SocialMediaPost', backref='pilot', lazy=True, cascade='all, delete-orphan')
    training_records = db.relationship('TrainingRecord', backref='pilot', lazy=True, cascade='all, delete-orphan')
    incident_reports = db.relationship('IncidentReport', backref='pilot', lazy=True, cascade='all, delete-orphan')
    financial_records = db.relationship('FinancialRecord', backref='pilot', lazy=True, cascade='all, delete-orphan')
    substance_tests = db.relationship('SubstanceTest', backref='pilot', lazy=True, cascade='all, delete-orphan')
    psychological_evals = db.relationship('PsychologicalEval', backref='pilot', lazy=True, cascade='all, delete-orphan')
    travel_records = db.relationship('TravelRecord', backref='pilot', lazy=True, cascade='all, delete-orphan')
    phone_records = db.relationship('PhoneRecord', backref='pilot', lazy=True, cascade='all, delete-orphan')
    email_records = db.relationship('EmailRecord', backref='pilot', lazy=True, cascade='all, delete-orphan')
    browsing_history = db.relationship('BrowsingHistory', backref='pilot', lazy=True, cascade='all, delete-orphan')
    message_records = db.relationship('MessageRecord', backref='pilot', lazy=True, cascade='all, delete-orphan')
    device_records = db.relationship('DeviceRecord', backref='pilot', lazy=True, cascade='all, delete-orphan')
    location_data = db.relationship('LocationData', backref='pilot', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'pilot_id': self.pilot_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'nationality': self.nationality,
            'license_number': self.license_number,
            'license_type': self.license_type,
            'license_issue_date': self.license_issue_date.isoformat() if self.license_issue_date else None,
            'license_expiry_date': self.license_expiry_date.isoformat() if self.license_expiry_date else None,
            'medical_certificate_class': self.medical_certificate_class,
            'medical_expiry': self.medical_expiry.isoformat() if self.medical_expiry else None,
            'total_flight_hours': self.total_flight_hours,
            'aircraft_type_ratings': json.loads(self.aircraft_type_ratings) if self.aircraft_type_ratings else [],
            'airline': self.airline,
            'base_airport': self.base_airport,
            'years_experience': self.years_experience,
            'email': self.email,
            'phone': self.phone,
            'social_media_handles': json.loads(self.social_media_handles) if self.social_media_handles else {},
        }


class Assessment(db.Model):
    """Overall fitness assessment results"""
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    assessed_by = db.Column(db.String(200))
    
    # Individual module scores (0-100)
    medical_score = db.Column(db.Float)
    psychological_score = db.Column(db.Float)
    social_media_score = db.Column(db.Float)
    socio_political_economic_score = db.Column(db.Float)
    staff_feedback_score = db.Column(db.Float)
    flight_history_score = db.Column(db.Float)
    substance_abuse_score = db.Column(db.Float)
    financial_stability_score = db.Column(db.Float)
    background_check_score = db.Column(db.Float)
    fatigue_lifestyle_score = db.Column(db.Float)
    training_certification_score = db.Column(db.Float)
    travel_history_score = db.Column(db.Float)
    behavior_pattern_score = db.Column(db.Float)
    digital_footprint_score = db.Column(db.Float)
    radicalization_score = db.Column(db.Float)
    
    # Overall
    overall_score = db.Column(db.Float)
    fitness_status = db.Column(db.String(20))
    risk_level = db.Column(db.String(20))
    
    # Detailed results
    module_results = db.Column(db.Text)
    red_flags = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    conditions = db.Column(db.Text)
    
    # Review
    reviewed_by = db.Column(db.String(200))
    review_date = db.Column(db.DateTime)
    review_notes = db.Column(db.Text)
    final_decision = db.Column(db.String(20))
    
    def to_dict(self):
        return {
            'id': self.id,
            'pilot_id': self.pilot_id,
            'assessment_date': self.assessment_date.isoformat(),
            'assessed_by': self.assessed_by,
            'medical_score': self.medical_score,
            'psychological_score': self.psychological_score,
            'social_media_score': self.social_media_score,
            'socio_political_economic_score': self.socio_political_economic_score,
            'staff_feedback_score': self.staff_feedback_score,
            'flight_history_score': self.flight_history_score,
            'substance_abuse_score': self.substance_abuse_score,
            'financial_stability_score': self.financial_stability_score,
            'background_check_score': self.background_check_score,
            'fatigue_lifestyle_score': self.fatigue_lifestyle_score,
            'training_certification_score': self.training_certification_score,
            'travel_history_score': self.travel_history_score,
            'behavior_pattern_score': self.behavior_pattern_score,
            'digital_footprint_score': self.digital_footprint_score,
            'radicalization_score': self.radicalization_score,
            'overall_score': self.overall_score,
            'fitness_status': self.fitness_status,
            'risk_level': self.risk_level,
            'red_flags': json.loads(self.red_flags) if self.red_flags else [],
            'recommendations': json.loads(self.recommendations) if self.recommendations else [],
            'conditions': json.loads(self.conditions) if self.conditions else [],
        }


class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    exam_date = db.Column(db.Date, nullable=False)
    examiner_name = db.Column(db.String(200))
    examiner_id = db.Column(db.String(50))
    vision_left_eye = db.Column(db.String(20))
    vision_right_eye = db.Column(db.String(20))
    color_vision = db.Column(db.String(20))
    corrective_lenses_required = db.Column(db.Boolean, default=False)
    hearing_left_ear = db.Column(db.String(20))
    hearing_right_ear = db.Column(db.String(20))
    hearing_aid_required = db.Column(db.Boolean, default=False)
    blood_pressure_systolic = db.Column(db.Integer)
    blood_pressure_diastolic = db.Column(db.Integer)
    heart_rate = db.Column(db.Integer)
    ecg_result = db.Column(db.String(50))
    cholesterol_total = db.Column(db.Float)
    cholesterol_ldl = db.Column(db.Float)
    cholesterol_hdl = db.Column(db.Float)
    lung_function_fev1 = db.Column(db.Float)
    lung_function_fvc = db.Column(db.Float)
    respiratory_conditions = db.Column(db.Text)
    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    bmi = db.Column(db.Float)
    mobility_issues = db.Column(db.Text)
    neurological_conditions = db.Column(db.Text)
    seizure_history = db.Column(db.Boolean, default=False)
    epilepsy = db.Column(db.Boolean, default=False)
    psychiatric_conditions = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    medication_side_effects = db.Column(db.Text)
    alcohol_consumption = db.Column(db.String(50))
    tobacco_use = db.Column(db.String(50))
    drug_use_history = db.Column(db.Text)
    blood_test_result = db.Column(db.String(50))
    urine_test_result = db.Column(db.String(50))
    drug_screen_result = db.Column(db.String(50))
    alcohol_test_result = db.Column(db.String(50))
    medical_fitness = db.Column(db.String(20))
    restrictions = db.Column(db.Text)
    follow_up_required = db.Column(db.Boolean, default=False)
    follow_up_date = db.Column(db.Date)
    notes = db.Column(db.Text)


class FlightLog(db.Model):
    __tablename__ = 'flight_logs'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    flight_date = db.Column(db.Date, nullable=False)
    aircraft_type = db.Column(db.String(50))
    aircraft_registration = db.Column(db.String(20))
    departure_airport = db.Column(db.String(10))
    arrival_airport = db.Column(db.String(10))
    flight_type = db.Column(db.String(50))
    flight_rules = db.Column(db.String(20))
    flight_duration_minutes = db.Column(db.Integer)
    night_flight = db.Column(db.Boolean, default=False)
    instrument_time = db.Column(db.Integer, default=0)
    landings = db.Column(db.Integer, default=1)
    incidents = db.Column(db.Text)
    weather_conditions = db.Column(db.String(100))
    crew_members = db.Column(db.Text)
    remarks = db.Column(db.Text)


class StaffFeedback(db.Model):
    __tablename__ = 'staff_feedback'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    feedback_date = db.Column(db.Date, default=datetime.utcnow)
    feedback_provider_name = db.Column(db.String(200))
    feedback_provider_role = db.Column(db.String(100))
    feedback_provider_id = db.Column(db.String(50))
    relationship_duration_months = db.Column(db.Integer)
    professionalism_rating = db.Column(db.Integer)
    communication_rating = db.Column(db.Integer)
    teamwork_rating = db.Column(db.Integer)
    decision_making_rating = db.Column(db.Integer)
    stress_management_rating = db.Column(db.Integer)
    punctuality_rating = db.Column(db.Integer)
    technical_knowledge_rating = db.Column(db.Integer)
    situational_awareness_rating = db.Column(db.Integer)
    leadership_rating = db.Column(db.Integer)
    overall_rating = db.Column(db.Integer)
    would_fly_with_again = db.Column(db.String(20))
    strengths = db.Column(db.Text)
    areas_for_improvement = db.Column(db.Text)
    concerns = db.Column(db.Text)
    additional_comments = db.Column(db.Text)
    signs_of_stress = db.Column(db.Boolean, default=False)
    signs_of_fatigue = db.Column(db.Boolean, default=False)
    signs_of_substance_use = db.Column(db.Boolean, default=False)
    signs_of_aggression = db.Column(db.Boolean, default=False)
    signs_of_depression = db.Column(db.Boolean, default=False)
    signs_of_financial_stress = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.String(200))
    verification_date = db.Column(db.Date)
    is_anonymous = db.Column(db.Boolean, default=False)


class SocialMediaPost(db.Model):
    __tablename__ = 'social_media_posts'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    platform = db.Column(db.String(50))
    post_date = db.Column(db.DateTime)
    post_content = db.Column(db.Text)
    post_type = db.Column(db.String(50))
    likes_count = db.Column(db.Integer, default=0)
    shares_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    sentiment_score = db.Column(db.Float)
    sentiment_label = db.Column(db.String(20))
    flagged = db.Column(db.Boolean, default=False)
    flag_reason = db.Column(db.Text)
    topics = db.Column(db.Text)
    entities = db.Column(db.Text)
    language = db.Column(db.String(10))
    contains_profanity = db.Column(db.Boolean, default=False)
    contains_violence = db.Column(db.Boolean, default=False)
    contains_political_content = db.Column(db.Boolean, default=False)
    contains_extremist_content = db.Column(db.Boolean, default=False)
    contains_discriminatory_content = db.Column(db.Boolean, default=False)
    contains_company_confidential = db.Column(db.Boolean, default=False)
    contains_alcohol_drugs = db.Column(db.Boolean, default=False)
    risk_indicators = db.Column(db.Text)


class TrainingRecord(db.Model):
    __tablename__ = 'training_records'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    training_type = db.Column(db.String(100))
    training_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    training_provider = db.Column(db.String(200))
    instructor_name = db.Column(db.String(200))
    result = db.Column(db.String(20))
    score = db.Column(db.Float)
    remedial_required = db.Column(db.Boolean, default=False)
    remedial_completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)


class IncidentReport(db.Model):
    __tablename__ = 'incident_reports'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    incident_date = db.Column(db.Date)
    incident_type = db.Column(db.String(100))
    severity = db.Column(db.String(20))
    description = db.Column(db.Text)
    investigation_findings = db.Column(db.Text)
    pilot_at_fault = db.Column(db.Boolean)
    corrective_actions = db.Column(db.Text)
    status = db.Column(db.String(50))


class FinancialRecord(db.Model):
    __tablename__ = 'financial_records'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    record_date = db.Column(db.Date, default=datetime.utcnow)
    annual_income = db.Column(db.Float)
    total_debt = db.Column(db.Float)
    credit_score = db.Column(db.Integer)
    bankruptcy_history = db.Column(db.Boolean, default=False)
    payment_delinquencies = db.Column(db.Integer, default=0)
    gambling_concerns = db.Column(db.Boolean, default=False)
    financial_stress_indicators = db.Column(db.Text)
    source_of_wealth_verified = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)


class SubstanceTest(db.Model):
    __tablename__ = 'substance_tests'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    test_date = db.Column(db.Date, nullable=False)
    test_type = db.Column(db.String(50))
    test_method = db.Column(db.String(50))
    alcohol_result = db.Column(db.String(20))
    alcohol_level = db.Column(db.Float)
    amphetamines = db.Column(db.String(20))
    cocaine = db.Column(db.String(20))
    opiates = db.Column(db.String(20))
    cannabis = db.Column(db.String(20))
    benzodiazepines = db.Column(db.String(20))
    pcp = db.Column(db.String(20))
    overall_result = db.Column(db.String(20))
    tested_by = db.Column(db.String(200))
    verified = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)


class PsychologicalEval(db.Model):
    __tablename__ = 'psychological_evals'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    eval_date = db.Column(db.Date, nullable=False)
    evaluator_name = db.Column(db.String(200))
    evaluator_license = db.Column(db.String(50))
    mmpi2_validity = db.Column(db.String(50))
    mmpi2_hs = db.Column(db.Float)
    mmpi2_d = db.Column(db.Float)
    mmpi2_hy = db.Column(db.Float)
    mmpi2_pd = db.Column(db.Float)
    mmpi2_mf = db.Column(db.Float)
    mmpi2_pa = db.Column(db.Float)
    mmpi2_pt = db.Column(db.Float)
    mmpi2_sc = db.Column(db.Float)
    mmpi2_ma = db.Column(db.Float)
    mmpi2_si = db.Column(db.Float)
    big5_openness = db.Column(db.Float)
    big5_conscientiousness = db.Column(db.Float)
    big5_extraversion = db.Column(db.Float)
    big5_agreeableness = db.Column(db.Float)
    big5_neuroticism = db.Column(db.Float)
    anxiety_level = db.Column(db.String(20))
    depression_level = db.Column(db.String(20))
    stress_level = db.Column(db.String(20))
    aggression_level = db.Column(db.String(20))
    impulsivity_level = db.Column(db.String(20))
    risk_taking_tendency = db.Column(db.String(20))
    cognitive_function = db.Column(db.String(20))
    memory_function = db.Column(db.String(20))
    attention_function = db.Column(db.String(20))
    decision_making_quality = db.Column(db.String(20))
    psychological_fitness = db.Column(db.String(20))
    recommendations = db.Column(db.Text)
    follow_up_needed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)


class TravelRecord(db.Model):
    __tablename__ = 'travel_records'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    departure_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    destination = db.Column(db.String(100))
    purpose = db.Column(db.String(100))
    trip_type = db.Column(db.String(50))
    booking_date = db.Column(db.Date)
    companion = db.Column(db.String(100))
    visa_status = db.Column(db.String(50))
    foreign_contacts = db.Column(db.Text)
    notes = db.Column(db.Text)


class PhoneRecord(db.Model):
    __tablename__ = 'phone_records'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    call_date = db.Column(db.DateTime)
    call_time = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Integer)
    contact_name = db.Column(db.String(200))
    contact_number = db.Column(db.String(50))
    contact_type = db.Column(db.String(50))
    is_international = db.Column(db.Boolean, default=False)
    is_known_associate = db.Column(db.Boolean, default=False)
    is_prepaid = db.Column(db.Boolean, default=False)
    call_direction = db.Column(db.String(20))
    notes = db.Column(db.Text)


class EmailRecord(db.Model):
    __tablename__ = 'email_records'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    email_date = db.Column(db.DateTime)
    sender = db.Column(db.String(200))
    recipient = db.Column(db.String(200))
    subject = db.Column(db.String(500))
    body = db.Column(db.Text)
    is_internal = db.Column(db.Boolean, default=True)
    is_encrypted = db.Column(db.Boolean, default=False)
    has_large_attachment = db.Column(db.Boolean, default=False)
    to_personal_account = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)


class BrowsingHistory(db.Model):
    __tablename__ = 'browsing_history'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    access_time = db.Column(db.DateTime)
    url = db.Column(db.String(1000))
    title = db.Column(db.String(500))
    category = db.Column(db.String(100))
    is_work_related = db.Column(db.Boolean, default=True)
    is_non_work_related = db.Column(db.Boolean, default=False)
    is_political_content = db.Column(db.Boolean, default=False)
    is_job_search = db.Column(db.Boolean, default=False)
    is_financial_stress = db.Column(db.Boolean, default=False)
    is_cleared = db.Column(db.Boolean, default=False)
    duration_seconds = db.Column(db.Integer)


class MessageRecord(db.Model):
    __tablename__ = 'message_records'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    message_time = db.Column(db.DateTime)
    sender = db.Column(db.String(200))
    recipient = db.Column(db.String(200))
    content = db.Column(db.Text)
    platform = db.Column(db.String(50))
    is_unknown_contact = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    is_encrypted_app = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)


class DeviceRecord(db.Model):
    __tablename__ = 'device_records'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    device_id = db.Column(db.String(100))
    device_type = db.Column(db.String(50))
    os_version = db.Column(db.String(50))
    is_authorized = db.Column(db.Boolean, default=True)
    is_tampered = db.Column(db.Boolean, default=False)
    uses_vpn = db.Column(db.Boolean, default=False)
    has_factory_reset = db.Column(db.Boolean, default=False)
    is_shared = db.Column(db.Boolean, default=False)
    has_outdated_security = db.Column(db.Boolean, default=False)
    last_check = db.Column(db.DateTime)
    notes = db.Column(db.Text)


class LocationData(db.Model):
    __tablename__ = 'location_data'
    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    timestamp = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_unusual = db.Column(db.Boolean, default=False)
    is_high_risk_area = db.Column(db.Boolean, default=False)
    is_spoofed = db.Column(db.Boolean, default=False)
    has_gap = db.Column(db.Boolean, default=False)
    is_border_crossing = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(50))
    notes = db.Column(db.Text)


# ============================================================
# ASSESSMENT MODULES INITIALIZATION
# ============================================================

medical_assessor = MedicalAssessment()
psych_assessor = PsychologicalAssessment()
social_analyzer = SocialMediaAnalyzer()
spe_analyzer = SocioPoliticalEconomicAnalyzer()
staff_analyzer = StaffFeedbackAnalyzer()
flight_analyzer = FlightHistoryAnalyzer()
substance_screener = SubstanceAbuseScreening()
financial_checker = FinancialStabilityChecker()
background_checker = BackgroundChecker()
fatigue_analyzer = FatigueLifestyleAnalyzer()
training_validator = TrainingCertificationValidator()
travel_analyzer = TravelHistoryAnalyzer()
behavior_analyzer = BehaviorPatternAnalyzer()
digital_analyzer = DigitalFootprintAnalyzer()
radicalization_detector = RadicalizationDetector()
scoring_engine = OverallScoringEngine()


# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    """Dashboard home page"""
    pilot_count = Pilot.query.count()
    assessment_count = Assessment.query.count()
    fit_count = Assessment.query.filter_by(fitness_status='FIT').count()
    unfit_count = Assessment.query.filter_by(fitness_status='UNFIT').count()
    conditional_count = Assessment.query.filter_by(fitness_status='CONDITIONAL').count()
    recent_assessments = Assessment.query.order_by(Assessment.assessment_date.desc()).limit(10).all()
    
    return render_template('index.html',
                         pilot_count=pilot_count,
                         assessment_count=assessment_count,
                         fit_count=fit_count,
                         unfit_count=unfit_count,
                         conditional_count=conditional_count,
                         recent_assessments=recent_assessments)


@app.route('/pilots')
def list_pilots():
    """List all pilots"""
    pilots = Pilot.query.order_by(Pilot.last_name).all()
    return render_template('pilots.html', pilots=pilots)


@app.route('/pilot/<int:pilot_id>')
def pilot_detail(pilot_id):
    """Pilot detail page"""
    pilot = Pilot.query.get_or_404(pilot_id)
    assessments = Assessment.query.filter_by(pilot_id=pilot_id).order_by(Assessment.assessment_date.desc()).all()
    medical_records = MedicalRecord.query.filter_by(pilot_id=pilot_id).order_by(MedicalRecord.exam_date.desc()).all()
    flight_logs = FlightLog.query.filter_by(pilot_id=pilot_id).order_by(FlightLog.flight_date.desc()).limit(50).all()
    staff_feedback = StaffFeedback.query.filter_by(pilot_id=pilot_id).order_by(StaffFeedback.feedback_date.desc()).all()
    social_posts = SocialMediaPost.query.filter_by(pilot_id=pilot_id).order_by(SocialMediaPost.post_date.desc()).limit(50).all()
    training_records = TrainingRecord.query.filter_by(pilot_id=pilot_id).order_by(TrainingRecord.training_date.desc()).all()
    incidents = IncidentReport.query.filter_by(pilot_id=pilot_id).order_by(IncidentReport.incident_date.desc()).all()
    financial_records = FinancialRecord.query.filter_by(pilot_id=pilot_id).order_by(FinancialRecord.record_date.desc()).all()
    substance_tests = SubstanceTest.query.filter_by(pilot_id=pilot_id).order_by(SubstanceTest.test_date.desc()).all()
    psych_evals = PsychologicalEval.query.filter_by(pilot_id=pilot_id).order_by(PsychologicalEval.eval_date.desc()).all()
    travel_records = TravelRecord.query.filter_by(pilot_id=pilot_id).order_by(TravelRecord.departure_date.desc()).all()
    phone_records = PhoneRecord.query.filter_by(pilot_id=pilot_id).order_by(PhoneRecord.call_date.desc()).limit(50).all()
    email_records = EmailRecord.query.filter_by(pilot_id=pilot_id).order_by(EmailRecord.email_date.desc()).limit(50).all()
    browsing_history = BrowsingHistory.query.filter_by(pilot_id=pilot_id).order_by(BrowsingHistory.access_time.desc()).limit(50).all()
    message_records = MessageRecord.query.filter_by(pilot_id=pilot_id).order_by(MessageRecord.message_time.desc()).limit(50).all()
    device_records = DeviceRecord.query.filter_by(pilot_id=pilot_id).all()
    location_data = LocationData.query.filter_by(pilot_id=pilot_id).order_by(LocationData.timestamp.desc()).limit(50).all()
    
    return render_template('pilot_detail.html',
                         pilot=pilot,
                         assessments=assessments,
                         medical_records=medical_records,
                         flight_logs=flight_logs,
                         staff_feedback=staff_feedback,
                         social_posts=social_posts,
                         training_records=training_records,
                         incidents=incidents,
                         financial_records=financial_records,
                         substance_tests=substance_tests,
                         psych_evals=psych_evals,
                         travel_records=travel_records,
                         phone_records=phone_records,
                         email_records=email_records,
                         browsing_history=browsing_history,
                         message_records=message_records,
                         device_records=device_records,
                         location_data=location_data)


@app.route('/pilot/add', methods=['GET', 'POST'])
def add_pilot():
    """Add a new pilot"""
    if request.method == 'POST':
        pilot = Pilot(
            pilot_id=request.form['pilot_id'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            date_of_birth=datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date(),
            nationality=request.form.get('nationality', ''),
            license_number=request.form.get('license_number', ''),
            license_type=request.form.get('license_type', ''),
            license_issue_date=datetime.strptime(request.form['license_issue_date'], '%Y-%m-%d').date() if request.form.get('license_issue_date') else None,
            license_expiry_date=datetime.strptime(request.form['license_expiry_date'], '%Y-%m-%d').date() if request.form.get('license_expiry_date') else None,
            medical_certificate_class=request.form.get('medical_certificate_class', ''),
            medical_expiry=datetime.strptime(request.form['medical_expiry'], '%Y-%m-%d').date() if request.form.get('medical_expiry') else None,
            total_flight_hours=float(request.form.get('total_flight_hours', 0)),
            aircraft_type_ratings=json.dumps(request.form.getlist('aircraft_type_ratings')),
            airline=request.form.get('airline', ''),
            base_airport=request.form.get('base_airport', ''),
            years_experience=float(request.form.get('years_experience', 0)),
            email=request.form.get('email', ''),
            phone=request.form.get('phone', ''),
            address=request.form.get('address', ''),
            emergency_contact=request.form.get('emergency_contact', ''),
            social_media_handles=json.dumps({
                'twitter': request.form.get('twitter_handle', ''),
                'facebook': request.form.get('facebook_handle', ''),
                'instagram': request.form.get('instagram_handle', ''),
                'linkedin': request.form.get('linkedin_handle', ''),
            }),
        )
        db.session.add(pilot)
        db.session.commit()
        flash('Pilot added successfully!', 'success')
        return redirect(url_for('pilot_detail', pilot_id=pilot.id))
    
    return render_template('add_pilot.html')


@app.route('/assess/<int:pilot_id>', methods=['GET', 'POST'])
def run_assessment(pilot_id):
    """Run comprehensive fitness assessment"""
    pilot = Pilot.query.get_or_404(pilot_id)
    
    if request.method == 'POST':
        # Gather all data
        medical_records = MedicalRecord.query.filter_by(pilot_id=pilot_id).order_by(MedicalRecord.exam_date.desc()).all()
        psych_evals = PsychologicalEval.query.filter_by(pilot_id=pilot_id).order_by(PsychologicalEval.eval_date.desc()).all()
        social_posts = SocialMediaPost.query.filter_by(pilot_id=pilot_id).all()
        staff_feedback = StaffFeedback.query.filter_by(pilot_id=pilot_id).all()
        flight_logs = FlightLog.query.filter_by(pilot_id=pilot_id).all()
        substance_tests = SubstanceTest.query.filter_by(pilot_id=pilot_id).order_by(SubstanceTest.test_date.desc()).all()
        financial_records = FinancialRecord.query.filter_by(pilot_id=pilot_id).order_by(FinancialRecord.record_date.desc()).all()
        training_records = TrainingRecord.query.filter_by(pilot_id=pilot_id).all()
        incidents = IncidentReport.query.filter_by(pilot_id=pilot_id).all()
        travel_records = TravelRecord.query.filter_by(pilot_id=pilot_id).all()
        phone_records = PhoneRecord.query.filter_by(pilot_id=pilot_id).all()
        email_records = EmailRecord.query.filter_by(pilot_id=pilot_id).all()
        browsing_history = BrowsingHistory.query.filter_by(pilot_id=pilot_id).all()
        message_records = MessageRecord.query.filter_by(pilot_id=pilot_id).all()
        device_records = DeviceRecord.query.filter_by(pilot_id=pilot_id).all()
        location_data = LocationData.query.filter_by(pilot_id=pilot_id).all()
        
        # Run all module assessments
        medical_result = medical_assessor.assess(pilot, medical_records)
        psych_result = psych_assessor.assess(pilot, psych_evals)
        social_result = social_analyzer.assess(pilot, social_posts)
        spe_result = spe_analyzer.assess(pilot, social_posts)
        staff_result = staff_analyzer.assess(pilot, staff_feedback)
        flight_result = flight_analyzer.assess(pilot, flight_logs)
        substance_result = substance_screener.assess(pilot, substance_tests)
        financial_result = financial_checker.assess(pilot, financial_records)
        background_result = background_checker.assess(pilot, incidents)
        fatigue_result = fatigue_analyzer.assess(pilot, flight_logs, medical_records)
        training_result = training_validator.assess(pilot, training_records)
        travel_result = travel_analyzer.assess(pilot, travel_records)
        behavior_result = behavior_analyzer.assess(pilot, flight_logs, staff_feedback, social_posts, medical_records)
        digital_result = digital_analyzer.assess(pilot, phone_records, email_records, browsing_history, message_records, device_records, location_data)
        radicalization_result = radicalization_detector.assess(pilot, social_posts, message_records, browsing_history, email_records, staff_feedback)
        
        # Calculate overall score
        module_results = {
            'medical': medical_result,
            'psychological': psych_result,
            'social_media': social_result,
            'socio_political_economic': spe_result,
            'staff_feedback': staff_result,
            'flight_history': flight_result,
            'substance_abuse': substance_result,
            'financial_stability': financial_result,
            'background_check': background_result,
            'fatigue_lifestyle': fatigue_result,
            'training_certification': training_result,
            'travel_history': travel_result,
            'behavior_pattern': behavior_result,
            'digital_footprint': digital_result,
            'radicalization': radicalization_result,
        }
        
        overall = scoring_engine.calculate(module_results)
        
        # Create assessment record
        assessment = Assessment(
            pilot_id=pilot_id,
            assessed_by=request.form.get('assessed_by', 'AI System'),
            medical_score=medical_result['score'],
            psychological_score=psych_result['score'],
            social_media_score=social_result['score'],
            socio_political_economic_score=spe_result['score'],
            staff_feedback_score=staff_result['score'],
            flight_history_score=flight_result['score'],
            substance_abuse_score=substance_result['score'],
            financial_stability_score=financial_result['score'],
            background_check_score=background_result['score'],
            fatigue_lifestyle_score=fatigue_result['score'],
            training_certification_score=training_result['score'],
            travel_history_score=travel_result['score'],
            behavior_pattern_score=behavior_result['score'],
            digital_footprint_score=digital_result['score'],
            radicalization_score=radicalization_result['score'],
            overall_score=overall['overall_score'],
            fitness_status=overall['fitness_status'],
            risk_level=overall['risk_level'],
            module_results=json.dumps(module_results),
            red_flags=json.dumps(overall['red_flags']),
            recommendations=json.dumps(overall['recommendations']),
            conditions=json.dumps(overall.get('conditions', [])),
        )
        db.session.add(assessment)
        db.session.commit()
        
        flash(f'Assessment completed! Overall Score: {overall["overall_score"]:.1f}/100 - Status: {overall["fitness_status"]}', 'success')
        return redirect(url_for('assessment_report', assessment_id=assessment.id))
    
    return render_template('run_assessment.html', pilot=pilot)


@app.route('/assessment/<int:assessment_id>')
def assessment_report(assessment_id):
    """View assessment report"""
    assessment = Assessment.query.get_or_404(assessment_id)
    pilot = assessment.pilot
    module_results = json.loads(assessment.module_results) if assessment.module_results else {}
    red_flags = json.loads(assessment.red_flags) if assessment.red_flags else []
    recommendations = json.loads(assessment.recommendations) if assessment.recommendations else []
    conditions = json.loads(assessment.conditions) if assessment.conditions else []
    
    return render_template('assessment_report.html',
                         assessment=assessment,
                         pilot=pilot,
                         module_results=module_results,
                         red_flags=red_flags,
                         recommendations=recommendations,
                         conditions=conditions)


@app.route('/api/pilots', methods=['GET'])
def api_list_pilots():
    """API: List all pilots"""
    pilots = Pilot.query.all()
    return jsonify([p.to_dict() for p in pilots])


@app.route('/api/pilot/<int:pilot_id>', methods=['GET'])
def api_pilot_detail(pilot_id):
    """API: Get pilot detail"""
    pilot = Pilot.query.get_or_404(pilot_id)
    return jsonify(pilot.to_dict())


@app.route('/api/assess/<int:pilot_id>', methods=['POST'])
def api_run_assessment(pilot_id):
    """API: Run assessment"""
    pilot = Pilot.query.get_or_404(pilot_id)
    
    medical_records = MedicalRecord.query.filter_by(pilot_id=pilot_id).order_by(MedicalRecord.exam_date.desc()).all()
    psych_evals = PsychologicalEval.query.filter_by(pilot_id=pilot_id).order_by(PsychologicalEval.eval_date.desc()).all()
    social_posts = SocialMediaPost.query.filter_by(pilot_id=pilot_id).all()
    staff_feedback = StaffFeedback.query.filter_by(pilot_id=pilot_id).all()
    flight_logs = FlightLog.query.filter_by(pilot_id=pilot_id).all()
    substance_tests = SubstanceTest.query.filter_by(pilot_id=pilot_id).order_by(SubstanceTest.test_date.desc()).all()
    financial_records = FinancialRecord.query.filter_by(pilot_id=pilot_id).order_by(FinancialRecord.record_date.desc()).all()
    training_records = TrainingRecord.query.filter_by(pilot_id=pilot_id).all()
    incidents = IncidentReport.query.filter_by(pilot_id=pilot_id).all()
    travel_records = TravelRecord.query.filter_by(pilot_id=pilot_id).all()
    phone_records = PhoneRecord.query.filter_by(pilot_id=pilot_id).all()
    email_records = EmailRecord.query.filter_by(pilot_id=pilot_id).all()
    browsing_history = BrowsingHistory.query.filter_by(pilot_id=pilot_id).all()
    message_records = MessageRecord.query.filter_by(pilot_id=pilot_id).all()
    device_records = DeviceRecord.query.filter_by(pilot_id=pilot_id).all()
    location_data = LocationData.query.filter_by(pilot_id=pilot_id).all()
    
    medical_result = medical_assessor.assess(pilot, medical_records)
    psych_result = psych_assessor.assess(pilot, psych_evals)
    social_result = social_analyzer.assess(pilot, social_posts)
    spe_result = spe_analyzer.assess(pilot, social_posts)
    staff_result = staff_analyzer.assess(pilot, staff_feedback)
    flight_result = flight_analyzer.assess(pilot, flight_logs)
    substance_result = substance_screener.assess(pilot, substance_tests)
    financial_result = financial_checker.assess(pilot, financial_records)
    background_result = background_checker.assess(pilot, incidents)
    fatigue_result = fatigue_analyzer.assess(pilot, flight_logs, medical_records)
    training_result = training_validator.assess(pilot, training_records)
    travel_result = travel_analyzer.assess(pilot, travel_records)
    behavior_result = behavior_analyzer.assess(pilot, flight_logs, staff_feedback, social_posts, medical_records)
    digital_result = digital_analyzer.assess(pilot, phone_records, email_records, browsing_history, message_records, device_records, location_data)
    radicalization_result = radicalization_detector.assess(pilot, social_posts, message_records, browsing_history, email_records, staff_feedback)
    
    module_results = {
        'medical': medical_result,
        'psychological': psych_result,
        'social_media': social_result,
        'socio_political_economic': spe_result,
        'staff_feedback': staff_result,
        'flight_history': flight_result,
        'substance_abuse': substance_result,
        'financial_stability': financial_result,
        'background_check': background_result,
        'fatigue_lifestyle': fatigue_result,
        'training_certification': training_result,
        'travel_history': travel_result,
        'behavior_pattern': behavior_result,
        'digital_footprint': digital_result,
        'radicalization': radicalization_result,
    }
    
    overall = scoring_engine.calculate(module_results)
    
    return jsonify({
        'pilot': pilot.to_dict(),
        'module_results': module_results,
        'overall': overall,
        'assessment_date': datetime.utcnow().isoformat(),
    })


@app.route('/api/assessments', methods=['GET'])
def api_list_assessments():
    """API: List all assessments"""
    assessments = Assessment.query.order_by(Assessment.assessment_date.desc()).all()
    return jsonify([a.to_dict() for a in assessments])


# ============================================================
# ADDITIONAL DATA ENTRY ROUTES
# ============================================================

@app.route('/pilot/<int:pilot_id>/medical/add', methods=['POST'])
def add_medical_record(pilot_id):
    data = request.form
    record = MedicalRecord(
        pilot_id=pilot_id,
        exam_date=datetime.strptime(data['exam_date'], '%Y-%m-%d').date(),
        examiner_name=data.get('examiner_name', ''),
        examiner_id=data.get('examiner_id', ''),
        vision_left_eye=data.get('vision_left_eye', ''),
        vision_right_eye=data.get('vision_right_eye', ''),
        color_vision=data.get('color_vision', ''),
        corrective_lenses_required=data.get('corrective_lenses_required') == 'on',
        hearing_left_ear=data.get('hearing_left_ear', ''),
        hearing_right_ear=data.get('hearing_right_ear', ''),
        hearing_aid_required=data.get('hearing_aid_required') == 'on',
        blood_pressure_systolic=int(data.get('bp_systolic', 0)) if data.get('bp_systolic') else None,
        blood_pressure_diastolic=int(data.get('bp_diastolic', 0)) if data.get('bp_diastolic') else None,
        heart_rate=int(data.get('heart_rate', 0)) if data.get('heart_rate') else None,
        ecg_result=data.get('ecg_result', ''),
        cholesterol_total=float(data.get('cholesterol_total', 0)) if data.get('cholesterol_total') else None,
        cholesterol_ldl=float(data.get('cholesterol_ldl', 0)) if data.get('cholesterol_ldl') else None,
        cholesterol_hdl=float(data.get('cholesterol_hdl', 0)) if data.get('cholesterol_hdl') else None,
        lung_function_fev1=float(data.get('fev1', 0)) if data.get('fev1') else None,
        lung_function_fvc=float(data.get('fvc', 0)) if data.get('fvc') else None,
        respiratory_conditions=data.get('respiratory_conditions', ''),
        height_cm=float(data.get('height_cm', 0)) if data.get('height_cm') else None,
        weight_kg=float(data.get('weight_kg', 0)) if data.get('weight_kg') else None,
        bmi=float(data.get('bmi', 0)) if data.get('bmi') else None,
        mobility_issues=data.get('mobility_issues', ''),
        neurological_conditions=data.get('neurological_conditions', ''),
        seizure_history=data.get('seizure_history') == 'on',
        epilepsy=data.get('epilepsy') == 'on',
        psychiatric_conditions=data.get('psychiatric_conditions', ''),
        current_medications=data.get('current_medications', ''),
        medication_side_effects=data.get('medication_side_effects', ''),
        alcohol_consumption=data.get('alcohol_consumption', ''),
        tobacco_use=data.get('tobacco_use', ''),
        drug_use_history=data.get('drug_use_history', ''),
        blood_test_result=data.get('blood_test_result', ''),
        urine_test_result=data.get('urine_test_result', ''),
        drug_screen_result=data.get('drug_screen_result', ''),
        alcohol_test_result=data.get('alcohol_test_result', ''),
        medical_fitness=data.get('medical_fitness', ''),
        restrictions=data.get('restrictions', ''),
        follow_up_required=data.get('follow_up_required') == 'on',
        follow_up_date=datetime.strptime(data['follow_up_date'], '%Y-%m-%d').date() if data.get('follow_up_date') else None,
        notes=data.get('notes', ''),
    )
    db.session.add(record)
    db.session.commit()
    flash('Medical record added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/flight/add', methods=['POST'])
def add_flight_log(pilot_id):
    data = request.form
    log = FlightLog(
        pilot_id=pilot_id,
        flight_date=datetime.strptime(data['flight_date'], '%Y-%m-%d').date(),
        aircraft_type=data.get('aircraft_type', ''),
        aircraft_registration=data.get('aircraft_registration', ''),
        departure_airport=data.get('departure_airport', ''),
        arrival_airport=data.get('arrival_airport', ''),
        flight_type=data.get('flight_type', ''),
        flight_rules=data.get('flight_rules', ''),
        flight_duration_minutes=int(data.get('flight_duration_minutes', 0)) if data.get('flight_duration_minutes') else None,
        night_flight=data.get('night_flight') == 'on',
        instrument_time=int(data.get('instrument_time', 0)) if data.get('instrument_time') else 0,
        landings=int(data.get('landings', 1)) if data.get('landings') else 1,
        incidents=data.get('incidents', ''),
        weather_conditions=data.get('weather_conditions', ''),
        crew_members=data.get('crew_members', ''),
        remarks=data.get('remarks', ''),
    )
    db.session.add(log)
    db.session.commit()
    flash('Flight log added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/feedback/add', methods=['POST'])
def add_staff_feedback(pilot_id):
    data = request.form
    feedback = StaffFeedback(
        pilot_id=pilot_id,
        feedback_date=datetime.strptime(data.get('feedback_date', datetime.utcnow().strftime('%Y-%m-%d')), '%Y-%m-%d').date(),
        feedback_provider_name=data.get('feedback_provider_name', ''),
        feedback_provider_role=data.get('feedback_provider_role', ''),
        feedback_provider_id=data.get('feedback_provider_id', ''),
        relationship_duration_months=int(data.get('relationship_duration_months', 0)) if data.get('relationship_duration_months') else None,
        professionalism_rating=int(data.get('professionalism_rating', 3)) if data.get('professionalism_rating') else None,
        communication_rating=int(data.get('communication_rating', 3)) if data.get('communication_rating') else None,
        teamwork_rating=int(data.get('teamwork_rating', 3)) if data.get('teamwork_rating') else None,
        decision_making_rating=int(data.get('decision_making_rating', 3)) if data.get('decision_making_rating') else None,
        stress_management_rating=int(data.get('stress_management_rating', 3)) if data.get('stress_management_rating') else None,
        punctuality_rating=int(data.get('punctuality_rating', 3)) if data.get('punctuality_rating') else None,
        technical_knowledge_rating=int(data.get('technical_knowledge_rating', 3)) if data.get('technical_knowledge_rating') else None,
        situational_awareness_rating=int(data.get('situational_awareness_rating', 3)) if data.get('situational_awareness_rating') else None,
        leadership_rating=int(data.get('leadership_rating', 3)) if data.get('leadership_rating') else None,
        overall_rating=int(data.get('overall_rating', 3)) if data.get('overall_rating') else None,
        would_fly_with_again=data.get('would_fly_with_again', ''),
        strengths=data.get('strengths', ''),
        areas_for_improvement=data.get('areas_for_improvement', ''),
        concerns=data.get('concerns', ''),
        additional_comments=data.get('additional_comments', ''),
        signs_of_stress=data.get('signs_of_stress') == 'on',
        signs_of_fatigue=data.get('signs_of_fatigue') == 'on',
        signs_of_substance_use=data.get('signs_of_substance_use') == 'on',
        signs_of_aggression=data.get('signs_of_aggression') == 'on',
        signs_of_depression=data.get('signs_of_depression') == 'on',
        signs_of_financial_stress=data.get('signs_of_financial_stress') == 'on',
        verified_by=data.get('verified_by', ''),
        is_anonymous=data.get('is_anonymous') == 'on',
    )
    db.session.add(feedback)
    db.session.commit()
    flash('Staff feedback added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/social/add', methods=['POST'])
def add_social_media_post(pilot_id):
    data = request.form
    content = data.get('post_content', '')
    
    sentiment_score, sentiment_label = social_analyzer.analyze_sentiment(content)
    topics = social_analyzer.extract_topics(content)
    entities = social_analyzer.extract_entities(content)
    contains_profanity = social_analyzer.check_profanity(content)
    contains_violence = social_analyzer.check_violence(content)
    contains_political = social_analyzer.check_political_content(content)
    contains_extremist = social_analyzer.check_extremist_content(content)
    contains_discriminatory = social_analyzer.check_discriminatory_content(content)
    contains_confidential = social_analyzer.check_company_confidential(content)
    contains_alcohol_drugs = social_analyzer.check_alcohol_drugs(content)
    risk_indicators = social_analyzer.identify_risk_indicators(content)
    
    flagged = any([contains_profanity, contains_violence, contains_extremist,
                   contains_discriminatory, contains_confidential, len(risk_indicators) > 0])
    
    post = SocialMediaPost(
        pilot_id=pilot_id,
        platform=data.get('platform', 'Twitter'),
        post_date=datetime.strptime(data.get('post_date', datetime.utcnow().strftime('%Y-%m-%d')), '%Y-%m-%d') if data.get('post_date') else datetime.utcnow(),
        post_content=content,
        post_type=data.get('post_type', 'Text'),
        likes_count=int(data.get('likes_count', 0)) if data.get('likes_count') else 0,
        shares_count=int(data.get('shares_count', 0)) if data.get('shares_count') else 0,
        comments_count=int(data.get('comments_count', 0)) if data.get('comments_count') else 0,
        sentiment_score=sentiment_score,
        sentiment_label=sentiment_label,
        flagged=flagged,
        flag_reason=json.dumps(risk_indicators) if flagged else None,
        topics=json.dumps(topics),
        entities=json.dumps(entities),
        language=data.get('language', 'en'),
        contains_profanity=contains_profanity,
        contains_violence=contains_violence,
        contains_political_content=contains_political,
        contains_extremist_content=contains_extremist,
        contains_discriminatory_content=contains_discriminatory,
        contains_company_confidential=contains_confidential,
        contains_alcohol_drugs=contains_alcohol_drugs,
        risk_indicators=json.dumps(risk_indicators),
    )
    db.session.add(post)
    db.session.commit()
    flash('Social media post added and analyzed!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/training/add', methods=['POST'])
def add_training_record(pilot_id):
    data = request.form
    record = TrainingRecord(
        pilot_id=pilot_id,
        training_type=data.get('training_type', ''),
        training_date=datetime.strptime(data['training_date'], '%Y-%m-%d').date() if data.get('training_date') else None,
        expiry_date=datetime.strptime(data['expiry_date'], '%Y-%m-%d').date() if data.get('expiry_date') else None,
        training_provider=data.get('training_provider', ''),
        instructor_name=data.get('instructor_name', ''),
        result=data.get('result', ''),
        score=float(data.get('score', 0)) if data.get('score') else None,
        remedial_required=data.get('remedial_required') == 'on',
        remedial_completed=data.get('remedial_completed') == 'on',
        notes=data.get('notes', ''),
    )
    db.session.add(record)
    db.session.commit()
    flash('Training record added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/incident/add', methods=['POST'])
def add_incident_report(pilot_id):
    data = request.form
    incident = IncidentReport(
        pilot_id=pilot_id,
        incident_date=datetime.strptime(data['incident_date'], '%Y-%m-%d').date() if data.get('incident_date') else None,
        incident_type=data.get('incident_type', ''),
        severity=data.get('severity', ''),
        description=data.get('description', ''),
        investigation_findings=data.get('investigation_findings', ''),
        pilot_at_fault=data.get('pilot_at_fault') == 'on',
        corrective_actions=data.get('corrective_actions', ''),
        status=data.get('status', 'Open'),
    )
    db.session.add(incident)
    db.session.commit()
    flash('Incident report added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/financial/add', methods=['POST'])
def add_financial_record(pilot_id):
    data = request.form
    record = FinancialRecord(
        pilot_id=pilot_id,
        record_date=datetime.strptime(data.get('record_date', datetime.utcnow().strftime('%Y-%m-%d')), '%Y-%m-%d').date(),
        annual_income=float(data.get('annual_income', 0)) if data.get('annual_income') else None,
        total_debt=float(data.get('total_debt', 0)) if data.get('total_debt') else None,
        credit_score=int(data.get('credit_score', 0)) if data.get('credit_score') else None,
        bankruptcy_history=data.get('bankruptcy_history') == 'on',
        payment_delinquencies=int(data.get('payment_delinquencies', 0)) if data.get('payment_delinquencies') else 0,
        gambling_concerns=data.get('gambling_concerns') == 'on',
        financial_stress_indicators=data.get('financial_stress_indicators', ''),
        source_of_wealth_verified=data.get('source_of_wealth_verified') == 'on',
        notes=data.get('notes', ''),
    )
    db.session.add(record)
    db.session.commit()
    flash('Financial record added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/substance/add', methods=['POST'])
def add_substance_test(pilot_id):
    data = request.form
    test = SubstanceTest(
        pilot_id=pilot_id,
        test_date=datetime.strptime(data['test_date'], '%Y-%m-%d').date(),
        test_type=data.get('test_type', ''),
        test_method=data.get('test_method', ''),
        alcohol_result=data.get('alcohol_result', ''),
        alcohol_level=float(data.get('alcohol_level', 0)) if data.get('alcohol_level') else None,
        amphetamines=data.get('amphetamines', ''),
        cocaine=data.get('cocaine', ''),
        opiates=data.get('opiates', ''),
        cannabis=data.get('cannabis', ''),
        benzodiazepines=data.get('benzodiazepines', ''),
        pcp=data.get('pcp', ''),
        overall_result=data.get('overall_result', ''),
        tested_by=data.get('tested_by', ''),
        verified=data.get('verified') == 'on',
        notes=data.get('notes', ''),
    )
    db.session.add(test)
    db.session.commit()
    flash('Substance test record added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/psych/add', methods=['POST'])
def add_psych_eval(pilot_id):
    data = request.form
    eval_record = PsychologicalEval(
        pilot_id=pilot_id,
        eval_date=datetime.strptime(data['eval_date'], '%Y-%m-%d').date(),
        evaluator_name=data.get('evaluator_name', ''),
        evaluator_license=data.get('evaluator_license', ''),
        mmpi2_validity=data.get('mmpi2_validity', ''),
        mmpi2_hs=float(data.get('mmpi2_hs', 0)) if data.get('mmpi2_hs') else None,
        mmpi2_d=float(data.get('mmpi2_d', 0)) if data.get('mmpi2_d') else None,
        mmpi2_hy=float(data.get('mmpi2_hy', 0)) if data.get('mmpi2_hy') else None,
        mmpi2_pd=float(data.get('mmpi2_pd', 0)) if data.get('mmpi2_pd') else None,
        mmpi2_mf=float(data.get('mmpi2_mf', 0)) if data.get('mmpi2_mf') else None,
        mmpi2_pa=float(data.get('mmpi2_pa', 0)) if data.get('mmpi2_pa') else None,
        mmpi2_pt=float(data.get('mmpi2_pt', 0)) if data.get('mmpi2_pt') else None,
        mmpi2_sc=float(data.get('mmpi2_sc', 0)) if data.get('mmpi2_sc') else None,
        mmpi2_ma=float(data.get('mmpi2_ma', 0)) if data.get('mmpi2_ma') else None,
        mmpi2_si=float(data.get('mmpi2_si', 0)) if data.get('mmpi2_si') else None,
        big5_openness=float(data.get('big5_openness', 0)) if data.get('big5_openness') else None,
        big5_conscientiousness=float(data.get('big5_conscientiousness', 0)) if data.get('big5_conscientiousness') else None,
        big5_extraversion=float(data.get('big5_extraversion', 0)) if data.get('big5_extraversion') else None,
        big5_agreeableness=float(data.get('big5_agreeableness', 0)) if data.get('big5_agreeableness') else None,
        big5_neuroticism=float(data.get('big5_neuroticism', 0)) if data.get('big5_neuroticism') else None,
        anxiety_level=data.get('anxiety_level', ''),
        depression_level=data.get('depression_level', ''),
        stress_level=data.get('stress_level', ''),
        aggression_level=data.get('aggression_level', ''),
        impulsivity_level=data.get('impulsivity_level', ''),
        risk_taking_tendency=data.get('risk_taking_tendency', ''),
        cognitive_function=data.get('cognitive_function', ''),
        memory_function=data.get('memory_function', ''),
        attention_function=data.get('attention_function', ''),
        decision_making_quality=data.get('decision_making_quality', ''),
        psychological_fitness=data.get('psychological_fitness', ''),
        recommendations=data.get('recommendations', ''),
        follow_up_needed=data.get('follow_up_needed') == 'on',
        notes=data.get('notes', ''),
    )
    db.session.add(eval_record)
    db.session.commit()
    flash('Psychological evaluation added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/travel/add', methods=['POST'])
def add_travel_record(pilot_id):
    data = request.form
    record = TravelRecord(
        pilot_id=pilot_id,
        departure_date=datetime.strptime(data['departure_date'], '%Y-%m-%d').date() if data.get('departure_date') else None,
        return_date=datetime.strptime(data['return_date'], '%Y-%m-%d').date() if data.get('return_date') else None,
        destination=data.get('destination', ''),
        purpose=data.get('purpose', ''),
        trip_type=data.get('trip_type', ''),
        booking_date=datetime.strptime(data['booking_date'], '%Y-%m-%d').date() if data.get('booking_date') else None,
        companion=data.get('companion', ''),
        visa_status=data.get('visa_status', ''),
        foreign_contacts=data.get('foreign_contacts', ''),
        notes=data.get('notes', ''),
    )
    db.session.add(record)
    db.session.commit()
    flash('Travel record added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/phone/add', methods=['POST'])
def add_phone_record(pilot_id):
    data = request.form
    record = PhoneRecord(
        pilot_id=pilot_id,
        call_date=datetime.strptime(data.get('call_date', datetime.utcnow().strftime('%Y-%m-%d')), '%Y-%m-%d') if data.get('call_date') else datetime.utcnow(),
        call_time=datetime.strptime(data.get('call_time', datetime.utcnow().strftime('%H:%M')), '%H:%M') if data.get('call_time') else datetime.utcnow(),
        duration_seconds=int(data.get('duration_seconds', 0)) if data.get('duration_seconds') else None,
        contact_name=data.get('contact_name', ''),
        contact_number=data.get('contact_number', ''),
        contact_type=data.get('contact_type', ''),
        is_international=data.get('is_international') == 'on',
        is_known_associate=data.get('is_known_associate') == 'on',
        is_prepaid=data.get('is_prepaid') == 'on',
        call_direction=data.get('call_direction', ''),
        notes=data.get('notes', ''),
    )
    db.session.add(record)
    db.session.commit()
    flash('Phone record added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/email/add', methods=['POST'])
def add_email_record(pilot_id):
    data = request.form
    record = EmailRecord(
        pilot_id=pilot_id,
        email_date=datetime.strptime(data.get('email_date', datetime.utcnow().strftime('%Y-%m-%d')), '%Y-%m-%d') if data.get('email_date') else datetime.utcnow(),
        sender=data.get('sender', ''),
        recipient=data.get('recipient', ''),
        subject=data.get('subject', ''),
        body=data.get('body', ''),
        is_internal=data.get('is_internal') == 'on',
        is_encrypted=data.get('is_encrypted') == 'on',
        has_large_attachment=data.get('has_large_attachment') == 'on',
        to_personal_account=data.get('to_personal_account') == 'on',
        notes=data.get('notes', ''),
    )
    db.session.add(record)
    db.session.commit()
    flash('Email record added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/browsing/add', methods=['POST'])
def add_browsing_record(pilot_id):
    data = request.form
    record = BrowsingHistory(
        pilot_id=pilot_id,
        access_time=datetime.strptime(data.get('access_time', datetime.utcnow().strftime('%Y-%m-%d %H:%M')), '%Y-%m-%d %H:%M') if data.get('access_time') else datetime.utcnow(),
        url=data.get('url', ''),
        title=data.get('title', ''),
        category=data.get('category', ''),
        is_work_related=data.get('is_work_related') == 'on',
        is_non_work_related=data.get('is_non_work_related') == 'on',
        is_political_content=data.get('is_political_content') == 'on',
        is_job_search=data.get('is_job_search') == 'on',
        is_financial_stress=data.get('is_financial_stress') == 'on',
        is_cleared=data.get('is_cleared') == 'on',
        duration_seconds=int(data.get('duration_seconds', 0)) if data.get('duration_seconds') else None,
    )
    db.session.add(record)
    db.session.commit()
    flash('Browsing record added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/message/add', methods=['POST'])
def add_message_record(pilot_id):
    data = request.form
    record = MessageRecord(
        pilot_id=pilot_id,
        message_time=datetime.strptime(data.get('message_time', datetime.utcnow().strftime('%Y-%m-%d %H:%M')), '%Y-%m-%d %H:%M') if data.get('message_time') else datetime.utcnow(),
        sender=data.get('sender', ''),
        recipient=data.get('recipient', ''),
        content=data.get('content', ''),
        platform=data.get('platform', ''),
        is_unknown_contact=data.get('is_unknown_contact') == 'on',
        is_deleted=data.get('is_deleted') == 'on',
        is_encrypted_app=data.get('is_encrypted_app') == 'on',
        notes=data.get('notes', ''),
    )
    db.session.add(record)
    db.session.commit()
    flash('Message record added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/device/add', methods=['POST'])
def add_device_record(pilot_id):
    data = request.form
    record = DeviceRecord(
        pilot_id=pilot_id,
        device_id=data.get('device_id', ''),
        device_type=data.get('device_type', ''),
        os_version=data.get('os_version', ''),
        is_authorized=data.get('is_authorized') == 'on',
        is_tampered=data.get('is_tampered') == 'on',
        uses_vpn=data.get('uses_vpn') == 'on',
        has_factory_reset=data.get('has_factory_reset') == 'on',
        is_shared=data.get('is_shared') == 'on',
        has_outdated_security=data.get('has_outdated_security') == 'on',
        last_check=datetime.utcnow(),
        notes=data.get('notes', ''),
    )
    db.session.add(record)
    db.session.commit()
    flash('Device record added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


@app.route('/pilot/<int:pilot_id>/location/add', methods=['POST'])
def add_location_data(pilot_id):
    data = request.form
    record = LocationData(
        pilot_id=pilot_id,
        timestamp=datetime.strptime(data.get('timestamp', datetime.utcnow().strftime('%Y-%m-%d %H:%M')), '%Y-%m-%d %H:%M') if data.get('timestamp') else datetime.utcnow(),
        location=data.get('location', ''),
        latitude=float(data.get('latitude', 0)) if data.get('latitude') else None,
        longitude=float(data.get('longitude', 0)) if data.get('longitude') else None,
        is_unusual=data.get('is_unusual') == 'on',
        is_high_risk_area=data.get('is_high_risk_area') == 'on',
        is_spoofed=data.get('is_spoofed') == 'on',
        has_gap=data.get('has_gap') == 'on',
        is_border_crossing=data.get('is_border_crossing') == 'on',
        source=data.get('source', ''),
        notes=data.get('notes', ''),
    )
    db.session.add(record)
    db.session.commit()
    flash('Location data added successfully!', 'success')
    return redirect(url_for('pilot_detail', pilot_id=pilot_id))


# ============================================================
# REPORTS & ANALYTICS
# ============================================================

@app.route('/search')
def search_pilots():
    """Search pilots by name, ID, or airline"""
    name = request.args.get('name', '').strip()
    pilot_id = request.args.get('pilot_id', '').strip()
    airline = request.args.get('airline', '').strip()
    
    pilots = Pilot.query
    
    if name:
        pilots = pilots.filter(
            db.or_(
                Pilot.first_name.ilike(f'%{name}%'),
                Pilot.last_name.ilike(f'%{name}%')
            )
        )
    
    if pilot_id:
        pilots = pilots.filter(Pilot.pilot_id.ilike(f'%{pilot_id}%'))
    
    if airline:
        pilots = pilots.filter(Pilot.airline.ilike(f'%{airline}%'))
    
    pilots = pilots.order_by(Pilot.last_name).all()
    
    return render_template('search.html', pilots=pilots)


@app.route('/reports')
def reports():
    """Reports and analytics page"""
    total_pilots = Pilot.query.count()
    total_assessments = Assessment.query.count()
    
    score_ranges = {
        '90-100': Assessment.query.filter(Assessment.overall_score >= 90).count(),
        '80-89': Assessment.query.filter(Assessment.overall_score >= 80, Assessment.overall_score < 90).count(),
        '70-79': Assessment.query.filter(Assessment.overall_score >= 70, Assessment.overall_score < 80).count(),
        '60-69': Assessment.query.filter(Assessment.overall_score >= 60, Assessment.overall_score < 70).count(),
        '0-59': Assessment.query.filter(Assessment.overall_score < 60).count(),
    }
    
    risk_distribution = {
        'LOW': Assessment.query.filter_by(risk_level='LOW').count(),
        'MEDIUM': Assessment.query.filter_by(risk_level='MEDIUM').count(),
        'HIGH': Assessment.query.filter_by(risk_level='HIGH').count(),
        'CRITICAL': Assessment.query.filter_by(risk_level='CRITICAL').count(),
    }
    
    fitness_distribution = {
        'FIT': Assessment.query.filter_by(fitness_status='FIT').count(),
        'CONDITIONAL': Assessment.query.filter_by(fitness_status='CONDITIONAL').count(),
        'UNFIT': Assessment.query.filter_by(fitness_status='UNFIT').count(),
    }
    
    avg_medical = db.session.query(db.func.avg(Assessment.medical_score)).scalar() or 0
    avg_psych = db.session.query(db.func.avg(Assessment.psychological_score)).scalar() or 0
    avg_social = db.session.query(db.func.avg(Assessment.social_media_score)).scalar() or 0
    avg_spe = db.session.query(db.func.avg(Assessment.socio_political_economic_score)).scalar() or 0
    avg_staff = db.session.query(db.func.avg(Assessment.staff_feedback_score)).scalar() or 0
    avg_flight = db.session.query(db.func.avg(Assessment.flight_history_score)).scalar() or 0
    avg_substance = db.session.query(db.func.avg(Assessment.substance_abuse_score)).scalar() or 0
    avg_financial = db.session.query(db.func.avg(Assessment.financial_stability_score)).scalar() or 0
    avg_background = db.session.query(db.func.avg(Assessment.background_check_score)).scalar() or 0
    avg_fatigue = db.session.query(db.func.avg(Assessment.fatigue_lifestyle_score)).scalar() or 0
    avg_training = db.session.query(db.func.avg(Assessment.training_certification_score)).scalar() or 0
    avg_travel = db.session.query(db.func.avg(Assessment.travel_history_score)).scalar() or 0
    avg_behavior = db.session.query(db.func.avg(Assessment.behavior_pattern_score)).scalar() or 0
    avg_digital = db.session.query(db.func.avg(Assessment.digital_footprint_score)).scalar() or 0
    avg_radicalization = db.session.query(db.func.avg(Assessment.radicalization_score)).scalar() or 0
    
    return render_template('reports.html',
                         total_pilots=total_pilots,
                         total_assessments=total_assessments,
                         score_ranges=score_ranges,
                         risk_distribution=risk_distribution,
                         fitness_distribution=fitness_distribution,
                         avg_scores={
                             'Medical': avg_medical,
                             'Psychological': avg_psych,
                             'Social Media': avg_social,
                             'Socio-Pol-Econ': avg_spe,
                             'Staff Feedback': avg_staff,
                             'Flight History': avg_flight,
                             'Substance Abuse': avg_substance,
                             'Financial': avg_financial,
                             'Background': avg_background,
                             'Fatigue': avg_fatigue,
                             'Training': avg_training,
                             'Travel History': avg_travel,
                             'Behavior Pattern': avg_behavior,
                             'Digital Footprint': avg_digital,
                             'Radicalization': avg_radicalization,
                         })


# ============================================================
# INITIALIZATION
# ============================================================

def create_sample_data():
    """Create sample data for demonstration"""
    if Pilot.query.first():
        return
    
    pilots_data = [
        {
            'pilot_id': 'PLT-001',
            'first_name': 'James',
            'last_name': 'Mitchell',
            'date_of_birth': datetime(1985, 3, 15).date(),
            'nationality': 'American',
            'license_number': 'ATPL-US-2010-45678',
            'license_type': 'ATPL',
            'license_issue_date': datetime(2010, 6, 1).date(),
            'license_expiry_date': datetime(2025, 6, 1).date(),
            'medical_certificate_class': 'Class 1',
            'medical_expiry': datetime(2025, 3, 15).date(),
            'total_flight_hours': 8500,
            'aircraft_type_ratings': json.dumps(['B737', 'A320', 'B777']),
            'airline': 'American Airlines',
            'base_airport': 'DFW',
            'years_experience': 14,
            'email': 'james.mitchell@email.com',
            'phone': '+1-555-0101',
            'social_media_handles': json.dumps({'twitter': '@jamesm_pilot', 'instagram': 'jamesmitchell_fly'}),
        },
        {
            'pilot_id': 'PLT-002',
            'first_name': 'Sarah',
            'last_name': 'Chen',
            'date_of_birth': datetime(1990, 7, 22).date(),
            'nationality': 'Canadian',
            'license_number': 'ATPL-CA-2015-78901',
            'license_type': 'ATPL',
            'license_issue_date': datetime(2015, 9, 1).date(),
            'license_expiry_date': datetime(2025, 9, 1).date(),
            'medical_certificate_class': 'Class 1',
            'medical_expiry': datetime(2025, 7, 22).date(),
            'total_flight_hours': 5200,
            'aircraft_type_ratings': json.dumps(['A320', 'A330', 'B787']),
            'airline': 'Air Canada',
            'base_airport': 'YYZ',
            'years_experience': 9,
            'email': 'sarah.chen@email.com',
            'phone': '+1-555-0102',
            'social_media_handles': json.dumps({'twitter': '@sarahchen_aviation', 'linkedin': 'sarah-chen-pilot'}),
        },
        {
            'pilot_id': 'PLT-003',
            'first_name': 'Michael',
            'last_name': 'Rodriguez',
            'date_of_birth': datetime(1978, 11, 8).date(),
            'nationality': 'British',
            'license_number': 'ATPL-UK-2005-12345',
            'license_type': 'ATPL',
            'license_issue_date': datetime(2005, 1, 15).date(),
            'license_expiry_date': datetime(2025, 1, 15).date(),
            'medical_certificate_class': 'Class 1',
            'medical_expiry': datetime(2025, 11, 8).date(),
            'total_flight_hours': 15000,
            'aircraft_type_ratings': json.dumps(['B747', 'B777', 'A380', 'B787']),
            'airline': 'British Airways',
            'base_airport': 'LHR',
            'years_experience': 19,
            'email': 'michael.rodriguez@email.com',
            'phone': '+44-555-0103',
            'social_media_handles': json.dumps({'twitter': '@mrod_captain'}),
        },
    ]
    
    for pdata in pilots_data:
        pilot = Pilot(**pdata)
        db.session.add(pilot)
    
    db.session.commit()
    
    # Add sample medical records
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        med = MedicalRecord(
            pilot_id=pilot1.id,
            exam_date=datetime(2024, 3, 15).date(),
            examiner_name='Dr. Robert Williams',
            examiner_id='AME-US-1234',
            vision_left_eye='20/20',
            vision_right_eye='20/20',
            color_vision='Normal',
            corrective_lenses_required=False,
            hearing_left_ear='Normal',
            hearing_right_ear='Normal',
            blood_pressure_systolic=125,
            blood_pressure_diastolic=82,
            heart_rate=68,
            ecg_result='Normal',
            cholesterol_total=195.0,
            cholesterol_ldl=110.0,
            cholesterol_hdl=55.0,
            lung_function_fev1=4.2,
            lung_function_fvc=5.1,
            height_cm=178.0,
            weight_kg=78.0,
            bmi=24.6,
            neurological_conditions='None',
            seizure_history=False,
            epilepsy=False,
            psychiatric_conditions='None',
            current_medications='None',
            alcohol_consumption='Occasional',
            tobacco_use='Never',
            drug_use_history='None',
            blood_test_result='Normal',
            urine_test_result='Normal',
            drug_screen_result='NEGATIVE',
            alcohol_test_result='NEGATIVE',
            medical_fitness='FIT',
            restrictions='None',
            follow_up_required=False,
            notes='Excellent health condition. No concerns.',
        )
        db.session.add(med)
    
    # Add sample flight logs
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        for i in range(10):
            log = FlightLog(
                pilot_id=pilot1.id,
                flight_date=(datetime(2024, 12, 1) - timedelta(days=i*3)).date(),
                aircraft_type='B737',
                aircraft_registration=f'N{100+i}AA',
                departure_airport='DFW',
                arrival_airport=['LAX', 'JFK', 'ORD', 'MIA', 'SEA'][i % 5],
                flight_type='Domestic',
                flight_rules='IFR',
                flight_duration_minutes=120 + (i * 15),
                night_flight=(i % 3 == 0),
                instrument_time=60 + (i * 5),
                landings=1,
                incidents='None',
                weather_conditions='VMC' if i % 2 == 0 else 'IMC',
                crew_members='FO: Smith, FA: Johnson, FA: Brown',
                remarks='Routine flight',
            )
            db.session.add(log)
    
    # Add sample staff feedback
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        feedback_data = [
            {
                'feedback_provider_name': 'David Smith',
                'feedback_provider_role': 'First Officer',
                'professionalism_rating': 5,
                'communication_rating': 5,
                'teamwork_rating': 5,
                'decision_making_rating': 4,
                'stress_management_rating': 5,
                'punctuality_rating': 5,
                'technical_knowledge_rating': 5,
                'situational_awareness_rating': 4,
                'leadership_rating': 5,
                'overall_rating': 5,
                'would_fly_with_again': 'YES',
                'strengths': 'Excellent CRM, calm under pressure, great mentor',
                'areas_for_improvement': 'Could share more during cruise',
                'concerns': 'None',
            },
            {
                'feedback_provider_name': 'Lisa Johnson',
                'feedback_provider_role': 'Flight Attendant',
                'professionalism_rating': 5,
                'communication_rating': 4,
                'teamwork_rating': 5,
                'decision_making_rating': 4,
                'stress_management_rating': 5,
                'punctuality_rating': 5,
                'technical_knowledge_rating': 4,
                'situational_awareness_rating': 5,
                'leadership_rating': 4,
                'overall_rating': 5,
                'would_fly_with_again': 'YES',
                'strengths': 'Very professional, great with cabin crew coordination',
                'areas_for_improvement': 'Sometimes too focused on technical aspects',
                'concerns': 'None',
            },
        ]
        for fb_data in feedback_data:
            fb = StaffFeedback(pilot_id=pilot1.id, **fb_data)
            db.session.add(fb)
    
    # Add sample social media posts
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        posts = [
            {'platform': 'Twitter', 'post_content': 'Another beautiful day in the skies! Loving my job as a pilot. #aviation #blessed', 'post_type': 'Text'},
            {'platform': 'Instagram', 'post_content': 'Sunset from 35,000 feet. Never gets old! #pilotlife #aviation #sunset', 'post_type': 'Image'},
            {'platform': 'Twitter', 'post_content': 'Important reminder: always prioritize safety over schedule. No flight is worth taking risks.', 'post_type': 'Text'},
        ]
        for post_data in posts:
            content = post_data['post_content']
            sentiment_score, sentiment_label = social_analyzer.analyze_sentiment(content)
            topics = social_analyzer.extract_topics(content)
            post = SocialMediaPost(
                pilot_id=pilot1.id,
                platform=post_data['platform'],
                post_date=datetime(2024, 11, 15),
                post_content=content,
                post_type=post_data['post_type'],
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label,
                topics=json.dumps(topics),
                entities=json.dumps([]),
                flagged=False,
            )
            db.session.add(post)
    
    # Add sample training records
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        trainings = [
            {'training_type': 'B737 Type Rating', 'training_date': datetime(2020, 5, 10).date(), 'expiry_date': datetime(2025, 5, 10).date(), 'training_provider': 'American Airlines Training Center', 'instructor_name': 'Capt. Anderson', 'result': 'PASS', 'score': 95.0},
            {'training_type': 'CRM Recurrent', 'training_date': datetime(2024, 1, 15).date(), 'expiry_date': datetime(2025, 1, 15).date(), 'training_provider': 'American Airlines Training Center', 'instructor_name': 'Capt. Baker', 'result': 'PASS', 'score': 92.0},
            {'training_type': 'Upset Recovery', 'training_date': datetime(2024, 6, 20).date(), 'expiry_date': datetime(2025, 6, 20).date(), 'training_provider': 'American Airlines Training Center', 'instructor_name': 'Capt. Davis', 'result': 'PASS', 'score': 88.0},
        ]
        for t_data in trainings:
            tr = TrainingRecord(pilot_id=pilot1.id, **t_data)
            db.session.add(tr)
    
    # Add sample substance tests
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        test = SubstanceTest(
            pilot_id=pilot1.id,
            test_date=datetime(2024, 6, 1).date(),
            test_type='Random',
            test_method='Urine',
            alcohol_result='NEGATIVE',
            amphetamines='NEGATIVE',
            cocaine='NEGATIVE',
            opiates='NEGATIVE',
            cannabis='NEGATIVE',
            benzodiazepines='NEGATIVE',
            pcp='NEGATIVE',
            overall_result='NEGATIVE',
            tested_by='MedTest Labs Inc.',
            verified=True,
        )
        db.session.add(test)
    
    # Add sample financial record
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        fin = FinancialRecord(
            pilot_id=pilot1.id,
            annual_income=185000.0,
            total_debt=45000.0,
            credit_score=780,
            bankruptcy_history=False,
            payment_delinquencies=0,
            gambling_concerns=False,
            source_of_wealth_verified=True,
            notes='Stable financial situation',
        )
        db.session.add(fin)
    
    # Add sample psychological eval
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        psych = PsychologicalEval(
            pilot_id=pilot1.id,
            eval_date=datetime(2024, 2, 1).date(),
            evaluator_name='Dr. Patricia Moore',
            evaluator_license='PSY-IL-5678',
            mmpi2_validity='Valid',
            mmpi2_hs=52.0,
            mmpi2_d=48.0,
            mmpi2_hy=50.0,
            mmpi2_pd=45.0,
            mmpi2_mf=55.0,
            mmpi2_pa=47.0,
            mmpi2_pt=51.0,
            mmpi2_sc=49.0,
            mmpi2_ma=53.0,
            mmpi2_si=46.0,
            big5_openness=65.0,
            big5_conscientiousness=80.0,
            big5_extraversion=60.0,
            big5_agreeableness=75.0,
            big5_neuroticism=35.0,
            anxiety_level='None',
            depression_level='None',
            stress_level='Mild',
            aggression_level='None',
            impulsivity_level='Low',
            risk_taking_tendency='Low',
            cognitive_function='Normal',
            memory_function='Normal',
            attention_function='Normal',
            decision_making_quality='Excellent',
            psychological_fitness='FIT',
            follow_up_needed=False,
            notes='Psychologically fit for duty. Excellent stress management and decision-making skills.',
        )
        db.session.add(psych)
    
    # Add sample travel records
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        travels = [
            {'departure_date': datetime(2024, 6, 15).date(), 'return_date': datetime(2024, 6, 22).date(), 'destination': 'Hawaii', 'purpose': 'Vacation', 'trip_type': 'Round-trip', 'companion': 'Family'},
            {'departure_date': datetime(2024, 3, 10).date(), 'return_date': datetime(2024, 3, 15).date(), 'destination': 'London', 'purpose': 'Training', 'trip_type': 'Round-trip', 'companion': 'Solo'},
        ]
        for t_data in travels:
            tr = TravelRecord(pilot_id=pilot1.id, **t_data)
            db.session.add(tr)
    
    # Add sample phone records
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        calls = [
            {'call_date': datetime(2024, 12, 1), 'call_time': datetime(2024, 12, 1, 10, 30), 'duration_seconds': 300, 'contact_name': 'Wife', 'contact_number': '+1-555-0201', 'contact_type': 'Family', 'call_direction': 'Outgoing'},
            {'call_date': datetime(2024, 12, 1), 'call_time': datetime(2024, 12, 1, 14, 0), 'duration_seconds': 120, 'contact_name': 'David Smith', 'contact_number': '+1-555-0202', 'contact_type': 'Colleague', 'is_known_associate': True, 'call_direction': 'Incoming'},
        ]
        for c_data in calls:
            cr = PhoneRecord(pilot_id=pilot1.id, **c_data)
            db.session.add(cr)
    
    # Add sample email records
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        emails = [
            {'email_date': datetime(2024, 12, 1, 9, 0), 'sender': 'james.mitchell@email.com', 'recipient': 'training@aa.com', 'subject': 'CRM Recurrent Confirmation', 'body': 'Confirming my attendance for next week.', 'is_internal': True},
            {'email_date': datetime(2024, 12, 1, 11, 0), 'sender': 'james.mitchell@email.com', 'recipient': 'wife@email.com', 'subject': 'Flight Schedule', 'body': 'Sending you my schedule for next month.', 'is_internal': False},
        ]
        for e_data in emails:
            er = EmailRecord(pilot_id=pilot1.id, **e_data)
            db.session.add(er)
    
    # Add sample browsing history
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        browsing = [
            {'access_time': datetime(2024, 12, 1, 8, 0), 'url': 'https://www.faa.gov/regulations', 'title': 'FAA Regulations', 'category': 'Work', 'is_work_related': True},
            {'access_time': datetime(2024, 12, 1, 12, 0), 'url': 'https://www.weather.com', 'title': 'Weather Forecast', 'category': 'Weather', 'is_work_related': True},
        ]
        for b_data in browsing:
            br = BrowsingHistory(pilot_id=pilot1.id, **b_data)
            db.session.add(br)
    
    # Add sample message records
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        messages = [
            {'message_time': datetime(2024, 12, 1, 10, 0), 'sender': 'Wife', 'recipient': 'James', 'content': 'Have a safe flight today!', 'platform': 'SMS'},
            {'message_time': datetime(2024, 12, 1, 15, 0), 'sender': 'James', 'recipient': 'David Smith', 'content': 'See you at briefing tomorrow.', 'platform': 'WhatsApp'},
        ]
        for m_data in messages:
            mr = MessageRecord(pilot_id=pilot1.id, **m_data)
            db.session.add(mr)
    
    # Add sample device records
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        devices = [
            {'device_id': 'DEV-001', 'device_type': 'iPhone', 'os_version': 'iOS 17.1', 'is_authorized': True},
            {'device_id': 'DEV-002', 'device_type': 'iPad', 'os_version': 'iPadOS 17.1', 'is_authorized': True},
        ]
        for d_data in devices:
            dr = DeviceRecord(pilot_id=pilot1.id, **d_data)
            db.session.add(dr)
    
    # Add sample location data
    pilot1 = Pilot.query.filter_by(pilot_id='PLT-001').first()
    if pilot1:
        locations = [
            {'timestamp': datetime(2024, 12, 1, 8, 0), 'location': 'DFW Airport', 'latitude': 32.8998, 'longitude': -97.0403, 'source': 'GPS'},
            {'timestamp': datetime(2024, 12, 1, 18, 0), 'location': 'Home', 'latitude': 32.7767, 'longitude': -96.7970, 'source': 'GPS'},
        ]
        for l_data in locations:
            lr = LocationData(pilot_id=pilot1.id, **l_data)
            db.session.add(lr)
    
    db.session.commit()
    print("Sample data created successfully!")


# ============================================================
# MAIN ENTRY POINT
# ============================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
    
    print("\n" + "="*60)
    print("  PILOT FITNESS ASSESSMENT AI TOOL")
    print("="*60)
    print("\n  Starting server at http://localhost:5000")
    print("\n  Routes:")
    print("    - Dashboard:        http://localhost:5000/")
    print("    - Pilots List:      http://localhost:5000/pilots")
    print("    - Reports:          http://localhost:5000/reports")
    print("    - API Pilots:       http://localhost:5000/api/pilots")
    print("    - API Assessments:  http://localhost:5000/api/assessments")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
