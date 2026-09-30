"""
Integration tests for Pilot Fitness Assessment AI Tool
"""

import unittest
import json
from app import app, db, Pilot, Assessment
from datetime import datetime


class TestApp(unittest.TestCase):
    """Test the main application"""
    
    def setUp(self):
        """Setup test environment"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Cleanup after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_index_page(self):
        """Test dashboard page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_pilots_page(self):
        """Test pilots list page loads"""
        response = self.client.get('/pilots')
        self.assertEqual(response.status_code, 200)
    
    def test_reports_page(self):
        """Test reports page loads"""
        response = self.client.get('/reports')
        self.assertEqual(response.status_code, 200)
    
    def test_api_pilots(self):
        """Test API endpoint for pilots list"""
        response = self.client.get('/api/pilots')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_api_assessments(self):
        """Test API endpoint for assessments list"""
        response = self.client.get('/api/assessments')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
    
    def test_add_pilot_page(self):
        """Test add pilot page loads"""
        response = self.client.get('/pilot/add')
        self.assertEqual(response.status_code, 200)
    
    def test_pilot_not_found(self):
        """Test pilot detail with invalid ID"""
        response = self.client.get('/pilot/9999')
        self.assertEqual(response.status_code, 404)


class TestPilotModel(unittest.TestCase):
    """Test Pilot model"""
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_pilot(self):
        """Test creating a pilot"""
        with app.app_context():
            pilot = Pilot(
                pilot_id='PLT-TEST-001',
                first_name='Test',
                last_name='Pilot',
                date_of_birth=datetime(1990, 1, 1).date(),
            )
            db.session.add(pilot)
            db.session.commit()
            
            self.assertIsNotNone(pilot.id)
            self.assertEqual(pilot.pilot_id, 'PLT-TEST-001')
            self.assertEqual(pilot.full_name, 'Test Pilot')
    
    def test_pilot_to_dict(self):
        """Test pilot serialization"""
        with app.app_context():
            pilot = Pilot(
                pilot_id='PLT-TEST-002',
                first_name='Jane',
                last_name='Doe',
                date_of_birth=datetime(1985, 5, 15).date(),
                nationality='American',
                total_flight_hours=5000,
            )
            db.session.add(pilot)
            db.session.commit()
            
            data = pilot.to_dict()
            self.assertEqual(data['pilot_id'], 'PLT-TEST-002')
            self.assertEqual(data['full_name'], 'Jane Doe')
            self.assertEqual(data['nationality'], 'American')


if __name__ == '__main__':
    unittest.main()
