from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///malnutrition_monitoring.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class ChildRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age_months = db.Column(db.Integer, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age_months': self.age_months,
            'weight_kg': self.weight_kg,
            'height_cm': self.height_cm,
            'status': self.status,
            'bmi': round(self.bmi, 2),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Functions
def calculate_bmi(weight_kg, height_cm):
    """Calculate BMI from weight and height"""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return bmi

def get_nutritional_status(age_months, bmi):
    """
    Determine nutritional status based on age and BMI
    Using WHO/CDC growth standards simplified version
    """
    if age_months < 24:
        # For children under 2 years, use weight-for-age categories
        if bmi < 13:
            return "Severely Underweight"
        elif bmi < 14.5:
            return "Underweight"
        elif bmi <= 16.5:
            return "Normal"
        else:
            return "Overweight"
    else:
        # For children 2+ years, use BMI categories
        if bmi < 14:
            return "Severely Underweight"
        elif bmi < 16:
            return "Underweight"
        elif bmi <= 21:
            return "Normal"
        elif bmi <= 24:
            return "Overweight"
        else:
            return "Obese"

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_record():
    """Add new child record"""
    if request.method == 'POST':
        data = request.get_json()
        
        name = data.get('name')
        age_months = int(data.get('age_months'))
        weight_kg = float(data.get('weight_kg'))
        height_cm = float(data.get('height_cm'))
        
        # Calculate BMI and status
        bmi = calculate_bmi(weight_kg, height_cm)
        status = get_nutritional_status(age_months, bmi)
        
        # Save to database
        record = ChildRecord(
            name=name,
            age_months=age_months,
            weight_kg=weight_kg,
            height_cm=height_cm,
            bmi=bmi,
            status=status
        )
        
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Record added successfully',
            'data': record.to_dict()
        })
    
    return render_template('add_record.html')

@app.route('/dashboard')
def dashboard():
    """View all records"""
    records = ChildRecord.query.all()
    
    # Calculate statistics
    total_records = len(records)
    status_count = {
        'Severely Underweight': 0,
        'Underweight': 0,
        'Normal': 0,
        'Overweight': 0,
        'Obese': 0
    }
    
    for record in records:
        if record.status in status_count:
            status_count[record.status] += 1
    
    return render_template('dashboard.html', 
                         records=records, 
                         total=total_records,
                         status_count=status_count)

@app.route('/api/records')
def get_records():
    """API to get all records as JSON"""
    records = ChildRecord.query.all()
    return jsonify([record.to_dict() for record in records])

@app.route('/api/record/<int:record_id>')
def get_record(record_id):
    """API to get specific record"""
    record = ChildRecord.query.get(record_id)
    if record:
        return jsonify(record.to_dict())
    return jsonify({'error': 'Record not found'}), 404

@app.route('/api/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete a record"""
    record = ChildRecord.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Record deleted'})
    return jsonify({'error': 'Record not found'}), 404

@app.route('/calculator')
def calculator():
    """Standalone BMI calculator"""
    return render_template('calculator.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
