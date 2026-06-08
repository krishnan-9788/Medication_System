import os

replacements = {
    '⚕': '<span class="material-symbols-outlined">medical_services</span>',
    '🏠': '<span class="material-symbols-outlined">home</span>',
    '👤': '<span class="material-symbols-outlined">person</span>',
    '♡': '<span class="material-symbols-outlined">favorite</span>',
    '💊': '<span class="material-symbols-outlined">medication</span>',
    '📄': '<span class="material-symbols-outlined">description</span>',
    '🔑': '<span class="material-symbols-outlined">health_and_safety</span>',
    '🛡️': '<span class="material-symbols-outlined">shield</span>',
    '⇄': '<span class="material-symbols-outlined">swap_horiz</span>',
    '↔': '<span class="material-symbols-outlined">swap_horiz</span>',
    '🍎': '<span class="material-symbols-outlined">nutrition</span>',
    '💬': '<span class="material-symbols-outlined">chat</span>',
    '🕒': '<span class="material-symbols-outlined">history</span>',
    '📥': '<span class="material-symbols-outlined">upload_file</span>',
    '🚪': '<span class="material-symbols-outlined">logout</span>',
    '🔍': '<span class="material-symbols-outlined">search</span>',
    '🔔': '<span class="material-symbols-outlined">notifications</span>',
    'ⓘ': '<span class="material-symbols-outlined">info</span>',
    '✓': '<span class="material-symbols-outlined">check_circle</span>',
    '📈': '<span class="material-symbols-outlined">trending_up</span>',
    '☁️': '<span class="material-symbols-outlined">cloud_upload</span>',
    '🤖': '<span class="material-symbols-outlined">robot_2</span>',
    '⚡': '<span class="material-symbols-outlined">bolt</span>',
    '◈': '<span class="material-symbols-outlined">medical_information</span>',
    '❋': '<span class="material-symbols-outlined">eco</span>',
    '⊡': '<span class="material-symbols-outlined">document_scanner</span>',
    '⚖️': '<span class="material-symbols-outlined" style="font-size:16px;">scale</span>',
    '📏': '<span class="material-symbols-outlined" style="font-size:16px;">height</span>',
    '🩸': '<span class="material-symbols-outlined" style="font-size:16px;">bloodtype</span>',
    '⏱️': '<span class="material-symbols-outlined" style="font-size:16px;">schedule</span>',
    '✦': '<span class="material-symbols-outlined">medication_liquid</span>',
    '⚠️': '<span class="material-symbols-outlined" style="font-size:18px;vertical-align:bottom;">warning</span>',
    '✗': '<span class="material-symbols-outlined" style="color:var(--red);">cancel</span>',
    '💧': '<span class="material-symbols-outlined">water_drop</span>',
    '🕐': '<span class="material-symbols-outlined">schedule</span>',
    '💪': '<span class="material-symbols-outlined">fitness_center</span>',
    '◉': '<span class="material-symbols-outlined">smart_toy</span>',
    '⊞': '<span class="material-symbols-outlined">picture_as_pdf</span>',
    '⬇': '<span class="material-symbols-outlined" style="font-size:18px">download</span>',
    '⌄': '<span class="material-symbols-outlined" style="font-size:18px">expand_more</span>',
}

files = ['frontend/index.html', 'frontend/script.js']

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for k, v in replacements.items():
        content = content.replace(k, v)
        
    # Also add the Google font link in index.html
    if fp == 'frontend/index.html' and 'Material+Symbols+Outlined' not in content:
        content = content.replace(
            '<link href="https://fonts.googleapis.com/css2?family=DM+Sans',
            '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />\n  <link href="https://fonts.googleapis.com/css2?family=DM+Sans'
        )
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Replaced emojis with icons!")
