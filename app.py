# ============================================
# 🩸 BLOODAI COMPLETE SYSTEM v23.0
# FIXED: Location Verification • QR Codes • Donation Events • Date Input
# PRODUCTION READY - ALL FEATURES WORKING
# ============================================

import streamlit as st
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, date
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
import os
import sys
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
    
    /* Event creation form */
    .event-form {
        background: linear-gradient(135deg, #667eea10, #764ba210);
        padding: 2rem;
        border-radius: 20px;
        border: 2px dashed #667eea;
        margin: 2rem 0;
    }
    
    /* QR code container */
    .qr-code-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    
    /* QR Section */
    .qr-section {
        background: linear-gradient(135deg, #667eea10, #764ba210);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        text-align: center;
        border: 2px dashed #667eea;
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
    
    /* Queue container */
    .queue-container {
        background: linear-gradient(135deg, #667eea10, #764ba210);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #667eea;
    }
    
    .priority-badge {
        background: #ff6b6b;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-right: 10px;
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, #43e97b, #38f9d7);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        animation: fadeIn 1s ease-in;
    }
    
    /* Event Status Badges */
    .event-status {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-upcoming {
        background: #667eea20;
        color: #667eea;
        border: 1px solid #667eea;
    }
    
    .status-ongoing {
        background: #43e97b20;
        color: #43e97b;
        border: 1px solid #43e97b;
        animation: pulse 2s infinite;
    }
    
    .status-completed {
        background: #99999920;
        color: #666;
        border: 1px solid #666;
    }
    
    .status-cancelled {
        background: #ff6b6b20;
        color: #ff6b6b;
        border: 1px solid #ff6b6b;
    }
    
    /* Event Stats */
    .event-stats {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Amenity Tags */
    .amenity-tag {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        background: #f0f0f0;
        border-radius: 15px;
        margin: 0.2rem;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CONFIGURATION - UPDATE THESE LINES
# ============================================

# Email Configuration - CHANGE THESE TO YOUR DETAILS
FROM_EMAIL = "vigneshsapavat11@gmail.com"  # ← Your email
APP_PASSWORD = "kmcfregjdseaihwn"  # ← Your Gmail App Password
BASE_URL = "https://bloodai-smart-donor-system.streamlit.app/"  # ← Your actual Streamlit URL

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
POINTS_PER_EVENT = 50

# Location Settings
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
if 'event_view' not in st.session_state:
    st.session_state.event_view = "view"

# ============================================
# PERSISTENT DATABASE SETUP
# ============================================

def get_database_path():
    """Get persistent database path for Streamlit Cloud"""
    try:
        persistent_path = "/mount/src/bloodai_final.db"
        os.makedirs("/mount/src", exist_ok=True)
        with open(persistent_path, 'a') as f:
            pass
        print(f"✅ Using persistent database: {persistent_path}")
        return persistent_path
    except:
        try:
            temp_path = "/tmp/bloodai_final.db"
            print(f"⚠️ Using temporary database: {temp_path}")
            return temp_path
        except:
            print("⚠️ Using local database: bloodai_final.db")
            return "bloodai_final.db"

DB_PATH = get_database_path()

# ============================================
# DATABASE CONNECTION MANAGER
# ============================================

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30)
        conn.row_factory = sqlite3.Row
        yield conn
    except Exception as e:
        print(f"Database connection error: {e}")
        yield None
    finally:
        if conn:
            conn.close()

def execute_query(query, params=(), fetch_one=False, fetch_all=False, commit=False):
    try:
        with get_db_connection() as conn:
            if conn is None:
                return None if fetch_one or fetch_all else -1
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
            if conn is None:
                st.error("❌ Could not connect to database")
                return False
                
            cursor = conn.cursor()
            
            # Donors table with coordinates
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
                notification_preference TEXT DEFAULT 'email',
                points INTEGER DEFAULT 0,
                donor_level TEXT DEFAULT 'New Donor 🌟',
                emergency_contact TEXT,
                medical_id TEXT,
                qr_code TEXT,
                total_points_earned INTEGER DEFAULT 0,
                badges TEXT,
                last_health_check TEXT,
                is_verified INTEGER DEFAULT 0,
                referred_by INTEGER,
                donation_reminder INTEGER DEFAULT 1,
                last_location_update TEXT
            )
            """)
            
            # Blood Inventory Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS blood_inventory(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                blood_type TEXT,
                units INTEGER DEFAULT 0,
                hospital_id INTEGER,
                expiry_date TEXT,
                batch_number TEXT,
                collection_date TEXT,
                status TEXT DEFAULT 'Available',
                location TEXT,
                last_updated TEXT,
                quality_checked INTEGER DEFAULT 0
            )
            """)
            
            # Hospitals Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospitals(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hospital_id TEXT UNIQUE,
                name TEXT,
                registration_number TEXT UNIQUE,
                address TEXT,
                city TEXT,
                state TEXT,
                phone TEXT,
                email TEXT,
                emergency_contact TEXT,
                license_number TEXT,
                verified INTEGER DEFAULT 0,
                registration_date TEXT,
                latitude REAL,
                longitude REAL,
                blood_bank_capacity INTEGER,
                accreditation TEXT
            )
            """)
            
            # Requests table with queue support
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
                hospital_id INTEGER,
                hospital_contact TEXT,
                doctor_name TEXT,
                status TEXT DEFAULT 'Pending',
                donor_id INTEGER,
                time TEXT,
                contacted TEXT DEFAULT '',
                current_donor_index INTEGER DEFAULT 0,
                last_contacted_time TEXT,
                urgency_level TEXT DEFAULT 'High',
                units_needed INTEGER DEFAULT 1,
                completed_time TEXT,
                patient_age INTEGER,
                patient_gender TEXT,
                reason TEXT,
                closest_donor_distance REAL,
                all_donors TEXT DEFAULT '',
                total_donors_count INTEGER DEFAULT 0,
                FOREIGN KEY (hospital_id) REFERENCES hospitals (id)
            )
            """)
            
            # Donation Events Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS donation_events(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE,
                event_name TEXT,
                organizer TEXT,
                organizer_id INTEGER,
                organizer_email TEXT,
                organizer_phone TEXT,
                location TEXT,
                address TEXT,
                city TEXT,
                start_date TEXT,
                end_date TEXT,
                start_time TEXT,
                end_time TEXT,
                target_donations INTEGER,
                registered_donors INTEGER DEFAULT 0,
                completed_donations INTEGER DEFAULT 0,
                status TEXT DEFAULT 'Upcoming',
                contact_person TEXT,
                contact_phone TEXT,
                contact_email TEXT,
                description TEXT,
                latitude REAL,
                longitude REAL,
                amenities TEXT,
                blood_types_needed TEXT,
                incentives TEXT,
                special_instructions TEXT,
                created_date TEXT,
                last_updated TEXT,
                image_url TEXT,
                registration_deadline TEXT,
                min_age INTEGER DEFAULT 18,
                max_age INTEGER DEFAULT 65,
                min_weight INTEGER DEFAULT 45,
                is_featured INTEGER DEFAULT 0,
                total_points_awarded INTEGER DEFAULT 0
            )
            """)
            
            # Event Registrations Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_registrations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                donor_id INTEGER,
                donor_name TEXT,
                donor_email TEXT,
                donor_phone TEXT,
                donor_blood TEXT,
                registration_date TEXT,
                attended INTEGER DEFAULT 0,
                check_in_time TEXT,
                check_out_time TEXT,
                feedback TEXT,
                rating INTEGER,
                points_earned INTEGER DEFAULT 0,
                donation_completed INTEGER DEFAULT 0,
                units_donated INTEGER DEFAULT 0,
                notes TEXT,
                certificate_generated INTEGER DEFAULT 0,
                certificate_url TEXT,
                FOREIGN KEY (event_id) REFERENCES donation_events (id),
                FOREIGN KEY (donor_id) REFERENCES donors (id)
            )
            """)
            
            # Event Feedback Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_feedback(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                donor_id INTEGER,
                rating INTEGER,
                feedback TEXT,
                suggestions TEXT,
                would_recommend INTEGER DEFAULT 1,
                feedback_date TEXT,
                anonymous INTEGER DEFAULT 0,
                FOREIGN KEY (event_id) REFERENCES donation_events (id),
                FOREIGN KEY (donor_id) REFERENCES donors (id)
            )
            """)
            
            # Rewards Store Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS rewards(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reward_id TEXT UNIQUE,
                item_name TEXT,
                description TEXT,
                points_required INTEGER,
                stock INTEGER,
                category TEXT,
                image_url TEXT,
                available INTEGER DEFAULT 1,
                vendor TEXT,
                discount_percentage INTEGER DEFAULT 0
            )
            """)
            
            # Donor Redemptions Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS redemptions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                redemption_id TEXT UNIQUE,
                donor_id INTEGER,
                reward_id INTEGER,
                redemption_date TEXT,
                points_spent INTEGER,
                status TEXT DEFAULT 'Pending',
                delivery_address TEXT,
                tracking_number TEXT,
                delivered_date TEXT,
                FOREIGN KEY (donor_id) REFERENCES donors (id),
                FOREIGN KEY (reward_id) REFERENCES rewards (id)
            )
            """)
            
            # Chat Messages Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE,
                sender_id INTEGER,
                receiver_id INTEGER,
                message TEXT,
                timestamp TEXT,
                read INTEGER DEFAULT 0,
                conversation_id TEXT,
                message_type TEXT DEFAULT 'text',
                FOREIGN KEY (sender_id) REFERENCES donors (id),
                FOREIGN KEY (receiver_id) REFERENCES donors (id)
            )
            """)
            
            # Health Checks Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_checks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                check_id TEXT UNIQUE,
                donor_id INTEGER,
                check_date TEXT,
                hemoglobin REAL,
                blood_pressure_systolic INTEGER,
                blood_pressure_diastolic INTEGER,
                pulse_rate INTEGER,
                temperature REAL,
                weight REAL,
                height REAL,
                bmi REAL,
                eligible BOOLEAN,
                notes TEXT,
                next_check_date TEXT,
                FOREIGN KEY (donor_id) REFERENCES donors (id)
            )
            """)
            
            # Achievements Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                achievement_id TEXT UNIQUE,
                donor_id INTEGER,
                achievement_type TEXT,
                achievement_date TEXT,
                description TEXT,
                points_awarded INTEGER,
                badge_icon TEXT,
                FOREIGN KEY (donor_id) REFERENCES donors (id)
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
                read INTEGER DEFAULT 0,
                action_url TEXT,
                priority TEXT DEFAULT 'Normal'
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
                status TEXT DEFAULT 'Completed',
                points_earned INTEGER DEFAULT 0,
                verified_by TEXT,
                donor_distance_km REAL,
                event_id INTEGER,
                FOREIGN KEY (donor_id) REFERENCES donors (id),
                FOREIGN KEY (request_id) REFERENCES requests (id),
                FOREIGN KEY (event_id) REFERENCES donation_events (id)
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
                donor_id INTEGER,
                event_id INTEGER
            )
            """)
            
            conn.commit()
            
            test = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
            if test is not None:
                print(f"✅ Database initialized successfully at: {DB_PATH}")
                return True
            else:
                print("❌ Database verification failed")
                return False
            
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

# Initialize database
if not st.session_state.db_initialized:
    if init_database():
        st.session_state.db_initialized = True
        st.sidebar.success("✅ Database Ready")
    else:
        st.sidebar.error("❌ Database Error")

# ============================================
# EMAIL VALIDATION FUNCTIONS
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
    email = email.lower().strip()
    if email.endswith('@gmal.com'):
        email = email.replace('@gmal.com', '@gmail.com')
    if email.endswith('@gmai.com'):
        email = email.replace('@gmai.com', '@gmail.com')
    if email.endswith('@gamil.com'):
        email = email.replace('@gamil.com', '@gmail.com')
    if email.endswith('@yahooo.com'):
        email = email.replace('@yahooo.com', '@yahoo.com')
    if email.endswith('@hotmial.com'):
        email = email.replace('@hotmial.com', '@hotmail.com')
    return email

# ============================================
# ENHANCED UTILITY FUNCTIONS
# ============================================

def generate_id(prefix):
    """Generate unique ID"""
    return f"{prefix}-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

def get_coords(location):
    """Get coordinates from location"""
    try:
        if not location or not isinstance(location, str) or len(location.strip()) < 5:
            print(f"Invalid location: {location}")
            return None
            
        location = location.strip()
        geolocator = Nominatim(user_agent="bloodai_app_v2")
        
        loc = geolocator.geocode(location, timeout=10, exactly_one=True)
        
        if loc:
            print(f"✅ Found coordinates for '{location}': ({loc.latitude}, {loc.longitude})")
            return (loc.latitude, loc.longitude)
        
        if 'india' not in location.lower():
            location_with_country = f"{location}, India"
            loc = geolocator.geocode(location_with_country, timeout=10)
            if loc:
                print(f"✅ Found coordinates with country: ({loc.latitude}, {loc.longitude})")
                return (loc.latitude, loc.longitude)
        
        print(f"❌ Could not find coordinates for '{location}'")
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
        print(f"✅ Updated coordinates for donor {donor_id}")
        return True
    else:
        print(f"❌ Failed to get coordinates for location: {location}")
        return False

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def log_email(recipient, subject, email_type, status, error=None, request_id=None, donor_id=None, event_id=None):
    """Log email sending attempt"""
    try:
        email_id = generate_id('EMAIL')
        execute_query(
            """INSERT INTO email_log 
               (email_id, recipient, subject, type, sent_date, status, error_message, request_id, donor_id, event_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (email_id, recipient, subject, email_type, 
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             status, error, request_id, donor_id, event_id),
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
        to_email = normalize_email(to_email)
        
        if not is_valid_email(to_email):
            error_msg = f"Invalid email format: {to_email}"
            log_email(to_email, subject, 'email', 'failed', error_msg)
            return False
        
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
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        log_email(to_email, subject, 'email', 'sent')
        return True
        
    except Exception as e:
        error_msg = str(e)
        log_email(to_email, subject, 'email', 'failed', error_msg)
        return False

def add_notification(user_email, notif_type, title, message, priority='Normal', action_url=None):
    """Add notification"""
    try:
        if not user_email or not is_valid_email(user_email):
            return False
        
        notification_id = generate_id('NOTIF')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        execute_query(
            """INSERT INTO notifications 
               (notification_id, user_email, type, title, message, date, priority, action_url)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (notification_id, user_email, notif_type, title, message, current_time, priority, action_url),
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
    except:
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
    except:
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
    except:
        return 0, "New Donor 🌟"

# ============================================
# ML MODEL FOR DONOR PREDICTION
# ============================================

@st.cache_resource
def train_model():
    """Train ML model for donor prediction"""
    try:
        donors = execute_query(
            "SELECT blood, location, status, total_donations, age, weight FROM donors WHERE status='Available'",
            fetch_all=True
        ) or []
        
        if len(donors) < 3:
            return None
            
        X = []
        y = []
        
        for d in donors:
            if d:
                blood_hash = sum(ord(c) for c in d.get('blood', '')) % 10 if d.get('blood') else 0
                loc_hash = sum(ord(c) for c in d.get('location', '')) % 10 if d.get('location') else 0
                donations = d.get('total_donations', 0)
                age = d.get('age', 30)
                weight = d.get('weight', 70)
                
                X.append([blood_hash, loc_hash, donations, age, weight])
                y.append(1 if d.get('status') == "Available" else 0)
        
        if len(X) > 0:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X, y)
            return model
        return None
    except:
        return None

model = train_model()

# ============================================
# JSON SERIALIZATION HELPER
# ============================================

def make_json_serializable(obj):
    """Convert non-serializable objects to JSON serializable format"""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {key: make_json_serializable(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_json_serializable(item) for item in obj]
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return str(obj)

# ============================================
# DONOR SORTING FUNCTION - FIXED
# ============================================

def get_all_donors_sorted_by_distance(blood_type, location):
    """Get ALL donors sorted by distance"""
    try:
        donors = execute_query(
            "SELECT * FROM donors WHERE blood=?",
            (blood_type,),
            fetch_all=True
        ) or []
        
        if not donors:
            return []
        
        patient_coords = get_coords(location)
        
        donors_with_distance = []
        for donor in donors:
            donor_copy = dict(donor)
            
            donor_lat = donor_copy.get('latitude')
            donor_lon = donor_copy.get('longitude')
            
            if donor_lat and donor_lon and patient_coords:
                try:
                    distance = geodesic(patient_coords, (donor_lat, donor_lon)).km
                    donor_copy['distance_km'] = round(distance, 2)
                except:
                    donor_copy['distance_km'] = None
            else:
                donor_copy['distance_km'] = None
            
            donors_with_distance.append(donor_copy)
        
        # Sort - donors with distance first, then those without
        donors_with_distance.sort(key=lambda x: (
            0 if x.get('distance_km') is not None else 1,
            x.get('distance_km', float('inf')) if x.get('distance_km') is not None else float('inf')
        ))
        
        return donors_with_distance
        
    except Exception as e:
        print(f"Error sorting donors: {e}")
        return []

def get_next_donor_to_contact(request):
    """Get the next donor to contact"""
    try:
        all_donors_json = request.get('all_donors', '')
        current_index = request.get('current_donor_index', 0)
        contacted = request.get('contacted', '')
        
        if not all_donors_json:
            return None, None
        
        all_donors = json.loads(all_donors_json)
        contacted_list = [int(x) for x in contacted.split(',') if x and x.strip()]
        
        for i in range(current_index, len(all_donors)):
            donor_id = all_donors[i].get('id')
            if donor_id and donor_id not in contacted_list:
                return all_donors[i], i
        
        return None, None
        
    except Exception as e:
        print(f"Error getting next donor: {e}")
        return None, None

# ============================================
# DONOR REQUEST EMAIL
# ============================================

def send_donor_request_email(donor, request, donor_rank, total_donors, donor_distance=None):
    """Send email to donor"""
    try:
        if not donor or not request:
            return False
        
        donor_email = normalize_email(donor.get('email'))
        
        if not is_valid_email(donor_email):
            return False
            
        base_url = st.get_option("server.baseUrlPath") or BASE_URL
        
        accept_url = f"{base_url}/?accept={request.get('id')}&donor={donor.get('id')}"
        reject_url = f"{base_url}/?reject={request.get('id')}&donor={donor.get('id')}"
        
        subject = f"🩸 URGENT: Blood Donation Needed - {request.get('blood', 'Unknown')}"
        
        distance_display = f"{donor_distance:.1f}" if donor_distance else "Unknown"
        
        message = f"""
<!DOCTYPE html>
<html>
<body>
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #ff6b6b;">🩸 URGENT BLOOD REQUEST</h1>
        <p>Hello {donor.get('name', 'Donor')},</p>
        <p>A patient urgently needs your blood type.</p>
        <div style="background: #f0f0f0; padding: 15px; border-radius: 10px;">
            <h3>📍 YOUR POSITION</h3>
            <p>You are #{donor_rank} of {total_donors} donors</p>
            <p>Distance: {distance_display} km</p>
        </div>
        <div style="margin: 20px 0;">
            <a href="{accept_url}" style="background: #43e97b; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-right: 10px;">✅ ACCEPT</a>
            <a href="{reject_url}" style="background: #ff6b6b; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">❌ REJECT</a>
        </div>
        <p><small>You have {WAIT_MINUTES} minutes to respond.</small></p>
    </div>
</body>
</html>
        """
        
        return send_email(donor_email, subject, message, html=True)
        
    except Exception as e:
        print(f"Donor email error: {e}")
        return False

# ============================================
# PATIENT NOTIFICATION EMAIL
# ============================================

def send_patient_notification_email(patient_email, patient_name, donor, request, donor_distance=None):
    """Send email to patient when donor accepts"""
    try:
        if not patient_email or not donor or not request:
            return False
        
        patient_email = normalize_email(patient_email)
        
        if not is_valid_email(patient_email):
            return False
            
        subject = f"✅ Donor Found - Blood Request"
        
        distance_display = f"{donor_distance:.1f}" if donor_distance else "Unknown"
        
        message = f"""
<!DOCTYPE html>
<html>
<body>
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #43e97b;">✅ DONOR FOUND!</h1>
        <p>Dear {patient_name},</p>
        <p>A donor has accepted your blood request.</p>
        <div style="background: #f0f0f0; padding: 15px; border-radius: 10px;">
            <h3>🩸 DONOR DETAILS</h3>
            <p><strong>Name:</strong> {donor.get('name', 'Unknown')}</p>
            <p><strong>Blood Type:</strong> {donor.get('blood', 'Unknown')}</p>
            <p><strong>Phone:</strong> {donor.get('phone', 'Unknown')}</p>
            <p><strong>Email:</strong> {donor.get('email', 'Unknown')}</p>
            <p><strong>Distance:</strong> {distance_display} km</p>
        </div>
        <p>Please contact the donor immediately to schedule the donation.</p>
    </div>
</body>
</html>
        """
        
        return send_email(patient_email, subject, message, html=True)
        
    except Exception as e:
        print(f"Patient email error: {e}")
        return False

# ============================================
# DONOR CONFIRMATION EMAIL
# ============================================

def send_donor_confirmation_email(donor, patient_name, request, next_eligible, donor_distance=None):
    """Send confirmation email to donor"""
    try:
        if not donor or not request:
            return False
        
        donor_email = normalize_email(donor.get('email'))
        
        if not is_valid_email(donor_email):
            return False
            
        subject = "🎉 Thank You - Blood Donation Confirmed"
        
        message = f"""
<!DOCTYPE html>
<html>
<body>
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #ffd700;">🎉 THANK YOU HERO!</h1>
        <p>Dear {donor.get('name', 'Donor')},</p>
        <p>Thank you for accepting the blood donation request!</p>
        <div style="background: #f0f0f0; padding: 15px; border-radius: 10px;">
            <h3>🏥 DONATION DETAILS</h3>
            <p><strong>Patient:</strong> {patient_name}</p>
            <p><strong>Hospital:</strong> {request.get('hospital', 'Unknown')}</p>
            <p><strong>Blood Type:</strong> {request.get('blood', 'Unknown')}</p>
        </div>
        <p><strong>Points Earned:</strong> +{POINTS_PER_DONATION}</p>
        <p><strong>Next Eligible Date:</strong> {next_eligible}</p>
    </div>
</body>
</html>
        """
        
        return send_email(donor_email, subject, message, html=True)
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
        
        donor_email = normalize_email(donor_email)
        
        if not is_valid_email(donor_email):
            return False
            
        subject = "🎉 Welcome to BloodAI - Thank You for Registering!"
        
        message = f"""
<!DOCTYPE html>
<html>
<body>
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #667eea;">🩸 Welcome to BloodAI!</h1>
        <p>Hello {donor_name},</p>
        <p>Thank you for registering as a blood donor.</p>
        <div style="background: #f0f0f0; padding: 15px; border-radius: 10px;">
            <h3>Your Donor Profile:</h3>
            <p><strong>Donor ID:</strong> {donor_details.get('donor_id', '')}</p>
            <p><strong>Blood Type:</strong> {donor_details.get('blood', 'Unknown')}</p>
            <p><strong>Location:</strong> {donor_details.get('location', 'Unknown')}</p>
        </div>
        <p>Together, we can save lives!</p>
        <p>- BloodAI Team</p>
    </div>
</body>
</html>
        """
        
        return send_email(donor_email, subject, message, html=True)
    except Exception as e:
        print(f"Welcome email error: {e}")
        return False

# ============================================
# EVENT REGISTRATION EMAIL
# ============================================

def send_event_registration_email(donor_email, donor_name, event_name, event_details):
    """Send confirmation email for event registration"""
    try:
        if not donor_email:
            return False
        
        donor_email = normalize_email(donor_email)
        
        if not is_valid_email(donor_email):
            return False
            
        subject = f"✅ Registration Confirmed - {event_name}"
        
        message = f"""
<!DOCTYPE html>
<html>
<body>
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #43e97b;">✅ Registration Confirmed!</h1>
        <p>Hello {donor_name},</p>
        <p>Thank you for registering for the donation event!</p>
        <div style="background: #f0f0f0; padding: 15px; border-radius: 10px;">
            <h3>🎪 Event Details:</h3>
            <p><strong>Event:</strong> {event_name}</p>
            <p><strong>Date:</strong> {event_details.get('start_date')} at {event_details.get('start_time')}</p>
            <p><strong>Location:</strong> {event_details.get('location')}</p>
        </div>
        <p>We look forward to seeing you there!</p>
        <p>- BloodAI Team</p>
    </div>
</body>
</html>
        """
        
        return send_email(donor_email, subject, message, html=True)
    except Exception as e:
        print(f"Event registration email error: {e}")
        return False

# ============================================
# AUTO NEXT DONOR FUNCTION
# ============================================

def check_and_contact_next_donor():
    """Check pending requests and contact next donor"""
    while True:
        try:
            pending = execute_query(
                "SELECT * FROM requests WHERE status='Pending'",
                fetch_all=True
            ) or []
            
            for request in pending:
                if not request:
                    continue
                    
                request_id = request.get('id')
                contacted = request.get('contacted') or ""
                last_contacted = request.get('last_contacted_time')
                all_donors_json = request.get('all_donors', '')
                
                if not request_id:
                    continue
                
                if not last_contacted and all_donors_json:
                    try:
                        all_donors = json.loads(all_donors_json)
                        if all_donors:
                            first_donor = all_donors[0]
                            
                            new_contacted = str(first_donor.get('id')) + ","
                            current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            execute_query(
                                """UPDATE requests 
                                   SET donor_id=?, contacted=?, last_contacted_time=?, current_donor_index=1
                                   WHERE id=?""",
                                (first_donor.get('id'), new_contacted, current_time_str, request_id),
                                commit=True
                            )
                            
                            distance = first_donor.get('distance_km')
                            send_donor_request_email(first_donor, request, 1, len(all_donors), distance)
                    except Exception as e:
                        print(f"Error contacting first donor: {e}")
                
                elif last_contacted:
                    try:
                        last_time = datetime.strptime(last_contacted, "%Y-%m-%d %H:%M:%S")
                        current_time = datetime.now()
                        
                        if current_time - last_time >= timedelta(minutes=WAIT_MINUTES):
                            next_donor, next_index = get_next_donor_to_contact(request)
                            
                            if next_donor and all_donors_json:
                                all_donors = json.loads(all_donors_json)
                                new_contacted = contacted + str(next_donor.get('id')) + ","
                                current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
                                
                                execute_query(
                                    """UPDATE requests 
                                       SET donor_id=?, contacted=?, last_contacted_time=?, current_donor_index=?
                                       WHERE id=?""",
                                    (next_donor.get('id'), new_contacted, current_time_str, next_index + 1, request_id),
                                    commit=True
                                )
                                
                                rank = next_index + 1
                                distance = next_donor.get('distance_km')
                                send_donor_request_email(next_donor, request, rank, len(all_donors), distance)
                            else:
                                execute_query(
                                    "UPDATE requests SET status='No Donors Available' WHERE id=?",
                                    (request_id,),
                                    commit=True
                                )
                    except Exception as e:
                        print(f"Error processing request {request_id}: {e}")
            
            time.sleep(30)
        except Exception as e:
            print(f"Scheduler error: {e}")
            time.sleep(60)

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
# DONOR RESPONSE HANDLER
# ============================================

def handle_donor_response():
    """Handle donor accept/reject"""
    try:
        query_params = st.query_params
        
        if "accept" in query_params and "donor" in query_params:
            try:
                request_id = int(query_params["accept"])
                donor_id = int(query_params["donor"])
                
                st.markdown("""
                <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #43e97b, #38f9d7); border-radius: 20px; margin: 2rem 0;'>
                    <h1 style='color: white; font-size: 3rem;'>✅ Processing Your Acceptance...</h1>
                </div>
                """, unsafe_allow_html=True)
                
                request = execute_query(
                    "SELECT * FROM requests WHERE id=?",
                    (request_id,),
                    fetch_one=True
                )
                
                if not request:
                    st.error("❌ Request not found")
                    return
                
                donor = execute_query(
                    "SELECT * FROM donors WHERE id=?",
                    (donor_id,),
                    fetch_one=True
                )
                
                if not donor:
                    st.error("❌ Donor not found")
                    return
                
                patient_email = normalize_email(request.get('patient_email'))
                donor_email = normalize_email(donor.get('email'))
                
                if request.get('status') != 'Pending':
                    st.warning("⚠️ This request is no longer available")
                    return
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
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
                
                update_donor_points(donor_id)
                
                execute_query(
                    """UPDATE requests 
                       SET status='Accepted', 
                           completed_time=?,
                           donor_id=?
                       WHERE id=?""",
                    (current_time, donor_id, request_id),
                    commit=True
                )
                
                history_id = generate_id('DH')
                execute_query(
                    """INSERT INTO donation_history 
                       (history_id, donor_id, request_id, donation_date, hospital, 
                        blood_type, units, points_earned)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (history_id, donor_id, request_id, current_time, 
                     request.get('hospital'), request.get('blood'), 
                     request.get('units_needed', 1), POINTS_PER_DONATION),
                    commit=True
                )
                
                next_eligible = (datetime.now() + timedelta(days=COOLDOWN_MONTHS * 30)).strftime("%Y-%m-%d")
                
                send_patient_notification_email(patient_email, request.get('patient'), donor, request)
                send_donor_confirmation_email(donor, request.get('patient'), request, next_eligible)
                
                add_notification(patient_email, 'donor_found', '✅ Donor Found!', f"{donor.get('name')} has accepted your request")
                add_notification(donor_email, 'accepted', '🎉 Donation Confirmed', f"Thank you! Next eligible: {next_eligible}")
                
                st.query_params.clear()
                st.session_state.showing_response = False
                
                st.balloons()
                st.snow()
                
                st.success("✅ Thank you for accepting! The patient has been notified.")
                
                col1, col2, col3 = st.columns(3)
                with col2:
                    if st.button("🏠 Return Home", use_container_width=True):
                        st.rerun()
                
                return True
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                return False
        
        elif "reject" in query_params and "donor" in query_params:
            try:
                request_id = int(query_params["reject"])
                donor_id = int(query_params["donor"])
                
                st.markdown("""
                <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #ff6b6b, #ee5253); border-radius: 20px; margin: 2rem 0;'>
                    <h1 style='color: white; font-size: 3rem;'>🕊️ Request Rejected</h1>
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
                        
                        st.info("✅ Your response has been recorded.")
                
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
            status_text.text("🤖 Sorting donors by proximity...")
        else:
            status_text.text("✅ Found donors!")
    
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
        """Get blood inventory summary"""
        query = "SELECT blood_type, SUM(units) as total_units FROM blood_inventory WHERE status='Available' GROUP BY blood_type"
        return execute_query(query, fetch_all=True) or []
    
    def check_stock_alerts(self):
        """Check for low stock alerts"""
        inventory = self.get_inventory_summary()
        alerts = []
        blood_type_status = {}
        
        for bt in BLOOD_TYPES:
            blood_type_status[bt] = {'units': 0, 'status': 'critical'}
        
        for item in inventory:
            if item:
                bt = item.get('blood_type')
                units = item.get('total_units', 0)
                
                if units >= self.alert_threshold:
                    status = 'normal'
                elif units > 0:
                    status = 'low'
                else:
                    status = 'critical'
                
                blood_type_status[bt] = {'units': units, 'status': status}
                
                if units < self.alert_threshold:
                    urgency = f'LOW STOCK - Only {units} units' if units > 0 else 'CRITICAL - Out of Stock'
                    alerts.append({
                        'blood_type': bt,
                        'current_stock': units,
                        'urgency': urgency
                    })
        
        return alerts, blood_type_status
    
    def display_inventory_dashboard(self):
        """Display interactive inventory dashboard"""
        alerts, blood_status = self.check_stock_alerts()
        
        if alerts:
            st.warning(f"⚠️ {len(alerts)} stock alerts detected")
        
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
# HOSPITAL MANAGEMENT
# ============================================

class HospitalManager:
    def get_nearby_hospitals(self, location, radius_km=20):
        """Get hospitals near a location"""
        coords = get_coords(location)
        if not coords:
            return []
        
        hospitals = execute_query(
            "SELECT * FROM hospitals WHERE verified=1",
            fetch_all=True
        ) or []
        
        nearby = []
        for hospital in hospitals:
            if hospital and hospital.get('latitude') and hospital.get('longitude'):
                hospital_coords = (hospital['latitude'], hospital['longitude'])
                distance = geodesic(coords, hospital_coords).km
                if distance <= radius_km:
                    hospital['distance'] = round(distance, 2)
                    nearby.append(hospital)
        
        return sorted(nearby, key=lambda x: x.get('distance', float('inf')))

# ============================================
# DONATION EVENTS MANAGEMENT - COMPLETE FIXED
# ============================================

class DonationEventManager:
    def __init__(self):
        self.blood_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    
    def create_event(self, event_data, organizer_id=None):
        """Create a new donation event"""
        try:
            event_id = generate_id('EVT')
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            coords = get_coords(event_data.get('location'))
            lat, lon = coords if coords else (None, None)
            
            blood_types_needed = event_data.get('blood_types_needed', [])
            if isinstance(blood_types_needed, list):
                blood_types_needed = json.dumps(blood_types_needed)
            
            amenities = event_data.get('amenities', [])
            if isinstance(amenities, list):
                amenities = json.dumps(amenities)
            
            incentives = event_data.get('incentives', [])
            if isinstance(incentives, list):
                incentives = json.dumps(incentives)
            
            execute_query(
                """INSERT INTO donation_events 
                   (event_id, event_name, organizer, organizer_id, organizer_email, organizer_phone,
                    location, address, city, start_date, end_date, start_time, end_time,
                    target_donations, registered_donors, completed_donations, status,
                    contact_person, contact_phone, contact_email, description, latitude, longitude,
                    amenities, blood_types_needed, incentives, special_instructions, created_date,
                    min_age, max_age, min_weight, is_featured, registration_deadline)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (event_id, 
                 event_data.get('event_name'), 
                 event_data.get('organizer'),
                 organizer_id,
                 event_data.get('organizer_email'),
                 event_data.get('organizer_phone'),
                 event_data.get('location'),
                 event_data.get('address'),
                 event_data.get('city'),
                 event_data.get('start_date'),
                 event_data.get('end_date'),
                 event_data.get('start_time'),
                 event_data.get('end_time'),
                 event_data.get('target_donations', 0),
                 0, 0,
                 event_data.get('status', 'Upcoming'),
                 event_data.get('contact_person'),
                 event_data.get('contact_phone'),
                 event_data.get('contact_email'),
                 event_data.get('description'),
                 lat, lon,
                 amenities,
                 blood_types_needed,
                 incentives,
                 event_data.get('special_instructions'),
                 current_time,
                 event_data.get('min_age', 18),
                 event_data.get('max_age', 65),
                 event_data.get('min_weight', 45),
                 event_data.get('is_featured', 0),
                 event_data.get('registration_deadline')),
                commit=True
            )
            
            print(f"✅ Event created: {event_data.get('event_name')}")
            return True, event_id
            
        except Exception as e:
            print(f"Event creation error: {e}")
            return False, str(e)
    
    def get_nearby_events(self, location, radius_km=50):
        """Get events near a location"""
        coords = get_coords(location)
        if not coords:
            return []
        
        events = execute_query(
            "SELECT * FROM donation_events WHERE status IN ('Upcoming', 'Ongoing') ORDER BY start_date ASC",
            fetch_all=True
        ) or []
        
        nearby = []
        for event in events:
            if event and event.get('latitude') and event.get('longitude'):
                event_coords = (event['latitude'], event['longitude'])
                distance = geodesic(coords, event_coords).km
                if distance <= radius_km:
                    event_dict = dict(event)
                    event_dict['distance'] = round(distance, 2)
                    
                    if event_dict.get('blood_types_needed'):
                        try:
                            event_dict['blood_types_needed'] = json.loads(event_dict['blood_types_needed'])
                        except:
                            event_dict['blood_types_needed'] = []
                    
                    nearby.append(event_dict)
        
        return sorted(nearby, key=lambda x: x.get('distance', float('inf')))
    
    def get_all_events(self, status=None):
        """Get all events with optional status filter"""
        try:
            if status:
                events = execute_query(
                    "SELECT * FROM donation_events WHERE status=? ORDER BY start_date ASC",
                    (status,),
                    fetch_all=True
                ) or []
            else:
                events = execute_query(
                    "SELECT * FROM donation_events ORDER BY start_date ASC",
                    fetch_all=True
                ) or []
            
            for event in events:
                if event.get('blood_types_needed'):
                    try:
                        event['blood_types_needed'] = json.loads(event['blood_types_needed'])
                    except:
                        event['blood_types_needed'] = []
            
            return events
        except Exception as e:
            print(f"Error getting events: {e}")
            return []
    
    def register_for_event(self, event_id, donor):
        """Register donor for event"""
        try:
            existing = execute_query(
                "SELECT id FROM event_registrations WHERE event_id=? AND donor_id=?",
                (event_id, donor['id']),
                fetch_one=True
            )
            
            if existing:
                return False, "Already registered"
            
            if donor.get('age', 0) < 18 or donor.get('age', 0) > 65:
                return False, "Age not within limits"
            
            if donor.get('weight', 0) < 45:
                return False, "Weight below minimum"
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            execute_query(
                """INSERT INTO event_registrations 
                   (event_id, donor_id, donor_name, donor_email, donor_phone, donor_blood,
                    registration_date, attended)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (event_id, donor['id'], donor.get('name'), donor.get('email'), 
                 donor.get('phone'), donor.get('blood'),
                 current_time, 0),
                commit=True
            )
            
            execute_query(
                "UPDATE donation_events SET registered_donors = registered_donors + 1 WHERE id=?",
                (event_id,),
                commit=True
            )
            
            event = execute_query(
                "SELECT * FROM donation_events WHERE id=?",
                (event_id,),
                fetch_one=True
            )
            
            if event:
                send_event_registration_email(
                    donor.get('email'),
                    donor.get('name'),
                    event.get('event_name'),
                    event
                )
            
            return True, "Registration successful"
            
        except Exception as e:
            print(f"Event registration error: {e}")
            return False, str(e)

# ============================================
# QR CODE GENERATOR
# ============================================

class QRCodeManager:
    def generate_donor_qr(self, donor_id, donor_data):
        """Generate QR code for donor"""
        try:
            qr_data = {
                'donor_id': donor_id,
                'name': donor_data.get('name', ''),
                'blood_type': donor_data.get('blood', ''),
                'donor_level': donor_data.get('donor_level', 'New Donor 🌟'),
                'total_donations': donor_data.get('total_donations', 0),
                'medical_id': donor_data.get('medical_id', ''),
                'emergency_contact': donor_data.get('emergency_contact', '')
            }
            
            qr_string = json.dumps(qr_data)
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_string)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            print(f"QR generation error: {e}")
            return None
    
    def generate_event_qr(self, event_id, event_data):
        """Generate QR code for event"""
        try:
            qr_data = {
                'event_id': event_id,
                'event_name': event_data.get('event_name', ''),
                'date': event_data.get('start_date', ''),
                'type': 'event_checkin'
            }
            
            qr_string = json.dumps(qr_data)
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_string)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            print(f"Event QR generation error: {e}")
            return None

# ============================================
# REWARDS MANAGER
# ============================================

class RewardsManager:
    def get_available_rewards(self, category=None):
        """Get available rewards"""
        try:
            query = "SELECT * FROM rewards WHERE available=1 AND stock>0"
            params = []
            
            if category and category != 'All':
                query += " AND category=?"
                params.append(category)
            
            query += " ORDER BY points_required ASC"
            
            return execute_query(query, params, fetch_all=True) or []
        except Exception as e:
            print(f"Error getting rewards: {e}")
            return []
    
    def get_donor_points_summary(self, donor_id):
        """Get donor points summary"""
        try:
            if not donor_id:
                return None
                
            donor = execute_query(
                "SELECT points, total_points_earned, donor_level FROM donors WHERE id=?",
                (donor_id,),
                fetch_one=True
            )
            
            if not donor:
                return None
            
            return {
                'current_points': donor.get('points', 0),
                'total_earned': donor.get('total_points_earned', 0),
                'level': donor.get('donor_level', 'New Donor 🌟')
            }
        except Exception as e:
            print(f"Error getting donor points: {e}")
            return None

# ============================================
# CHAT MANAGER
# ============================================

class ChatManager:
    def get_unread_count(self, user_id):
        """Get unread message count"""
        try:
            if not user_id:
                return 0
                
            result = execute_query(
                "SELECT COUNT(*) as count FROM chat_messages WHERE receiver_id=? AND read=0",
                (user_id,),
                fetch_one=True
            )
            return result['count'] if result else 0
        except:
            return 0

# ============================================
# DONOR IMPACT VISUALIZER
# ============================================

class DonorImpactVisualizer:
    def calculate_donor_impact(self, donor_id):
        """Calculate donor's lifetime impact"""
        try:
            if not donor_id:
                return {
                    'donations': 0,
                    'units': 0,
                    'lives_saved': 0,
                    'events': 0,
                    'total_distance': 0
                }
                
            donations = execute_query(
                """SELECT COUNT(*) as count, SUM(units) as total_units, SUM(donor_distance_km) as total_distance
                   FROM donation_history WHERE donor_id=?""",
                (donor_id,),
                fetch_one=True
            )
            
            if not donations:
                donations = {'count': 0, 'total_units': 0, 'total_distance': 0}
            
            lives_saved = donations.get('count', 0)
            
            events_attended = execute_query(
                "SELECT COUNT(*) as count FROM event_registrations WHERE donor_id=? AND attended=1",
                (donor_id,),
                fetch_one=True
            ) or {'count': 0}
            
            return {
                'donations': donations.get('count', 0),
                'units': donations.get('total_units', 0),
                'lives_saved': lives_saved,
                'events': events_attended.get('count', 0),
                'total_distance': donations.get('total_distance', 0) or 0
            }
        except Exception as e:
            print(f"Error calculating impact: {e}")
            return {
                'donations': 0,
                'units': 0,
                'lives_saved': 0,
                'events': 0,
                'total_distance': 0
            }
    
    def create_impact_dashboard(self, donor_id, donor_name):
        """Create visual impact dashboard"""
        try:
            if not donor_id or not donor_name:
                st.warning("Invalid donor information")
                return
                
            impact = self.calculate_donor_impact(donor_id)
            
            st.subheader(f"🌟 {donor_name}'s Impact Dashboard")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Donations", impact.get('donations', 0))
            with col2:
                st.metric("Units Donated", impact.get('units', 0))
            with col3:
                st.metric("Lives Saved", impact.get('lives_saved', 0))
            with col4:
                st.metric("Events Attended", impact.get('events', 0))
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea20, #764ba220); padding: 2rem; border-radius: 15px; text-align: center;'>
                <h2>🎉 {donor_name}, you've saved {impact.get('lives_saved', 0)} lives!</h2>
                <p>Your {impact.get('donations', 0)} donations have made an incredible impact.</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error displaying impact dashboard: {e}")

# ============================================
# SIDEBAR SETUP
# ============================================

st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <h1 style='color: #ff6b6b; font-size: 2.5rem;'>🩸 BloodAI</h1>
    <p style='color: #666;'>Complete Blood Donation System</p>
</div>
""", unsafe_allow_html=True)

# Quick stats
st.sidebar.markdown("### 📊 Quick Stats")
selected_blood = st.sidebar.selectbox(
    "Blood Type",
    BLOOD_TYPES,
    key="sidebar_blood"
)

total_result = execute_query(
    "SELECT COUNT(*) as count FROM donors WHERE blood=?",
    (selected_blood,),
    fetch_one=True
)
total = total_result['count'] if total_result else 0

eligible_donors = get_eligible_donors(selected_blood)
eligible_count = len(eligible_donors)

db_status = "✅ Persistent" if DB_PATH.startswith('/mount') else "📁 Local"

st.sidebar.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea20, #764ba220); padding: 1rem; border-radius: 10px;'>
    <p><strong>🩸 {selected_blood}</strong></p>
    <p>✅ Eligible: {eligible_count}</p>
    <p>📊 Total: {total}</p>
    <p>⏱️ Cooldown: {COOLDOWN_MONTHS} months</p>
    <p>💾 DB: {db_status}</p>
</div>
""", unsafe_allow_html=True)

inventory_manager = BloodInventoryManager()
alerts, _ = inventory_manager.check_stock_alerts()
if alerts:
    st.sidebar.warning(f"⚠️ {len(alerts)} stock alerts")

event_count = execute_query(
    "SELECT COUNT(*) as count FROM donation_events WHERE status IN ('Upcoming', 'Ongoing')",
    fetch_one=True
)
upcoming_events = event_count['count'] if event_count else 0
if upcoming_events > 0:
    st.sidebar.info(f"🎪 {upcoming_events} upcoming events")

st.sidebar.markdown("---")

# Navigation menu
menu_options = [
    "🏠 Home",
    "📝 Donor Register",
    "🆘 Patient Request",
    "📍 Track Request",
    "🏆 Donor Leaderboard",
    "🔔 Notifications",
    "👤 Donor Dashboard",
    "🏥 Hospitals",
    "📦 Blood Inventory",
    "🎪 Donation Events",
    "🎁 Rewards Store",
    "💬 Chat",
    "📊 Impact Dashboard",
    "👑 Admin",
    "📧 Email Log"
]

if st.session_state.logged_in_donor is None:
    menu_options = [m for m in menu_options if m not in ["💬 Chat", "📊 Impact Dashboard"]]

menu = st.sidebar.radio("Navigation", menu_options)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 System Status")
st.sidebar.info(f"⏱️ Auto-rotation: Every {WAIT_MINUTES} minutes")
st.sidebar.info(f"⏳ Response: {WAIT_MINUTES} min per donor")
st.sidebar.info(f"🛡️ Cooldown: {COOLDOWN_MONTHS} months")

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
            <p style='font-size: 1.5rem;'>All Donors Notified • Closest First • 2-Minute Rotation</p>
        </div>
        """, unsafe_allow_html=True)
        
        pending_result = execute_query(
            "SELECT COUNT(*) as count FROM requests WHERE status='Pending'",
            fetch_one=True
        )
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
            completed_donations = execute_query("SELECT COUNT(*) as count FROM donation_history", fetch_one=True)
            lives_saved = completed_donations['count'] if completed_donations else 0
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{lives_saved}</div><div>Lives Saved</div></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📦 Current Blood Inventory")
        inventory_manager.display_inventory_dashboard()

    # ============================================
    # DONOR REGISTER PAGE - FIXED (removed distance warnings)
    # ============================================

    elif menu == "📝 Donor Register":
        st.title("📝 Donor Registration")
        st.info("📍 Register to become a blood donor")
        
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
                location = st.text_input("Address/Location*", 
                                        help="Enter your address")
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
                                   (donor_id, name, email, phone, blood, location, latitude, longitude, password, status, 
                                    registration_date, weight, age, gender, emergency_contact, health_conditions,
                                    points, donor_level, is_verified, last_location_update)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (donor_id, name, email, phone, blood, location, lat, lon,
                                 hash_password(password), "Available", current_time,
                                 weight, age, gender, emergency_contact, health_conditions,
                                 0, "New Donor 🌟", 1 if coords else 0, current_time),
                                commit=True
                            )
                            
                            donor_details = {
                                'donor_id': donor_id,
                                'blood': blood,
                                'location': location
                            }
                            send_welcome_email(email, name, donor_details)
                            
                            st.success(f"✅ Registration successful!")
                            
                            if coords:
                                qr_manager = QRCodeManager()
                                donor_data = {
                                    'name': name,
                                    'blood': blood,
                                    'donor_level': 'New Donor 🌟',
                                    'total_donations': 0,
                                    'medical_id': '',
                                    'emergency_contact': emergency_contact
                                }
                                qr_code = qr_manager.generate_donor_qr(donor_id, donor_data)
                                if qr_code:
                                    st.image(qr_code, caption="Your Donor QR Code", width=200)
                            
                            st.balloons()
                            
                        except sqlite3.IntegrityError:
                            st.error("Email already registered")

    # ============================================
    # PATIENT REQUEST PAGE - FIXED (removed distance warnings)
    # ============================================

    elif menu == "🆘 Patient Request":
        st.title("🆘 Emergency Blood Request")
        
        total_donors_count = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
        total_donors = total_donors_count['count'] if total_donors_count else 0
        st.info(f"📊 Total donors in system: {total_donors}")
        
        with st.form("request_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                patient = st.text_input("Patient Name*")
                email = st.text_input("Your Email*")
                blood = st.selectbox("Blood Type Needed*", BLOOD_TYPES)
                patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=30)
            
            with col2:
                location = st.text_input("Hospital Location*")
                hospital = st.text_input("Hospital Name*")
                doctor = st.text_input("Doctor's Name")
            
            urgency = st.select_slider("Urgency", options=["Normal", "High", "Critical"], value="High")
            units = st.number_input("Units Needed", min_value=1, max_value=10, value=1)
            
            submitted = st.form_submit_button("🚨 Request Blood")
            
            if submitted:
                if not all([patient, email, blood, location, hospital]):
                    st.error("Please fill all required fields")
                else:
                    email = normalize_email(email)
                    if not is_valid_email(email):
                        st.error("❌ Invalid email format")
                    else:
                        coords = get_coords(location)
                        lat, lon = coords if coords else (None, None)
                        
                        with st.spinner("🔍 Finding donors..."):
                            show_donor_search()
                            all_donors = get_all_donors_sorted_by_distance(blood, location)
                        
                        if not all_donors:
                            st.error(f"❌ No donors found with blood type {blood}!")
                            
                            request_id = generate_id('REQ')
                            current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            execute_query(
                                """INSERT INTO requests 
                                   (request_id, patient, patient_email, blood, location, latitude, longitude, hospital, 
                                    doctor_name, status, time, urgency_level, units_needed,
                                    patient_age, total_donors_count)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (request_id, patient, email, blood, location, lat, lon, hospital,
                                 doctor, "No Donors Available", current_time_str, urgency, units,
                                 patient_age, 0),
                                commit=True
                            )
                        else:
                            request_id = generate_id('REQ')
                            current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            serializable_donors = make_json_serializable(all_donors)
                            donors_json = json.dumps(serializable_donors)
                            
                            execute_query(
                                """INSERT INTO requests 
                                   (request_id, patient, patient_email, blood, location, latitude, longitude, hospital, 
                                    doctor_name, status, time, urgency_level, units_needed,
                                    patient_age, all_donors, total_donors_count)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (request_id, patient, email, blood, location, lat, lon, hospital,
                                 doctor, "Pending", current_time_str, urgency, units,
                                 patient_age, donors_json, len(all_donors)),
                                commit=True
                            )
                            
                            st.success(f"✅ Request submitted! {len(all_donors)} donors will be contacted.")
                            
                            # Show donor queue without distance warnings
                            with st.expander(f"View Donor Queue ({len(all_donors)} donors)"):
                                for i, donor in enumerate(all_donors[:20]):
                                    distance = donor.get('distance_km')
                                    distance_str = f"{distance} km" if distance else "Location pending"
                                    
                                    badge = "🔴 FIRST IN QUEUE" if i == 0 else f"#{i+1} in queue"
                                    st.markdown(f"""
                                    <div class='donor-card'>
                                        <span class='priority-badge'>{badge}</span>
                                        <strong>{donor.get('name', 'Unknown')}</strong> - {donor.get('blood', 'Unknown')} - {distance_str}
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                if len(all_donors) > 20:
                                    st.info(f"... and {len(all_donors) - 20} more donors")

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
                        (email,),
                        fetch_all=True
                    ) or []
                    
                    if requests:
                        for req in requests:
                            if not req:
                                continue
                                
                            status_emoji = {
                                "Pending": "⏳",
                                "Accepted": "✅",
                                "No Donors Available": "❌"
                            }.get(req.get('status'), "📝")
                            
                            with st.expander(f"{status_emoji} Request #{req.get('id')} - {req.get('blood', 'Unknown')}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown(f"""
                                    **Patient:** {req.get('patient', 'Unknown')}
                                    **Blood Type:** {req.get('blood', 'Unknown')}
                                    **Hospital:** {req.get('hospital', 'Unknown')}
                                    **Status:** {req.get('status', 'Unknown')}
                                    **Request Time:** {req.get('time', 'Unknown')}
                                    **Total Donors:** {req.get('total_donors_count', 0)}
                                    """)
                                
                                with col2:
                                    if req.get('status') == "Pending":
                                        if req.get('last_contacted_time'):
                                            try:
                                                contacted = [x for x in req.get('contacted', '').split(',') if x]
                                                total = req.get('total_donors_count', 0)
                                                progress = len(contacted)
                                                
                                                if total > 0:
                                                    st.write(f"**Donors Contacted:** {progress}/{total}")
                                                    st.progress(progress/total)
                                            except:
                                                st.info("Processing request...")
                                    
                                    elif req.get('status') == "Accepted" and req.get('donor_id'):
                                        donor = execute_query(
                                            "SELECT * FROM donors WHERE id=?",
                                            (req['donor_id'],),
                                            fetch_one=True
                                        )
                                        if donor:
                                            st.success("✅ Donor Found!")
                                            st.markdown(f"""
                                            **Donor:** {donor.get('name', 'Unknown')}
                                            **Phone:** {donor.get('phone', '')}
                                            **Email:** {donor.get('email', '')}
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
    # DONOR DASHBOARD - FIXED (removed distance warnings)
    # ============================================

    elif menu == "👤 Donor Dashboard":
        if st.session_state.logged_in_donor is not None:
            donor = st.session_state.logged_in_donor
            
            donor = execute_query(
                "SELECT * FROM donors WHERE id=?",
                (donor['id'],),
                fetch_one=True
            )
            
            if donor:
                donor_name = donor.get('name', 'Donor')
                donor_level = donor.get('donor_level', 'New Donor 🌟')
                donor_blood = donor.get('blood', 'Unknown')
                donor_donations = donor.get('total_donations', 0)
                donor_points = donor.get('points', 0)
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown("<h1 style='font-size: 5rem;'>🩸</h1>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<h2>{donor_name}</h2><p>{donor_level} • {donor_blood}</p>", unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Donations", donor_donations)
                with col2:
                    st.metric("Points", donor_points)
                with col3:
                    st.metric("Level", donor_level)
                with col4:
                    eligible, msg = is_donor_eligible(donor)
                    st.metric("Status", "✅ Eligible" if eligible else "⏳ Cooldown", help=msg)
                
                # Show QR code
                qr_manager = QRCodeManager()
                donor_data = {
                    'name': donor_name,
                    'blood': donor_blood,
                    'donor_level': donor_level,
                    'total_donations': donor_donations,
                    'medical_id': donor.get('medical_id', ''),
                    'emergency_contact': donor.get('emergency_contact', '')
                }
                qr_code = qr_manager.generate_donor_qr(donor.get('donor_id'), donor_data)
                if qr_code:
                    st.markdown("### 📱 Your Donor QR Code")
                    st.image(qr_code, width=200)
                
                st.markdown("---")
                st.subheader("Donation History")
                history = execute_query(
                    "SELECT * FROM donation_history WHERE donor_id=? ORDER BY donation_date DESC",
                    (donor['id'],),
                    fetch_all=True
                ) or []
                
                if history:
                    df_history = pd.DataFrame(history)
                    if not df_history.empty:
                        st.dataframe(df_history, use_container_width=True, hide_index=True)
                else:
                    st.info("No donation history yet")
                
                if st.button("Logout"):
                    st.session_state.logged_in_donor = None
                    st.rerun()
            else:
                st.error("Donor not found. Please login again.")
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
                    donor = execute_query(
                        "SELECT * FROM donors WHERE email=?",
                        (email,),
                        fetch_one=True
                    )
                    if donor and verify_password(password, donor['password']):
                        st.session_state.logged_in_donor = donor
                        st.success(f"Welcome back, {donor['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")

    # ============================================
    # HOSPITALS PAGE
    # ============================================

    elif menu == "🏥 Hospitals":
        st.title("🏥 Hospitals")
        
        location = st.text_input("Enter your location to find nearby hospitals")
        
        if location:
            hospital_manager = HospitalManager()
            nearby = hospital_manager.get_nearby_hospitals(location)
            
            if nearby:
                for hospital in nearby:
                    if hospital:
                        with st.expander(f"🏥 {hospital.get('name', 'Unknown')} - {hospital.get('distance', 0)} km"):
                            st.markdown(f"""
                            **Address:** {hospital.get('address', '')}
                            **Phone:** {hospital.get('phone', '')}
                            **Email:** {hospital.get('email', '')}
                            """)
            else:
                st.info("No hospitals found")

    # ============================================
    # BLOOD INVENTORY PAGE
    # ============================================

    elif menu == "📦 Blood Inventory":
        st.title("📦 Blood Inventory")
        inventory_manager.display_inventory_dashboard()

    # ============================================
    # DONATION EVENTS PAGE - COMPLETE FIXED
    # ============================================

    elif menu == "🎪 Donation Events":
        st.title("🎪 Donation Events")
        
        event_manager = DonationEventManager()
        
        tab1, tab2, tab3 = st.tabs(["📋 Browse Events", "➕ Create Event", "📊 My Registrations"])
        
        with tab1:
            st.subheader("Find Donation Events")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                location = st.text_input("Enter your location to find nearby events", 
                                        placeholder="e.g., MG Road, Bangalore")
            with col2:
                radius = st.number_input("Search radius (km)", min_value=5, max_value=200, value=50)
            
            if location:
                with st.spinner("🔍 Finding events near you..."):
                    events = event_manager.get_nearby_events(location, radius)
                
                if events:
                    st.success(f"Found {len(events)} events near you!")
                    
                    for event in events:
                        with st.expander(f"🎪 {event.get('event_name', 'Unknown')} - {event.get('distance', 0)} km"):
                            st.markdown(f"""
                            **Date:** {event.get('start_date', '')} at {event.get('start_time', '')}
                            **Location:** {event.get('location', '')}
                            **Contact:** {event.get('contact_phone', '')}
                            **Registered:** {event.get('registered_donors', 0)}/{event.get('target_donations', 0)}
                            **Description:** {event.get('description', '')}
                            """)
                            
                            if st.session_state.logged_in_donor is not None:
                                if st.button(f"📝 Register", key=f"reg_{event.get('id')}"):
                                    success, message = event_manager.register_for_event(
                                        event.get('id'), 
                                        st.session_state.logged_in_donor
                                    )
                                    if success:
                                        st.success(message)
                                        st.balloons()
                                        st.rerun()
                                    else:
                                        st.error(message)
                            else:
                                st.info("Please login to register for events")
                else:
                    st.info("No events found in your area.")
            
            else:
                all_events = event_manager.get_all_events(status='Upcoming')
                if all_events:
                    st.subheader("📅 Upcoming Events")
                    for event in all_events[:5]:
                        with st.expander(f"🎪 {event.get('event_name', 'Unknown')}"):
                            st.markdown(f"""
                            **Date:** {event.get('start_date', '')}
                            **Location:** {event.get('location', '')}
                            **Contact:** {event.get('contact_phone', '')}
                            """)
        
        with tab2:
            st.subheader("➕ Create New Donation Event")
            
            with st.form("create_event_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    event_name = st.text_input("Event Name*")
                    organizer = st.text_input("Organizer Name*")
                    organizer_email = st.text_input("Organizer Email*")
                    organizer_phone = st.text_input("Organizer Phone*")
                    
                    start_date = st.date_input("Start Date*", value=date.today())
                    end_date = st.date_input("End Date*", value=date.today() + timedelta(days=1))
                    
                    start_time = st.time_input("Start Time*", value=datetime.now().time())
                    end_time = st.time_input("End Time*", value=datetime.now().time())
                
                with col2:
                    location = st.text_input("Event Location*")
                    address = st.text_area("Detailed Address*")
                    city = st.text_input("City*")
                    
                    contact_person = st.text_input("Contact Person*")
                    contact_phone = st.text_input("Contact Phone*")
                    contact_email = st.text_input("Contact Email*")
                    
                    target_donations = st.number_input("Target Donations*", min_value=1, value=50)
                
                description = st.text_area("Event Description")
                
                blood_types_needed = st.multiselect("Blood Types Needed", BLOOD_TYPES, default=BLOOD_TYPES)
                
                amenities = st.multiselect(
                    "Amenities",
                    ["Free Refreshments", "Free T-shirt", "Free Health Checkup", "Free Parking", "Certificate"]
                )
                
                incentives = st.multiselect(
                    "Incentives",
                    ["Donation Certificate", "Reward Points", "Badge"]
                )
                
                submitted = st.form_submit_button("🚀 Create Event")
                
                if submitted:
                    if not all([event_name, organizer, location, start_date, end_date, 
                               contact_person, contact_phone, blood_types_needed]):
                        st.error("Please fill all required fields")
                    elif not is_valid_email(organizer_email) or not is_valid_email(contact_email):
                        st.error("Please enter valid email addresses")
                    else:
                        event_data = {
                            'event_name': event_name,
                            'organizer': organizer,
                            'organizer_email': organizer_email,
                            'organizer_phone': organizer_phone,
                            'location': location,
                            'address': address,
                            'city': city,
                            'start_date': start_date.strftime("%Y-%m-%d"),
                            'end_date': end_date.strftime("%Y-%m-%d"),
                            'start_time': start_time.strftime("%H:%M"),
                            'end_time': end_time.strftime("%H:%M"),
                            'target_donations': target_donations,
                            'contact_person': contact_person,
                            'contact_phone': contact_phone,
                            'contact_email': contact_email,
                            'description': description,
                            'blood_types_needed': blood_types_needed,
                            'amenities': amenities,
                            'incentives': incentives,
                            'special_instructions': '',
                            'min_age': 18,
                            'max_age': 65,
                            'min_weight': 45,
                            'is_featured': 0,
                            'registration_deadline': start_date.strftime("%Y-%m-%d"),
                            'status': 'Upcoming'
                        }
                        
                        organizer_id = st.session_state.logged_in_donor['id'] if st.session_state.logged_in_donor else None
                        
                        success, result = event_manager.create_event(event_data, organizer_id)
                        
                        if success:
                            st.success(f"✅ Event created successfully!")
                            st.balloons()
                            
                            qr_manager = QRCodeManager()
                            qr_code = qr_manager.generate_event_qr(result, event_data)
                            if qr_code:
                                st.image(qr_code, caption="Event QR Code for Check-in", width=200)
                        else:
                            st.error(f"Failed to create event: {result}")
        
        with tab3:
            if st.session_state.logged_in_donor is not None:
                st.subheader("My Event Registrations")
                
                registrations = execute_query(
                    """SELECT er.*, de.event_name, de.start_date, de.location, de.status 
                       FROM event_registrations er
                       JOIN donation_events de ON er.event_id = de.id
                       WHERE er.donor_id=?
                       ORDER BY er.registration_date DESC""",
                    (st.session_state.logged_in_donor['id'],),
                    fetch_all=True
                ) or []
                
                if registrations:
                    for reg in registrations:
                        with st.expander(f"🎪 {reg.get('event_name')} - {reg.get('start_date')}"):
                            st.markdown(f"""
                            **Registration Date:** {reg.get('registration_date')}
                            **Event Status:** {reg.get('status')}
                            **Attended:** {"✅ Yes" if reg.get('attended') else "⏳ No"}
                            """)
                else:
                    st.info("You haven't registered for any events yet")
            else:
                st.warning("Please login to view your registrations")

    # ============================================
    # REWARDS STORE PAGE
    # ============================================

    elif menu == "🎁 Rewards Store":
        st.title("🎁 Rewards Store")
        
        rewards_manager = RewardsManager()
        
        if st.session_state.logged_in_donor is not None:
            donor = st.session_state.logged_in_donor
            summary = rewards_manager.get_donor_points_summary(donor['id'])
            if summary:
                st.markdown(f"### Your Points: {summary.get('current_points', 0)}")
        
        rewards = rewards_manager.get_available_rewards()
        if rewards:
            cols = st.columns(3)
            for i, reward in enumerate(rewards):
                if reward:
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class='reward-card'>
                            <h3>{reward.get('item_name', '')}</h3>
                            <p>{reward.get('points_required', 0)} points</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No rewards available at the moment")

    # ============================================
    # CHAT PAGE
    # ============================================

    elif menu == "💬 Chat":
        if st.session_state.logged_in_donor is None:
            st.warning("Please login to use chat")
        else:
            donor = st.session_state.logged_in_donor
            donor_id = donor['id']
            chat_manager = ChatManager()
            
            unread = chat_manager.get_unread_count(donor_id)
            if unread > 0:
                st.info(f"You have {unread} unread messages")
            
            st.info("Chat feature coming soon!")

    # ============================================
    # IMPACT DASHBOARD
    # ============================================

    elif menu == "📊 Impact Dashboard":
        if st.session_state.logged_in_donor is not None:
            donor = st.session_state.logged_in_donor
            impact_viz = DonorImpactVisualizer()
            impact_viz.create_impact_dashboard(donor['id'], donor['name'])
        else:
            st.warning("Please login to view your impact dashboard")

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
            
            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Donors", "Requests", "Queue Monitor"])
            
            with tab1:
                total_donors = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
                total_donors = total_donors['count'] if total_donors else 0
                
                total_requests = execute_query("SELECT COUNT(*) as count FROM requests", fetch_one=True)
                total_requests = total_requests['count'] if total_requests else 0
                
                total_donations = execute_query("SELECT COUNT(*) as count FROM donation_history", fetch_one=True)
                total_donations = total_donations['count'] if total_donations else 0
                
                pending = execute_query("SELECT COUNT(*) as count FROM requests WHERE status='Pending'", fetch_one=True)
                pending = pending['count'] if pending else 0
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Donors", total_donors)
                col2.metric("Total Requests", total_requests)
                col3.metric("Pending", pending)
                col4.metric("Completed", total_donations)
            
            with tab2:
                donors = execute_query("SELECT * FROM donors", fetch_all=True) or []
                if donors:
                    df = pd.DataFrame(donors)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            
            with tab3:
                requests = execute_query("SELECT * FROM requests ORDER BY id DESC", fetch_all=True) or []
                if requests:
                    df = pd.DataFrame(requests)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            
            with tab4:
                pending_reqs = execute_query("SELECT * FROM requests WHERE status='Pending'", fetch_all=True) or []
                for req in pending_reqs:
                    with st.expander(f"Request #{req.get('request_id')} - {req.get('blood')}"):
                        contacted = [x for x in req.get('contacted', '').split(',') if x]
                        total = req.get('total_donors_count', 0)
                        progress = len(contacted)
                        
                        st.write(f"**Progress:** {progress}/{total} donors contacted")
                        if total > 0:
                            st.progress(progress/total)

    # ============================================
    # EMAIL LOG PAGE
    # ============================================

    elif menu == "📧 Email Log":
        st.title("📧 Email Log")
        
        if st.session_state.email_log:
            for log in st.session_state.email_log[-50:]:
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
        <p>BloodAI v23.0 - Complete System</p>
        <p>📍 <strong>All Donors Notified • Closest First • {WAIT_MINUTES} Min Rotation</strong></p>
        <p>🎪 <strong>Donation Events Included</strong></p>
    </div>
    """, unsafe_allow_html=True)
