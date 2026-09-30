"""
Seed script to populate database with comprehensive demo data
"""

from app import app, db, Pilot, MedicalRecord, FlightLog, StaffFeedback
from app import SocialMediaPost, TrainingRecord, SubstanceTest, FinancialRecord
from app import PsychologicalEval, TravelRecord, PhoneRecord, EmailRecord
from app import BrowsingHistory, MessageRecord, DeviceRecord, LocationData
from datetime import datetime, timedelta
import json


def seed_comprehensive_data():
    """Seed database with comprehensive demo data"""
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create pilots
        pilots = [
            Pilot(
                pilot_id='PLT-001',
                first_name='James',
                last_name='Mitchell',
                date_of_birth=datetime(1985, 3, 15).date(),
                nationality='American',
                license_number='ATPL-US-2010-45678',
                license_type='ATPL',
                license_issue_date=datetime(2010, 6, 1).date(),
                license_expiry_date=datetime(2025, 6, 1).date(),
                medical_certificate_class='Class 1',
                medical_expiry=datetime(2025, 3, 15).date(),
                total_flight_hours=8500,
                aircraft_type_ratings=json.dumps(['B737', 'A320', 'B777']),
                airline='American Airlines',
                base_airport='DFW',
                years_experience=14,
                email='james.mitchell@email.com',
                phone='+1-555-0101',
                social_media_handles=json.dumps({'twitter': '@jamesm_pilot', 'instagram': 'jamesmitchell_fly'}),
            ),
            Pilot(
                pilot_id='PLT-002',
                first_name='Sarah',
                last_name='Chen',
                date_of_birth=datetime(1990, 7, 22).date(),
                nationality='Canadian',
                license_number='ATPL-CA-2015-78901',
                license_type='ATPL',
                license_issue_date=datetime(2015, 9, 1).date(),
                license_expiry_date=datetime(2025, 9, 1).date(),
                medical_certificate_class='Class 1',
                medical_expiry=datetime(2025, 7, 22).date(),
                total_flight_hours=5200,
                aircraft_type_ratings=json.dumps(['A320', 'A330', 'B787']),
                airline='Air Canada',
                base_airport='YYZ',
                years_experience=9,
                email='sarah.chen@email.com',
                phone='+1-555-0102',
                social_media_handles=json.dumps({'twitter': '@sarahchen_aviation', 'linkedin': 'sarah-chen-pilot'}),
            ),
            Pilot(
                pilot_id='PLT-003',
                first_name='Michael',
                last_name='Rodriguez',
                date_of_birth=datetime(1978, 11, 8).date(),
                nationality='British',
                license_number='ATPL-UK-2005-12345',
                license_type='ATPL',
                license_issue_date=datetime(2005, 1, 15).date(),
                license_expiry_date=datetime(2025, 1, 15).date(),
                medical_certificate_class='Class 1',
                medical_expiry=datetime(2025, 11, 8).date(),
                total_flight_hours=15000,
                aircraft_type_ratings=json.dumps(['B747', 'B777', 'A380', 'B787']),
                airline='British Airways',
                base_airport='LHR',
                years_experience=19,
                email='michael.rodriguez@email.com',
                phone='+44-555-0103',
                social_media_handles=json.dumps({'twitter': '@mrod_captain'}),
            ),
        ]
        
        for pilot in pilots:
            db.session.add(pilot)
        db.session.commit()
        
        # Add comprehensive data for each pilot
        for pilot in pilots:
            _add_medical_records(pilot)
            _add_flight_logs(pilot)
            _add_staff_feedback(pilot)
            _add_social_media_posts(pilot)
            _add_training_records(pilot)
            _add_substance_tests(pilot)
            _add_financial_records(pilot)
            _add_psychological_evals(pilot)
            _add_travel_records(pilot)
            _add_phone_records(pilot)
            _add_email_records(pilot)
            _add_browsing_history(pilot)
            _add_message_records(pilot)
            _add_device_records(pilot)
            _add_location_data(pilot)
        
        db.session.commit()
        print("Comprehensive demo data seeded successfully!")


def _add_medical_records(pilot):
    """Add medical records for pilot"""
    records = [
        MedicalRecord(
            pilot_id=pilot.id,
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
        ),
    ]
    for record in records:
        db.session.add(record)


def _add_flight_logs(pilot):
    """Add flight logs for pilot"""
    airports = ['LAX', 'JFK', 'ORD', 'MIA', 'SEA', 'DEN', 'ATL', 'SFO']
    for i in range(20):
        log = FlightLog(
            pilot_id=pilot.id,
            flight_date=(datetime(2024, 12, 1) - timedelta(days=i*2)).date(),
            aircraft_type=['B737', 'A320', 'B777'][i % 3],
            aircraft_registration=f'N{100+i}AA',
            departure_airport='DFW',
            arrival_airport=airports[i % len(airports)],
            flight_type='Domestic',
            flight_rules='IFR',
            flight_duration_minutes=120 + (i * 10),
            night_flight=(i % 3 == 0),
            instrument_time=60 + (i * 5),
            landings=1,
            incidents='None',
            weather_conditions='VMC' if i % 2 == 0 else 'IMC',
            crew_members='FO: Smith, FA: Johnson, FA: Brown',
            remarks='Routine flight',
        )
        db.session.add(log)


def _add_staff_feedback(pilot):
    """Add staff feedback for pilot"""
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
        fb = StaffFeedback(pilot_id=pilot.id, **fb_data)
        db.session.add(fb)


def _add_social_media_posts(pilot):
    """Add social media posts for pilot"""
    posts = [
        {'platform': 'Twitter', 'post_content': 'Another beautiful day in the skies! Loving my job as a pilot. #aviation #blessed', 'post_type': 'Text'},
        {'platform': 'Instagram', 'post_content': 'Sunset from 35,000 feet. Never gets old! #pilotlife #aviation #sunset', 'post_type': 'Image'},
        {'platform': 'Twitter', 'post_content': 'Important reminder: always prioritize safety over schedule. No flight is worth taking risks.', 'post_type': 'Text'},
        {'platform': 'LinkedIn', 'post_content': 'Completed my recurrent CRM training today. Always learning and improving! #aviation #safety', 'post_type': 'Text'},
    ]
    for post_data in posts:
        post = SocialMediaPost(
            pilot_id=pilot.id,
            platform=post_data['platform'],
            post_date=datetime(2024, 11, 15),
            post_content=post_data['post_content'],
            post_type=post_data['post_type'],
            sentiment_score=0.5,
            sentiment_label='Positive',
            flagged=False,
        )
        db.session.add(post)


def _add_training_records(pilot):
    """Add training records for pilot"""
    trainings = [
        {'training_type': 'B737 Type Rating', 'training_date': datetime(2020, 5, 10).date(), 'expiry_date': datetime(2025, 5, 10).date(), 'training_provider': 'American Airlines Training Center', 'instructor_name': 'Capt. Anderson', 'result': 'PASS', 'score': 95.0},
        {'training_type': 'CRM Recurrent', 'training_date': datetime(2024, 1, 15).date(), 'expiry_date': datetime(2025, 1, 15).date(), 'training_provider': 'American Airlines Training Center', 'instructor_name': 'Capt. Baker', 'result': 'PASS', 'score': 92.0},
        {'training_type': 'Upset Recovery', 'training_date': datetime(2024, 6, 20).date(), 'expiry_date': datetime(2025, 6, 20).date(), 'training_provider': 'American Airlines Training Center', 'instructor_name': 'Capt. Davis', 'result': 'PASS', 'score': 88.0},
    ]
    for t_data in trainings:
        tr = TrainingRecord(pilot_id=pilot.id, **t_data)
        db.session.add(tr)


def _add_substance_tests(pilot):
    """Add substance tests for pilot"""
    test = SubstanceTest(
        pilot_id=pilot.id,
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


def _add_financial_records(pilot):
    """Add financial records for pilot"""
    fin = FinancialRecord(
        pilot_id=pilot.id,
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


def _add_psychological_evals(pilot):
    """Add psychological evaluations for pilot"""
    psych = PsychologicalEval(
        pilot_id=pilot.id,
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


def _add_travel_records(pilot):
    """Add travel records for pilot"""
    travels = [
        {'departure_date': datetime(2024, 6, 15).date(), 'return_date': datetime(2024, 6, 22).date(), 'destination': 'Hawaii', 'purpose': 'Vacation', 'trip_type': 'Round-trip', 'companion': 'Family'},
        {'departure_date': datetime(2024, 3, 10).date(), 'return_date': datetime(2024, 3, 15).date(), 'destination': 'London', 'purpose': 'Training', 'trip_type': 'Round-trip', 'companion': 'Solo'},
    ]
    for t_data in travels:
        tr = TravelRecord(pilot_id=pilot.id, **t_data)
        db.session.add(tr)


def _add_phone_records(pilot):
    """Add phone records for pilot"""
    calls = [
        {'call_date': datetime(2024, 12, 1), 'call_time': datetime(2024, 12, 1, 10, 30), 'duration_seconds': 300, 'contact_name': 'Wife', 'contact_number': '+1-555-0201', 'contact_type': 'Family', 'call_direction': 'Outgoing'},
        {'call_date': datetime(2024, 12, 1), 'call_time': datetime(2024, 12, 1, 14, 0), 'duration_seconds': 120, 'contact_name': 'David Smith', 'contact_number': '+1-555-0202', 'contact_type': 'Colleague', 'is_known_associate': True, 'call_direction': 'Incoming'},
    ]
    for c_data in calls:
        cr = PhoneRecord(pilot_id=pilot.id, **c_data)
        db.session.add(cr)


def _add_email_records(pilot):
    """Add email records for pilot"""
    emails = [
        {'email_date': datetime(2024, 12, 1, 9, 0), 'sender': 'james.mitchell@email.com', 'recipient': 'training@aa.com', 'subject': 'CRM Recurrent Confirmation', 'body': 'Confirming my attendance for next week.', 'is_internal': True},
        {'email_date': datetime(2024, 12, 1, 11, 0), 'sender': 'james.mitchell@email.com', 'recipient': 'wife@email.com', 'subject': 'Flight Schedule', 'body': 'Sending you my schedule for next month.', 'is_internal': False},
    ]
    for e_data in emails:
        er = EmailRecord(pilot_id=pilot.id, **e_data)
        db.session.add(er)


def _add_browsing_history(pilot):
    """Add browsing history for pilot"""
    browsing = [
        {'access_time': datetime(2024, 12, 1, 8, 0), 'url': 'https://www.faa.gov/regulations', 'title': 'FAA Regulations', 'category': 'Work', 'is_work_related': True},
        {'access_time': datetime(2024, 12, 1, 12, 0), 'url': 'https://www.weather.com', 'title': 'Weather Forecast', 'category': 'Weather', 'is_work_related': True},
    ]
    for b_data in browsing:
        br = BrowsingHistory(pilot_id=pilot.id, **b_data)
        db.session.add(br)


def _add_message_records(pilot):
    """Add message records for pilot"""
    messages = [
        {'message_time': datetime(2024, 12, 1, 10, 0), 'sender': 'Wife', 'recipient': 'James', 'content': 'Have a safe flight today!', 'platform': 'SMS'},
        {'message_time': datetime(2024, 12, 1, 15, 0), 'sender': 'James', 'recipient': 'David Smith', 'content': 'See you at briefing tomorrow.', 'platform': 'WhatsApp'},
    ]
    for m_data in messages:
        mr = MessageRecord(pilot_id=pilot.id, **m_data)
        db.session.add(mr)


def _add_device_records(pilot):
    """Add device records for pilot"""
    devices = [
        {'device_id': 'DEV-001', 'device_type': 'iPhone', 'os_version': 'iOS 17.1', 'is_authorized': True},
        {'device_id': 'DEV-002', 'device_type': 'iPad', 'os_version': 'iPadOS 17.1', 'is_authorized': True},
    ]
    for d_data in devices:
        dr = DeviceRecord(pilot_id=pilot.id, **d_data)
        db.session.add(dr)


def _add_location_data(pilot):
    """Add location data for pilot"""
    locations = [
        {'timestamp': datetime(2024, 12, 1, 8, 0), 'location': 'DFW Airport', 'latitude': 32.8998, 'longitude': -97.0403, 'source': 'GPS'},
        {'timestamp': datetime(2024, 12, 1, 18, 0), 'location': 'Home', 'latitude': 32.7767, 'longitude': -96.7970, 'source': 'GPS'},
    ]
    for l_data in locations:
        lr = LocationData(pilot_id=pilot.id, **l_data)
        db.session.add(lr)


if __name__ == '__main__':
    seed_comprehensive_data()
