# ============================================
# 🩸 BLOODAI ENHANCED PROFESSIONAL SYSTEM v9.7
# COMPLETE SYSTEM WITH FIXED EMAIL DELIVERY - ALL ERRORS RESOLVED
# ============================================

import streamlit as st
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import bcrypt
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import time
import threading
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import hashlib
import atexit
from contextlib import contextmanager
import qrcode
from io import BytesIO
import base64
import json
import uuid
import secrets
import re
import warnings
warnings.filterwarnings('ignore')

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="BloodAI - Complete Blood Donation System",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ENHANCED CUSTOM CSS
# ============================================

st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes glow-pulse {
        0% { box-shadow: 0 0 5px #ff4b4b; }
        50% { box-shadow: 0 0 20px #ff4b4b, 0 0 30px #ff6b6b; }
        100% { box-shadow: 0 0 5px #ff4b4b; }
    }
    
    .emergency-glow {
        animation: glow-pulse 1.5s infinite;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s, box-shadow 0.3s;
        cursor: pointer;
    }
    
    .metric-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card:nth-child(2) {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .metric-card:nth-child(3) {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .metric-card:nth-child(4) {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
        animation: countUp 1s ease-out;
    }
    
    @keyframes countUp {
        from { transform: scale(0.5); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    /* Inventory cards */
    .inventory-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        transition: transform 0.3s;
        margin: 0.5rem;
    }
    
    .inventory-card.critical {
        background: linear-gradient(135deg, #ff6b6b, #ee5253);
    }
    
    .inventory-card.low {
        background: linear-gradient(135deg, #feca57, #ff9f43);
    }
    
    .inventory-card:hover {
        transform: translateY(-5px) scale(1.05);
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s;
        height: 100%;
        border: 1px solid #e0e0e0;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.3);
        border-color: #667eea;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Emergency banner */
    .emergency-banner {
        background: linear-gradient(90deg, #ff6b6b, #ee5253);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        margin: 1rem 0;
        animation: pulse 2s infinite;
        cursor: pointer;
        transition: transform 0.3s;
    }
    
    .emergency-banner:hover {
        transform: scale(1.02);
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.9; transform: scale(1.02); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Event card */
    .event-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: all 0.3s;
    }
    
    .event-card:hover {
        transform: translateX(10px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* QR code container */
    .qr-code-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Reward card */
    .reward-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .reward-card:hover {
        transform: scale(1.05) rotate(2deg);
        box-shadow: 0 15px 30px rgba(67, 233, 123, 0.4);
    }
    
    /* Chat bubble */
    .chat-bubble {
        padding: 1rem;
        border-radius: 20px;
        margin: 0.5rem 0;
        max-width: 70%;
    }
    
    .chat-bubble.sent {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        margin-left: auto;
    }
    
    .chat-bubble.received {
        background: #f0f0f0;
        color: black;
        margin-right: auto;
    }
    
    /* Blood badge */
    .blood-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #ff6b6b, #ee5253);
        color: white;
        border-radius: 50px;
        font-weight: bold;
        margin: 0.25rem;
        font-size: 0.9rem;
        transition: all 0.3s;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(238, 82, 83, 0.3);
    }
    
    .blood-badge:hover {
        transform: scale(1.1) rotate(2deg);
        box-shadow: 0 5px 15px rgba(238, 82, 83, 0.5);
    }
    
    /* Success message */
    .success-message {
        animation: successPop 0.5s ease-out;
        background: linear-gradient(135deg, #43e97b, #38f9d7);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 1.5rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(67, 233, 123, 0.4);
    }
    
    @keyframes successPop {
        0% { transform: scale(0); opacity: 0; }
        80% { transform: scale(1.1); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Testimonial card */
    .testimonial-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        transition: all 0.3s;
    }
    
    .testimonial-card:hover {
        transform: translateX(10px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    /* Donor card */
    .donor-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
    }
    
    .donor-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    /* Email preview */
    .email-preview {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        font-family: monospace;
    }
    
    /* Countdown timer */
    .countdown-timer {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #ff6b6b;
        animation: pulse 1s infinite;
    }
    
    /* Distance badge */
    .distance-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    /* Location priority indicator */
    .location-priority {
        background: linear-gradient(135deg, #43e97b20, #38f9d720);
        border: 2px solid #43e97b;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CONFIGURATION
# ============================================

# Email Configuration - CORRECTED
FROM_EMAIL = "vigneshsapavat11@gmail.com"  # This is CORRECT (with 'e')
APP_PASSWORD = "kmcfregjdseaihwn"  # Your Gmail App Password
BASE_URL = "http://localhost:8501"

# System Settings
WAIT_MINUTES = 2
COOLDOWN_MONTHS = 3
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# Blood Types
BLOOD_TYPES = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']

# Blood Inventory Settings
BLOOD_STOCK_ALERT_THRESHOLD = 5
BLOOD_EXPIRY_DAYS = 42

# Reward Points System
POINTS_PER_DONATION = 100

# Location Settings - NO DISTANCE LIMIT
UNLIMITED_DISTANCE = True

# Initialize session state
if 'db_initialized' not in st.session_state:
    st.session_state.db_initialized = False
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'logged_in_donor' not in st.session_state:
    st.session_state.logged_in_donor = None
if 'scheduler_started' not in st.session_state:
    st.session_state.scheduler_started = False
if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = None
if 'email_log' not in st.session_state:
    st.session_state.email_log = []
if 'donor_search_progress' not in st.session_state:
    st.session_state.donor_search_progress = 0
if 'showing_response' not in st.session_state:
    st.session_state.showing_response = False

# ============================================
# EMAIL VALIDATION FUNCTION
# ============================================

def is_valid_email(email):
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def normalize_email(email):
    """Normalize email address to prevent common typos"""
    if not email:
        return email
    # Convert to lowercase
    email = email.lower().strip()
    # Fix common typos in your email domain
    if email.endswith('@gmal.com'):
        email = email.replace('@gmal.com', '@gmail.com')
    if email.endswith('@gmai.com'):
        email = email.replace('@gmai.com', '@gmail.com')
    if email.endswith('@gamil.com'):
        email = email.replace('@gamil.com', '@gmail.com')
    return email

# ============================================
# DATABASE CONNECTION MANAGER
# ============================================

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect("bloodai_final.db", timeout=30)
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        if conn:
            conn.close()

def execute_query(query, params=(), fetch_one=False, fetch_all=False, commit=False):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if commit:
                conn.commit()
                return cursor.lastrowid
            
            if fetch_one:
                result = cursor.fetchone()
                return dict(result) if result else None
            
            if fetch_all:
                results = cursor.fetchall()
                return [dict(row) for row in results]
            
            return cursor.lastrowid
    except Exception as e:
        print(f"Database error: {e}")
        return None if fetch_one or fetch_all else -1

# ============================================
# COMPLETE DATABASE SETUP
# ============================================

def init_database():
    """Initialize complete database with all tables"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Donors table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS donors(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                donor_id TEXT UNIQUE,
                name TEXT,
                email TEXT UNIQUE,
                phone TEXT,
                blood TEXT,
                location TEXT,
                latitude REAL,
                longitude REAL,
                password BLOB,
                status TEXT DEFAULT 'Available',
                registration_date TEXT,
                total_donations INTEGER DEFAULT 0,
                last_donation_date TEXT,
                health_conditions TEXT,
                weight REAL,
                age INTEGER,
                gender TEXT,
                points INTEGER DEFAULT 0,
                donor_level TEXT DEFAULT 'New Donor 🌟',
                emergency_contact TEXT,
                medical_id TEXT,
                is_verified INTEGER DEFAULT 0,
                last_location_update TEXT
            )
            """)
            
            # Requests table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT UNIQUE,
                patient TEXT,
                patient_email TEXT,
                patient_phone TEXT,
                blood TEXT,
                location TEXT,
                latitude REAL,
                longitude REAL,
                hospital TEXT,
                hospital_contact TEXT,
                status TEXT DEFAULT 'Pending',
                donor_id INTEGER,
                time TEXT,
                contacted TEXT DEFAULT '',
                last_contacted_time TEXT,
                units_needed INTEGER DEFAULT 1,
                completed_time TEXT,
                closest_donor_distance REAL
            )
            """)
            
            # Donation History
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS donation_history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                history_id TEXT UNIQUE,
                donor_id INTEGER,
                request_id INTEGER,
                donation_date TEXT,
                hospital TEXT,
                blood_type TEXT,
                units INTEGER DEFAULT 1,
                points_earned INTEGER DEFAULT 0,
                donor_distance_km REAL,
                FOREIGN KEY (donor_id) REFERENCES donors (id),
                FOREIGN KEY (request_id) REFERENCES requests (id)
            )
            """)
            
            # Notifications Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notification_id TEXT UNIQUE,
                user_email TEXT,
                type TEXT,
                title TEXT,
                message TEXT,
                date TEXT,
                read INTEGER DEFAULT 0
            )
            """)
            
            # Email Log Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_log(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id TEXT UNIQUE,
                recipient TEXT,
                subject TEXT,
                type TEXT,
                sent_date TEXT,
                status TEXT,
                error_message TEXT,
                request_id TEXT,
                donor_id INTEGER
            )
            """)
            
            # Blood Inventory Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS blood_inventory(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                blood_type TEXT,
                units INTEGER DEFAULT 0,
                expiry_date TEXT,
                status TEXT DEFAULT 'Available'
            )
            """)
            
            conn.commit()
            print("✅ Database initialized successfully")
            
    except Exception as e:
        print(f"Database initialization error: {e}")

# Initialize database
if not st.session_state.db_initialized:
    init_database()
    st.session_state.db_initialized = True

# ============================================
# UTILITY FUNCTIONS
# ============================================

def generate_id(prefix):
    """Generate unique ID"""
    return f"{prefix}-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

def get_coords(location):
    """Get coordinates from location"""
    try:
        if not location or not isinstance(location, str):
            return None
        geolocator = Nominatim(user_agent="bloodai_app")
        loc = geolocator.geocode(location)
        if loc:
            return (loc.latitude, loc.longitude)
        return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

def update_donor_coordinates(donor_id, location):
    """Update donor coordinates in database"""
    coords = get_coords(location)
    if coords:
        lat, lon = coords
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        execute_query(
            "UPDATE donors SET latitude=?, longitude=?, last_location_update=?, is_verified=1 WHERE id=?",
            (lat, lon, current_time, donor_id),
            commit=True
        )
        return True
    return False

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def log_email(recipient, subject, email_type, status, error=None, request_id=None, donor_id=None):
    """Log email sending attempt"""
    try:
        email_id = generate_id('EMAIL')
        execute_query(
            """INSERT INTO email_log 
               (email_id, recipient, subject, type, sent_date, status, error_message, request_id, donor_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (email_id, recipient, subject, email_type, 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             status, error, request_id, donor_id),
            commit=True
        )
        st.session_state.email_log.append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'to': recipient,
            'subject': subject,
            'status': status
        })
    except Exception as e:
        print(f"Email log error: {e}")

def send_email(to_email, subject, message, html=False):
    """Send email with logging and validation"""
    try:
        # Normalize and validate email
        to_email = normalize_email(to_email)
        
        if not is_valid_email(to_email):
            error_msg = f"Invalid email format: {to_email}"
            log_email(to_email, subject, 'email', 'failed', error_msg)
            print(f"❌ {error_msg}")
            return False
        
        # Create message
        msg = MIMEMultipart() if html else MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        
        if html:
            html_part = MIMEText(message, 'html')
            msg.attach(html_part)
        else:
            text_part = MIMEText(message, 'plain')
            msg.attach(text_part)
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        log_email(to_email, subject, 'email', 'sent')
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except smtplib.SMTPRecipientsRefused:
        error_msg = f"Recipient email address rejected: {to_email}"
        log_email(to_email, subject, 'email', 'failed', error_msg)
        print(f"❌ {error_msg}")
        return False
        
    except smtplib.SMTPAuthenticationError:
        error_msg = "Email authentication failed. Check your Gmail App Password."
        log_email(to_email, subject, 'email', 'failed', error_msg)
        print(f"❌ {error_msg}")
        st.error("⚠️ Email configuration error. Please check your Gmail App Password.")
        return False
        
    except Exception as e:
        error_msg = str(e)
        log_email(to_email, subject, 'email', 'failed', error_msg)
        print(f"❌ Email error: {error_msg}")
        return False

def add_notification(user_email, notif_type, title, message):
    """Add notification"""
    try:
        if not user_email or not is_valid_email(user_email):
            return False
        
        notification_id = generate_id('NOTIF')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        execute_query(
            """INSERT INTO notifications 
               (notification_id, user_email, type, title, message, date, read)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (notification_id, user_email, notif_type, title, message, current_time, 0),
            commit=True
        )
        return True
    except Exception as e:
        print(f"Notification error: {e}")
        return False

def get_unread_notifications(user_email):
    """Get unread notifications"""
    try:
        if not user_email or not is_valid_email(user_email):
            return []
        return execute_query(
            "SELECT * FROM notifications WHERE user_email=? AND read=0 ORDER BY date DESC",
            (user_email,),
            fetch_all=True
        ) or []
    except:
        return []

def mark_notifications_read(user_email):
    """Mark all notifications as read"""
    try:
        if not user_email or not is_valid_email(user_email):
            return False
        execute_query(
            "UPDATE notifications SET read=1 WHERE user_email=?",
            (user_email,),
            commit=True
        )
        return True
    except:
        return False

# ============================================
# DONOR ELIGIBILITY CHECK
# ============================================

def is_donor_eligible(donor):
    """Check if donor is eligible to donate"""
    try:
        if not donor:
            return False, "Invalid donor"
        
        last_donation = donor.get('last_donation_date')
        if not last_donation:
            return True, "Eligible (First-time donor)"
        
        try:
            last_date = datetime.strptime(last_donation, "%Y-%m-%d %H:%M:%S")
            current_date = datetime.now()
            months_diff = (current_date.year - last_date.year) * 12 + current_date.month - last_date.month
            
            if months_diff >= COOLDOWN_MONTHS:
                return True, f"Eligible (Last: {last_date.strftime('%Y-%m-%d')})"
            else:
                next_eligible = last_date + timedelta(days=COOLDOWN_MONTHS * 30)
                days = (next_eligible - current_date).days
                return False, f"On cooldown ({days} days left)"
        except:
            return True, "Eligible"
    except Exception as e:
        print(f"Eligibility error: {e}")
        return True, "Eligible"

def get_eligible_donors(blood_type):
    """Get all eligible donors for a blood type"""
    try:
        donors = execute_query(
            "SELECT * FROM donors WHERE blood=? AND status='Available'",
            (blood_type,),
            fetch_all=True
        ) or []
        
        eligible = []
        for donor in donors:
            if donor:
                eligible_flag, _ = is_donor_eligible(donor)
                if eligible_flag:
                    eligible.append(donor)
        return eligible
    except Exception as e:
        print(f"Error getting eligible donors: {e}")
        return []

# ============================================
# DONOR LEVEL CALCULATION
# ============================================

def calculate_donor_level(donations):
    """Calculate donor level based on donation count"""
    if donations >= 20:
        return "Platinum 🏆"
    elif donations >= 10:
        return "Gold 🥇"
    elif donations >= 5:
        return "Silver 🥈"
    elif donations >= 1:
        return "Bronze 🥉"
    else:
        return "New Donor 🌟"

def update_donor_points(donor_id):
    """Update donor points and level after donation"""
    try:
        result = execute_query(
            "SELECT COUNT(*) as count FROM donation_history WHERE donor_id=? AND status='Completed'",
            (donor_id,),
            fetch_one=True
        )
        donations = result['count'] if result else 0
        
        points = donations * 10
        level = calculate_donor_level(donations)
        
        execute_query(
            "UPDATE donors SET points=?, donor_level=? WHERE id=?",
            (points, level, donor_id),
            commit=True
        )
        
        return points, level
    except Exception as e:
        print(f"Error updating points: {e}")
        return 0, "New Donor 🌟"

# ============================================
# FIND NEXT DONOR FUNCTION - UNLIMITED DISTANCE
# ============================================

def find_next_donor(blood_type, location, contacted_ids):
    """
    Find the next best eligible donor based on location proximity
    UNLIMITED DISTANCE - nearest donor always contacted first
    """
    try:
        eligible_donors = get_eligible_donors(blood_type)
        if not eligible_donors:
            print(f"No eligible donors found")
            return None, None
        
        contacted_list = []
        if contacted_ids:
            contacted_list = [int(x) for x in contacted_ids.split(',') if x and x.strip()]
        
        available = [d for d in eligible_donors if d and d.get('id') not in contacted_list]
        if not available:
            print(f"All donors have been contacted already")
            return None, None
        
        print(f"Found {len(available)} available donors")
        
        patient_coords = get_coords(location)
        
        if not patient_coords:
            print("Could not get patient coordinates")
            return available[0] if available else None, None
        
        patient_lat, patient_lon = patient_coords
        
        donors_with_distance = []
        
        for donor in available:
            if not donor:
                continue
                
            donor_lat = donor.get('latitude')
            donor_lon = donor.get('longitude')
            
            if not donor_lat or not donor_lon:
                donor_coords = get_coords(donor.get('location', ''))
                if donor_coords:
                    donor_lat, donor_lon = donor_coords
                    execute_query(
                        "UPDATE donors SET latitude=?, longitude=?, is_verified=1 WHERE id=?",
                        (donor_lat, donor_lon, donor.get('id')),
                        commit=True
                    )
            
            if donor_lat and donor_lon:
                try:
                    donor_coords = (donor_lat, donor_lon)
                    distance = geodesic(patient_coords, donor_coords).km
                    
                    donors_with_distance.append({
                        'donor': donor,
                        'distance': distance,
                        'verified': donor.get('is_verified', 0)
                    })
                        
                except Exception as e:
                    print(f"Distance calculation error")
            else:
                donors_with_distance.append({
                    'donor': donor,
                    'distance': float('inf'),
                    'verified': 0
                })
        
        donors_with_distance.sort(key=lambda x: x['distance'])
        
        if not donors_with_distance:
            return None, None
        
        closest = donors_with_distance[0]
        return closest['donor'], donors_with_distance
        
    except Exception as e:
        print(f"Error in find_next_donor: {e}")
        return None, None

# ============================================
# ENHANCED DONOR REQUEST EMAIL
# ============================================

def send_donor_request_email(donor, request, donor_rank=1, total_donors=1):
    """Send email to donor when requested"""
    try:
        if not donor or not request:
            return False
        
        # Get donor email and normalize
        donor_email = normalize_email(donor.get('email'))
        
        # Validate donor email
        if not is_valid_email(donor_email):
            print(f"❌ Invalid donor email: {donor_email}")
            return False
            
        base_url = st.get_option("server.baseUrlPath") or "http://localhost:8501"
        
        accept_url = f"{base_url}/?accept={request.get('id')}&donor={donor.get('id')}"
        reject_url = f"{base_url}/?reject={request.get('id')}&donor={donor.get('id')}"
        
        subject = f"🩸 URGENT: Blood Donation Needed - {request.get('blood', 'Unknown')}"
        
        # Calculate distance
        distance_text = ""
        priority_text = ""
        patient_coords = get_coords(request.get('location', ''))
        donor_coords = (donor.get('latitude'), donor.get('longitude')) if donor.get('latitude') else get_coords(donor.get('location', ''))
        
        if patient_coords and donor_coords and donor_coords[0] and donor_coords[1]:
            try:
                distance = geodesic(patient_coords, donor_coords).km
                distance_display = f"{distance:.1f}" if distance is not None else "Unknown"
                distance_text = f"<p><strong>📍 Distance from you:</strong> <span style='font-size: 1.2rem; color: #ff6b6b;'>{distance_display} km</span></p>"
                
                if donor_rank == 1:
                    priority_text = "<p><strong style='color: #43e97b;'>🌟 You are the CLOSEST donor to this patient!</strong></p>"
                else:
                    priority_text = f"<p><strong>Donor Rank:</strong> #{donor_rank} of {total_donors} eligible donors</p>"
            except:
                pass
        else:
            distance_text = "<p><strong>📍 Distance:</strong> Unable to calculate</p>"
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea20, #764ba220);">
    <div style="max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <div style="background: linear-gradient(135deg, #ff6b6b, #ee5253); padding: 30px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 32px;">🩸 URGENT BLOOD REQUEST</h1>
            <p style="color: white; margin: 10px 0 0;">Someone needs your help!</p>
        </div>
        
        <div style="padding: 30px;">
            <h2>Hello {donor.get('name', 'Donor')},</h2>
            
            <p>A patient urgently needs your blood type. You are the closest available donor.</p>
            
            {priority_text}
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin: 20px 0; border-left: 5px solid #ff6b6b;">
                <h3 style="color: #ff6b6b;">📋 REQUEST DETAILS</h3>
                <table style="width: 100%;">
                    <tr><td><strong>Blood Type:</strong></td><td><span style="background: #ff6b6b; color: white; padding: 5px 15px; border-radius: 5px;">{request.get('blood', 'Unknown')}</span></td></tr>
                    <tr><td><strong>Units Needed:</strong></td><td>{request.get('units_needed', 1)}</td></tr>
                    <tr><td><strong>Hospital:</strong></td><td>{request.get('hospital', 'Unknown')}</td></tr>
                    <tr><td><strong>Location:</strong></td><td>{request.get('location', 'Unknown')}</td></tr>
                    <tr><td><strong>Patient:</strong></td><td>{request.get('patient', 'Unknown')}</td></tr>
                </table>
                {distance_text}
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{accept_url}" style="background: #43e97b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 50px; margin: 0 10px; display: inline-block;">✅ ACCEPT</a>
                <a href="{reject_url}" style="background: #ff6b6b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 50px; margin: 0 10px; display: inline-block;">❌ REJECT</a>
            </div>
            
            <div style="background: #fff3cd; padding: 20px; border-radius: 15px;">
                <p><strong>⏰ Important:</strong> If you don't respond within {WAIT_MINUTES} minutes, we'll contact the next closest donor.</p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        success = send_email(donor_email, subject, message, html=True)
        return success
        
    except Exception as e:
        print(f"Donor email error: {e}")
        return False

# ============================================
# ENHANCED PATIENT NOTIFICATION EMAIL
# ============================================

def send_patient_notification_email(patient_email, patient_name, donor, request, donor_distance=None):
    """Send email to patient when donor accepts"""
    try:
        if not patient_email or not donor or not request:
            return False
        
        # Normalize and validate patient email
        patient_email = normalize_email(patient_email)
        
        if not is_valid_email(patient_email):
            print(f"❌ Invalid patient email: {patient_email}")
            return False
            
        subject = f"✅ Donor Found - Blood Request #{request.get('request_id', '')[:8]}"
        
        # Calculate distance if not provided
        if not donor_distance and request.get('latitude') and donor.get('latitude'):
            try:
                donor_distance = geodesic(
                    (request['latitude'], request['longitude']),
                    (donor['latitude'], donor['longitude'])
                ).km
            except:
                donor_distance = None
        
        distance_display = f"{donor_distance:.1f}" if donor_distance else "Unknown"
        distance_text = f"<p><strong>📍 Distance from hospital:</strong> {distance_display} km</p>" if donor_distance else ""
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #43e97b20, #38f9d720);">
    <div style="max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 30px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 32px;">✅ DONOR FOUND!</h1>
            <p style="color: white; margin: 10px 0 0;">A donor has accepted your request</p>
        </div>
        
        <div style="padding: 30px;">
            <h2>Dear {patient_name},</h2>
            
            <p>Great news! A donor has accepted your blood request. Here are their contact details:</p>
            
            <div style="background: linear-gradient(135deg, #43e97b20, #38f9d720); padding: 20px; border-radius: 15px; margin: 20px 0; border: 2px solid #43e97b;">
                <h3 style="color: #43e97b;">🩸 DONOR DETAILS</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr><td style="padding: 10px;"><strong>Name:</strong></td><td style="padding: 10px;">{donor.get('name', 'Unknown')}</td></tr>
                    <tr><td style="padding: 10px;"><strong>Blood Type:</strong></td><td style="padding: 10px;"><span style="background: #ff6b6b; color: white; padding: 5px 15px; border-radius: 5px;">{donor.get('blood', 'Unknown')}</span></td></tr>
                    <tr><td style="padding: 10px;"><strong>Phone:</strong></td><td style="padding: 10px;"><a href="tel:{donor.get('phone', '')}" style="color: #667eea; text-decoration: none; font-weight: bold;">{donor.get('phone', '')}</a></td></tr>
                    <tr><td style="padding: 10px;"><strong>Email:</strong></td><td style="padding: 10px;"><a href="mailto:{donor.get('email', '')}" style="color: #667eea;">{donor.get('email', '')}</a></td></tr>
                    <tr><td style="padding: 10px;"><strong>Location:</strong></td><td style="padding: 10px;">{donor.get('location', 'Unknown')}</td></tr>
                    {distance_text}
                    <tr><td style="padding: 10px;"><strong>Donor Level:</strong></td><td style="padding: 10px;">{donor.get('donor_level', 'New Donor 🌟')}</td></tr>
                    <tr><td style="padding: 10px;"><strong>Total Donations:</strong></td><td style="padding: 10px;">{donor.get('total_donations', 0)}</td></tr>
                </table>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin: 20px 0;">
                <h3 style="color: #333;">📋 REQUEST SUMMARY</h3>
                <table style="width: 100%;">
                    <tr><td><strong>Request ID:</strong></td><td>{request.get('request_id', '')}</td></tr>
                    <tr><td><strong>Blood Type:</strong></td><td><span style="background: #ff6b6b; color: white; padding: 3px 10px; border-radius: 5px;">{request.get('blood', 'Unknown')}</span></td></tr>
                    <tr><td><strong>Units:</strong></td><td>{request.get('units_needed', 1)}</td></tr>
                    <tr><td><strong>Hospital:</strong></td><td>{request.get('hospital', 'Unknown')}</td></tr>
                </table>
            </div>
            
            <div style="background: #fff3cd; padding: 20px; border-radius: 15px;">
                <h4 style="color: #856404;">📝 NEXT STEPS</h4>
                <ol style="color: #856404; margin-bottom: 0;">
                    <li><strong>Contact the donor IMMEDIATELY</strong> using the phone number above</li>
                    <li>Schedule the donation time with the donor and hospital</li>
                    <li>Confirm the appointment with the hospital blood bank</li>
                    <li>Keep the donor's contact information handy</li>
                </ol>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="tel:{donor.get('phone', '')}" style="background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 50px; margin: 0 10px; display: inline-block;">📞 CALL DONOR NOW</a>
                <a href="mailto:{donor.get('email', '')}" style="background: #764ba2; color: white; padding: 15px 30px; text-decoration: none; border-radius: 50px; margin: 0 10px; display: inline-block;">📧 EMAIL DONOR</a>
            </div>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px; text-align: center;">BloodAI - Connecting Donors with Those in Need</p>
        </div>
    </div>
</body>
</html>
        """
        
        success = send_email(patient_email, subject, message, html=True)
        if success:
            print(f"✅ Patient notification email sent to {patient_email}")
        return success
        
    except Exception as e:
        print(f"Patient email error: {e}")
        return False

# ============================================
# DONOR CONFIRMATION EMAIL
# ============================================

def send_donor_confirmation_email(donor, patient_name, request, next_eligible, donor_distance=None):
    """Send confirmation email to donor after acceptance"""
    try:
        if not donor or not request:
            return False
        
        # Normalize and validate donor email
        donor_email = normalize_email(donor.get('email'))
        
        if not is_valid_email(donor_email):
            print(f"❌ Invalid donor email: {donor_email}")
            return False
            
        subject = "🎉 Thank You - Blood Donation Confirmed"
        
        distance_display = f"{donor_distance:.1f}" if donor_distance else "Unknown"
        distance_text = f"<p><strong>📍 Distance to hospital:</strong> {distance_display} km</p>" if donor_distance else ""
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #ffd70020, #ffa50020);">
    <div style="max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <div style="background: linear-gradient(135deg, #ffd700 0%, #ffa500 100%); padding: 30px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 36px;">🎉 THANK YOU HERO!</h1>
            <p style="color: white; margin: 10px 0 0;">You've accepted a donation request</p>
        </div>
        
        <div style="padding: 30px;">
            <h2>Dear {donor.get('name', 'Donor')},</h2>
            
            <p>Thank you for accepting the blood donation request! Your willingness to help is truly heroic.</p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin: 20px 0; border-left: 5px solid #ffd700;">
                <h3 style="color: #ffa500;">🏥 DONATION DETAILS</h3>
                <table style="width: 100%;">
                    <tr><td><strong>Patient:</strong></td><td>{patient_name}</td></tr>
                    <tr><td><strong>Hospital:</strong></td><td>{request.get('hospital', 'Unknown')}</td></tr>
                    <tr><td><strong>Location:</strong></td><td>{request.get('location', 'Unknown')}</td></tr>
                    <tr><td><strong>Blood Type:</strong></td><td><span style="background: #ff6b6b; color: white; padding: 3px 10px; border-radius: 5px;">{request.get('blood', 'Unknown')}</span></td></tr>
                    <tr><td><strong>Units:</strong></td><td>{request.get('units_needed', 1)}</td></tr>
                    {distance_text}
                </table>
            </div>
            
            <div style="background: #e8f4fd; padding: 20px; border-radius: 15px; margin: 20px 0;">
                <h4 style="color: #0056b3;">🎁 REWARDS EARNED</h4>
                <p><strong>Points:</strong> +{POINTS_PER_DONATION}</p>
                <p><strong>Next Eligible Date:</strong> {next_eligible}</p>
            </div>
            
            <div style="background: #fff3cd; padding: 20px; border-radius: 15px;">
                <h4 style="color: #856404;">⏰ IMPORTANT INFORMATION</h4>
                <ul style="color: #856404; margin-bottom: 0;">
                    <li>You are now on cooldown for {COOLDOWN_MONTHS} months</li>
                    <li>The patient will contact you shortly</li>
                    <li>Please bring a valid ID to the hospital</li>
                    <li>Stay hydrated and eat well before donating</li>
                </ul>
            </div>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px; text-align: center;">BloodAI - Thank You for Saving Lives!</p>
        </div>
    </div>
</body>
</html>
        """
        
        success = send_email(donor_email, subject, message, html=True)
        if success:
            print(f"✅ Donor confirmation email sent to {donor_email}")
        return success
    except Exception as e:
        print(f"Confirmation email error: {e}")
        return False

# ============================================
# WELCOME EMAIL FOR NEW DONORS
# ============================================

def send_welcome_email(donor_email, donor_name, donor_details):
    """Send welcome email to new donors"""
    try:
        if not donor_email:
            return False
        
        # Normalize and validate donor email
        donor_email = normalize_email(donor_email)
        
        if not is_valid_email(donor_email):
            print(f"❌ Invalid donor email: {donor_email}")
            return False
            
        subject = "🎉 Welcome to BloodAI - Thank You for Registering!"
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea20, #764ba220);">
    <div style="max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 36px;">🩸 Welcome to BloodAI!</h1>
        </div>
        
        <div style="padding: 30px;">
            <h2>Hello {donor_name},</h2>
            
            <p>Thank you for registering as a blood donor!</p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin: 20px 0;">
                <h3>Your Donor Profile:</h3>
                <p><strong>Donor ID:</strong> {donor_details.get('donor_id', '')}</p>
                <p><strong>Blood Type:</strong> {donor_details.get('blood', 'Unknown')}</p>
                <p><strong>Location:</strong> {donor_details.get('location', 'Unknown')}</p>
            </div>
            
            <div style="background: #e8f4fd; padding: 20px; border-radius: 15px;">
                <h3>📍 Location-Based Matching</h3>
                <p>The closest donors are always contacted first!</p>
            </div>
            
            <p>Together, we can save lives!</p>
        </div>
    </div>
</body>
</html>
        """
        
        return send_email(donor_email, subject, message, html=True)
    except Exception as e:
        print(f"Welcome email error: {e}")
        return False

# ============================================
# AUTO NEXT DONOR FUNCTION
# ============================================

def check_and_contact_next_donor():
    """Check pending requests and contact next donor after timeout"""
    try:
        pending = execute_query(
            "SELECT * FROM requests WHERE status='Pending'",
            fetch_all=True
        ) or []
        
        for request in pending:
            if not request:
                continue
                
            request_id = request.get('id')
            blood_type = request.get('blood')
            location = request.get('location')
            contacted = request.get('contacted') or ""
            last_contacted = request.get('last_contacted_time')
            
            if not last_contacted or not request_id or not blood_type or not location:
                continue
            
            try:
                last_time = datetime.strptime(last_contacted, "%Y-%m-%d %H:%M:%S")
                current_time = datetime.now()
                
                if current_time - last_time >= timedelta(minutes=WAIT_MINUTES):
                    print(f"⏰ {WAIT_MINUTES} minutes passed for request {request_id}")
                    
                    next_donor, all_sorted = find_next_donor(blood_type, location, contacted)
                    
                    if next_donor:
                        donor_rank = 1
                        total_donors = 1
                        donor_distance = None
                        
                        if all_sorted:
                            for i, d in enumerate(all_sorted):
                                if d and d.get('donor') and d['donor'].get('id') == next_donor.get('id'):
                                    donor_rank = i + 1
                                    total_donors = len(all_sorted)
                                    if d.get('distance') != float('inf'):
                                        donor_distance = d.get('distance')
                                    break
                        
                        new_contacted = contacted + str(next_donor.get('id')) + ","
                        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
                        
                        execute_query(
                            """UPDATE requests 
                               SET donor_id=?, contacted=?, last_contacted_time=?, closest_donor_distance=?
                               WHERE id=?""",
                            (next_donor.get('id'), new_contacted, current_time_str, donor_distance, request_id),
                            commit=True
                        )
                        
                        send_donor_request_email(next_donor, request, donor_rank, total_donors)
                        print(f"✅ Contacted next donor {next_donor.get('id')}")
                    else:
                        print(f"❌ No more donors available")
                        execute_query(
                            "UPDATE requests SET status='No Donors Available' WHERE id=?",
                            (request_id,),
                            commit=True
                        )
                        
                        add_notification(
                            request.get('patient_email'),
                            'no_donors',
                            'No Donors Available',
                            "No donors available for your request"
                        )
            except Exception as e:
                print(f"Error processing request {request_id}: {e}")
    except Exception as e:
        print(f"Scheduler error: {e}")

# ============================================
# SCHEDULER THREAD
# ============================================

def run_scheduler():
    while True:
        try:
            check_and_contact_next_donor()
        except Exception as e:
            print(f"Scheduler error: {e}")
        time.sleep(30)

if not st.session_state.scheduler_started:
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
    st.session_state.scheduler_started = True

# ============================================
# FIXED DONOR RESPONSE HANDLER
# ============================================

def handle_donor_response():
    """Handle donor accept/reject with proper error handling and email notifications"""
    try:
        query_params = st.query_params
        
        if "accept" in query_params and "donor" in query_params:
            try:
                request_id = int(query_params["accept"])
                donor_id = int(query_params["donor"])
                
                st.markdown("""
                <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #43e97b, #38f9d7); border-radius: 20px; margin: 2rem 0;'>
                    <h1 style='color: white; font-size: 3rem;'>✅ Processing Your Acceptance...</h1>
                    <p style='color: white;'>Please wait while we update the system and notify the patient.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Get request
                request = execute_query(
                    "SELECT * FROM requests WHERE id=?",
                    (request_id,),
                    fetch_one=True
                )
                
                if not request:
                    st.error("❌ Request not found")
                    return
                
                # Get donor
                donor = execute_query(
                    "SELECT * FROM donors WHERE id=?",
                    (donor_id,),
                    fetch_one=True
                )
                
                if not donor:
                    st.error("❌ Donor not found")
                    return
                
                # Normalize and validate emails
                patient_email = normalize_email(request.get('patient_email'))
                donor_email = normalize_email(donor.get('email'))
                
                if not is_valid_email(patient_email):
                    st.error(f"❌ Invalid patient email: {patient_email}")
                    return
                    
                if not is_valid_email(donor_email):
                    st.error(f"❌ Invalid donor email: {donor_email}")
                    return
                
                # Check if request is still pending
                if request.get('status') != 'Pending':
                    if request.get('status') == 'Accepted':
                        st.warning("⚠️ This request has already been accepted by another donor.")
                    else:
                        st.warning(f"⚠️ This request is no longer available")
                    return
                
                # Calculate donor distance for records
                donor_distance = None
                if request.get('latitude') and donor.get('latitude'):
                    try:
                        donor_distance = geodesic(
                            (request['latitude'], request['longitude']),
                            (donor['latitude'], donor['longitude'])
                        ).km
                    except:
                        pass
                
                # Process the acceptance
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Update donor status and details
                execute_query(
                    """UPDATE donors 
                       SET status='Busy', 
                           last_donation_date=?,
                           total_donations = COALESCE(total_donations, 0) + 1,
                           points = COALESCE(points, 0) + ?
                       WHERE id=?""",
                    (current_time, POINTS_PER_DONATION, donor_id),
                    commit=True
                )
                
                # Update donor level based on new donation count
                update_donor_points(donor_id)
                
                # Update request status
                execute_query(
                    """UPDATE requests 
                       SET status='Accepted', 
                           completed_time=?,
                           donor_id=?,
                           closest_donor_distance=?
                       WHERE id=?""",
                    (current_time, donor_id, donor_distance, request_id),
                    commit=True
                )
                
                # Add to donation history
                history_id = generate_id('DH')
                execute_query(
                    """INSERT INTO donation_history 
                       (history_id, donor_id, request_id, donation_date, hospital, 
                        blood_type, units, points_earned, donor_distance_km)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (history_id, donor_id, request_id, current_time, 
                     request.get('hospital'), request.get('blood'), 
                     request.get('units_needed', 1), POINTS_PER_DONATION,
                     donor_distance),
                    commit=True
                )
                
                # Calculate next eligible date
                next_eligible = (datetime.now() + timedelta(days=COOLDOWN_MONTHS * 30)).strftime("%Y-%m-%d")
                
                # SEND EMAIL NOTIFICATIONS
                email_status = []
                
                # 1. Send email to patient with donor details
                patient_email_sent = send_patient_notification_email(
                    patient_email, 
                    request.get('patient'), 
                    donor, 
                    request, 
                    donor_distance
                )
                email_status.append(("Patient", "✅ Sent" if patient_email_sent else "❌ Failed"))
                
                # 2. Send confirmation email to donor
                donor_email_sent = send_donor_confirmation_email(
                    donor, 
                    request.get('patient'), 
                    request, 
                    next_eligible, 
                    donor_distance
                )
                email_status.append(("Donor", "✅ Sent" if donor_email_sent else "❌ Failed"))
                
                # Add notifications
                add_notification(
                    patient_email,
                    'donor_found',
                    '✅ Donor Found!',
                    f"{donor.get('name')} has accepted your blood request. Contact them at {donor.get('phone')}"
                )
                
                add_notification(
                    donor_email,
                    'accepted',
                    '🎉 Donation Confirmed',
                    f"Thank you for accepting! You can donate again after {next_eligible}"
                )
                
                # Clear query parameters
                st.query_params.clear()
                st.session_state.showing_response = False
                
                # Show success page with animations
                st.balloons()
                st.snow()
                
                # Display email status
                st.info("📧 Email Notifications:")
                for recipient, status in email_status:
                    st.write(f"{recipient}: {status}")
                
                # Show donor stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea, #764ba2); padding: 2rem; border-radius: 20px; color: white; text-align: center;'>
                        <h1 style='font-size: 3rem;'>🩸</h1>
                        <h2>{donor.get('total_donations', 0) + 1}</h2>
                        <p>Total Donations</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    donor_level_display = donor.get('donor_level', 'New Donor 🌟')
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #43e97b, #38f9d7); padding: 2rem; border-radius: 20px; color: white; text-align: center;'>
                        <h1 style='font-size: 3rem;'>⭐</h1>
                        <h2>{donor_level_display}</h2>
                        <p>Donor Level</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #f093fb, #f5576c); padding: 2rem; border-radius: 20px; color: white; text-align: center;'>
                        <h1 style='font-size: 3rem;'>🎁</h1>
                        <h2>+{POINTS_PER_DONATION}</h2>
                        <p>Points Earned</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if donor_distance:
                    distance_display = f"{donor_distance:.1f}"
                    st.info(f"📍 Distance to hospital: {distance_display} km")
                
                # Show donation summary
                st.markdown(f"""
                <div style='background: white; padding: 2rem; border-radius: 20px; margin-top: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>
                    <h2>📋 Donation Summary</h2>
                    <table style='width: 100%;'>
                        <tr><td><strong>Patient:</strong></td><td>{request.get('patient', 'Unknown')}</td></tr>
                        <tr><td><strong>Patient Email:</strong></td><td>{patient_email}</td></tr>
                        <tr><td><strong>Hospital:</strong></td><td>{request.get('hospital', 'Unknown')}</td></tr>
                        <tr><td><strong>Blood Type:</strong></td><td><span style='background: #ff6b6b; color: white; padding: 5px 10px; border-radius: 5px;'>{request.get('blood', 'Unknown')}</span></td></tr>
                        <tr><td><strong>Next Eligible:</strong></td><td><strong>{next_eligible}</strong></td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                
                # Show donor contact information
                st.markdown(f"""
                <div style='background: #e8f4fd; padding: 2rem; border-radius: 20px; margin-top: 2rem;'>
                    <h3>📞 Your Contact Information (Sent to Patient)</h3>
                    <p><strong>Name:</strong> {donor.get('name', 'Unknown')}</p>
                    <p><strong>Phone:</strong> {donor.get('phone', 'Unknown')}</p>
                    <p><strong>Email:</strong> {donor_email}</p>
                    <p><strong>Location:</strong> {donor.get('location', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col2:
                    if st.button("🏠 Return Home", use_container_width=True):
                        st.rerun()
                
                return True
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                print(f"Accept error details: {e}")
                return False
        
        elif "reject" in query_params and "donor" in query_params:
            try:
                request_id = int(query_params["reject"])
                donor_id = int(query_params["donor"])
                
                st.markdown("""
                <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #ff6b6b, #ee5253); border-radius: 20px; margin: 2rem 0;'>
                    <h1 style='color: white; font-size: 3rem;'>🕊️ Request Rejected</h1>
                    <p style='color: white;'>The next closest donor will be contacted.</p>
                </div>
                """, unsafe_allow_html=True)
                
                request = execute_query(
                    "SELECT * FROM requests WHERE id=?",
                    (request_id,),
                    fetch_one=True
                )
                
                if request and request.get('status') == 'Pending':
                    contacted = request.get('contacted', '')
                    if str(donor_id) not in contacted:
                        new_contacted = contacted + str(donor_id) + ","
                        execute_query(
                            "UPDATE requests SET contacted=? WHERE id=?",
                            (new_contacted, request_id),
                            commit=True
                        )
                        
                        st.info("✅ Your response has been recorded. The system will now contact the next closest donor.")
                
                st.query_params.clear()
                st.session_state.showing_response = False
                
                col1, col2, col3 = st.columns(3)
                with col2:
                    if st.button("🏠 Return Home", use_container_width=True):
                        st.rerun()
                
                return True
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                return False
                
    except Exception as e:
        print(f"Response handler error: {e}")
        return False

# ============================================
# RESPONSE HANDLER INITIALIZATION
# ============================================

def init_response_handler():
    """Initialize and handle donor responses"""
    try:
        query_params = st.query_params
        
        if "accept" in query_params or "reject" in query_params:
            st.session_state.showing_response = True
            handle_donor_response()
            
            if st.button("🏠 Return to Home", use_container_width=True):
                st.query_params.clear()
                st.session_state.showing_response = False
                st.rerun()
            
            st.stop()
    except Exception as e:
        print(f"Response handler init error: {e}")

init_response_handler()

# ============================================
# DONOR SEARCH ANIMATION
# ============================================

def show_donor_search():
    """Show interactive donor search animation"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        time.sleep(0.02)
        progress_bar.progress(i + 1)
        
        if i < 30:
            status_text.text("🔍 Scanning donor database...")
        elif i < 60:
            status_text.text("📍 Calculating distances...")
        elif i < 90:
            status_text.text("🤖 Sorting by proximity...")
        else:
            status_text.text("✅ Found closest match!")
    
    time.sleep(0.5)
    progress_bar.empty()
    status_text.empty()

# ============================================
# BLOOD INVENTORY MANAGEMENT
# ============================================

class BloodInventoryManager:
    def __init__(self):
        self.alert_threshold = BLOOD_STOCK_ALERT_THRESHOLD
    
    def get_inventory_summary(self):
        query = "SELECT blood_type, SUM(units) as total_units FROM blood_inventory WHERE status='Available' GROUP BY blood_type"
        return execute_query(query, fetch_all=True) or []
    
    def check_stock_alerts(self):
        inventory = self.get_inventory_summary()
        blood_status = {}
        
        for item in inventory:
            if item:
                blood_status[item.get('blood_type')] = {
                    'units': item.get('total_units', 0),
                    'status': 'normal' if item.get('total_units', 0) >= self.alert_threshold else 'low'
                }
        
        for bt in BLOOD_TYPES:
            if bt not in blood_status:
                blood_status[bt] = {'units': 0, 'status': 'critical'}
        
        return blood_status
    
    def display_inventory_dashboard(self):
        blood_status = self.check_stock_alerts()
        
        st.subheader("📊 Current Blood Inventory")
        
        cols = st.columns(4)
        for i, bt in enumerate(BLOOD_TYPES):
            with cols[i % 4]:
                status = blood_status.get(bt, {'units': 0, 'status': 'critical'})
                units = status.get('units', 0)
                status_text = status.get('status', 'critical')
                
                if units == 0:
                    card_class = "inventory-card critical"
                elif units < self.alert_threshold:
                    card_class = "inventory-card low"
                else:
                    card_class = "inventory-card"
                
                st.markdown(f"""
                <div class='{card_class}'>
                    <h3>{bt}</h3>
                    <h2>{units} units</h2>
                    <p>Status: {status_text.upper()}</p>
                </div>
                """, unsafe_allow_html=True)

# ============================================
# QR CODE GENERATOR
# ============================================

class QRCodeManager:
    def generate_donor_qr(self, donor_id, donor_data):
        try:
            qr_data = {
                'donor_id': donor_id,
                'name': donor_data.get('name', ''),
                'blood_type': donor_data.get('blood', ''),
                'donor_level': donor_data.get('donor_level', 'New Donor 🌟'),
                'total_donations': donor_data.get('total_donations', 0),
                'verified': donor_data.get('is_verified', 0)
            }
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(json.dumps(qr_data))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"
        except:
            return None

# ============================================
# SIDEBAR SETUP
# ============================================

st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <h1 style='color: #ff6b6b; font-size: 2.5rem;'>🩸 BloodAI</h1>
    <p>Complete Blood Donation System</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📊 Quick Stats")
selected_blood = st.sidebar.selectbox("Blood Type", BLOOD_TYPES, key="sidebar_blood")

eligible_donors = get_eligible_donors(selected_blood)
eligible_count = len(eligible_donors)

total_result = execute_query("SELECT COUNT(*) as count FROM donors WHERE blood=?", (selected_blood,), fetch_one=True)
total = total_result['count'] if total_result else 0

st.sidebar.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea20, #764ba220); padding: 1rem; border-radius: 10px;'>
    <p><strong>🩸 {selected_blood}</strong></p>
    <p>✅ Eligible: {eligible_count}</p>
    <p>📊 Total: {total}</p>
    <p>📍 Sorted by: <strong style='color: #43e97b;'>NEAREST FIRST</strong></p>
</div>
""", unsafe_allow_html=True)

inventory_manager = BloodInventoryManager()
st.sidebar.markdown("---")

menu_options = [
    "🏠 Home",
    "📝 Donor Register",
    "🆘 Patient Request",
    "📍 Track Request",
    "🏆 Donor Leaderboard",
    "🔔 Notifications",
    "👤 Donor Dashboard",
    "📦 Blood Inventory",
    "👑 Admin",
    "📧 Email Log"
]

menu = st.sidebar.radio("Navigation", menu_options)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 System Status")
st.sidebar.info(f"⏱️ Auto-donor: Every 30s")
st.sidebar.info(f"⏳ Response: {WAIT_MINUTES} min")
st.sidebar.info(f"🛡️ Cooldown: {COOLDOWN_MONTHS} months")
st.sidebar.markdown("📍 **Closest donors contacted first - UNLIMITED DISTANCE**")

# ============================================
# MAIN CONTENT
# ============================================

if not st.session_state.get('showing_response', False):
    
    # ============================================
    # HOME PAGE
    # ============================================
    
    if menu == "🏠 Home":
        st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 3rem;'>🩸 BloodAI Complete System</h1>
            <p style='font-size: 1.5rem;'>Location-Based Donor Matching</p>
        </div>
        """, unsafe_allow_html=True)
        
        pending_result = execute_query("SELECT COUNT(*) as count FROM requests WHERE status='Pending'", fetch_one=True)
        pending_count = pending_result['count'] if pending_result else 0
        
        if pending_count > 0:
            st.markdown(f"""
            <div class='emergency-banner emergency-glow'>
                🚨 {pending_count} patient(s) waiting for blood!
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_donors = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
            total_donors = total_donors['count'] if total_donors else 0
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{total_donors}</div><div>Total Donors</div></div>", unsafe_allow_html=True)
        
        with col2:
            eligible = sum(len(get_eligible_donors(bt)) for bt in BLOOD_TYPES)
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{eligible}</div><div>Eligible Now</div></div>", unsafe_allow_html=True)
        
        with col3:
            total_requests = execute_query("SELECT COUNT(*) as count FROM requests", fetch_one=True)
            total_requests = total_requests['count'] if total_requests else 0
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{total_requests}</div><div>Total Requests</div></div>", unsafe_allow_html=True)
        
        with col4:
            total_units = execute_query("SELECT SUM(units) as total FROM donation_history", fetch_one=True)
            total_units_value = total_units.get('total', 0) if total_units else 0
            lives_saved = (total_units_value or 0) * 3
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{lives_saved}</div><div>Lives Saved</div></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📦 Current Blood Inventory")
        inventory_manager.display_inventory_dashboard()

    # ============================================
    # DONOR REGISTER PAGE
    # ============================================

    elif menu == "📝 Donor Register":
        st.title("📝 Donor Registration")
        st.info("📍 Your location will be used to find nearby requests")
        
        with st.form("donor_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*")
                email = st.text_input("Email*")
                phone = st.text_input("Phone Number*")
                age = st.number_input("Age*", min_value=18, max_value=65, value=25)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            with col2:
                blood = st.selectbox("Blood Type*", BLOOD_TYPES)
                location = st.text_input("Full Address/Location*")
                weight = st.number_input("Weight (kg)*", min_value=45, value=70)
                emergency_contact = st.text_input("Emergency Contact")
            
            health_conditions = st.text_area("Any health conditions?")
            password = st.text_input("Password*", type="password")
            confirm = st.text_input("Confirm Password*", type="password")
            
            submitted = st.form_submit_button("Register")
            
            if submitted:
                if not all([name, email, phone, location, password]):
                    st.error("Please fill all required fields")
                elif password != confirm:
                    st.error("Passwords do not match")
                elif age < 18:
                    st.error("Must be 18+")
                elif weight < 45:
                    st.error("Minimum weight 45 kg")
                else:
                    # Normalize and validate email
                    email = normalize_email(email)
                    if not is_valid_email(email):
                        st.error("❌ Invalid email format")
                    else:
                        try:
                            donor_id = generate_id('DNR')
                            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            coords = get_coords(location)
                            lat, lon = coords if coords else (None, None)
                            
                            execute_query(
                                """INSERT INTO donors 
                                   (donor_id, name, email, phone, blood, location, latitude, longitude, password, 
                                    registration_date, weight, age, gender, emergency_contact, health_conditions,
                                    points, donor_level, is_verified, last_location_update)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (donor_id, name, email, phone, blood, location, lat, lon,
                                 hash_password(password), current_time, weight, age, gender,
                                 emergency_contact, health_conditions, 0, "New Donor 🌟",
                                 1 if coords else 0, current_time),
                                commit=True
                            )
                            
                            donor_details = {'donor_id': donor_id, 'blood': blood, 'location': location}
                            send_welcome_email(email, name, donor_details)
                            
                            st.success("✅ Registration successful!")
                            
                            if coords:
                                qr_manager = QRCodeManager()
                                donor_data = {'name': name, 'blood': blood, 'is_verified': 1}
                                qr_code = qr_manager.generate_donor_qr(donor_id, donor_data)
                                if qr_code:
                                    st.image(qr_code, caption="Your Donor QR Code", width=200)
                            
                            st.balloons()
                        except sqlite3.IntegrityError:
                            st.error("Email already registered")

    # ============================================
    # PATIENT REQUEST PAGE
    # ============================================

    elif menu == "🆘 Patient Request":
        st.title("🆘 Emergency Blood Request")
        st.info(f"⏱️ Donors have {WAIT_MINUTES} minutes to respond. Closest donors contacted first!")
        
        with st.form("request_form"):
            col1, col2 = st.columns(2)
            with col1:
                patient = st.text_input("Patient Name*")
                email = st.text_input("Your Email*")
                blood = st.selectbox("Blood Type Needed*", BLOOD_TYPES)
            with col2:
                location = st.text_input("Hospital Location*")
                hospital = st.text_input("Hospital Name*")
                hospital_contact = st.text_input("Hospital Contact")
            
            units = st.number_input("Units Needed", min_value=1, max_value=10, value=1)
            submitted = st.form_submit_button("🚨 Request Blood")
            
            if submitted:
                if not all([patient, email, blood, location, hospital]):
                    st.error("Please fill all required fields")
                else:
                    # Normalize and validate email
                    email = normalize_email(email)
                    if not is_valid_email(email):
                        st.error("❌ Invalid email format")
                    else:
                        coords = get_coords(location)
                        lat, lon = coords if coords else (None, None)
                        
                        request_id = generate_id('REQ')
                        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        execute_query(
                            """INSERT INTO requests 
                               (request_id, patient, patient_email, blood, location, latitude, longitude, 
                                hospital, hospital_contact, status, time, units_needed)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (request_id, patient, email, blood, location, lat, lon,
                             hospital, hospital_contact, "Pending", current_time_str, units),
                            commit=True
                        )
                        
                        with st.spinner("🔍 Finding closest donors..."):
                            show_donor_search()
                            first_donor, all_sorted_donors = find_next_donor(blood, location, "")
                        
                        if first_donor:
                            donor_rank = 1
                            total_donors = 1
                            donor_distance = None
                            
                            if all_sorted_donors:
                                for i, d in enumerate(all_sorted_donors):
                                    if d and d.get('donor') and d['donor'].get('id') == first_donor.get('id'):
                                        donor_rank = i + 1
                                        total_donors = len(all_sorted_donors)
                                        if d.get('distance') != float('inf'):
                                            donor_distance = d.get('distance')
                                        break
                            
                            execute_query(
                                """UPDATE requests 
                                   SET donor_id=?, contacted=?, last_contacted_time=?, closest_donor_distance=?
                                   WHERE request_id=?""",
                                (first_donor.get('id'), str(first_donor.get('id')) + ",", current_time_str, donor_distance, request_id),
                                commit=True
                            )
                            
                            request = execute_query("SELECT * FROM requests WHERE request_id=?", (request_id,), fetch_one=True)
                            
                            if send_donor_request_email(first_donor, request, donor_rank, total_donors):
                                distance_display = f"{donor_distance:.1f}" if donor_distance else "Unknown"
                                st.success(f"✅ Closest donor contacted! Email sent to {first_donor.get('email')}")
                                
                                st.markdown(f"""
                                <div class='location-priority'>
                                    <h3 style='color: #43e97b;'>📍 Location Priority</h3>
                                    <p><strong>Donor Rank:</strong> #{donor_rank} of {total_donors} eligible donors</p>
                                    <p><strong>Distance:</strong> {distance_display} km</p>
                                    <p><strong>Response Time:</strong> {WAIT_MINUTES} minutes</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.markdown(f"""
                                <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; color: white; margin: 2rem 0;'>
                                    <h3>⏳ Response Timer</h3>
                                    <div class='countdown-timer'>{WAIT_MINUTES}:00</div>
                                    <p>Waiting for donor response...</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.markdown(f"""
                                **First Donor (Closest):**
                                - Name: {first_donor.get('name', 'Unknown')}
                                - Level: {first_donor.get('donor_level', 'New Donor 🌟')}
                                - Distance: {distance_display} km
                                """)
                        else:
                            st.warning("No eligible donors available.")
                            execute_query("UPDATE requests SET status='No Donors Available' WHERE request_id=?", (request_id,), commit=True)

    # ============================================
    # TRACK REQUEST PAGE
    # ============================================

    elif menu == "📍 Track Request":
        st.title("📍 Track Your Request")
        
        email = st.text_input("Enter your email")
        
        if st.button("Track"):
            if email:
                email = normalize_email(email)
                if not is_valid_email(email):
                    st.error("❌ Invalid email format")
                else:
                    requests = execute_query(
                        "SELECT * FROM requests WHERE patient_email=? ORDER BY id DESC",
                        (email,), fetch_all=True
                    ) or []
                    
                    if requests:
                        for req in requests:
                            if not req:
                                continue
                            status_emoji = {"Pending": "⏳", "Accepted": "✅", "No Donors Available": "❌"}.get(req.get('status'), "📝")
                            
                            with st.expander(f"{status_emoji} Request #{req.get('id')} - {req.get('blood', 'Unknown')}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown(f"""
                                    **Patient:** {req.get('patient', 'Unknown')}
                                    **Blood Type:** {req.get('blood', 'Unknown')}
                                    **Hospital:** {req.get('hospital', 'Unknown')}
                                    **Status:** {req.get('status', 'Unknown')}
                                    **Request Time:** {req.get('time', 'Unknown')}
                                    """)
                                with col2:
                                    if req.get('status') == "Pending" and req.get('last_contacted_time'):
                                        try:
                                            last = datetime.strptime(req['last_contacted_time'], "%Y-%m-%d %H:%M:%S")
                                            elapsed = datetime.now() - last
                                            remaining = max(0, WAIT_MINUTES - (elapsed.total_seconds() / 60))
                                            if remaining > 0:
                                                st.warning(f"⏳ Waiting for response... {remaining:.1f} min left")
                                                st.progress(min(elapsed.total_seconds() / (WAIT_MINUTES * 60), 1.0))
                                        except:
                                            pass
                                    
                                    if req.get('status') == "Accepted" and req.get('donor_id'):
                                        donor = execute_query("SELECT * FROM donors WHERE id=?", (req['donor_id'],), fetch_one=True)
                                        if donor:
                                            distance_display = f"{req.get('closest_donor_distance', 0):.1f}" if req.get('closest_donor_distance') else "Unknown"
                                            st.success("✅ Donor Found!")
                                            st.markdown(f"""
                                            **Donor:** {donor.get('name', 'Unknown')}
                                            **Phone:** {donor.get('phone', '')}
                                            **Distance:** {distance_display} km
                                            """)
                    else:
                        st.info("No requests found")

    # ============================================
    # DONOR LEADERBOARD
    # ============================================

    elif menu == "🏆 Donor Leaderboard":
        st.title("🏆 Donor Leaderboard")
        top_donors = execute_query(
            "SELECT name, total_donations, donor_level, blood, location FROM donors WHERE total_donations > 0 ORDER BY total_donations DESC LIMIT 20",
            fetch_all=True
        ) or []
        if top_donors:
            df = pd.DataFrame(top_donors)
            if not df.empty:
                df.insert(0, "Rank", range(1, len(df) + 1))
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No donations yet")

    # ============================================
    # NOTIFICATIONS PAGE
    # ============================================

    elif menu == "🔔 Notifications":
        st.title("🔔 Notifications")
        email = st.text_input("Enter your email")
        if email:
            email = normalize_email(email)
            if not is_valid_email(email):
                st.error("❌ Invalid email format")
            else:
                notifications = get_unread_notifications(email)
                if notifications:
                    st.success(f"You have {len(notifications)} notifications")
                    for notif in notifications:
                        if notif:
                            st.markdown(f"""
                            <div class='testimonial-card'>
                                <h4>{notif.get('title', '')}</h4>
                                <p>{notif.get('message', '')}</p>
                                <small>{notif.get('date', '')}</small>
                            </div>
                            """, unsafe_allow_html=True)
                    if st.button("Mark all as read"):
                        mark_notifications_read(email)
                        st.rerun()
                else:
                    st.info("No notifications")

    # ============================================
    # DONOR DASHBOARD
    # ============================================

    elif menu == "👤 Donor Dashboard":
        if st.session_state.logged_in_donor:
            donor = execute_query("SELECT * FROM donors WHERE id=?", (st.session_state.logged_in_donor['id'],), fetch_one=True)
            if donor:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown("<h1 style='font-size: 5rem;'>🩸</h1>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<h2>{donor.get('name', 'Donor')}</h2><p>{donor.get('donor_level', 'New Donor 🌟')} • {donor.get('blood', 'Unknown')}</p>", unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Donations", donor.get('total_donations', 0))
                with col2:
                    st.metric("Points", donor.get('points', 0))
                with col3:
                    st.metric("Level", donor.get('donor_level', 'New Donor 🌟'))
                with col4:
                    eligible, _ = is_donor_eligible(donor)
                    st.metric("Status", "✅ Eligible" if eligible else "⏳ Cooldown")
                
                if donor.get('latitude') and donor.get('longitude'):
                    st.success("📍 Location verified")
                else:
                    st.warning("⚠️ Location not verified")
                    new_location = st.text_input("Update your location:")
                    if st.button("Update"):
                        if update_donor_coordinates(donor['id'], new_location):
                            st.success("Location updated!")
                            st.rerun()
                
                st.markdown("---")
                st.subheader("Donation History")
                history = execute_query("SELECT * FROM donation_history WHERE donor_id=? ORDER BY donation_date DESC", (donor['id'],), fetch_all=True) or []
                if history:
                    st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)
                
                if st.button("Logout"):
                    st.session_state.logged_in_donor = None
                    st.rerun()
            else:
                st.session_state.logged_in_donor = None
        else:
            st.subheader("Login to Dashboard")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                email = normalize_email(email)
                if not is_valid_email(email):
                    st.error("❌ Invalid email format")
                else:
                    donor = execute_query("SELECT * FROM donors WHERE email=?", (email,), fetch_one=True)
                    if donor and verify_password(password, donor['password']):
                        st.session_state.logged_in_donor = donor
                        st.rerun()
                    else:
                        st.error("Invalid credentials")

    # ============================================
    # BLOOD INVENTORY PAGE
    # ============================================

    elif menu == "📦 Blood Inventory":
        st.title("📦 Blood Inventory")
        inventory_manager.display_inventory_dashboard()

    # ============================================
    # ADMIN PANEL
    # ============================================

    elif menu == "👑 Admin":
        if not st.session_state.admin_logged_in:
            with st.form("admin_login"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if username == ADMIN_USER and password == ADMIN_PASS:
                        st.session_state.admin_logged_in = True
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        else:
            st.success("Logged in as Admin")
            if st.button("Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()
            
            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Donors", "Requests", "Email Log"])
            
            with tab1:
                total_donors = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
                total_donors = total_donors['count'] if total_donors else 0
                total_requests = execute_query("SELECT COUNT(*) as count FROM requests", fetch_one=True)
                total_requests = total_requests['count'] if total_requests else 0
                total_donations = execute_query("SELECT COUNT(*) as count FROM donation_history", fetch_one=True)
                total_donations = total_donations['count'] if total_donations else 0
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Donors", total_donors)
                col2.metric("Requests", total_requests)
                col3.metric("Donations", total_donations)
            
            with tab2:
                donors = execute_query("SELECT * FROM donors", fetch_all=True) or []
                if donors:
                    st.dataframe(pd.DataFrame(donors), use_container_width=True, hide_index=True)
            
            with tab3:
                requests = execute_query("SELECT * FROM requests ORDER BY id DESC", fetch_all=True) or []
                if requests:
                    st.dataframe(pd.DataFrame(requests), use_container_width=True, hide_index=True)
            
            with tab4:
                email_logs = execute_query("SELECT * FROM email_log ORDER BY sent_date DESC LIMIT 50", fetch_all=True) or []
                if email_logs:
                    st.dataframe(pd.DataFrame(email_logs), use_container_width=True, hide_index=True)

    # ============================================
    # EMAIL LOG PAGE
    # ============================================

    elif menu == "📧 Email Log":
        st.title("📧 Email Log")
        if st.session_state.email_log:
            for log in st.session_state.email_log[-20:]:
                if log:
                    color = "#43e97b" if log.get('status') == 'sent' else "#ff6b6b"
                    st.markdown(f"""
                    <div class='testimonial-card' style='border-left-color: {color};'>
                        <p><strong>{log.get('time', '')}</strong> - {log.get('to', '')}</p>
                        <p>{log.get('subject', '')}</p>
                        <p style='color: {color};'>Status: {log.get('status', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No emails sent this session")

    # ============================================
    # FOOTER
    # ============================================

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <p>BloodAI v9.7 - Complete System</p>
        <p>📍 <strong style='color: #43e97b;'>Closest Donors First - UNLIMITED DISTANCE</strong></p>
    </div>

    """, unsafe_allow_html=True)
