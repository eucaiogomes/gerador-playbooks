"""
Ferramenta para criar playbooks HTML interativos com identidade visual Lector
- Logo oficial SVG embutida
- Exportação Word (.doc) e PDF via impressão
- Impressão com estilo de playbook profissional (sem cara de app)
- Dashboard, checklists interativos, seções colapsáveis
"""

import base64
import re
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


# ─────────────────────────────────────────────────────────────────────────────
# CSS – App + Impressão
# ─────────────────────────────────────────────────────────────────────────────
_CSS = """
:root {
  --navy:        #00347E;
  --navy-dark:   #001C66;
  --navy-mid:    #1E3A5F;
  --navy-light:  #2A4F80;
  --navy-subtle: #EBF0F8;
  --orange:      #EF6315;
  --orange2:     #FF930F;
  --orange-sub:  #FFF3E8;
  --blue:        #2563EB;
  --blue-light:  #EBF4FF;
  --white:       #FFFFFF;
  --gray-50:     #F7FAFC;
  --gray-100:    #EDF2F7;
  --gray-200:    #E2E8F0;
  --gray-300:    #CBD5E0;
  --gray-600:    #718096;
  --gray-700:    #4A5568;
  --gray-800:    #2D3748;
  --success:     #38A169;
  --success-lt:  #F0FFF4;
  --warn:        #D97706;
  --warn-lt:     #FFFBEB;
  --danger:      #E53E3E;
  --danger-lt:   #FFF5F5;
  --sw: 280px;
  --hh: 64px;
  --r:  8px;
  --r2: 4px;
  --sh: 0 1px 3px rgba(0,0,0,.12),0 1px 2px rgba(0,0,0,.08);
  --shm:0 4px 12px rgba(0,0,0,.12);
  --tr: all .2s ease;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Segoe UI',Calibri,Arial,sans-serif;font-size:15px;line-height:1.65;color:var(--gray-800);background:var(--gray-50);min-height:100vh}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--gray-100)}
::-webkit-scrollbar-thumb{background:var(--gray-300);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--gray-600)}

/* ── HEADER ── */
.app-header{position:fixed;top:0;left:0;right:0;height:var(--hh);background:var(--navy-dark);display:flex;align-items:center;gap:12px;padding:0 20px;z-index:100;box-shadow:0 2px 8px rgba(0,0,0,.35)}
.header-logo{display:flex;align-items:center;flex-shrink:0;text-decoration:none}
.header-logo svg{height:36px;width:auto}
.header-div{width:1px;height:28px;background:rgba(255,255,255,.15);flex-shrink:0}
.header-title{font-size:14px;font-weight:500;color:rgba(255,255,255,.8);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:380px;flex:1;min-width:0}
.header-actions{display:flex;align-items:center;gap:8px;flex-shrink:0}
.header-prog{display:flex;align-items:center;gap:8px;color:rgba(255,255,255,.65);font-size:13px}
.hpbar{width:110px;height:6px;background:rgba(255,255,255,.15);border-radius:3px;overflow:hidden}
.hpfill{height:100%;background:var(--orange);border-radius:3px;transition:width .4s ease;width:0%}
.hbtn{display:flex;align-items:center;gap:5px;padding:7px 12px;border-radius:var(--r2);font-size:13px;font-weight:500;cursor:pointer;transition:var(--tr);border:1px solid transparent;white-space:nowrap;text-decoration:none}
.hbtn-ghost{background:rgba(255,255,255,.08);color:var(--white);border-color:rgba(255,255,255,.18)}
.hbtn-ghost:hover{background:rgba(255,255,255,.18);border-color:rgba(255,255,255,.3)}
.hbtn-orange{background:var(--orange);color:var(--white);border-color:var(--orange)}
.hbtn-orange:hover{background:var(--orange2);border-color:var(--orange2)}
.hbtn-blue{background:var(--blue);color:var(--white);border-color:var(--blue)}
.hbtn-blue:hover{filter:brightness(1.1)}
.mob-toggle{display:none;width:38px;height:38px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:var(--r2);color:var(--white);font-size:17px;cursor:pointer;align-items:center;justify-content:center;transition:var(--tr)}
.mob-toggle:hover{background:rgba(255,255,255,.18)}

/* ── LAYOUT ── */
.app-layout{display:flex;padding-top:var(--hh);min-height:100vh}

/* ── SIDEBAR ── */
.sidebar{position:fixed;top:var(--hh);left:0;width:var(--sw);height:calc(100vh - var(--hh));background:var(--navy-mid);overflow-y:auto;z-index:50;display:flex;flex-direction:column;transition:transform .3s ease}
.sb-stats{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:16px}
.sbs{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.09);border-radius:var(--r2);padding:10px 12px;text-align:center}
.sbs-val{font-size:22px;font-weight:700;color:var(--orange);display:block;line-height:1}
.sbs-lbl{font-size:10px;color:rgba(255,255,255,.5);display:block;margin-top:3px;text-transform:uppercase;letter-spacing:.5px}
.sb-prog{padding:12px 16px;border-bottom:1px solid rgba(255,255,255,.08)}
.sb-prog-row{display:flex;justify-content:space-between;font-size:12px;color:rgba(255,255,255,.6);margin-bottom:7px}
.sb-prog-bar{height:7px;background:rgba(255,255,255,.1);border-radius:4px;overflow:hidden}
.sb-prog-fill{height:100%;background:linear-gradient(90deg,var(--orange),var(--orange2));border-radius:4px;transition:width .4s ease;width:0%}
.nav-menu{padding:6px 0;flex:1}
.nav-lbl{padding:14px 16px 5px;font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:rgba(255,255,255,.35)}
.nav-item{display:flex;align-items:center;gap:9px;padding:9px 16px;color:rgba(255,255,255,.6);text-decoration:none;font-size:13px;font-weight:400;transition:var(--tr);border-left:3px solid transparent;cursor:pointer}
.nav-item:hover{background:rgba(255,255,255,.07);color:var(--white);border-left-color:rgba(255,255,255,.3)}
.nav-item.active{background:rgba(239,99,21,.12);color:var(--white);font-weight:600;border-left-color:var(--orange)}
.nav-dot{width:5px;height:5px;border-radius:50%;background:rgba(255,255,255,.25);flex-shrink:0}
.nav-item.active .nav-dot{background:var(--orange)}
.sb-foot{padding:14px 16px;border-top:1px solid rgba(255,255,255,.08);font-size:11px;color:rgba(255,255,255,.28)}

/* ── MAIN ── */
.main-content{margin-left:var(--sw);flex:1;min-width:0;padding:28px 32px}

/* ── DASHBOARD ── */
.dashboard{margin-bottom:28px}
.db-title{font-size:24px;font-weight:700;color:var(--navy-mid);margin-bottom:4px}
.db-sub{font-size:13px;color:var(--gray-600);margin-bottom:18px}
.db-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-bottom:0}
.dbc{background:var(--white);border-radius:var(--r);padding:18px;box-shadow:var(--sh);border:1px solid var(--gray-200);display:flex;align-items:flex-start;gap:12px;transition:var(--tr)}
.dbc:hover{box-shadow:var(--shm);transform:translateY(-2px)}
.dbc-icon{width:42px;height:42px;border-radius:var(--r);display:flex;align-items:center;justify-content:center;font-size:19px;flex-shrink:0}
.dbc-icon.or{background:var(--orange-sub)}
.dbc-icon.bl{background:var(--blue-light)}
.dbc-icon.nv{background:var(--navy-subtle)}
.dbc-icon.gr{background:var(--success-lt)}
.dbc-val{font-size:26px;font-weight:700;color:var(--navy-mid);line-height:1}
.dbc-lbl{font-size:12px;color:var(--gray-600);margin-top:3px;font-weight:500}

/* ── SECTIONS ── */
.content-section{background:var(--white);border-radius:var(--r);box-shadow:var(--sh);border:1px solid var(--gray-200);margin-bottom:18px;overflow:hidden}
.sec-hdr{display:flex;align-items:center;justify-content:space-between;padding:16px 22px;background:linear-gradient(135deg,var(--navy-mid) 0%,var(--navy-light) 100%);cursor:pointer;user-select:none;transition:var(--tr);gap:10px}
.sec-hdr:hover{background:linear-gradient(135deg,var(--navy-dark) 0%,var(--navy-mid) 100%)}
.sec-hdr-l{display:flex;align-items:center;gap:11px;flex:1;min-width:0}
.sec-num{width:30px;height:30px;background:var(--orange);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:var(--white);flex-shrink:0}
.sec-title{font-size:15.5px;font-weight:600;color:var(--white);margin:0;line-height:1.3}
.sec-tog{color:rgba(255,255,255,.55);font-size:17px;transition:transform .22s ease;flex-shrink:0}
.sec-tog.col{transform:rotate(-90deg)}
.sec-body{padding:22px;display:block}
.sec-body.col{display:none}

/* ── CONTENT ── */
.tp{color:var(--gray-800);margin-bottom:10px;font-size:14.5px;line-height:1.7}
.tp:last-child{margin-bottom:0}

/* Headings e Subtítulos */
.subhd{font-size:14.5px;font-weight:600;color:var(--navy-mid);margin:18px 0 9px;padding-bottom:5px;border-bottom:2px solid var(--orange);display:inline-block}
h3.subhd,h3.level-3{font-size:16px;font-weight:600;color:var(--navy-mid);margin:20px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--orange);display:block}
h4.level-4{font-size:15px;font-weight:600;color:var(--navy-mid);margin:18px 0 9px;padding-left:8px;border-left:3px solid var(--orange)}
h5.level-5{font-size:14px;font-weight:600;color:var(--navy-light);margin:16px 0 8px}
h6.level-6{font-size:13px;font-weight:600;color:var(--gray-700);margin:14px 0 7px;text-transform:uppercase;letter-spacing:0.5px}

/* Listas do Documento */
.doc-list{margin:12px 0;padding-left:24px}
.doc-list.ordered-list{list-style-type:decimal}
.doc-list.bullet-list{list-style-type:disc}
.doc-list.level-0{margin-left:0}
.doc-list.level-1{margin-left:16px}
.doc-list.level-2{margin-left:32px}
.doc-list.level-3{margin-left:48px}
.doc-list .doc-list-item{margin:6px 0;font-size:14px;line-height:1.6;color:var(--gray-800)}
.doc-list.ordered-list .doc-list-item{list-style-type:decimal}
.doc-list.bullet-list .doc-list-item{list-style-type:disc}

/* Imagens do Documento */
.doc-image{margin:18px 0;text-align:center}
.doc-image .pb-img{max-width:100%;height:auto;border-radius:var(--r);box-shadow:var(--shm);border:1px solid var(--gray-200)}
.doc-image .pb-img:hover{box-shadow:0 6px 20px rgba(0,0,0,.15)}

/* Formatação de texto */
.tp.bold-text{font-weight:600}
.tp.italic-text{font-style:italic}

/* ── INFO BOXES ── */
.ibox{border-radius:var(--r);padding:14px 16px;margin:14px 0;border-left:4px solid}
.ibox-hdr{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:7px}
.ibox-ico{font-size:15px}
.ibox-cnt{font-size:13.5px;line-height:1.6}
.box-tip    {background:#FFF8F0;border-color:var(--orange)}
.box-tip .ibox-hdr{color:var(--orange)}
.box-warning{background:var(--warn-lt);border-color:var(--warn)}
.box-warning .ibox-hdr{color:var(--warn)}
.box-info   {background:var(--blue-light);border-color:var(--blue)}
.box-info .ibox-hdr{color:var(--blue)}
.box-goal   {background:var(--success-lt);border-color:var(--success)}
.box-goal .ibox-hdr{color:var(--success)}

/* ── CHECKLISTS ── */
.cl-wrap{background:var(--gray-50);border:1px solid var(--gray-200);border-radius:var(--r);padding:14px 16px;margin:14px 0}
.cl-hdr{display:flex;align-items:center;gap:7px;margin-bottom:10px;padding-bottom:9px;border-bottom:1px solid var(--gray-200)}
.cl-hdr-ico{font-size:17px;color:var(--navy-mid)}
.cl-hdr-lbl{font-size:12px;font-weight:700;color:var(--navy-mid);text-transform:uppercase;letter-spacing:.5px;flex:1}
.cl-cnt{font-size:12px;font-weight:600;color:var(--gray-600);background:var(--gray-200);border-radius:20px;padding:2px 9px}
.cl-cnt.done{color:var(--white);background:var(--success)}
.cl-pbar{height:4px;background:var(--gray-200);border-radius:2px;margin-bottom:12px;overflow:hidden}
.cl-pfill{height:100%;background:linear-gradient(90deg,var(--success),#48BB78);border-radius:2px;transition:width .3s ease;width:0%}
.cl-list{list-style:none;display:flex;flex-direction:column;gap:5px}
.cl-item{}
.ck-lbl{display:flex;align-items:flex-start;gap:10px;cursor:pointer;padding:7px 9px;border-radius:var(--r2);transition:var(--tr)}
.ck-lbl:hover{background:rgba(0,0,0,.03)}
.ck-lbl input[type=checkbox]{position:absolute;opacity:0;width:0;height:0}
.ck-box{width:19px;height:19px;border:2px solid var(--gray-300);border-radius:4px;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;transition:var(--tr);background:var(--white)}
.ck-lbl input:checked+.ck-box{background:var(--success);border-color:var(--success)}
.ck-lbl input:checked+.ck-box::after{content:'';width:4px;height:8px;border:2px solid var(--white);border-top:none;border-left:none;transform:rotate(45deg) translateY(-1px);display:block}
.ck-txt{font-size:13.5px;color:var(--gray-700);line-height:1.5;flex:1;transition:var(--tr)}
.ck-lbl input:checked~.ck-txt{text-decoration:line-through;color:var(--gray-600)}

/* ── TABLE ── */
.tbl-wrap{overflow-x:auto;margin:14px 0;border-radius:var(--r);border:1px solid var(--gray-200);box-shadow:var(--sh)}
.dtbl{width:100%;border-collapse:collapse;font-size:13.5px}
.dtbl thead{background:var(--navy-mid)}
.dtbl thead th{padding:11px 14px;text-align:left;font-size:11px;font-weight:600;color:var(--white);white-space:nowrap;text-transform:uppercase;letter-spacing:.5px}
.dtbl tbody tr{border-bottom:1px solid var(--gray-100)}
.dtbl tbody tr:last-child{border-bottom:none}
.dtbl tbody tr:hover{background:var(--gray-50)}
.dtbl tbody td{padding:10px 14px;color:var(--gray-700);vertical-align:top}

/* ── IMAGE ── */
.img-wrap{margin:14px 0;text-align:center}
.pb-img{max-width:100%;border-radius:var(--r);box-shadow:var(--shm);border:1px solid var(--gray-200)}

/* ── PRINT HEADER (hidden in app, visible in print) ── */
.print-header{display:none}

/* ─────────────────────────────────────────────
   PRINT / PDF – Estilo Playbook Profissional
───────────────────────────────────────────── */
@media print {
  /* Reset layout */
  .app-header,.sidebar,.mob-toggle{display:none !important}
  .app-layout{padding-top:0}
  .main-content{margin-left:0 !important;padding:0 !important}
  body{background:white !important;font-size:10.5pt;color:#2D3748}

  /* Page */
  @page{size:A4;margin:2cm 2cm 2.2cm 2cm}

  /* Print header with logo */
  .print-header{
    display:flex !important;
    align-items:center;
    justify-content:space-between;
    padding-bottom:8pt;
    margin-bottom:16pt;
    border-bottom:1pt solid #E2E8F0;
  }
  .print-header svg{height:28pt;width:auto}
  .print-header-date{font-size:8.5pt;color:#718096}

  /* Dashboard: keep title, hide cards */
  .dashboard{margin-bottom:16pt}
  .db-grid{display:none !important}
  .db-title{font-size:18pt;font-weight:700;color:#1E3A5F;border-bottom:2.5pt solid #EF6315;padding-bottom:6pt;margin-bottom:3pt}
  .db-sub{font-size:8.5pt;color:#718096;margin-bottom:0}

  /* Sections */
  .content-section{box-shadow:none !important;border:none !important;margin-bottom:14pt;page-break-inside:avoid}
  .sec-body.col{display:block !important}
  .sec-tog{display:none !important}
  .sec-hdr{
    print-color-adjust:exact;-webkit-print-color-adjust:exact;
    background:#1E3A5F !important;
    padding:9pt 13pt !important;
    border-radius:0 !important;
    cursor:default !important;
  }
  .sec-num{
    print-color-adjust:exact;-webkit-print-color-adjust:exact;
    background:#EF6315 !important;
    width:22pt !important;height:22pt !important;
    font-size:10pt !important;
  }
  .sec-title{font-size:12pt !important}

  /* Body content */
  .sec-body{padding:12pt 14pt !important}
  .tp{font-size:10.5pt;line-height:1.6;margin-bottom:7pt}
  .subhd{font-size:11pt;color:#1E3A5F;border-bottom:1.5pt solid #EF6315;padding-bottom:2pt;margin:12pt 0 7pt}

  /* Info boxes */
  .ibox{
    print-color-adjust:exact;-webkit-print-color-adjust:exact;
    margin:9pt 0;padding:9pt 12pt;
  }
  .box-tip    {background:#FFF8F0 !important;border-color:#EF6315 !important}
  .box-warning{background:#FFFBEB !important;border-color:#D97706 !important}
  .box-info   {background:#EBF4FF !important;border-color:#2563EB !important}
  .box-goal   {background:#F0FFF4 !important;border-color:#38A169 !important}
  .ibox-hdr{font-size:9pt !important;margin-bottom:5pt}
  .ibox-cnt{font-size:10pt !important}

  /* Checklists */
  .cl-wrap{background:#FAFAFA !important;border:1pt solid #E2E8F0;padding:9pt 12pt;margin:9pt 0}
  .cl-pbar{display:none !important}
  .ck-box,.ck-lbl input{display:none !important}
  .cl-list{gap:3pt}
  .ck-lbl{padding:3pt 0 !important}
  .ck-lbl::before{content:"□  ";font-size:12pt;color:#1E3A5F;font-family:Arial}
  .ck-txt{font-size:10pt !important;text-decoration:none !important;color:#2D3748 !important}
  .cl-cnt{display:none}
  .cl-hdr{border-bottom:1pt solid #E2E8F0;padding-bottom:6pt;margin-bottom:8pt}
  .cl-hdr-lbl{font-size:9pt}

  /* Tables */
  .tbl-wrap{box-shadow:none !important;border:1pt solid #CBD5E0 !important;margin:9pt 0}
  .dtbl{font-size:9.5pt}
  .dtbl thead{print-color-adjust:exact;-webkit-print-color-adjust:exact;background:#1E3A5F !important}
  .dtbl thead th{color:#FFFFFF !important;padding:7pt 10pt !important;font-size:8.5pt !important}
  .dtbl tbody td{padding:6pt 10pt !important;border:0.5pt solid #E2E8F0 !important}

  /* Headings H3-H6 em print */
  h3.subhd,h3.level-3{font-size:12pt !important;color:#1E3A5F !important;margin:12pt 0 6pt !important;border-bottom:1.5pt solid #EF6315 !important}
  h4.level-4{font-size:11pt !important;color:#1E3A5F !important;margin:10pt 0 5pt !important;border-left:2pt solid #EF6315 !important;padding-left:6pt !important}
  h5.level-5{font-size:10pt !important;color:#1E3A5F !important;margin:8pt 0 4pt !important;font-weight:600}
  h6.level-6{font-size:9pt !important;color:#4A5568 !important;margin:6pt 0 3pt !important;text-transform:uppercase !important;letter-spacing:0.5pt}

  /* Listas em print */
  .doc-list{margin:8pt 0 !important;padding-left:20pt !important}
  .doc-list.level-1{margin-left:12pt !important}
  .doc-list.level-2{margin-left:24pt !important}
  .doc-list.level-3{margin-left:36pt !important}
  .doc-list .doc-list-item{font-size:10pt !important;margin:4pt 0 !important;line-height:1.5}
  .ordered-list .doc-list-item{list-style-type:decimal !important}
  .bullet-list .doc-list-item{list-style-type:disc !important}

  /* Imagens em print */
  .doc-image{margin:12pt 0 !important;page-break-inside:avoid}
  .doc-image .pb-img{max-width:100% !important;height:auto !important;border:0.5pt solid #E2E8F0 !important;box-shadow:none !important;border-radius:4pt !important}

  /* Avoid breaks */
  h2,h3,h4,h5,h6,.cl-wrap,.ibox,.doc-image{page-break-inside:avoid;page-break-after:avoid}
  .content-section{page-break-before:auto}
}

/* ── RESPONSIVE ── */
@media(max-width:768px){
  :root{--sw:260px}
  .sidebar{transform:translateX(-100%)}
  .sidebar.open{transform:translateX(0);box-shadow:0 0 24px rgba(0,0,0,.3)}
  .main-content{margin-left:0 !important;padding:18px 14px}
  .mob-toggle{display:flex}
  .header-title{display:none}
  .db-grid{grid-template-columns:1fr 1fr}
  .header-prog{display:none}
}
"""


# ─────────────────────────────────────────────────────────────────────────────
# JAVASCRIPT
# ─────────────────────────────────────────────────────────────────────────────
_JS = r"""
(function(){
'use strict';
var PID = document.body.dataset.playbookId || 'pb';
var SK  = 'lector_' + PID;

function ls(){ try{ return JSON.parse(localStorage.getItem(SK)||'{}'); }catch(e){ return {}; } }
function ss(s){ try{ localStorage.setItem(SK, JSON.stringify(s)); }catch(e){} }

/* ── Checklists ── */
function initCL(){
  var state = ls();
  document.querySelectorAll('input[type=checkbox]').forEach(function(cb){
    if(state[cb.id]) cb.checked = true;
    cb.addEventListener('change', function(){
      var s = ls(); s[this.id] = this.checked; ss(s);
      updateCLProg(this.closest('.cl-wrap'));
      updateGlobal();
    });
  });
  document.querySelectorAll('.cl-wrap').forEach(function(c){ updateCLProg(c); });
  updateGlobal();
}
function updateCLProg(c){
  if(!c) return;
  var all  = c.querySelectorAll('input[type=checkbox]').length;
  var done = c.querySelectorAll('input[type=checkbox]:checked').length;
  var pct  = all>0 ? Math.round(done/all*100) : 0;
  var fill = c.querySelector('.cl-pfill');
  var cnt  = c.querySelector('.cl-cnt');
  if(fill) fill.style.width = pct+'%';
  if(cnt){ cnt.textContent = done+'/'+all; cnt.classList.toggle('done', done===all&&all>0); }
}
function updateGlobal(){
  var all  = document.querySelectorAll('input[type=checkbox]').length;
  var done = document.querySelectorAll('input[type=checkbox]:checked').length;
  var pct  = all>0 ? Math.round(done/all*100) : 0;
  document.querySelectorAll('.hpfill,.sb-prog-fill').forEach(function(el){ el.style.width=pct+'%'; });
  document.querySelectorAll('.prog-pct').forEach(function(el){ el.textContent=pct+'%'; });
  document.querySelectorAll('.stat-done').forEach(function(el){ el.textContent=done; });
}

/* ── Sections ── */
window.toggleSection = function(id){
  var b = document.getElementById('body-'+id);
  var t = document.querySelector('#sec-'+id+' .sec-tog');
  if(!b) return;
  var col = b.classList.toggle('col');
  if(t) t.classList.toggle('col', col);
  var s = ls(); s['sec_'+id] = col?'c':'o'; ss(s);
};
function initSecs(){
  var state = ls();
  document.querySelectorAll('.content-section').forEach(function(sec){
    var id = sec.id.replace('sec-','');
    if(state['sec_'+id]==='c'){
      var b = document.getElementById('body-'+id);
      var t = sec.querySelector('.sec-tog');
      if(b) b.classList.add('col');
      if(t) t.classList.add('col');
    }
  });
}

/* ── Navigation ── */
function initNav(){
  var secs = document.querySelectorAll('.content-section');
  var navs = document.querySelectorAll('.nav-item');
  var obs  = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){
        var id = e.target.id.replace('sec-','');
        navs.forEach(function(n){ n.classList.toggle('active', n.dataset.sec===id); });
      }
    });
  },{rootMargin:'-15% 0px -60% 0px'});
  secs.forEach(function(s){ obs.observe(s); });
  navs.forEach(function(n){
    n.addEventListener('click', function(e){
      e.preventDefault();
      var t = document.getElementById('sec-'+this.dataset.sec);
      if(!t) return;
      var b = document.getElementById('body-'+this.dataset.sec);
      if(b&&b.classList.contains('col')) toggleSection(this.dataset.sec);
      t.scrollIntoView({behavior:'smooth',block:'start'});
      document.querySelector('.sidebar').classList.remove('open');
    });
  });
}

/* ── Mobile sidebar ── */
function initMobile(){
  var btn = document.querySelector('.mob-toggle');
  var sb  = document.querySelector('.sidebar');
  if(!btn||!sb) return;
  btn.addEventListener('click', function(){ sb.classList.toggle('open'); });
  document.addEventListener('click', function(e){
    if(!sb.contains(e.target)&&!btn.contains(e.target)) sb.classList.remove('open');
  });
}

/* ── PDF via print ── */
window.printPlaybook = function(){
  document.querySelectorAll('.sec-body.col').forEach(function(el){ el.classList.remove('col'); });
  window.print();
};

/* ── Word Export – replica visual idêntico ao PDF ── */
function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function buildWordContent(){
  var html = '';
  document.querySelectorAll('.content-section').forEach(function(sec, idx){
    var tEl    = sec.querySelector('.sec-title');
    var sTitle = tEl ? tEl.textContent.trim() : '';
    var num    = String(idx + 1);

    /* ── Cabeçalho da seção – tabela navy com badge laranja (= print CSS) ── */
    html +=
      '<table width="100%" bgcolor="#1E3A5F" cellpadding="0" cellspacing="0" '+
      'style="background-color:#1E3A5F;border-collapse:collapse;margin-top:14pt;page-break-after:avoid">'+
        '<tr>'+
          '<td bgcolor="#1E3A5F" width="40" valign="middle" '+
          'style="background-color:#1E3A5F;padding:8pt 4pt 8pt 12pt;vertical-align:middle;width:40pt">'+
            '<span style="background-color:#EF6315;color:#ffffff;font-weight:700;font-size:11.5pt;padding:2pt 7pt">'+
              num+
            '</span>'+
          '</td>'+
          '<td bgcolor="#1E3A5F" valign="middle" '+
          'style="background-color:#1E3A5F;color:#ffffff;padding:8pt 14pt 8pt 6pt;'+
          'font-size:13pt;font-weight:700;vertical-align:middle">'+
            esc(sTitle)+
          '</td>'+
        '</tr>'+
      '</table>';

    /* ── Corpo da seção – moldura com borda inferior e laterais ── */
    html += '<div style="border-left:1pt solid #E2E8F0;border-right:1pt solid #E2E8F0;'+
            'border-bottom:1pt solid #E2E8F0;padding:12pt 14pt;margin-bottom:14pt">';

    var body = sec.querySelector('.sec-body');
    if(body){
      [].forEach.call(body.children, function(el){
        var cl = el.className || '';

        /* Parágrafo */
        if(cl.indexOf('tp') > -1){
          var t = el.textContent.trim();
          if(t) html += '<p style="margin:0 0 7pt;font-size:10.5pt;line-height:1.6">'+esc(t)+'</p>';
        }
        /* Subtítulo com sublinhado laranja */
        else if(cl.indexOf('subhd') > -1 || /^H[3-5]$/.test(el.tagName)){
          html +=
            '<h3 style="font-size:11pt;font-weight:700;color:#1E3A5F;'+
            'border-bottom:1.5pt solid #EF6315;padding-bottom:2pt;margin:12pt 0 7pt;display:block">'+
              esc(el.textContent.trim())+
            '</h3>';
        }
        /* Caixas de informação */
        else if(cl.indexOf('ibox') > -1){
          var isTip  = cl.indexOf('box-tip')  > -1;
          var isWarn = cl.indexOf('box-warning') > -1;
          var isGoal = cl.indexOf('box-goal') > -1;
          var bdrClr = isTip?'#EF6315': isWarn?'#D97706': isGoal?'#38A169':'#2563EB';
          var bgClr  = isTip?'#FFF8F0': isWarn?'#FFFBEB': isGoal?'#F0FFF4':'#EBF4FF';
          var bh     = ((el.querySelector('.ibox-hdr')||{}).textContent||'').trim();
          var bc     = ((el.querySelector('.ibox-cnt')||{}).textContent||'').trim();
          html +=
            '<div style="border-left:4pt solid '+bdrClr+';background-color:'+bgClr+';'+
            'padding:8pt 12pt;margin:9pt 0;font-size:10pt">'+
              '<div style="font-weight:700;font-size:9pt;color:'+bdrClr+';text-transform:uppercase;'+
              'letter-spacing:.5pt;margin-bottom:5pt">'+esc(bh)+'</div>'+
              '<div style="font-size:10.5pt;line-height:1.5">'+esc(bc)+'</div>'+
            '</div>';
        }
        /* Checklist – caixa cinza com ☐ inline */
        else if(cl.indexOf('cl-wrap') > -1){
          var items_html = '';
          el.querySelectorAll('.ck-txt').forEach(function(it){
            items_html +=
              '<li style="padding:3pt 0;font-size:10.5pt;list-style:none">'+
                '<span style="color:#1E3A5F;font-family:Arial">&#9744; </span>'+
                esc(it.textContent.trim())+
              '</li>';
          });
          html +=
            '<div style="background-color:#FAFAFA;border:1pt solid #E2E8F0;padding:9pt 12pt;margin:9pt 0">'+
              '<div style="font-weight:700;font-size:9pt;color:#1E3A5F;text-transform:uppercase;'+
              'letter-spacing:.5pt;border-bottom:1pt solid #E2E8F0;padding-bottom:6pt;margin-bottom:8pt">'+
                '&#9745; Checklist'+
              '</div>'+
              '<ul style="list-style:none;margin:0;padding:0">'+items_html+'</ul>'+
            '</div>';
        }
        /* Tabela – header navy com bgcolor para Word */
        else if(cl.indexOf('tbl-wrap') > -1){
          var t = el.querySelector('table');
          if(!t) return;
          var th_html = '';
          t.querySelectorAll('thead tr').forEach(function(tr){
            th_html += '<tr>';
            tr.querySelectorAll('th').forEach(function(th){
              th_html +=
                '<th bgcolor="#1E3A5F" style="background-color:#1E3A5F;color:#ffffff;'+
                'padding:7pt 10pt;text-align:left;font-size:9pt;font-weight:700">'+
                  esc(th.textContent.trim())+
                '</th>';
            });
            th_html += '</tr>';
          });
          var td_html = '';
          t.querySelectorAll('tbody tr').forEach(function(tr, ri){
            var bg = ri%2===1 ? 'background-color:#F7FAFC;' : '';
            td_html += '<tr>';
            tr.querySelectorAll('td').forEach(function(td){
              td_html +=
                '<td style="'+bg+'border:0.75pt solid #E2E8F0;padding:6pt 10pt;'+
                'font-size:9.5pt;vertical-align:top">'+
                  esc(td.textContent.trim())+
                '</td>';
            });
            td_html += '</tr>';
          });
          html +=
            '<table width="100%" cellpadding="0" cellspacing="0" '+
            'style="border-collapse:collapse;width:100%;margin:9pt 0;font-size:9.5pt">'+
              '<thead>'+th_html+'</thead>'+
              '<tbody>'+td_html+'</tbody>'+
            '</table>';
        }
      });
    }
    html += '</div>'; /* fecha moldura da seção */
  });
  return html;
}

window.exportToWord = function(){
  var titleEl = document.querySelector('.db-title');
  var title   = titleEl ? titleEl.textContent.trim() : document.title;
  var date    = new Date().toLocaleDateString('pt-BR');
  var content = buildWordContent();

  /* CSS mínimo – estilos restantes são todos inline acima */
  var css =
    '@page{size:A4;margin:2cm 2cm 2.2cm 2cm}'+
    'body{font-family:Calibri,Arial,sans-serif;font-size:11pt;color:#2D3748;line-height:1.5;margin:0}'+
    'p,ul,h1,h3,table,div{orphans:2;widows:2}'+
    'h1{font-size:20pt;font-weight:700;color:#1E3A5F;margin:0 0 4pt}'+
    '.doc-sub{font-size:8.5pt;color:#718096;margin:0 0 18pt;display:block}'+
    '.doc-foot{margin-top:20pt;font-size:8.5pt;color:#718096;'+
    'border-top:1pt solid #E2E8F0;padding-top:7pt;text-align:center}';

  var doc =
    '<!DOCTYPE html>'+
    '<html xmlns:o="urn:schemas-microsoft-com:office:office" '+
    'xmlns:w="urn:schemas-microsoft-com:office:word" '+
    'xmlns="http://www.w3.org/TR/REC-html40">'+
    '<head><meta charset="utf-8">'+
    '<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View>'+
    '<w:Zoom>90</w:Zoom><w:DoNotOptimizeForBrowser/></w:WordDocument></xml><![endif]-->'+
    '<style>'+css+'</style></head><body>'+

    /* Cabeçalho do documento – igual ao print-header */
    '<table width="100%" cellpadding="0" cellspacing="0" '+
    'style="border-collapse:collapse;border-bottom:1pt solid #E2E8F0;margin-bottom:0">'+
      '<tr>'+
        '<td style="padding-bottom:8pt;vertical-align:bottom">'+
          '<span style="font-size:15pt;font-weight:700;color:#00347E">iT </span>'+
          '<span style="font-size:15pt;font-weight:700;color:#EF6315">Lector</span>'+
        '</td>'+
        '<td style="text-align:right;padding-bottom:8pt;vertical-align:bottom">'+
          '<span style="font-size:8.5pt;color:#718096">Lector Tecnologia &nbsp;&middot;&nbsp; '+esc(date)+'</span>'+
        '</td>'+
      '</tr>'+
    '</table>'+
    /* Linha laranja sob o cabeçalho */
    '<hr style="border:none;border-top:2.5pt solid #EF6315;margin:0 0 14pt">'+
    /* Título do playbook */
    '<h1>'+esc(title)+'</h1>'+
    '<span class="doc-sub">Playbook Lector Tecnologia &nbsp;&middot;&nbsp; '+esc(date)+'</span>'+
    /* Seções */
    content+
    /* Rodapé */
    '<div class="doc-foot">&#169; Lector Tecnologia &nbsp;&middot;&nbsp; Documento gerado automaticamente</div>'+
    '</body></html>';

  var fname = title.replace(/[\/\\?%*:|"<>]/g,'').trim()+'.doc';
  var blob  = new Blob(['\ufeff', doc], {type:'application/msword'});
  var url   = URL.createObjectURL(blob);
  var a     = document.createElement('a');
  a.href = url; a.download = fname;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a);
  setTimeout(function(){ URL.revokeObjectURL(url); }, 150);
};

document.addEventListener('DOMContentLoaded', function(){
  initCL(); initSecs(); initNav(); initMobile();
});
})();
"""


# ─────────────────────────────────────────────────────────────────────────────
# HTMLWriter CLASS
# ─────────────────────────────────────────────────────────────────────────────
class HTMLWriter:
    """Gera playbooks HTML interativos com identidade visual Lector"""

    def __init__(self, output_path: Path, title: str = "Playbook", logo_svg: str = ""):
        self.output_path = Path(output_path)
        self.title       = title
        self.logo_svg    = logo_svg      # SVG content as string
        self._sections: list = []
        self._images_b64: dict = {}

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _slug(self, text: str) -> str:
        t = re.sub(r'[^\w\s-]', '', str(text).lower())
        t = re.sub(r'[\s_-]+', '-', t)
        return t.strip('-')[:50] or "sec"

    def _esc(self, text: str) -> str:
        return (str(text)
                .replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))

    def _detect(self, text: str) -> str:
        s = str(text).strip()
        if re.match(r'^(💡|dica|tip|nota\b)', s, re.I):    return 'tip'
        if re.match(r'^(⚠|atenção|atencao|aviso|importante\b)', s, re.I): return 'warning'
        if re.match(r'^(ℹ|info|informação|obs\.)', s, re.I): return 'info'
        if re.match(r'^(🎯|objetivo|meta\b|o que você vai)', s, re.I): return 'goal'
        if re.match(r'^[□☐✓✔]', s) or re.match(r'^\-\s*\[\s*\]', s): return 'cl_item'
        return 'p'

    # ── Build from doc_content ────────────────────────────────────────────────

    def build_from_doc_content(self, doc_content: Dict[str, Any]) -> None:
        """
        Constrói o playbook HTML a partir do conteúdo do DOCX.
        Preserva: imagens na posição, listas ordenadas/não ordenadas, hierarquia de títulos.
        """
        self.title = doc_content.get("file_name", self.title).replace(".docx", "")

        # Encode images to base64
        for img in doc_content.get("images", []):
            try:
                data = img.image_data if hasattr(img, 'image_data') else img.get('image_data', b'')
                h    = img.hash       if hasattr(img, 'hash')       else img.get('hash', '')
                if data and h:
                    # Detectar extensão da imagem
                    ext = 'png'
                    if hasattr(img, 'filename'):
                        if img.filename.endswith('.jpg') or img.filename.endswith('.jpeg'):
                            ext = 'jpeg'
                        elif img.filename.endswith('.gif'):
                            ext = 'gif'
                        elif img.filename.endswith('.png'):
                            ext = 'png'
                    self._images_b64[h] = f"data:image/{ext};base64," + base64.b64encode(data).decode()
            except Exception:
                pass

        cur: Optional[dict] = None

        def ensure_section(title_fallback="Introdução"):
            nonlocal cur
            if cur is None:
                cur = {'id': self._slug(title_fallback), 'title': title_fallback, 'items': []}
                self._sections.append(cur)

        def render_list_items(items: list, is_ordered: bool) -> str:
            """Renderiza itens de lista com níveis hierárquicos"""
            if not items:
                return ""

            html_parts = []
            current_level = 0
            list_stack = []

            tag = 'ol' if is_ordered else 'ul'

            for item in items:
                level = item.get('level', 0)

                # Abrir listas necessárias
                while current_level < level:
                    html_parts.append(f'<{tag} class="doc-list level-{current_level}">')
                    list_stack.append(tag)
                    current_level += 1

                # Fechar listas necessárias
                while current_level > level:
                    html_parts.append(f'</{list_stack.pop()}>')
                    current_level -= 1

                # Garantir que temos uma lista aberta
                if current_level == 0 and not list_stack:
                    html_parts.append(f'<{tag} class="doc-list">')
                    list_stack.append(tag)
                    current_level = 1

                text = self._esc(item.get('text', ''))
                html_parts.append(f'<li class="doc-list-item">{text}</li>')

            # Fechar todas as listas abertas
            while list_stack:
                html_parts.append(f'</{list_stack.pop()}>')

            return '\n'.join(html_parts)

        for el in doc_content.get("elements", []):
            t = el.type    if hasattr(el, 'type')    else el.get('type', 'paragraph')
            c = el.content if hasattr(el, 'content') else el.get('content', '')
            lv = el.level  if hasattr(el, 'level')  else el.get('level', 1)
            fmt = el.formatting if hasattr(el, 'formatting') else el.get('formatting', {})

            # Heading (H1, H2)
            if t == 'heading':
                level = lv or 2
                if level <= 2:
                    # Novo capítulo/seção
                    cur = {'id': self._slug(str(c)), 'title': str(c), 'items': []}
                    self._sections.append(cur)
                else:
                    # Subtítulo dentro da seção atual
                    ensure_section()
                    cur['items'].append({
                        'type': f'h{min(level, 6)}',
                        'content': str(c),
                        'level': level
                    })

            # Subheading (H3-H6)
            elif t == 'subheading':
                ensure_section()
                cur['items'].append({
                    'type': f'h{min(lv or 3, 6)}',
                    'content': str(c),
                    'level': lv or 3
                })

            # Imagem (posição preservada)
            elif t == 'image':
                ensure_section()
                img_hash = c.get('hash', '') if isinstance(c, dict) else ''
                img_data = c.get('data', b'') if isinstance(c, dict) else b''
                filename = c.get('filename', '') if isinstance(c, dict) else ''

                if img_hash and img_hash in self._images_b64:
                    cur['items'].append({
                        'type': 'image',
                        'src': self._images_b64[img_hash],
                        'alt': filename or 'Imagem do documento',
                        'hash': img_hash
                    })

            # Lista ordenada ou não ordenada
            elif t == 'list':
                ensure_section()
                is_ordered = fmt.get('ordered', False) if isinstance(fmt, dict) else False
                items = c if isinstance(c, list) else []

                if items:
                    cur['items'].append({
                        'type': 'list',
                        'ordered': is_ordered,
                        'items': items
                    })

            # Tabela
            elif t == 'table':
                ensure_section()
                rows = c if isinstance(c, list) else []
                if rows:
                    cur['items'].append({
                        'type': 'tbl',
                        'headers': rows[0] if rows else [],
                        'rows': rows[1:] if len(rows) > 1 else [],
                    })

            # Parágrafo normal
            elif t == 'paragraph':
                ensure_section()
                text = str(c).strip()
                if text:
                    # Detectar tipo especial (dica, aviso, etc.)
                    k = self._detect(text)
                    if k in ('tip', 'warning', 'info', 'goal'):
                        cur['items'].append({
                            'type': 'ibox',
                            'btype': k,
                            'content': text
                        })
                    else:
                        # Preservar formatação do parágrafo
                        p_fmt = {'type': 'p', 'content': text}
                        if isinstance(fmt, dict):
                            if fmt.get('is_bold'):
                                p_fmt['bold'] = True
                            if fmt.get('is_italic'):
                                p_fmt['italic'] = True
                            if fmt.get('alignment'):
                                p_fmt['alignment'] = fmt['alignment']
                        cur['items'].append(p_fmt)

    # ── Stats ────────────────────────────────────────────────────────────────

    def _stats(self) -> dict:
        cl_items = tables = 0
        for s in self._sections:
            for it in s.get('items', []):
                if it['type'] == 'cl':   cl_items += len(it.get('items', []))
                elif it['type'] == 'tbl': tables   += 1
        return {'sections': len(self._sections), 'cl_items': cl_items, 'tables': tables}

    # ── HTML rendering ────────────────────────────────────────────────────────

    def _render_list_html(self, items: list, is_ordered: bool) -> str:
        """Renderiza lista com suporte a níveis hierárquicos"""
        if not items:
            return ""

        html_parts = []
        current_level = 0
        list_stack = []
        tag = 'ol' if is_ordered else 'ul'

        for item in items:
            level = item.get('level', 0)

            # Abrir listas necessárias
            while current_level < level:
                list_classes = f'doc-list level-{current_level}'
                if is_ordered:
                    list_classes += ' ordered-list'
                else:
                    list_classes += ' bullet-list'
                html_parts.append(f'<{tag} class="{list_classes}">')
                list_stack.append(tag)
                current_level += 1

            # Fechar listas necessárias
            while current_level > level:
                if list_stack:
                    html_parts.append(f'</{list_stack.pop()}>')
                    current_level -= 1

            # Garantir que temos uma lista aberta no nível atual
            if current_level == 0:
                list_classes = 'doc-list' + (' ordered-list' if is_ordered else ' bullet-list')
                html_parts.append(f'<{tag} class="{list_classes}">')
                list_stack.append(tag)
                current_level = 1

            text = self._esc(item.get('text', ''))
            html_parts.append(f'<li class="doc-list-item">{text}</li>')

        # Fechar todas as listas abertas
        while list_stack:
            html_parts.append(f'</{list_stack.pop()}>')

        return '\n'.join(html_parts)

    def _render_items(self, items: list, sid: str) -> str:
        html = []
        icons  = {'tip': '💡', 'warning': '⚠️', 'info': 'ℹ️', 'goal': '🎯'}
        labels = {'tip': 'Dica', 'warning': 'Atenção', 'info': 'Informação', 'goal': 'Objetivo'}

        for i, it in enumerate(items):
            tp = it.get('type', 'p')

            # Parágrafo normal
            if tp == 'p':
                text = self._esc(it.get('content', ''))
                if text:
                    # Aplicar formatação se presente
                    extra_classes = []
                    styles = []

                    if it.get('bold'):
                        extra_classes.append('bold-text')
                    if it.get('italic'):
                        extra_classes.append('italic-text')
                    if it.get('alignment'):
                        styles.append(f"text-align: {it['alignment']}")

                    cls = ' ' + ' '.join(extra_classes) if extra_classes else ''
                    style = f' style="{"; ".join(styles)}"' if styles else ''
                    html.append(f'<p class="tp{cls}"{style}>{text}</p>')

            # Headings H3-H6
            elif tp in ('h3', 'h4', 'h5', 'h6'):
                level = int(tp[1])
                cls = f'subhd level-{level}'
                html.append(f'<h{level} class="{cls}">{self._esc(it["content"])}</h{level}>')

            # Subtítulo legado
            elif tp == 'subhd':
                html.append(f'<h3 class="subhd">{self._esc(it["content"])}</h3>')

            # Lista ordenada ou não ordenada
            elif tp == 'list':
                is_ordered = it.get('ordered', False)
                list_items = it.get('items', [])
                if list_items:
                    list_html = self._render_list_html(list_items, is_ordered)
                    html.append(list_html)

            # Imagem
            elif tp == 'image':
                src = it.get('src', '')
                alt = self._esc(it.get('alt', 'Imagem'))
                if src:
                    html.append(
                        f'<div class="img-wrap doc-image">'
                        f'<img src="{src}" alt="{alt}" class="pb-img" loading="lazy">'
                        f'</div>'
                    )

            # Caixas de informação
            elif tp == 'ibox':
                bt = it.get('btype', 'info')
                html.append(
                    f'<div class="ibox box-{bt}">'
                    f'<div class="ibox-hdr"><span class="ibox-ico">{icons[bt]}</span>'
                    f' <strong>{labels[bt]}</strong></div>'
                    f'<div class="ibox-cnt">{self._esc(it["content"])}</div></div>'
                )

            # Checklist interativo
            elif tp == 'cl':
                cid   = f"cl-{sid}-{i}"
                total = len(it.get('items', []))
                rows  = ''.join(
                    f'<li class="cl-item"><label class="ck-lbl">'
                    f'<input type="checkbox" id="{cid}-{j}" onchange="updateGlobal()">'
                    f'<span class="ck-box"></span>'
                    f'<span class="ck-txt">{self._esc(str(v))}</span>'
                    f'</label></li>'
                    for j, v in enumerate(it.get('items', []))
                )
                html.append(
                    f'<div class="cl-wrap" id="{cid}">'
                    f'<div class="cl-hdr">'
                    f'<span class="cl-hdr-ico">☑</span>'
                    f'<span class="cl-hdr-lbl">Checklist</span>'
                    f'<span class="cl-cnt">0/{total}</span></div>'
                    f'<div class="cl-pbar"><div class="cl-pfill"></div></div>'
                    f'<ul class="cl-list">{rows}</ul></div>'
                )

            # Tabela
            elif tp == 'tbl':
                hs  = it.get('headers', [])
                rs  = it.get('rows', [])
                ths = ''.join(f'<th>{self._esc(str(h))}</th>' for h in hs)
                trs = ''.join(
                    '<tr>' + ''.join(f'<td>{self._esc(str(c))}</td>' for c in r) + '</tr>'
                    for r in rs
                )
                html.append(
                    f'<div class="tbl-wrap"><table class="dtbl">'
                    f'<thead><tr>{ths}</tr></thead>'
                    f'<tbody>{trs}</tbody></table></div>'
                )

        return '\n'.join(html)

    def _render_nav(self) -> str:
        return '\n'.join(
            f'<a class="nav-item" data-sec="{s["id"]}" href="#sec-{s["id"]}">'
            f'<span class="nav-dot"></span>{self._esc(s["title"])}</a>'
            for s in self._sections
        )

    def _render_sections(self) -> str:
        parts = []
        for idx, s in enumerate(self._sections, 1):
            body = self._render_items(s.get('items', []), s['id'])
            parts.append(
                f'<section id="sec-{s["id"]}" class="content-section">'
                f'<div class="sec-hdr" onclick="toggleSection(\'{s["id"]}\')">'
                f'<div class="sec-hdr-l">'
                f'<span class="sec-num">{idx}</span>'
                f'<h2 class="sec-title">{self._esc(s["title"])}</h2>'
                f'</div><span class="sec-tog">▾</span></div>'
                f'<div class="sec-body" id="body-{s["id"]}">{body}</div>'
                f'</section>'
            )
        return '\n'.join(parts)

    def _logo_html(self) -> str:
        """Retorna o SVG inline ou fallback textual"""
        if self.logo_svg:
            # Inject height attribute for sizing
            svg = self.logo_svg.strip()
            svg = re.sub(r'<svg ', '<svg style="height:34px;width:auto" ', svg, count=1)
            return svg
        # Text fallback
        return (
            '<span style="font-size:18px;font-weight:800;color:#fff;letter-spacing:-0.5px;">'
            '<span style="color:#EF6315">iT</span> Lector</span>'
        )

    # ── Generate HTML ─────────────────────────────────────────────────────────

    def generate_html(self) -> str:
        st   = self._stats()
        pid  = self._slug(self.title)
        now  = datetime.now().strftime('%d/%m/%Y')
        logo = self._logo_html()

        nav      = self._render_nav()
        sections = self._render_sections()

        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{self._esc(self.title)} | Lector Playbook</title>
  <style>{_CSS}</style>
</head>
<body data-playbook-id="{pid}">

<!-- Print-only header -->
<div class="print-header">
  {logo}
  <span class="print-header-date">Lector Tecnologia · {now}</span>
</div>

<!-- App Header -->
<header class="app-header">
  <a class="header-logo" href="#" title="Lector Playbook">{logo}</a>
  <div class="header-div"></div>
  <span class="header-title">{self._esc(self.title)}</span>
  <div class="header-actions">
    <div class="header-prog">
      <span class="prog-pct">0%</span>
      <div class="hpbar"><div class="hpfill"></div></div>
    </div>
    <button class="hbtn hbtn-ghost" onclick="exportToWord()" title="Baixar como Word">
      📄 Word
    </button>
    <button class="hbtn hbtn-orange" onclick="printPlaybook()" title="Imprimir / Salvar PDF">
      🖨 PDF
    </button>
    <button class="mob-toggle">☰</button>
  </div>
</header>

<!-- Layout -->
<div class="app-layout">

  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="sb-stats">
      <div class="sbs"><span class="sbs-val">{st['sections']}</span><span class="sbs-lbl">Seções</span></div>
      <div class="sbs"><span class="sbs-val">{st['cl_items']}</span><span class="sbs-lbl">Tarefas</span></div>
      <div class="sbs"><span class="sbs-val">{st['tables']}</span><span class="sbs-lbl">Tabelas</span></div>
      <div class="sbs"><span class="sbs-val stat-done">0</span><span class="sbs-lbl">Concluídas</span></div>
    </div>
    <div class="sb-prog">
      <div class="sb-prog-row"><span>Progresso</span><span class="prog-pct">0%</span></div>
      <div class="sb-prog-bar"><div class="sb-prog-fill"></div></div>
    </div>
    <nav class="nav-menu">
      <div class="nav-lbl">Seções</div>
      {nav}
    </nav>
    <div class="sb-foot">Lector Tecnologia · {now}</div>
  </aside>

  <!-- Main -->
  <main class="main-content">
    <div class="dashboard">
      <h1 class="db-title">{self._esc(self.title)}</h1>
      <p class="db-sub">Playbook interativo · {now}</p>
      <div class="db-grid">
        <div class="dbc"><div class="dbc-icon nv">📋</div>
          <div><div class="dbc-val">{st['sections']}</div><div class="dbc-lbl">Seções</div></div></div>
        <div class="dbc"><div class="dbc-icon or">☑</div>
          <div><div class="dbc-val">{st['cl_items']}</div><div class="dbc-lbl">Itens de checklist</div></div></div>
        <div class="dbc"><div class="dbc-icon bl">📊</div>
          <div><div class="dbc-val">{st['tables']}</div><div class="dbc-lbl">Tabelas</div></div></div>
        <div class="dbc"><div class="dbc-icon gr">✅</div>
          <div><div class="dbc-val stat-done">0</div><div class="dbc-lbl">Concluídas</div></div></div>
      </div>
    </div>

    {sections}
  </main>
</div>

<script>{_JS}</script>
</body>
</html>"""

    def _render_full_html(self) -> str:
        """Retorna o HTML completo do playbook (usado pelo gerador v2)"""
        return self.generate_html()

    def save(self) -> Path:
        html = self.generate_html()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return self.output_path
