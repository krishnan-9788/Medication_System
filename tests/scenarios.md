# MedAssist AI - Quality Testing Scenarios

This document outlines **3 comprehensive quality testing scenarios** to verify all sections and integrations of the MedAssist AI application. Each test scenario exercises the full patient lifecycle: health profile, conditions management, daily medication storage, temporary medicine safety checking, side effect lookup, alternative suggestions, personalized nutrition guidance, and health chatbot conversation.

---

## 📋 Scenario 1: Elderly Patient with Diabetes & Hypertension (Severe Profile)
This scenario tests the interactions between common pain relievers (NSAIDs) and diabetic/hypertensive medication regimens.

### 👤 Profile Details
*   **Name**: `Harish Kumar`
*   **Age**: `68`
*   **Gender**: `Male`
*   **Weight**: `74 kg`
*   **Height**: `165 cm`
*   **Blood Group**: `B+`

### 🏥 Medical Conditions
*   **Condition 1**: `Type 2 Diabetes`  
    *   *Severity*: `Moderate`
    *   *Diagnosed Date*: `2020-03-12`
    *   *Notes*: Under dietary and medicinal control.
*   **Condition 2**: `Hypertension`  
    *   *Severity*: `High` (or Severe)
    *   *Diagnosed Date*: `2018-09-05`
    *   *Notes*: Regulated by Amlodipine.

### 💊 Daily Medications (Stored in Database)
1.  **Metformin**
    *   *Dosage*: `500mg`
    *   *Frequency*: `Twice daily after meals`
    *   *Notes*: For blood sugar control.
2.  **Amlodipine**
    *   *Dosage*: `5mg`
    *   *Frequency*: `Once daily in the morning`
    *   *Notes*: For blood pressure control.

### 🧪 Test Case: Lower Back Pain Incident
*   **Situation**: The patient experiences severe lower back pain and wants to take **Ibuprofen 400mg**.

#### 1. Medication Safety Analyzer Test
*   **Input in analyzer**: `Metformin, Amlodipine, Ibuprofen`
*   **Expected AI Output**:
    *   **Risk Level**: `Moderate Risk` or `High Risk`
    *   **Clash identified**: Ibuprofen (an NSAID) reduces the effectiveness of Amlodipine (blood pressure medication) and can increase kidney burden when taken with Metformin.

#### 2. Side Effect Lookup Test
*   **Input**: `Ibuprofen`
*   **Expected AI Output**:
    *   Lists common side effects (nausea, stomach pain, dizziness).
    *   **Personalized warning box**: Should specifically alert that because the patient has *Hypertension*, Ibuprofen can raise blood pressure further, and that it may interact with their stored *Amlodipine* and *Metformin*.

#### 3. Alternative Recommendation Test
*   **Input**: `Ibuprofen`
*   **Expected AI Output**:
    *   Explains that NSAIDs present renal and cardiovascular risks for this profile.
    *   **Alternatives Recommended**: **Acetaminophen (Paracetamol)** as a safer alternative for pain relief because it does not affect blood pressure or kidney function.

#### 4. Personalized Nutrition Advisor Test
*   **Expected AI Output**:
    *   **Foods to Eat**: Fiber-rich items (leafy greens, oats, whole grains), fatty fish, and magnesium-rich foods.
    *   **Foods to Avoid**: High sodium foods (processed meats, chips) and simple refined carbs (white bread, sodas).

#### 5. Chatbot Conversation Test
*   **Query**: `Can I take Ibuprofen while taking Metformin and Amlodipine?`
*   **Expected Response**: AI should warn against combining NSAIDs like Ibuprofen with Amlodipine (due to reduced efficacy and renal risk) and suggest consulting their doctor about Acetaminophen instead.

---

## 📋 Scenario 2: Young Adult with Asthma & Severe Acid Reflux (GERD)
This scenario tests how temporary medications (e.g. fever relievers and antibiotics) interact with respiratory conditions and GI tracts.

### 👤 Profile Details
*   **Name**: `Priya Sharma`
*   **Age**: `29`
*   **Gender**: `Female`
*   **Weight**: `58 kg`
*   **Height**: `162 cm`
*   **Blood Group**: `O-`

### 🏥 Medical Conditions
*   **Condition 1**: `Chronic Asthma`  
    *   *Severity*: `Mild`
    *   *Diagnosed Date*: `2015-05-20`
    *   *Notes*: Uses inhaler during flare-ups.
*   **Condition 2**: `GERD / Acid Reflux`  
    *   *Severity*: `Moderate`
    *   *Diagnosed Date*: `2023-11-10`
    *   *Notes*: Triggers heartburn and acidity.

### 💊 Daily Medications (Stored in Database)
1.  **Montelukast**
    *   *Dosage*: `10mg`
    *   *Frequency*: `Once daily at night`
    *   *Notes*: For asthma prevention.
2.  **Pantoprazole**
    *   *Dosage*: `40mg`
    *   *Frequency*: `Once daily before breakfast`
    *   *Notes*: For reducing acid reflux.

### 🧪 Test Case: Throat Infection & Fever
*   **Situation**: The patient gets a throat infection and fever, and takes **Clarithromycin (500mg)** and **Aspirin (325mg)**.

#### 1. Medication Safety Analyzer Test
*   **Input**: `Montelukast, Pantoprazole, Clarithromycin, Aspirin`
*   **Expected AI Output**:
    *   **Risk Level**: `Moderate Risk`
    *   **Clash identified**: Aspirin is an NSAID that can severely irritate the stomach lining, worsening her active GERD/Acid Reflux. In some patients, Aspirin can also trigger bronchospasms (Asthma attacks).

#### 2. Side Effect Lookup Test
*   **Input**: `Aspirin`
*   **Expected AI Output**:
    *   **Personalized warning box**: Alarms that Aspirin increases gastric acid irritation, which clashes with her GERD, and flags potential triggers for asthma symptoms.

#### 3. Alternative Recommendation Test
*   **Input**: `Aspirin`
*   **Expected AI Output**:
    *   Suggests safer fever relievers. **Acetaminophen** is recommended over Aspirin to prevent GI distress and avoid respiratory triggers.

#### 4. Personalized Nutrition Advisor Test
*   **Expected AI Output**:
    *   **Foods to Eat**: Non-citrus fruits, oatmeal, ginger tea, healthy fats.
    *   **Foods to Avoid**: Acidic foods (tomatoes, lemons), caffeine, chocolate, spicy foods, carbonated drinks.

#### 5. Chatbot Conversation Test
*   **Query**: `Is it safe to take Aspirin if I have acid reflux and asthma?`
*   **Expected Response**: Chatbot should warn that Aspirin can irritate stomach lining (GERD) and sometimes trigger asthma flares, advising her to discuss Acetaminophen with a doctor.

---

## 📋 Scenario 3: Elderly Patient with Chronic Kidney Disease & Gout
This scenario tests strict contraindications of pain relievers in kidney disease.

### 👤 Profile Details
*   **Name**: `Robert D'Souza`
*   **Age**: `72`
*   **Gender**: `Male`
*   **Weight**: `80 kg`
*   **Height**: `172 cm`
*   **Blood Group**: `A+`

### 🏥 Medical Conditions
*   **Condition 1**: `Chronic Kidney Disease`  
    *   *Severity*: `Severe` (Stage 3)
    *   *Diagnosed Date*: `2021-02-15`
    *   *Notes*: GFR is around 32.
*   **Condition 2**: `Gout`  
    *   *Severity*: `Moderate`
    *   *Diagnosed Date*: `2022-07-18`
    *   *Notes*: Causes acute joint flare-ups.

### 💊 Daily Medications (Stored in Database)
1.  **Allopurinol**
    *   *Dosage*: `100mg`
    *   *Frequency*: `Once daily`
    *   *Notes*: To lower uric acid levels.
2.  **Losartan**
    *   *Dosage*: `50mg`
    *   *Frequency*: `Once daily`
    *   *Notes*: For hypertension and kidney protection.

### 🧪 Test Case: Acute Joint Pain Flare-up
*   **Situation**: The patient experiences acute joint pain in the big toe (Gout flare-up) and takes **Naproxen (500mg)** and **Colchicine (0.6mg)**.

#### 1. Medication Safety Analyzer Test
*   **Input**: `Allopurinol, Losartan, Naproxen, Colchicine`
*   **Expected AI Output**:
    *   **Risk Level**: `High Risk` or `Dangerous`
    *   **Clash identified**: Naproxen (NSAID) is heavily contraindicated in Stage 3 CKD because it restricts renal blood flow and can cause acute kidney injury. Colchicine requires dosage adjustments in renal impairment.

#### 2. Side Effect Lookup Test
*   **Input**: `Naproxen`
*   **Expected AI Output**:
    *   **Personalized warning box**: Emphasizes that Naproxen has severe renal toxicity and should be avoided entirely in Stage 3 Chronic Kidney Disease.

#### 3. Alternative Recommendation Test
*   **Input**: `Naproxen`
*   **Expected AI Output**:
    *   Excludes standard NSAIDs. Recommends consulting a nephrologist for low-dose corticosteroids or acetaminophen, and discusses non-medicinal cold packs.

#### 4. Personalized Nutrition Advisor Test
*   **Expected AI Output**:
    *   **Foods to Eat**: Cherries (lowers uric acid), low-fat dairy, plenty of water, low-potassium vegetables.
    *   **Foods to Avoid**: Purine-rich foods (red meat, shellfish, alcohol, yeast extracts) and high-sodium foods.

#### 5. Chatbot Conversation Test
*   **Query**: `Why is Naproxen dangerous for Stage 3 Chronic Kidney Disease?`
*   **Expected Response**: The chatbot explains that NSAIDs block prostaglandins, leading to renal vasoconstriction, which can crash kidney function (e.g. drop GFR further) in Stage 3 CKD.
