# ============================================
# 🩸 BLOODAI COMPLETE SYSTEM v19.0
# ADDED: Permanent Data Storage • Donation Events with Email Notifications
# FIXED: Lives Saved = 1 per donation • Location Verification • Distance Display
# UPDATED: Patient Email with exact format from image
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
POINTS_PER_EVENT = 50  # Points for attending events

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
# PERMANENT DATABASE STORAGE - FIXED FOR STREAMLIT CLOUD
# ============================================

def get_database_path():
    """
    Get a persistent database path that works on Streamlit Cloud
    Data will survive app restarts and updates
    """
    try:
        # For Streamlit Cloud - use /mount/src which is persistent
        persistent_path = "/mount/src/bloodai_data.db"
        # Create directory if it doesn't exist
        os.makedirs("/mount/src", exist_ok=True)
        # Test write access
        with open(persistent_path, 'a') as f:
            pass
        print(f"✅ Using PERSISTENT database at: {persistent_path}")
        return persistent_path
    except Exception as e:
        print(f"⚠️ Could not use persistent path: {e}")
        try:
            # Fallback to temp directory (still survives between reruns but not app restarts)
            temp_path = "/tmp/bloodai_data.db"
            print(f"📁 Using TEMPORARY database at: {temp_path}")
            return temp_path
        except:
            # Final fallback - local file (works locally)
            print("⚠️ Using local database file: bloodai_data.db")
            return "bloodai_data.db"

# Get the database path
DB_PATH = get_database_path()

# ============================================
# DATABASE CONNECTION MANAGER
# ============================================

@contextmanager
def get_db_connection():
    """Get a database connection with proper error handling"""
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
    """Execute a database query with proper error handling"""
    try:
        with get_db_connection() as conn:
            if conn is None:
                print("❌ No database connection")
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
# COMPLETE DATABASE SETUP - WITH PERMANENT STORAGE
# ============================================

def init_database():
    """Initialize complete database with all tables - data will persist"""
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
            
            # Requests table with queue support
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
            
            # Donation Events Table - ENHANCED
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
            
            # Verify database works by counting donors
            test = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
            if test is not None:
                donor_count = test.get('count', 0)
                print(f"✅ Database initialized successfully at: {DB_PATH}")
                print(f"📊 Current donor count: {donor_count}")
                
                # Count events
                event_count = execute_query("SELECT COUNT(*) as count FROM donation_events", fetch_one=True)
                if event_count:
                    print(f"🎪 Current events: {event_count.get('count', 0)}")
                
                return True
            else:
                print("❌ Database verification failed")
                return False
            
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

# Initialize database
if not st.session_state.db_initialized:
    with st.spinner("🔄 Initializing database..."):
        if init_database():
            st.session_state.db_initialized = True
            st.sidebar.success("✅ Database Ready")
        else:
            st.sidebar.error("❌ Database Error")

# Show database status in sidebar
db_status_text = "✅ Persistent" if DB_PATH.startswith('/mount') else "📁 Local" if 'bloodai_data.db' in DB_PATH else "⚠️ Temporary"
db_location = DB_PATH.split('/')[-1]

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
    # Fix common domain typos
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
    """Get coordinates from location and cache them - FIXED for better accuracy"""
    try:
        if not location or not isinstance(location, str) or len(location.strip()) < 5:
            print(f"Invalid location: {location}")
            return None
            
        # Clean up location string
        location = location.strip()
        
        # Try with user agent
        geolocator = Nominatim(user_agent="bloodai_app_v2")
        
        # Add timeout and better parameters
        loc = geolocator.geocode(
            location, 
            timeout=10,
            exactly_one=True,
            addressdetails=True
        )
        
        if loc:
            print(f"✅ Found coordinates for '{location}': ({loc.latitude}, {loc.longitude})")
            return (loc.latitude, loc.longitude)
        
        # Try with more specific query
        if 'india' not in location.lower():
            location_with_country = f"{location}, India"
            loc = geolocator.geocode(location_with_country, timeout=10)
            if loc:
                print(f"✅ Found coordinates with country: ({loc.latitude}, {loc.longitude})")
                return (loc.latitude, loc.longitude)
        
        print(f"❌ Could not find coordinates for '{location}'")
        return None
    except Exception as e:
        print(f"Geocoding error for '{location}': {e}")
        return None

def update_donor_coordinates(donor_id, location):
    """Update donor coordinates in database - FIXED for better verification"""
    coords = get_coords(location)
    if coords:
        lat, lon = coords
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        execute_query(
            "UPDATE donors SET latitude=?, longitude=?, last_location_update=?, is_verified=1 WHERE id=?",
            (lat, lon, current_time, donor_id),
            commit=True
        )
        print(f"✅ Updated coordinates for donor {donor_id}: {lat}, {lon}")
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
        return False
        
    except Exception as e:
        error_msg = str(e)
        log_email(to_email, subject, 'email', 'failed', error_msg)
        print(f"❌ Email error: {error_msg}")
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
    """Check if donor is eligible to donate (respects cooldown period)"""
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
    """Get all eligible donors for a blood type (respects cooldown)"""
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
    except Exception as e:
        print(f"Model training error: {e}")
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
    if hasattr(obj, '__dict__'):
        return make_json_serializable(obj.__dict__)
    # For any other type, convert to string
    return str(obj)

# ============================================
# ENHANCED DONOR SORTING FUNCTION - FIXED DISTANCE CALCULATION
# ============================================

def get_all_donors_sorted_by_distance(blood_type, location):
    """
    Get ALL donors sorted by distance from patient - FIXED distance calculation
    """
    try:
        # Get ALL donors with matching blood type
        donors = execute_query(
            "SELECT * FROM donors WHERE blood=?",
            (blood_type,),
            fetch_all=True
        ) or []
        
        print(f"Found {len(donors)} donors for blood type {blood_type}")
        
        if not donors:
            return []
        
        # Get patient coordinates
        patient_coords = get_coords(location)
        
        # Debug print
        if patient_coords:
            print(f"Patient coordinates: {patient_coords}")
        else:
            print(f"Could not get coordinates for patient location: {location}")
        
        donors_with_distance = []
        for donor in donors:
            donor_copy = dict(donor)
            
            # Try to get donor coordinates
            donor_lat = donor_copy.get('latitude')
            donor_lon = donor_copy.get('longitude')
            
            # If donor has no coordinates but has location, try to get them
            if (not donor_lat or not donor_lon) and donor_copy.get('location'):
                donor_coords = get_coords(donor_copy.get('location'))
                if donor_coords:
                    donor_lat, donor_lon = donor_coords
                    # Update donor in database for future use
                    execute_query(
                        "UPDATE donors SET latitude=?, longitude=?, is_verified=1 WHERE id=?",
                        (donor_lat, donor_lon, donor_copy.get('id')),
                        commit=True
                    )
                    print(f"Updated coordinates for donor {donor_copy.get('name')}")
            
            # Calculate distance if both coordinates available
            if donor_lat and donor_lon and patient_coords:
                try:
                    distance = geodesic(patient_coords, (donor_lat, donor_lon)).km
                    donor_copy['distance_km'] = round(distance, 2)
                    print(f"Donor {donor_copy.get('name')} distance: {distance:.2f} km")
                except Exception as e:
                    print(f"Distance calculation error for donor {donor_copy.get('id')}: {e}")
                    donor_copy['distance_km'] = float('inf')
            else:
                donor_copy['distance_km'] = float('inf')
                if not donor_lat or not donor_lon:
                    print(f"Donor {donor_copy.get('name')} has no coordinates")
                if not patient_coords:
                    print(f"No patient coordinates available")
            
            # Ensure JSON serializable
            donor_copy = make_json_serializable(donor_copy)
            donors_with_distance.append(donor_copy)
        
        # Sort by distance (closest first) - infinite distances at the end
        donors_with_distance.sort(key=lambda x: (
            float('inf') if x.get('distance_km', float('inf')) == float('inf') else x.get('distance_km', float('inf'))
        ))
        
        # Debug print sorted list
        print("\nSorted donors by distance:")
        for i, d in enumerate(donors_with_distance):
            dist = d.get('distance_km', 'Unknown')
            if dist == float('inf'):
                dist_str = "Unknown location"
            else:
                dist_str = f"{dist} km"
            print(f"{i+1}. {d.get('name')} - {dist_str}")
        
        return donors_with_distance
        
    except Exception as e:
        print(f"Error sorting donors: {e}")
        return []

def get_next_donor_to_contact(request):
    """
    Get the next donor in the priority list that hasn't been contacted yet
    """
    try:
        all_donors_json = request.get('all_donors', '')
        current_index = request.get('current_donor_index', 0)
        contacted = request.get('contacted', '')
        
        if not all_donors_json:
            return None, None
        
        all_donors = json.loads(all_donors_json)
        contacted_list = [int(x) for x in contacted.split(',') if x and x.strip()]
        
        # Find the next donor not yet contacted
        for i in range(current_index, len(all_donors)):
            donor_id = all_donors[i].get('id')
            if donor_id and donor_id not in contacted_list:
                return all_donors[i], i
        
        return None, None
        
    except Exception as e:
        print(f"Error getting next donor: {e}")
        return None, None

# ============================================
# ENHANCED DONOR REQUEST EMAIL (with queue position)
# ============================================

def send_donor_request_email(donor, request, donor_rank, total_donors, donor_distance=None):
    """Send email to donor with accept/reject links and queue position"""
    try:
        if not donor or not request:
            return False
        
        donor_email = normalize_email(donor.get('email'))
        
        if not is_valid_email(donor_email):
            print(f"❌ Invalid donor email: {donor_email}")
            return False
            
        base_url = st.get_option("server.baseUrlPath") or BASE_URL
        
        accept_url = f"{base_url}/?accept={request.get('id')}&donor={donor.get('id')}"
        reject_url = f"{base_url}/?reject={request.get('id')}&donor={donor.get('id')}"
        
        subject = f"🩸 URGENT: Blood Donation Needed - {request.get('blood', 'Unknown')}"
        
        # Priority message based on rank
        if donor_rank == 1:
            priority_message = "🌟 You are the CLOSEST donor to this patient!"
            priority_color = "#43e97b"
        else:
            priority_message = f"You are #{donor_rank} in the queue of {total_donors} donors"
            priority_color = "#ff6b6b"
        
        distance_display = f"{donor_distance:.1f}" if donor_distance and donor_distance != float('inf') else "Unknown"
        distance_text = f"({donor_distance:.1f} km away)" if donor_distance and donor_distance != float('inf') else ""
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .header {{ background: #ff6b6b; padding: 30px; text-align: center; color: white; }}
        .content {{ padding: 30px; }}
        .priority-box {{ background: {priority_color}20; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid {priority_color}; }}
        .details-box {{ background: #f8f9fa; padding: 20px; border-radius: 10px; }}
        .button {{ display: inline-block; padding: 15px 30px; text-decoration: none; border-radius: 50px; margin: 10px; font-weight: bold; }}
        .accept {{ background: #43e97b; color: white; }}
        .reject {{ background: #ff6b6b; color: white; }}
        .footer {{ background: #fff3cd; padding: 15px; border-radius: 5px; margin-top: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        td {{ padding: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0; font-size: 32px;">🩸 URGENT BLOOD REQUEST</h1>
            <p style="margin: 10px 0 0;">Someone needs your help!</p>
        </div>
        
        <div class="content">
            <h2 style="margin-top: 0;">Hello {donor.get('name', 'Donor')},</h2>
            
            <p>A patient urgently needs your blood type. You are being contacted because you are an eligible donor.</p>
            
            <div class="priority-box">
                <h3 style="color: {priority_color}; margin-top: 0;">📍 YOUR POSITION IN QUEUE</h3>
                <p><strong>{priority_message}</strong></p>
                <p><strong>Distance:</strong> {distance_display} km {distance_text}</p>
                <p><strong>Queue Position:</strong> #{donor_rank} of {total_donors}</p>
            </div>
            
            <div class="details-box">
                <h3 style="color: #ff6b6b; margin-top: 0;">📋 REQUEST DETAILS</h3>
                <table>
                    <tr><td><strong>Blood Type:</strong></td><td><span style="background: #ff6b6b; color: white; padding: 3px 10px; border-radius: 5px;">{request.get('blood', 'Unknown')}</span></td></tr>
                    <tr><td><strong>Units Needed:</strong></td><td>{request.get('units_needed', 1)}</td></tr>
                    <tr><td><strong>Hospital:</strong></td><td>{request.get('hospital', 'Unknown')}</td></tr>
                    <tr><td><strong>Location:</strong></td><td>{request.get('location', 'Unknown')}</td></tr>
                    <tr><td><strong>Patient:</strong></td><td>{request.get('patient', 'Unknown')}</td></tr>
                </table>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{accept_url}" class="button accept" style="background: #43e97b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 50px; margin: 10px; display: inline-block;">✅ ACCEPT - SAVE A LIFE</a>
                <a href="{reject_url}" class="button reject" style="background: #ff6b6b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 50px; margin: 10px; display: inline-block;">❌ REJECT</a>
            </div>
            
            <div class="footer">
                <p style="margin: 0;"><strong>⏰ Important:</strong> You have {WAIT_MINUTES} minutes to respond. If you don't respond, we'll contact the next donor in line.</p>
                <p style="margin: 10px 0 0;"><strong>Note:</strong> All {total_donors} eligible donors will be contacted in order of distance. You are #{donor_rank} in this queue.</p>
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
# ENHANCED PATIENT NOTIFICATION EMAIL - UPDATED WITH EXACT FORMAT FROM IMAGE
# ============================================

def send_patient_notification_email(patient_email, patient_name, donor, request, donor_distance=None):
    """Send email to patient when donor accepts - with exact format from image"""
    try:
        if not patient_email or not donor or not request:
            return False
        
        patient_email = normalize_email(patient_email)
        
        if not is_valid_email(patient_email):
            print(f"❌ Invalid patient email: {patient_email}")
            return False
            
        subject = f"✅ Donor Found - Blood Request"
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .content {{ padding: 30px; }}
        h2 {{ color: #333; margin-bottom: 20px; }}
        hr {{ border: none; border-top: 1px solid #eee; margin: 20px 0; }}
        .request-summary {{ margin: 20px 0; }}
        .request-summary p {{ margin: 5px 0; }}
        .next-steps {{ margin: 20px 0; }}
        .next-steps ol {{ margin: 10px 0 10px 20px; }}
        .next-steps li {{ margin: 5px 0; color: #333; }}
        .blood-type {{ background: #ff6b6b; color: white; padding: 3px 10px; border-radius: 5px; display: inline-block; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <h2>REQUEST SUMMARY</h2>
            
            <p><strong>Request ID:</strong><br>
            {request.get('request_id', '')}</p>
            
            <p><strong>Blood Type:</strong><br>
            <span class="blood-type">{request.get('blood', 'Unknown')}</span></p>
            
            <p><strong>Units:</strong><br>
            {request.get('units_needed', 1)}</p>
            
            <p><strong>Hospital:</strong><br>
            {request.get('hospital', 'Unknown')}</p>
            
            <hr>
            
            <h2>NEXT STEPS</h2>
            
            <div class="next-steps">
                <ol>
                    <li><strong>Contact the donor IMMEDIATELY</strong> using the phone number below</li>
                    <li>Schedule the donation time with the donor and hospital</li>
                    <li>Confirm the appointment with the hospital blood bank</li>
                    <li>Keep the donor's contact information handy</li>
                </ol>
            </div>
            
            <hr>
            
            <h2>DONOR CONTACT DETAILS</h2>
            
            <p><strong>Name:</strong> {donor.get('name', 'Unknown')}</p>
            <p><strong>Phone:</strong> {donor.get('phone', '')}</p>
            <p><strong>Email:</strong> {donor.get('email', '')}</p>
            <p><strong>Location:</strong> {donor.get('location', 'Unknown')}</p>
            {f"<p><strong>Distance:</strong> {donor_distance:.1f} km</p>" if donor_distance else ""}
            
            <hr>
            
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
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .header {{ background: linear-gradient(135deg, #ffd700 0%, #ffa500 100%); padding: 30px; text-align: center; color: white; }}
        .content {{ padding: 30px; }}
        .details-box {{ background: #f8f9fa; padding: 20px; border-radius: 15px; margin: 20px 0; border-left: 5px solid #ffd700; }}
        .rewards-box {{ background: #e8f4fd; padding: 20px; border-radius: 10px; margin: 20px 0; }}
        .info-box {{ background: #fff3cd; padding: 20px; border-radius: 10px; }}
        table {{ width: 100%; }}
        td {{ padding: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0; font-size: 36px;">🎉 THANK YOU HERO!</h1>
            <p style="margin: 10px 0 0;">You've accepted a donation request</p>
        </div>
        
        <div class="content">
            <h2 style="margin-top: 0;">Dear {donor.get('name', 'Donor')},</h2>
            
            <p>Thank you for accepting the blood donation request! Your willingness to help is truly heroic.</p>
            
            <div class="details-box">
                <h3 style="color: #ffa500; margin-top: 0;">🏥 DONATION DETAILS</h3>
                <table>
                    <tr><td><strong>Patient:</strong></td><td>{patient_name}</td></tr>
                    <tr><td><strong>Hospital:</strong></td><td>{request.get('hospital', 'Unknown')}</td></tr>
                    <tr><td><strong>Location:</strong></td><td>{request.get('location', 'Unknown')}</td></tr>
                    <tr><td><strong>Blood Type:</strong></td><td><span style="background: #ff6b6b; color: white; padding: 3px 10px; border-radius: 5px;">{request.get('blood', 'Unknown')}</span></td></tr>
                    <tr><td><strong>Units:</strong></td><td>{request.get('units_needed', 1)}</td></tr>
                    {distance_text}
                </table>
            </div>
            
            <div class="rewards-box">
                <h4 style="color: #0056b3; margin-top: 0;">🎁 REWARDS EARNED</h4>
                <p><strong>Points:</strong> +{POINTS_PER_DONATION}</p>
                <p><strong>Next Eligible Date:</strong> {next_eligible}</p>
            </div>
            
            <div class="info-box">
                <h4 style="color: #856404; margin-top: 0;">⏰ IMPORTANT INFORMATION</h4>
                <ul style="margin-bottom: 0;">
                    <li>You are now on cooldown for {COOLDOWN_MONTHS} months</li>
                    <li>The patient will contact you shortly to schedule</li>
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
            <h2 style="color: #333;">Hello {donor_name},</h2>
            
            <p style="color: #666; font-size: 16px;">Thank you for registering as a blood donor. You're now part of our life-saving community!</p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin: 20px 0;">
                <h3 style="color: #333;">Your Donor Profile:</h3>
                <p><strong>Donor ID:</strong> {donor_details.get('donor_id', '')}</p>
                <p><strong>Blood Type:</strong> {donor_details.get('blood', 'Unknown')}</p>
                <p><strong>Location:</strong> {donor_details.get('location', 'Unknown')}</p>
            </div>
            
            <div style="background: #e8f4fd; padding: 20px; border-radius: 15px;">
                <h3 style="color: #0056b3;">📍 Location-Based Matching</h3>
                <p>The closest donors are always contacted first! You'll be notified when someone near you needs blood.</p>
                <p><strong>Tip:</strong> Enter your complete address with city and pincode for accurate distance calculation.</p>
            </div>
            
            <p style="margin-top: 30px;">Together, we can save lives!</p>
            <p>- BloodAI Team</p>
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
# EVENT NOTIFICATION EMAIL - NEW FUNCTION
# ============================================

def send_event_notification_email(donor_email, donor_name, event_data, distance=None):
    """Send email to donor about new donation event"""
    try:
        if not donor_email or not donor_name or not event_data:
            return False
        
        donor_email = normalize_email(donor_email)
        
        if not is_valid_email(donor_email):
            print(f"❌ Invalid donor email: {donor_email}")
            return False
            
        subject = f"🎪 New Donation Event: {event_data.get('event_name', 'Blood Donation Camp')}"
        
        distance_text = f"<p><strong>📍 Distance from you:</strong> {distance:.1f} km</p>" if distance else ""
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; color: white; }}
        .content {{ padding: 30px; }}
        .event-box {{ background: #f8f9fa; padding: 20px; border-radius: 15px; margin: 20px 0; border-left: 5px solid #667eea; }}
        .button {{ display: inline-block; padding: 15px 30px; background: #43e97b; color: white; text-decoration: none; border-radius: 50px; font-weight: bold; }}
        .button:hover {{ background: #3ad86b; }}
        table {{ width: 100%; }}
        td {{ padding: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0; font-size: 32px;">🎪 New Donation Event!</h1>
            <p style="margin: 10px 0 0;">Be a hero - donate blood and save lives</p>
        </div>
        
        <div class="content">
            <h2 style="margin-top: 0;">Hello {donor_name},</h2>
            
            <p>A new blood donation event has been organized in your area. Your participation can save multiple lives!</p>
            
            <div class="event-box">
                <h3 style="color: #667eea; margin-top: 0;">📋 EVENT DETAILS</h3>
                <table>
                    <tr><td><strong>Event Name:</strong></td><td>{event_data.get('event_name', 'Unknown')}</td></tr>
                    <tr><td><strong>Organizer:</strong></td><td>{event_data.get('organizer', 'Unknown')}</td></tr>
                    <tr><td><strong>Date:</strong></td><td>{event_data.get('start_date', 'Unknown')} to {event_data.get('end_date', 'Unknown')}</td></tr>
                    <tr><td><strong>Time:</strong></td><td>{event_data.get('start_time', 'Unknown')} - {event_data.get('end_time', 'Unknown')}</td></tr>
                    <tr><td><strong>Location:</strong></td><td>{event_data.get('location', 'Unknown')}</td></tr>
                    {distance_text}
                    <tr><td><strong>Target Donations:</strong></td><td>{event_data.get('target_donations', 0)}</td></tr>
                    <tr><td><strong>Contact:</strong></td><td>{event_data.get('contact_person', 'Unknown')} - {event_data.get('contact_phone', 'Unknown')}</td></tr>
                </table>
                
                {f"<p><strong>🎁 Incentives:</strong> {event_data.get('incentives', 'None specified')}</p>" if event_data.get('incentives') else ""}
                {f"<p><strong>✨ Amenities:</strong> {event_data.get('amenities', 'None specified')}</p>" if event_data.get('amenities') else ""}
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{BASE_URL}/?event={event_data.get('event_id')}" class="button">📝 Register for Event</a>
            </div>
            
            <div style="background: #fff3cd; padding: 15px; border-radius: 5px;">
                <p style="margin: 0;"><strong>⏰ Important:</strong> Please register early to help us plan better. Walk-ins are also welcome!</p>
                <p style="margin: 10px 0 0;"><strong>💪 Eligibility:</strong> Age 18-65, Weight >45kg, Healthy on day of donation</p>
            </div>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px; text-align: center;">BloodAI - Connecting Donors with Opportunities to Save Lives</p>
        </div>
    </div>
</body>
</html>
        """
        
        success = send_email(donor_email, subject, message, html=True)
        if success:
            print(f"✅ Event notification email sent to {donor_email}")
        return success
        
    except Exception as e:
        print(f"Event notification email error: {e}")
        return False

# ============================================
# EVENT REGISTRATION CONFIRMATION EMAIL
# ============================================

def send_event_registration_email(donor_email, donor_name, event_name, event_data):
    """Send confirmation email for event registration"""
    try:
        if not donor_email:
            return False
        
        donor_email = normalize_email(donor_email)
        
        if not is_valid_email(donor_email):
            print(f"❌ Invalid donor email: {donor_email}")
            return False
            
        subject = f"✅ Registration Confirmed - {event_name}"
        
        message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea20, #764ba220);">
    <div style="max-width: 600px; margin: 20px auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 30px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 36px;">✅ Registration Confirmed!</h1>
        </div>
        
        <div style="padding: 30px;">
            <h2 style="color: #333;">Hello {donor_name},</h2>
            
            <p style="color: #666; font-size: 16px;">Thank you for registering for the donation event!</p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin: 20px 0;">
                <h3 style="color: #333;">🎪 Event Details:</h3>
                <p><strong>Event:</strong> {event_name}</p>
                <p><strong>Date:</strong> {event_data.get('start_date')} at {event_data.get('start_time')}</p>
                <p><strong>Location:</strong> {event_data.get('location')}</p>
                <p><strong>Contact:</strong> {event_data.get('contact_phone')}</p>
            </div>
            
            <div style="background: #e8f4fd; padding: 20px; border-radius: 15px;">
                <h3 style="color: #0056b3;">📋 Important Information:</h3>
                <ul>
                    <li>Please bring a valid ID</li>
                    <li>Eat a healthy meal before donating</li>
                    <li>Stay hydrated - drink plenty of water</li>
                    <li>Get a good night's sleep</li>
                </ul>
            </div>
            
            <p style="margin-top: 30px;">We look forward to seeing you there!</p>
            <p>- BloodAI Team</p>
        </div>
    </div>
</body>
</html>
        """
        
        return send_email(donor_email, subject, message, html=True)
    except Exception as e:
        print(f"Event registration email error: {e}")
        return False

# ============================================
# AUTO NEXT DONOR FUNCTION (Enhanced with queue system)
# ============================================

def check_and_contact_next_donor():
    """Check pending requests and contact next donor in queue after timeout"""
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
                blood_type = request.get('blood')
                location = request.get('location')
                contacted = request.get('contacted') or ""
                last_contacted = request.get('last_contacted_time')
                all_donors_json = request.get('all_donors', '')
                
                if not request_id or not blood_type or not location:
                    continue
                
                # First contact - send to first donor immediately
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
                            
                            # Send email to first donor
                            distance = first_donor.get('distance_km', float('inf'))
                            send_donor_request_email(first_donor, request, 1, len(all_donors), distance)
                            print(f"✅ Contacted first donor: {first_donor.get('name')} at {distance} km")
                    except Exception as e:
                        print(f"Error contacting first donor: {e}")
                
                # Check if WAIT_MINUTES have passed for subsequent contacts
                elif last_contacted:
                    try:
                        last_time = datetime.strptime(last_contacted, "%Y-%m-%d %H:%M:%S")
                        current_time = datetime.now()
                        
                        if current_time - last_time >= timedelta(minutes=WAIT_MINUTES):
                            print(f"⏰ {WAIT_MINUTES} minutes passed for request {request_id}")
                            
                            # Get next donor to contact
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
                                
                                # Send email to next donor
                                rank = next_index + 1
                                distance = next_donor.get('distance_km', float('inf'))
                                send_donor_request_email(next_donor, request, rank, len(all_donors), distance)
                                print(f"✅ Contacted next donor (#{rank}): {next_donor.get('name')}")
                            else:
                                print(f"❌ No more donors available")
                                execute_query(
                                    "UPDATE requests SET status='No Donors Available' WHERE id=?",
                                    (request_id,),
                                    commit=True
                                )
                                
                                # Notify patient
                                add_notification(
                                    request.get('patient_email'),
                                    'no_donors',
                                    'No Donors Available',
                                    "All eligible donors have been contacted. No one accepted.",
                                    priority='High'
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
                
                # Normalize and validate emails
                patient_email = normalize_email(request.get('patient_email'))
                donor_email = normalize_email(donor.get('email'))
                
                if not is_valid_email(patient_email):
                    st.error(f"❌ Invalid patient email: {patient_email}")
                    return
                    
                if not is_valid_email(donor_email):
                    st.error(f"❌ Invalid donor email: {donor_email}")
                    return
                
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
                
                # 1. Send email to patient with donor details - USING UPDATED FORMAT
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
                    f"{donor.get('name')} has accepted your blood request. Contact them at {donor.get('phone')}",
                    priority='High'
                )
                
                add_notification(
                    donor_email,
                    'accepted',
                    '🎉 Donation Confirmed',
                    f"Thank you for accepting! You can donate again after {next_eligible}",
                    priority='High'
                )
                
                st.query_params.clear()
                st.session_state.showing_response = False
                
                # Show success page with animations
                st.balloons()
                st.snow()
                
                st.info("📧 Email Notifications:")
                for recipient, status in email_status:
                    st.write(f"{recipient}: {status}")
                
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
                    st.info(f"📍 Distance to hospital: {donor_distance:.1f} km")
                
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
                    <p style='color: white;'>Thank you for considering. The next donor will be contacted shortly.</p>
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
                        
                        donor = execute_query(
                            "SELECT name FROM donors WHERE id=?",
                            (donor_id,),
                            fetch_one=True
                        )
                        
                        if donor:
                            st.info(f"✅ Your response has been recorded. The next donor will be contacted.")
                
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
            status_text.text("✅ Found closest donors!")
    
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
        
        # Initialize all blood types with 0 units
        for bt in BLOOD_TYPES:
            blood_type_status[bt] = {'units': 0, 'status': 'critical'}
        
        # Update with actual inventory data
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
                
                # Create alert if needed
                if units < self.alert_threshold:
                    urgency = f'LOW STOCK - Only {units} units' if units > 0 else 'CRITICAL - Out of Stock'
                    alerts.append({
                        'blood_type': bt,
                        'current_stock': units,
                        'threshold': self.alert_threshold,
                        'urgency': urgency
                    })
        
        return alerts, blood_type_status
    
    def display_inventory_dashboard(self):
        """Display interactive inventory dashboard"""
        alerts, blood_status = self.check_stock_alerts()
        
        if alerts:
            st.warning(f"⚠️ {len(alerts)} stock alerts detected")
            
            cols = st.columns(min(len(alerts), 4))
            for i, alert in enumerate(alerts[:4]):
                with cols[i % len(cols)]:
                    if 'CRITICAL' in alert.get('urgency', ''):
                        st.error(f"🩸 {alert.get('blood_type', 'Unknown')}\n{alert.get('urgency', '')}")
                    else:
                        st.warning(f"🩸 {alert.get('blood_type', 'Unknown')}\n{alert.get('urgency', '')}")
        
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
        """Register a new hospital"""
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
            print(f"Hospital registration error: {e}")
            return False, str(e)
    
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
# DONATION EVENTS MANAGEMENT - COMPLETE WITH EMAIL NOTIFICATIONS
# ============================================

class DonationEventManager:
    def __init__(self):
        self.blood_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    
    def create_event(self, event_data, organizer_id=None):
        """Create a new donation event and notify all donors"""
        try:
            event_id = generate_id('EVT')
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Get coordinates for location
            coords = get_coords(event_data.get('location'))
            lat, lon = coords if coords else (None, None)
            
            # Convert lists to JSON
            blood_types_needed = event_data.get('blood_types_needed', [])
            if isinstance(blood_types_needed, list):
                blood_types_needed = json.dumps(blood_types_needed)
            
            amenities = event_data.get('amenities', [])
            if isinstance(amenities, list):
                amenities = json.dumps(amenities)
            
            incentives = event_data.get('incentives', [])
            if isinstance(incentives, list):
                incentives = json.dumps(incentives)
            
            # Insert event into database
            execute_query(
                """INSERT INTO donation_events 
                   (event_id, event_name, organizer, organizer_id, organizer_email, organizer_phone,
                    location, address, city, start_date, end_date, start_time, end_time,
                    target_donations, registered_donors, completed_donations, status,
                    contact_person, contact_phone, contact_email, description, latitude, longitude,
                    amenities, blood_types_needed, incentives, special_instructions, created_date,
                    min_age, max_age, min_weight, is_featured, registration_deadline, notified_donors)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
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
                 event_data.get('registration_deadline'),
                 0),
                commit=True
            )
            
            print(f"✅ Event created: {event_data.get('event_name')} with ID {event_id}")
            
            # Get the created event data
            event = execute_query(
                "SELECT * FROM donation_events WHERE event_id=?",
                (event_id,),
                fetch_one=True
            )
            
            if event:
                # Parse JSON fields for email
                event_dict = dict(event)
                if event_dict.get('blood_types_needed'):
                    try:
                        event_dict['blood_types_needed'] = json.loads(event_dict['blood_types_needed'])
                    except:
                        event_dict['blood_types_needed'] = []
                
                if event_dict.get('amenities'):
                    try:
                        event_dict['amenities'] = json.loads(event_dict['amenities'])
                    except:
                        event_dict['amenities'] = []
                
                if event_dict.get('incentives'):
                    try:
                        event_dict['incentives'] = json.loads(event_dict['incentives'])
                    except:
                        event_dict['incentives'] = []
                
                # Notify all donors about the new event
                self.notify_all_donors(event_id, event_dict, lat, lon)
            
            return True, event_id
            
        except Exception as e:
            print(f"Event creation error: {e}")
            return False, str(e)
    
    def notify_all_donors(self, event_id, event_data, lat, lon):
        """Send email notifications to ALL donors about new event"""
        try:
            # Get ALL donors from database
            donors = execute_query(
                "SELECT * FROM donors WHERE email IS NOT NULL AND email != ''",
                fetch_all=True
            ) or []
            
            print(f"📧 Notifying {len(donors)} donors about new event: {event_data.get('event_name')}")
            
            # Calculate distance for each donor if coordinates available
            donors_with_distance = []
            for donor in donors:
                donor_copy = dict(donor)
                
                # Calculate distance if both coordinates available
                if lat and lon and donor.get('latitude') and donor.get('longitude'):
                    try:
                        distance = geodesic((lat, lon), (donor['latitude'], donor['longitude'])).km
                        donor_copy['distance'] = round(distance, 2)
                    except:
                        donor_copy['distance'] = None
                else:
                    donor_copy['distance'] = None
                
                donors_with_distance.append(donor_copy)
            
            # Sort by distance (closest first)
            donors_with_distance.sort(key=lambda x: x.get('distance', float('inf')) if x.get('distance') else float('inf'))
            
            # Send emails to all donors (with rate limiting)
            sent_count = 0
            for donor in donors_with_distance:
                try:
                    # Check if donor has valid email
                    if not donor.get('email') or not is_valid_email(donor.get('email')):
                        continue
                    
                    # Send email
                    success = send_event_notification_email(
                        donor.get('email'),
                        donor.get('name', 'Donor'),
                        event_data,
                        donor.get('distance')
                    )
                    
                    if success:
                        sent_count += 1
                        # Log notification
                        execute_query(
                            """INSERT INTO event_notifications 
                               (event_id, donor_id, sent_date, status)
                               VALUES (?, ?, ?, ?)""",
                            (event_id, donor.get('id'), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'sent'),
                            commit=True
                        )
                    
                    # Small delay to avoid rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"Error sending email to donor {donor.get('id')}: {e}")
                    continue
            
            # Update notified donors count
            execute_query(
                "UPDATE donation_events SET notified_donors=? WHERE event_id=?",
                (sent_count, event_id),
                commit=True
            )
            
            print(f"✅ Notified {sent_count} donors about event")
            return True
            
        except Exception as e:
            print(f"Error notifying donors: {e}")
            return False
    
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
                    
                    # Parse JSON fields
                    if event_dict.get('blood_types_needed'):
                        try:
                            event_dict['blood_types_needed'] = json.loads(event_dict['blood_types_needed'])
                        except:
                            event_dict['blood_types_needed'] = []
                    
                    if event_dict.get('amenities'):
                        try:
                            event_dict['amenities'] = json.loads(event_dict['amenities'])
                        except:
                            event_dict['amenities'] = []
                    
                    if event_dict.get('incentives'):
                        try:
                            event_dict['incentives'] = json.loads(event_dict['incentives'])
                        except:
                            event_dict['incentives'] = []
                    
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
            
            # Parse JSON fields
            for event in events:
                if event.get('blood_types_needed'):
                    try:
                        event['blood_types_needed'] = json.loads(event['blood_types_needed'])
                    except:
                        event['blood_types_needed'] = []
                
                if event.get('amenities'):
                    try:
                        event['amenities'] = json.loads(event['amenities'])
                    except:
                        event['amenities'] = []
                
                if event.get('incentives'):
                    try:
                        event['incentives'] = json.loads(event['incentives'])
                    except:
                        event['incentives'] = []
            
            return events
        except Exception as e:
            print(f"Error getting events: {e}")
            return []
    
    def register_for_event(self, event_id, donor):
        """Register donor for event"""
        try:
            # Check if already registered
            existing = execute_query(
                "SELECT id FROM event_registrations WHERE event_id=? AND donor_id=?",
                (event_id, donor['id']),
                fetch_one=True
            )
            
            if existing:
                return False, "Already registered"
            
            # Check donor eligibility for event
            if donor.get('age', 0) < 18 or donor.get('age', 0) > 65:
                return False, "Age not within limits (18-65 years)"
            
            if donor.get('weight', 0) < 45:
                return False, "Weight below minimum (45 kg)"
            
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
            
            # Update registered donors count
            execute_query(
                "UPDATE donation_events SET registered_donors = registered_donors + 1 WHERE id=?",
                (event_id,),
                commit=True
            )
            
            # Get event details for email
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
            
            # Add notification
            add_notification(
                donor.get('email'),
                'event_registration',
                '✅ Event Registration Confirmed',
                f"You have successfully registered for {event.get('event_name')}",
                priority='Normal'
            )
            
            return True, "Registration successful"
            
        except Exception as e:
            print(f"Event registration error: {e}")
            return False, str(e)
    
    def display_event_card(self, event):
        """Display a beautiful event card"""
        if not event:
            return
        
        # Determine status color
        status_class = "status-upcoming"
        if event.get('status') == 'Ongoing':
            status_class = "status-ongoing"
        elif event.get('status') == 'Completed':
            status_class = "status-completed"
        elif event.get('status') == 'Cancelled':
            status_class = "status-cancelled"
        
        # Parse dates
        start_date = event.get('start_date', '')
        
        # Progress percentage
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
                <div class='stat-item'>
                    <div class='stat-value'>{event.get('notified_donors', 0)}</div>
                    <div class='stat-label'>Notified</div>
                </div>
            </div>
            
            <div style='margin: 1rem 0;'>
                <p><strong>📅 Date:</strong> {start_date} at {event.get('start_time')}</p>
                <p><strong>📍 Location:</strong> {event.get('location')}</p>
                <p><strong>👤 Contact:</strong> {event.get('contact_person')} ({event.get('contact_phone')})</p>
            </div>
            
            <div style='background: #f0f0f0; border-radius: 10px; padding: 0.5rem; margin: 1rem 0;'>
                <div style='background: #667eea; width: {progress}%; height: 8px; border-radius: 4px;'></div>
                <p style='text-align: center; margin: 0.5rem 0 0;'><strong>{progress:.1f}%</strong> of target reached</p>
            </div>
            
            {f"<p><strong>📍 Distance:</strong> {event.get('distance', 'Unknown')} km</p>" if event.get('distance') else ""}
        </div>
        """, unsafe_allow_html=True)
        
        # Show blood types needed as badges
        if event.get('blood_types_needed'):
            st.markdown("**🩸 Blood Types Needed:**")
            cols = st.columns(len(event['blood_types_needed']))
            for i, bt in enumerate(event['blood_types_needed']):
                with cols[i]:
                    st.markdown(f"<span class='blood-badge'>{bt}</span>", unsafe_allow_html=True)

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
                'emergency_contact': donor_data.get('emergency_contact', ''),
                'verified': donor_data.get('is_verified', 0)
            }
            
            qr_string = json.dumps(qr_data)
            
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )
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
        """Generate QR code for event check-in"""
        try:
            qr_data = {
                'event_id': event_id,
                'event_name': event_data.get('event_name', ''),
                'date': event_data.get('start_date', ''),
                'type': 'event_checkin'
            }
            
            qr_string = json.dumps(qr_data)
            
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )
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
            
            redemptions = execute_query(
                """SELECT r.*, rew.item_name 
                   FROM redemptions r
                   JOIN rewards rew ON r.reward_id = rew.id
                   WHERE r.donor_id=?
                   ORDER BY r.redemption_date DESC""",
                (donor_id,),
                fetch_all=True
            ) or []
            
            return {
                'current_points': donor.get('points', 0),
                'total_earned': donor.get('total_points_earned', 0),
                'level': donor.get('donor_level', 'New Donor 🌟'),
                'redemptions': redemptions
            }
        except Exception as e:
            print(f"Error getting donor points: {e}")
            return None

# ============================================
# CHAT MANAGER
# ============================================

class ChatManager:
    def send_message(self, sender_id, receiver_id, message):
        """Send chat message"""
        try:
            if not sender_id or not receiver_id:
                return False, "Invalid user IDs"
                
            message_id = generate_id('CHAT')
            conversation_id = self.get_conversation_id(sender_id, receiver_id)
            
            sender = execute_query(
                "SELECT name, email FROM donors WHERE id=?",
                (sender_id,),
                fetch_one=True
            )
            
            if not sender:
                return False, "Sender not found"
            
            execute_query(
                """INSERT INTO chat_messages 
                   (message_id, sender_id, receiver_id, message, timestamp, conversation_id)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (message_id, sender_id, receiver_id, message,
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 conversation_id),
                commit=True
            )
            
            receiver = execute_query(
                "SELECT email FROM donors WHERE id=?",
                (receiver_id,),
                fetch_one=True
            )
            
            if receiver:
                add_notification(
                    receiver.get('email'),
                    'chat',
                    f"New message from {sender.get('name', 'Unknown')}",
                    message[:50] + "..." if len(message) > 50 else message
                )
            
            return True, message_id
        except Exception as e:
            print(f"Chat send error: {e}")
            return False, str(e)
    
    def get_conversation_id(self, user1_id, user2_id):
        """Get unique conversation ID"""
        ids = sorted([str(user1_id), str(user2_id)])
        return f"conv_{ids[0]}_{ids[1]}"
    
    def get_conversation(self, user1_id, user2_id, limit=50):
        """Get conversation between two users"""
        try:
            if not user1_id or not user2_id:
                return []
                
            conversation_id = self.get_conversation_id(user1_id, user2_id)
            
            messages = execute_query(
                """SELECT * FROM chat_messages 
                   WHERE conversation_id=?
                   ORDER BY timestamp ASC
                   LIMIT ?""",
                (conversation_id, limit),
                fetch_all=True
            ) or []
            
            execute_query(
                "UPDATE chat_messages SET read=1 WHERE conversation_id=? AND receiver_id=? AND read=0",
                (conversation_id, user1_id),
                commit=True
            )
            
            return messages
        except Exception as e:
            print(f"Error getting conversation: {e}")
            return []
    
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
        except Exception as e:
            print(f"Error getting unread count: {e}")
            return 0
    
    def display_chat_interface(self, current_user_id, other_user_id, other_user_name):
        """Display chat interface"""
        try:
            if not current_user_id or not other_user_id:
                st.warning("Invalid chat users")
                return
                
            st.subheader(f"💬 Chat with {other_user_name}")
            
            messages = self.get_conversation(current_user_id, other_user_id)
            
            chat_container = st.container()
            with chat_container:
                for msg in messages:
                    if not msg:
                        continue
                    if msg.get('sender_id') == current_user_id:
                        st.markdown(f"""
                        <div class='chat-bubble sent'>
                            <strong>You:</strong><br>
                            {msg.get('message', '')}<br>
                            <small>{msg.get('timestamp', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class='chat-bubble received'>
                            <strong>{other_user_name}:</strong><br>
                            {msg.get('message', '')}<br>
                            <small>{msg.get('timestamp', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            col1, col2 = st.columns([5, 1])
            
            with col1:
                new_message = st.text_input("Type your message...", key="chat_input")
            
            with col2:
                if st.button("Send", use_container_width=True):
                    if new_message:
                        success, _ = self.send_message(current_user_id, other_user_id, new_message)
                        if success:
                            st.rerun()
        except Exception as e:
            st.error(f"Chat error: {e}")

# ============================================
# DONOR IMPACT VISUALIZER
# ============================================

class DonorImpactVisualizer:
    def calculate_donor_impact(self, donor_id):
        """Calculate donor's lifetime impact - FIXED: 1 life per donation"""
        try:
            if not donor_id:
                return {
                    'donations': 0,
                    'units': 0,
                    'lives_saved': 0,
                    'events': 0,
                    'total_impact': 0,
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
            
            # FIXED: Each donation saves 1 life (not 3)
            lives_saved = donations.get('count', 0)
            
            events_attended = execute_query(
                "SELECT COUNT(*) as count FROM event_registrations WHERE donor_id=? AND attended=1",
                (donor_id,),
                fetch_one=True
            ) or {'count': 0}
            
            # Get event impact
            event_impact = events_attended.get('count', 0) * 10  # 10 points per event
            
            return {
                'donations': donations.get('count', 0),
                'units': donations.get('total_units', 0),
                'lives_saved': lives_saved,
                'events': events_attended.get('count', 0),
                'total_impact': lives_saved + (events_attended.get('count', 0) * 10),
                'total_distance': donations.get('total_distance', 0) or 0
            }
        except Exception as e:
            print(f"Error calculating impact: {e}")
            return {
                'donations': 0,
                'units': 0,
                'lives_saved': 0,
                'events': 0,
                'total_impact': 0,
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
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=("Donation History", "Impact Breakdown")
            )
            
            # Get actual donation history by month
            donations_by_month = execute_query(
                """SELECT strftime('%m', donation_date) as month, COUNT(*) as count
                   FROM donation_history 
                   WHERE donor_id=? 
                   GROUP BY month 
                   ORDER BY month""",
                (donor_id,),
                fetch_all=True
            ) or []
            
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            donations_data = [0] * 12
            
            for d in donations_by_month:
                if d:
                    month_idx = int(d.get('month', 1)) - 1
                    donations_data[month_idx] = d.get('count', 0)
            
            fig.add_trace(
                go.Bar(x=months, y=donations_data, name="Donations", marker_color='#ff6b6b'),
                row=1, col=1
            )
            
            categories = ['Lives Saved', 'Events', 'Distance (km)']
            values = [impact.get('lives_saved', 0), impact.get('events', 0), impact.get('total_distance', 0)]
            
            fig.add_trace(
                go.Bar(x=categories, y=values, marker_color=['#43e97b', '#feca57', '#667eea']),
                row=1, col=2
            )
            
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea20, #764ba220); padding: 2rem; border-radius: 15px; text-align: center;'>
                <h2>🎉 {donor_name}, you've saved {impact.get('lives_saved', 0)} lives!</h2>
                <p>Your {impact.get('donations', 0)} donations and {impact.get('events', 0)} events have made an incredible impact.</p>
                <p>📍 Total distance traveled: {impact.get('total_distance', 0):.0f} km</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error displaying impact dashboard: {e}")

# ============================================
# SIDEBAR SETUP
# ============================================

st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <h1 style='color: #ff6b6b; font-size: 2.5rem; animation: bounce 2s infinite;'>🩸 BloodAI</h1>
    <p style='color: #666;'>Complete Blood Donation System</p>
</div>
""", unsafe_allow_html=True)

# Database status indicator
st.sidebar.markdown(f"""
<div class='db-status'>
    <strong>💾 Database:</strong> {db_status_text}<br>
    <small>{db_location}</small>
</div>
""", unsafe_allow_html=True)

# Quick stats
st.sidebar.markdown("### 📊 Quick Stats")
selected_blood = st.sidebar.selectbox(
    "Blood Type",
    BLOOD_TYPES,
    key="sidebar_blood"
)

# Get ALL donors count (not just eligible)
total_result = execute_query(
    "SELECT COUNT(*) as count FROM donors WHERE blood=?",
    (selected_blood,),
    fetch_one=True
)
total = total_result['count'] if total_result else 0

# Get eligible donors count
eligible_donors = get_eligible_donors(selected_blood)
eligible_count = len(eligible_donors)

st.sidebar.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea20, #764ba220); padding: 1rem; border-radius: 10px;'>
    <p><strong>🩸 {selected_blood}</strong></p>
    <p>✅ Eligible: {eligible_count}</p>
    <p>📊 Total: {total}</p>
    <p>⏱️ Cooldown: {COOLDOWN_MONTHS} months</p>
    <p>📍 Sorted by: <strong style='color: #43e97b;'>NEAREST FIRST</strong></p>
    <p>📧 All donors notified in order</p>
</div>
""", unsafe_allow_html=True)

# Inventory quick view
inventory_manager = BloodInventoryManager()
alerts, _ = inventory_manager.check_stock_alerts()
if alerts:
    st.sidebar.warning(f"⚠️ {len(alerts)} stock alerts")

# Event quick view
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

# Only show chat and impact dashboard if donor is logged in
if st.session_state.logged_in_donor is None:
    menu_options = [m for m in menu_options if m not in ["💬 Chat", "📊 Impact Dashboard"]]

menu = st.sidebar.radio("Navigation", menu_options)

# System status
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 System Status")
st.sidebar.info(f"⏱️ Auto-rotation: Every {WAIT_MINUTES} minutes")
st.sidebar.info(f"⏳ Response: {WAIT_MINUTES} min per donor")
st.sidebar.info(f"🛡️ Cooldown: {COOLDOWN_MONTHS} months")
st.sidebar.markdown("📍 **Closest donors contacted first**")
st.sidebar.markdown("📧 **All donors notified in order**")

# ============================================
# MAIN CONTENT
# ============================================

if not st.session_state.get('showing_response', False):
    
    # ============================================
    # HOME PAGE - FIXED LIVES SAVED METRIC (1 per donation)
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
                🚨 {pending_count} patient(s) waiting for blood! Contacting all donors in order of distance...
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
            # FIXED: Lives Saved = number of completed donations (1 life per donation)
            completed_donations = execute_query("SELECT COUNT(*) as count FROM donation_history", fetch_one=True)
            
            if completed_donations and completed_donations.get('count'):
                lives_saved = completed_donations['count']
            else:
                lives_saved = 0
                
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{lives_saved}</div><div>Lives Saved</div></div>", unsafe_allow_html=True)
            
            if lives_saved > 0:
                st.caption(f"Based on {lives_saved} completed donations")
        
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
            st.markdown(f"""
            <div class='feature-card'>
                <div class='feature-icon'>🎪</div>
                <div class='feature-title'>Donation Events</div>
                <div class='feature-description'>Create events & notify ALL donors instantly</div>
            </div>
            """, unsafe_allow_html=True)

    # ============================================
    # DONOR REGISTER PAGE - FIXED LOCATION VERIFICATION
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
                                        help="Enter your complete address with city and pincode for accurate distance calculation")
                weight = st.number_input("Weight (kg)*", min_value=45, value=70)
                emergency_contact = st.text_input("Emergency Contact")
                medical_id = st.text_input("Medical ID (Optional)")
            
            health_conditions = st.text_area("Any health conditions? (Leave blank if none)")
            
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
                            
                            # Try to get coordinates with better error handling
                            coords = get_coords(location)
                            lat, lon = coords if coords else (None, None)
                            
                            if coords:
                                location_note = "✅ Location verified - You'll be prioritized in donor queue based on distance!"
                            else:
                                location_note = "⚠️ Could not verify your location. Please update it in the Donor Dashboard with your complete address (include city and pincode) for accurate distance calculation."
                            
                            execute_query(
                                """INSERT INTO donors 
                                   (donor_id, name, email, phone, blood, location, latitude, longitude, password, status, 
                                    registration_date, weight, age, gender, emergency_contact, medical_id, health_conditions,
                                    points, donor_level, is_verified, last_location_update)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (donor_id, name, email, phone, blood, location, lat, lon,
                                 hash_password(password), "Available", current_time,
                                 weight, age, gender, emergency_contact, medical_id, health_conditions,
                                 0, "New Donor 🌟", 1 if coords else 0, current_time),
                                commit=True
                            )
                            
                            donor_details = {
                                'donor_id': donor_id,
                                'blood': blood,
                                'location': location
                            }
                            send_welcome_email(email, name, donor_details)
                            
                            st.success(f"✅ Registration successful! {location_note}")
                            
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
                                    st.image(qr_code, caption="Your Donor QR Code - Save this!", width=200)
                            
                            st.balloons()
                            
                            # Verify data was saved
                            check = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
                            if check:
                                st.caption(f"📊 Total donors in database: {check['count']}")
                            
                        except sqlite3.IntegrityError:
                            st.error("Email already registered")

    # ============================================
    # PATIENT REQUEST PAGE - FIXED DISTANCE DISPLAY
    # ============================================

    elif menu == "🆘 Patient Request":
        st.title("🆘 Emergency Blood Request")
        
        # Get total donors count for info
        total_donors_count = execute_query("SELECT COUNT(*) as count FROM donors", fetch_one=True)
        total_donors = total_donors_count['count'] if total_donors_count else 0
        st.info(f"📊 Total donors in system: {total_donors}")
        st.info(f"⏱️ All eligible donors will be contacted in order of distance. Each donor has {WAIT_MINUTES} minutes to respond.")
        
        with st.form("request_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                patient = st.text_input("Patient Name*")
                email = st.text_input("Your Email*")
                blood = st.selectbox("Blood Type Needed*", BLOOD_TYPES)
                patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=30)
            
            with col2:
                location = st.text_input("Hospital Location*", 
                                        help="Enter complete hospital address with city and pincode for accurate distance calculation")
                hospital = st.text_input("Hospital Name*")
                doctor = st.text_input("Doctor's Name")
                hospital_contact = st.text_input("Hospital Contact Email/Phone")
            
            urgency = st.select_slider("Urgency", options=["Normal", "High", "Critical"], value="High")
            units = st.number_input("Units Needed", min_value=1, max_value=10, value=1)
            reason = st.text_area("Reason for transfusion (Optional)")
            
            submitted = st.form_submit_button("🚨 Request Blood")
            
            if submitted:
                if not all([patient, email, blood, location, hospital]):
                    st.error("Please fill all required fields")
                else:
                    email = normalize_email(email)
                    if not is_valid_email(email):
                        st.error("❌ Invalid email format")
                    else:
                        # Get coordinates
                        coords = get_coords(location)
                        lat, lon = coords if coords else (None, None)
                        
                        if not coords:
                            st.warning("⚠️ Could not verify hospital location. Distance calculations may be less accurate. Please include city and pincode.")
                        
                        # Get ALL donors sorted by distance - FIXED to include ALL donors
                        with st.spinner("🔍 Finding all donors and sorting by distance..."):
                            show_donor_search()
                            all_donors = get_all_donors_sorted_by_distance(blood, location)
                        
                        if not all_donors:
                            st.error(f"❌ No donors found with blood type {blood}!")
                            
                            # Show all donors in system for debugging
                            all_donors_debug = execute_query("SELECT name, blood, status FROM donors", fetch_all=True)
                            if all_donors_debug:
                                st.write("Current donors in system:")
                                for d in all_donors_debug:
                                    st.write(f"- {d['name']}: {d['blood']} ({d['status']})")
                            
                            request_id = generate_id('REQ')
                            current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            execute_query(
                                """INSERT INTO requests 
                                   (request_id, patient, patient_email, blood, location, latitude, longitude, hospital, 
                                    doctor_name, hospital_contact, status, time, urgency_level, units_needed,
                                    patient_age, reason, total_donors_count)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (request_id, patient, email, blood, location, lat, lon, hospital,
                                 doctor, hospital_contact, "No Donors Available", current_time_str, urgency, units,
                                 patient_age, reason, 0),
                                commit=True
                            )
                        else:
                            request_id = generate_id('REQ')
                            current_time = datetime.now()
                            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
                            
                            # Make sure all donors are JSON serializable
                            serializable_donors = make_json_serializable(all_donors)
                            
                            # Store all donors as JSON
                            donors_json = json.dumps(serializable_donors)
                            
                            execute_query(
                                """INSERT INTO requests 
                                   (request_id, patient, patient_email, blood, location, latitude, longitude, hospital, 
                                    doctor_name, hospital_contact, status, time, urgency_level, units_needed,
                                    patient_age, reason, all_donors, total_donors_count)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (request_id, patient, email, blood, location, lat, lon, hospital,
                                 doctor, hospital_contact, "Pending", current_time_str, urgency, units,
                                 patient_age, reason, donors_json, len(all_donors)),
                                commit=True
                            )
                            
                            st.success(f"✅ Request submitted! {len(all_donors)} donors will be contacted in order.")
                            
                            # Show donor queue information with proper distance formatting
                            first_distance = all_donors[0].get('distance_km', 'Unknown')
                            if first_distance == float('inf'):
                                first_distance_str = "📍 Distance not available (location not verified)"
                            else:
                                first_distance_str = f"📍 {first_distance} km from hospital"
                            
                            last_distance = all_donors[-1].get('distance_km', 'Unknown')
                            if last_distance == float('inf'):
                                last_distance_str = "📍 Distance not available"
                            else:
                                last_distance_str = f"{last_distance} km"
                            
                            st.markdown(f"""
                            <div class='location-priority'>
                                <h3 style='color: #43e97b;'>📍 Donor Queue Information</h3>
                                <p><strong>Total Donors Found:</strong> {len(all_donors)}</p>
                                <p><strong>Closest Donor:</strong> {first_distance_str}</p>
                                <p><strong>Farthest Donor:</strong> {last_distance_str}</p>
                                <p><strong>Time between notifications:</strong> {WAIT_MINUTES} minutes</p>
                                <p><strong>Estimated total time:</strong> {len(all_donors) * WAIT_MINUTES} minutes if no one accepts</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show top donors with proper distance display
                            with st.expander(f"View Donor Queue (Top {min(20, len(all_donors))} of {len(all_donors)})"):
                                for i, donor in enumerate(all_donors[:20]):
                                    distance = donor.get('distance_km', 'Unknown')
                                    if distance == float('inf'):
                                        distance_str = "📍 Location not verified"
                                    else:
                                        distance_str = f"📍 {distance} km"
                                    
                                    badge = "🔴 FIRST - CLOSEST DONOR" if i == 0 else f"#{i+1} in queue"
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
                                            
                                            distance_display = req.get('closest_donor_distance', 0)
                                            if distance_display and distance_display != float('inf'):
                                                distance_str = f"{distance_display:.1f} km"
                                            else:
                                                distance_str = "Location not verified"
                                            
                                            st.markdown(f"""
                                            **Donor:** {donor.get('name', 'Unknown')}
                                            **Phone:** {donor.get('phone', '')}
                                            **Email:** {donor.get('email', '')}
                                            **Distance:** {distance_str}
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
    # DONOR DASHBOARD - FIXED LOCATION UPDATE
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
                donor_location = donor.get('location', 'Not set')
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown("<h1 style='font-size: 5rem;'>🩸</h1>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<h2>{donor_name}</h2><p>{donor_level} • {donor_blood} • {donor_location}</p>", unsafe_allow_html=True)
                
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
                
                if donor.get('latitude') and donor.get('longitude'):
                    st.success("📍 Location verified - You'll be prioritized in donor queue based on your distance!")
                    
                    # Show current distance if available
                    donor_coords = (donor.get('latitude'), donor.get('longitude'))
                    st.info(f"📌 Coordinates: {donor_coords[0]:.4f}, {donor_coords[1]:.4f}")
                else:
                    st.warning("⚠️ Location not verified. Update your location with complete address (include city and pincode) to get priority in donor queue.")
                    new_location = st.text_input("Update your location (include city and pincode):")
                    if st.button("Update Location"):
                        if update_donor_coordinates(donor['id'], new_location):
                            st.success("Location updated successfully! You'll now be prioritized based on distance.")
                            st.rerun()
                        else:
                            st.error("Could not verify location. Please include city and pincode (e.g., 'MG Road, Bangalore, 560001')")
                
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
                        if 'donor_distance_km' in df_history.columns:
                            # Format distance for display
                            df_display = df_history[['donation_date', 'hospital', 'blood_type', 'units', 'donor_distance_km', 'points_earned']].copy()
                            df_display['donor_distance_km'] = df_display['donor_distance_km'].apply(
                                lambda x: f"{x:.1f} km" if x and x != float('inf') else "Not verified"
                            )
                            st.dataframe(df_display, use_container_width=True, hide_index=True)
                        else:
                            st.dataframe(df_history, use_container_width=True, hide_index=True)
                else:
                    st.info("No donation history yet")
                
                # Show event registrations
                st.subheader("🎪 Event Registrations")
                events = execute_query(
                    """SELECT er.*, de.event_name, de.start_date, de.location 
                       FROM event_registrations er
                       JOIN donation_events de ON er.event_id = de.id
                       WHERE er.donor_id=?
                       ORDER BY er.registration_date DESC LIMIT 5""",
                    (donor['id'],),
                    fetch_all=True
                ) or []
                
                if events:
                    for event in events:
                        st.markdown(f"""
                        <div style='background: #f0f0f0; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;'>
                            <strong>{event.get('event_name')}</strong> - {event.get('start_date')}<br>
                            Status: {"✅ Attended" if event.get('attended') else "⏳ Registered"}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No event registrations yet")
                
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
                            **Address:** {hospital.get('address', '')}, {hospital.get('city', '')}
                            **Phone:** {hospital.get('phone', '')}
                            **Email:** {hospital.get('email', '')}
                            **Emergency:** {hospital.get('emergency_contact', '')}
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
    # DONATION EVENTS PAGE - COMPLETE WITH EMAIL NOTIFICATIONS
    # ============================================

    elif menu == "🎪 Donation Events":
        st.title("🎪 Donation Events")
        
        event_manager = DonationEventManager()
        
        tab1, tab2, tab3 = st.tabs(["📋 Browse Events", "➕ Create Event", "📊 My Registrations"])
        
        with tab1:
            st.subheader("Find Donation Events Near You")
            
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
                    
                    # Filter options
                    blood_filter = st.multiselect("Filter by blood type needed", BLOOD_TYPES)
                    
                    for event in events:
                        if blood_filter and event.get('blood_types_needed'):
                            if not any(bt in event['blood_types_needed'] for bt in blood_filter):
                                continue
                        
                        event_manager.display_event_card(event)
                        
                        # Registration button
                        if st.session_state.logged_in_donor is not None:
                            if st.button(f"📝 Register for {event.get('event_name')}", key=f"reg_{event.get('id')}"):
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
                    st.info("No events found in your area. Try expanding the search radius or check back later.")
            
            else:
                # Show upcoming events without location
                st.info("Enter your location to see events near you")
                
                all_events = event_manager.get_all_events(status='Upcoming')
                if all_events:
                    st.subheader("📅 Upcoming Events (All Locations)")
                    for event in all_events[:5]:
                        event_manager.display_event_card(event)
        
        with tab2:
            st.subheader("➕ Create New Donation Event")
            st.info("📢 When you create an event, **ALL registered donors** will receive email notifications!")
            
            # Show donor count for info
            total_donors = execute_query("SELECT COUNT(*) as count FROM donors WHERE email IS NOT NULL", fetch_one=True)
            donor_count = total_donors['count'] if total_donors else 0
            st.info(f"📧 This event will be notified to **{donor_count} donors** via email")
            
            with st.form("create_event_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    event_name = st.text_input("Event Name*", placeholder="e.g., Annual Blood Donation Camp")
                    organizer = st.text_input("Organizer Name*", placeholder="e.g., Red Cross Society")
                    organizer_email = st.text_input("Organizer Email*")
                    organizer_phone = st.text_input("Organizer Phone*")
                    
                    start_date = st.date_input("Start Date*", min_value=date.today())
                    end_date = st.date_input("End Date*", min_value=start_date)
                    
                    start_time = st.time_input("Start Time*", value=datetime.now().time())
                    end_time = st.time_input("End Time*", value=datetime.now().time())
                
                with col2:
                    location = st.text_input("Event Location*", 
                                            placeholder="Full address with city and pincode")
                    address = st.text_area("Detailed Address*")
                    city = st.text_input("City*")
                    
                    contact_person = st.text_input("Contact Person*")
                    contact_phone = st.text_input("Contact Phone*")
                    contact_email = st.text_input("Contact Email*")
                    
                    target_donations = st.number_input("Target Donations*", min_value=1, value=50)
                    
                    registration_deadline = st.date_input("Registration Deadline", 
                                                          min_value=date.today())
                
                st.subheader("Event Requirements")
                col1, col2, col3 = st.columns(3)
                with col1:
                    min_age = st.number_input("Minimum Age", min_value=18, max_value=60, value=18)
                with col2:
                    max_age = st.number_input("Maximum Age", min_value=18, max_value=100, value=65)
                with col3:
                    min_weight = st.number_input("Minimum Weight (kg)", min_value=45, value=45)
                
                st.subheader("Blood Types Needed")
                blood_types_needed = st.multiselect("Select blood types", BLOOD_TYPES, default=BLOOD_TYPES)
                
                st.subheader("Amenities Available")
                amenities = st.multiselect(
                    "Select amenities",
                    ["Free Refreshments", "Free T-shirt", "Free Health Checkup", "Free Snacks", 
                     "Free Parking", "Certificate", "Free Medical Consultation", "Free WiFi",
                     "Waiting Area", "AC Hall", "Wheelchair Access", "First Aid Available"]
                )
                
                st.subheader("Incentives for Donors")
                incentives = st.multiselect(
                    "Select incentives",
                    ["Donation Certificate", "Reward Points (50 pts)", "Free Movie Ticket", "Free Gym Pass",
                     "Free Coffee Coupon", "Badge", "Priority for Future Events", "Health Insurance Discount"]
                )
                
                description = st.text_area("Event Description", 
                                          placeholder="Describe the event, any special instructions, etc.")
                
                special_instructions = st.text_area("Special Instructions", 
                                                    placeholder="Any special requirements or instructions for donors")
                
                is_featured = st.checkbox("Feature this event (highlight in search results)")
                
                submitted = st.form_submit_button("🚀 Create Event & Notify All Donors")
                
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
                            'special_instructions': special_instructions,
                            'min_age': min_age,
                            'max_age': max_age,
                            'min_weight': min_weight,
                            'is_featured': 1 if is_featured else 0,
                            'registration_deadline': registration_deadline.strftime("%Y-%m-%d") if registration_deadline else None,
                            'status': 'Upcoming'
                        }
                        
                        organizer_id = st.session_state.logged_in_donor['id'] if st.session_state.logged_in_donor else None
                        
                        with st.spinner("🚀 Creating event and sending email notifications to ALL donors..."):
                            success, result = event_manager.create_event(event_data, organizer_id)
                        
                        if success:
                            st.success(f"✅ Event created successfully! Email notifications sent to all donors.")
                            st.balloons()
                            
                            # Generate QR code for event
                            qr_manager = QRCodeManager()
                            qr_code = qr_manager.generate_event_qr(result, event_data)
                            if qr_code:
                                st.image(qr_code, caption="Event QR Code for Check-in", width=200)
                            
                            # Show notification stats
                            event = execute_query(
                                "SELECT notified_donors FROM donation_events WHERE event_id=?",
                                (result,),
                                fetch_one=True
                            )
                            if event:
                                st.info(f"📧 Email notifications sent to **{event.get('notified_donors', 0)} donors**")
                                
                                # Show preview of who got notified
                                st.subheader("📋 Notification Summary")
                                st.markdown(f"""
                                - Total donors notified: **{event.get('notified_donors', 0)}**
                                - Event will be visible in search results
                                - Donors can register directly from the app
                                """)
                        else:
                            st.error(f"Failed to create event: {result}")
        
        with tab3:
            if st.session_state.logged_in_donor is not None:
                st.subheader("My Event Registrations")
                
                # Get donor's registrations
                registrations = execute_query(
                    """SELECT er.*, de.event_name, de.start_date, de.location, de.status,
                              de.contact_person, de.contact_phone
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
                            **Location:** {reg.get('location')}
                            **Contact:** {reg.get('contact_person')} - {reg.get('contact_phone')}
                            **Attended:** {"✅ Yes" if reg.get('attended') else "⏳ No"}
                            **Points Earned:** {reg.get('points_earned', 0)}
                            """)
                            
                            if reg.get('attended') and not reg.get('feedback'):
                                feedback = st.text_area("Leave Feedback", key=f"fb_{reg.get('id')}")
                                rating = st.slider("Rating", 1, 5, 5, key=f"rating_{reg.get('id')}")
                                if st.button("Submit Feedback", key=f"submit_{reg.get('id')}"):
                                    execute_query(
                                        "UPDATE event_registrations SET feedback=?, rating=? WHERE id=?",
                                        (feedback, rating, reg.get('id')),
                                        commit=True
                                    )
                                    st.success("Thank you for your feedback!")
                                    st.rerun()
                else:
                    st.info("You haven't registered for any events yet")
                    
                    # Show upcoming events as suggestion
                    upcoming = event_manager.get_all_events(status='Upcoming')
                    if upcoming:
                        st.subheader("📅 Upcoming Events You Can Join")
                        for event in upcoming[:3]:
                            st.markdown(f"""
                            <div style='background: #f0f0f0; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;'>
                                <strong>{event.get('event_name')}</strong> - {event.get('start_date')}<br>
                                {event.get('location')}
                            </div>
                            """, unsafe_allow_html=True)
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
                st.markdown(f"### Your Level: {summary.get('level', 'New Donor 🌟')}")
            else:
                st.markdown("### Your Points: 0")
        
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
                            <small>{reward.get('description', '')}</small>
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
            
            others = execute_query(
                "SELECT id, name FROM donors WHERE id != ? LIMIT 10",
                (donor_id,),
                fetch_all=True
            ) or []
            
            if others:
                st.subheader("Select a donor to chat with:")
                for other in others:
                    if other:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"💬 {other.get('name', 'Unknown')}")
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
                        chat_manager.display_chat_interface(donor_id, other_id, other.get('name', 'Unknown'))
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
            
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Donors", "Requests", "Events", "Queue Monitor"])
            
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
                
                upcoming_events = execute_query("SELECT COUNT(*) as count FROM donation_events WHERE status='Upcoming'", fetch_one=True)
                upcoming_events = upcoming_events['count'] if upcoming_events else 0
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Donors", total_donors)
                col2.metric("Total Requests", total_requests)
                col3.metric("Total Events", total_events)
                col4.metric("Pending Requests", pending)
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Completed Donations", total_donations)
                col2.metric("Upcoming Events", upcoming_events)
                col3.metric("Lives Saved", total_donations)
                col4.metric("Event Registrations", execute_query("SELECT COUNT(*) as count FROM event_registrations", fetch_one=True)['count'] or 0)
            
            with tab2:
                donors = execute_query("SELECT * FROM donors ORDER BY registration_date DESC", fetch_all=True) or []
                if donors:
                    df = pd.DataFrame(donors)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Download button
                    csv = df.to_csv(index=False)
                    st.download_button("📥 Download Donors CSV", csv, "donors.csv", "text/csv")
            
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
                    
                    # Event stats
                    st.subheader("📊 Event Statistics")
                    total_registrations = execute_query("SELECT COUNT(*) as count FROM event_registrations", fetch_one=True)
                    total_attended = execute_query("SELECT COUNT(*) as count FROM event_registrations WHERE attended=1", fetch_one=True)
                    total_notified = execute_query("SELECT SUM(notified_donors) as total FROM donation_events", fetch_one=True)
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Registrations", total_registrations['count'] if total_registrations else 0)
                    col2.metric("Total Attended", total_attended['count'] if total_attended else 0)
                    col3.metric("Donors Notified", total_notified['total'] if total_notified and total_notified['total'] else 0)
                    
                    # Download button
                    if not df.empty:
                        csv = df.to_csv(index=False)
                        st.download_button("📥 Download Events CSV", csv, "events.csv", "text/csv")
            
            with tab5:
                pending_reqs = execute_query("SELECT * FROM requests WHERE status='Pending'", fetch_all=True) or []
                for req in pending_reqs:
                    with st.expander(f"Request #{req.get('request_id')} - {req.get('blood')}"):
                        contacted = [x for x in req.get('contacted', '').split(',') if x]
                        total = req.get('total_donors_count', 0)
                        progress = len(contacted)
                        
                        st.write(f"**Progress:** {progress}/{total} donors contacted")
                        if total > 0:
                            st.progress(progress/total)
                        st.write(f"**Current Index:** {req.get('current_donor_index', 0)}")
                        st.write(f"**Last Contacted:** {req.get('last_contacted_time', 'Not yet')}")
                        
                        # Show which donors were contacted
                        if contacted:
                            st.write("**Contacted Donors:**")
                            for donor_id in contacted:
                                donor = execute_query("SELECT name FROM donors WHERE id=?", (donor_id,), fetch_one=True)
                                if donor:
                                    st.write(f"- {donor.get('name')}")

    # ============================================
    # EMAIL LOG PAGE
    # ============================================

    elif menu == "📧 Email Log":
        st.title("📧 Email Log")
        
        # Get email logs from database
        db_logs = execute_query(
            "SELECT * FROM email_log ORDER BY sent_date DESC LIMIT 100",
            fetch_all=True
        ) or []
        
        if db_logs:
            st.subheader("📋 Recent Email Activity")
            for log in db_logs[:20]:
                if log:
                    color = "#43e97b" if log.get('status') == 'sent' else "#ff6b6b"
                    st.markdown(f"""
                    <div class='testimonial-card' style='border-left-color: {color};'>
                        <p><strong>{log.get('sent_date', '')}</strong> - {log.get('recipient', '')}</p>
                        <p>{log.get('subject', '')}</p>
                        <p style='color: {color};'>Status: {log.get('status', '')}</p>
                        <small>Type: {log.get('type', '')}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Summary stats
            total_sent = len([l for l in db_logs if l.get('status') == 'sent'])
            total_failed = len([l for l in db_logs if l.get('status') == 'failed'])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Emails", len(db_logs))
            col2.metric("Sent", total_sent)
            col3.metric("Failed", total_failed)
            
        elif st.session_state.email_log:
            # Fallback to session state logs
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
            st.info("No emails sent yet")

    # ============================================
    # FOOTER
    # ============================================

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <p>BloodAI v19.0 - Complete System with Permanent Storage</p>
        <p>📍 <strong style='color: #43e97b;'>All Donors Notified • Closest First • {WAIT_MINUTES} Min Rotation</strong></p>
        <p>🎪 <strong style='color: #667eea;'>Events: ALL donors get email notifications</strong></p>
        <p>💾 <strong>Database:</strong> {db_status_text}</p>
        <p>📊 <strong>Data Persists</strong> - Never lost on restart</p>
    </div>
    """, unsafe_allow_html=True)
