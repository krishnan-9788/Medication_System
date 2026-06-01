import os
from PIL import Image, ImageDraw, ImageFont

def generate_pdf_prescription():
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        pdf_path = "tests/rx_prescription_harish.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                                rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor='#1A365D',
            spaceAfter=15
        )
        
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=16,
            spaceAfter=10
        )
        
        story = []
        story.append(Paragraph("METRO HEALTH CLINIC", title_style))
        story.append(Paragraph("123 Health Ave, New Delhi | Tel: +91 11 2345 6789", body_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph("<b>PATIENT:</b> Harish Kumar", body_style))
        story.append(Paragraph("<b>AGE:</b> 68  |  <b>GENDER:</b> Male", body_style))
        story.append(Paragraph("<b>DATE:</b> May 30, 2026", body_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph("<b>PRESCRIPTION DIAGNOSIS:</b> Type 2 Diabetes, Severe Hypertension", body_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>MEDICATIONS:</b>", body_style))
        story.append(Paragraph("1. Metformin 500mg - Take 1 tablet twice daily after meals (morning and night).", body_style))
        story.append(Paragraph("2. Amlodipine 5mg - Take 1 tablet once daily in the morning.", body_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph("<b>DOCTOR NOTES:</b> Avoid high salt foods. Monitor blood sugar and blood pressure daily. Return for follow-up in 4 weeks.", body_style))
        story.append(Spacer(1, 30))
        story.append(Paragraph("Dr. Sameer Gupta, MD (Cardiology)<br/>Reg No: 98765-A", body_style))
        
        doc.build(story)
        print(f"Successfully generated: {pdf_path}")
    except Exception as e:
        print(f"Error generating PDF: {e}")

def generate_png_prescription():
    try:
        # Create a white background image
        img = Image.new('RGB', (800, 1000), color='white')
        d = ImageDraw.Draw(img)
        
        # Load default font
        font = ImageFont.load_default()
        
        # Draw doctor header
        d.text((50, 50), "CITY PULMONARY CARE CENTER", fill=(26, 54, 93))
        d.text((50, 75), "Priya Sharma, Age 29, Female", fill=(0, 0, 0))
        d.text((50, 95), "Date: May 30, 2026", fill=(0, 0, 0))
        
        d.text((50, 150), "DIAGNOSIS: Chronic Asthma and Acid Reflux (GERD)", fill=(0, 0, 0))
        
        d.text((50, 220), "Rx:", fill=(26, 54, 93))
        d.text((50, 250), "1. Montelukast 10mg - 1 tablet daily at night.", fill=(0, 0, 0))
        d.text((50, 290), "2. Pantoprazole 40mg - 1 tablet daily before breakfast.", fill=(0, 0, 0))
        d.text((50, 330), "3. Inhaler Levosalbutamol - 2 puffs as needed for shortness of breath.", fill=(0, 0, 0))
        
        d.text((50, 420), "DOCTOR NOTES:", fill=(0, 0, 0))
        d.text((50, 450), "Avoid cold items, pollen, and sleeping immediately after meals.", fill=(0, 0, 0))
        
        d.text((50, 550), "Dr. Ananya Roy, DNB (Pulmonology)", fill=(0, 0, 0))
        
        png_path = "tests/rx_prescription_priya.png"
        img.save(png_path)
        print(f"Successfully generated: {png_path}")
    except Exception as e:
        print(f"Error generating PNG prescription: {e}")

def generate_png_lab_report():
    try:
        img = Image.new('RGB', (800, 1000), color='white')
        d = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        
        d.text((50, 50), "APEX DIAGNOSTICS LAB REPORT", fill=(220, 20, 60))
        d.text((50, 80), "Patient Name: Robert D'Souza", fill=(0, 0, 0))
        d.text((50, 100), "Age: 72  |  Gender: Male", fill=(0, 0, 0))
        d.text((50, 120), "Ref By: Dr. J. Fernandes", fill=(0, 0, 0))
        d.text((50, 140), "Date: May 30, 2026", fill=(0, 0, 0))
        
        d.text((50, 200), "TEST RESULTS:", fill=(26, 54, 93))
        d.text((50, 230), "Serum Creatinine: 2.1 mg/dL   (High)   [Normal: 0.7 - 1.3]", fill=(0, 0, 0))
        d.text((50, 270), "Estimated GFR (eGFR): 32 mL/min/1.73m2 (Low) [Normal: > 90]", fill=(0, 0, 0))
        d.text((50, 310), "Serum Uric Acid: 8.8 mg/dL    (High)   [Normal: 3.5 - 7.2]", fill=(0, 0, 0))
        d.text((50, 350), "Blood Urea Nitrogen: 38 mg/dL   (High)   [Normal: 7 - 20]", fill=(0, 0, 0))
        
        d.text((50, 420), "CLINICAL REMARKS / DIAGNOSIS:", fill=(0, 0, 0))
        d.text((50, 450), "Consistent with Stage 3 Chronic Kidney Disease (CKD) and Hyperuricemia (Gout).", fill=(0, 0, 0))
        d.text((50, 480), "Avoid NSAIDs like Naproxen, Ibuprofen, Diclofenac.", fill=(0, 0, 0))
        d.text((50, 510), "Prescribed daily Allopurinol 100mg and Losartan 50mg.", fill=(0, 0, 0))
        
        d.text((50, 600), "Pathologist Signature", fill=(0, 0, 0))
        
        png_path = "tests/lab_report_robert.png"
        img.save(png_path)
        print(f"Successfully generated: {png_path}")
    except Exception as e:
        print(f"Error generating PNG lab report: {e}")

if __name__ == "__main__":
    os.makedirs("tests", exist_ok=True)
    generate_pdf_prescription()
    generate_png_prescription()
    generate_png_lab_report()
