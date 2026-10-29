# -*- coding: utf-8 -*-
"""Modul widgets untuk ZarCryptoDES."""

import base64
from assets import LOGO_B64
from qt_compat import QBrush, QColor, QFont, QFrame, QHBoxLayout, QHeaderView, QIcon, QImage, QLabel, QLineEdit, QLinearGradient, QPainter, QPainterPath, QPen, QPixmap, QPointF, QPushButton, QRectF, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, Qt
from theme import GREEN, NAVY

# BARIS ASLI 2484: Mendefinisikan fungsi dragon_image. Membangun gambar/logo yang akan ditampilkan pada antarmuka.
def dragon_image(color=NAVY):
    # BARIS ASLI 2485: Di dragon_image: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
    """Render logo pengguna dengan warna tema; bentuk asli dipertahankan."""
    # BARIS ASLI 2486: Di dragon_image: Menghitung/menyiapkan nilai original untuk dipakai oleh proses berikutnya.
    original=QImage.fromData(base64.b64decode(LOGO_B64))
    # BARIS ASLI 2487: Di dragon_image: Menghitung/menyiapkan nilai original untuk dipakai oleh proses berikutnya.
    original=original.scaled(260,350,Qt.KeepAspectRatio,Qt.SmoothTransformation)
    # BARIS ASLI 2488: Di dragon_image: Menghitung/menyiapkan nilai alpha untuk dipakai oleh proses berikutnya.
    alpha=original.convertToFormat(QImage.Format_Grayscale8)
    # BARIS ASLI 2489: Di dragon_image: Menjalankan langkah alpha.invertPixels() sebagai bagian dari alur fungsi ini.
    alpha.invertPixels()
    # BARIS ASLI 2490: Di dragon_image: Menghitung/menyiapkan nilai tinted untuk dipakai oleh proses berikutnya.
    tinted=QImage(original.size(),QImage.Format_ARGB32)
    # BARIS ASLI 2491: Di dragon_image: Menyiapkan nilai warna yang digunakan antarmuka.
    tinted.fill(QColor(color));tinted.setAlphaChannel(alpha)
    # BARIS ASLI 2492: Di dragon_image: Mengembalikan nilai perhitungan ke pemanggil: QPixmap.fromImage(tinted).
    return QPixmap.fromImage(tinted)


# BARIS ASLI 2495: Mendefinisikan fungsi icon. Menggambar ikon antarmuka dengan perintah QPainter.
def icon(name,color='#5E7FA7',size=24):
    # BARIS ASLI 2496: Di icon: Menghitung/menyiapkan nilai pix untuk dipakai oleh proses berikutnya.
    pix=QPixmap(size,size);pix.fill(Qt.transparent)
    # BARIS ASLI 2497: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
    p=QPainter(pix);p.setRenderHint(QPainter.Antialiasing)
    # BARIS ASLI 2498: Di icon: Mengatur pena/kuas untuk pewarnaan komponen visual.
    p.scale(size/24,size/24);p.setPen(QPen(QColor(color),1.65,Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin))
    # BARIS ASLI 2499: Di icon: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: name=='home'.
    if name=='home':
        # BARIS ASLI 2500: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        path=QPainterPath();path.moveTo(3,11);path.lineTo(12,3);path.lineTo(21,11);p.drawPath(path)
        # BARIS ASLI 2501: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.drawRoundedRect(QRectF(6,10,12,11),1,1);p.drawRect(QRectF(10,15,4,6))
    # BARIS ASLI 2502: Di icon: Menguji kondisi alternatif: name in ('encrypt','decrypt','file').
    elif name in ('encrypt','decrypt','file'):
        # BARIS ASLI 2503: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        path=QPainterPath();path.moveTo(6,2);path.lineTo(15,2);path.lineTo(20,7);path.lineTo(20,22);path.lineTo(6,22);path.closeSubpath();p.drawPath(path)
        # BARIS ASLI 2504: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.drawLine(15,2,15,7);p.drawLine(15,7,20,7)
        # BARIS ASLI 2505: Di icon: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: name=='file':p.drawLine(9,12,16,12);p.drawLine(9,16,16,16).
        if name=='file':p.drawLine(9,12,16,12);p.drawLine(9,16,16,16)
        # BARIS ASLI 2506: Di icon: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
        else:
            # BARIS ASLI 2507: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
            p.drawRoundedRect(QRectF(9,13,8,6),1,1)
            # BARIS ASLI 2508: Di icon: Menghitung/menyiapkan nilai path untuk dipakai oleh proses berikutnya.
            path=QPainterPath();path.moveTo(11,13);path.lineTo(11,10);path.cubicTo(11,8,15,8,15,10)
            # BARIS ASLI 2509: Di icon: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: name=='encrypt':path.lineTo(15,13).
            if name=='encrypt':path.lineTo(15,13)
            # BARIS ASLI 2510: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
            p.drawPath(path)
    # BARIS ASLI 2511: Di icon: Menguji kondisi alternatif: name in ('test','compare').
    elif name in ('test','compare'):
        # BARIS ASLI 2512: Di icon: Melakukan iterasi pada elemen/urutan: x,y in [(3,4),(14,4),(3,15),(14,15)]:p.drawRoundedRect(QRectF(x,y,7,5),1,1).
        for x,y in [(3,4),(14,4),(3,15),(14,15)]:p.drawRoundedRect(QRectF(x,y,7,5),1,1)
        # BARIS ASLI 2513: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.drawLine(6,9,6,15);p.drawLine(17,9,17,15);p.drawLine(10,6,14,6);p.drawLine(10,17,14,17)
    # BARIS ASLI 2514: Di icon: Menguji kondisi alternatif: name=='rounds'.
    elif name=='rounds':
        # BARIS ASLI 2515: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.drawEllipse(QRectF(4,4,16,16));p.drawLine(12,7,12,12);p.drawLine(12,12,16,12)
    # BARIS ASLI 2516: Di icon: Menguji kondisi alternatif: name=='history'.
    elif name=='history':
        # BARIS ASLI 2517: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.drawArc(QRectF(4,4,16,16),35*16,295*16);p.drawLine(3,8,7,8);p.drawLine(3,8,3,4)
        # BARIS ASLI 2518: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.drawLine(12,7,12,12);p.drawLine(12,12,16,14)
    # BARIS ASLI 2519: Di icon: Menguji kondisi alternatif: name=='check'.
    elif name=='check':
        # BARIS ASLI 2520: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        path=QPainterPath();path.moveTo(5,12);path.lineTo(10,17);path.lineTo(19,7);p.drawPath(path)
    # BARIS ASLI 2521: Di icon: Menguji kondisi alternatif: name=='arrow'.
    elif name=='arrow':
        # BARIS ASLI 2522: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.drawLine(4,12,20,12);p.drawLine(14,6,20,12);p.drawLine(14,18,20,12)
    # BARIS ASLI 2523: Di icon: Menguji kondisi alternatif: name=='key'.
    elif name=='key':
        # BARIS ASLI 2524: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.drawEllipse(QRectF(3,3,8,8));p.drawLine(10,10,20,20);p.drawLine(16,16,19,13);p.drawLine(19,19,22,16)
    # BARIS ASLI 2525: Di icon: Menguji kondisi alternatif: name=='save'.
    elif name=='save':
        # BARIS ASLI 2526: Di icon: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.drawRoundedRect(QRectF(4,3,16,18),1,1);p.drawRect(QRectF(8,3,8,6));p.drawRect(QRectF(8,14,8,7))
    # BARIS ASLI 2527: Di icon: Menjalankan langkah p.end();return QIcon(pix) sebagai bagian dari alur fungsi ini.
    p.end();return QIcon(pix)


# BARIS ASLI 2530: Mendefinisikan fungsi text. Membuat QLabel teks dengan parameter gaya aplikasi.
def text(value='',kind=None):
    # BARIS ASLI 2531: Di text: Menghitung/menyiapkan nilai w untuk dipakai oleh proses berikutnya.
    w=QLabel(value)
    # BARIS ASLI 2532: Di text: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: kind:w.setObjectName(kind).
    if kind:w.setObjectName(kind)
    # BARIS ASLI 2533: Di text: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
    w.setWordWrap(True)
    # BARIS ASLI 2534: Di text: Mengembalikan nilai perhitungan ke pemanggil: w.
    return w


# BARIS ASLI 2537: Mendefinisikan fungsi field. Membuat komponen input dengan pengaturan gaya yang seragam.
def field(value='',mono=False):
    # BARIS ASLI 2538: Di field: Menghitung/menyiapkan nilai w untuk dipakai oleh proses berikutnya.
    w=QLineEdit(value)
    # BARIS ASLI 2539: Di field: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: mono:w.setFont(QFont('Consolas',10)).
    if mono:w.setFont(QFont('Consolas',10))
    # BARIS ASLI 2540: Di field: Mengembalikan nilai perhitungan ke pemanggil: w.
    return w


# BARIS ASLI 2543: Mendefinisikan fungsi button. Membuat tombol GUI dan menghubungkannya dengan aksi.
def button(title,fn=None,kind=None,symbol=None):
    # BARIS ASLI 2544: Di button: Menghitung/menyiapkan nilai w untuk dipakai oleh proses berikutnya.
    w=QPushButton(title)
    # BARIS ASLI 2545: Di button: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: kind:w.setObjectName(kind).
    if kind:w.setObjectName(kind)
    # BARIS ASLI 2546: Di button: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: symbol:w.setIcon(icon(symbol,'white' if kind=='primary' else GREEN if kind=='gr....
    if symbol:w.setIcon(icon(symbol,'white' if kind=='primary' else GREEN if kind=='green' else '#5369ED',19))
    # BARIS ASLI 2547: Di button: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: fn:w.clicked.connect(fn).
    if fn:w.clicked.connect(fn)
    # BARIS ASLI 2548: Di button: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
    w.setCursor(Qt.PointingHandCursor);return w


# BARIS ASLI 2551: Mendefinisikan fungsi card. Membangun panel/kartu tata letak antarmuka.
def card(title=None):
    # BARIS ASLI 2552: Di card: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
    w=QFrame();w.setObjectName('card');layout=QVBoxLayout(w);layout.setContentsMargins(17,16,17,16);layout.setSpacing(11)
    # BARIS ASLI 2553: Di card: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: title:layout.addWidget(text(title,'section')).
    if title:layout.addWidget(text(title,'section'))
    # BARIS ASLI 2554: Di card: Mengembalikan hasil akumulasi pemrosesan.
    return w,layout


# BARIS ASLI 2557: Mendefinisikan fungsi notice. Membuat pesan informasi untuk ditampilkan di GUI.
def notice(message,success=True):
    # BARIS ASLI 2558: Di notice: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
    w=QFrame();w.setStyleSheet('QFrame { background:'+('#E5F8EB' if success else '#EDF1FF')+'; border:1px solid '+('#BDEDD2' if success else '#D6DEFF')+'; border-radius:9px; }')
    # BARIS ASLI 2559: Di notice: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
    row=QHBoxLayout(w);row.setContentsMargins(15,13,15,13)
    # BARIS ASLI 2560: Di notice: Memasang tata letak antarmuka dan komponennya.
    image=QLabel();image.setPixmap(icon('check' if success else 'test',GREEN if success else '#6F7CEE',25).pixmap(25,25));row.addWidget(image)
    # BARIS ASLI 2561: Di notice: Memasang tata letak antarmuka dan komponennya.
    label=text(message);label.setStyleSheet('color:'+('#007854' if success else '#536BBC')+'; border:0; font-size:12px;');row.addWidget(label,1)
    # BARIS ASLI 2562: Di notice: Mengembalikan nilai perhitungan ke pemanggil: w,label.
    return w,label


# BARIS ASLI 2565: Mendefinisikan fungsi table. Membuat tabel GUI untuk hasil uji dan data lain.
def table(headers):
    # BARIS ASLI 2566: Di table: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
    w=QTableWidget(0,len(headers));w.setHorizontalHeaderLabels(headers);w.verticalHeader().hide()
    # BARIS ASLI 2567: Di table: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
    w.setEditTriggers(QTableWidget.NoEditTriggers);w.setSelectionBehavior(QTableWidget.SelectRows)
    # BARIS ASLI 2568: Di table: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
    w.setAlternatingRowColors(True);w.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    # BARIS ASLI 2569: Di table: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
    w.verticalHeader().setDefaultSectionSize(39);return w


# BARIS ASLI 2572: Mendefinisikan fungsi fill_table. Mengisi tabel GUI dengan data baris/kolom.
def fill_table(widget,rows):
    # BARIS ASLI 2573: Di fill_table: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
    widget.setRowCount(len(rows))
    # BARIS ASLI 2574: Di fill_table: Melakukan iterasi pada elemen/urutan: r,row in enumerate(rows).
    for r,row in enumerate(rows):
        # BARIS ASLI 2575: Di fill_table: Melakukan iterasi pada elemen/urutan: c,value in enumerate(row).
        for c,value in enumerate(row):
            # BARIS ASLI 2576: Di fill_table: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
            item=QTableWidgetItem(str(value));widget.setItem(r,c,item)
            # BARIS ASLI 2577: Di fill_table: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
            if c==len(row)-1 and str(value) in ('Sama','LULUS','Pulih'):
                # BARIS ASLI 2578: Di fill_table: Menyiapkan nilai warna yang digunakan antarmuka.
                item.setForeground(QColor(GREEN));item.setBackground(QColor('#E4F7EA'))


# BARIS ASLI 2581: Mendefinisikan kelas HeroBanner. Komponen header atau banner halaman utama.
class HeroBanner(QWidget):
    # BARIS ASLI 2582: Mendefinisikan fungsi __init__. Fungsi ini menangani aksi khusus dalam aplikasi.
    def __init__(self,logo):
        # BARIS ASLI 2583: Di __init__: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        super().__init__();self.logo=logo;self.setMinimumHeight(180)
        # BARIS ASLI 2584: Di __init__: Menetapkan nilai, keadaan, atau properti objek pada aplikasi.
        layout=QHBoxLayout(self);layout.setContentsMargins(24,20,24,20)
        # BARIS ASLI 2585: Di __init__: Memasang tata letak antarmuka dan komponennya.
        left=QVBoxLayout();left.addWidget(text('Selamat Datang di\nZarCryptoDES','title'))
        # BARIS ASLI 2586: Di __init__: Memasang tata letak antarmuka dan komponennya.
        desc=text('Enkripsi dan dekripsi DES / 3DES,\nserta perbandingan implementasi manual dan library.');desc.setStyleSheet('color:#345DA2; font-size:12px;');left.addWidget(desc);left.addStretch()
        # BARIS ASLI 2587: Di __init__: Memasang tata letak antarmuka dan komponennya.
        layout.addLayout(left,3);layout.addStretch(2)
    # BARIS ASLI 2588: Mendefinisikan fungsi paintEvent. Fungsi ini menangani aksi khusus dalam aplikasi.
    def paintEvent(self,event):
        # BARIS ASLI 2589: Di paintEvent: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p=QPainter(self);p.setRenderHint(QPainter.Antialiasing)
        # BARIS ASLI 2590: Di paintEvent: Menyiapkan nilai warna yang digunakan antarmuka.
        gradient=QLinearGradient(0,0,self.width(),0);gradient.setColorAt(0,QColor('#EEF4FC'));gradient.setColorAt(1,QColor('#E0E5FF'))
        # BARIS ASLI 2591: Di paintEvent: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.setBrush(QBrush(gradient));p.setPen(Qt.NoPen);p.drawRoundedRect(self.rect(),10,10)
        # BARIS ASLI 2592: Di paintEvent: Mengatur pena/kuas untuk pewarnaan komponen visual.
        p.setPen(QPen(QColor('#C8D3FC'),1.3))
        # BARIS ASLI 2593: Di paintEvent: Menghitung/menyiapkan nilai x untuk dipakai oleh proses berikutnya.
        x=self.width()-190;y=self.height()/2
        # BARIS ASLI 2594: Di paintEvent: Melakukan iterasi pada elemen/urutan: dx,dy in [(-90,-30),(-55,40),(65,-45),(95,35),(-100,5),(35,65),(30,-65)].
        for dx,dy in [(-90,-30),(-55,40),(65,-45),(95,35),(-100,5),(35,65),(30,-65)]:
            # BARIS ASLI 2595: Di paintEvent: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
            p.drawLine(QPointF(x+dx,y+dy),QPointF(x+dx*.45,y+dy*.45));p.setBrush(QColor('#CDD7FF'));p.drawEllipse(QPointF(x+dx,y+dy),3,3)
        # BARIS ASLI 2596: Di paintEvent: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.setPen(Qt.NoPen);p.setBrush(QColor('#FCFCFF'));p.drawEllipse(QPointF(x,y),62,62)
        # BARIS ASLI 2597: Di paintEvent: Menghitung/menyiapkan nilai scaled untuk dipakai oleh proses berikutnya.
        scaled=self.logo.scaled(70,99,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        # BARIS ASLI 2598: Di paintEvent: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.drawPixmap(int(x-scaled.width()/2),int(y-scaled.height()/2),scaled);p.end()


# BARIS ASLI 3104: Mendefinisikan kelas RoundDiagram. Komponen visualisasi struktur ronde Feistel.
class RoundDiagram(QWidget):
    # BARIS ASLI 3105: Mendefinisikan fungsi __init__. Fungsi ini menangani aksi khusus dalam aplikasi.
    def __init__(self):super().__init__();self.n=1;self.setMinimumSize(190,220)
    # BARIS ASLI 3106: Mendefinisikan fungsi paintEvent. Fungsi ini menangani aksi khusus dalam aplikasi.
    def paintEvent(self,event):
        # BARIS ASLI 3107: Di paintEvent: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p=QPainter(self);p.setRenderHint(QPainter.Antialiasing);w=self.width();h=self.height()
        # BARIS ASLI 3108: Di paintEvent: Menghitung/menyiapkan nilai scale untuk dipakai oleh proses berikutnya.
        scale=min(w/240,h/250);p.translate((w-240*scale)/2,(h-250*scale)/2);p.scale(scale,scale)
        # BARIS ASLI 3109: Di paintEvent: Mengatur pena/kuas untuk pewarnaan komponen visual.
        pen=QPen(QColor('#768AF4'),1.4);p.setPen(pen)
        # BARIS ASLI 3110: Mendefinisikan fungsi box. Fungsi ini menangani aksi khusus dalam aplikasi.
        def box(x,y,width,height,label):
            # BARIS ASLI 3111: Di box: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
            p.setBrush(QColor('#F3F6FF'));p.drawRoundedRect(QRectF(x,y,width,height),5,5);p.setPen(QColor('#3A5AD4'));p.setFont(QFont('Segoe UI',10));p.drawText(QRectF(x,y,width,height),Qt.AlignCenter,label);p.setPen(pen)
        # BARIS ASLI 3112: Di paintEvent: Menjalankan langkah box(14,15,75,32,'L'+str(self.n-1));box(150,15,75,32,'R'+str(self.n-1));box(98,79,126,... sebagai bagian dari alur fungsi ini.
        box(14,15,75,32,'L'+str(self.n-1));box(150,15,75,32,'R'+str(self.n-1));box(98,79,126,39,'F(R, K'+str(self.n)+')');box(14,197,75,32,'L'+str(self.n));box(150,197,75,32,'R'+str(self.n))
        # BARIS ASLI 3113: Di paintEvent: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.drawLine(187,47,187,79);p.drawLine(187,118,187,153);p.drawLine(52,47,52,154);p.drawLine(52,154,170,154)
        # BARIS ASLI 3114: Di paintEvent: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        p.setBrush(QColor('#FCFCFF'));p.drawEllipse(QPointF(187,154),13,13);p.drawLine(181,154,193,154);p.drawLine(187,148,187,160);p.drawLine(187,167,187,197)
        # BARIS ASLI 3115: Di paintEvent: Menggambar bentuk/garis/teks sebagai bagian dari visualisasi Feistel.
        path=QPainterPath();path.moveTo(153,47);path.lineTo(124,61);path.lineTo(34,180);path.lineTo(34,197);p.drawPath(path)
        # BARIS ASLI 3116: Di paintEvent: Menjalankan langkah p.end() sebagai bagian dari alur fungsi ini.
        p.end()
