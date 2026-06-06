/**
 * script.js — MedAssist AI Frontend
 * All API calls, UI interactions, and state management.
 */

const API = "/api";
let currentUser = null;

// ═══════════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ═══════════════════════════════════════════════════════════

async function fetchAPI(endpoint, method = "GET", body = null) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
    credentials: "include"
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API + endpoint, opts);
  return res.json();
}

function showLoading(text = "Processing...") {
  document.getElementById("loading-overlay").classList.remove("hidden");
  document.getElementById("loading-text").textContent = text;
}

function hideLoading() {
  document.getElementById("loading-overlay").classList.add("hidden");
}

function showToast(message, type = "success") {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.className = `toast toast-${type}`;
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), 3500);
}

function showMsg(id, message, type) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = message;
  el.className = `form-message ${type}`;
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 5000);
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatDate(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("en-IN", { year: "numeric", month: "short", day: "numeric" });
}

function getRiskClass(risk) {
  const r = (risk || "").toLowerCase();
  if (r.includes("safe")) return "risk-safe";
  if (r.includes("moderate")) return "risk-moderate";
  if (r.includes("high")) return "risk-high";
  if (r.includes("dangerous")) return "risk-dangerous";
  return "risk-moderate";
}

function getBadgeClass(type) {
  const map = {
    "medication_safety": "badge-blue",
    "side_effects": "badge-orange",
    "alternatives": "badge-teal",
    "nutrition": "badge-green",
    "ocr": "badge-teal"
  };
  return map[type] || "badge-teal";
}

function analysisTypeLabel(type) {
  const map = {
    "medication_safety": "Drug Safety",
    "side_effects": "Side Effects",
    "alternatives": "Alternatives",
    "nutrition": "Nutrition"
  };
  return map[type] || type.replace(/_/g, " ");
}

// ═══════════════════════════════════════════════════════════
// AUTH
// ═══════════════════════════════════════════════════════════

function switchAuth(panel) {
  document.getElementById("login-form").classList.remove("active");
  document.getElementById("register-form").classList.remove("active");
  document.getElementById(`${panel}-form`).classList.add("active");
}

async function handleLogin() {
  const username = document.getElementById("login-username").value.trim();
  const password = document.getElementById("login-password").value.trim();

  if (!username || !password) {
    showMsg("login-error", "Please enter username and password.", "error");
    return;
  }

  showLoading("Signing in...");
  const data = await fetchAPI("/auth/login", "POST", { username, password });
  hideLoading();

  if (data.success) {
    currentUser = { username: data.username, user_id: data.user_id };
    initApp();
  } else {
    showMsg("login-error", data.error || "Login failed.", "error");
  }
}

async function handleRegister() {
  const username = document.getElementById("reg-username").value.trim();
  const email = document.getElementById("reg-email").value.trim();
  const password = document.getElementById("reg-password").value.trim();

  if (!username || !email || !password) {
    showMsg("register-error", "All fields are required.", "error");
    return;
  }

  showLoading("Creating account...");
  const data = await fetchAPI("/auth/register", "POST", { username, email, password });
  hideLoading();

  if (data.success) {
    showMsg("register-success", "Account created! Please sign in.", "success");
    setTimeout(() => switchAuth("login"), 1500);
  } else {
    showMsg("register-error", data.error || "Registration failed.", "error");
  }
}

async function handleLogout() {
  await fetchAPI("/auth/logout", "POST");
  currentUser = null;
  document.getElementById("auth-screen").classList.remove("hidden");
  document.getElementById("app").classList.add("hidden");
  document.getElementById("login-username").value = "";
  document.getElementById("login-password").value = "";
}

async function checkAuthStatus() {
  try {
    const data = await fetchAPI("/auth/status");
    if (data.authenticated) {
      currentUser = { username: data.username, user_id: data.user_id };
      initApp();
    }
  } catch (e) {
    // Not authenticated — stay on auth screen
  }
}

// ═══════════════════════════════════════════════════════════
// APP INIT & NAVIGATION
// ═══════════════════════════════════════════════════════════

function initApp() {
  document.getElementById("auth-screen").classList.add("hidden");
  document.getElementById("app").classList.remove("hidden");
  document.getElementById("sidebar-username").textContent = currentUser.username;
  document.getElementById("sidebar-avatar").textContent = currentUser.username[0].toUpperCase();
  document.getElementById("topbar-username").textContent = currentUser.username;

  showSection("dashboard");
  loadDashboard();
}

function showSection(name) {
  // Hide all sections
  document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));

  // Show target section
  document.getElementById(`section-${name}`)?.classList.add("active");
  document.querySelector(`[data-section="${name}"]`)?.classList.add("active");

  const titles = {
    dashboard: "Dashboard", profile: "My Profile", diseases: "Medical Conditions",
    medications: "Medications", ocr: "Upload Reports", "med-analyzer": "Drug Safety Analyzer",
    "side-effects": "Side Effect Analyzer", alternatives: "Alternative Medicines",
    nutrition: "Nutrition Guide", chat: "Health Chat", history: "Analysis History",
    reports: "PDF Reports"
  };
  document.getElementById("topbar-title").textContent = titles[name] || name;

  // Close mobile sidebar
  document.getElementById("sidebar").classList.remove("open");

  // Lazy load section data
  const loaders = {
    profile: loadProfile,
    diseases: loadDiseases,
    medications: loadMedications,
    ocr: loadOCRHistory,
    history: loadHistory,
    reports: loadReports,
    chat: loadChatHistory
  };
  if (loaders[name]) loaders[name]();
}

function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("open");
}

// ═══════════════════════════════════════════════════════════
// DASHBOARD
// ═══════════════════════════════════════════════════════════

async function loadDashboard() {
  const data = await fetchAPI("/dashboard");
  if (!data.success) return;

  const s = data.stats;
  document.getElementById("stat-diseases").textContent = s.disease_count ?? "0";
  document.getElementById("stat-meds").textContent = s.medication_count ?? "0";
  document.getElementById("stat-reports").textContent = s.report_count ?? "0";
  document.getElementById("stat-analyses").textContent = s.analysis_count ?? "0";

  // Profile summary
  const profile = data.profile;
  const nameEl = document.getElementById("dashboard-name-display");
  const metaEl = document.getElementById("dashboard-meta-display");
  const detailsEl = document.getElementById("dashboard-profile-details");
  const avatarEl = document.getElementById("dashboard-avatar-initial");
  
  if (profile && profile.name) {
    if(nameEl) nameEl.textContent = profile.name;
    if(avatarEl) avatarEl.textContent = profile.name.charAt(0).toUpperCase();
    
    const ageStr = profile.age ? `${profile.age} years` : "Age N/A";
    const genderStr = profile.gender || "Gender N/A";
    const bloodStr = profile.blood_group || "Blood N/A";
    if(metaEl) metaEl.textContent = `${ageStr} • ${genderStr} • ${bloodStr}`;
    
    if(detailsEl) {
      detailsEl.innerHTML = `
        <div class="p-stat"><div class="p-stat-label">⚖️ Weight</div><div class="p-stat-val">${profile.weight ? profile.weight + " kg" : "-- kg"}</div></div>
        <div class="p-stat"><div class="p-stat-label">📏 Height</div><div class="p-stat-val">${profile.height ? profile.height + " cm" : "-- cm"}</div></div>
        <div class="p-stat"><div class="p-stat-label">🩸 Blood Group</div><div class="p-stat-val">${escapeHtml(profile.blood_group) || "--"}</div></div>
        <div class="p-stat"><div class="p-stat-label">⏱️ Last Updated</div><div class="p-stat-val">Today</div></div>
      `;
    }
    const pEl = document.getElementById("dashboard-profile");
    if(pEl) pEl.style.display = "none";
  } else {
    if(nameEl) nameEl.textContent = "Welcome!";
    if(metaEl) metaEl.textContent = "Please set up your profile";
    const pEl = document.getElementById("dashboard-profile");
    if (pEl) {
      pEl.style.display = "block";
      pEl.innerHTML = `<p class="empty-state" style="margin-top:1rem;">No profile yet. <a href="#" onclick="showSection('profile')">Set up your profile →</a></p>`;
    }
    if(detailsEl) detailsEl.innerHTML = "";
  }

  // Recent analyses
  const recent = data.recent_analyses;
  const rEl = document.getElementById("dashboard-recent");
  if (recent && recent.length > 0) {
    rEl.innerHTML = recent.map(a => {
      let icon = "⚡";
      if(a.analysis_type === "side_effects") icon = "◈";
      if(a.analysis_type === "nutrition") icon = "❋";
      if(a.analysis_type === "ocr") icon = "⊡";
      if(a.analysis_type === "alternatives") icon = "↔";
      return `
        <div class="recent-item">
          <div class="recent-icon">${icon}</div>
          <div class="recent-content">
            <div class="recent-title">${analysisTypeLabel(a.analysis_type)}</div>
            <div class="recent-desc">${escapeHtml(a.input_data || "").substring(0, 40)}...</div>
          </div>
          <div class="recent-time" style="font-size:0.8rem;color:var(--gray);">${formatDate(a.created_at)}</div>
        </div>
      `;
    }).join("");
  } else {
    rEl.innerHTML = `<p class="empty-state">No analyses yet.</p>`;
  }
}

// ═══════════════════════════════════════════════════════════
// PROFILE
// ═══════════════════════════════════════════════════════════

async function loadProfile() {
  const data = await fetchAPI("/profile");
  if (data.profile) {
    const p = data.profile;
    document.getElementById("p-name").value = p.name || "";
    document.getElementById("p-age").value = p.age || "";
    document.getElementById("p-gender").value = p.gender || "";
    document.getElementById("p-weight").value = p.weight || "";
    document.getElementById("p-height").value = p.height || "";
    document.getElementById("p-blood").value = p.blood_group || "";
  }
}

async function saveProfile() {
  const name = document.getElementById("p-name").value.trim();
  if (!name) { showMsg("profile-msg", "Name is required.", "error"); return; }

  showLoading("Saving profile...");
  const data = await fetchAPI("/profile", "POST", {
    name,
    age: document.getElementById("p-age").value || null,
    gender: document.getElementById("p-gender").value,
    weight: document.getElementById("p-weight").value || null,
    height: document.getElementById("p-height").value || null,
    blood_group: document.getElementById("p-blood").value
  });
  hideLoading();

  if (data.success) {
    showMsg("profile-msg", "Profile saved successfully!", "success");
    loadDashboard();
  } else {
    showMsg("profile-msg", data.error || "Failed to save.", "error");
  }
}

// ═══════════════════════════════════════════════════════════
// DISEASES
// ═══════════════════════════════════════════════════════════

async function loadDiseases() {
  const data = await fetchAPI("/diseases");
  const el = document.getElementById("diseases-list");
  if (!data.success || !data.diseases.length) {
    el.innerHTML = `<p class="empty-state">No conditions recorded yet.</p>`;
    return;
  }
  el.innerHTML = data.diseases.map(d => `
    <div class="item-row">
      <div class="item-icon item-icon-teal">♡</div>
      <div class="item-body">
        <div class="item-title">${escapeHtml(d.disease_name)}
          ${d.severity ? `<span class="badge badge-orange ml-1">${escapeHtml(d.severity)}</span>` : ""}
        </div>
        <div class="item-subtitle">
          ${d.diagnosed_date ? "Diagnosed: " + formatDate(d.diagnosed_date) + " · " : ""}
          ${escapeHtml(d.notes) || "No notes"}
        </div>
      </div>
      <div class="item-actions">
        <button class="btn btn-sm btn-danger" onclick="deleteDisease(${d.id})">Delete</button>
      </div>
    </div>
  `).join("");
}

async function addDisease() {
  const name = document.getElementById("d-name").value.trim();
  if (!name) { showMsg("disease-msg", "Condition name is required.", "error"); return; }

  const data = await fetchAPI("/diseases", "POST", {
    disease_name: name,
    severity: document.getElementById("d-severity").value,
    notes: document.getElementById("d-notes").value,
    diagnosed_date: document.getElementById("d-date").value
  });

  if (data.success) {
    showMsg("disease-msg", "Condition added!", "success");
    document.getElementById("d-name").value = "";
    document.getElementById("d-severity").value = "";
    document.getElementById("d-notes").value = "";
    document.getElementById("d-date").value = "";
    loadDiseases();
    loadDashboard();
  } else {
    showMsg("disease-msg", data.error || "Failed to add.", "error");
  }
}

async function deleteDisease(id) {
  if (!confirm("Delete this condition?")) return;
  await fetchAPI(`/diseases/${id}`, "DELETE");
  loadDiseases();
  loadDashboard();
  showToast("Condition removed.", "success");
}

// ═══════════════════════════════════════════════════════════
// MEDICATIONS
// ═══════════════════════════════════════════════════════════

async function loadMedications() {
  const data = await fetchAPI("/medications");
  const el = document.getElementById("medications-list");
  if (!data.success || !data.medications.length) {
    el.innerHTML = `<p class="empty-state">No medications recorded yet.</p>`;
    return;
  }
  el.innerHTML = data.medications.map(m => `
    <div class="item-row">
      <div class="item-icon item-icon-blue">✦</div>
      <div class="item-body">
        <div class="item-title">${escapeHtml(m.medicine_name)}</div>
        <div class="item-subtitle">
          ${m.dosage ? escapeHtml(m.dosage) : ""}
          ${m.frequency ? " · " + escapeHtml(m.frequency) : ""}
          ${m.notes ? " · " + escapeHtml(m.notes) : ""}
        </div>
      </div>
      <div class="item-actions">
        <button class="btn btn-sm btn-danger" onclick="deleteMedication(${m.id})">Delete</button>
      </div>
    </div>
  `).join("");
}

async function addMedication() {
  const name = document.getElementById("m-name").value.trim();
  if (!name) { showMsg("med-msg", "Medicine name is required.", "error"); return; }

  const data = await fetchAPI("/medications", "POST", {
    medicine_name: name,
    dosage: document.getElementById("m-dosage").value,
    frequency: document.getElementById("m-frequency").value,
    notes: document.getElementById("m-notes").value
  });

  if (data.success) {
    showMsg("med-msg", "Medication added!", "success");
    document.getElementById("m-name").value = "";
    document.getElementById("m-dosage").value = "";
    document.getElementById("m-frequency").value = "";
    document.getElementById("m-notes").value = "";
    loadMedications();
    loadDashboard();
  } else {
    showMsg("med-msg", data.error || "Failed to add.", "error");
  }
}

async function deleteMedication(id) {
  if (!confirm("Delete this medication?")) return;
  await fetchAPI(`/medications/${id}`, "DELETE");
  loadMedications();
  loadDashboard();
  showToast("Medication removed.", "success");
}

// ═══════════════════════════════════════════════════════════
// OCR UPLOAD
// ═══════════════════════════════════════════════════════════

let selectedFile = null;

function handleFileSelect(input) {
  selectedFile = input.files[0];
  if (!selectedFile) return;
  document.getElementById("ocr-filename").textContent = selectedFile.name;
  document.getElementById("ocr-selected").classList.remove("hidden");
}

async function uploadOCR() {
  if (!selectedFile) { showToast("Please select a file first.", "error"); return; }

  const formData = new FormData();
  formData.append("file", selectedFile);

  const btn = document.getElementById("ocr-btn-text");
  btn.textContent = "Processing...";
  showLoading("Extracting text with OCR...");

  try {
    const res = await fetch(`${API}/ocr/upload`, {
      method: "POST",
      body: formData,
      credentials: "include"
    });
    const data = await res.json();
    hideLoading();
    btn.textContent = "Extract Text";

    if (data.success) {
      renderOCRResult(data);
      loadOCRHistory();
      loadDashboard();
    } else {
      showToast(data.error || "OCR failed.", "error");
    }
  } catch (e) {
    hideLoading();
    btn.textContent = "Extract Text";
    showToast("Upload failed. Is the server running?", "error");
  }
}

function renderOCRResult(data) {
  const card = document.getElementById("ocr-result-card");
  const body = document.getElementById("ocr-result-body");
  card.classList.remove("hidden");

  const ocr = data.ocr_result;
  const ai = data.ai_analysis || {};

  let html = "";

  if (!ocr.success) {
    html = `<div class="form-message error">${escapeHtml(ocr.error || "OCR extraction failed.")}</div>`;
    body.innerHTML = html;
    return;
  }

  html += `
    <p class="text-muted mb-2" style="font-size:0.82rem;">Words extracted: <strong>${ocr.word_count}</strong> · Method: ${escapeHtml(ocr.method || "image_ocr")}</p>
    <div class="ocr-result-text">${escapeHtml(ocr.text || "No text extracted.")}</div>
  `;

  if (ai && Object.keys(ai).length > 0) {
    html += `<h3 style="margin-bottom:0.75rem;margin-top:0.75rem;">AI Document Analysis</h3>`;
    html += `<div class="ocr-findings">`;

    if (ai.document_type) {
      html += `<div class="ocr-finding-card"><div class="ocr-finding-title">Document Type</div><span class="badge badge-teal">${escapeHtml(ai.document_type)}</span></div>`;
    }
    if (ai.detected_medicines?.length) {
      html += `<div class="ocr-finding-card"><div class="ocr-finding-title">Medicines Found</div>${ai.detected_medicines.map(m => `<span class="tag">${escapeHtml(m)}</span>`).join("")}</div>`;
    }
    if (ai.detected_conditions?.length) {
      html += `<div class="ocr-finding-card"><div class="ocr-finding-title">Conditions Found</div>${ai.detected_conditions.map(c => `<span class="tag">${escapeHtml(c)}</span>`).join("")}</div>`;
    }
    if (ai.key_findings?.length) {
      html += `<div class="ocr-finding-card"><div class="ocr-finding-title">Key Findings</div>${ai.key_findings.map(f => `<span class="tag">${escapeHtml(f)}</span>`).join("")}</div>`;
    }
    html += `</div>`;
    if (ai.summary) {
      html += `<p style="margin-top:0.75rem;font-size:0.875rem;color:var(--gray);">${escapeHtml(ai.summary)}</p>`;
    }
  }

  body.innerHTML = html;
}

async function loadOCRHistory() {
  const data = await fetchAPI("/ocr/reports");
  const el = document.getElementById("ocr-history-list");
  if (!data.success || !data.reports.length) {
    el.innerHTML = `<p class="empty-state">No reports uploaded yet.</p>`;
    return;
  }
  el.innerHTML = data.reports.map(r => `
    <div class="item-row">
      <div class="item-icon item-icon-teal">⊡</div>
      <div class="item-body">
        <div class="item-title">${escapeHtml(r.filename)}</div>
        <div class="item-subtitle">${formatDate(r.created_at)} · ${r.extracted_text ? r.extracted_text.split(" ").length + " words" : "No text"}</div>
      </div>
    </div>
  `).join("");
}

// ═══════════════════════════════════════════════════════════
// MEDICATION SAFETY ANALYZER
// ═══════════════════════════════════════════════════════════

async function analyzeMedications() {
  const input = document.getElementById("ma-medicines").value.trim();
  if (!input) { showToast("Please enter at least one medicine.", "error"); return; }

  const btn = document.getElementById("ma-btn-text");
  btn.textContent = "Analyzing...";
  showLoading("Analyzing medication safety...");

  const data = await fetchAPI("/analyze/medications", "POST", { medicines: input });
  hideLoading();
  btn.textContent = "⚡ Analyze Safety";

  if (!data.success) { showToast(data.error || "Analysis failed.", "error"); return; }

  const r = data.result;
  const riskClass = getRiskClass(r.risk_level || "");

  let html = `<div class="result-card">
    <div class="result-header">
      <h3>Safety Analysis Result</h3>
      <span class="result-risk-badge ${riskClass}">${escapeHtml(r.risk_level || "Unknown")}</span>
      ${r.risk_score !== undefined ? `<span style="color:var(--gray);font-size:0.85rem;">Risk Score: ${r.risk_score}/10</span>` : ""}
    </div>
    <div class="result-body">`;

  if (r.summary) {
    html += `<div class="result-section">
      <div class="result-section-title">Summary</div>
      <p style="font-size:0.9rem;color:var(--dark-2);">${escapeHtml(r.summary)}</p>
    </div>`;
  }

  if (r.interactions?.length) {
    html += `<div class="result-section">
      <div class="result-section-title">Drug Interactions</div>
      <div class="result-list">${r.interactions.map(i => `<div class="result-list-item">${escapeHtml(i)}</div>`).join("")}</div>
    </div>`;
  }

  if (r.warnings?.length) {
    html += `<div class="result-section">
      <div class="result-section-title">⚠️ Warnings</div>
      <div class="result-list">${r.warnings.map(w => `<div class="result-list-item" style="color:var(--red)">${escapeHtml(w)}</div>`).join("")}</div>
    </div>`;
  }

  if (r.recommendations?.length) {
    html += `<div class="result-section">
      <div class="result-section-title">Recommendations</div>
      <div class="result-list">${r.recommendations.map(rec => `<div class="result-list-item">${escapeHtml(rec)}</div>`).join("")}</div>
    </div>`;
  }

  if (r.individual_medicines?.length) {
    html += `<div class="result-section">
      <div class="result-section-title">Individual Medicines</div>
      <div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-top:0.3rem;">
        ${r.individual_medicines.map(m => `
          <div style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:0.5rem 0.75rem;font-size:0.82rem;">
            <strong>${escapeHtml(m.name)}</strong><br>
            <span style="color:var(--teal)">${escapeHtml(m.category)}</span><br>
            <span style="color:var(--gray)">${escapeHtml(m.note)}</span>
          </div>
        `).join("")}
      </div>
    </div>`;
  }

  html += `</div></div>`;
  const el = document.getElementById("ma-result");
  el.innerHTML = html;
  el.classList.remove("hidden");
}

// ═══════════════════════════════════════════════════════════
// SIDE EFFECTS
// ═══════════════════════════════════════════════════════════

async function analyzeSideEffects() {
  const medicine = document.getElementById("se-medicine").value.trim();
  if (!medicine) { showToast("Please enter a medicine name.", "error"); return; }

  const btn = document.getElementById("se-btn-text");
  btn.textContent = "Analyzing...";
  showLoading(`Looking up side effects for ${medicine}...`);

  const data = await fetchAPI("/analyze/side-effects", "POST", { medicine });
  hideLoading();
  btn.textContent = "◈ Get Side Effects";

  if (!data.success) { showToast(data.error || "Analysis failed.", "error"); return; }

  const r = data.result;
  let html = `<div class="result-card">
    <div class="result-header">
      <div>
        <h3>${escapeHtml(r.medicine || medicine)}</h3>
        ${r.generic_name ? `<span style="color:var(--gray);font-size:0.82rem;">${escapeHtml(r.generic_name)}</span>` : ""}
      </div>
      ${r.drug_class ? `<span class="badge badge-blue">${escapeHtml(r.drug_class)}</span>` : ""}
    </div>
    <div class="result-body">`;

  if (r.patient_specific_warnings && r.patient_specific_warnings.length > 0) {
    html += `<div class="result-section patient-warnings" style="background:#fff5f5;border:2px solid var(--red);border-radius:10px;padding:0.75rem 1rem;margin-bottom:1.5rem;">
      <div class="result-section-title" style="color:var(--red);font-weight:bold;margin-bottom:0.5rem;font-size:0.95rem;">⚠️ Personalized Warning based on your Profile, Conditions & Daily Meds:</div>
      <div class="result-list">
        ${r.patient_specific_warnings.map(w => `<div class="result-list-item" style="color:var(--dark);font-weight:550;">• ${escapeHtml(w)}</div>`).join("")}
      </div>
    </div>`;
  }

  const sections = [
    { key: "common_side_effects", label: "Common Side Effects", color: "var(--dark-2)" },
    { key: "moderate_side_effects", label: "Moderate Side Effects", color: "var(--orange)" },
    { key: "rare_side_effects", label: "Rare Side Effects", color: "var(--gray)" },
    { key: "serious_warnings", label: "⚠️ Serious Warnings", color: "var(--red)" },
    { key: "contraindications", label: "Contraindications", color: "var(--red)" }
  ];

  sections.forEach(s => {
    if (r[s.key]?.length) {
      html += `<div class="result-section">
        <div class="result-section-title">${s.label}</div>
        <div class="result-list">
          ${r[s.key].map(item => `<div class="result-list-item" style="color:${s.color}">${escapeHtml(item)}</div>`).join("")}
        </div>
      </div>`;
    }
  });

  if (r.when_to_seek_help) {
    html += `<div class="disclaimer-box">
      <strong>When to seek help:</strong> ${escapeHtml(r.when_to_seek_help)}
    </div>`;
  }

  html += `</div></div>`;
  const el = document.getElementById("se-result");
  el.innerHTML = html;
  el.classList.remove("hidden");
}

// ═══════════════════════════════════════════════════════════
// ALTERNATIVES
// ═══════════════════════════════════════════════════════════

async function analyzeAlternatives() {
  const medicine = document.getElementById("alt-medicine").value.trim();
  if (!medicine) { showToast("Please enter a medicine name.", "error"); return; }

  const btn = document.getElementById("alt-btn-text");
  btn.textContent = "Searching...";
  showLoading(`Finding alternatives for ${medicine}...`);

  const data = await fetchAPI("/analyze/alternatives", "POST", { medicine });
  hideLoading();
  btn.textContent = "↔ Find Alternatives";

  if (!data.success) { showToast(data.error || "Analysis failed.", "error"); return; }

  const r = data.result;
  let html = `<div class="result-card">
    <div class="result-header">
      <div>
        <h3>Alternatives for ${escapeHtml(r.original_medicine || medicine)}</h3>
        ${r.original_class ? `<span style="color:var(--gray);font-size:0.82rem;">${escapeHtml(r.original_class)}</span>` : ""}
      </div>
    </div>
    <div class="result-body">`;

  if (r.patient_specific_warnings && r.patient_specific_warnings.length > 0) {
    html += `<div class="result-section patient-warnings" style="background:#fff5f5;border:2px solid var(--red);border-radius:10px;padding:0.75rem 1rem;margin-bottom:1.5rem;">
      <div class="result-section-title" style="color:var(--red);font-weight:bold;margin-bottom:0.5rem;font-size:0.95rem;">⚠️ Personalized Warning based on your Profile, Conditions & Daily Meds:</div>
      <div class="result-list">
        ${r.patient_specific_warnings.map(w => `<div class="result-list-item" style="color:var(--dark);font-weight:550;">• ${escapeHtml(w)}</div>`).join("")}
      </div>
    </div>`;
  }

  if (r.reason_for_alternatives) {
    html += `<p style="font-size:0.88rem;color:var(--gray);margin-bottom:1rem;">${escapeHtml(r.reason_for_alternatives)}</p>`;
  }

  if (r.alternatives?.length) {
    html += `<div class="alt-cards-grid">`;
    r.alternatives.forEach(alt => {
      const typeClass = alt.type === "Natural" ? "badge-green" : alt.type === "Generic" ? "badge-blue" : "badge-teal";
      html += `<div class="alt-card">
        <div class="alt-card-name">${escapeHtml(alt.name)}</div>
        <span class="badge ${typeClass} alt-card-type">${escapeHtml(alt.type || "Alternative")}</span>
        ${alt.availability ? `<span class="badge badge-teal" style="margin-left:4px">${escapeHtml(alt.availability)}</span>` : ""}
        <div class="alt-card-reason">${escapeHtml(alt.reason)}</div>
        ${alt.notes ? `<div class="alt-card-note">⚠️ ${escapeHtml(alt.notes)}</div>` : ""}
      </div>`;
    });
    html += `</div>`;
  } else {
    html += `<p class="empty-state">No alternatives found for this medicine.</p>`;
  }

  if (r.general_advice) {
    html += `<div class="result-section" style="margin-top:1rem;">
      <div class="result-section-title">General Advice</div>
      <p style="font-size:0.88rem;color:var(--dark-2);">${escapeHtml(r.general_advice)}</p>
    </div>`;
  }

  html += `<div class="disclaimer-box" style="margin-top:1rem;">${escapeHtml(r.disclaimer || "Always consult your doctor before switching medications.")}</div>`;
  html += `</div></div>`;

  const el = document.getElementById("alt-result");
  el.innerHTML = html;
  el.classList.remove("hidden");
}

// ═══════════════════════════════════════════════════════════
// NUTRITION
// ═══════════════════════════════════════════════════════════

async function analyzeNutrition() {
  const btn = document.getElementById("nut-btn-text");
  btn.textContent = "Generating...";
  showLoading("Creating your personalized nutrition plan...");

  const data = await fetchAPI("/analyze/nutrition", "POST", {});
  hideLoading();
  btn.textContent = "❋ Generate My Nutrition Plan";

  if (!data.success) { showToast(data.error || "Analysis failed.", "error"); return; }

  const r = data.result;
  let html = `<div class="result-card"><div class="result-body">`;

  html += `<div class="nut-grid">`;

  // Foods to eat
  if (r.foods_to_eat?.length) {
    html += `<div class="nut-section eat">
      <div class="result-section-title">✓ Foods to Eat</div>
      ${r.foods_to_eat.map(f => `
        <div class="nut-item">
          <div class="nut-item-food">${escapeHtml(f.food)}</div>
          <div class="nut-item-reason">${escapeHtml(f.reason)} ${f.frequency ? `· ${escapeHtml(f.frequency)}` : ""}</div>
        </div>`).join("")}
    </div>`;
  }

  // Foods to avoid
  if (r.foods_to_avoid?.length) {
    html += `<div class="nut-section avoid">
      <div class="result-section-title">✗ Foods to Avoid</div>
      ${r.foods_to_avoid.map(f => `
        <div class="nut-item">
          <div class="nut-item-food">${escapeHtml(f.food)}</div>
          <div class="nut-item-reason" style="color:var(--red)">${escapeHtml(f.reason)}</div>
        </div>`).join("")}
    </div>`;
  }

  html += `</div>`;

  // Daily tips
  if (r.daily_tips?.length) {
    html += `<div class="nut-section tips" style="margin-bottom:0.75rem;">
      <div class="result-section-title">Daily Nutrition Tips</div>
      ${r.daily_tips.map(t => `<div class="nut-item"><div class="nut-item-food">• ${escapeHtml(t)}</div></div>`).join("")}
    </div>`;
  }

  if (r.hydration_advice) {
    html += `<div class="result-section">
      <div class="result-section-title">💧 Hydration</div>
      <p style="font-size:0.88rem;color:var(--dark-2);">${escapeHtml(r.hydration_advice)}</p>
    </div>`;
  }

  if (r.meal_timing) {
    html += `<div class="result-section">
      <div class="result-section-title">🕐 Meal Timing</div>
      <p style="font-size:0.88rem;color:var(--dark-2);">${escapeHtml(r.meal_timing)}</p>
    </div>`;
  }

  if (r.lifestyle_habits?.length) {
    html += `<div class="result-section">
      <div class="result-section-title">💪 Healthy Habits</div>
      <div class="result-list">${r.lifestyle_habits.map(h => `<div class="result-list-item">${escapeHtml(h)}</div>`).join("")}</div>
    </div>`;
  }

  html += `<div class="disclaimer-box">${escapeHtml(r.disclaimer || "Educational guidance only. Consult a dietitian for personalized advice.")}</div>`;
  html += `</div></div>`;

  const el = document.getElementById("nut-result");
  el.innerHTML = html;
  el.classList.remove("hidden");
}

// ═══════════════════════════════════════════════════════════
// HEALTH CHAT
// ═══════════════════════════════════════════════════════════

function sendSuggestion(text) {
  document.getElementById("chat-input").value = text;
  sendChat();
}

async function loadChatHistory() {
  const data = await fetchAPI("/chat/history");
  if (!data.success || !data.history.length) return;

  const container = document.getElementById("chat-messages");
  // Clear welcome message
  container.innerHTML = "";

  data.history.forEach(msg => appendChatMessage(msg.role, msg.message));
  container.scrollTop = container.scrollHeight;
}

function appendChatMessage(role, message) {
  const container = document.getElementById("chat-messages");

  // Remove welcome screen if present
  const welcome = container.querySelector(".chat-welcome");
  if (welcome) welcome.remove();

  const div = document.createElement("div");
  div.className = `chat-msg ${role}`;
  div.innerHTML = `
    <div class="chat-msg-avatar">${role === "user" ? "U" : "⚕"}</div>
    <div class="chat-msg-bubble">${escapeHtml(message)}</div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function showTypingIndicator() {
  const container = document.getElementById("chat-messages");
  const typing = document.createElement("div");
  typing.id = "typing-indicator";
  typing.className = "chat-msg assistant";
  typing.innerHTML = `
    <div class="chat-msg-avatar">⚕</div>
    <div class="chat-msg-bubble chat-typing">
      <span></span><span></span><span></span>
    </div>
  `;
  container.appendChild(typing);
  container.scrollTop = container.scrollHeight;
}

function removeTypingIndicator() {
  document.getElementById("typing-indicator")?.remove();
}

async function sendChat() {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return;

  input.value = "";
  appendChatMessage("user", message);
  showTypingIndicator();

  const data = await fetchAPI("/chat", "POST", { message });
  removeTypingIndicator();

  if (data.success) {
    appendChatMessage("assistant", data.response);
  } else {
    appendChatMessage("assistant", `Error: ${data.error || "Something went wrong."}`);
  }
}

async function clearChat() {
  if (!confirm("Clear all chat history?")) return;
  await fetchAPI("/chat/clear", "POST");
  const container = document.getElementById("chat-messages");
  container.innerHTML = `
    <div class="chat-welcome">
      <div class="chat-welcome-icon">◉</div>
      <h3>Hello! I'm your AI health assistant.</h3>
      <p>Ask me about medications, side effects, drug interactions, or dietary advice.</p>
      <div class="chat-suggestions">
        <button class="chat-suggestion" onclick="sendSuggestion('What are the side effects of Metformin?')">Side effects of Metformin?</button>
        <button class="chat-suggestion" onclick="sendSuggestion('Can I take Ibuprofen and Aspirin together?')">Ibuprofen + Aspirin safe?</button>
        <button class="chat-suggestion" onclick="sendSuggestion('What foods should I avoid with diabetes?')">Foods to avoid for diabetes</button>
      </div>
    </div>`;
  showToast("Chat history cleared.", "success");
}

// ═══════════════════════════════════════════════════════════
// HISTORY
// ═══════════════════════════════════════════════════════════

async function loadHistory() {
  const data = await fetchAPI("/history");
  const el = document.getElementById("history-list");

  if (!data.success || !data.history.length) {
    el.innerHTML = `<p class="empty-state">No analyses yet. Use the AI tools to generate insights.</p>`;
    return;
  }

  el.innerHTML = data.history.map(h => `
    <div class="history-item">
      <div class="history-item-header">
        <span class="badge ${getBadgeClass(h.analysis_type)}">${analysisTypeLabel(h.analysis_type)}</span>
        <span class="history-item-date">${formatDate(h.created_at)}</span>
      </div>
      <div class="history-item-input">Input: ${escapeHtml((h.input_data || "").substring(0, 100))}</div>
    </div>
  `).join("");
}

// ═══════════════════════════════════════════════════════════
// PDF REPORTS
// ═══════════════════════════════════════════════════════════

async function generatePDF() {
  const btn = document.getElementById("pdf-btn-text");
  if (btn) btn.textContent = "Generating...";
  showLoading("Building your health report...");

  const data = await fetchAPI("/reports/generate", "POST", {});
  hideLoading();
  if (btn) btn.textContent = "⊞ Generate PDF Report";

  if (data.success) {
    showMsg("pdf-msg", `✓ Report generated: ${data.filename}`, "success");
    showToast("PDF report ready for download!", "success");
    loadReports();
    loadDashboard();
  } else {
    const errMsg = data.error || "PDF generation failed.";
    if (btn) showMsg("pdf-msg", errMsg, "error");
    showToast(errMsg, "error");
  }
}

async function loadReports() {
  const data = await fetchAPI("/reports");
  const el = document.getElementById("reports-list");

  if (!data.success || !data.reports.length) {
    el.innerHTML = `<p class="empty-state">No reports generated yet.</p>`;
    return;
  }

  el.innerHTML = data.reports.map(r => `
    <div class="report-item">
      <div class="report-icon">📄</div>
      <div>
        <div class="report-name">${escapeHtml(r.filename)}</div>
        <div class="report-date">${formatDate(r.created_at)}</div>
      </div>
      <a href="${API}/reports/download/${encodeURIComponent(r.filename)}" class="btn btn-sm btn-outline" download>
        ⬇ Download
      </a>
    </div>
  `).join("");
}

// ═══════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════

// Allow pressing Enter to submit login/register
document.addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    const loginPanel = document.getElementById("login-form");
    const registerPanel = document.getElementById("register-form");
    if (loginPanel.classList.contains("active")) handleLogin();
    else if (registerPanel.classList.contains("active")) handleRegister();
  }
});

// Check auth on load
window.addEventListener("DOMContentLoaded", checkAuthStatus);