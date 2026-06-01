# MedAssist AI

### AI-Powered Medication Safety, Medical Report Analysis & Nutrition Guidance Platform

MedAssist AI is a complete, production-ready healthcare assistant platform that helps users maintain health profiles, manage diseases, track medications, upload prescriptions/medical reports, extract info using OCR, analyze medication safety/drug interactions, recommend alternatives, and get nutrition advice.

---

## Features

1. **Patient Profile & Condition Management**: Maintain personal details (age, weight, blood group) and track chronic diseases/conditions.
2. **Medication Tracker**: Track daily medications, dosage, frequency, and notes.
3. **OCR Prescription Analyzer**: Upload PDFs/images of medical reports/prescriptions to extract text via EasyOCR and summarize findings via AI.
4. **Drug Safety & Interaction Analyzer**: Check safety ratings and dangerous interactions between multiple medications.
5. **Side Effect Lookup**: Detailed breakdown of common, moderate, and rare side effects.
6. **Alternative Medicine Recommender**: Discover generic or natural alternatives for high-risk medications.
7. **Personalized Nutrition Advisor**: Tailored diet, foods to eat/avoid, hydration recommendations based on health profile and diseases.
8. **Health Chatbot**: Conversational interface to ask medical/nutrition questions.
9. **PDF Report Generator**: Downloadable comprehensive patient health summary.

---

## Folder Structure

```text
medassist-ai/
├── backend/
│   ├── app.py              # Flask backend entrypoint & APIs
│   ├── db.py               # Database layer (SQLite)
│   ├── ai_engine.py        # Groq LLM integration
│   ├── ocr_engine.py       # EasyOCR processor
│   ├── pdf_generator.py    # ReportLab PDF generator
│   ├── database.db         # SQLite Database (auto-generated)
│   ├── uploads/            # Temporary OCR uploaded files
│   └── reports/            # Generated PDF health reports
├── frontend/
│   ├── index.html          # SPA main page structure
│   ├── style.css           # Modern, custom CSS styling
│   └── script.js           # UI logic, state, and API routing
├── .env                    # Environment credentials
├── requirements.txt        # Python dependency manifest
└── README.md               # Documentation
```

---

## Setup & Installation

### 1. Prerequisites
- Python 3.8+ installed.
- (Optional but recommended) A virtual environment.

### 2. Install Dependencies
Run the following command to install required packages:
```bash
pip install -r requirements.txt
```
*(Note: If EasyOCR is used, it may download OCR model files on the first run).*

### 3. Environment Variables
Rename or configure the `.env` file in the root directory:
```env
GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE
SECRET_KEY=YOUR_FLASK_SECRET_KEY_HERE
```
Ensure you obtain a free API key from [Groq Console](https://console.groq.com/).

---

## Running the Application

### Running Backend (Flask)
Start the Flask development server:
```bash
python backend/app.py
```
By default, the server will start on [http://localhost:5000](http://localhost:5000).

### Running Frontend
You can run the frontend in two ways:
1. Open the [frontend/index.html](file:///c:/Users/Indhu%20Priyan/OneDrive/Desktop/medication/frontend/index.html) file directly in any modern web browser.
2. Serve it using a simple HTTP server or the Flask app route at `/`.

---

## Troubleshooting & FAQ

- **Groq API Error**: Ensure your `.env` contains a valid Groq API key and is configured correctly.
- **EasyOCR issues**: When running OCR for the first time, EasyOCR will automatically download model weights. Ensure you have internet access. If you run into CPU/PyTorch compatibility issues, verify you installed the correct PyTorch package for your hardware.
- **Database lock errors**: If the database gets locked, make sure you don't have multiple python processes writing to `database.db` concurrently.
