# Pilot Fitness Assessment AI Tool

A comprehensive AI-powered system for evaluating pilot fitness for duty across 15 assessment modules.

## Features

### 15 Assessment Modules

1. **Medical Fitness** - Vision, hearing, cardiovascular, respiratory, musculoskeletal, neurological health
2. **Psychological Evaluation** - MMPI-2, Big Five personality, emotional stability, cognitive function
3. **Social Media Analysis** - Sentiment analysis, risk indicators, behavior patterns
4. **Socio-Political-Economic** - Political extremism, economic stress, social risk factors
5. **Staff Feedback** - Crew feedback, behavioral flags, peer assessments
6. **Flight History** - Flight logs, incidents, currency, performance trends
7. **Substance Abuse Screening** - Drug/alcohol tests, screening results, patterns
8. **Financial Stability** - Credit score, debt, bankruptcy, gambling concerns
9. **Background Check** - Incident reports, criminal history, security clearance
10. **Fatigue & Lifestyle** - Sleep disorders, lifestyle factors, fitness indicators
11. **Training & Certification** - License validity, training currency, type ratings
12. **Travel History** - Destinations, high-risk areas, unusual patterns
13. **Behavior Pattern Change** - Change detection, trend analysis, sudden shifts
14. **Digital Footprint** - Phone records, email, browsing history, messages, devices, location data
15. **Radicalization Detection** - Extremist content, ideology indicators, risk assessment

## Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd PilotFitnessAI
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open browser and navigate to:
```
http://localhost:5000
```

## Docker Deployment

```bash
docker build -t pilot-fitness-ai .
docker run -p 5000:5000 pilot-fitness-ai
```

Or use docker-compose:
```bash
docker-compose up -d
```

## API Endpoints

- `GET /api/pilots` - List all pilots
- `GET /api/pilot/<id>` - Get pilot details
- `POST /api/assess/<id>` - Run assessment
- `GET /api/assessments` - List all assessments

## Usage

1. **Add Pilot**: Click "Add Pilot" and fill in pilot information
2. **Add Data**: Add medical records, flight logs, staff feedback, social media posts, etc.
3. **Run Assessment**: Click "Assess" on pilot detail page
4. **View Report**: View comprehensive assessment report with all module scores

## Security Notice

This tool is intended for authorized aviation safety personnel only. All data should be handled in accordance with applicable privacy regulations and company policies.

## License

Proprietary - For authorized use only.
