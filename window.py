# -*- coding: utf-8 -*-
"""Modul window untuk ZarCryptoDES."""

from pathlib import Path
from datetime import datetime
import secrets
from cipher import decrypt_record, encrypt_bytes, encrypt_message, pad, parse_hex
from ciphertext import message_summary, parse_ciphertext, serialize_ciphertext
from constants import ACUAN_3DES, KUNCI_3DES_CONTOH, KUNCI_CONTOH
from crypto_backend import DES, DES3
from des_manual import DESManual, round_function
from keys import parse_key, random_3des_key
from qt_compat import QApplication, QButtonGroup, QCheckBox, QComboBox, QDialog, QFileDialog, QFont, QFrame, QGridLayout, QHBoxLayout, QHeaderView, QIcon, QLabel, QLineEdit, QMainWindow, QMessageBox, QPlainTextEdit, QProgressBar, QPushButton, QScrollArea, QSize, QSpinBox, QStackedWidget, QVBoxLayout, QWidget, Qt
from theme import GREEN, STYLE
from triple_des import TripleDESManual
from verification import comparison, run_3des_verification, run_verification, verify
from widgets import HeroBanner, RoundDiagram, button, card, dragon_image, field, fill_table, icon, notice, table, text
from worker import Worker

# BARIS ASLI 2610: Mendefinisikan kelas ZarCryptoDES. Jendela utama GUI aplikasi ZarCryptoDES.
class ZarCryptoDES(QMainWindow):
    # BARIS ASLI 2611: Mendefinisikan fungsi __init__. Fungsi ini menangani aksi khusus dalam aplikasi.
    def __init__(self):
        # BARIS ASLI 2612: Di __init__: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        super().__init__();self.setWindowTitle('ZarCryptoDES')
        # BARIS ASLI 2613: Di __init__: Menghitung/menyiapkan nilai screen untuk dipakai oleh proses berikutnya.
        screen=QApplication.primaryScreen().availableGeometry()
        # BARIS ASLI 2614: Di __init__: Mengatur properti komponen GUI yang digunakan.
        self.resize(max(1040,min(1260,screen.width()-40)),max(720,min(820,screen.height()-40)));self.setMinimumSize(1040,720)
        # BARIS ASLI 2615: Di __init__: Menerapkan gaya dan warna pada elemen antarmuka.
        self.logo=dragon_image();self.setWindowIcon(QIcon(self.logo));self.setStyleSheet(STYLE)
        # BARIS ASLI 2616: Di __init__: Menghitung/menyiapkan nilai self.worker untuk dipakai oleh proses berikutnya.
        self.worker=None;self.job_buttons=[];self.process_controls=[];self.history=[];self.last_test='';self.keep_history=True
        # BARIS ASLI 2617: Di __init__: Menghitung/menyiapkan nilai self.format_boxes untuk dipakai oleh proses berikutnya.
        self.format_boxes={};self.original_plain=None;self.file_states={};self.keys=[];self.nav={};self.pages={}
        # BARIS ASLI 2618: Di __init__: Menghitung/menyiapkan nilai self.algorithm untuk dipakai oleh proses berikutnya.
        self.algorithm='DES';self.algorithm_boxes=[];self.key_format='hex';self.key_format_boxes=[]
        # Simpan masukan HEX dan teks secara terpisah untuk masing-masing algoritma.
        self.saved_keys={('DES','hex'):KUNCI_CONTOH,('3DES','hex'):KUNCI_3DES_CONTOH,('DES','text'):'cerdas00',('3DES','text'):'cerdashumanis000'};self.info_labels=[]
        # BARIS ASLI 2619: Di __init__: Menjalankan langkah self.build() sebagai bagian dari alur fungsi ini.
        self.build()
        # BARIS ASLI 2620: Di __init__: Mengatur properti komponen GUI yang digunakan.
        self.set_page('home')

    # BARIS ASLI 2622: Mendefinisikan fungsi build. Fungsi ini menangani aksi khusus dalam aplikasi.
    def build(self):
        # BARIS ASLI 2623: Di build: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        root=QWidget();root.setObjectName('root');self.setCentralWidget(root)
        # BARIS ASLI 2624: Di build: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        shell=QHBoxLayout(root);shell.setContentsMargins(0,0,0,0);shell.setSpacing(0)
        # BARIS ASLI 2625: Di build: Memasang tata letak antarmuka dan komponennya.
        side=QFrame();side.setObjectName('sidebar');side.setFixedWidth(210);shell.addWidget(side)
        # BARIS ASLI 2626: Di build: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        nav=QVBoxLayout(side);nav.setContentsMargins(16,19,16,12);nav.setSpacing(7)
        # BARIS ASLI 2627: Di build: Memasang tata letak antarmuka dan komponennya.
        brand=QHBoxLayout();badge=QLabel();badge.setPixmap(self.logo.scaled(34,44,Qt.KeepAspectRatio,Qt.SmoothTransformation));brand.addWidget(badge)
        # BARIS ASLI 2628: Di build: Memasang tata letak antarmuka dan komponennya.
        brand.addWidget(text('ZarCryptoDES','brand'));nav.addLayout(brand);nav.addSpacing(15)
        # BARIS ASLI 2629: Di build: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        group=QButtonGroup(self);group.setExclusive(True)
        # BARIS ASLI 2630: Di build: Menghitung/menyiapkan nilai titles untuk dipakai oleh proses berikutnya.
        titles=[('home','Beranda','home'),('encrypt','Enkripsi File','encrypt'),('decrypt','Dekripsi File','decrypt'),('test','Uji DES / 3DES','test'),('compare','Perbandingan','compare'),('rounds','Jejak Feistel','rounds'),('history','Riwayat','history')]
        # BARIS ASLI 2631: Di build: Melakukan iterasi pada elemen/urutan: key,title,symbol in titles.
        for key,title,symbol in titles:
            # BARIS ASLI 2632: Di build: Memasang tata letak antarmuka dan komponennya.
            b=button(title,lambda checked=False,k=key:self.set_page(k));b.setObjectName('nav');b.setCheckable(True);b.setIcon(icon(symbol));b.setIconSize(QSize(21,21));group.addButton(b);nav.addWidget(b);self.nav[key]=b
        # BARIS ASLI 2633: Di build: Menjalankan langkah nav.addStretch() sebagai bagian dari alur fungsi ini.
        nav.addStretch()
        # BARIS ASLI 2634: Di build: Memasang tata letak antarmuka dan komponennya.
        water=QLabel();water.setPixmap(dragon_image('#D8D8CB').scaled(153,210,Qt.KeepAspectRatio,Qt.SmoothTransformation));water.setAlignment(Qt.AlignCenter);nav.addWidget(water)
        # BARIS ASLI 2635: Di build: Memasang tata letak antarmuka dan komponennya.
        main=QVBoxLayout();main.setContentsMargins(21,22,21,13);main.setSpacing(10);shell.addLayout(main,1)
        # BARIS ASLI 2636: Di build: Memasukkan widget/layout ke susunan tampilan.
        self.stack=QStackedWidget();main.addWidget(self.stack,1)
        # BARIS ASLI 2637: Di build: Memasukkan widget/layout ke susunan tampilan.
        self.progress=QProgressBar();self.progress.setTextVisible(False);self.progress.setFixedHeight(5);self.progress.setRange(0,1);self.progress.setValue(0);main.addWidget(self.progress)
        # BARIS ASLI 2638: Di build: Memasukkan widget/layout ke susunan tampilan.
        self.status=text('Siap untuk praktikum. Pilih menu di sebelah kiri.','muted');main.addWidget(self.status)
        # BARIS ASLI 2639: Di build: Menjalankan langkah self.home_page();self.file_page('encrypt');self.file_page('decrypt');self.test_page()... sebagai bagian dari alur fungsi ini.
        self.home_page();self.file_page('encrypt');self.file_page('decrypt');self.test_page();self.compare_page();self.rounds_page();self.history_page()

    # BARIS ASLI 2641: Mendefinisikan fungsi page. Fungsi ini menangani aksi khusus dalam aplikasi.
    def page(self,key,title,description,scrollable=True):
        # BARIS ASLI 2642: Di page: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        frame=QFrame();frame.setObjectName('workspace');outer=QVBoxLayout(frame);outer.setContentsMargins(20,20,20,20);outer.setSpacing(6)
        # BARIS ASLI 2643: Di page: Memasang tata letak antarmuka dan komponennya.
        outer.addWidget(text(title,'title'));outer.addWidget(text(description,'muted'));outer.addSpacing(10)
        # BARIS ASLI 2644: Di page: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        body=QWidget();layout=QVBoxLayout(body);layout.setContentsMargins(0,0,0,0);layout.setSpacing(12)
        # BARIS ASLI 2645: Di page: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: scrollable.
        if scrollable:
            # BARIS ASLI 2646: Di page: Memasang tata letak antarmuka dan komponennya.
            scroll=QScrollArea();scroll.setWidgetResizable(True);scroll.setWidget(body);outer.addWidget(scroll,1)
        # BARIS ASLI 2647: Di page: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
        else:outer.addWidget(body,1)
        # BARIS ASLI 2648: Di page: Memasukkan widget/layout ke susunan tampilan.
        self.pages[key]=self.stack.addWidget(frame);return layout

    # BARIS ASLI 2650: Mendefinisikan fungsi set_page. Fungsi ini menangani aksi khusus dalam aplikasi.
    def set_page(self,key):
        # BARIS ASLI 2651: Di set_page: Mengubah pilihan aktif pada kontrol GUI.
        self.stack.setCurrentIndex(self.pages[key]);self.nav[key].setChecked(True)

    # BARIS ASLI 2653: Mendefinisikan fungsi track. Fungsi ini menangani aksi khusus dalam aplikasi.
    def track(self,b):self.job_buttons.append(b);return b

    # BARIS ASLI 2655: Mendefinisikan fungsi home_page. Fungsi ini menangani aksi khusus dalam aplikasi.
    def home_page(self):
        # BARIS ASLI 2656: Di home_page: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        outer=QFrame();outer.setObjectName('workspace');shell=QVBoxLayout(outer);shell.setContentsMargins(18,18,18,18)
        # BARIS ASLI 2657: Di home_page: Memasang tata letak antarmuka dan komponennya.
        scroll=QScrollArea();scroll.setWidgetResizable(True);body=QWidget();lay=QVBoxLayout(body);lay.setContentsMargins(0,0,2,0);lay.setSpacing(18);scroll.setWidget(body);shell.addWidget(scroll)
        # BARIS ASLI 2658: Di home_page: Memasang tata letak antarmuka dan komponennya.
        lay.addWidget(HeroBanner(self.logo),2)
        # BARIS ASLI 2659: Di home_page: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        row=QHBoxLayout();row.setSpacing(12)
        # BARIS ASLI 2660: Di home_page: Menghitung/menyiapkan nilai features untuk dipakai oleh proses berikutnya.
        features=[('encrypt','Enkripsi File','Enkripsi file teks dan simpan ciphertext.','encrypt'),('decrypt','Dekripsi File','Pulihkan ciphertext menjadi teks asli.','decrypt'),('test','Uji DES / 3DES','Bandingkan DES / 3DES manual dengan library.','test'),('compare','Perbandingan','Lihat kesamaan hasil dan dekripsi silang.','compare'),('rounds','Jejak Feistel','Pelajari 16 ronde DES dan fungsi ronde.','rounds')]
        # BARIS ASLI 2661: Di home_page: Melakukan iterasi pada elemen/urutan: key,title,desc,symbol in features.
        for key,title,desc,symbol in features:
            # BARIS ASLI 2662: Di home_page: Memasang tata letak antarmuka dan komponennya.
            w,c=card();badge=QLabel();badge.setPixmap(icon(symbol,'#FFFFFF',26).pixmap(26,26));badge.setFixedSize(40,40);badge.setAlignment(Qt.AlignCenter);badge.setStyleSheet('background:#818CFA; border-radius:12px;');c.addWidget(badge)
            # BARIS ASLI 2663: Di home_page: Memasang tata letak antarmuka dan komponennya.
            c.addWidget(text(title,'section'));c.addWidget(text(desc,'muted'));c.addStretch();c.addWidget(button('Buka',lambda checked=False,k=key:self.set_page(k),symbol='arrow'));row.addWidget(w,1)
        # BARIS ASLI 2664: Di home_page: Memasang tata letak antarmuka dan komponennya.
        lay.addLayout(row,3)
        # BARIS ASLI 2665: Di home_page: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        about,a=card('ZarCryptoDES');a.setContentsMargins(22,20,22,20)
        # BARIS ASLI 2666: Di home_page: Memakai operasi bit AND/OR untuk menyeleksi atau menggabungkan bit.
        heading=text('Enkripsi & Dekripsi Pesan');heading.setStyleSheet('color:#073B86; font-size:23px; font-weight:650;');a.addWidget(heading)
        # BARIS ASLI 2667: Di home_page: Memasang tata letak antarmuka dan komponennya.
        a.addWidget(text('DES dan Triple DES dengan implementasi manual serta library Crypto.','muted'));a.addStretch(1)
        # BARIS ASLI 2668: Di home_page: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        summary=QHBoxLayout();summary.setSpacing(16)
        # BARIS ASLI 2669: Di home_page: Melakukan iterasi pada elemen/urutan: symbol,title,detail in [('encrypt','DES & 3DES','Dua algoritma enkripsi'),('com....
        for symbol,title,detail in [('encrypt','DES & 3DES','Dua algoritma enkripsi'),('compare','Manual & Library','Perbandingan implementasi'),('file','Format TXT','Masukan dan hasil berbentuk teks')]:
            # BARIS ASLI 2670: Di home_page: Memasang tata letak antarmuka dan komponennya.
            item=QHBoxLayout();item.setSpacing(12);mark=QLabel();mark.setPixmap(icon(symbol,'#6879DC',23).pixmap(23,23));mark.setAlignment(Qt.AlignCenter);mark.setFixedSize(40,40);mark.setStyleSheet('background:#EEF1FF; border-radius:10px;');item.addWidget(mark)
            # BARIS ASLI 2671: Di home_page: Memasang tata letak antarmuka dan komponennya.
            labels=QVBoxLayout();labels.setSpacing(5);labels.addWidget(text(title,'section'));labels.addWidget(text(detail,'muted'));item.addLayout(labels,1);summary.addLayout(item,1)
        # BARIS ASLI 2672: Di home_page: Memasang tata letak antarmuka dan komponennya.
        a.addLayout(summary);lay.addWidget(about,2)
        # BARIS ASLI 2673: Di home_page: Memasang tata letak antarmuka dan komponennya.
        banner,_=notice('Siap untuk praktikum DES / 3DES. Gunakan kunci yang sama saat enkripsi dan dekripsi.');lay.addWidget(banner)
        # BARIS ASLI 2674: Di home_page: Memasang tata letak antarmuka dan komponennya.
        bottom=text('DES dan 3DES digunakan untuk pembelajaran. CBC menyediakan enkripsi tanpa autentikasi.','muted');lay.addWidget(bottom)
        # BARIS ASLI 2675: Di home_page: Memasukkan widget/layout ke susunan tampilan.
        self.pages['home']=self.stack.addWidget(outer)

    # BARIS ASLI 2677: Mendefinisikan fungsi algorithm_selector. Fungsi ini menangani aksi khusus dalam aplikasi.
    def algorithm_selector(self, layout):
        # Pilihan algoritma dan jenis kunci disinkronkan di semua halaman aplikasi.
        row=QHBoxLayout();row.addWidget(text('Algoritma','fieldLabel'))
        box=QComboBox();box.addItems(['DES','3DES']);box.setCurrentText(self.algorithm)
        self.algorithm_boxes.append(box);row.addWidget(box,1);layout.addLayout(row)
        box.currentTextChanged.connect(self.set_algorithm)
        row=QHBoxLayout();row.addWidget(text('Jenis kunci','fieldLabel'))
        kind=QComboBox();kind.addItem('HEX','hex');kind.addItem('Teks UTF-8','text')
        kind.setCurrentIndex(kind.findData(self.key_format));self.key_format_boxes.append(kind)
        row.addWidget(kind,1);layout.addLayout(row)
        kind.currentIndexChanged.connect(lambda _:self.set_key_format(kind.currentData()))
        return box

    def set_key_format(self, value):
        # Jangan mengganti interpretasi kunci ketika pekerjaan kriptografi sedang berjalan.
        if value == self.key_format:
            return
        if self.busy():
            for box in self.key_format_boxes:
                box.blockSignals(True);box.setCurrentIndex(box.findData(self.key_format));box.blockSignals(False)
            return
        if self.keys:
            self.saved_keys[(self.algorithm,self.key_format)] = self.keys[0].text()
        self.key_format=value
        for box in self.key_format_boxes:
            box.blockSignals(True);box.setCurrentIndex(box.findData(value));box.blockSignals(False)
        self.set_keys(self.saved_keys[(self.algorithm,value)])
        self.update_key_hints()
        self.clear_key_results()
        self.status.setText('Jenis kunci '+('Teks UTF-8' if value=='text' else 'HEX')+' dipilih. Gunakan pilihan yang sama saat dekripsi.')

    def clear_key_results(self):
        # Hasil lama tidak boleh disimpan seolah-olah dihitung memakai kunci yang baru.
        for op in self.file_states:
            self.format_changed(op)
        if hasattr(self,'compare_table'):
            self.compare_table.setRowCount(0);self.compare_detail.clear()
        if hasattr(self,'test_log'):
            self.last_test='';self.test_log.clear()
            for label in self.test_result_labels:label.setText('Belum diuji')
        if hasattr(self,'trace_note'):
            self.trace_note.setText('Kunci berubah. Klik Hitung jejak untuk memperbarui ronde.')

    def update_key_hints(self):
        # Ukuran selalu dihitung dalam byte; karakter UTF-8 dapat berukuran lebih dari satu byte.
        sizes='8 byte' if self.algorithm=='DES' else '16 / 24 byte'
        hint=(sizes+' teks UTF-8') if self.key_format=='text' else ('16 digit HEX' if self.algorithm=='DES' else '32 / 48 digit HEX')
        for edit in self.keys:
            edit.setMaxLength(256);edit.setPlaceholderText(hint)
            edit.setToolTip('Pilih jenis kunci yang benar. DES: 8 byte; 3DES: 16 atau 24 byte. Kapitalisasi dan spasi pada teks harus sama.')
        count=None
        if self.keys:
            try:
                value=self.keys[0].text()
                count=len(value.encode('utf-8')) if self.key_format=='text' else len(bytes.fromhex(value))
            except ValueError:
                pass
        for rep,material,_ in self.info_labels:
            if self.algorithm=='DES':
                rep.setText('64 bit (8 byte)');material.setText('56 bit')
            elif count==16:
                rep.setText('128 bit (16 byte)');material.setText('2 × 56 bit (nominal)')
            elif count==24:
                rep.setText('192 bit (24 byte)');material.setText('3 × 56 bit (nominal)')
            else:
                rep.setText('128 / 192 bit (16 / 24 byte)');material.setText('2 atau 3 kunci DES')

    # BARIS ASLI 2684: Mendefinisikan fungsi key_length. Fungsi ini menangani aksi khusus dalam aplikasi.
    def key_length(self):return 8 if self.algorithm=='DES' else 24

    # BARIS ASLI 2686: Mendefinisikan fungsi example_key. Fungsi ini menangani aksi khusus dalam aplikasi.
    def example_key(self):
        # Contoh mengikuti jenis kunci yang aktif, bukan memaksa teks menjadi HEX.
        if self.key_format=='text':
            return 'cerdas00' if self.algorithm=='DES' else 'cerdashumanis000'
        return KUNCI_CONTOH if self.algorithm=='DES' else KUNCI_3DES_CONTOH

    # BARIS ASLI 2688: Mendefinisikan fungsi read_key. Fungsi ini menangani aksi khusus dalam aplikasi.
    def read_key(self, edit):
        # Satu parser yang sama dipakai oleh enkripsi, dekripsi, uji, perbandingan, dan jejak.
        return parse_key(edit.text(),self.algorithm,self.key_format)

    # BARIS ASLI 2691: Mendefinisikan fungsi generate_key. Fungsi ini menangani aksi khusus dalam aplikasi.
    def generate_key(self):
        # Generate teks menghasilkan karakter ASCII sehingga jumlah karakter sama dengan byte.
        if self.key_format=='hex':
            value=(secrets.token_bytes(8) if self.algorithm=='DES' else random_3des_key()).hex().upper()
        else:
            alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            while True:
                value=''.join(secrets.choice(alphabet) for _ in range(self.key_length()))
                try:
                    parse_key(value,self.algorithm,'text');break
                except ValueError:
                    pass
        self.set_keys(value);self.clear_key_results()

    # BARIS ASLI 2694: Mendefinisikan fungsi set_algorithm. Fungsi ini menangani aksi khusus dalam aplikasi.
    def set_algorithm(self,value):
        # BARIS ASLI 2695: Di set_algorithm: Memilih jalur operasi sesuai backend atau jenis algoritma.
        if value==self.algorithm:return
        # BARIS ASLI 2696: Di set_algorithm: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if self.busy():
            # BARIS ASLI 2697: Di set_algorithm: Melakukan iterasi pada elemen/urutan: box in self.algorithm_boxes:box.blockSignals(True);box.setCurrentText(self.algo....
            for box in self.algorithm_boxes:box.blockSignals(True);box.setCurrentText(self.algorithm);box.blockSignals(False)
            # BARIS ASLI 2698: Di set_algorithm: Mengakhiri fungsi dan kembali ke pemanggil.
            return
        # BARIS ASLI 2699: Di set_algorithm: Memilih jalur operasi sesuai backend atau jenis algoritma.
        if self.keys:self.saved_keys[(self.algorithm,self.key_format)]=self.keys[0].text()
        # BARIS ASLI 2700: Di set_algorithm: Menghitung/menyiapkan nilai self.algorithm untuk dipakai oleh proses berikutnya.
        self.algorithm=value
        # BARIS ASLI 2701: Di set_algorithm: Melakukan iterasi pada elemen/urutan: box in self.algorithm_boxes:box.blockSignals(True);box.setCurrentText(value);bo....
        for box in self.algorithm_boxes:box.blockSignals(True);box.setCurrentText(value);box.blockSignals(False)
        # BARIS ASLI 2702: Di set_algorithm: Melakukan iterasi pada elemen/urutan: edit in self.keys:edit.setMaxLength(64);edit.setPlaceholderText(f'{self.key_len....
        self.update_key_hints()
        # BARIS ASLI 2703: Di set_algorithm: Mengatur properti komponen GUI yang digunakan.
        self.set_keys(self.saved_keys[(value,self.key_format)])
        # BARIS ASLI 2704: Di set_algorithm: Melakukan iterasi pada elemen/urutan: rep,material,mode in self.info_labels.
        for rep,material,mode in self.info_labels:
            # BARIS ASLI 2705: Di set_algorithm: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            rep.setText('64 bit (8 byte)' if value=='DES' else '192 bit (24 byte)')
            # BARIS ASLI 2706: Di set_algorithm: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            material.setText('56 bit' if value=='DES' else '3 × 56 bit (nominal)')
            # BARIS ASLI 2707: Di set_algorithm: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            mode.setText(value+'-CBC · PKCS#7')
        # BARIS ASLI 2708: Di set_algorithm: Melakukan iterasi pada elemen/urutan: state in self.file_states.values().
        for state in self.file_states.values():
            # BARIS ASLI 2709: Di set_algorithm: Menghitung/menyiapkan nilai combo untuk dipakai oleh proses berikutnya.
            combo=state['backend'];idx=combo.currentIndex()
            # BARIS ASLI 2710: Di set_algorithm: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            combo.setItemText(0,value+' Library (PyCryptodome)');combo.setItemText(1,value+' Buatan Sendiri');combo.setCurrentIndex(idx)
            # BARIS ASLI 2711: Di set_algorithm: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state['payload']=None;state['save'].setEnabled(False);state['output'].clear();state['stats'].setText('');state['state'].setText(value+' siap.')
        # BARIS ASLI 2712: Di set_algorithm: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: hasattr(self,'test_result_titles').
        if hasattr(self,'test_result_titles'):
            # BARIS ASLI 2713: Di set_algorithm: Memperbarui teks yang terlihat pada elemen antarmuka.
            self.test_result_titles[0].setText(value+' Library (PyCryptodome)');self.test_result_titles[1].setText(value+' Buatan Sendiri')
            # BARIS ASLI 2714: Di set_algorithm: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            self.reset_vector(False)
        # BARIS ASLI 2715: Di set_algorithm: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: hasattr(self,'compare_table').
        if hasattr(self,'compare_table'):
            # BARIS ASLI 2716: Di set_algorithm: Memperbarui teks yang terlihat pada elemen antarmuka.
            self.compare_table.setHorizontalHeaderLabels(['No','Parameter',value+' Library',value+' Buatan Sendiri','Status']);self.compare_table.setRowCount(0);self.compare_detail.clear();self.compare_notice.setText('Algoritma '+value+' dipilih. Jalankan perbandingan.')
        # BARIS ASLI 2717: Di set_algorithm: Melakukan iterasi pada elemen/urutan: op in self.file_states:self.format_changed(op).
        for op in self.file_states:self.format_changed(op)
        # BARIS ASLI 2718: Di set_algorithm: Memperbarui teks yang terlihat pada elemen antarmuka.
        self.update_key_hints()
        self.status.setText(value+' dipilih. '+('Kunci 16 / 24 byte; HEX atau teks UTF-8.' if value=='3DES' else 'Kunci 8 byte; HEX atau teks UTF-8.'))

    # BARIS ASLI 2720: Mendefinisikan fungsi key_panel. Fungsi ini menangani aksi khusus dalam aplikasi.
    def key_panel(self,parent_layout,operation):
        # BARIS ASLI 2721: Di key_panel: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        parent_layout.setSpacing(6);parent_layout.setContentsMargins(12,12,12,12)
        # BARIS ASLI 2722: Di key_panel: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        parent_layout.parentWidget().setStyleSheet('QLineEdit, QComboBox { padding:5px 8px; } QPushButton { padding:5px 8px; }')
        # BARIS ASLI 2723: Di key_panel: Menjalankan langkah self.algorithm_selector(parent_layout) sebagai bagian dari alur fungsi ini.
        self.algorithm_selector(parent_layout)
        # BARIS ASLI 2724: Di key_panel: Menambahkan elemen baru pada daftar hasil atau riwayat.
        edit=field(self.example_key(),True);edit.setMaxLength(256);edit.setPlaceholderText('16 digit HEX / 8 byte teks');parent_layout.addWidget(edit);self.keys.append(edit);edit.textEdited.connect(lambda value:self.sync_keys(value,edit))
        # BARIS ASLI 2725: Di key_panel: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        row=QHBoxLayout();row.setSpacing(5)
        # BARIS ASLI 2726: Di key_panel: Melakukan iterasi pada elemen/urutan: title,fn in [('Contoh',lambda:self.set_keys(self.example_key())),('Generate',se....
        for title,fn in [('Contoh',lambda:self.set_keys(self.example_key())),('Generate',self.generate_key),('Salin kunci',lambda:self.copy_key(edit))]:row.addWidget(button(title,fn))
        # BARIS ASLI 2727: Di key_panel: Memasang tata letak antarmuka dan komponennya.
        parent_layout.addLayout(row);row=QHBoxLayout();row.setSpacing(5);row.addWidget(button('Unggah kunci',lambda:self.load_key(edit)));row.addWidget(button('Simpan kunci',lambda:self.save_key(edit)))
        # BARIS ASLI 2728: Di key_panel: Memasang tata letak antarmuka dan komponennya.
        show=QCheckBox('Lihat');show.setChecked(True);show.toggled.connect(lambda v:edit.setEchoMode(QLineEdit.Normal if v else QLineEdit.Password));row.addWidget(show);parent_layout.addLayout(row)
        # BARIS ASLI 2729: Di key_panel: Memasang tata letak antarmuka dan komponennya.
        backend=QComboBox();backend.addItem('DES Library (PyCryptodome)','library');backend.addItem('DES Buatan Sendiri','manual');parent_layout.addWidget(backend)
        # BARIS ASLI 2730: Di key_panel: Memasang tata letak antarmuka dan komponennya.
        row=QHBoxLayout();row.addWidget(text('Format','fieldLabel'));formats=QComboBox();formats.addItem('CBC · IV + ciphertext','cbc');formats.addItem('ECB · ciphertext saja','ecb');formats.setCurrentIndex(0);row.addWidget(formats,1);parent_layout.addLayout(row);self.format_boxes[operation]=formats
        # BARIS ASLI 2731: Di key_panel: Melakukan iterasi pada elemen/urutan: w in [edit,backend,formats]+parent_layout.parentWidget().findChildren(QPushButt....
        for w in [edit,backend,formats]+parent_layout.parentWidget().findChildren(QPushButton):w.setMinimumHeight(36)
        # BARIS ASLI 2732: Di key_panel: Mengembalikan nilai perhitungan ke pemanggil: edit,backend.
        return edit,backend

    # BARIS ASLI 2734: Mendefinisikan fungsi sync_keys. Fungsi ini menangani aksi khusus dalam aplikasi.
    def sync_keys(self, value, origin):
        # Menyamakan teks mentah, tanpa mengubah huruf besar/kecil atau spasi.
        for edit in self.keys:
            if edit is not origin:edit.setText(value)
        self.saved_keys[(self.algorithm,self.key_format)]=value
        self.update_key_hints();self.clear_key_results()

    # BARIS ASLI 2739: Mendefinisikan fungsi set_keys. Fungsi ini menangani aksi khusus dalam aplikasi.
    def set_keys(self, value):
        # Perubahan lewat tombol Contoh / Generate juga harus memperbarui informasi ukuran.
        for edit in self.keys:edit.setText(value)
        self.saved_keys[(self.algorithm,self.key_format)]=value
        self.update_key_hints();self.clear_key_results()

    # BARIS ASLI 2743: Mendefinisikan fungsi copy_key. Fungsi ini menangani aksi khusus dalam aplikasi.
    def copy_key(self,edit):
        # BARIS ASLI 2744: Di copy_key: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        QApplication.clipboard().setText(edit.text());self.status.setText('Kunci disalin. Gunakan kunci yang sama untuk dekripsi.')

    # BARIS ASLI 2746: Mendefinisikan fungsi load_key. Fungsi ini menangani aksi khusus dalam aplikasi.
    def load_key(self, edit):
        # File tetap TXT polos. Pilih HEX / Teks UTF-8 sesuai isi file sebelum mengunggah.
        name,_=QFileDialog.getOpenFileName(self,'Unggah kunci '+self.algorithm,'','Kunci teks (*.txt)')
        if not name:return
        try:
            value=Path(name).read_text(encoding='utf-8-sig')
            if self.key_format=='hex':
                value=value.strip()
            else:
                # Abaikan satu penutup baris file; spasi serta kapitalisasi kunci tetap dipertahankan.
                value=value.removesuffix('\n').removesuffix('\r')
            parse_key(value,self.algorithm,self.key_format)
            self.set_keys(value.upper() if self.key_format=='hex' else value)
            self.status.setText('Kunci berhasil dimuat sebagai '+('HEX.' if self.key_format=='hex' else 'teks UTF-8.'))
        except (OSError,ValueError) as exc:self.error(str(exc))

    # BARIS ASLI 2753: Mendefinisikan fungsi save_key. Fungsi ini menangani aksi khusus dalam aplikasi.
    def save_key(self, edit):
        # Simpan representasi yang dipilih dalam TXT, terpisah dari ciphertext.
        try:
            key=self.read_key(edit)
            value=key.hex().upper() if self.key_format=='hex' else edit.text()
            name,_=QFileDialog.getSaveFileName(self,'Simpan kunci (berkas terpisah)','kunci_'+self.algorithm+'.txt','Teks (*.txt)')
            if name:
                Path(name).with_suffix('.txt').write_text(value,encoding='utf-8')
                self.status.setText('Kunci disimpan sebagai '+('HEX' if self.key_format=='hex' else 'teks UTF-8')+'. Gunakan jenis yang sama saat memuat.')
        except (OSError,ValueError) as exc:self.error(str(exc))

    # BARIS ASLI 2761: Mendefinisikan fungsi file_page. Fungsi ini menangani aksi khusus dalam aplikasi.
    def file_page(self,operation):
        # BARIS ASLI 2762: Di file_page: Menghitung/menyiapkan nilai enc untuk dipakai oleh proses berikutnya.
        enc=operation=='encrypt'
        # BARIS ASLI 2763: Di file_page: Menghitung/menyiapkan nilai lay untuk dipakai oleh proses berikutnya.
        lay=self.page(operation,'Enkripsi Pesan' if enc else 'Dekripsi Pesan','Pilih file TXT atau ketik teks, lalu proses dengan DES / 3DES.' if enc else 'Pilih ciphertext TXT atau tempel HEX. Samakan algoritma, kunci, dan format dengan pengirim.',scrollable=False)
        # BARIS ASLI 2764: Di file_page: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        grid=QGridLayout();grid.setSpacing(10)
        # BARIS ASLI 2765: Di file_page: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        sourcecard,src=card('1. Masukan Plaintext' if enc else '1. Masukan Ciphertext');src.setContentsMargins(12,12,12,12);src.setSpacing(6)
        # BARIS ASLI 2766: Di file_page: Memasang tata letak antarmuka dan komponennya.
        filelabel=text('Belum ada masukan','muted');src.addWidget(filelabel)
        # BARIS ASLI 2767: Di file_page: Memasang tata letak antarmuka dan komponennya.
        sourcecard.setStyleSheet('QPushButton { padding:5px 8px; }');row=QHBoxLayout();row.setSpacing(5);choose=button('Pilih TXT',lambda:self.choose_input(operation),'primary','file');row.addWidget(choose)
        # BARIS ASLI 2768: Di file_page: Memasang tata letak antarmuka dan komponennya.
        row.addWidget(button('Tulis / tempel',lambda:self.plaintext_dialog() if enc else self.ciphertext_dialog()));src.addLayout(row)
        # BARIS ASLI 2769: Di file_page: Menambahkan elemen baru pada daftar hasil atau riwayat.
        preview=QPlainTextEdit();preview.setReadOnly(True);preview.setMinimumHeight(55);preview.setFont(QFont('Consolas',10));preview.setPlaceholderText('Isi masukan tampil di sini.');src.addWidget(preview,1);grid.addWidget(sourcecard,0,0);self.process_controls.append(sourcecard)
        # BARIS ASLI 2770: Di file_page: Memakai operasi bit AND/OR untuk menyeleksi atau menggabungkan bit.
        keycard,k=card('2. Algoritma & Kunci');key,backend=self.key_panel(k,operation);grid.addWidget(keycard,0,1);self.process_controls.append(keycard);self.format_boxes[operation].currentIndexChanged.connect(lambda _,op=operation:self.format_changed(op))
        # BARIS ASLI 2771: Di file_page: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        infocard,info=card('Informasi');info.setContentsMargins(12,12,12,12);info.setSpacing(6)
        # BARIS ASLI 2772: Di file_page: Menambahkan elemen baru pada daftar hasil atau riwayat.
        info.addWidget(text('Ukuran kunci','fieldLabel'));rep=text('64 bit (8 byte)','section');info.addWidget(rep);info.addWidget(text('Material kunci','fieldLabel'));material=text('56 bit','section');info.addWidget(material);mode=text('DES-CBC · PKCS#7','section');info.addWidget(mode);self.info_labels.append((rep,material,mode))
        # BARIS ASLI 2773: Di file_page: Memasang tata letak antarmuka dan komponennya.
        info.addWidget(text('CBC: IV dibaca otomatis. ECB: tanpa IV.','muted'));statuscard,state=notice('Siap diproses.');info.addWidget(statuscard);info.addStretch(1);grid.addWidget(infocard,0,2)
        # BARIS ASLI 2774: Di file_page: Memasang tata letak antarmuka dan komponennya.
        grid.setColumnStretch(0,3);grid.setColumnStretch(1,3);grid.setColumnStretch(2,2);lay.addLayout(grid)
        # BARIS ASLI 2775: Di file_page: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        resultcard,r=card('3. Hasil Enkripsi' if enc else '3. Hasil Dekripsi');resultcard.setStyleSheet('QPushButton { padding:5px 10px; }');r.setContentsMargins(12,10,12,10);r.setSpacing(6)
        # BARIS ASLI 2776: Di file_page: Memasang tata letak antarmuka dan komponennya.
        row=QHBoxLayout();row.setSpacing(6);start=self.track(button('Enkripsi' if enc else 'Dekripsi',lambda:self.start_operation(operation),'primary',operation));row.addWidget(start);save=button('Simpan ciphertext TXT' if enc else 'Simpan plaintext TXT',lambda:self.save_result(operation),symbol='save');save.setEnabled(False);row.addWidget(save);row.addStretch(1);r.addLayout(row)
        # BARIS ASLI 2777: Di file_page: Memasang tata letak antarmuka dan komponennya.
        output=QPlainTextEdit();output.setReadOnly(True);output.setFont(QFont('Consolas',10));output.setMinimumHeight(55);output.setPlaceholderText('Hasil proses tampil di sini.');r.addWidget(output,1)
        # BARIS ASLI 2778: Di file_page: Memasang tata letak antarmuka dan komponennya.
        stats=text('','muted');stats.setStyleSheet('color:#7894BD; font-size:10px;');r.addWidget(stats);lay.addWidget(resultcard,1)
        # BARIS ASLI 2779: Di file_page: Melakukan iterasi pada elemen/urutan: btn in sourcecard.findChildren(QPushButton)+resultcard.findChildren(QPushButton....
        for btn in sourcecard.findChildren(QPushButton)+resultcard.findChildren(QPushButton):btn.setMinimumHeight(36)
        # BARIS ASLI 2780: Di file_page: Menghitung/menyiapkan nilai self.file_states[operation] untuk dipakai oleh proses berikutnya.
        self.file_states[operation]={'path':None,'manual_text':None,'label':filelabel,'preview':preview,'key':key,'backend':backend,'state':state,'output':output,'save':save,'stats':stats,'payload':None,'result_source':None}

    # BARIS ASLI 2782: Mendefinisikan fungsi format_changed. Fungsi ini menangani aksi khusus dalam aplikasi.
    def format_changed(self,operation):
        # BARIS ASLI 2783: Di format_changed: Menghitung/menyiapkan nilai state untuk dipakai oleh proses berikutnya.
        state=self.file_states.get(operation)
        # BARIS ASLI 2784: Di format_changed: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: state.
        if state:
            # BARIS ASLI 2785: Di format_changed: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state['payload']=None;state['save'].setEnabled(False);state['output'].clear();state['stats'].clear()
            # BARIS ASLI 2786: Di format_changed: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state['state'].setText('Format dipilih.')
        # BARIS ASLI 2787: Di format_changed: Melakukan iterasi pada elemen/urutan: op,labels in zip(('encrypt','decrypt'),self.info_labels).
        for op,labels in zip(('encrypt','decrypt'),self.info_labels):
            # BARIS ASLI 2788: Di format_changed: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            labels[2].setText(self.algorithm+('-ECB' if self.format_boxes[op].currentData()=='ecb' else '-CBC')+' · PKCS#7')

    # BARIS ASLI 2790: Mendefinisikan fungsi choose_input. Fungsi ini menangani aksi khusus dalam aplikasi.
    def choose_input(self,operation):
        # BARIS ASLI 2791: Di choose_input: Menghitung/menyiapkan nilai enc untuk dipakai oleh proses berikutnya.
        enc=operation=='encrypt';filters='Teks (*.txt)' if enc else 'Ciphertext TXT (*.txt)'
        # BARIS ASLI 2792: Di choose_input: Menampilkan dialog untuk memilih lokasi file input/output.
        name,_=QFileDialog.getOpenFileName(self,'Pilih file teks' if enc else 'Pilih file ciphertext','',filters)
        # BARIS ASLI 2793: Di choose_input: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if name:self.set_input(operation,Path(name))

    # BARIS ASLI 2795: Mendefinisikan fungsi set_input. Fungsi ini menangani aksi khusus dalam aplikasi.
    def set_input(self,operation,path):
        # BARIS ASLI 2796: Di set_input: Menghitung/menyiapkan nilai state untuk dipakai oleh proses berikutnya.
        state=self.file_states[operation]
        # BARIS ASLI 2797: Di set_input: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:
            # BARIS ASLI 2798: Di set_input: Mengelola resource atau file sementara agar ditutup/dibersihkan otomatis.
            with path.open('rb') as f:data=f.read(24000)
            # BARIS ASLI 2799: Di set_input: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: operation=='decrypt'.
            if operation=='decrypt':
                # BARIS ASLI 2800: Di set_input: Membaca seluruh konten file sebagai byte/teks.
                record=self.resolve_ciphertext(path.read_text(encoding='utf-8'));algo=record.get('algorithm')
                # BARIS ASLI 2801: Di set_input: Memastikan dependensi atau algoritma kriptografi tersedia/valid.
                if algo not in ('DES','3DES'):raise ValueError('Algoritma ciphertext tidak didukung.')
                # BARIS ASLI 2802: Di set_input: Mengatur properti komponen GUI yang digunakan.
                self.set_algorithm(algo)
            # BARIS ASLI 2803: Di set_input: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state['path']=path;state['manual_text']=None;state['label'].setText(path.name+'  ('+f'{path.stat().st_size:,}'+' byte)');state['label'].setToolTip(str(path))
            # BARIS ASLI 2804: Di set_input: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state['preview'].setPlainText((serialize_ciphertext(record,self.format_boxes['decrypt'].currentData()).strip() if operation=='decrypt' else data.decode('utf-8',errors='replace'))[:16000]);state['payload']=None;state['save'].setEnabled(False);state['output'].clear();state['stats'].setText('')
            # BARIS ASLI 2805: Di set_input: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state['state'].setText('Masukan siap.');self.status.setText('File dipilih: '+path.name)
        # BARIS ASLI 2806: Di set_input: Menangani kesalahan (OSError,ValueError) as excself.error(str(exc)).
        except (OSError,ValueError) as exc:self.error(str(exc))

    # BARIS ASLI 2808: Mendefinisikan fungsi resolve_ciphertext. Fungsi ini menangani aksi khusus dalam aplikasi.
    def resolve_ciphertext(self,value):
        # BARIS ASLI 2809: Di resolve_ciphertext: Menghitung/menyiapkan nilai compact untuk dipakai oleh proses berikutnya.
        compact=''.join(value.lstrip('\ufeff').split()).upper()
        # BARIS ASLI 2810: Di resolve_ciphertext: Memeriksa jenis format atau mode penyimpanan data.
        if compact.startswith('5A434432') or value.lstrip('\ufeff').startswith(('ZAR1:','ZarCryptoDES Ciphertext v1')):self.format_boxes['decrypt'].setCurrentIndex(0)
        # BARIS ASLI 2811: Di resolve_ciphertext: Mengembalikan keluaran metode/hasil pemrosesan objek.
        return parse_ciphertext(value,self.algorithm,wire_format=self.format_boxes['decrypt'].currentData())

    # BARIS ASLI 2813: Mendefinisikan fungsi set_manual_ciphertext. Fungsi ini menangani aksi khusus dalam aplikasi.
    def set_manual_ciphertext(self,value):
        # BARIS ASLI 2814: Di set_manual_ciphertext: Menghitung/menyiapkan nilai record untuk dipakai oleh proses berikutnya.
        record=self.resolve_ciphertext(value)
        # BARIS ASLI 2815: Di set_manual_ciphertext: Mengatur properti komponen GUI yang digunakan.
        self.set_algorithm(record['algorithm'])
        # BARIS ASLI 2816: Di set_manual_ciphertext: Menghitung/menyiapkan nilai state untuk dipakai oleh proses berikutnya.
        state=self.file_states['decrypt'];state['path']=None;state['manual_text']=value
        # BARIS ASLI 2817: Di set_manual_ciphertext: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        state['label'].setText('Ciphertext dari masukan manual');state['label'].setToolTip('Diketik / ditempel langsung')
        # BARIS ASLI 2818: Di set_manual_ciphertext: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        state['preview'].setPlainText(value);state['payload']=None;state['save'].setEnabled(False)
        # BARIS ASLI 2819: Di set_manual_ciphertext: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        state['output'].clear();state['stats'].setText('');state['state'].setText('Ciphertext siap.')
        # BARIS ASLI 2820: Di set_manual_ciphertext: Memperbarui teks yang terlihat pada elemen antarmuka.
        self.status.setText('Ciphertext manual siap didekripsi.')

    # BARIS ASLI 2822: Mendefinisikan fungsi ciphertext_dialog. Fungsi ini menangani aksi khusus dalam aplikasi.
    def ciphertext_dialog(self):
        # BARIS ASLI 2823: Di ciphertext_dialog: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        dialog=QDialog(self);dialog.setWindowTitle('Tulis / tempel ciphertext');dialog.resize(650,430)
        # BARIS ASLI 2824: Di ciphertext_dialog: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        lay=QVBoxLayout(dialog);lay.setContentsMargins(22,22,22,22);lay.setSpacing(12)
        # BARIS ASLI 2825: Di ciphertext_dialog: Memasang tata letak antarmuka dan komponennya.
        lay.addWidget(text('Masukan ciphertext','section'))
        # BARIS ASLI 2826: Di ciphertext_dialog: Memasang tata letak antarmuka dan komponennya.
        lay.addWidget(text('Tempel seluruh rangkaian HEX hasil enkripsi. IV dibaca otomatis; pilih algoritma dan gunakan kunci yang sama. Format TXT lama dan ZAR1 juga dapat dibaca.','muted'))
        # BARIS ASLI 2827: Di ciphertext_dialog: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        editor=QPlainTextEdit();editor.setFont(QFont('Consolas',10))
        # BARIS ASLI 2828: Di ciphertext_dialog: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        editor.setPlainText(self.file_states['decrypt']['manual_text'] or '')
        # BARIS ASLI 2829: Di ciphertext_dialog: Memasang tata letak antarmuka dan komponennya.
        editor.setPlaceholderText('Tempel ciphertext lengkap di sini…');lay.addWidget(editor,1)
        # BARIS ASLI 2830: Mendefinisikan fungsi use. Fungsi ini menangani aksi khusus dalam aplikasi.
        def use():
            # BARIS ASLI 2831: Di use: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
            try:self.set_manual_ciphertext(editor.toPlainText());dialog.accept()
            # BARIS ASLI 2832: Di use: Menangani kesalahan ValueError as excself.error(str(exc)).
            except ValueError as exc:self.error(str(exc))
        # BARIS ASLI 2833: Di ciphertext_dialog: Memasang tata letak antarmuka dan komponennya.
        lay.addWidget(button('Gunakan ciphertext',use,'primary','decrypt'));dialog.exec()

    # BARIS ASLI 2835: Mendefinisikan fungsi set_manual_plaintext. Fungsi ini menangani aksi khusus dalam aplikasi.
    def set_manual_plaintext(self,value):
        # BARIS ASLI 2836: Di set_manual_plaintext: Menghitung/menyiapkan nilai state untuk dipakai oleh proses berikutnya.
        state=self.file_states['encrypt'];state['path']=None;state['manual_text']=value
        # BARIS ASLI 2837: Di set_manual_plaintext: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        state['label'].setText('Plaintext dari masukan manual');state['label'].setToolTip('Diketik / ditempel langsung')
        # BARIS ASLI 2838: Di set_manual_plaintext: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        state['preview'].setPlainText(value);state['payload']=None;state['save'].setEnabled(False);state['output'].clear();state['stats'].setText('')
        # BARIS ASLI 2839: Di set_manual_plaintext: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        state['state'].setText('Plaintext siap dienkripsi.');self.status.setText('Masukan plaintext manual siap.')

    # BARIS ASLI 2841: Mendefinisikan fungsi plaintext_dialog. Fungsi ini menangani aksi khusus dalam aplikasi.
    def plaintext_dialog(self,target='encrypt'):
        # BARIS ASLI 2842: Di plaintext_dialog: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        dialog=QDialog(self);dialog.setWindowTitle('Tulis / tempel plaintext');dialog.resize(650,430)
        # BARIS ASLI 2843: Di plaintext_dialog: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        layout=QVBoxLayout(dialog);layout.setContentsMargins(22,22,22,22);layout.setSpacing(12)
        # BARIS ASLI 2844: Di plaintext_dialog: Memasang tata letak antarmuka dan komponennya.
        layout.addWidget(text('Pesan untuk dienkripsi','section'));layout.addWidget(text('Ketik atau tempel teks. Spasi, tanda baca, dan baris baru ikut diproses.','muted'))
        # BARIS ASLI 2845: Di plaintext_dialog: Memasang tata letak antarmuka dan komponennya.
        editor=QPlainTextEdit();editor.setPlainText((self.file_states['encrypt']['manual_text'] if target=='encrypt' else self.compare_text) or '');layout.addWidget(editor,1)
        # BARIS ASLI 2846: Mendefinisikan fungsi use. Fungsi ini menangani aksi khusus dalam aplikasi.
        def use():
            # BARIS ASLI 2847: Di use: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
            if target=='encrypt':self.set_manual_plaintext(editor.toPlainText())
            # BARIS ASLI 2848: Di use: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
            else:self.set_compare_plaintext(editor.toPlainText())
            # BARIS ASLI 2849: Di use: Menjalankan langkah dialog.accept() sebagai bagian dari alur fungsi ini.
            dialog.accept()
        # BARIS ASLI 2850: Di plaintext_dialog: Memasang tata letak antarmuka dan komponennya.
        layout.addWidget(button('Gunakan plaintext',use,'primary','encrypt'));dialog.exec()

    # BARIS ASLI 2852: Mendefinisikan fungsi start_operation. Fungsi ini menangani aksi khusus dalam aplikasi.
    def start_operation(self,operation):
        # BARIS ASLI 2853: Di start_operation: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if self.busy():return
        # BARIS ASLI 2854: Di start_operation: Menghitung/menyiapkan nilai state untuk dipakai oleh proses berikutnya.
        state=self.file_states[operation]
        # BARIS ASLI 2855: Di start_operation: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:
            # BARIS ASLI 2856: Di start_operation: Menghitung/menyiapkan nilai manual_text untuk dipakai oleh proses berikutnya.
            manual_text=state['manual_text']
            # BARIS ASLI 2857: Di start_operation: Menghitung/menyiapkan nilai source untuk dipakai oleh proses berikutnya.
            source=state['path'] or (Path('plaintext_manual.txt' if operation=='encrypt' else 'ciphertext_manual.txt') if manual_text is not None else None)
            # BARIS ASLI 2858: Di start_operation: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: not source:raise ValueError('Pilih file masukan atau tulis / tempel teks terleb....
            if not source:raise ValueError('Pilih file masukan atau tulis / tempel teks terlebih dahulu.')
            # BARIS ASLI 2859: Di start_operation: Menghitung/menyiapkan nilai algorithm untuk dipakai oleh proses berikutnya.
            algorithm=self.algorithm;key=self.read_key(state['key']);backend=state['backend'].currentData();wire_format=self.format_boxes[operation].currentData();original=self.original_plain
            # Hapus hasil lama ketika operasi baru dimulai atau validasi gagal.
            # BARIS ASLI 2861: Di start_operation: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state['payload']=None;state['save'].setEnabled(False);state['output'].clear()
            # BARIS ASLI 2862: Mendefinisikan fungsi work. Fungsi ini menangani aksi khusus dalam aplikasi.
            def work():
                # BARIS ASLI 2863: Di work: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: operation=='encrypt'.
                if operation=='encrypt':
                    # BARIS ASLI 2864: Di work: Membaca seluruh konten file sebagai byte/teks.
                    data=manual_text.encode('utf-8') if manual_text is not None else source.read_bytes();record=encrypt_message(data,key,backend,algorithm,wire_format);payload=serialize_ciphertext(record,wire_format).encode('utf-8')
                    # BARIS ASLI 2865: Di work: Mendekode teks heksadesimal menjadi representasi byte.
                    preview=payload.decode('utf-8').strip();n_input=len(data);n_output=len(bytes.fromhex(record['ciphertext_hex']))
                # BARIS ASLI 2866: Di work: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
                else:
                    # BARIS ASLI 2867: Di work: Membaca seluruh konten file sebagai byte/teks.
                    record=parse_ciphertext(manual_text if manual_text is not None else source.read_text(encoding='utf-8'),algorithm,wire_format=wire_format)
                    # BARIS ASLI 2868: Di work: Memilih jalur operasi sesuai backend atau jenis algoritma.
                    if record.get('algorithm')!=algorithm:raise ValueError('Pilih algoritma '+str(record.get('algorithm'))+' sesuai file ciphertext.')
                    # BARIS ASLI 2869: Di work: Memulihkan plaintext berdasarkan metadata ciphertext dan kunci.
                    payload=decrypt_record(record,key,backend)
                    
                    # BARIS ASLI 2871: Di work: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
                    try:preview=payload.decode('utf-8')
                    # BARIS ASLI 2872: Di work: Menangani kesalahan UnicodeDecodeError as excraise ValueError('Hasil dekripsi bukan tek....
                    except UnicodeDecodeError as exc:raise ValueError('Hasil dekripsi bukan teks UTF-8. Periksa kunci dan format CBC/ECB sesuai pengirim.') from exc
                    # BARIS ASLI 2873: Di work: Mendekode teks heksadesimal menjadi representasi byte.
                    n_input=len(bytes.fromhex(record['ciphertext_hex']));n_output=len(payload)
                # BARIS ASLI 2874: Di work: Mengembalikan hasil akumulasi pemrosesan.
                return {'algorithm':algorithm,'operation':operation,'backend':backend,'source':source,'payload':payload,'preview':preview,'input':n_input,'output':n_output,'iv':record['iv_hex'],'summary':message_summary(len(data) if operation=='encrypt' else len(payload),len(serialize_ciphertext(record,wire_format).strip())//2),'verification':None if operation=='encrypt' or original is None else payload==original}
            # BARIS ASLI 2875: Di start_operation: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state['state'].setText('Proses sedang berjalan...');self.launch(operation,work)
        # BARIS ASLI 2876: Di start_operation: Menangani kesalahan (ValueError,OSError) as exc.
        except (ValueError,OSError) as exc:
            # BARIS ASLI 2877: Di start_operation: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state['payload']=None;state['save'].setEnabled(False);state['output'].clear();state['stats'].setText('');state['state'].setText('Masukan belum valid. Hasil baru belum dibuat.');self.error(str(exc))

    # BARIS ASLI 2879: Mendefinisikan fungsi save_result. Fungsi ini menangani aksi khusus dalam aplikasi.
    def save_result(self,operation):
        # BARIS ASLI 2880: Di save_result: Menghitung/menyiapkan nilai state untuk dipakai oleh proses berikutnya.
        state=self.file_states[operation]
        # BARIS ASLI 2881: Di save_result: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: state['payload'] is None:return.
        if state['payload'] is None:return
        # BARIS ASLI 2882: Di save_result: Menghitung/menyiapkan nilai src untuk dipakai oleh proses berikutnya.
        src=state['result_source'];enc=operation=='encrypt'
        # BARIS ASLI 2883: Di save_result: Menghitung/menyiapkan nilai initial untuk dipakai oleh proses berikutnya.
        initial=str(src.with_name(src.stem+('_cipher.txt' if enc else '_pulih.txt')))
        # BARIS ASLI 2884: Di save_result: Menampilkan dialog untuk memilih lokasi file input/output.
        name,_=QFileDialog.getSaveFileName(self,'Simpan ciphertext' if enc else 'Simpan plaintext',initial,'Teks (*.txt)')
        # BARIS ASLI 2885: Di save_result: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: not name:return.
        if not name:return
        # BARIS ASLI 2886: Di save_result: Menghitung/menyiapkan nilai name untuk dipakai oleh proses berikutnya.
        name=str(Path(name).with_suffix('.txt'))
        # BARIS ASLI 2887: Di save_result: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:
            # BARIS ASLI 2888: Di save_result: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: Path(name).resolve()==src.resolve():raise ValueError('File masukan tidak boleh ....
            if Path(name).resolve()==src.resolve():raise ValueError('File masukan tidak boleh ditimpa oleh hasil operasi.')
            # BARIS ASLI 2889: Di save_result: Menyimpan byte/teks hasil operasi ke berkas yang dipilih.
            Path(name).write_bytes(state['payload']);state['state'].setText('Enkripsi disimpan.' if enc else 'Plaintext berhasil disimpan.')
            # BARIS ASLI 2890: Di save_result: Memperbarui teks yang terlihat pada elemen antarmuka.
            self.status.setText('File tersimpan: '+name);self.add_history('Simpan '+('ciphertext' if enc else 'plaintext'),state['result_backend'],src.name,str(Path(name).resolve()),len(state['payload']))
        # BARIS ASLI 2891: Di save_result: Menangani kesalahan (ValueError,OSError) as excself.error(str(exc)).
        except (ValueError,OSError) as exc:self.error(str(exc))

    # BARIS ASLI 2893: Mendefinisikan fungsi test_page. Fungsi ini menangani aksi khusus dalam aplikasi.
    def test_page(self):
        # BARIS ASLI 2894: Di test_page: Menghitung/menyiapkan nilai lay untuk dipakai oleh proses berikutnya.
        lay=self.page('test','Uji DES / 3DES','Bandingkan DES atau 3DES library dengan implementasi buatan sendiri menggunakan vektor uji.')
        # BARIS ASLI 2895: Di test_page: Menambahkan elemen baru pada daftar hasil atau riwayat.
        box,b=card('Vektor Uji Standar');self.process_controls.append(box);self.algorithm_selector(b);form=QGridLayout()
        # BARIS ASLI 2896: Di test_page: Menghitung/menyiapkan nilai self.test_key untuk dipakai oleh proses berikutnya.
        self.test_key=field(KUNCI_CONTOH,True);self.keys.append(self.test_key);self.test_key.textEdited.connect(lambda value:self.sync_keys(value,self.test_key));self.test_plain=field('0123456789ABCDEF',True);self.test_expected=field('85E813540F0AB405',True)
        # BARIS ASLI 2897: Di test_page: Melakukan iterasi pada elemen/urutan: c,(title,edit) in enumerate([('Kunci',self.test_key),('Plaintext (HEX)',s....
        for c,(title,edit) in enumerate([('Kunci',self.test_key),('Plaintext (HEX)',self.test_plain),('Ciphertext acuan (HEX, boleh kosong)',self.test_expected)]):form.addWidget(text(title,'fieldLabel'),0,c);form.addWidget(edit,1,c)
        # BARIS ASLI 2898: Di test_page: Memasang tata letak antarmuka dan komponennya.
        b.addLayout(form);b.addWidget(button('Pulihkan vektor contoh',lambda:self.reset_vector()));lay.addWidget(box)
        # BARIS ASLI 2899: Di test_page: Menghitung/menyiapkan nilai results untuk dipakai oleh proses berikutnya.
        results=QHBoxLayout();self.test_result_labels=[];self.test_result_notes=[];self.test_result_titles=[]
        # BARIS ASLI 2900: Di test_page: Melakukan iterasi pada elemen/urutan: title in ['DES Library (PyCryptodome)','DES Buatan Sendiri','Hasil Pengujian'].
        for title in ['DES Library (PyCryptodome)','DES Buatan Sendiri','Hasil Pengujian']:
            # BARIS ASLI 2901: Di test_page: Menambahkan elemen baru pada daftar hasil atau riwayat.
            w,c=card(title);self.test_result_titles.append(c.itemAt(0).widget());label=text('Belum diuji','section');label.setTextInteractionFlags(Qt.TextSelectableByMouse);c.addWidget(label);note=text('Jalankan pengujian untuk melihat hasil.','muted');c.addWidget(note);results.addWidget(w,1);self.test_result_labels.append(label);self.test_result_notes.append(note)
        # BARIS ASLI 2902: Di test_page: Memasang tata letak antarmuka dan komponennya.
        lay.addLayout(results)
        # BARIS ASLI 2903: Di test_page: Memasang tata letak antarmuka dan komponennya.
        lay.addWidget(self.track(button('Jalankan pengujian',self.start_test,'primary','test')))
        # BARIS ASLI 2904: Di test_page: Memasukkan widget/layout ke susunan tampilan.
        self.test_log=QPlainTextEdit();self.test_log.setReadOnly(True);self.test_log.setMinimumHeight(160);self.test_log.setFont(QFont('Consolas',10));self.test_log.setPlaceholderText('Log pengujian vektor, CBC, file, dan Feistel muncul di sini.');lay.addWidget(self.test_log,1)
        # BARIS ASLI 2905: Di test_page: Memasang tata letak antarmuka dan komponennya.
        lay.addWidget(button('Simpan hasil pengujian .txt',self.save_test,symbol='save'))

    # BARIS ASLI 2907: Mendefinisikan fungsi reset_vector. Fungsi ini menangani aksi khusus dalam aplikasi.
    def reset_vector(self, force_hex=True):
        # Tombol pemulihan memilih vektor HEX standar; pergantian algoritma tidak mengubah jenis kunci.
        if force_hex:
            self.set_key_format('hex')
            self.set_keys(self.example_key())
        self.test_key.setText(self.keys[0].text())
        self.test_plain.setText('0123456789ABCDEF')
        self.test_expected.setText(('85E813540F0AB405' if self.algorithm=='DES' else ACUAN_3DES) if self.key_format=='hex' else '')
        self.last_test='';self.test_log.clear()
        for label in self.test_result_labels:label.setText('Belum diuji');label.setStyleSheet('')
        for label in self.test_result_notes:label.setText('Jalankan pengujian untuk melihat hasil.')

    # BARIS ASLI 2913: Mendefinisikan fungsi start_test. Fungsi ini menangani aksi khusus dalam aplikasi.
    def start_test(self):
        # BARIS ASLI 2914: Di start_test: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if self.busy():return
        # BARIS ASLI 2915: Di start_test: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:
            # BARIS ASLI 2916: Di start_test: Menghitung/menyiapkan nilai algorithm untuk dipakai oleh proses berikutnya.
            algorithm=self.algorithm;key=self.read_key(self.test_key);plain=parse_hex(self.test_plain.text(),8,'Plaintext');expect=self.test_expected.text().strip();expected=None if not expect else parse_hex(expect,8,'Ciphertext acuan')
            # BARIS ASLI 2917: Mendefinisikan fungsi work. Fungsi ini menangani aksi khusus dalam aplikasi.
            def work():
                # BARIS ASLI 2918: Di work: Menghitung/menyiapkan nilai manual untuk dipakai oleh proses berikutnya.
                manual=DESManual(key) if algorithm=='DES' else TripleDESManual(key);module=DES if algorithm=='DES' else DES3
                # BARIS ASLI 2919: Di work: Membuat cipher dari PyCryptodome untuk implementasi library/pembanding.
                cm=manual.encrypt_block(plain);cl=module.new(key,module.MODE_ECB).encrypt(plain)
                # BARIS ASLI 2920: Di work: Membuat cipher dari PyCryptodome untuk implementasi library/pembanding.
                verify(cm==cl,'Implementasi manual berbeda dengan library.');verify(manual.decrypt_block(cl)==plain,'Dekripsi silang gagal.');verify(module.new(key,module.MODE_ECB).decrypt(cm)==plain,'Dekripsi library gagal.')
                # BARIS ASLI 2921: Di work: Menghitung/menyiapkan nilai result untuk dipakai oleh proses berikutnya.
                result=run_verification() if algorithm=='DES' else run_3des_verification();result.update({'algorithm':algorithm,'manual':cm.hex().upper(),'library':cl.hex().upper(),'expected_match':None if expected is None else cm==expected,'plaintext':plain.hex().upper()})
                # BARIS ASLI 2922: Di work: Mengembalikan nilai perhitungan ke pemanggil: result.
                return result
            # BARIS ASLI 2923: Di start_test: Menjalankan langkah self.launch('test',work) sebagai bagian dari alur fungsi ini.
            self.launch('test',work)
        # BARIS ASLI 2924: Di start_test: Menangani kesalahan ValueError as excself.error(str(exc)).
        except ValueError as exc:self.error(str(exc))

    # BARIS ASLI 2926: Mendefinisikan fungsi save_test. Fungsi ini menangani aksi khusus dalam aplikasi.
    def save_test(self):
        # BARIS ASLI 2927: Di save_test: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if not self.last_test:self.error('Jalankan pengujian terlebih dahulu.');return
        # BARIS ASLI 2928: Di save_test: Menampilkan dialog untuk memilih lokasi file input/output.
        name,_=QFileDialog.getSaveFileName(self,'Simpan hasil uji','hasil_uji_'+self.algorithm+'.txt','Teks (*.txt)')
        # BARIS ASLI 2929: Di save_test: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: name.
        if name:
            # BARIS ASLI 2930: Di save_test: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
            try:Path(name).with_suffix('.txt').write_text(self.last_test+'\n',encoding='utf-8');self.status.setText('Hasil pengujian tersimpan.')
            # BARIS ASLI 2931: Di save_test: Menangani kesalahan OSError as excself.error(str(exc)).
            except OSError as exc:self.error(str(exc))

    # BARIS ASLI 2933: Mendefinisikan fungsi compare_page. Fungsi ini menangani aksi khusus dalam aplikasi.
    def compare_page(self):
        # BARIS ASLI 2934: Di compare_page: Menghitung/menyiapkan nilai lay untuk dipakai oleh proses berikutnya.
        lay=self.page('compare','Perbandingan DES / 3DES','Bandingkan data, kunci, IV, padding, ciphertext dan hasil dekripsi kedua implementasi.')
        # BARIS ASLI 2935: Di compare_page: Menambahkan elemen baru pada daftar hasil atau riwayat.
        box,b=card('Masukan perbandingan');self.process_controls.append(box);self.algorithm_selector(b);row=QHBoxLayout();self.compare_path=text('Vektor contoh satu blok (default)','muted');row.addWidget(self.compare_path,1);row.addWidget(button('Pilih plaintext',self.choose_compare,symbol='file'));row.addWidget(button('Tulis plaintext',lambda:self.plaintext_dialog('compare')));row.addWidget(button('Vektor contoh',self.use_vector));b.addLayout(row)
        # BARIS ASLI 2936: Di compare_page: Menambahkan elemen baru pada daftar hasil atau riwayat.
        self.compare_file=None;self.compare_text=None;self.compare_key=field(KUNCI_CONTOH,True);self.keys.append(self.compare_key);self.compare_key.textEdited.connect(lambda v:self.sync_keys(v,self.compare_key))
        # BARIS ASLI 2937: Di compare_page: Memasang tata letak antarmuka dan komponennya.
        row=QHBoxLayout();row.addWidget(text('Kunci','fieldLabel'));row.addWidget(self.compare_key,1);row.addWidget(self.track(button('Bandingkan hasil',self.start_compare,'primary','compare')));b.addLayout(row);lay.addWidget(box)
        # BARIS ASLI 2938: Di compare_page: Memasukkan widget/layout ke susunan tampilan.
        self.compare_table=table(['No','Parameter','DES Library','DES Buatan Sendiri','Status']);self.compare_table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents);self.compare_table.setMinimumHeight(310);lay.addWidget(self.compare_table,1)
        # BARIS ASLI 2939: Di compare_page: Memasang tata letak antarmuka dan komponennya.
        banner,self.compare_notice=notice('Pilih masukan lalu jalankan perbandingan.');lay.addWidget(banner)
        # BARIS ASLI 2940: Di compare_page: Memasukkan widget/layout ke susunan tampilan.
        self.compare_detail=QPlainTextEdit();self.compare_detail.setReadOnly(True);self.compare_detail.setMinimumHeight(230);self.compare_detail.setFont(QFont('Consolas',10));lay.addWidget(self.compare_detail)

    # BARIS ASLI 2942: Mendefinisikan fungsi set_compare_plaintext. Fungsi ini menangani aksi khusus dalam aplikasi.
    def set_compare_plaintext(self,value):
        # BARIS ASLI 2943: Di set_compare_plaintext: Memperbarui teks yang terlihat pada elemen antarmuka.
        self.compare_file=None;self.compare_text=value;self.compare_path.setText('Plaintext dari masukan manual')
        # BARIS ASLI 2944: Di set_compare_plaintext: Memperbarui teks yang terlihat pada elemen antarmuka.
        self.compare_table.setRowCount(0);self.compare_detail.clear();self.compare_notice.setText('Plaintext siap. Jalankan perbandingan.')

    # BARIS ASLI 2946: Mendefinisikan fungsi choose_compare. Fungsi ini menangani aksi khusus dalam aplikasi.
    def choose_compare(self):
        # BARIS ASLI 2947: Di choose_compare: Menampilkan dialog untuk memilih lokasi file input/output.
        name,_=QFileDialog.getOpenFileName(self,'Pilih file plaintext','','Teks (*.txt)')
        # BARIS ASLI 2948: Di choose_compare: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if name:self.compare_text=None;self.compare_file=Path(name);self.compare_path.setText(Path(name).name);self.compare_table.setRowCount(0);self.compare_notice.setText('File dipilih. Jalankan perbandingan dengan kunci yang sama.')

    # BARIS ASLI 2950: Mendefinisikan fungsi use_vector. Fungsi ini menangani aksi khusus dalam aplikasi.
    def use_vector(self):
        # BARIS ASLI 2951: Di use_vector: Memperbarui teks yang terlihat pada elemen antarmuka.
        self.compare_file=None;self.compare_text=None;self.compare_path.setText('Vektor contoh satu blok (default)');self.set_keys(self.example_key());self.compare_table.setRowCount(0)

    # BARIS ASLI 2953: Mendefinisikan fungsi start_compare. Fungsi ini menangani aksi khusus dalam aplikasi.
    def start_compare(self):
        # BARIS ASLI 2954: Di start_compare: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if self.busy():return
        # BARIS ASLI 2955: Di start_compare: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:
            # BARIS ASLI 2956: Di start_compare: Menghitung/menyiapkan nilai algorithm untuk dipakai oleh proses berikutnya.
            algorithm=self.algorithm;key=self.read_key(self.compare_key);source=self.compare_file;compare_text=self.compare_text;is_message=source is not None or compare_text is not None
            # BARIS ASLI 2957: Mendefinisikan fungsi work. Fungsi ini menangani aksi khusus dalam aplikasi.
            def work():
                # BARIS ASLI 2958: Di work: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: is_message.
                if is_message:
                    # BARIS ASLI 2959: Di work: Mendekode teks heksadesimal menjadi representasi byte.
                    data=compare_text.encode('utf-8') if compare_text is not None else source.read_bytes();record=comparison(data,key,algorithm);mode='CBC + PKCS#7';iv=record['iv_hex'];ct=bytes.fromhex(record['ciphertext_hex']);n=len(pad(data))
                    # BARIS ASLI 2960: Di work: Mendekode teks heksadesimal menjadi representasi byte.
                    cm=encrypt_bytes(data,key,'manual',bytes.fromhex(iv),algorithm);cl=record
                    # BARIS ASLI 2961: Di work: Memulihkan plaintext berdasarkan metadata ciphertext dan kunci.
                    pm=decrypt_record(cl,key,'manual');pl=decrypt_record(cm,key,'library');caption=source.name if source else 'Plaintext manual'
                # BARIS ASLI 2962: Di work: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
                else:
                    # BARIS ASLI 2963: Di work: Mendekode teks heksadesimal menjadi representasi byte.
                    data=bytes.fromhex('0123456789ABCDEF');module=DES if algorithm=='DES' else DES3;engine=DESManual(key) if algorithm=='DES' else TripleDESManual(key);ct=module.new(key,module.MODE_ECB).encrypt(data);manual=engine.encrypt_block(data);verify(ct==manual,'Ciphertext berbeda.');pm=engine.decrypt_block(ct);pl=module.new(key,module.MODE_ECB).decrypt(manual);mode='ECB / satu blok';iv='Tidak digunakan';n=len(data);caption='Vektor '+algorithm+' satu blok'
                # BARIS ASLI 2964: Di work: Memeriksa bahwa hasil nyata cocok dengan nilai/ketentuan pengujian.
                verify(pm==pl==data,'Plaintext hasil dekripsi berbeda.')
                # BARIS ASLI 2965: Di work: Mendekode teks heksadesimal menjadi representasi byte.
                manual_ct=bytes.fromhex(cm['ciphertext_hex']) if is_message else manual
                # BARIS ASLI 2966: Di work: Memeriksa bahwa hasil nyata cocok dengan nilai/ketentuan pengujian.
                verify(manual_ct==ct,'Ciphertext manual berbeda dari library.')
                # BARIS ASLI 2967: Di work: Menghitung/menyiapkan nilai values untuk dipakai oleh proses berikutnya.
                values=[('Algoritma',algorithm),('Kunci (HEX)',key.hex().upper()),('Plaintext (HEX)',data.hex().upper()),('Mode',mode),('IV',iv),('Data diproses',f'{n} byte'),('Ciphertext (HEX)',ct.hex().upper()),('Hasil dekripsi (HEX)',pm.hex().upper())]
                # BARIS ASLI 2968: Di work: Menghitung/menyiapkan nilai pairs untuk dipakai oleh proses berikutnya.
                pairs=[(name,value,manual_ct.hex().upper() if name=='Ciphertext (HEX)' else pl.hex().upper() if name=='Hasil dekripsi (HEX)' else value) for name,value in values]
                # BARIS ASLI 2969: Di work: Menghitung/menyiapkan nilai rows untuk dipakai oleh proses berikutnya.
                rows=[(i,name,left[:48]+('...' if len(left)>48 else ''),right[:48]+('...' if len(right)>48 else ''),'Sama' if left==right else 'Berbeda') for i,(name,left,right) in enumerate(pairs,1)]
                # BARIS ASLI 2970: Di work: Menghitung/menyiapkan nilai detail untuk dipakai oleh proses berikutnya.
                detail=('Masukan: '+caption+'\nCiphertext manual = library: SAMA\nDekripsi silang: BERHASIL\nPlaintext identik dengan masukan (byte demi byte): YA\n\n'+message_summary(len(data),padding_used=is_message)+'\n\nPLAINTEXT ASLI:\n'+data.decode('utf-8',errors='replace')+'\n\nHASIL DEKRIPSI MANUAL:\n'+pm.decode('utf-8',errors='replace')+'\n\nHASIL DEKRIPSI LIBRARY:\n'+pl.decode('utf-8',errors='replace')+'\n\nCIPHERTEXT LENGKAP (HEX):\n'+ct.hex().upper())
                # BARIS ASLI 2971: Di work: Mengembalikan nilai perhitungan ke pemanggil: {'rows':rows,'detail':detail,'source':caption,'n':len(data)}.
                return {'rows':rows,'detail':detail,'source':caption,'n':len(data)}
            # BARIS ASLI 2972: Di start_compare: Menjalankan langkah self.launch('compare',work) sebagai bagian dari alur fungsi ini.
            self.launch('compare',work)
        # BARIS ASLI 2973: Di start_compare: Menangani kesalahan ValueError as excself.error(str(exc)).
        except ValueError as exc:self.error(str(exc))

    # BARIS ASLI 2975: Mendefinisikan fungsi rounds_page. Fungsi ini menangani aksi khusus dalam aplikasi.
    def rounds_page(self):
        # BARIS ASLI 2976: Di rounds_page: Menghitung/menyiapkan nilai lay untuk dipakai oleh proses berikutnya.
        lay=self.page('rounds','Jejak Feistel','Inti DES / 3DES per blok, sebelum penggabungan mode CBC. Pilih masukan lalu hitung ulang.')
        # BARIS ASLI 2977: Di rounds_page: Menambahkan elemen baru pada daftar hasil atau riwayat.
        box,b=card('Masukan Jejak');self.algorithm_selector(b);self.trace_key=field(KUNCI_CONTOH,True);self.keys.append(self.trace_key);self.trace_key.textEdited.connect(lambda v:self.sync_keys(v,self.trace_key));b.addWidget(text('Kunci','fieldLabel'));b.addWidget(self.trace_key);self.trace_input=QPlainTextEdit('cryptography');self.trace_input.setMaximumHeight(90);b.addWidget(self.trace_input);row=QHBoxLayout();row.addWidget(button('Buka plaintext TXT',self.choose_trace_file));self.trace_block=QSpinBox();self.trace_block.setRange(1,100000000);row.addWidget(text('Nomor blok','fieldLabel'));row.addWidget(self.trace_block);row.addWidget(button('Hitung jejak',self.calculate_trace));b.addLayout(row);self.trace_stage=QComboBox();self.trace_stage.currentIndexChanged.connect(self.change_trace_stage);b.addWidget(self.trace_stage);self.trace_note=text('Vektor contoh DES; klik Hitung jejak untuk masukan baru.','muted');b.addWidget(self.trace_note);lay.addWidget(box);self.process_controls.append(box);self.trace_file=None;self.trace_input.textChanged.connect(self.trace_text_changed);self.trace_stages=[]
        # BARIS ASLI 2978: Di rounds_page: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        select,s=card('Pilih Ronde');grid=QGridLayout();group=QButtonGroup(self);group.setExclusive(True);self.round_buttons=[]
        # BARIS ASLI 2979: Di rounds_page: Melakukan iterasi pada elemen/urutan: i in range(1,17).
        for i in range(1,17):
            # BARIS ASLI 2980: Di rounds_page: Menambahkan elemen baru pada daftar hasil atau riwayat.
            b=button('R'+str(i),lambda checked=False,n=i:self.select_round(n));b.setObjectName('round');b.setCheckable(True);group.addButton(b);grid.addWidget(b,(i-1)//8,(i-1)%8);self.round_buttons.append(b)
        # BARIS ASLI 2981: Di rounds_page: Memasang tata letak antarmuka dan komponennya.
        s.addLayout(grid);lay.addWidget(select)
        # BARIS ASLI 2982: Di rounds_page: Mendekode teks heksadesimal menjadi representasi byte.
        self.trace=[];DESManual(bytes.fromhex(KUNCI_CONTOH)).encrypt_block(bytes.fromhex('0123456789ABCDEF'),self.trace)
        # BARIS ASLI 2983: Di rounds_page: Menghitung/menyiapkan nilai panels untuk dipakai oleh proses berikutnya.
        panels=QHBoxLayout();detail,d=card('Detail Ronde 1');self.round_title=d.itemAt(0).widget();self.round_fields={};form=QGridLayout()
        # BARIS ASLI 2984: Di rounds_page: Melakukan iterasi pada elemen/urutan: i,title in enumerate(['L sebelumnya','R sebelumnya','Subkunci (48 bit)','F(R, K....
        for i,title in enumerate(['L sebelumnya','R sebelumnya','Subkunci (48 bit)','F(R, K)','L sesudah','R sesudah']):
            # BARIS ASLI 2985: Di rounds_page: Memasang tata letak antarmuka dan komponennya.
            name=text(title,'fieldLabel');value=field('',True);value.setReadOnly(True);form.addWidget(name,(i//2)*2,i%2);form.addWidget(value,(i//2)*2+1,i%2);self.round_fields[title]=value
        # BARIS ASLI 2986: Di rounds_page: Memasang tata letak antarmuka dan komponennya.
        d.addLayout(form);panels.addWidget(detail,3)
        # BARIS ASLI 2987: Di rounds_page: Memasang tata letak antarmuka dan komponennya.
        diagram,c=card('Proses Feistel');self.round_diagram=RoundDiagram();c.addWidget(self.round_diagram,1);panels.addWidget(diagram,2)
        # BARIS ASLI 2988: Di rounds_page: Menghitung/menyiapkan nilai summary,c untuk dipakai oleh proses berikutnya.
        summary,c=card('Ringkasan')
        # BARIS ASLI 2989: Di rounds_page: Melakukan iterasi pada elemen/urutan: heading,value in [('Jumlah ronde','16 ronde'),('Ukuran blok','64 bit'),('Bagian....
        for heading,value in [('Jumlah ronde','16 ronde'),('Ukuran blok','64 bit'),('Bagian L / R','32 bit'),('Kunci efektif','56 bit')]:c.addWidget(text(heading,'fieldLabel'));c.addWidget(text(value,'section'))
        # BARIS ASLI 2990: Di rounds_page: Memasang tata letak antarmuka dan komponennya.
        c.addStretch();panels.addWidget(summary,1);lay.addLayout(panels)
        # BARIS ASLI 2991: Di rounds_page: Memasang tata letak antarmuka dan komponennya.
        desc,self.round_desc=notice('',False);lay.addWidget(desc)
        # BARIS ASLI 2992: Di rounds_page: Memasang tata letak antarmuka dan komponennya.
        xorbox,x=card('Pembuktian XOR');self.xor_note=text('','section');x.addWidget(self.xor_note)
        # BARIS ASLI 2993: Di rounds_page: Memasukkan widget/layout ke susunan tampilan.
        self.xor_binary=QPlainTextEdit();self.xor_binary.setReadOnly(True);self.xor_binary.setFont(QFont('Consolas',10));self.xor_binary.setFixedHeight(94);x.addWidget(self.xor_binary)
        # BARIS ASLI 2994: Di rounds_page: Memakai operasi bit AND/OR untuk menyeleksi atau menggabungkan bit.
        x.addWidget(text('Tabel kebenaran: 0 ⊕ 0 = 0   |   0 ⊕ 1 = 1   |   1 ⊕ 0 = 1   |   1 ⊕ 1 = 0','muted'))
        # BARIS ASLI 2995: Di rounds_page: Memasukkan widget/layout ke susunan tampilan.
        self.xor_table=table(['Ronde','L sebelumnya','F(R, K)','L ⊕ F','R sesudah','Cek']);self.xor_table.setMinimumHeight(320);x.addWidget(self.xor_table);lay.addWidget(xorbox);self.select_round(1)

    # BARIS ASLI 2997: Mendefinisikan fungsi trace_text_changed. Fungsi ini menangani aksi khusus dalam aplikasi.
    def trace_text_changed(self):
        # BARIS ASLI 2998: Di trace_text_changed: Menghitung/menyiapkan nilai self.trace_file untuk dipakai oleh proses berikutnya.
        self.trace_file=None

    # BARIS ASLI 3000: Mendefinisikan fungsi choose_trace_file. Fungsi ini menangani aksi khusus dalam aplikasi.
    def choose_trace_file(self):
        # BARIS ASLI 3001: Di choose_trace_file: Menampilkan dialog untuk memilih lokasi file input/output.
        name,_=QFileDialog.getOpenFileName(self,'Pilih plaintext untuk jejak','','Teks (*.txt)')
        # BARIS ASLI 3002: Di choose_trace_file: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: not name:return.
        if not name:return
        # BARIS ASLI 3003: Di choose_trace_file: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:
            # BARIS ASLI 3004: Di choose_trace_file: Membaca seluruh konten file sebagai byte/teks.
            data=Path(name).read_bytes();self.trace_input.setPlainText(data.decode('utf-8',errors='replace'));self.trace_file=data;self.trace_note.setText(Path(name).name+' dipilih. Klik Hitung jejak.')
        # BARIS ASLI 3005: Di choose_trace_file: Menangani kesalahan OSError as excself.error(str(exc)).
        except OSError as exc:self.error(str(exc))

    # BARIS ASLI 3007: Mendefinisikan fungsi calculate_trace. Fungsi ini menangani aksi khusus dalam aplikasi.
    def calculate_trace(self):
        # BARIS ASLI 3008: Di calculate_trace: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:
            # BARIS ASLI 3009: Di calculate_trace: Menghitung/menyiapkan nilai data untuk dipakai oleh proses berikutnya.
            data=self.trace_file if self.trace_file is not None else self.trace_input.toPlainText().encode('utf-8');padded=pad(data);count=len(padded)//8;index=self.trace_block.value()
            # BARIS ASLI 3010: Di calculate_trace: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: index>count:raise ValueError(f'Nomor blok harus antara 1 dan {count}.').
            if index>count:raise ValueError(f'Nomor blok harus antara 1 dan {count}.')
            # BARIS ASLI 3011: Di calculate_trace: Menghitung/menyiapkan nilai key untuk dipakai oleh proses berikutnya.
            key=self.read_key(self.trace_key)
            if self.algorithm=='3DES' and len(key)==16:key=key+key[:8]  # Jejak 2-key 3DES tetap memiliki tiga tahap EDE.
            incoming=padded[(index-1)*8:index*8];stages=[];block=incoming
            # BARIS ASLI 3012: Di calculate_trace: Melakukan iterasi pada elemen/urutan: title,k,dec in ([('DES E(K)',key,False)] if self.algorithm=='DES' else [('Tahap....
            for title,k,dec in ([('DES E(K)',key,False)] if self.algorithm=='DES' else [('Tahap 1 · E(K1)',key[:8],False),('Tahap 2 · D(K2)',key[8:16],True),('Tahap 3 · E(K3)',key[16:],False)]):
                # BARIS ASLI 3013: Di calculate_trace: Mengenkripsi satu blok 8 byte menggunakan mesin DES/3DES manual.
                trace=[];engine=DESManual(k);out=engine.decrypt_block(block,trace) if dec else engine.encrypt_block(block,trace);stages.append((title,trace,block,out));block=out
            # BARIS ASLI 3014: Di calculate_trace: Mengenkripsi satu blok 8 byte menggunakan mesin DES/3DES manual.
            expected=(DESManual(key) if self.algorithm=='DES' else TripleDESManual(key)).encrypt_block(incoming);verify(block==expected,'Jejak tidak cocok dengan inti algoritma.')
            # BARIS ASLI 3015: Di calculate_trace: Menghitung/menyiapkan nilai self.trace_stages untuk dipakai oleh proses berikutnya.
            self.trace_stages=stages;self.trace_stage.blockSignals(True);self.trace_stage.clear();self.trace_stage.addItems([x[0] for x in stages]);self.trace_stage.blockSignals(False);self.change_trace_stage(0)
            # BARIS ASLI 3016: Di calculate_trace: Memperbarui teks yang terlihat pada elemen antarmuka.
            self.trace_note.setText(f'{self.algorithm} | Blok {index}/{count} | Plaintext blok: {incoming.hex().upper()} | Hasil inti: {block.hex().upper()}')
        # BARIS ASLI 3017: Di calculate_trace: Menangani kesalahan (ValueError,OSError) as excself.error(str(exc)).
        except (ValueError,OSError) as exc:self.error(str(exc))

    # BARIS ASLI 3019: Mendefinisikan fungsi change_trace_stage. Fungsi ini menangani aksi khusus dalam aplikasi.
    def change_trace_stage(self,index):
        # BARIS ASLI 3020: Di change_trace_stage: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
        if 0<=index<len(self.trace_stages):self.trace=self.trace_stages[index][1];self.select_round(1)

    # BARIS ASLI 3022: Mendefinisikan fungsi select_round. Fungsi ini menangani aksi khusus dalam aplikasi.
    def select_round(self,n):
        # BARIS ASLI 3023: Di select_round: Memanggil fungsi Feistel F(R,K) untuk menghitung komponen ronde DES.
        before=self.trace[n-1];after=self.trace[n];key=int(after['K'],16);f=round_function(int(before['R'],16),key)
        # BARIS ASLI 3024: Di select_round: Menghitung/menyiapkan nilai values untuk dipakai oleh proses berikutnya.
        values=[before['L'],before['R'],after['K'],f'{f:08X}',after['L'],after['R']]
        # BARIS ASLI 3025: Di select_round: Melakukan iterasi pada elemen/urutan: w,value in zip(self.round_fields.values(),values):w.setText(value).
        for w,value in zip(self.round_fields.values(),values):w.setText(value)
        # BARIS ASLI 3026: Di select_round: Memperbarui teks yang terlihat pada elemen antarmuka.
        self.round_title.setText('Detail Ronde '+str(n));self.round_buttons[n-1].setChecked(True);self.round_diagram.n=n;self.round_diagram.update()
        # BARIS ASLI 3027: Di select_round: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        left=int(before['L'],16);right=int(after['R'],16);self.xor_note.setText(f'Ronde {n}: {left:08X} ⊕ {f:08X} = {right:08X} (HEX)')
        # BARIS ASLI 3028: Di select_round: Memperbarui teks yang terlihat pada elemen antarmuka.
        self.xor_binary.setPlainText(f'L sebelumnya  {left:032b}\nF(R, K)       {f:032b}\n              '+('─'*32)+f'\nHasil XOR     {(left^f):032b}')
        # BARIS ASLI 3029: Di select_round: Menghitung/menyiapkan nilai rows untuk dipakai oleh proses berikutnya.
        rows=[]
        # BARIS ASLI 3030: Di select_round: Menelusuri data per blok agar tiap iterasi memproses ukuran yang sesuai.
        for i in range(1,len(self.trace)):
            # BARIS ASLI 3031: Di select_round: Memanggil fungsi Feistel F(R,K) untuk menghitung komponen ronde DES.
            prev,cur=self.trace[i-1],self.trace[i];fv=round_function(int(prev['R'],16),int(cur['K'],16));lv=int(prev['L'],16);rv=int(cur['R'],16)
            # BARIS ASLI 3032: Di select_round: Menambahkan elemen baru pada daftar hasil atau riwayat.
            rows.append((i,prev['L'],f'{fv:08X}',f'{lv^fv:08X}',cur['R'],'Sama' if lv^fv==rv else 'Berbeda'))
        # BARIS ASLI 3033: Di select_round: Menjalankan langkah fill_table(self.xor_table,rows) sebagai bagian dari alur fungsi ini.
        fill_table(self.xor_table,rows)
        # BARIS ASLI 3034: Di select_round: Memperbarui teks yang terlihat pada elemen antarmuka.
        self.round_desc.setText(f'Ronde {n}: L baru = R lama; R baru = L lama XOR F(R lama, K{n}). F memakai ekspansi, XOR subkunci, S-box dan permutasi P.')

    # BARIS ASLI 3036: Mendefinisikan fungsi history_page. Fungsi ini menangani aksi khusus dalam aplikasi.
    def history_page(self):
        # BARIS ASLI 3037: Di history_page: Menghitung/menyiapkan nilai lay untuk dipakai oleh proses berikutnya.
        lay=self.page('history','Riwayat','Aktivitas sesi berjalan. Kunci dan isi plaintext tidak dicatat dalam riwayat.')
        # BARIS ASLI 3038: Di history_page: Memasukkan widget/layout ke susunan tampilan.
        self.history_table=table(['Waktu','Aktivitas','Implementasi','Masukan','Keluaran / status']);self.history_table.setMinimumHeight(370);lay.addWidget(self.history_table,1)
        # BARIS ASLI 3039: Di history_page: Memasang tata letak antarmuka dan komponennya.
        row=QHBoxLayout();row.addWidget(button('Simpan riwayat .txt',self.export_history,symbol='save'));row.addStretch();row.addWidget(button('Hapus riwayat',self.clear_history));lay.addLayout(row)
        # BARIS ASLI 3040: Di history_page: Memasang tata letak antarmuka dan komponennya.
        lay.addWidget(text('Riwayat berada dalam memori dan hilang saat aplikasi ditutup.','muted'))

    # BARIS ASLI 3042: Mendefinisikan fungsi add_history. Fungsi ini menangani aksi khusus dalam aplikasi.
    def add_history(self,operation,backend,source,output='',length=0):
        # BARIS ASLI 3043: Di add_history: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if not self.keep_history:return
        # BARIS ASLI 3044: Di add_history: Menambahkan elemen baru pada daftar hasil atau riwayat.
        self.history.append((datetime.now().strftime('%H:%M:%S'),operation,backend,source,output or 'Berhasil'))
        # BARIS ASLI 3045: Di add_history: Menjalankan langkah fill_table(self.history_table,self.history) sebagai bagian dari alur fungsi ini.
        fill_table(self.history_table,self.history)

    # BARIS ASLI 3047: Mendefinisikan fungsi clear_history. Fungsi ini menangani aksi khusus dalam aplikasi.
    def clear_history(self):
        # BARIS ASLI 3048: Di clear_history: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if QMessageBox.question(self,'Hapus riwayat','Hapus riwayat sesi ini?')==QMessageBox.Yes:self.history.clear();self.history_table.setRowCount(0)

    # BARIS ASLI 3050: Mendefinisikan fungsi export_history. Fungsi ini menangani aksi khusus dalam aplikasi.
    def export_history(self):
        # BARIS ASLI 3051: Di export_history: Menampilkan dialog untuk memilih lokasi file input/output.
        name,_=QFileDialog.getSaveFileName(self,'Simpan riwayat sesi','riwayat_ZarCryptoDES.txt','Teks (*.txt)')
        # BARIS ASLI 3052: Di export_history: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: name.
        if name:
            # BARIS ASLI 3053: Di export_history: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
            try:Path(name).with_suffix('.txt').write_text('RIWAYAT ZARCRYPTODES\n'+'\n'.join(' | '.join(row) for row in self.history)+'\n',encoding='utf-8');self.status.setText('Riwayat berhasil disimpan.')
            # BARIS ASLI 3054: Di export_history: Menangani kesalahan OSError as excself.error(str(exc)).
            except OSError as exc:self.error(str(exc))

    # BARIS ASLI 3056: Mendefinisikan fungsi busy. Fungsi ini menangani aksi khusus dalam aplikasi.
    def busy(self):return self.worker is not None

    # BARIS ASLI 3058: Mendefinisikan fungsi launch. Fungsi ini menangani aksi khusus dalam aplikasi.
    def launch(self,kind,fn):
        # BARIS ASLI 3059: Di launch: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if self.busy():return
        # BARIS ASLI 3060: Di launch: Melakukan iterasi pada elemen/urutan: b in self.job_buttons:b.setEnabled(False).
        for b in self.job_buttons:b.setEnabled(False)
        # BARIS ASLI 3061: Di launch: Melakukan iterasi pada elemen/urutan: control in self.process_controls:control.setEnabled(False).
        for control in self.process_controls:control.setEnabled(False)
        # BARIS ASLI 3062: Di launch: Memperbarui teks yang terlihat pada elemen antarmuka.
        self.progress.setRange(0,0);self.status.setText('Memproses... tunggu hingga selesai.')
        # BARIS ASLI 3063: Di launch: Menghubungkan sinyal/kejadian GUI dengan fungsi callback.
        self.worker=Worker(kind,fn);self.worker.completed.connect(self.finished);self.worker.failed.connect(self.job_failed)
        # BARIS ASLI 3064: Di launch: Menghubungkan sinyal/kejadian GUI dengan fungsi callback.
        self.worker.finished.connect(self.cleanup_worker);self.worker.start()

    # BARIS ASLI 3066: Mendefinisikan fungsi cleanup_worker. Fungsi ini menangani aksi khusus dalam aplikasi.
    def cleanup_worker(self):
        # BARIS ASLI 3067: Di cleanup_worker: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if self.worker:self.worker.deleteLater();self.worker=None
        # BARIS ASLI 3068: Di cleanup_worker: Melakukan iterasi pada elemen/urutan: b in self.job_buttons:b.setEnabled(True).
        for b in self.job_buttons:b.setEnabled(True)
        # BARIS ASLI 3069: Di cleanup_worker: Melakukan iterasi pada elemen/urutan: control in self.process_controls:control.setEnabled(True).
        for control in self.process_controls:control.setEnabled(True)
        # BARIS ASLI 3070: Di cleanup_worker: Mengatur properti komponen GUI yang digunakan.
        self.progress.setRange(0,1);self.progress.setValue(0)

    # BARIS ASLI 3072: Mendefinisikan fungsi finished. Fungsi ini menangani aksi khusus dalam aplikasi.
    def finished(self,kind,result):
        # BARIS ASLI 3073: Di finished: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: kind in ('encrypt','decrypt').
        if kind in ('encrypt','decrypt'):
            # BARIS ASLI 3074: Di finished: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state=self.file_states[kind];state['payload']=result['payload'];state['result_source']=result['source'];state['result_backend']=result['algorithm']+' / '+result['backend'];state['save'].setEnabled(True)
            # BARIS ASLI 3075: Di finished: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            preview=result['preview'];state['output'].setPlainText(preview[:16000]+('\n[Pratinjau dipotong; hasil tersimpan lengkap]' if len(preview)>16000 else ''))
            # BARIS ASLI 3076: Di finished: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state['stats'].setText(result['summary']+('' if result['verification'] is None else '\nVerifikasi file asli (byte demi byte): '+('IDENTIK' if result['verification'] else 'BERBEDA — hasil tidak sama dengan file pembanding.')))
            # BARIS ASLI 3077: Di finished: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            state['state'].setText('Berhasil. Simpan hasil.')
            # BARIS ASLI 3078: Di finished: Memeriksa jenis format atau mode penyimpanan data.
            if result['verification'] is False:state['state'].setText('VERIFIKASI BERBEDA: hasil tidak identik dengan plaintext pembanding. Periksa kunci, format, dan file asli.')
            # BARIS ASLI 3079: Di finished: Memperbarui teks yang terlihat pada elemen antarmuka.
            self.status.setText('Proses selesai. Hasil belum disimpan; pilih tombol Simpan.');self.add_history('Enkripsi' if kind=='encrypt' else 'Dekripsi',result['algorithm']+' / '+result['backend'],result['source'].name,'Selesai, belum disimpan')
        # BARIS ASLI 3080: Di finished: Menguji kondisi alternatif: kind=='test'.
        elif kind=='test':
            # BARIS ASLI 3081: Di finished: Memperbarui teks yang terlihat pada elemen antarmuka.
            self.test_result_labels[0].setText(result['library']);self.test_result_labels[1].setText(result['manual']);self.test_result_labels[2].setText('Hasil identik!' if result['expected_match'] is not False else 'Identik antarimplementasi; berbeda dari acuan')
            # BARIS ASLI 3082: Di finished: Memperbarui teks yang terlihat pada elemen antarmuka.
            self.test_result_notes[0].setText('ECB satu blok tanpa padding.');self.test_result_notes[1].setText('DES lengkap dengan 16 ronde.' if result['algorithm']=='DES' else '3DES EDE: tiga tahap DES manual, masing-masing 16 ronde.')
            # BARIS ASLI 3083: Di finished: Memperbarui teks yang terlihat pada elemen antarmuka.
            self.test_result_notes[2].setText('Cocok dengan library dan acuan.' if result['expected_match'] is True else 'Acuan tidak diisi.' if result['expected_match'] is None else 'Nilai acuan berbeda dari hasil enkripsi.')
            # BARIS ASLI 3084: Di finished: Menerapkan gaya dan warna pada elemen antarmuka.
            self.test_result_labels[2].setStyleSheet('color:'+('#AD7525' if result['expected_match'] is False else GREEN)+'; font-weight:650;')
            # BARIS ASLI 3085: Di finished: Menghitung/menyiapkan nilai custom untuk dipakai oleh proses berikutnya.
            custom=f'VEKTOR PADA FORM\nPlaintext: {result["plaintext"]}\n{result["algorithm"]} library: {result["library"]}\n{result["algorithm"]} manual: {result["manual"]}\nSesuai acuan: '+('Tidak diisi' if result['expected_match'] is None else str(result['expected_match']))+'\n\n'
            # BARIS ASLI 3086: Di finished: Memperbarui teks yang terlihat pada elemen antarmuka.
            self.last_test=custom+result['log'];self.test_log.setPlainText(self.last_test);self.status.setText(f'Uji {result["algorithm"]} selesai. Kedua implementasi cocok; pengujian tambahan lulus.');self.add_history('Uji '+result['algorithm'],'library + manual','Vektor / CBC / file','Cocok library, beda acuan' if result['expected_match'] is False else 'LULUS')
        # BARIS ASLI 3087: Di finished: Menguji kondisi alternatif: kind=='compare'.
        elif kind=='compare':
            # BARIS ASLI 3088: Di finished: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            fill_table(self.compare_table,result['rows']);self.compare_detail.setPlainText(result['detail']);self.compare_notice.setText('Hasil identik! Ciphertext sama dan dekripsi silang memulihkan byte asli.');self.status.setText('Perbandingan lulus.');self.add_history('Perbandingan','library + manual',result['source'],'Sama')

    # BARIS ASLI 3090: Mendefinisikan fungsi job_failed. Fungsi ini menangani aksi khusus dalam aplikasi.
    def job_failed(self,message):
        # BARIS ASLI 3091: Di job_failed: Memperbarui teks yang terlihat pada elemen antarmuka.
        self.status.setText('Proses gagal. Periksa masukan dan kunci.')
        # BARIS ASLI 3092: Di job_failed: Melakukan iterasi pada elemen/urutan: state in self.file_states.values().
        for state in self.file_states.values():
            # BARIS ASLI 3093: Di job_failed: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: state['payload'] is None:state['state'].setText('Proses belum berhasil. Periksa....
            if state['payload'] is None:state['state'].setText('Proses belum berhasil. Periksa file dan kunci.')
        # BARIS ASLI 3094: Di job_failed: Menjalankan langkah self.error(message) sebagai bagian dari alur fungsi ini.
        self.error(message)

    # BARIS ASLI 3096: Mendefinisikan fungsi error. Fungsi ini menangani aksi khusus dalam aplikasi.
    def error(self,message):QMessageBox.warning(self,'ZarCryptoDES',message)

    # BARIS ASLI 3098: Mendefinisikan fungsi closeEvent. Fungsi ini menangani aksi khusus dalam aplikasi.
    def closeEvent(self,event):
        # BARIS ASLI 3099: Di closeEvent: Menentukan perubahan tampilan atau aksi berdasarkan status GUI.
        if self.busy():
            # BARIS ASLI 3100: Di closeEvent: Menampilkan pesan dialog informasi, peringatan, atau kegagalan.
            QMessageBox.information(self,'Proses berjalan','Tunggu proses selesai sebelum menutup aplikasi.');event.ignore()
        # BARIS ASLI 3101: Di closeEvent: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
        else:event.accept()
