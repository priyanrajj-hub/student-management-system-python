<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Student Management System — README</title>
<link rel="stylesheet" href="https://unpkg.com/@tabler/icons-webfont@latest/tabler-icons.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=JetBrains+Mono:wght@400;600&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  :root{
    --ink:#0f0f0f;--paper:#fafaf7;--muted:#6b6b6b;
    --accent:#1a6b3c;--accent2:#e8a020;--accent3:#c0392b;
    --surface:#f2f0eb;--border:#d8d5ce;
    --code-bg:#1e1e1e;--code-text:#d4d4d4;
  }
  body{font-family:'DM Sans',sans-serif;background:var(--paper);color:var(--ink);overflow-x:hidden;}
  .wrap{max-width:860px;margin:0 auto;padding:0 0 80px;}

  .hero{background:var(--ink);color:var(--paper);padding:56px 48px 44px;position:relative;overflow:hidden;}
  .hero::before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(-45deg,transparent,transparent 20px,rgba(255,255,255,0.018) 20px,rgba(255,255,255,0.018) 21px);}
  .hero-badge{display:inline-block;border:1px solid rgba(255,255,255,0.25);font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:2px;padding:5px 14px;border-radius:2px;color:rgba(255,255,255,0.6);margin-bottom:24px;text-transform:uppercase;}
  .hero h1{font-family:'Syne',sans-serif;font-size:clamp(32px,6vw,52px);font-weight:800;line-height:1.05;margin-bottom:16px;letter-spacing:-1.5px;}
  .hero h1 span{color:var(--accent2);}
  .hero-sub{font-size:16px;color:rgba(255,255,255,0.55);line-height:1.7;max-width:520px;font-weight:300;margin-bottom:32px;}
  .hero-meta{display:flex;gap:24px;flex-wrap:wrap;}
  .meta-chip{display:flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;font-size:12px;color:rgba(255,255,255,0.5);}
  .meta-chip span{color:var(--accent2);font-weight:600;font-size:13px;}
  .hero-deco{position:absolute;right:-30px;top:-20px;font-family:'Syne',sans-serif;font-size:180px;font-weight:800;color:rgba(255,255,255,0.03);line-height:1;user-select:none;pointer-events:none;letter-spacing:-8px;}

  .stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-bottom:1px solid var(--border);}
  .stat{padding:28px 24px;border-right:1px solid var(--border);}
  .stat:last-child{border-right:none;}
  .stat-num{font-family:'Syne',sans-serif;font-size:36px;font-weight:800;line-height:1;color:var(--ink);margin-bottom:4px;}
  .stat-num.green{color:var(--accent);}
  .stat-num.amber{color:var(--accent2);}
  .stat-num.red{color:var(--accent3);}
  .stat-label{font-size:12px;color:var(--muted);letter-spacing:0.5px;}

  .section{padding:40px 48px;border-bottom:1px solid var(--border);}
  .section-title{font-family:'Syne',sans-serif;font-size:13px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--muted);margin-bottom:28px;display:flex;align-items:center;gap:10px;}
  .section-title::after{content:'';flex:1;height:1px;background:var(--border);}

  .feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;}
  .feat{border:1px solid var(--border);padding:20px;border-radius:4px;background:var(--surface);transition:border-color 0.2s,transform 0.2s;}
  .feat:hover{border-color:var(--ink);transform:translateY(-2px);}
  .feat-icon{width:36px;height:36px;border-radius:6px;display:flex;align-items:center;justify-content:center;margin-bottom:12px;font-size:16px;}
  .feat-icon.g{background:#d4eddf;color:var(--accent);}
  .feat-icon.a{background:#fdebd0;color:var(--accent2);}
  .feat-icon.r{background:#fadbd8;color:var(--accent3);}
  .feat-icon.b{background:#d6eaf8;color:#1a5276;}
  .feat h3{font-family:'Syne',sans-serif;font-size:14px;font-weight:700;margin-bottom:6px;}
  .feat p{font-size:12px;color:var(--muted);line-height:1.6;}

  .grade-bars{display:flex;gap:8px;align-items:flex-end;height:100px;margin-bottom:10px;}
  .bar-wrap{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;}
  .bar{width:100%;border-radius:3px 3px 0 0;transition:height 1s cubic-bezier(0.23,1,0.32,1);}
  .bar-val{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;color:var(--muted);}
  .bar-lbl{font-size:11px;font-weight:700;color:var(--ink);}

  .tech-row{display:flex;flex-wrap:wrap;gap:8px;}
  .tech{border:1px solid var(--border);padding:10px 16px;font-family:'JetBrains Mono',monospace;font-size:12px;border-radius:3px;background:var(--paper);display:flex;align-items:center;gap:8px;color:var(--ink);}
  .tech-dot{width:8px;height:8px;border-radius:50%;}

  .tree{background:var(--code-bg);color:var(--code-text);font-family:'JetBrains Mono',monospace;font-size:13px;padding:24px 28px;border-radius:6px;line-height:2;}
  .tree-file{color:#9cdcfe;} .tree-json{color:#ce9178;} .tree-txt{color:#dcdcaa;} .tree-dir{color:#4ec9b0;font-weight:600;} .tree-md{color:#c586c0;} .tree-dim{color:#555;}

  .flow{display:flex;align-items:center;gap:0;flex-wrap:wrap;margin-top:4px;}
  .flow-step{background:var(--surface);border:1px solid var(--border);padding:10px 16px;font-size:12px;font-weight:500;border-radius:3px;white-space:nowrap;}
  .flow-arrow{padding:0 8px;color:var(--muted);font-size:14px;}

  .road-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
  .road{border-left:3px solid var(--border);padding:14px 18px;border-radius:0 4px 4px 0;background:var(--surface);}
  .road.done{border-left-color:var(--accent);}
  .road.soon{border-left-color:var(--accent2);}
  .road.later{border-left-color:var(--accent3);}
  .road-tag{font-size:10px;letter-spacing:1.5px;font-weight:700;text-transform:uppercase;margin-bottom:4px;}
  .road.done .road-tag{color:var(--accent);}
  .road.soon .road-tag{color:var(--accent2);}
  .road.later .road-tag{color:var(--accent3);}
  .road h4{font-family:'Syne',sans-serif;font-size:14px;font-weight:700;margin-bottom:4px;}
  .road p{font-size:12px;color:var(--muted);}

  .donut-wrap{display:flex;align-items:center;gap:32px;}
  .donut-legend{display:flex;flex-direction:column;gap:10px;}
  .leg-item{display:flex;align-items:center;gap:10px;font-size:13px;}
  .leg-dot{width:12px;height:12px;border-radius:2px;flex-shrink:0;}
  .leg-val{font-family:'JetBrains Mono',monospace;font-weight:600;margin-left:auto;padding-left:16px;}

  .author{display:flex;align-items:center;gap:24px;padding:32px 48px;background:var(--ink);color:var(--paper);}
  .avatar{width:64px;height:64px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:white;flex-shrink:0;}
  .author-name{font-family:'Syne',sans-serif;font-size:20px;font-weight:800;}
  .author-role{font-size:13px;color:rgba(255,255,255,0.45);margin-top:3px;}
  .author-chips{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;}
  .chip{border:1px solid rgba(255,255,255,0.18);font-family:'JetBrains Mono',monospace;font-size:11px;padding:4px 12px;border-radius:2px;color:rgba(255,255,255,0.55);}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <div class="hero-deco">SMS</div>
    <div class="hero-badge">Open Source · Python · v2.0</div>
    <h1>Student<br><span>Management</span><br>System</h1>
    <p class="hero-sub">A complete, production-quality command-line application for managing student records, attendance, grades, and analytics — built entirely in Python with zero external dependencies.</p>
    <div class="hero-meta">
      <div class="meta-chip">Language <span>Python 3</span></div>
      <div class="meta-chip">Libraries <span>Built-in only</span></div>
      <div class="meta-chip">Version <span>2.0</span></div>
      <div class="meta-chip">Lines <span>1,212</span></div>
    </div>
  </div>

  <div class="stats-row">
    <div class="stat"><div class="stat-num green" id="s1">0</div><div class="stat-label">Core Features</div></div>
    <div class="stat"><div class="stat-num amber" id="s2">0</div><div class="stat-label">Lines of Code</div></div>
    <div class="stat"><div class="stat-num" id="s3">0</div><div class="stat-label">Code Sections</div></div>
    <div class="stat"><div class="stat-num red" id="s4">0</div><div class="stat-label">External Libraries</div></div>
  </div>

  <div class="section">
    <div class="section-title">Features</div>
    <div class="feat-grid">
      <div class="feat"><div class="feat-icon g"><i class="ti ti-user-plus"></i></div><h3>Student Records</h3><p>Full profile — name, age, gender, department, guardian, contact, and enrollment date.</p></div>
      <div class="feat"><div class="feat-icon a"><i class="ti ti-search"></i></div><h3>Smart Search</h3><p>Find students by roll, name (partial), department, grade, or email in real time.</p></div>
      <div class="feat"><div class="feat-icon b"><i class="ti ti-chart-bar"></i></div><h3>GPA Calculator</h3><p>Automatic grade and GPA computation from 5-subject marks with visual bar charts.</p></div>
      <div class="feat"><div class="feat-icon g"><i class="ti ti-calendar"></i></div><h3>Attendance</h3><p>Daily P/A/L marking per student with percentage reports and low-attendance alerts.</p></div>
      <div class="feat"><div class="feat-icon a"><i class="ti ti-trophy"></i></div><h3>Rank & Sort</h3><p>Sort and rank students by marks, GPA, name, department, or age. Merit list ready.</p></div>
      <div class="feat"><div class="feat-icon r"><i class="ti ti-file-export"></i></div><h3>Export & Backup</h3><p>Export to CSV (Excel-ready), text reports, JSON backup, and one-click restore.</p></div>
      <div class="feat"><div class="feat-icon b"><i class="ti ti-edit"></i></div><h3>Update Records</h3><p>Edit any single field without touching the rest. Marks auto-recalculate on update.</p></div>
      <div class="feat"><div class="feat-icon g"><i class="ti ti-activity"></i></div><h3>Activity Log</h3><p>Every add, edit, delete, and export is timestamped and written to a log file.</p></div>
      <div class="feat"><div class="feat-icon a"><i class="ti ti-report-analytics"></i></div><h3>Class Statistics</h3><p>Top 3 students, grade distribution chart, class average, and failed-student alerts.</p></div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Sample Grade Distribution</div>
    <div class="grade-bars" id="bars"></div>
    <div style="display:flex;gap:8px;margin-top:2px;" id="bar-labels"></div>
    <p style="font-size:12px;color:var(--muted);margin-top:16px;">Auto-generated from class average marks across 5 subjects: Mathematics, Science, English, History, Computer Science.</p>
  </div>

  <div class="section">
    <div class="section-title">Attendance Tracking</div>
    <div class="donut-wrap">
      <svg width="130" height="130" viewBox="0 0 130 130">
        <circle cx="65" cy="65" r="50" fill="none" stroke="#f0ede8" stroke-width="22"/>
        <circle cx="65" cy="65" r="50" fill="none" stroke="#1a6b3c" stroke-width="22" stroke-dasharray="220 314" stroke-dashoffset="78"/>
        <circle cx="65" cy="65" r="50" fill="none" stroke="#e8a020" stroke-width="22" stroke-dasharray="47 314" stroke-dashoffset="-142"/>
        <circle cx="65" cy="65" r="50" fill="none" stroke="#c0392b" stroke-width="22" stroke-dasharray="30 314" stroke-dashoffset="-189"/>
        <text x="65" y="60" text-anchor="middle" font-family="Syne,sans-serif" font-size="20" font-weight="800" fill="#0f0f0f">75%</text>
        <text x="65" y="76" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="10" fill="#6b6b6b">present</text>
      </svg>
      <div class="donut-legend">
        <div class="leg-item"><div class="leg-dot" style="background:#1a6b3c"></div><span>Present (P)</span><span class="leg-val" style="color:#1a6b3c">75%</span></div>
        <div class="leg-item"><div class="leg-dot" style="background:#e8a020"></div><span>Leave (L)</span><span class="leg-val" style="color:#e8a020">15%</span></div>
        <div class="leg-item"><div class="leg-dot" style="background:#c0392b"></div><span>Absent (A)</span><span class="leg-val" style="color:#c0392b">10%</span></div>
        <div style="border-top:1px solid var(--border);padding-top:10px;margin-top:4px;"><p style="font-size:12px;color:var(--muted);">Students below 75% attendance receive an automatic warning flag.</p></div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">How to Run</div>
    <div class="flow">
      <div class="flow-step">1. Clone the repo</div><div class="flow-arrow">→</div>
      <div class="flow-step">2. Navigate to folder</div><div class="flow-arrow">→</div>
      <div class="flow-step">3. Run main.py</div><div class="flow-arrow">→</div>
      <div class="flow-step">4. Use the menu</div>
    </div>
    <div class="tree" style="margin-top:20px">
      <div style="color:#555;margin-bottom:8px"># Clone &amp; run</div>
      <div><span style="color:#9cdcfe">git</span> clone https://github.com/<span style="color:#ce9178">priyanrajj</span>/student-management-system-python</div>
      <div><span style="color:#9cdcfe">cd</span> student-management-system-python</div>
      <div><span style="color:#9cdcfe">python</span> main.py</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Project Structure</div>
    <div class="tree">
      <div><span class="tree-dir">student-management-system-python/</span></div>
      <div class="tree-dim">│</div>
      <div><span class="tree-dim">├── </span><span class="tree-file">main.py</span><span class="tree-dim">              # Entry point — all features</span></div>
      <div><span class="tree-dim">├── </span><span class="tree-json">students_data.json</span><span class="tree-dim">   # Auto-created student database</span></div>
      <div><span class="tree-dim">├── </span><span class="tree-json">students_backup.json</span><span class="tree-dim"> # Backup snapshot</span></div>
      <div><span class="tree-dim">├── </span><span class="tree-txt">activity_log.txt</span><span class="tree-dim">     # Timestamped action log</span></div>
      <div><span class="tree-dim">├── </span><span class="tree-txt">students_export.csv</span><span class="tree-dim">  # CSV export (auto-generated)</span></div>
      <div><span class="tree-dim">└── </span><span class="tree-md">README.md</span><span class="tree-dim">            # You are here</span></div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Technologies Used</div>
    <div class="tech-row">
      <div class="tech"><div class="tech-dot" style="background:#3572A5"></div>Python 3</div>
      <div class="tech"><div class="tech-dot" style="background:#e8a020"></div>JSON</div>
      <div class="tech"><div class="tech-dot" style="background:#1a6b3c"></div>CSV</div>
      <div class="tech"><div class="tech-dot" style="background:#c0392b"></div>Regex (re)</div>
      <div class="tech"><div class="tech-dot" style="background:#1a5276"></div>datetime</div>
      <div class="tech"><div class="tech-dot" style="background:#6b6b6b"></div>os / File I/O</div>
    </div>
    <p style="font-size:12px;color:var(--muted);margin-top:16px;">No pip install required. 100% Python built-in standard library.</p>
  </div>

  <div class="section">
    <div class="section-title">Code Architecture</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
      <div style="border:1px solid var(--border);border-radius:4px;padding:14px 16px;background:var(--surface);"><div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--accent);margin-bottom:4px;font-weight:600;">SECTION 1–2</div><div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;margin-bottom:2px;">Imports & Utilities</div><div style="font-size:12px;color:var(--muted);">Constants, screen helpers, log writer</div></div>
      <div style="border:1px solid var(--border);border-radius:4px;padding:14px 16px;background:var(--surface);"><div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--accent2);margin-bottom:4px;font-weight:600;">SECTION 3</div><div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;margin-bottom:2px;">File Persistence</div><div style="font-size:12px;color:var(--muted);">Load / Save / Backup / Restore JSON</div></div>
      <div style="border:1px solid var(--border);border-radius:4px;padding:14px 16px;background:var(--surface);"><div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--accent3);margin-bottom:4px;font-weight:600;">SECTION 4–5</div><div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;margin-bottom:2px;">Validation & Builder</div><div style="font-size:12px;color:var(--muted);">Email, phone, age checks + record builder</div></div>
      <div style="border:1px solid var(--border);border-radius:4px;padding:14px 16px;background:var(--surface);"><div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#1a5276;margin-bottom:4px;font-weight:600;">SECTION 6–9</div><div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;margin-bottom:2px;">Features & Menus</div><div style="font-size:12px;color:var(--muted);">Display, all 10 features, navigation</div></div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Roadmap</div>
    <div class="road-grid">
      <div class="road done"><div class="road-tag">Completed</div><h4>CLI Application</h4><p>Full-featured terminal program with all 10 features and JSON persistence.</p></div>
      <div class="road done"><div class="road-tag">Completed</div><h4>Attendance System</h4><p>Daily P/A/L marking with percentage report and low-attendance flag.</p></div>
      <div class="road soon"><div class="road-tag">Coming Soon</div><h4>Tkinter GUI</h4><p>Desktop graphical interface with forms, tables, and charts.</p></div>
      <div class="road soon"><div class="road-tag">Coming Soon</div><h4>SQLite Database</h4><p>Replace JSON with a relational database for better querying.</p></div>
      <div class="road later"><div class="road-tag">Planned</div><h4>Flask Web App</h4><p>Browser-based interface with login, dashboard, and REST API.</p></div>
      <div class="road later"><div class="road-tag">Planned</div><h4>Authentication</h4><p>Role-based access: Admin, Teacher, and Student views.</p></div>
    </div>
  </div>

  <div class="author">
    <div class="avatar">PJ</div>
    <div>
      <div class="author-name">Priyanraj J</div>
      <div class="author-role">First-year CS Student · Open Source Contributor</div>
      <div class="author-chips">
        <div class="chip">Python</div>
        <div class="chip">AI &amp; Data Science</div>
        <div class="chip">Open Source</div>
        <div class="chip">GSSoC 2026</div>
      </div>
    </div>
  </div>
</div>

<script>
  function animCount(el,target,duration){let s=null;function step(ts){if(!s)s=ts;let p=Math.min((ts-s)/duration,1);el.textContent=Math.round(p*target);if(p<1)requestAnimationFrame(step);}requestAnimationFrame(step);}
  animCount(document.getElementById('s1'),10,1000);
  animCount(document.getElementById('s2'),1212,1400);
  animCount(document.getElementById('s3'),9,900);
  animCount(document.getElementById('s4'),0,600);
  const gradeData=[{label:'A+',val:22,color:'#1a6b3c'},{label:'A',val:35,color:'#2e8b57'},{label:'B+',val:60,color:'#3aaa6e'},{label:'B',val:78,color:'#e8a020'},{label:'C+',val:55,color:'#d4890a'},{label:'C',val:30,color:'#c0392b'},{label:'D',val:15,color:'#922b21'},{label:'F',val:5,color:'#6b1a1a'}];
  const maxVal=Math.max(...gradeData.map(d=>d.val));
  const barsEl=document.getElementById('bars');const lblsEl=document.getElementById('bar-labels');
  gradeData.forEach((d,i)=>{
    const bw=document.createElement('div');bw.className='bar-wrap';
    const vEl=document.createElement('div');vEl.className='bar-val';vEl.textContent=d.val;
    const bar=document.createElement('div');bar.className='bar';bar.style.background=d.color;bar.style.height='4px';
    bw.appendChild(vEl);bw.appendChild(bar);barsEl.appendChild(bw);
    setTimeout(()=>{bar.style.height=Math.round((d.val/maxVal)*88)+'px';},200+i*60);
    const lbl=document.createElement('div');lbl.className='bar-lbl';lbl.style.flex='1';lbl.style.textAlign='center';lbl.textContent=d.label;lblsEl.appendChild(lbl);
  });
</script>
</body>
</html>
