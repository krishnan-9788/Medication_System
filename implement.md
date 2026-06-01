# MEDASSIST AI - MASTER PROJECT GENERATION PROMPT

Create a complete production-ready AI healthcare web application called:

# MedAssist AI

### AI-Powered Medication Safety, Medical Report Analysis & Nutrition Guidance Platform

---

# IMPORTANT

This is NOT a prototype.

This must be a complete working production-ready application.

Generate all source code files.

Generate all backend code.

Generate all frontend code.

Generate all database code.

Generate all API routes.

Generate all OCR functionality.

Generate all Groq integrations.

Generate all PDF generation functionality.

Generate all history management functionality.

Generate all database tables automatically.

Generate a clean, modern healthcare UI.

Everything must be connected and fully functional.

The project should run immediately after:

1. Installing requirements
2. Adding a Groq API key
3. Running the Flask application

---

# FIRST REQUIREMENT (VERY IMPORTANT)

Before generating any code:

You must first generate a complete software architecture document.

Explain the project completely.

Do NOT generate code immediately.

First explain:

1. Project Overview
2. Project Objectives
3. User Flow
4. System Flow
5. Folder Structure
6. File Responsibilities
7. Database Design
8. API Design
9. Frontend Architecture
10. Backend Architecture
11. OCR Workflow
12. Groq Workflow
13. Medication Analysis Workflow
14. Side Effect Analysis Workflow
15. Alternative Recommendation Workflow
16. Nutrition Workflow
17. PDF Generation Workflow
18. History Workflow
19. Dashboard Workflow
20. Security Strategy
21. Error Handling Strategy

Only after explaining the architecture completely should you generate source code.

---

# PROJECT GOAL

MedAssist AI is an AI-powered healthcare assistant platform that helps users:

* Maintain personal health profiles
* Store diseases and medical conditions
* Track medications
* Upload prescriptions and medical reports
* Extract information from reports using OCR
* Analyze medication safety
* Check medicine interactions
* View side effects
* Discover alternative medicines
* Receive personalized nutrition guidance
* Generate downloadable PDF reports
* Maintain complete analysis history
* Chat with an AI health assistant

The application should use:

OCR + Groq LLM

Do NOT create custom ML training pipelines.

Do NOT create model training code.

Do NOT create model.pkl files.

All intelligence must come from Groq API.

---

# TECHNOLOGY STACK

Frontend:

* HTML
* CSS
* JavaScript

Backend:

* Python
* Flask

Database:

* SQLite

OCR:

* EasyOCR

AI:

* Groq API

PDF:

* ReportLab

Environment Variables:

* python-dotenv

Storage:

* SQLite
* uploads folder
* reports folder

---

# SIMPLIFIED PROJECT STRUCTURE

Create exactly this structure:

medassist-ai/

│
├── backend/
│   │
│   ├── app.py
│   ├── db.py
│   ├── ai_engine.py
│   ├── ocr_engine.py
│   ├── pdf_generator.py
│   │
│   ├── database.db
│   │
│   ├── uploads/
│   │
│   └── reports/
│
├── frontend/
│   │
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .env
├── requirements.txt
└── README.md

---

# FILE RESPONSIBILITY DOCUMENTATION

Before generating code explain every file.

---

## app.py

Project Entry Point

Responsibilities:

* Flask initialization
* Route management
* API endpoints
* Request handling
* Response handling
* Authentication
* Dashboard APIs
* History APIs
* Report APIs

Connection Flow:

Frontend

↓

app.py

↓

ai_engine.py

↓

Groq

---

Frontend

↓

app.py

↓

ocr_engine.py

↓

OCR Results

---

Frontend

↓

app.py

↓

pdf_generator.py

↓

PDF Report

---

Frontend

↓

app.py

↓

db.py

↓

SQLite

---

## db.py

Database Layer

Responsibilities:

* Database creation
* Table creation
* CRUD operations
* History storage
* Profile storage
* Disease storage
* Medication storage
* Report storage

---

Database Tables:

users

profiles

diseases

medications

ocr_reports

analysis_history

pdf_reports

chat_history

---

## ai_engine.py

Groq Integration Layer

Responsibilities:

* Load Groq API key
* Medication analysis
* Drug interaction analysis
* Side effect analysis
* Alternative medicine recommendation
* Nutrition recommendation
* Health chatbot

All Groq prompts must be centralized here.

No Groq logic should exist anywhere else.

---

## ocr_engine.py

OCR Processing Layer

Responsibilities:

* PDF reading
* Image reading
* OCR extraction
* Text cleaning
* Structured result generation

Use EasyOCR.

---

## pdf_generator.py

PDF Generation Layer

Responsibilities:

* Patient summary PDF
* Medication report PDF
* Nutrition report PDF
* Analysis report PDF
* Report download support

Use ReportLab.

---

## frontend/index.html

Single Page Application.

Do NOT create multiple HTML pages.

Everything must exist inside one HTML application.

Sections:

* Login
* Register
* Dashboard
* Profile
* Diseases
* Medications
* OCR Upload
* Medication Analyzer
* Side Effects
* Alternative Medicines
* Nutrition
* Health Chat Assistant
* History
* Reports

JavaScript must switch sections dynamically.

---

## frontend/script.js

Responsibilities:

* API calls
* Form submissions
* Dashboard updates
* OCR uploads
* PDF downloads
* Chatbot requests
* Dynamic UI updates

---

## frontend/style.css

Responsibilities:

* Modern healthcare design
* Sidebar
* Dashboard
* Forms
* Cards
* Tables
* Mobile responsiveness
* Professional color palette

---

# ENVIRONMENT FILE

Create:

.env

Include:

GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE

Use environment variables.

Never hardcode API keys.

Load API key using:

python-dotenv

---

# USER FLOW

Step 1

User registers.

Step 2

User logs in.

Step 3

User creates health profile.

Store:

* Name
* Age
* Gender
* Weight
* Height
* Blood Group

---

# DISEASE MANAGEMENT

Allow:

* Add disease
* Edit disease
* Delete disease
* View disease

Examples:

* Diabetes
* Hypertension
* Asthma
* Thyroid
* Kidney Disease
* Heart Disease

Store in database.

---

# MEDICATION MANAGEMENT

Allow:

* Add medication
* Edit medication
* Delete medication
* View medication

Store:

* Medicine Name
* Dosage
* Frequency
* Notes

Store in database.

---

# MEDICAL REPORT UPLOAD

Allow upload:

* PDF
* JPG
* JPEG
* PNG

Store uploaded files.

Save path in database.

---

# OCR PROCESSING

Use EasyOCR.

Extract:

* Medicine Names
* Diseases
* Prescription Text
* Doctor Notes

Display extracted content.

Store extracted content.

Store original file path.

---

# MEDICATION ANALYZER

User enters:

One or multiple medicines.

Examples:

* Paracetamol
* Dolo650
* Aspirin
* Ibuprofen

Send to Groq.

Groq must analyze:

* Interaction Risk
* Medication Safety
* Warnings
* Recommendations

Return:

* Safe
* Moderate Risk
* High Risk
* Dangerous

Include explanation.

Store result in history.

---

# SIDE EFFECT ANALYZER

User enters medicine.

Groq returns:

* Common Side Effects
* Moderate Side Effects
* Rare Side Effects
* Warnings

Store result in history.

---

# ALTERNATIVE MEDICINE RECOMMENDER

User enters medicine.

Groq returns:

* Alternative Medicines
* Reasons
* Usage Notes

Display professionally.

Store result in history.

---

# NUTRITION ADVISOR

Use:

* User profile
* Diseases
* Medications

Generate:

Foods To Eat

Foods To Avoid

Nutrition Tips

Hydration Advice

Healthy Habits

Display disclaimer:

Educational guidance only.

Store result in history.

---

# HEALTH CHAT ASSISTANT

User questions:

Examples:

Can I take Dolo650?

What are side effects of Ibuprofen?

What foods should diabetics avoid?

Analyze my medicines.

Use Groq.

Store conversations.

Maintain chat history.

---

# PDF REPORT GENERATOR

Generate PDF report containing:

* Profile Information
* Diseases
* Medications
* Medication Analysis
* Side Effects
* Nutrition Recommendations
* Generated Date

Save PDF in reports folder.

Allow download.

Store report metadata in database.

---

# DASHBOARD

Display:

* Profile Summary
* Disease Count
* Medication Count
* Uploaded Reports
* Analysis History
* Generated PDFs
* Recent Activities
* Health Summary

Use cards and analytics sections.

---

# APPLICATION FLOW

User Login

↓

Profile Setup

↓

Disease Setup

↓

Medication Setup

↓

Medical Report Upload

↓

OCR Extraction

↓

Database Storage

↓

Groq Analysis

↓

History Storage

↓

Dashboard Update

↓

PDF Generation

↓

Download Report

---

# GROQ PROMPT ENGINEERING

Create centralized prompt templates inside ai_engine.py

Include:

1. Medication Analysis Prompt
2. Side Effect Prompt
3. Alternative Medicine Prompt
4. Nutrition Prompt
5. Health Chat Prompt

All prompts must be reusable.

---

# DATABASE FLOW

User

↓

Profile

↓

Diseases

↓

Medications

↓

OCR Reports

↓

Analyses

↓

PDF Reports

↓

Chat History

All linked through User ID.

---

# ERROR HANDLING

Implement handling for:

* Missing API key
* Invalid medicine input
* Empty profile
* Empty disease list
* Invalid file upload
* OCR failure
* Groq timeout
* Groq API failure
* Database failure
* PDF generation failure

Application must never crash.

Display user-friendly messages.

---

# SECURITY

Implement:

* Input validation
* File validation
* SQL injection prevention
* Safe file uploads
* API error protection

---

# REQUIREMENTS.TXT

Generate complete requirements.txt

Include:

flask

flask-cors

python-dotenv

groq

easyocr

opencv-python

pillow

reportlab

numpy

pandas

requests

werkzeug

---

# README

Generate complete README.

Include:

* Project Overview
* Features
* Installation
* Setup
* Folder Structure
* Environment Variables
* Running Backend
* Running Frontend
* Troubleshooting
* Future Enhancements

---

# FINAL REQUIREMENT

Generate COMPLETE WORKING SOURCE CODE.

All files must connect correctly.

All routes must work.

All frontend components must work.

Database must work.

OCR must work.

Groq integration must work.

History must work.

PDF generation must work.

Dashboard must work.

Application must be production-style, clean, modular, and fully functional.

After architecture explanation, generate every file completely with comments and proper code organization.
