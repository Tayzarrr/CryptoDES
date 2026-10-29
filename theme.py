# -*- coding: utf-8 -*-
"""Modul theme untuk ZarCryptoDES."""



# BAGIAN 2: IDENTITAS VISUAL DAN KOMPONEN ANTARMUKA.
# BARIS ASLI 2431: Warna utama biru tua untuk identitas visual.
NAVY='#073983'


# BARIS ASLI 2432: Warna tinta/biru untuk teks dan garis pada GUI.
INK='#1A4381'


# BARIS ASLI 2433: Warna biru pudar untuk teks pendukung.
MUTED='#6180A3'


# BARIS ASLI 2434: Warna hijau untuk informasi status berhasil.
GREEN='#07986C'


# PENJELASAN: STYLE berisi aturan QSS antarmuka (baris 2436-2481), bukan instruksi Python.
STYLE='''
QMainWindow, QWidget#root { background: #F2F0E6; }
QWidget { color: #234F87; font-family: "Segoe UI", "DejaVu Sans", sans-serif; font-size: 12px; }
QFrame#sidebar { background:#F7F5ED; border-right:1px solid #E2E4E0; }
QFrame#card { background:#FCFBF7; border:1px solid #DCE5ED; border-radius:11px; }
QFrame#workspace { background:#FCFBF7; border:1px solid #E0E5E7; border-radius:13px; }
QScrollArea { border:0; background:transparent; }
QScrollArea > QWidget > QWidget { background:transparent; }
QLabel { background:transparent; border:0; }
QLabel#title { color:#043685; font-size:24px; font-weight:700; }
QLabel#section { color:#073C91; font-size:13px; font-weight:650; }
QLabel#muted { color:#6583A8; font-size:11px; }
QLabel#brand { color:#052B70; font-weight:750; font-size:17px; }
QLabel#fieldLabel { color:#466E9F; font-size:11px; }
QPushButton { background:#F0F3FF; border:1px solid #C9D3FA; border-radius:7px;
             padding:9px 12px; color:#455DDC; font-weight:600; }
QPushButton:hover { background:#E5EAFE; border-color:#A7B7F8; }
QPushButton:pressed { background:#D5DFFF; }
QPushButton:disabled { color:#A4AEC0; background:#F0F1F4; border-color:#E0E3EA; }
QPushButton#primary { color:white; border:1px solid #727DF2;
 background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #878DFD,stop:1 #6573EA); }
QPushButton#primary:hover { background:#6270E7; }
QPushButton#green { color:#00895C; background:#E1F8E9; border-color:#B9EDD1; }
QPushButton#green:hover { background:#CDF2DD; }
QPushButton#nav { text-align:left; padding:11px 12px; color:#567DA8; background:transparent; border:0; border-radius:8px; font-weight:450; }
QPushButton#nav:hover { background:#EDF0F6; }
QPushButton#nav:checked { color:#334CED; background:#E3E9FF; font-weight:650; }
QPushButton#round { padding:7px 0px; min-width:32px; border-radius:6px; }
QPushButton#round:checked { color:white; background:#7681F4; }
QLineEdit, QComboBox { background:#F4F7FB; border:1px solid #D6E2ED; border-radius:6px; padding:9px; color:#315E99; }
QLineEdit:focus, QComboBox:focus { border:1px solid #8A9EF5; }
QComboBox::drop-down { border:0; width:24px; }
QPlainTextEdit { font-family: "Consolas", "DejaVu Sans Mono", monospace; font-size:11px; background:#F6F8FA; border:1px solid #D7E3EF; border-radius:7px; color:#2F5E94; padding:9px; selection-background-color:#DDE6FF; }
QCheckBox { color:#5676A1; spacing:7px; }
QCheckBox::indicator { width:15px; height:15px; }
QTableWidget { background:#FCFCFA; alternate-background-color:#F5F7FA; border:1px solid #D7E2EF;
              border-radius:7px; gridline-color:#DFE7EF; color:#254F8A; selection-background-color:#E5EBFF; }
QHeaderView::section { background:#EEF2F8; color:#144487; padding:10px 8px;
                      border:0; border-right:1px solid #E0E7F0; font-size:11px; font-weight:650; }
QProgressBar { border:0; background:#EBEEF5; border-radius:3px; height:5px; }
QProgressBar::chunk { background:#7B87F2; border-radius:3px; }
QScrollBar:vertical { width:8px; background:transparent; margin:0; }
QScrollBar::handle:vertical { background:#CFD6E2; border-radius:4px; min-height:25px; }
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical { height:0; }
QDialog { background:#FCFBF7; }
'''
