# 🩸 BloodAI - Complete Blood Donation Management System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bloodai-smart-donor-system.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Overview

BloodAI is a comprehensive blood donation management system that connects donors with patients in need. The system automatically contacts donors in order of **distance (NEAREST FIRST)** and implements a **3-month cooldown period** for donor safety.

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📍 **Nearest Donor First** | Automatically sorts and contacts donors by distance |
| ⏱️ **3-Month Cooldown** | Ensures donor safety between donations |
| 📧 **Email Notifications** | Accept/reject requests via email with Google Maps links |
| 🔄 **3 Retry Cycles** | Re-contacts all donors if no one responds |
| 👤 **Donor Dashboard** | Track donations, points, and level |
| 🏆 **Rewards Store** | Redeem points for movie tickets, vouchers, etc. |
| 🏥 **Hospital Management** | Register and find nearby hospitals |
| 📦 **Blood Inventory** | Track blood units by type |
| 🎪 **Donation Events** | Create and manage blood donation camps |
| 💬 **Chat System** | Donors can communicate with each other |
| 👑 **Admin Panel** | Full system control and monitoring |
| 📊 **Impact Dashboard** | Visualize lives saved |

## 🚀 Live Demo

**Try it now:** [https://bloodai-smart-donor-system.streamlit.app/](https://bloodai-smart-donor-system.streamlit.app/)

## 📸 Screenshots

*Add screenshots of your app here*

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.9+
- **Database:** PostgreSQL (Supabase)
- **Email Service:** SMTP (Gmail)
- **Maps Integration:** Google Maps API
- **Machine Learning:** Scikit-learn (donor prediction)
- **Charts:** Plotly
- **QR Codes:** qrcode library

## 📋 Prerequisites

- Python 3.9 or higher
- PostgreSQL database (or Supabase account)
- Gmail account with App Password

## 🔧 Installation

### 1. Clone the repository
```bash
git clone https://github.com/vigneshsapavat11/BloodAIS.git
cd BloodAIS
