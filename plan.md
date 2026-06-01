
# PROJECT GENERATION PROMPT



Create a complete production-ready AI healthcare web application called:



# MedAssist AI



### AI-Powered Medication Safety, Medical Report Analysis & Nutrition Guidance Platform



---



# IMPORTANT



This is a FULL WORKING PROJECT.



Generate all source code files.



Generate complete folder structure.



Generate backend, frontend, database, OCR processing, Groq integration, PDF generation, and all required pages.



Everything must be connected and functional.



Do not generate placeholders except where explicitly mentioned.



The application should be runnable after installing requirements and adding a Groq API key.



---



# PROJECT GOAL



MedAssist AI is a healthcare assistant platform that helps users:



* Maintain health profiles

* Store diseases

* Track medications

* Upload prescriptions and medical reports

* Extract information using OCR

* Analyze medication safety

* Check medicine interactions

* View side effects

* Get alternative medicine suggestions

* Receive AI-generated dietary guidance

* Generate PDF reports

* Maintain analysis history



The application should use OCR + Groq LLM instead of training custom ML models.



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



Storage:



* SQLite Database

* Uploaded Files Folder

* Generated Reports Folder



---



# PROJECT STRUCTURE



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



# ENVIRONMENT FILE



Create:



.env



Include:



GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE



Do not hardcode keys.



Load key from environment.



---



# USER FLOW



Step 1:



User registers.



Step 2:



User logs in.



Step 3:



User creates profile.



Store:



* Name

* Age

* Gender

* Weight

* Height

* Blood Group



---



# DISEASE MANAGEMENT



User can add diseases.



Examples:



* Diabetes

* Hypertension

* Asthma

* Thyroid

* Kidney Disease

* Heart Disease



Store in database.



Allow:



* Add

* Edit

* Delete

* View



---



# MEDICATION MANAGEMENT



User can add medications.



Store:



* Medicine Name

* Dosage

* Frequency

* Notes



Allow:



* Add

* Edit

* Delete

* View



---



# MEDICAL REPORT UPLOAD



User uploads:



* PDF

* PNG

* JPG

* JPEG



Store uploaded files.



---



# OCR PROCESSING



Use EasyOCR.



Extract:



* Medicine Names

* Diseases

* Doctor Notes

* Prescription Text



Display extracted text.



Save extracted content.



---



# GROQ INTEGRATION



Create reusable Groq service.



Load API key from:



.env



Use Groq API.



All AI features must use Groq.



---



# MEDICATION SAFETY ANALYZER



Page:



medication-analyzer.html



User enters:



One or multiple medicines.



Examples:



Paracetamol

Dolo650

Ibuprofen

Aspirin



Send medicines to Groq.



Prompt Groq to analyze:



* Interaction Risk

* Safety

* Warnings

* Recommendations



Display:



Safe

Moderate Risk

High Risk

Dangerous



Include explanation.



---



# SIDE EFFECT ANALYZER



Page:



side-effects.html



User enters medicine name.



Groq should return:



* Common Side Effects

* Moderate Side Effects

* Rare Side Effects

* Safety Warnings



Display professionally.



---



# ALTERNATIVE MEDICINE RECOMMENDER



Page:



alternatives.html



User enters medicine.



Groq returns:



* Alternative Medicines

* Reasons

* Usage Notes



Display as cards.



---



# NUTRITION ADVISOR



Page:



nutrition.html



Use:



User diseases

User profile

User medications



Send to Groq.



Generate:



Foods To Eat



Foods To Avoid



Daily Nutrition Tips



Hydration Advice



Healthy Habits



Display professionally.



Add disclaimer:



Educational guidance only.



---



# HEALTH CHAT ASSISTANT



Create chatbot section.



User can ask:



Can I take Dolo650?



What are side effects of Ibuprofen?



Foods for diabetes?



Analyze my medications.



Use Groq.



Display chat history.



---



# HISTORY PAGE



Store:



* Medication analyses

* Side effect analyses

* Nutrition analyses

* OCR uploads



Allow viewing previous results.



---



# PDF REPORT GENERATOR



Generate downloadable PDF.



Include:



Patient Profile



Diseases



Current Medications



Medication Analysis



Side Effects



Nutrition Suggestions



Date



Save PDF in reports folder.



Allow download.



---



# DASHBOARD



Display:



Profile Summary



Diseases Count



Medication Count



Uploaded Reports



Recent Analyses



Recent PDFs



Health Summary



Modern cards layout.



---



# DATABASE TABLES



Create all required tables automatically.



Include:



users



profiles



diseases



medications



ocr_reports



analysis_history



pdf_reports



chat_history



Use SQLite.



---



# UI REQUIREMENTS



Modern healthcare design.



Responsive.



Mobile friendly.



Sidebar navigation.



Top navigation bar.



Cards.



Professional colors.



Dashboard layout.



Loading indicators.



Success messages.



Error handling.



---



# SECURITY



Validate inputs.



Handle missing files.



Handle OCR failures.



Handle API failures.



Prevent application crashes.



Display user-friendly errors.



---



# REQUIREMENTS.TXT



Generate complete requirements.txt with all required packages.



Include at minimum:



flask



flask-cors



python-dotenv



groq



easyocr



opencv-python



pillow



reportlab



sqlite-utils



numpy



pandas



werkzeug



requests



---



# README



Generate complete README.



Include:



Installation



Setup



Environment Variables



Running Backend



Running Frontend



Project Structure



Features



Troubleshooting



---



# FINAL REQUIREMENT



Generate COMPLETE WORKING SOURCE CODE.



All pages must connect properly.



All APIs must work properly.



All frontend pages must connect to backend APIs.



Database must work.



OCR must work.



Groq integration must work.



PDF generation must work.



History must work.



Dashboard must work.



Navigation must work.



Project should run after:



1. pip install -r requirements.txt



2. Add Groq API key in .env



3. python backend/app.py



Generate production-ready code with proper comments and clean structure.