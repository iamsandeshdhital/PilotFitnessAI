"""
Entry point for Pilot Fitness Assessment AI Tool
"""

from app import app, db, create_sample_data

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
    
    print("\n" + "="*60)
    print("  PILOT FITNESS ASSESSMENT AI TOOL")
    print("="*60)
    print("\n  Starting server at http://localhost:5000")
    print("\n  Press CTRL+C to stop")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
