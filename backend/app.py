"""
app.py - MedAssist AI Flask Application
Main entry point with all API routes.
"""

import os
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, request, jsonify, session, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

import db
import ai_engine
import ocr_engine
import pdf_generator

load_dotenv()

app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.secret_key = os.getenv("SECRET_KEY", "dev_fallback_secret_key_change_in_production")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20 MB

CORS(app, supports_credentials=True, origins=["*"])

BASE_DIR = os.path.dirname(__file__)
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Initialize database on startup
db.init_db()


# ─── HELPER FUNCTIONS ──────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def require_auth(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required", "authenticated": False}), 401
        return f(*args, **kwargs)
    return decorated


def success(data: dict = None, message: str = "Success"):
    response = {"success": True, "message": message}
    if data:
        response.update(data)
    return jsonify(response)


def error(message: str, status: int = 400):
    return jsonify({"success": False, "error": message}), status


# ─── AUTH ROUTES ───────────────────────────────────────────────────────────────

@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return error("Username, email, and password are required.")
    if len(username) < 3:
        return error("Username must be at least 3 characters.")
    if len(password) < 6:
        return error("Password must be at least 6 characters.")
    if "@" not in email:
        return error("Invalid email address.")

    created = db.create_user(username, email, hash_password(password))
    if not created:
        return error("Username or email already exists.")

    return success(message="Account created successfully! Please log in.")


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return error("Username and password are required.")

    user = db.get_user_by_username(username)
    if not user or user["password"] != hash_password(password):
        return error("Invalid username or password.", 401)

    session.permanent = True
    session["user_id"] = user["id"]
    session["username"] = user["username"]

    return success({"username": user["username"], "user_id": user["id"]}, "Login successful!")


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return success(message="Logged out successfully.")


@app.route("/api/auth/status", methods=["GET"])
def auth_status():
    if "user_id" in session:
        return success({"authenticated": True, "username": session.get("username"), "user_id": session.get("user_id")})
    return jsonify({"authenticated": False})


# ─── DASHBOARD ─────────────────────────────────────────────────────────────────

@app.route("/api/dashboard", methods=["GET"])
@require_auth
def dashboard():
    user_id = session["user_id"]
    stats = db.get_dashboard_stats(user_id)
    profile = db.get_profile(user_id)
    recent_analyses = db.get_analysis_history(user_id, limit=5)
    recent_pdfs = db.get_pdf_reports(user_id)[:3]

    return success({
        "stats": stats,
        "profile": profile,
        "recent_analyses": recent_analyses,
        "recent_pdfs": recent_pdfs
    })


# ─── PROFILE ROUTES ────────────────────────────────────────────────────────────

@app.route("/api/profile", methods=["GET"])
@require_auth
def get_profile():
    profile = db.get_profile(session["user_id"])
    return success({"profile": profile})


@app.route("/api/profile", methods=["POST"])
@require_auth
def save_profile():
    data = request.get_json() or {}
    user_id = session["user_id"]

    name = data.get("name", "").strip()
    if not name:
        return error("Name is required.")

    db.upsert_profile(
        user_id=user_id,
        name=name,
        age=data.get("age"),
        gender=data.get("gender", ""),
        weight=data.get("weight"),
        height=data.get("height"),
        blood_group=data.get("blood_group", "")
    )
    return success(message="Profile saved successfully!")


# ─── DISEASE ROUTES ────────────────────────────────────────────────────────────

@app.route("/api/diseases", methods=["GET"])
@require_auth
def get_diseases():
    diseases = db.get_diseases(session["user_id"])
    return success({"diseases": diseases})


@app.route("/api/diseases", methods=["POST"])
@require_auth
def add_disease():
    data = request.get_json() or {}
    disease_name = data.get("disease_name", "").strip()
    if not disease_name:
        return error("Disease name is required.")

    db.add_disease(
        user_id=session["user_id"],
        disease_name=disease_name,
        severity=data.get("severity", ""),
        notes=data.get("notes", ""),
        diagnosed_date=data.get("diagnosed_date", "")
    )
    return success(message="Disease added successfully!")


@app.route("/api/diseases/<int:disease_id>", methods=["PUT"])
@require_auth
def update_disease(disease_id):
    data = request.get_json() or {}
    disease_name = data.get("disease_name", "").strip()
    if not disease_name:
        return error("Disease name is required.")

    db.update_disease(
        disease_id=disease_id,
        user_id=session["user_id"],
        disease_name=disease_name,
        severity=data.get("severity", ""),
        notes=data.get("notes", ""),
        diagnosed_date=data.get("diagnosed_date", "")
    )
    return success(message="Disease updated successfully!")


@app.route("/api/diseases/<int:disease_id>", methods=["DELETE"])
@require_auth
def delete_disease(disease_id):
    db.delete_disease(disease_id, session["user_id"])
    return success(message="Disease deleted.")


# ─── MEDICATION ROUTES ─────────────────────────────────────────────────────────

@app.route("/api/medications", methods=["GET"])
@require_auth
def get_medications():
    medications = db.get_medications(session["user_id"])
    return success({"medications": medications})


@app.route("/api/medications", methods=["POST"])
@require_auth
def add_medication():
    data = request.get_json() or {}
    medicine_name = data.get("medicine_name", "").strip()
    if not medicine_name:
        return error("Medicine name is required.")

    db.add_medication(
        user_id=session["user_id"],
        medicine_name=medicine_name,
        dosage=data.get("dosage", ""),
        frequency=data.get("frequency", ""),
        notes=data.get("notes", "")
    )
    return success(message="Medication added successfully!")


@app.route("/api/medications/<int:med_id>", methods=["PUT"])
@require_auth
def update_medication(med_id):
    data = request.get_json() or {}
    medicine_name = data.get("medicine_name", "").strip()
    if not medicine_name:
        return error("Medicine name is required.")

    db.update_medication(
        med_id=med_id,
        user_id=session["user_id"],
        medicine_name=medicine_name,
        dosage=data.get("dosage", ""),
        frequency=data.get("frequency", ""),
        notes=data.get("notes", "")
    )
    return success(message="Medication updated successfully!")


@app.route("/api/medications/<int:med_id>", methods=["DELETE"])
@require_auth
def delete_medication(med_id):
    db.delete_medication(med_id, session["user_id"])
    return success(message="Medication deleted.")


# ─── TIMETABLE ROUTES ──────────────────────────────────────────────────────────

@app.route("/api/timetable", methods=["GET"])
@require_auth
def get_timetable():
    timetable = db.get_timetable(session["user_id"])
    return success({"timetable": timetable})


@app.route("/api/timetable", methods=["POST"])
@require_auth
def add_timetable_entry():
    data = request.get_json() or {}
    medicine_name = data.get("medicine_name", "").strip()
    time_scheduled = data.get("time_scheduled", "").strip()
    if not medicine_name or not time_scheduled:
        return error("Medicine name and scheduled time are required.")

    db.add_timetable_entry(
        user_id=session["user_id"],
        medicine_name=medicine_name,
        dosage=data.get("dosage", ""),
        time_scheduled=time_scheduled
    )
    return success(message="Timetable entry added successfully!")


@app.route("/api/timetable/<int:entry_id>/status", methods=["PUT"])
@require_auth
def update_timetable_status(entry_id):
    data = request.get_json() or {}
    status = data.get("status", "").strip()
    if not status:
        return error("Status is required.")

    db.update_timetable_status(
        entry_id=entry_id,
        user_id=session["user_id"],
        status=status
    )
    return success(message="Timetable status updated!")


@app.route("/api/timetable/<int:entry_id>", methods=["DELETE"])
@require_auth
def delete_timetable_entry(entry_id):
    db.delete_timetable_entry(entry_id, session["user_id"])
    return success(message="Timetable entry deleted.")


# ─── OCR UPLOAD ────────────────────────────────────────────────────────────────

@app.route("/api/ocr/upload", methods=["POST"])
@require_auth
def ocr_upload():
    if "file" not in request.files:
        return error("No file uploaded.")

    file = request.files["file"]
    if not file.filename:
        return error("Empty filename.")

    # Validate file
    validation = ocr_engine.validate_file(file.filename, 0)
    if not validation["valid"]:
        return error(validation["error"])

    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{session['user_id']}_{timestamp}_{filename}"
    file_path = os.path.join(UPLOADS_DIR, unique_filename)

    file.save(file_path)

    # Run OCR
    ocr_result = ocr_engine.extract_text_from_file(file_path)

    extracted_text = ocr_result.get("text", "")
    ai_analysis = {}

    # If OCR succeeded, run AI analysis on extracted text
    if ocr_result["success"] and extracted_text:
        ai_analysis = ai_engine.analyze_ocr_text(extracted_text)

    # Save to database
    db.save_ocr_report(
        user_id=session["user_id"],
        filename=filename,
        file_path=unique_filename,
        extracted_text=extracted_text
    )

    return success({
        "ocr_result": ocr_result,
        "ai_analysis": ai_analysis,
        "filename": filename
    }, "File processed successfully!")


@app.route("/api/ocr/reports", methods=["GET"])
@require_auth
def get_ocr_reports():
    reports = db.get_ocr_reports(session["user_id"])
    return success({"reports": reports})


# ─── AI ANALYSIS ROUTES ────────────────────────────────────────────────────────

@app.route("/api/analyze/medications", methods=["POST"])
@require_auth
def analyze_medications():
    data = request.get_json() or {}
    medicines_input = data.get("medicines", "")

    if not medicines_input:
        return error("Please enter at least one medicine name.")

    # Parse comma/newline separated medicines
    medicines = [m.strip() for m in medicines_input.replace("\n", ",").split(",") if m.strip()]

    if not medicines:
        return error("No valid medicine names found.")

    user_id = session["user_id"]
    profile = db.get_profile(user_id)
    diseases = db.get_diseases(user_id)
    daily_meds = db.get_medications(user_id)

    result = ai_engine.analyze_medication_safety(
        new_medicines=medicines,
        profile=profile,
        diseases=diseases,
        daily_medications=daily_meds
    )

    # Save to history
    db.save_analysis(
        user_id=session["user_id"],
        analysis_type="medication_safety",
        input_data=", ".join(medicines),
        result=json.dumps(result)
    )

    return success({"result": result})


@app.route("/api/analyze/side-effects", methods=["POST"])
@require_auth
def analyze_side_effects():
    data = request.get_json() or {}
    medicine = data.get("medicine", "").strip()

    if not medicine:
        return error("Medicine name is required.")

    user_id = session["user_id"]
    profile = db.get_profile(user_id)
    diseases = db.get_diseases(user_id)
    daily_meds = db.get_medications(user_id)

    result = ai_engine.analyze_side_effects(
        medicine=medicine,
        profile=profile,
        diseases=diseases,
        daily_medications=daily_meds
    )

    db.save_analysis(
        user_id=session["user_id"],
        analysis_type="side_effects",
        input_data=medicine,
        result=json.dumps(result)
    )

    return success({"result": result})


@app.route("/api/analyze/alternatives", methods=["POST"])
@require_auth
def analyze_alternatives():
    data = request.get_json() or {}
    medicine = data.get("medicine", "").strip()

    if not medicine:
        return error("Medicine name is required.")

    user_id = session["user_id"]
    profile = db.get_profile(user_id)
    diseases = db.get_diseases(user_id)
    daily_meds = db.get_medications(user_id)

    result = ai_engine.recommend_alternatives(
        medicine=medicine,
        profile=profile,
        diseases=diseases,
        daily_medications=daily_meds
    )

    db.save_analysis(
        user_id=session["user_id"],
        analysis_type="alternatives",
        input_data=medicine,
        result=json.dumps(result)
    )

    return success({"result": result})


@app.route("/api/analyze/nutrition", methods=["POST"])
@require_auth
def analyze_nutrition():
    user_id = session["user_id"]
    profile = db.get_profile(user_id)
    diseases = db.get_diseases(user_id)
    medications = db.get_medications(user_id)

    if not profile:
        return error("Please complete your health profile first.")

    result = ai_engine.generate_nutrition_advice(profile, diseases, medications)

    db.save_analysis(
        user_id=user_id,
        analysis_type="nutrition",
        input_data=f"Profile: {profile.get('name')}, Conditions: {len(diseases)}, Meds: {len(medications)}",
        result=json.dumps(result)
    )

    return success({"result": result})


# ─── CHAT ROUTES ───────────────────────────────────────────────────────────────

@app.route("/api/chat", methods=["POST"])
@require_auth
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return error("Message cannot be empty.")

    user_id = session["user_id"]
    profile = db.get_profile(user_id)
    diseases = db.get_diseases(user_id)
    medications = db.get_medications(user_id)
    chat_history = db.get_chat_history(user_id, limit=20)

    # Get AI response
    response = ai_engine.chat_with_assistant(
        user_message=user_message,
        chat_history=chat_history,
        profile=profile,
        diseases=diseases,
        medications=medications
    )

    # Save both messages
    db.save_chat_message(user_id, "user", user_message)
    db.save_chat_message(user_id, "assistant", response)

    return success({"response": response})


@app.route("/api/chat/history", methods=["GET"])
@require_auth
def get_chat_history():
    history = db.get_chat_history(session["user_id"], limit=50)
    return success({"history": history})


@app.route("/api/chat/clear", methods=["POST"])
@require_auth
def clear_chat():
    db.clear_chat_history(session["user_id"])
    return success(message="Chat history cleared.")


# ─── HISTORY ROUTES ────────────────────────────────────────────────────────────

@app.route("/api/history", methods=["GET"])
@require_auth
def get_history():
    history = db.get_analysis_history(session["user_id"], limit=50)
    return success({"history": history})


# ─── PDF REPORT ROUTES ─────────────────────────────────────────────────────────

@app.route("/api/reports/generate", methods=["POST"])
@require_auth
def generate_report():
    user_id = session["user_id"]
    profile = db.get_profile(user_id)
    diseases = db.get_diseases(user_id)
    medications = db.get_medications(user_id)
    analyses = db.get_analysis_history(user_id, limit=10)

    result = pdf_generator.generate_health_report(
        profile=profile,
        diseases=diseases,
        medications=medications,
        analyses=analyses,
        reports_dir=REPORTS_DIR
    )

    if not result["success"]:
        return error(result["error"])

    # Save report record
    db.save_pdf_report(user_id, result["filename"], result["file_path"])

    return success({
        "filename": result["filename"],
        "download_url": f"/api/reports/download/{result['filename']}"
    }, "PDF report generated successfully!")


@app.route("/api/reports/download/<filename>", methods=["GET"])
@require_auth
def download_report(filename):
    safe_filename = secure_filename(filename)
    file_path = os.path.join(REPORTS_DIR, safe_filename)

    if not os.path.exists(file_path):
        return error("Report not found.", 404)

    return send_file(file_path, as_attachment=True, download_name=safe_filename)


@app.route("/api/reports", methods=["GET"])
@require_auth
def get_reports():
    reports = db.get_pdf_reports(session["user_id"])
    return success({"reports": reports})


# ─── HEALTH CHECK ──────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "app": "MedAssist AI",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    })


# ─── SERVE FRONTEND ────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  [MedAssist AI] Starting Server")
    print("="*60)
    print(f"  Backend:  http://localhost:5000")
    print(f"  API Docs: http://localhost:5000/api/health")
    print(f"  Database: {os.path.join(BASE_DIR, 'database.db')}")
    print("="*60 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)