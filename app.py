# ============================================
# 🩸 BLOODAI COMPLETE SYSTEM v19.0 - ULTIMATE EDITION
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
from pathlib import Path
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
    
    /* Database status indicator */
    .db-status {
        background: linear-gradient(135deg, #43e97b20, #38f9d720);
        border: 2px solid #43e97b;
        padding: 0.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Progress bar */
    .custom-progress {
        background: #f0f0f0;
        border-radius: 15px;
        height: 12px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .custom-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 15px;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CONFIGURATION
# ============================================

# Email Configuration
FROM_EMAIL = "vigneshsapavat11@gmail.com"
APP_PASSWORD = "kmcfregjdseaihwn"
BASE_URL = "https://bloodai-smart-donor-system.streamlit.app/"

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

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

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
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# ============================================
# PERMANENT DATABASE STORAGE
# ============================================

def get_database_path():
    """Get persistent database path that survives app restarts"""
    try:
        # Use user's home directory (persistent on Streamlit Cloud)
        home_dir = str(Path.home())
        persistent_dir = os.path.join(home_dir, ".bloodai_data")
        os.makedirs(persistent_dir, mode=0o777, exist_ok=True)
        
        # Test write access
        test_file = os.path.join(persistent_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        
        db_path = os.path.join(persistent_dir, "bloodai_permanent.db")
        print(f"✅ Using persistent database: {db_path}")
        return db_path
        
    except Exception as e:
        print(f"⚠️ Using temporary database: {e}")
        return "/tmp/bloodai.db"

DB_PATH = get_database_path()

# ============================================
# DATABASE CONNECTION MANAGER
# ============================================

@contextmanager
def get_db_connection():
    conn = None
    try:
        if DB_PATH == ":memory:":
            conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
        else:
            conn = sqlite3.connect(DB_PATH, timeout=30)
        
        conn.row_factory = sqlite3.Row
        yield conn
    except Exception as e:
        print(f"Database error: {e}")
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
        print(f"Query error: {e}")
        return None if fetch_one or fetch_all else -1

# ============================================
# COMPLETE DATABASE SETUP
# ============================================

def init_database():
    try:
        with get_db_connection() as conn:
            if conn is None:
                st.error("❌ Could not connect to database")
                return False
                
            cursor = conn.cursor()
            
            # Donors table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS donors(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                donor_id TEXT UNIQUE,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                blood TEXT NOT NULL,
                location TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                password BLOB NOT NULL,
                status TEXT DEFAULT 'Available',
                registration_date TEXT NOT NULL,
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
                blood_type TEXT NOT NULL,
                units INTEGER DEFAULT 0,
                hospital_id INTEGER,
                expiry_date TEXT,
                batch_number TEXT,
                collection_date TEXT,
                status TEXT DEFAULT 'Available',
                location TEXT,
                last_updated TEXT,
                quality_checked INTEGER DEFAULT 0,
                FOREIGN KEY (hospital_id) REFERENCES hospitals (id)
            )
            """)
            
            # Hospitals Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospitals(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hospital_id TEXT UNIQUE,
                name TEXT NOT NULL,
                registration_number TEXT UNIQUE,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT,
                phone TEXT NOT NULL,
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
            
            # Requests table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT UNIQUE NOT NULL,
                patient TEXT NOT NULL,
                patient_email TEXT NOT NULL,
                patient_phone TEXT,
                blood TEXT NOT NULL,
                location TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                hospital TEXT NOT NULL,
                hospital_id INTEGER,
                hospital_contact TEXT,
                doctor_name TEXT,
                status TEXT DEFAULT 'Pending',
                donor_id INTEGER,
                time TEXT NOT NULL,
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
                FOREIGN KEY (hospital_id) REFERENCES hospitals (id),
                FOREIGN KEY (donor_id) REFERENCES donors (id)
            )
            """)
            
            # Donation Events Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS donation_events(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE NOT NULL,
                event_name TEXT NOT NULL,
                organizer TEXT NOT NULL,
                organizer_id INTEGER,
                organizer_email TEXT NOT NULL,
                organizer_phone TEXT NOT NULL,
                location TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                target_donations INTEGER NOT NULL,
                registered_donors INTEGER DEFAULT 0,
                completed_donations INTEGER DEFAULT 0,
                status TEXT DEFAULT 'Upcoming',
                contact_person TEXT NOT NULL,
                contact_phone TEXT NOT NULL,
                contact_email TEXT NOT NULL,
                description TEXT,
                latitude REAL,
                longitude REAL,
                amenities TEXT,
                blood_types_needed TEXT,
                incentives TEXT,
                special_instructions TEXT,
                created_date TEXT NOT NULL,
                last_updated TEXT,
                registration_deadline TEXT,
                min_age INTEGER DEFAULT 18,
                max_age INTEGER DEFAULT 65,
                min_weight INTEGER DEFAULT 45,
                is_featured INTEGER DEFAULT 0,
                notified_donors INTEGER DEFAULT 0,
                FOREIGN KEY (organizer_id) REFERENCES donors (id)
            )
            """)
            
            # Event Registrations Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_registrations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                donor_id INTEGER NOT NULL,
                donor_name TEXT NOT NULL,
                donor_email TEXT NOT NULL,
                donor_phone TEXT,
                donor_blood TEXT,
                registration_date TEXT NOT NULL,
                attended INTEGER DEFAULT 0,
                check_in_time TEXT,
                feedback TEXT,
                rating INTEGER,
                points_earned INTEGER DEFAULT 0,
                FOREIGN KEY (event_id) REFERENCES donation_events (id),
                FOREIGN KEY (donor_id) REFERENCES donors (id),
                UNIQUE(event_id, donor_id)
            )
            """)
            
            # Event Notifications Log
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_notifications(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                donor_id INTEGER NOT NULL,
                sent_date TEXT NOT NULL,
                status TEXT DEFAULT 'sent',
                FOREIGN KEY (event_id) REFERENCES donation_events (id),
                FOREIGN KEY (donor_id) REFERENCES donors (id)
            )
            """)
            
            # Rewards Store Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS rewards(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reward_id TEXT UNIQUE,
                item_name TEXT NOT NULL,
                description TEXT,
                points_required INTEGER NOT NULL,
                stock INTEGER DEFAULT 0,
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
                donor_id INTEGER NOT NULL,
                reward_id INTEGER NOT NULL,
                redemption_date TEXT NOT NULL,
                points_spent INTEGER NOT NULL,
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
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                read INTEGER DEFAULT 0,
                conversation_id TEXT NOT NULL,
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
                donor_id INTEGER NOT NULL,
                check_date TEXT NOT NULL,
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
                donor_id INTEGER NOT NULL,
                achievement_type TEXT NOT NULL,
                achievement_date TEXT NOT NULL,
                description TEXT,
                points_awarded INTEGER DEFAULT 0,
                badge_icon TEXT,
                FOREIGN KEY (donor_id) REFERENCES donors (id)
            )
            """)
            
            # Notifications Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notification_id TEXT UNIQUE,
                user_email TEXT NOT NULL,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                date TEXT NOT NULL,
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
                donor_id INTEGER NOT NULL,
                request_id INTEGER,
                donation_date TEXT NOT NULL,
                hospital TEXT NOT NULL,
                blood_type TEXT NOT NULL,
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
                recipient TEXT NOT NULL,
                subject TEXT NOT NULL,
                type TEXT NOT NULL,
                sent_date TEXT NOT NULL,
                status TEXT NOT NULL,
                error_message TEXT,
                request_id TEXT,
                donor_id INTEGER,
                event_id INTEGER
            )
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_donors_email ON donors(email)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_donors_blood ON donors(blood)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_requests_status ON requests(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_status ON donation_events(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_date ON donation_events(start_date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_registrations_event ON event_registrations(event_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_registrations_donor ON event_registrations(donor_id)")
            
            conn.commit()
            
            test = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
            if test is not None:
                donor_count = test.get('count', 0)
                print(f"✅ Database initialized at: {DB_PATH}")
                return True
            return False
            
    except Exception as e:
        print(f"Init error: {e}")
        return False

# Initialize database
if not st.session_state.db_initialized:
    with st.spinner("🔄 Initializing database..."):
        if init_database():
            st.session_state.db_initialized = True

# Show database status
if os.path.exists(DB_PATH):
    file_size = os.path.getsize(DB_PATH)
    if file_size < 1024:
        size_str = f"{file_size} bytes"
    elif file_size < 1024 * 1024:
        size_str = f"{file_size/1024:.1f} KB"
    else:
        size_str = f"{file_size/(1024*1024):.1f} MB"
    db_status = f"✅ PERMANENT - {size_str}"
    db_location = os.path.basename(DB_PATH)
else:
    db_status = "⚠️ TEMPORARY"
    db_location = "in-memory"

# ============================================
# EMAIL VALIDATION FUNCTIONS
# ============================================

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email)) if email else False

def normalize_email(email):
    if not email:
        return email
    email = email.lower().strip()
    email = email.replace('@gmal.com', '@gmail.com')
    email = email.replace('@gmai.com', '@gmail.com')
    email = email.replace('@gamil.com', '@gmail.com')
    return email

# ============================================
# UTILITY FUNCTIONS
# ============================================

def generate_id(prefix):
    return f"{prefix}-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

def get_coords(location):
    try:
        if not location or len(location.strip()) < 5:
            return None
        geolocator = Nominatim(user_agent="bloodai_app")
        loc = geolocator.geocode(location, timeout=10)
        if loc:
            return (loc.latitude, loc.longitude)
        return None
    except:
        return None

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def log_email(recipient, subject, status):
    try:
        email_id = generate_id('EMAIL')
        execute_query(
            "INSERT INTO email_log (email_id, recipient, subject, type, sent_date, status) VALUES (?, ?, ?, ?, ?, ?)",
            (email_id, recipient, subject, 'email', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status),
            commit=True
        )
    except:
        pass

def send_email(to_email, subject, message, html=False):
    try:
        to_email = normalize_email(to_email)
        if not is_valid_email(to_email):
            log_email(to_email, subject, "failed")
            return False
        
        msg = MIMEMultipart() if html else MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        
        if html:
            msg.attach(MIMEText(message, 'html'))
        else:
            msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        log_email(to_email, subject, "sent")
        return True
    except Exception as e:
        log_email(to_email, subject, f"failed: {str(e)}")
        return False

def add_notification(user_email, title, message):
    try:
        if not user_email or not is_valid_email(user_email):
            return False
        notification_id = generate_id('NOTIF')
        execute_query(
            "INSERT INTO notifications (notification_id, user_email, type, title, message, date) VALUES (?, ?, ?, ?, ?, ?)",
            (notification_id, user_email, 'system', title, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            commit=True
        )
        return True
    except:
        return False

def get_unread_notifications(user_email):
    try:
        return execute_query(
            "SELECT * FROM notifications WHERE user_email=? AND read=0 ORDER BY date DESC",
            (user_email,),
            fetch_all=True
        ) or []
    except:
        return []

def mark_notifications_read(user_email):
    try:
        execute_query(
            "UPDATE notifications SET read=1 WHERE user_email=?",
            (user_email,),
            commit=True
        )
        return True
    except:
        return False

# ============================================
# DONOR ELIGIBILITY
# ============================================

def is_donor_eligible(donor):
    try:
        if not donor:
            return False, "Invalid donor"
        
        last_donation = donor.get('last_donation_date')
        if not last_donation:
            return True, "Eligible"
        
        try:
            last_date = datetime.strptime(last_donation, "%Y-%m-%d %H:%M:%S")
            current_date = datetime.now()
            months_diff = (current_date.year - last_date.year) * 12 + current_date.month - last_date.month
            
            if months_diff >= COOLDOWN_MONTHS:
                return True, "Eligible"
            else:
                next_eligible = last_date + timedelta(days=COOLDOWN_MONTHS * 30)
                days = (next_eligible - current_date).days
                return False, f"On cooldown ({days} days left)"
        except:
            return True, "Eligible"
    except:
        return True, "Eligible"

def get_eligible_donors(blood_type):
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
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='ignore')
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
# DONOR SORTING FUNCTION
# ============================================

def get_all_donors_sorted_by_distance(blood_type, location):
    """Get ALL donors sorted by distance from patient - nearest first"""
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
            if 'password' in donor_copy:
                del donor_copy['password']
            
            donor_lat = donor_copy.get('latitude')
            donor_lon = donor_copy.get('longitude')
            
            if donor_lat and donor_lon and patient_coords:
                try:
                    distance = geodesic(patient_coords, (donor_lat, donor_lon)).km
                    donor_copy['distance_km'] = round(distance, 2)
                except:
                    donor_copy['distance_km'] = 999999
            else:
                donor_copy['distance_km'] = 999999
            
            donors_with_distance.append(donor_copy)
        
        donors_with_distance.sort(key=lambda x: x.get('distance_km', 999999))
        return donors_with_distance
        
    except Exception as e:
        return []

def get_next_donor_to_contact(request):
    try:
        all_donors_json = request.get('all_donors', '')
        current_index = request.get('current_donor_index', 0)
        contacted = request.get('contacted', '')
        
        if not all_donors_json:
            return None, None
        
        all_donors = json.loads(all_donors_json)
        contacted_list = [int(x) for x in contacted.split(',') if x]
        
        for i in range(current_index, len(all_donors)):
            donor_id = all_donors[i].get('id')
            if donor_id and donor_id not in contacted_list:
                return all_donors[i], i
        
        return None, None
    except:
        return None, None

# ============================================
# EMAIL FUNCTIONS
# ============================================

def send_donor_request_email(donor, request, donor_rank, total_donors, donor_distance=None):
    try:
        donor_email = normalize_email(donor.get('email'))
        if not is_valid_email(donor_email):
            return False
        
        accept_url = f"{BASE_URL}/?accept={request.get('id')}&donor={donor.get('id')}"
        reject_url = f"{BASE_URL}/?reject={request.get('id')}&donor={donor.get('id')}"
        
        subject = f"🩸 URGENT: Blood Donation Needed - {request.get('blood')}"
        
        if donor_rank == 1:
            priority_message = "🌟 YOU ARE THE CLOSEST DONOR - Please respond first!"
            priority_color = "#43e97b"
        else:
            priority_message = f"You are #{donor_rank} in the queue of {total_donors} donors"
            priority_color = "#ff6b6b"
        
        distance_text = f"({donor_distance:.1f} km away)" if donor_distance and donor_distance != 999999 else ""
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; }}
        .header {{ background: #ff6b6b; padding: 30px; text-align: center; color: white; }}
        .priority-box {{ background: {priority_color}20; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid {priority_color}; }}
        .button {{ display: inline-block; padding: 15px 30px; text-decoration: none; border-radius: 50px; margin: 10px; }}
        .accept {{ background: #43e97b; color: white; }}
        .reject {{ background: #ff6b6b; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🩸 URGENT BLOOD REQUEST</h1>
        </div>
        <div style="padding: 30px;">
            <h2>Hello {donor.get('name')},</h2>
            <div class="priority-box">
                <h3 style="color: {priority_color};">📍 YOUR POSITION</h3>
                <p><strong>{priority_message}</strong> {distance_text}</p>
            </div>
            <p><strong>Blood Type:</strong> {request.get('blood')}</p>
            <p><strong>Hospital:</strong> {request.get('hospital')}</p>
            <p><strong>Patient:</strong> {request.get('patient')}</p>
            <div style="text-align: center;">
                <a href="{accept_url}" class="button accept">✅ ACCEPT</a>
                <a href="{reject_url}" class="button reject">❌ REJECT</a>
            </div>
            <p><small>You have {WAIT_MINUTES} minutes to respond.</small></p>
        </div>
    </div>
</body>
</html>
        """
        
        return send_email(donor_email, subject, message, html=True)
    except:
        return False

def send_patient_notification_email(patient_email, patient_name, donor, request, donor_distance=None):
    try:
        patient_email = normalize_email(patient_email)
        if not is_valid_email(patient_email):
            return False
        
        subject = "✅ Donor Found - Blood Request"
        
        distance_text = f"<p><strong>Distance:</strong> {donor_distance:.1f} km</p>" if donor_distance and donor_distance != 999999 else ""
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 10px; padding: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>✅ DONOR FOUND</h2>
        <p>A donor has accepted your blood request!</p>
        <hr>
        <h3>DONOR CONTACT DETAILS</h3>
        <p><strong>Name:</strong> {donor.get('name')}</p>
        <p><strong>Phone:</strong> {donor.get('phone')}</p>
        <p><strong>Email:</strong> {donor.get('email')}</p>
        {distance_text}
        <hr>
        <p><strong>Next Steps:</strong> Contact the donor immediately to schedule the donation.</p>
    </div>
</body>
</html>
        """
        
        return send_email(patient_email, subject, message, html=True)
    except:
        return False

def send_donor_confirmation_email(donor, patient_name, request, next_eligible):
    try:
        donor_email = normalize_email(donor.get('email'))
        if not is_valid_email(donor_email):
            return False
        
        subject = "🎉 Thank You - Blood Donation Confirmed"
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; padding: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>🎉 THANK YOU HERO!</h2>
        <p>Dear {donor.get('name')},</p>
        <p>Thank you for accepting the blood donation request!</p>
        <p><strong>Patient:</strong> {patient_name}</p>
        <p><strong>Hospital:</strong> {request.get('hospital')}</p>
        <p><strong>Blood Type:</strong> {request.get('blood')}</p>
        <p><strong>Points Earned:</strong> +{POINTS_PER_DONATION}</p>
        <p><strong>Next Eligible Date:</strong> {next_eligible}</p>
    </div>
</body>
</html>
        """
        
        return send_email(donor_email, subject, message, html=True)
    except:
        return False

def send_welcome_email(donor_email, donor_name, donor_details):
    try:
        donor_email = normalize_email(donor_email)
        if not is_valid_email(donor_email):
            return False
        
        subject = "🎉 Welcome to BloodAI"
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; padding: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome {donor_name}!</h2>
        <p>Thank you for registering as a blood donor.</p>
        <p><strong>Donor ID:</strong> {donor_details.get('donor_id')}</p>
        <p><strong>Blood Type:</strong> {donor_details.get('blood')}</p>
        <p>You'll be notified when someone near you needs blood.</p>
    </div>
</body>
</html>
        """
        
        return send_email(donor_email, subject, message, html=True)
    except:
        return False

def send_event_notification_email(donor_email, donor_name, event_data, distance=None):
    try:
        donor_email = normalize_email(donor_email)
        if not is_valid_email(donor_email):
            return False
        
        subject = f"🎪 New Donation Event: {event_data.get('event_name')}"
        
        distance_text = f"<p><strong>📍 Distance from you:</strong> {distance:.1f} km</p>" if distance else ""
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; padding: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>🎪 New Donation Event!</h2>
        <p>Hello {donor_name},</p>
        <p>A new blood donation event has been organized!</p>
        <p><strong>Event:</strong> {event_data.get('event_name')}</p>
        <p><strong>Date:</strong> {event_data.get('start_date')} at {event_data.get('start_time')}</p>
        <p><strong>Location:</strong> {event_data.get('location')}</p>
        {distance_text}
        <p>Please register through the app if interested.</p>
    </div>
</body>
</html>
        """
        
        return send_email(donor_email, subject, message, html=True)
    except:
        return False

def send_event_registration_email(donor_email, donor_name, event_name, event_data):
    try:
        donor_email = normalize_email(donor_email)
        if not is_valid_email(donor_email):
            return False
        
        subject = f"✅ Registration Confirmed - {event_name}"
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; padding: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>✅ Registration Confirmed!</h2>
        <p>Hello {donor_name},</p>
        <p>Thank you for registering for the donation event!</p>
        <p><strong>Event:</strong> {event_name}</p>
        <p><strong>Date:</strong> {event_data.get('start_date')} at {event_data.get('start_time')}</p>
        <p><strong>Location:</strong> {event_data.get('location')}</p>
        <p>We look forward to seeing you there!</p>
    </div>
</body>
</html>
        """
        
        return send_email(donor_email, subject, message, html=True)
    except:
        return False

# ============================================
# AUTO DONOR SCHEDULER
# ============================================

def check_and_contact_next_donor():
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
                last_contacted = request.get('last_contacted_time')
                all_donors_json = request.get('all_donors', '')
                
                if not request_id:
                    continue
                
                # First contact - nearest donor immediately
                if not last_contacted and all_donors_json:
                    try:
                        all_donors = json.loads(all_donors_json)
                        if all_donors:
                            nearest_donor = all_donors[0]
                            new_contacted = str(nearest_donor.get('id')) + ","
                            current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            execute_query(
                                "UPDATE requests SET donor_id=?, contacted=?, last_contacted_time=?, current_donor_index=1 WHERE id=?",
                                (nearest_donor.get('id'), new_contacted, current_time_str, request_id),
                                commit=True
                            )
                            
                            distance = nearest_donor.get('distance_km', 999999)
                            send_donor_request_email(nearest_donor, request, 1, len(all_donors), distance)
                    except:
                        pass
                
                # Subsequent contacts after timeout
                elif last_contacted:
                    try:
                        last_time = datetime.strptime(last_contacted, "%Y-%m-%d %H:%M:%S")
                        current_time = datetime.now()
                        
                        if current_time - last_time >= timedelta(minutes=WAIT_MINUTES):
                            next_donor, next_index = get_next_donor_to_contact(request)
                            
                            if next_donor and all_donors_json:
                                all_donors = json.loads(all_donors_json)
                                contacted = request.get('contacted', '')
                                new_contacted = contacted + str(next_donor.get('id')) + ","
                                current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
                                
                                execute_query(
                                    "UPDATE requests SET donor_id=?, contacted=?, last_contacted_time=?, current_donor_index=? WHERE id=?",
                                    (next_donor.get('id'), new_contacted, current_time_str, next_index + 1, request_id),
                                    commit=True
                                )
                                
                                rank = next_index + 1
                                distance = next_donor.get('distance_km', 999999)
                                send_donor_request_email(next_donor, request, rank, len(all_donors), distance)
                            else:
                                execute_query(
                                    "UPDATE requests SET status='No Donors Available' WHERE id=?",
                                    (request_id,),
                                    commit=True
                                )
                    except:
                        pass
            
            time.sleep(30)
        except:
            time.sleep(60)

def run_scheduler():
    while True:
        try:
            check_and_contact_next_donor()
        except:
            pass
        time.sleep(30)

if not st.session_state.scheduler_started:
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
    st.session_state.scheduler_started = True

# ============================================
# DONOR RESPONSE HANDLER
# ============================================

def handle_donor_response():
    try:
        query_params = st.query_params
        
        if "accept" in query_params and "donor" in query_params:
            try:
                request_id = int(query_params["accept"])
                donor_id = int(query_params["donor"])
                
                st.markdown("""
                <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #43e97b, #38f9d7); border-radius: 20px; margin: 2rem 0;'>
                    <h1 style='color: white;'>✅ Processing Your Acceptance...</h1>
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
                
                if request.get('status') != 'Pending':
                    st.warning("This request is no longer available")
                    return
                
                donor_distance = None
                if request.get('latitude') and donor.get('latitude'):
                    try:
                        donor_distance = geodesic(
                            (request['latitude'], request['longitude']),
                            (donor['latitude'], donor['longitude'])
                        ).km
                    except:
                        pass
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                execute_query(
                    "UPDATE donors SET status='Busy', last_donation_date=?, total_donations=total_donations+1, points=points+? WHERE id=?",
                    (current_time, POINTS_PER_DONATION, donor_id),
                    commit=True
                )
                
                update_donor_points(donor_id)
                
                execute_query(
                    "UPDATE requests SET status='Accepted', completed_time=?, donor_id=?, closest_donor_distance=? WHERE id=?",
                    (current_time, donor_id, donor_distance, request_id),
                    commit=True
                )
                
                history_id = generate_id('DH')
                execute_query(
                    "INSERT INTO donation_history (history_id, donor_id, request_id, donation_date, hospital, blood_type, units, points_earned, donor_distance_km) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (history_id, donor_id, request_id, current_time, request.get('hospital'), request.get('blood'), request.get('units_needed', 1), POINTS_PER_DONATION, donor_distance),
                    commit=True
                )
                
                next_eligible = (datetime.now() + timedelta(days=COOLDOWN_MONTHS * 30)).strftime("%Y-%m-%d")
                
                patient_email_sent = send_patient_notification_email(patient_email, request.get('patient'), donor, request, donor_distance)
                donor_email_sent = send_donor_confirmation_email(donor, request.get('patient'), request, next_eligible)
                
                add_notification(patient_email, "✅ Donor Found!", f"{donor.get('name')} has accepted your request")
                
                st.query_params.clear()
                st.session_state.showing_response = False
                
                st.balloons()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Donations", donor.get('total_donations', 0) + 1)
                with col2:
                    st.metric("Donor Level", donor.get('donor_level', 'New'))
                with col3:
                    st.metric("Points Earned", f"+{POINTS_PER_DONATION}")
                
                if donor_distance and donor_distance != 999999:
                    st.info(f"📍 Distance to hospital: {donor_distance:.1f} km")
                
                if st.button("🏠 Return Home"):
                    st.rerun()
                
                return True
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                return False
        
        elif "reject" in query_params and "donor" in query_params:
            try:
                request_id = int(query_params["reject"])
                donor_id = int(query_params["donor"])
                
                st.markdown("""
                <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #ff6b6b, #ee5253); border-radius: 20px; margin: 2rem 0;'>
                    <h1 style='color: white;'>🕊️ Request Rejected</h1>
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
                
                st.query_params.clear()
                st.session_state.showing_response = False
                
                if st.button("🏠 Return Home"):
                    st.rerun()
                
                return True
                
            except:
                return False
    except:
        return False

def init_response_handler():
    try:
        if "accept" in st.query_params or "reject" in st.query_params:
            st.session_state.showing_response = True
            handle_donor_response()
            if st.button("🏠 Return to Home"):
                st.query_params.clear()
                st.session_state.showing_response = False
                st.rerun()
            st.stop()
    except:
        pass

init_response_handler()

# ============================================
# DONOR SEARCH ANIMATION
# ============================================

def show_donor_search():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='loading-spinner'></div>", unsafe_allow_html=True)
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
            
            if i < 30:
                status_text.text("🔍 Scanning donor database...")
            elif i < 60:
                status_text.text("📍 Calculating distances...")
            elif i < 90:
                status_text.text("🤖 Sorting donors by proximity...")
            else:
                status_text.text("✅ Found donors - nearest first!")
        
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
                    alerts.append({
                        'blood_type': bt,
                        'current_stock': units
                    })
        
        return alerts, blood_type_status
    
    def display_inventory_dashboard(self):
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
    def register_hospital(self, hospital_data):
        try:
            hospital_id = generate_id('HOSP')
            coords = get_coords(f"{hospital_data.get('address', '')}, {hospital_data.get('city', '')}")
            lat, lon = coords if coords else (None, None)
            
            execute_query(
                """INSERT INTO hospitals 
                   (hospital_id, name, registration_number, address, city, state, 
                    phone, email, emergency_contact, license_number, registration_date,
                    latitude, longitude, blood_bank_capacity, accreditation)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (hospital_id, hospital_data.get('name'), hospital_data.get('reg_number'),
                 hospital_data.get('address'), hospital_data.get('city'), hospital_data.get('state'),
                 hospital_data.get('phone'), hospital_data.get('email'), hospital_data.get('emergency_contact'),
                 hospital_data.get('license'), datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 lat, lon, hospital_data.get('capacity'), hospital_data.get('accreditation', 'Pending')),
                commit=True
            )
            return True, hospital_id
        except Exception as e:
            return False, str(e)
    
    def get_nearby_hospitals(self, location, radius_km=20):
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
# DONATION EVENTS MANAGEMENT
# ============================================

class DonationEventManager:
    def __init__(self):
        self.blood_types = BLOOD_TYPES
    
    def create_event(self, event_data, organizer_id=None):
        try:
            event_id = generate_id('EVT')
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            coords = get_coords(event_data.get('location'))
            lat, lon = coords if coords else (None, None)
            
            blood_types_needed = json.dumps(event_data.get('blood_types_needed', []))
            amenities = json.dumps(event_data.get('amenities', []))
            incentives = json.dumps(event_data.get('incentives', []))
            
            execute_query(
                """INSERT INTO donation_events 
                   (event_id, event_name, organizer, organizer_id, organizer_email, organizer_phone,
                    location, address, city, start_date, end_date, start_time, end_time,
                    target_donations, registered_donors, completed_donations, status,
                    contact_person, contact_phone, contact_email, description, latitude, longitude,
                    amenities, blood_types_needed, incentives, special_instructions, created_date,
                    min_age, max_age, min_weight, is_featured, registration_deadline, notified_donors)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (event_id, event_data.get('event_name'), event_data.get('organizer'),
                 organizer_id, event_data.get('organizer_email'), event_data.get('organizer_phone'),
                 event_data.get('location'), event_data.get('address'), event_data.get('city'),
                 event_data.get('start_date'), event_data.get('end_date'),
                 event_data.get('start_time'), event_data.get('end_time'),
                 event_data.get('target_donations', 0), 0, 0,
                 event_data.get('status', 'Upcoming'),
                 event_data.get('contact_person'), event_data.get('contact_phone'),
                 event_data.get('contact_email'), event_data.get('description'),
                 lat, lon, amenities, blood_types_needed, incentives,
                 event_data.get('special_instructions'), current_time,
                 event_data.get('min_age', 18), event_data.get('max_age', 65),
                 event_data.get('min_weight', 45), event_data.get('is_featured', 0),
                 event_data.get('registration_deadline'), 0),
                commit=True
            )
            
            event = execute_query(
                "SELECT * FROM donation_events WHERE event_id=?",
                (event_id,),
                fetch_one=True
            )
            
            if event:
                event_dict = dict(event)
                self.notify_all_donors(event_id, event_dict, lat, lon)
            
            return True, event_id
            
        except Exception as e:
            return False, str(e)
    
    def notify_all_donors(self, event_id, event_data, lat, lon):
        try:
            donors = execute_query(
                "SELECT * FROM donors WHERE email IS NOT NULL",
                fetch_all=True
            ) or []
            
            sent_count = 0
            for donor in donors:
                try:
                    if donor.get('email') and is_valid_email(donor.get('email')):
                        distance = None
                        if lat and lon and donor.get('latitude') and donor.get('longitude'):
                            try:
                                distance = geodesic((lat, lon), (donor['latitude'], donor['longitude'])).km
                            except:
                                pass
                        
                        send_event_notification_email(
                            donor.get('email'),
                            donor.get('name', 'Donor'),
                            event_data,
                            distance
                        )
                        sent_count += 1
                        time.sleep(0.1)
                except:
                    continue
            
            execute_query(
                "UPDATE donation_events SET notified_donors=? WHERE event_id=?",
                (sent_count, event_id),
                commit=True
            )
            
            return True
        except:
            return False
    
    def get_nearby_events(self, location, radius_km=50):
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
        except:
            return []
    
    def register_for_event(self, event_id, donor):
        try:
            existing = execute_query(
                "SELECT id FROM event_registrations WHERE event_id=? AND donor_id=?",
                (event_id, donor['id']),
                fetch_one=True
            )
            
            if existing:
                return False, "Already registered"
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            execute_query(
                """INSERT INTO event_registrations 
                   (event_id, donor_id, donor_name, donor_email, donor_phone, donor_blood,
                    registration_date, attended)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (event_id, donor['id'], donor.get('name'), donor.get('email'),
                 donor.get('phone'), donor.get('blood'), current_time, 0),
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
            
            add_notification(
                donor.get('email'),
                '✅ Event Registration Confirmed',
                f"You have successfully registered for {event.get('event_name')}"
            )
            
            return True, "Registration successful"
            
        except Exception as e:
            return False, str(e)
    
    def display_event_card(self, event):
        if not event:
            return
        
        status_class = "status-upcoming"
        if event.get('status') == 'Ongoing':
            status_class = "status-ongoing"
        
        target = event.get('target_donations', 0) or 0
        registered = event.get('registered_donors', 0) or 0
        progress = (registered / target * 100) if target > 0 else 0
        
        st.markdown(f"""
        <div class='event-card'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <h3>{event.get('event_name')}</h3>
                <span class='event-status {status_class}'>{event.get('status')}</span>
            </div>
            <div class='event-stats'>
                <div class='stat-item'>
                    <div class='stat-value'>{registered}</div>
                    <div class='stat-label'>Registered</div>
                </div>
                <div class='stat-item'>
                    <div class='stat-value'>{target}</div>
                    <div class='stat-label'>Target</div>
                </div>
            </div>
            <p><strong>📅 Date:</strong> {event.get('start_date')} at {event.get('start_time')}</p>
            <p><strong>📍 Location:</strong> {event.get('location')}</p>
            <div class='custom-progress'>
                <div class='custom-progress-bar' style='width: {progress}%;'></div>
            </div>
            {f"<p><strong>📍 Distance:</strong> {event.get('distance')} km</p>" if event.get('distance') else ""}
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
        except:
            return None
    
    def generate_event_qr(self, event_id, event_data):
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
        except:
            return None

# ============================================
# REWARDS MANAGER
# ============================================

class RewardsManager:
    def get_available_rewards(self, category=None):
        try:
            query = "SELECT * FROM rewards WHERE available=1 AND stock>0"
            params = []
            
            if category and category != 'All':
                query += " AND category=?"
                params.append(category)
            
            query += " ORDER BY points_required ASC"
            
            return execute_query(query, params, fetch_all=True) or []
        except:
            return []
    
    def get_donor_points_summary(self, donor_id):
        try:
            if not donor_id:
                return None
                
            donor = execute_query(
                "SELECT points, donor_level FROM donors WHERE id=?",
                (donor_id,),
                fetch_one=True
            )
            
            if not donor:
                return None
            
            return {
                'current_points': donor.get('points', 0),
                'level': donor.get('donor_level', 'New Donor 🌟')
            }
        except:
            return None

# ============================================
# CHAT MANAGER
# ============================================

class ChatManager:
    def send_message(self, sender_id, receiver_id, message):
        try:
            message_id = generate_id('CHAT')
            conversation_id = f"conv_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
            
            execute_query(
                "INSERT INTO chat_messages (message_id, sender_id, receiver_id, message, timestamp, conversation_id) VALUES (?, ?, ?, ?, ?, ?)",
                (message_id, sender_id, receiver_id, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), conversation_id),
                commit=True
            )
            return True, message_id
        except:
            return False, "Error"
    
    def get_conversation(self, user1_id, user2_id, limit=50):
        try:
            conversation_id = f"conv_{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"
            
            messages = execute_query(
                "SELECT * FROM chat_messages WHERE conversation_id=? ORDER BY timestamp ASC LIMIT ?",
                (conversation_id, limit),
                fetch_all=True
            ) or []
            
            return messages
        except:
            return []
    
    def get_unread_count(self, user_id):
        try:
            result = execute_query(
                "SELECT COUNT(*) as count FROM chat_messages WHERE receiver_id=? AND read=0",
                (user_id,),
                fetch_one=True
            )
            return result['count'] if result else 0
        except:
            return 0
    
    def display_chat_interface(self, current_user_id, other_user_id, other_user_name):
        st.subheader(f"💬 Chat with {other_user_name}")
        
        messages = self.get_conversation(current_user_id, other_user_id)
        
        for msg in messages:
            if msg.get('sender_id') == current_user_id:
                st.markdown(f"""
                <div class='chat-bubble sent'>
                    <strong>You:</strong><br>
                    {msg.get('message')}<br>
                    <small>{msg.get('timestamp')}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='chat-bubble received'>
                    <strong>{other_user_name}:</strong><br>
                    {msg.get('message')}<br>
                    <small>{msg.get('timestamp')}</small>
                </div>
                """, unsafe_allow_html=True)
        
        new_message = st.text_input("Type your message...")
        if st.button("Send"):
            if new_message:
                self.send_message(current_user_id, other_user_id, new_message)
                st.rerun()

# ============================================
# DONOR IMPACT VISUALIZER
# ============================================

class DonorImpactVisualizer:
    def calculate_donor_impact(self, donor_id):
        try:
            donations = execute_query(
                "SELECT COUNT(*) as count FROM donation_history WHERE donor_id=?",
                (donor_id,),
                fetch_one=True
            )
            count = donations['count'] if donations else 0
            
            return {
                'donations': count,
                'lives_saved': count,
                'events': 0,
                'total_distance': 0
            }
        except:
            return {'donations': 0, 'lives_saved': 0, 'events': 0, 'total_distance': 0}
    
    def create_impact_dashboard(self, donor_id, donor_name):
        impact = self.calculate_donor_impact(donor_id)
        
        st.subheader(f"🌟 {donor_name}'s Impact Dashboard")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Donations", impact.get('donations', 0))
        with col2:
            st.metric("Lives Saved", impact.get('lives_saved', 0))
        with col3:
            st.metric("Events Attended", impact.get('events', 0))
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea20, #764ba220); padding: 2rem; border-radius: 15px; text-align: center;'>
            <h2>🎉 {donor_name}, you've saved {impact.get('lives_saved', 0)} lives!</h2>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# SIDEBAR SETUP
# ============================================

st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <h1 style='color: #ff6b6b; font-size: 2.5rem;'>🩸 BloodAI</h1>
    <p style='color: #666;'>Complete Blood Donation System</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div class='db-status'>
    <strong>💾 Database:</strong> {db_status}<br>
    <small>{db_location}</small>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📊 Quick Stats")
selected_blood = st.sidebar.selectbox("Blood Type", BLOOD_TYPES, key="sidebar_blood")

total_result = execute_query("SELECT COUNT(*) as count FROM donors WHERE blood=?", (selected_blood,), fetch_one=True)
total = total_result['count'] if total_result else 0

eligible_donors = get_eligible_donors(selected_blood)
eligible_count = len(eligible_donors)

st.sidebar.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea20, #764ba220); padding: 1rem; border-radius: 10px;'>
    <p><strong>🩸 {selected_blood}</strong></p>
    <p>✅ Eligible: {eligible_count}</p>
    <p>📊 Total: {total}</p>
</div>
""", unsafe_allow_html=True)

inventory_manager = BloodInventoryManager()
alerts, _ = inventory_manager.check_stock_alerts()
if alerts:
    st.sidebar.warning(f"⚠️ {len(alerts)} stock alerts")

event_count = execute_query("SELECT COUNT(*) as count FROM donation_events WHERE status IN ('Upcoming', 'Ongoing')", fetch_one=True)
upcoming_events = event_count['count'] if event_count else 0
if upcoming_events > 0:
    st.sidebar.info(f"🎪 {upcoming_events} upcoming events")

st.sidebar.markdown("---")

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
st.sidebar.info(f"⏱️ Response: {WAIT_MINUTES} min per donor")
st.sidebar.markdown("📍 **Closest donors contacted first**")

# ============================================
# MAIN CONTENT
# ============================================

if not st.session_state.get('showing_response', False):
    
    # ============================================
    # HOME
    # ============================================
    
    if menu == "🏠 Home":
        st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 3rem;'>🩸 BloodAI Complete System</h1>
            <p style='font-size: 1.5rem;'>All Donors Notified • Closest First • 2-Minute Rotation</p>
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
            completed = execute_query("SELECT COUNT(*) as count FROM donation_history", fetch_one=True)
            lives_saved = completed['count'] if completed else 0
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{lives_saved}</div><div>Lives Saved</div></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📦 Current Blood Inventory")
        inventory_manager.display_inventory_dashboard()
        
        st.markdown("---")
        st.subheader("🌟 System Features")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>📍</div>
                <div class='feature-title'>Location-Based Matching</div>
                <div class='feature-description'>All donors sorted by distance - closest first</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>📧</div>
                <div class='feature-title'>All Donors Notified</div>
                <div class='feature-description'>Every eligible donor gets an email in order</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>🎪</div>
                <div class='feature-title'>Donation Events</div>
                <div class='feature-description'>Create events & notify ALL donors instantly</div>
            </div>
            """, unsafe_allow_html=True)

    # ============================================
    # DONOR REGISTER
    # ============================================

    elif menu == "📝 Donor Register":
        st.title("📝 Donor Registration")
        st.info("📍 Your location helps us prioritize you based on distance to patients")
        
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
                location = st.text_input("Full Address/Location*", 
                                        help="Enter complete address with city and pincode")
                weight = st.number_input("Weight (kg)*", min_value=45, value=70)
                emergency_contact = st.text_input("Emergency Contact")
                medical_id = st.text_input("Medical ID (Optional)")
            
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
                                   (donor_id, name, email, phone, blood, location, latitude, longitude, password, 
                                    registration_date, weight, age, gender, emergency_contact, medical_id, health_conditions,
                                    points, donor_level, is_verified)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (donor_id, name, email, phone, blood, location, lat, lon,
                                 hash_password(password), current_time, weight, age, gender,
                                 emergency_contact, medical_id, health_conditions,
                                 0, "New Donor 🌟", 1 if coords else 0),
                                commit=True
                            )
                            
                            donor_details = {'donor_id': donor_id, 'blood': blood, 'location': location}
                            send_welcome_email(email, name, donor_details)
                            
                            st.success("✅ Registration successful!")
                            
                            if coords:
                                qr_manager = QRCodeManager()
                                donor_data = {
                                    'name': name,
                                    'blood': blood,
                                    'donor_level': 'New Donor 🌟',
                                    'total_donations': 0,
                                    'medical_id': medical_id,
                                    'emergency_contact': emergency_contact,
                                    'is_verified': 1
                                }
                                qr_code = qr_manager.generate_donor_qr(donor_id, donor_data)
                                if qr_code:
                                    st.image(qr_code, caption="Your Donor QR Code", width=200)
                            
                            st.balloons()
                            
                        except sqlite3.IntegrityError:
                            st.error("Email already registered")

    # ============================================
    # PATIENT REQUEST
    # ============================================

    elif menu == "🆘 Patient Request":
        st.title("🆘 Emergency Blood Request")
        
        total_donors_count = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
        total_donors = total_donors_count['count'] if total_donors_count else 0
        st.info(f"📊 Total donors in system: {total_donors}")
        st.info(f"⏱️ All donors contacted in order of distance. Each has {WAIT_MINUTES} minutes to respond.")
        
        with st.form("request_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                patient = st.text_input("Patient Name*")
                email = st.text_input("Your Email*")
                blood = st.selectbox("Blood Type Needed*", BLOOD_TYPES)
                patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=30)
            
            with col2:
                location = st.text_input("Hospital Location*", 
                                        help="Enter complete hospital address")
                hospital = st.text_input("Hospital Name*")
                doctor = st.text_input("Doctor's Name")
                hospital_contact = st.text_input("Hospital Contact")
            
            urgency = st.select_slider("Urgency", options=["Normal", "High", "Critical"], value="High")
            units = st.number_input("Units Needed", min_value=1, max_value=10, value=1)
            reason = st.text_area("Reason for transfusion")
            
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
                        
                        show_donor_search()
                        all_donors = get_all_donors_sorted_by_distance(blood, location)
                        
                        if not all_donors:
                            st.error(f"❌ No donors found with blood type {blood}!")
                            
                            request_id = generate_id('REQ')
                            current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            execute_query(
                                """INSERT INTO requests 
                                   (request_id, patient, patient_email, blood, location, latitude, longitude, hospital, 
                                    status, time, urgency_level, units_needed, patient_age, reason, total_donors_count)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (request_id, patient, email, blood, location, lat, lon, hospital,
                                 "No Donors Available", current_time_str, urgency, units,
                                 patient_age, reason, 0),
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
                                    status, time, urgency_level, units_needed, patient_age, reason, all_donors, total_donors_count)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (request_id, patient, email, blood, location, lat, lon, hospital,
                                 "Pending", current_time_str, urgency, units,
                                 patient_age, reason, donors_json, len(all_donors)),
                                commit=True
                            )
                            
                            nearest_distance = all_donors[0].get('distance_km')
                            if nearest_distance and nearest_distance != 999999:
                                distance_str = f"{nearest_distance} km"
                            else:
                                distance_str = "unknown distance"
                            
                            st.success(f"✅ Request submitted! {len(all_donors)} donors will be contacted.")
                            st.markdown(f"""
                            <div class='location-priority'>
                                <h3 style='color: #43e97b;'>📍 Donor Queue Information</h3>
                                <p><strong>Closest Donor:</strong> {all_donors[0].get('name')} ({distance_str})</p>
                                <p><strong>Total Donors Found:</strong> {len(all_donors)}</p>
                                <p><strong>First email sent to nearest donor!</strong></p>
                            </div>
                            """, unsafe_allow_html=True)

    # ============================================
    # TRACK REQUEST
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
                            status_emoji = {
                                "Pending": "⏳",
                                "Accepted": "✅",
                                "No Donors Available": "❌"
                            }.get(req.get('status'), "📝")
                            
                            with st.expander(f"{status_emoji} Request #{req.get('id')} - {req.get('blood')}"):
                                st.markdown(f"""
                                **Patient:** {req.get('patient')}
                                **Blood Type:** {req.get('blood')}
                                **Hospital:** {req.get('hospital')}
                                **Status:** {req.get('status')}
                                **Request Time:** {req.get('time')}
                                **Total Donors:** {req.get('total_donors_count', 0)}
                                """)
                                
                                if req.get('status') == "Pending":
                                    if req.get('last_contacted_time'):
                                        try:
                                            last = datetime.strptime(req['last_contacted_time'], "%Y-%m-%d %H:%M:%S")
                                            elapsed = datetime.now() - last
                                            remaining = max(0, WAIT_MINUTES - (elapsed.total_seconds() / 60))
                                            
                                            contacted = [x for x in req.get('contacted', '').split(',') if x]
                                            total = req.get('total_donors_count', 0)
                                            progress = len(contacted)
                                            
                                            if total > 0:
                                                st.write(f"**Donors Contacted:** {progress}/{total}")
                                                st.progress(progress/total)
                                            
                                            if remaining > 0 and progress < total:
                                                st.warning(f"⏳ Next donor in {remaining:.1f} minutes")
                                            elif progress >= total:
                                                st.warning("All donors contacted. No one accepted.")
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
                                        **Donor:** {donor.get('name')}
                                        **Phone:** {donor.get('phone')}
                                        """)
                    else:
                        st.info("No requests found")

    # ============================================
    # DONOR LEADERBOARD
    # ============================================

    elif menu == "🏆 Donor Leaderboard":
        st.title("🏆 Donor Leaderboard")
        
        top_donors = execute_query(
            "SELECT name, total_donations, donor_level, blood FROM donors WHERE total_donations > 0 ORDER BY total_donations DESC LIMIT 20",
            fetch_all=True
        ) or []
        
        if top_donors:
            df = pd.DataFrame(top_donors)
            df.insert(0, "Rank", range(1, len(df) + 1))
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No donations yet")

    # ============================================
    # NOTIFICATIONS
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
        if st.session_state.logged_in_donor is not None:
            donor = st.session_state.logged_in_donor
            
            donor = execute_query(
                "SELECT * FROM donors WHERE id=?",
                (donor['id'],),
                fetch_one=True
            )
            
            if donor:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown("<h1 style='font-size: 5rem;'>🩸</h1>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<h2>{donor.get('name')}</h2><p>{donor.get('donor_level')} • {donor.get('blood')}</p>", unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Donations", donor.get('total_donations', 0))
                with col2:
                    st.metric("Points", donor.get('points', 0))
                with col3:
                    st.metric("Level", donor.get('donor_level', 'New'))
                with col4:
                    eligible, msg = is_donor_eligible(donor)
                    st.metric("Status", "✅ Eligible" if eligible else "⏳ Cooldown", help=msg)
                
                st.markdown("---")
                st.subheader("Donation History")
                history = execute_query(
                    "SELECT * FROM donation_history WHERE donor_id=? ORDER BY donation_date DESC",
                    (donor['id'],),
                    fetch_all=True
                ) or []
                
                if history:
                    st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)
                else:
                    st.info("No donation history yet")
                
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
    # HOSPITALS
    # ============================================

    elif menu == "🏥 Hospitals":
        st.title("🏥 Hospitals")
        
        location = st.text_input("Enter your location to find nearby hospitals")
        
        if location:
            hospital_manager = HospitalManager()
            nearby = hospital_manager.get_nearby_hospitals(location)
            
            if nearby:
                for hospital in nearby:
                    with st.expander(f"🏥 {hospital.get('name')} - {hospital.get('distance', 0)} km"):
                        st.markdown(f"""
                        **Address:** {hospital.get('address')}
                        **Phone:** {hospital.get('phone')}
                        **Email:** {hospital.get('email')}
                        """)
            else:
                st.info("No hospitals found")

    # ============================================
    # BLOOD INVENTORY
    # ============================================

    elif menu == "📦 Blood Inventory":
        st.title("📦 Blood Inventory")
        inventory_manager.display_inventory_dashboard()

    # ============================================
    # DONATION EVENTS
    # ============================================

    elif menu == "🎪 Donation Events":
        st.title("🎪 Donation Events")
        
        event_manager = DonationEventManager()
        
        tab1, tab2, tab3 = st.tabs(["📋 Browse Events", "➕ Create Event", "📊 My Registrations"])
        
        with tab1:
            st.subheader("Find Donation Events Near You")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                location = st.text_input("Enter your location to find nearby events")
            with col2:
                radius = st.number_input("Search radius (km)", min_value=5, max_value=200, value=50)
            
            if location:
                with st.spinner("🔍 Finding events..."):
                    events = event_manager.get_nearby_events(location, radius)
                
                if events:
                    st.success(f"Found {len(events)} events near you!")
                    for event in events:
                        event_manager.display_event_card(event)
                        
                        if st.session_state.logged_in_donor is not None:
                            if st.button(f"📝 Register", key=f"reg_{event.get('id')}"):
                                success, message = event_manager.register_for_event(
                                    event.get('id'), 
                                    st.session_state.logged_in_donor
                                )
                                if success:
                                    st.success(message)
                                    st.balloons()
                                else:
                                    st.error(message)
                        else:
                            st.info("Please login to register")
                else:
                    st.info("No events found")
        
        with tab2:
            st.subheader("➕ Create New Donation Event")
            st.info("📢 ALL registered donors will receive email notifications!")
            
            total_donors = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
            donor_count = total_donors['count'] if total_donors else 0
            st.info(f"📧 This event will be notified to {donor_count} donors")
            
            with st.form("create_event_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    event_name = st.text_input("Event Name*")
                    organizer = st.text_input("Organizer Name*")
                    organizer_email = st.text_input("Organizer Email*")
                    organizer_phone = st.text_input("Organizer Phone*")
                    
                    start_date = st.date_input("Start Date*", min_value=date.today())
                    end_date = st.date_input("End Date*", min_value=start_date)
                    
                    start_time = st.time_input("Start Time*")
                    end_time = st.time_input("End Time*")
                
                with col2:
                    location = st.text_input("Event Location*")
                    address = st.text_area("Detailed Address*")
                    city = st.text_input("City*")
                    
                    contact_person = st.text_input("Contact Person*")
                    contact_phone = st.text_input("Contact Phone*")
                    contact_email = st.text_input("Contact Email*")
                    
                    target_donations = st.number_input("Target Donations*", min_value=1, value=50)
                
                blood_types_needed = st.multiselect("Blood Types Needed*", BLOOD_TYPES, default=BLOOD_TYPES)
                description = st.text_area("Event Description")
                
                submitted = st.form_submit_button("🚀 Create Event")
                
                if submitted:
                    if not all([event_name, organizer, location, blood_types_needed]):
                        st.error("Please fill all required fields")
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
                            'status': 'Upcoming'
                        }
                        
                        organizer_id = st.session_state.logged_in_donor['id'] if st.session_state.logged_in_donor else None
                        
                        with st.spinner("Creating event..."):
                            success, result = event_manager.create_event(event_data, organizer_id)
                        
                        if success:
                            st.success("✅ Event created successfully!")
                            st.balloons()
                            
                            qr_manager = QRCodeManager()
                            qr_code = qr_manager.generate_event_qr(result, event_data)
                            if qr_code:
                                st.image(qr_code, caption="Event QR Code", width=200)
                        else:
                            st.error(f"Failed: {result}")
        
        with tab3:
            if st.session_state.logged_in_donor is not None:
                st.subheader("My Event Registrations")
                st.info("You haven't registered for any events yet")
            else:
                st.warning("Please login to view registrations")

    # ============================================
    # REWARDS STORE
    # ============================================

    elif menu == "🎁 Rewards Store":
        st.title("🎁 Rewards Store")
        
        rewards_manager = RewardsManager()
        
        if st.session_state.logged_in_donor is not None:
            donor = st.session_state.logged_in_donor
            summary = rewards_manager.get_donor_points_summary(donor['id'])
            if summary:
                st.markdown(f"### Your Points: {summary.get('current_points', 0)}")
                st.markdown(f"### Your Level: {summary.get('level', 'New Donor 🌟')}")
        
        rewards = rewards_manager.get_available_rewards()
        if rewards:
            cols = st.columns(3)
            for i, reward in enumerate(rewards):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class='reward-card'>
                        <h3>{reward.get('item_name', '')}</h3>
                        <p>{reward.get('points_required', 0)} points</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No rewards available")

    # ============================================
    # CHAT
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
            
            others = execute_query(
                "SELECT id, name FROM donors WHERE id != ? LIMIT 10",
                (donor_id,),
                fetch_all=True
            ) or []
            
            if others:
                st.subheader("Select a donor to chat with:")
                for other in others:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"💬 {other.get('name')}")
                    with col2:
                        if st.button("Chat", key=f"chat_{other.get('id')}"):
                            st.session_state.current_conversation = other.get('id')
                            st.rerun()
                
                if st.session_state.current_conversation is not None:
                    other_id = st.session_state.current_conversation
                    other = execute_query(
                        "SELECT name FROM donors WHERE id=?",
                        (other_id,),
                        fetch_one=True
                    )
                    
                    if other:
                        chat_manager.display_chat_interface(donor_id, other_id, other.get('name'))
            else:
                st.info("No other donors found")

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
            
            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Donors", "Requests", "Events"])
            
            with tab1:
                total_donors = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
                total_donors = total_donors['count'] if total_donors else 0
                total_requests = execute_query("SELECT COUNT(*) as count FROM requests", fetch_one=True)
                total_requests = total_requests['count'] if total_requests else 0
                total_donations = execute_query("SELECT COUNT(*) as count FROM donation_history", fetch_one=True)
                total_donations = total_donations['count'] if total_donations else 0
                total_events = execute_query("SELECT COUNT(*) as count FROM donation_events", fetch_one=True)
                total_events = total_events['count'] if total_events else 0
                pending = execute_query("SELECT COUNT(*) as count FROM requests WHERE status='Pending'", fetch_one=True)
                pending = pending['count'] if pending else 0
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Donors", total_donors)
                col2.metric("Total Requests", total_requests)
                col3.metric("Total Events", total_events)
                col4.metric("Pending Requests", pending)
            
            with tab2:
                donors = execute_query("SELECT * FROM donors ORDER BY registration_date DESC", fetch_all=True) or []
                if donors:
                    df = pd.DataFrame(donors)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    csv = df.to_csv(index=False)
                    st.download_button("📥 Download CSV", csv, "donors.csv", "text/csv")
            
            with tab3:
                requests = execute_query("SELECT * FROM requests ORDER BY id DESC", fetch_all=True) or []
                if requests:
                    df = pd.DataFrame(requests)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            
            with tab4:
                events = execute_query("SELECT * FROM donation_events ORDER BY start_date DESC", fetch_all=True) or []
                if events:
                    df = pd.DataFrame(events)
                    st.dataframe(df, use_container_width=True, hide_index=True)

    # ============================================
    # EMAIL LOG
    # ============================================

    elif menu == "📧 Email Log":
        st.title("📧 Email Log")
        
        logs = execute_query(
            "SELECT * FROM email_log ORDER BY sent_date DESC LIMIT 50",
            fetch_all=True
        ) or []
        
        if logs:
            for log in logs:
                color = "#43e97b" if log.get('status') == 'sent' else "#ff6b6b"
                st.markdown(f"""
                <div style='border-left: 5px solid {color}; background: #f9f9f9; padding: 1rem; margin: 0.5rem 0; border-radius: 5px;'>
                    <p><strong>{log.get('sent_date')}</strong> - {log.get('recipient')}</p>
                    <p>{log.get('subject')}</p>
                    <p style='color: {color};'>Status: {log.get('status')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No emails sent yet")

    # ============================================
    # FOOTER
    # ============================================

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <p>BloodAI v19.0 - Complete System</p>
        <p>📍 <strong>Closest First • {WAIT_MINUTES} Min Response</strong></p>
        <p>💾 <strong>{db_status}</strong></p>
        <p>📧 <strong>Email Notifications Active</strong></p>
    </div>
    """, unsafe_allow_html=True)
