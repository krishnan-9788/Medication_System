"""
ai_engine.py - Groq AI Integration Layer for MedAssist AI
All Groq LLM prompts and AI interactions are centralized here.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "YOUR_GROQ_API_KEY_HERE":
        raise ValueError("GROQ_API_KEY not set. Please add your key to the .env file.")
    return Groq(api_key=api_key)


def _call_groq(system_prompt: str, user_message: str, max_tokens: int = 1500) -> str:
    """Internal helper to call Groq API with error handling."""
    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.4,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except ValueError as e:
        return f"ERROR: {str(e)}"
    except Exception as e:
        return f"ERROR: Groq API call failed - {str(e)}"


# ─── MEDICATION SAFETY ANALYZER ────────────────────────────────────────────────

def analyze_medication_safety(new_medicines: list, profile: dict = None, diseases: list = None, daily_medications: list = None) -> dict:
    """
    Analyze drug interactions and safety for a list of new medicines in context of patient's history.
    """
    new_meds_str = ", ".join(new_medicines)
    
    # Construct context info
    context_str = "No existing profile/conditions recorded."
    if profile or diseases or daily_medications:
        context_parts = []
        if profile:
            context_parts.append(f"- Profile: Age {profile.get('age', '?')} years, Gender {profile.get('gender', '?')}, Weight {profile.get('weight', '?')} kg, Height {profile.get('height', '?')} cm, Blood group {profile.get('blood_group', '?')}")
        if diseases:
            d_names = [d.get("disease_name") for d in diseases]
            context_parts.append(f"- Stored Medical Conditions (Diseases): {', '.join(d_names)}")
        if daily_medications:
            m_names = [f"{m.get('medicine_name')} ({m.get('dosage')}, {m.get('frequency')})" for m in daily_medications]
            context_parts.append(f"- Stored Daily Medications (Taken regularly): {', '.join(m_names)}")
        context_str = "\n".join(context_parts)

    system_prompt = f"""You are a clinical pharmacist AI assistant. Do not use any emojis in your response.
    Analyze the safety of taking the new medication(s) in context of the patient's existing health profile, stored chronic conditions (diseases), and stored daily medications they are already taking.
    Identify any interactions between the new medicines and the daily medicines, and check if the new medicines exacerbate the chronic conditions.
    
    Patient Context:
    {context_str}
    
    Respond ONLY in this exact JSON format:
    {{
      "risk_level": "Safe|Moderate Risk|High Risk|Dangerous",
      "risk_score": 0-10,
      "interactions": ["interaction between new medicine and daily medicines or other new medicines"],
      "warnings": ["specific warnings about new medicine worsening stored chronic conditions or reacting with daily medicines"],
      "recommendations": ["recommendation 1", "recommendation 2"],
      "summary": "Brief professional summary of the analysis showing how the new medicine fits into the patient's existing regimen",
      "individual_medicines": [
        {{"name": "medicine name", "category": "drug class", "note": "key note (e.g. daily medicine, or new medicine)"}}
      ]
    }}
    Only return valid JSON. No preamble or explanation outside the JSON."""

    user_message = f"Analyze these new medications for safety and interactions: {new_meds_str}"

    raw = _call_groq(system_prompt, user_message, max_tokens=1200)

    try:
        import json
        raw_clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw_clean)
    except Exception:
        # Fallback structured response
        return {
            "risk_level": "Unknown",
            "risk_score": 5,
            "interactions": [],
            "warnings": ["Could not parse structured response"],
            "recommendations": [],
            "summary": raw,
            "individual_medicines": []
        }


# ─── SIDE EFFECT ANALYZER ──────────────────────────────────────────────────────

def analyze_side_effects(medicine: str, profile: dict = None, diseases: list = None, daily_medications: list = None) -> dict:
    """
    Get detailed side effects for a specific medicine, analyzed in context of the patient's health profile.
    """
    # Construct context info
    context_str = "No existing profile/conditions recorded."
    if profile or diseases or daily_medications:
        context_parts = []
        if profile:
            context_parts.append(f"- Profile: Age {profile.get('age', '?')} years, Gender {profile.get('gender', '?')}, Weight {profile.get('weight', '?')} kg")
        if diseases:
            d_names = [d.get("disease_name") for d in diseases]
            context_parts.append(f"- Stored Medical Conditions (Diseases): {', '.join(d_names)}")
        if daily_medications:
            m_names = [m.get('medicine_name') for m in daily_medications]
            context_parts.append(f"- Stored Daily Medications (Taken regularly): {', '.join(m_names)}")
        context_str = "\n".join(context_parts)

    system_prompt = f"""You are a medical information AI. Provide detailed side effects for the medication. Do not use any emojis in your response.
    Additionally, analyze whether the patient's existing profile, medical conditions, or stored daily medications will increase the risk/severity of these side effects or introduce contraindications.
    
    Patient Context:
    {context_str}
    
    Respond ONLY in this exact JSON format:
    {{
      "medicine": "medicine name",
      "generic_name": "generic/chemical name",
      "drug_class": "pharmacological class",
      "common_side_effects": ["effect 1", "effect 2", "effect 3"],
      "moderate_side_effects": ["effect 1", "effect 2"],
      "rare_side_effects": ["effect 1", "effect 2"],
      "serious_warnings": ["warning 1", "warning 2"],
      "contraindications": ["condition 1", "condition 2"],
      "patient_specific_warnings": ["List specific personalized side effect risks or warnings due to the patient's stored conditions or daily medications. Example: 'Since you have Hypertension, Ibuprofen can increase blood pressure further.' or 'Ibuprofen interacts with your stored Lisinopril, potentially increasing risk of kidney side effects.' If no specific risks, return an empty array."],
      "when_to_seek_help": "Guidance on when to contact a doctor"
    }}
    Only return valid JSON."""

    user_message = f"Provide comprehensive side effect profile and patient compatibility for: {medicine}"

    raw = _call_groq(system_prompt, user_message, max_tokens=1000)

    try:
        import json
        raw_clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw_clean)
    except Exception:
        return {
            "medicine": medicine,
            "generic_name": "N/A",
            "drug_class": "N/A",
            "common_side_effects": [],
            "moderate_side_effects": [],
            "rare_side_effects": [],
            "serious_warnings": ["Could not parse structured response"],
            "contraindications": [],
            "patient_specific_warnings": [],
            "when_to_seek_help": raw
        }


# ─── ALTERNATIVE MEDICINE RECOMMENDER ─────────────────────────────────────────

def recommend_alternatives(medicine: str, profile: dict = None, diseases: list = None, daily_medications: list = None) -> dict:
    """
    Recommend alternative medicines for a given medication, customized for the patient's health profile.
    """
    # Construct context info
    context_str = "No existing profile/conditions recorded."
    if profile or diseases or daily_medications:
        context_parts = []
        if profile:
            context_parts.append(f"- Profile: Age {profile.get('age', '?')} years, Gender {profile.get('gender', '?')}, Weight {profile.get('weight', '?')} kg")
        if diseases:
            d_names = [d.get("disease_name") for d in diseases]
            context_parts.append(f"- Stored Medical Conditions (Diseases): {', '.join(d_names)}")
        if daily_medications:
            m_names = [m.get('medicine_name') for m in daily_medications]
            context_parts.append(f"- Stored Daily Medications (Taken regularly): {', '.join(m_names)}")
        context_str = "\n".join(context_parts)

    system_prompt = f"""You are a clinical pharmacist AI. Suggest safe and evidence-based alternative medicines. Do not use any emojis in your response.
    Ensure recommended alternatives do not interact negatively with the patient's stored daily medications and are safe to take with the patient's chronic conditions.
    
    Patient Context:
    {context_str}
    
    Respond ONLY in this exact JSON format:
    {{
      "original_medicine": "medicine name",
      "original_class": "drug class",
      "reason_for_alternatives": "Why someone might seek alternatives",
      "patient_specific_warnings": ["Specific personalized warnings about why the original medicine clashes with the patient's profile/conditions/meds, or any caution for alternatives. If none, return empty array."],
      "alternatives": [
        {{
          "name": "alternative medicine name",
          "type": "Generic|Brand|Natural",
          "reason": "Why this is a good alternative and why it is safe specifically for this patient's profile",
          "notes": "Important usage notes or precautions",
          "availability": "Common/Less Common"
        }}
      ],
      "general_advice": "Overall advice about switching medications",
      "disclaimer": "Always consult your doctor before switching medications"
    }}
    Only return valid JSON."""

    user_message = f"Suggest alternatives for: {medicine}"

    raw = _call_groq(system_prompt, user_message, max_tokens=1200)

    try:
        import json
        raw_clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw_clean)
    except Exception:
        return {
            "original_medicine": medicine,
            "original_class": "N/A",
            "reason_for_alternatives": "N/A",
            "patient_specific_warnings": [],
            "alternatives": [],
            "general_advice": raw,
            "disclaimer": "Always consult your doctor before switching medications."
        }


# ─── NUTRITION ADVISOR ─────────────────────────────────────────────────────────

def generate_nutrition_advice(profile: dict, diseases: list, medications: list) -> dict:
    """
    Generate personalized nutrition advice based on profile, diseases, and medications.
    """
    disease_names = [d.get("disease_name", "") for d in diseases]
    med_names = [m.get("medicine_name", "") for m in medications]

    context = f"""
    Patient Profile:
    - Age: {profile.get('age', 'Unknown')}
    - Gender: {profile.get('gender', 'Unknown')}
    - Weight: {profile.get('weight', 'Unknown')} kg
    - Height: {profile.get('height', 'Unknown')} cm
    - Blood Group: {profile.get('blood_group', 'Unknown')}
    
    Conditions: {', '.join(disease_names) if disease_names else 'None reported'}
    Medications: {', '.join(med_names) if med_names else 'None reported'}
    """

    system_prompt = """You are a clinical nutritionist AI. Provide personalized dietary guidance based on the patient profile. Do not use any emojis in your response.
    
    Respond ONLY in this exact JSON format:
    {
      "foods_to_eat": [
        {"food": "food name", "reason": "why beneficial", "frequency": "how often"}
      ],
      "foods_to_avoid": [
        {"food": "food name", "reason": "why to avoid"}
      ],
      "daily_tips": ["tip 1", "tip 2", "tip 3", "tip 4", "tip 5"],
      "hydration_advice": "Detailed hydration guidance",
      "meal_timing": "Advice on meal timing and frequency",
      "supplements_to_consider": ["supplement 1", "supplement 2"],
      "lifestyle_habits": ["habit 1", "habit 2", "habit 3"],
      "calorie_guidance": "General calorie intake guidance",
      "disclaimer": "This is educational guidance only. Consult a registered dietitian for personalized medical nutrition therapy."
    }
    Only return valid JSON."""

    user_message = f"Generate personalized nutrition advice for this patient:\n{context}"

    raw = _call_groq(system_prompt, user_message, max_tokens=1500)

    try:
        import json
        raw_clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw_clean)
    except Exception:
        return {
            "foods_to_eat": [],
            "foods_to_avoid": [],
            "daily_tips": [],
            "hydration_advice": raw,
            "meal_timing": "N/A",
            "supplements_to_consider": [],
            "lifestyle_habits": [],
            "calorie_guidance": "N/A",
            "disclaimer": "This is educational guidance only. Consult a registered dietitian."
        }


# ─── HEALTH CHAT ASSISTANT ─────────────────────────────────────────────────────

def chat_with_assistant(user_message: str, chat_history: list, profile: dict = None, diseases: list = None, medications: list = None) -> str:
    """
    Health chatbot using Groq. Maintains conversation context.
    """
    context_parts = ["You are MedAssist AI, a helpful and knowledgeable health assistant."]
    context_parts.append("You provide accurate, evidence-based health information. Do not use any emojis in your responses, maintain a professional tone.")
    context_parts.append("Always advise users to consult a doctor for medical decisions.")

    if profile:
        context_parts.append(f"Patient context: {profile.get('age', '?')} y/o {profile.get('gender', '?')}, Blood group: {profile.get('blood_group', '?')}")

    if diseases:
        disease_names = [d.get("disease_name", "") for d in diseases]
        context_parts.append(f"Known conditions: {', '.join(disease_names)}")

    if medications:
        med_names = [m.get("medicine_name", "") for m in medications]
        context_parts.append(f"Current medications: {', '.join(med_names)}")

    system_prompt = " ".join(context_parts)

    # Build message history for Groq (max last 10 turns to stay within context)
    messages = [{"role": "system", "content": system_prompt}]
    for entry in chat_history[-10:]:
        messages.append({"role": entry["role"], "content": entry["message"]})
    messages.append({"role": "user", "content": user_message})

    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.5,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except ValueError as e:
        return f"Configuration error: {str(e)}"
    except Exception as e:
        return f"I'm sorry, I couldn't process that right now. Please try again. ({str(e)})"


# ─── OCR TEXT ANALYSIS ─────────────────────────────────────────────────────────

def analyze_ocr_text(extracted_text: str) -> dict:
    """
    Parse and structure OCR-extracted text from medical documents.
    """
    system_prompt = """You are a medical document parser AI. Extract structured information from raw OCR text of medical reports/prescriptions.
    
    Respond ONLY in this exact JSON format:
    {
      "detected_medicines": ["medicine 1", "medicine 2"],
      "detected_conditions": ["condition 1", "condition 2"],
      "dosage_instructions": ["instruction 1", "instruction 2"],
      "doctor_notes": ["note 1", "note 2"],
      "document_type": "Prescription|Lab Report|Discharge Summary|Other",
      "key_findings": ["finding 1", "finding 2"],
      "summary": "Brief summary of the document content"
    }
    Only return valid JSON. If nothing is detected for a field, return an empty array."""

    user_message = f"Parse this medical document OCR text:\n\n{extracted_text[:3000]}"

    raw = _call_groq(system_prompt, user_message, max_tokens=800)

    try:
        import json
        raw_clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw_clean)
    except Exception:
        return {
            "detected_medicines": [],
            "detected_conditions": [],
            "dosage_instructions": [],
            "doctor_notes": [],
            "document_type": "Other",
            "key_findings": [],
            "summary": "Could not parse document structure."
        }