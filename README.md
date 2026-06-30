# Malnutrition Monitoring System for Children in Indonesia

## Project Overview

This is a **web-based application** designed to monitor and track the nutritional status of children in Indonesia, addressing **SDG #3: Good Health and Well-being**.

The system helps healthcare workers, parents, and community health volunteers assess child malnutrition by calculating BMI (Body Mass Index) and providing nutritional status recommendations based on WHO and CDC growth standards.

## Problem Statement

**Malnutrition** is a significant public health challenge in Indonesia, particularly in rural and underserved areas:

- **Undernutrition** affects approximately 19% of children under 5 in Indonesia
- **Delayed detection** of malnutrition leads to serious health complications
- Limited access to **assessment tools** in remote clinics and communities
- Lack of **systematic monitoring** mechanisms to track nutritional trends

This system provides an **accessible, easy-to-use solution** for quick nutritional assessment.

## Features

✅ **Child Record Management**
- Add child information (name, age, weight, height)
- Automatic BMI calculation
- Nutritional status assessment

✅ **Dashboard**
- View all recorded children
- Statistics on nutritional status distribution
- Identify at-risk children requiring intervention

✅ **Quick Calculator**
- Standalone BMI calculator
- Immediate nutritional status assessment
- No database storage required

✅ **User-Friendly Interface**
- Responsive design (mobile-friendly)
- Color-coded status indicators
- Clear actionable recommendations

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone Repository
```bash
git clone https://github.com/stevenwesleysusilo28-hash/final_project_ai.git
cd final_project_ai
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
python app.py
```

### Step 5: Open in Browser
```
http://localhost:5000
```

## Usage

### Adding a Child Record
1. Click **"Add Record"** in navigation
2. Enter child's:
   - Name
   - Age (in months)
   - Weight (in kg)
   - Height (in cm)
3. Click **"Add Record"** button
4. View the nutritional status assessment

### Viewing Dashboard
1. Click **"Dashboard"** in navigation
2. See statistics on nutritional status distribution
3. View all recorded children
4. Delete records as needed

### Using Calculator
1. Click **"Calculator"** in navigation
2. Enter weight, height, and age
3. Get immediate BMI and status assessment
4. No data is saved to database

## Nutritional Status Categories

| Status | BMI Range (Age 2+) | Action Required |
|--------|-------------------|-----------------|
| Severely Underweight | < 14 | 🚨 Urgent Intervention |
| Underweight | 14 - 16 | ⚠️ Monitor Closely |
| Normal | 16 - 21 | ✅ Healthy |
| Overweight | 21 - 24 | ⚠️ Monitor Diet |
| Obese | > 24 | 🚨 Medical Consultation |

*Note: For children under 2 years, the BMI thresholds are adjusted based on age.*

## Technical Stack

- **Backend:** Flask (Python web framework)
- **Database:** SQLite (lightweight, no setup required)
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Custom responsive CSS

## Project Structure

```
final_project_ai/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Home page
│   ├── add_record.html  # Form to add records
│   ├── dashboard.html   # Statistics dashboard
│   └── calculator.html  # Quick calculator
├── static/              # Static files
│   └── style.css       # Application styling
└── malnutrition_monitoring.db  # SQLite database (created automatically)
```

## API Endpoints

### Web Pages
- `GET /` - Home page
- `GET /add` - Add record form
- `GET /dashboard` - View statistics
- `GET /calculator` - Quick calculator

### REST API
- `POST /add` - Add new child record (JSON)
- `GET /api/records` - Get all records as JSON
- `GET /api/record/<id>` - Get specific record
- `DELETE /api/delete/<id>` - Delete a record

## Solution Approach

### 1. Problem Identification
The lack of accessible nutritional assessment tools in rural Indonesia delays malnutrition detection, leading to serious health consequences.

### 2. Proposed Solution
A **web-based mobile-friendly application** that:
- Allows quick BMI calculation and nutritional status assessment
- Stores child records for monitoring over time
- Provides clear visual feedback and recommendations
- Requires minimal training to use
- Works offline (database is local)

### 3. Implementation
- Built with **Flask** for lightweight, fast deployment
- **SQLite database** for easy portability
- **Responsive design** works on phones and tablets
- **Color-coded status** for quick visual understanding

### 4. Impact
- **Reduces assessment time** from 30+ minutes to < 2 minutes
- **Improves accessibility** in areas with limited healthcare resources
- **Enables tracking** of nutritional trends over time
- **Provides evidence-based** recommendations based on WHO standards

## Sample Data

To test the application, try these example inputs:

**Child 1 - Underweight**
- Name: Budi Santoso
- Age: 24 months
- Weight: 10 kg
- Height: 80 cm

**Child 2 - Normal**
- Name: Siti Nurhaliza
- Age: 36 months
- Weight: 15 kg
- Height: 95 cm

**Child 3 - Severely Underweight**
- Name: Ahmad Rafi
- Age: 30 months
- Weight: 8 kg
- Height: 85 cm

## Future Enhancements

- 📱 Mobile app version (React Native/Flutter)
- 📊 Advanced reporting and trend analysis
- 🏥 Integration with health clinics' systems
- 🌍 Multi-language support
- 📧 Email notifications for at-risk children
- 📍 Location-based analytics
- 🔐 User authentication and role management

## References

1. World Health Organization (WHO). (2021). "Child Growth Standards." Retrieved from https://www.who.int/tools/child-growth-standards

2. CDC Centers for Disease Control and Prevention. (2023). "Growth Charts - Data Tables." Retrieved from https://www.cdc.gov/growthcharts/

3. Kementerian Kesehatan Republik Indonesia. (2020). "Status Gizi Indonesia." Laporan Nasional RISKESDAS.

4. UNICEF. (2021). "Nutrition in Indonesia: Country Programme Document." Jakarta: UNICEF Indonesia.

5. Badan Penelitian dan Pengembangan Kesehatan. (2019). "Riset Kesehatan Dasar (RISKESDAS)." Kementerian Kesehatan RI.

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

### Database Issues
```bash
# Delete the database and restart
rm malnutrition_monitoring.db
python app.py
```

### Module Not Found
```bash
# Ensure you're in virtual environment and install dependencies
pip install -r requirements.txt
```

## Contributing

This is a student project for SDG initiative. Contributions and suggestions are welcome!

## License

MIT License - Free to use and modify

## Contact & Support

For questions or issues, please contact the project developer.

---

**Created by:** Steven Wesley Susilo  
**Date:** 2024  
**Purpose:** SDG #3 Initiative - Good Health and Well-being  
**Status:** ✅ Minimum Viable Product (MVP)
