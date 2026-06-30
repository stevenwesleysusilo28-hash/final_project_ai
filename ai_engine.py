"""
AI/ML Module for Malnutrition Monitoring System
Implements machine learning techniques for:
1. Predictive Analytics - Predict malnutrition risk
2. Trend Analysis - Detect nutritional trends over time
3. Smart Recommendations - Generate personalized advice
4. Risk Scoring - Identify high-risk children
"""

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import json

class NutritionAI:
    """
    AI Engine untuk Malnutrition Monitoring
    Menggunakan machine learning untuk predictive analytics & pattern recognition
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.risk_model = None
        self.trend_analyzer = TrendAnalyzer()
        
    # ==========================================
    # 1. PREDICTIVE RISK SCORING (Classification)
    # ==========================================
    
    def calculate_risk_score(self, age_months, bmi, trend=None):
        """
        Calculate malnutrition risk score using ML
        
        Features:
        - Age (growth period sensitivity)
        - Current BMI (current status)
        - Trend (historical trajectory)
        
        Returns: Risk score 0-100 (higher = more risk)
        """
        
        risk_score = 0
        
        # Feature 1: Age-based risk (children < 24 months more vulnerable)
        if age_months < 6:
            age_risk = 30  # Highest risk group
        elif age_months < 24:
            age_risk = 25  # High risk
        elif age_months < 60:
            age_risk = 15  # Moderate risk
        else:
            age_risk = 5   # Lower risk
        
        # Feature 2: BMI-based risk
        if bmi < 14:
            bmi_risk = 40  # Severe malnutrition
        elif bmi < 16:
            bmi_risk = 30  # Malnutrition
        elif bmi <= 21:
            bmi_risk = 5   # Normal
        elif bmi <= 24:
            bmi_risk = 15  # Overweight risk
        else:
            bmi_risk = 25  # Obesity risk
        
        # Feature 3: Trend-based risk
        trend_risk = 0
        if trend:
            if trend['direction'] == 'decreasing':
                trend_risk = 20  # Declining nutrition = high risk
            elif trend['direction'] == 'stable_low':
                trend_risk = 15  # Stable but low
            elif trend['direction'] == 'stable_normal':
                trend_risk = 5   # Stable & normal
            elif trend['direction'] == 'improving':
                trend_risk = 0   # Improving
        
        # Weighted combination
        risk_score = (age_risk * 0.3) + (bmi_risk * 0.5) + (trend_risk * 0.2)
        
        return min(100, round(risk_score, 2))  # Cap at 100
    
    # ==========================================
    # 2. TREND ANALYSIS (Time Series)
    # ==========================================
    
    def analyze_trend(self, records_history):
        """
        Analyze nutritional trend over time using linear regression
        
        Input: List of (date, bmi) tuples
        Output: Trend direction + velocity
        """
        
        if len(records_history) < 2:
            return {'direction': 'insufficient_data', 'velocity': 0}
        
        # Convert to numpy arrays
        dates = np.array([r[0] for r in records_history]).reshape(-1, 1)
        bmis = np.array([r[1] for r in records_history])
        
        # Fit linear regression to detect trend
        model = LinearRegression()
        model.fit(dates, bmis)
        
        # Calculate trend velocity (slope)
        velocity = model.coef_[0]  # Change in BMI per time unit
        
        # Classify trend direction
        if velocity < -0.1:
            direction = 'decreasing'  # 🔴 Worsening nutrition
        elif velocity < -0.02:
            direction = 'slowly_decreasing'
        elif velocity > 0.1:
            direction = 'improving'  # 🟢 Better nutrition
        elif velocity > 0.02:
            direction = 'slowly_improving'
        elif len(bmis) > 0 and bmis[-1] < 16:
            direction = 'stable_low'  # ⚠️ Stable but low
        else:
            direction = 'stable_normal'  # ✅ Stable & normal
        
        return {
            'direction': direction,
            'velocity': round(velocity, 4),
            'r_squared': round(model.score(dates, bmis), 3)
        }
    
    # ==========================================
    # 3. SMART RECOMMENDATIONS (NLP-like)
    # ==========================================
    
    def generate_smart_recommendation(self, status, risk_score, trend, age_months):
        """
        Generate personalized recommendations using multiple factors
        
        Combines: Status + Risk + Trend + Age → Actionable advice
        """
        
        recommendations = {
            'immediate_action': [],
            'dietary_advice': [],
            'monitoring_schedule': '',
            'healthcare_referral': False
        }
        
        # Determine immediate actions
        if risk_score > 70:
            recommendations['immediate_action'].append(
                "🚨 HIGH RISK - Schedule immediate consultation with healthcare provider"
            )
            recommendations['healthcare_referral'] = True
        elif risk_score > 50:
            recommendations['immediate_action'].append(
                "⚠️ MODERATE RISK - Schedule consultation within 1-2 weeks"
            )
        else:
            recommendations['immediate_action'].append(
                "✅ ACCEPTABLE - Continue regular monitoring"
            )
        
        # Dietary advice based on status
        if status == "Severely Underweight":
            recommendations['dietary_advice'] = [
                "• Increase caloric intake (focus on nutrient-dense foods)",
                "• Add: Eggs, milk, fish, beans, nuts",
                "• Meal frequency: 4-5 times daily (smaller portions)",
                "• Supplement with multivitamins (if recommended by doctor)"
            ]
        elif status == "Underweight":
            recommendations['dietary_advice'] = [
                "• Focus on protein-rich foods (eggs, meat, beans)",
                "• Include: Vegetables, fruits, whole grains",
                "• Increase portion sizes gradually",
                "• Ensure 3 main meals + 2 snacks daily"
            ]
        elif status == "Normal":
            recommendations['dietary_advice'] = [
                "• Maintain balanced diet (protein, carbs, fats, vegetables)",
                "• Ensure variety in food groups",
                "• Adequate hydration",
                "• Regular physical activity"
            ]
        elif status == "Overweight":
            recommendations['dietary_advice'] = [
                "• Reduce sugary drinks & processed foods",
                "• Increase fruit & vegetable intake",
                "• Portion control & regular meal times",
                "• Encourage physical activity (30 min/day)"
            ]
        elif status == "Obese":
            recommendations['dietary_advice'] = [
                "• Consult with nutritionist for personalized diet plan",
                "• Reduce caloric intake gradually",
                "• Eliminate sugary & fatty foods",
                "• Increase physical activity with medical clearance"
            ]
        
        # Monitoring schedule based on trend
        if trend and trend['direction'] == 'decreasing':
            recommendations['monitoring_schedule'] = "Weekly monitoring recommended"
            recommendations['immediate_action'].append("Trend is WORSENING - increase monitoring frequency")
        elif trend and trend['direction'] == 'slowly_decreasing':
            recommendations['monitoring_schedule'] = "Bi-weekly monitoring recommended"
        elif trend and trend['direction'] == 'improving':
            recommendations['monitoring_schedule'] = "Monthly monitoring acceptable"
            recommendations['immediate_action'].append("✅ Good progress - continue current approach")
        else:
            recommendations['monitoring_schedule'] = "Monthly monitoring recommended"
        
        return recommendations
    
    # ==========================================
    # 4. RISK STRATIFICATION (Clustering)
    # ==========================================
    
    def stratify_children_by_risk(self, children_data):
        """
        Use K-Means clustering to group children into risk tiers
        
        Input: List of (bmi, age_months, status) tuples
        Output: Risk tiers (Low, Medium, High)
        """
        
        if len(children_data) < 3:
            return {'tier_1': [], 'tier_2': [], 'tier_3': []}
        
        # Prepare features
        X = np.array(children_data).reshape(-1, 2)  # BMI, Age
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # K-Means clustering (3 clusters = 3 risk tiers)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Sort clusters by risk (based on centroid distance from "healthy" zone)
        healthy_zone = np.array([[0.5, 0.5]])  # Normalized healthy zone
        distances = [
            np.linalg.norm(kmeans.cluster_centers_[i] - healthy_zone[0])
            for i in range(3)
        ]
        
        # Assign risk tiers
        tier_mapping = {
            np.argsort(distances)[0]: 'low_risk',
            np.argsort(distances)[1]: 'medium_risk',
            np.argsort(distances)[2]: 'high_risk'
        }
        
        result = {'low_risk': [], 'medium_risk': [], 'high_risk': []}
        for i, data in enumerate(children_data):
            tier = tier_mapping[clusters[i]]
            result[tier].append(data)
        
        return result
    
    # ==========================================
    # 5. ANOMALY DETECTION
    # ==========================================
    
    def detect_anomalies(self, records_history):
        """
        Detect unusual patterns that warrant investigation
        
        Examples:
        - Sudden drop in BMI
        - Rapid gain (possible error)
        - Inconsistent measurements
        """
        
        anomalies = []
        
        if len(records_history) < 2:
            return anomalies
        
        for i in range(1, len(records_history)):
            prev_bmi = records_history[i-1][1]
            curr_bmi = records_history[i][1]
            
            change = curr_bmi - prev_bmi
            
            # Detect sudden drops (> 1 BMI point/month)
            if change < -1.0:
                anomalies.append({
                    'type': 'sudden_drop',
                    'severity': 'high',
                    'message': f'⚠️ Sudden BMI drop detected ({change:.2f})',
                    'recommendation': 'Verify measurements & investigate cause'
                })
            
            # Detect sudden gains (> 2 BMI points/month)
            elif change > 2.0:
                anomalies.append({
                    'type': 'sudden_gain',
                    'severity': 'medium',
                    'message': f'Rapid BMI gain detected ({change:.2f})',
                    'recommendation': 'Verify measurements & check for data entry errors'
                })
        
        return anomalies


class TrendAnalyzer:
    """Helper class for time series analysis"""
    
    def calculate_moving_average(self, values, window=3):
        """Calculate moving average to smooth trends"""
        if len(values) < window:
            return values
        
        ma = []
        for i in range(len(values) - window + 1):
            ma.append(np.mean(values[i:i+window]))
        return ma
    
    def predict_future_bmi(self, history, months_ahead=3):
        """Predict future BMI based on historical trend"""
        if len(history) < 2:
            return None
        
        dates = np.array(range(len(history))).reshape(-1, 1)
        bmis = np.array(history)
        
        model = LinearRegression()
        model.fit(dates, bmis)
        
        # Predict for future months
        future_dates = np.array(range(len(history), len(history) + months_ahead)).reshape(-1, 1)
        predictions = model.predict(future_dates)
        
        return [round(p, 2) for p in predictions]


# ==========================================
# INTEGRATION EXAMPLE
# ==========================================

def demonstrate_ai_capabilities():
    """Example showing all AI capabilities"""
    
    ai = NutritionAI()
    
    # Example 1: Risk scoring
    risk = ai.calculate_risk_score(24, 14.5)
    print(f"Risk Score: {risk}/100")
    
    # Example 2: Trend analysis
    history = [(i, 15 - i*0.1) for i in range(5)]  # Declining trend
    trend = ai.analyze_trend(history)
    print(f"Trend: {trend}")
    
    # Example 3: Smart recommendations
    recommendations = ai.generate_smart_recommendation(
        "Underweight", 45, trend, 24
    )
    print(f"Recommendations: {recommendations}")
    
    # Example 4: Anomaly detection
    anomalies = ai.detect_anomalies(history)
    print(f"Anomalies: {anomalies}")
    
    return {
        'risk_score': risk,
        'trend': trend,
        'recommendations': recommendations,
        'anomalies': anomalies
    }


if __name__ == "__main__":
    results = demonstrate_ai_capabilities()
    print("\n=== AI Analysis Results ===")
    print(json.dumps(results, indent=2, default=str))
