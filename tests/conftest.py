"""
Pytest configuration and fixtures
"""

import pytest
from app import app, db, Pilot
from datetime import datetime


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture
def sample_pilot():
    """Create a sample pilot for testing"""
    with app.app_context():
        pilot = Pilot(
            pilot_id='PLT-TEST-001',
            first_name='Test',
            last_name='Pilot',
            date_of_birth=datetime(1990, 1, 1).date(),
            nationality='American',
            license_number='ATPL-TEST-001',
            license_type='ATPL',
            total_flight_hours=5000,
            airline='Test Air',
            years_experience=10,
        )
        db.session.add(pilot)
        db.session.commit()
        return pilot
