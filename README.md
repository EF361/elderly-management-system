
# 🏥 CareLink: Elderly Management System

**A comprehensive, multi-role Streamlit application designed to streamline care coordination, medical tracking, and resident engagement in elderly care facilities.**

## 🚀 Overview

CareLink is an industrial-grade management platform built to bridge the gap between healthcare providers, facility administrators, and residents. The system centralizes critical data—from medication records and shift scheduling to real-time resident demographics—into a single, intuitive interface.

By leveraging a robust PostgreSQL backend and a modern Streamlit frontend, CareLink automates the administrative overhead of elderly care. It ensures that doctors can manage prescriptions, staff can track their shifts, and residents can access their personal schedules and an AI-powered assistant for immediate support.

## ✨ Key Features

* 🔐 **Multi-Role Authentication**: Tailored dashboards and permissions for Admins, Staff (Doctors/Nurses), and Residents.
* 💊 **Medical Record Management**: Dedicated portal for Doctors to create, update, and track resident diagnoses and treatments.
* 📅 **Dynamic Scheduling**: Automated management for medical appointments, social activities, and staff shifts.
* 📊 **Administrative Analytics**: Real-time data visualization of resident demographics and staff distribution using Plotly.
* 🤖 **AI Resident Assistant**: An integrated GPT-powered chatbot that helps residents check their medication and daily schedules.
* 📄 **Automated Reporting**: One-click PDF generation for comprehensive resident and staff activity logs.

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **Database**: PostgreSQL
* **ORM/Querying**: SQLAlchemy & Psycopg2
* **Data Visualization**: Plotly & Pandas
* **AI Integration**: OpenAI API
* **PDF Generation**: ReportLab

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/EF361/elderly-management-system.git
cd elderly-management-system
```
### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate

```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

## 🏃‍♂️ How to Run

1. **Configure Database**: Ensure your PostgreSQL server is running and update the connection string in `app.py` and `management.py` with your credentials.
2. **Set API Keys**: Add your `OPENAI_API_KEY` to your Streamlit `secrets.toml` file.
3. **Launch Application**:

```bash
streamlit run app.py

```

4. **Access the App**: Open `http://localhost:8501` in your browser.

## 📖 Usage Guide

1. **Login**: Select your role (Admin, Staff, or Resident) and enter your credentials on the landing page.
2. **Manage Records**: Admins can use the "Management" tabs to register new residents, staff members, or update facility inventory.
3. **Update Health Data**: Staff with 'Doctor' privileges can navigate to "Medical Record" to log new diagnoses and treatments.
4. **Check Schedules**: Residents can view their daily activities in the "Schedule" tab or ask the "Chatbot" for their next appointment.
5. **Generate Insights**: Admins can visit the "Reports" section to export activity data as professional PDF documents.

## 📂 Project Structure

```text
.
├── admin/
│   ├── admin_management.py      # Admin user CRUD operations
│   ├── dashboard.py             # Facility-wide analytics and metrics
│   ├── medication.py            # Medicine inventory management
│   ├── reports.py               # PDF report generation logic
│   ├── resident_management.py    # Resident and emergency contact CRUD
│   ├── schedule.py              # Global event and appointment manager
│   └── staff_management.py       # Staff registration and role assignment
├── resident/
│   ├── chatbot.py               # AI assistant for resident queries
│   ├── dashboard.py             # Personal profile and emergency info
│   └── schedule.py              # Resident-specific daily agenda
├── staff/
│   ├── dashboard.py             # Staff profile and assigned task metrics
│   ├── medication.py            # Clinical medical record entry
│   └── shift.py                 # Staff work schedule and shift tracking
├── images/                      # UI assets and logos
├── app.py                       # Main entry point and navigation
├── management.py                # Shared database logic and Management class
├── contact_number.py            # Reusable phone number validation component
├── requirements.txt             # Project dependencies
└── styles.css                   # Custom UI styling

```
