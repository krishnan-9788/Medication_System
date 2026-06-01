"""
db.py - Database Layer for MedAssist AI
Handles all SQLite database operations: creation, CRUD, and queries.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all required tables if they don't exist."""
    conn = get_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Profiles table
    c.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            name TEXT,
            age INTEGER,
            gender TEXT,
            weight REAL,
            height REAL,
            blood_group TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Diseases table
    c.execute("""
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            disease_name TEXT NOT NULL,
            severity TEXT,
            notes TEXT,
            diagnosed_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Medications table
    c.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            medicine_name TEXT NOT NULL,
            dosage TEXT,
            frequency TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # OCR Reports table
    c.execute("""
        CREATE TABLE IF NOT EXISTS ocr_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            extracted_text TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Analysis History table
    c.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            analysis_type TEXT NOT NULL,
            input_data TEXT,
            result TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # PDF Reports table
    c.execute("""
        CREATE TABLE IF NOT EXISTS pdf_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Chat History table
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")


# ─── USER OPERATIONS ───────────────────────────────────────────────────────────

def create_user(username, email, password_hash):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user_by_username(username):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ─── PROFILE OPERATIONS ────────────────────────────────────────────────────────

def upsert_profile(user_id, name, age, gender, weight, height, blood_group):
    conn = get_connection()
    existing = conn.execute("SELECT id FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
    now = datetime.utcnow().isoformat()
    if existing:
        conn.execute("""
            UPDATE profiles SET name=?, age=?, gender=?, weight=?, height=?, blood_group=?, updated_at=?
            WHERE user_id=?
        """, (name, age, gender, weight, height, blood_group, now, user_id))
    else:
        conn.execute("""
            INSERT INTO profiles (user_id, name, age, gender, weight, height, blood_group, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, name, age, gender, weight, height, blood_group, now))
    conn.commit()
    conn.close()


def get_profile(user_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ─── DISEASE OPERATIONS ────────────────────────────────────────────────────────

def add_disease(user_id, disease_name, severity="", notes="", diagnosed_date=""):
    conn = get_connection()
    conn.execute("""
        INSERT INTO diseases (user_id, disease_name, severity, notes, diagnosed_date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, disease_name, severity, notes, diagnosed_date))
    conn.commit()
    conn.close()


def get_diseases(user_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM diseases WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_disease(disease_id, user_id, disease_name, severity, notes, diagnosed_date):
    conn = get_connection()
    conn.execute("""
        UPDATE diseases SET disease_name=?, severity=?, notes=?, diagnosed_date=?
        WHERE id=? AND user_id=?
    """, (disease_name, severity, notes, diagnosed_date, disease_id, user_id))
    conn.commit()
    conn.close()


def delete_disease(disease_id, user_id):
    conn = get_connection()
    conn.execute("DELETE FROM diseases WHERE id=? AND user_id=?", (disease_id, user_id))
    conn.commit()
    conn.close()


# ─── MEDICATION OPERATIONS ─────────────────────────────────────────────────────

def add_medication(user_id, medicine_name, dosage="", frequency="", notes=""):
    conn = get_connection()
    conn.execute("""
        INSERT INTO medications (user_id, medicine_name, dosage, frequency, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, medicine_name, dosage, frequency, notes))
    conn.commit()
    conn.close()


def get_medications(user_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM medications WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_medication(med_id, user_id, medicine_name, dosage, frequency, notes):
    conn = get_connection()
    conn.execute("""
        UPDATE medications SET medicine_name=?, dosage=?, frequency=?, notes=?
        WHERE id=? AND user_id=?
    """, (medicine_name, dosage, frequency, notes, med_id, user_id))
    conn.commit()
    conn.close()


def delete_medication(med_id, user_id):
    conn = get_connection()
    conn.execute("DELETE FROM medications WHERE id=? AND user_id=?", (med_id, user_id))
    conn.commit()
    conn.close()


# ─── OCR REPORT OPERATIONS ─────────────────────────────────────────────────────

def save_ocr_report(user_id, filename, file_path, extracted_text):
    conn = get_connection()
    conn.execute("""
        INSERT INTO ocr_reports (user_id, filename, file_path, extracted_text)
        VALUES (?, ?, ?, ?)
    """, (user_id, filename, file_path, extracted_text))
    conn.commit()
    conn.close()


def get_ocr_reports(user_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM ocr_reports WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── ANALYSIS HISTORY OPERATIONS ───────────────────────────────────────────────

def save_analysis(user_id, analysis_type, input_data, result):
    conn = get_connection()
    conn.execute("""
        INSERT INTO analysis_history (user_id, analysis_type, input_data, result)
        VALUES (?, ?, ?, ?)
    """, (user_id, analysis_type, input_data, result))
    conn.commit()
    conn.close()


def get_analysis_history(user_id, limit=50):
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM analysis_history WHERE user_id = ?
        ORDER BY created_at DESC LIMIT ?
    """, (user_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── PDF REPORT OPERATIONS ─────────────────────────────────────────────────────

def save_pdf_report(user_id, filename, file_path):
    conn = get_connection()
    conn.execute("""
        INSERT INTO pdf_reports (user_id, filename, file_path)
        VALUES (?, ?, ?)
    """, (user_id, filename, file_path))
    conn.commit()
    conn.close()


def get_pdf_reports(user_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM pdf_reports WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── CHAT HISTORY OPERATIONS ───────────────────────────────────────────────────

def save_chat_message(user_id, role, message):
    conn = get_connection()
    conn.execute("""
        INSERT INTO chat_history (user_id, role, message)
        VALUES (?, ?, ?)
    """, (user_id, role, message))
    conn.commit()
    conn.close()


def get_chat_history(user_id, limit=50):
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM chat_history WHERE user_id = ?
        ORDER BY created_at ASC LIMIT ?
    """, (user_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def clear_chat_history(user_id):
    conn = get_connection()
    conn.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


# ─── DASHBOARD STATS ───────────────────────────────────────────────────────────

def get_dashboard_stats(user_id):
    conn = get_connection()
    stats = {
        "disease_count": conn.execute("SELECT COUNT(*) FROM diseases WHERE user_id=?", (user_id,)).fetchone()[0],
        "medication_count": conn.execute("SELECT COUNT(*) FROM medications WHERE user_id=?", (user_id,)).fetchone()[0],
        "report_count": conn.execute("SELECT COUNT(*) FROM ocr_reports WHERE user_id=?", (user_id,)).fetchone()[0],
        "analysis_count": conn.execute("SELECT COUNT(*) FROM analysis_history WHERE user_id=?", (user_id,)).fetchone()[0],
        "pdf_count": conn.execute("SELECT COUNT(*) FROM pdf_reports WHERE user_id=?", (user_id,)).fetchone()[0],
    }
    conn.close()
    return stats