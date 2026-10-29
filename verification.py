# -*- coding: utf-8 -*-
"""Modul verification untuk ZarCryptoDES."""

from pathlib import Path
import platform
import random
from cipher import decrypt_record, encrypt_bytes, pad, unpad
from constants import ACUAN_3DES, KUNCI_3DES_CONTOH, KUNCI_CONTOH
from crypto_backend import Crypto, DES, DES3
from des_manual import DESManual
from feistel import feistel_decrypt, feistel_encrypt
from file_ops import process_file
from keys import validate_algorithm_key
from triple_des import TripleDESManual

# 3. PENGUJIAN DAN PROSES FILE (TERPISAH DARI TAMPILAN).
# BARIS ASLI 349: Mendefinisikan fungsi verify. Menghentikan pengujian dengan AssertionError jika kondisi tidak dipenuhi.
def verify(condition, message):
    # BARIS ASLI 350: Di verify: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: not condition.
    if not condition:
        # BARIS ASLI 351: Di verify: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise AssertionError(message)


# BARIS ASLI 354: Mendefinisikan fungsi comparison. Membuktikan hasil manual dan library identik saat kunci dan IV sama.
def comparison(data,key,algorithm='DES'):
    # BARIS ASLI 355: Di comparison: Memanggil operasi enkripsi lalu membentuk metadata ciphertext.
    lib=encrypt_bytes(data,key,'library',algorithm=algorithm)
    # BARIS ASLI 356: Di comparison: Mendekode teks heksadesimal menjadi representasi byte.
    manual=encrypt_bytes(data,key,'manual',bytes.fromhex(lib['iv_hex']),algorithm)
    # BARIS ASLI 357: Di comparison: Memeriksa bahwa hasil nyata cocok dengan nilai/ketentuan pengujian.
    verify(lib==manual,'Ciphertext manual berbeda dari library.')
    # BARIS ASLI 358: Di comparison: Memulihkan plaintext berdasarkan metadata ciphertext dan kunci.
    verify(decrypt_record(lib,key,'manual')==data,'Dekripsi manual gagal.')
    # BARIS ASLI 359: Di comparison: Memulihkan plaintext berdasarkan metadata ciphertext dan kunci.
    verify(decrypt_record(manual,key,'library')==data,'Dekripsi library gagal.')
    # BARIS ASLI 360: Di comparison: Mengembalikan nilai perhitungan ke pemanggil: lib.
    return lib


# BARIS ASLI 385: Mendefinisikan fungsi run_verification. Menjalankan pengujian DES standar, CBC, padding, file, dan Feistel dosen.
def run_verification():
    # BARIS ASLI 386: Di run_verification: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
    """Menguji inti DES, padding, file lintas backend, dan Feistel."""
    # BARIS ASLI 387: Di run_verification: Memastikan dependensi atau algoritma kriptografi tersedia/valid.
    if Crypto is None:
        # BARIS ASLI 388: Di run_verification: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ImportError('Instal PyCryptodome: python -m pip install pycryptodome')
    # BARIS ASLI 389: Di run_verification: Menghitung/menyiapkan nilai rows, log untuk dipakai oleh proses berikutnya.
    rows, log = [], []
    # BARIS ASLI 390: Di run_verification: Menghitung/menyiapkan nilai vectors untuk dipakai oleh proses berikutnya.
    vectors = [('133457799BBCDFF1','0123456789ABCDEF','85E813540F0AB405'),
               # BARIS ASLI 391: Di run_verification: Melanjutkan atau menutup kumpulan parameter/nilai dari ekspresi sebelumnya.
               ('0000000000000000','0000000000000000','8CA64DE9C1B123A7'),
               # BARIS ASLI 392: Di run_verification: Melanjutkan atau menutup kumpulan parameter/nilai dari ekspresi sebelumnya.
               ('FFFFFFFFFFFFFFFF','FFFFFFFFFFFFFFFF','7359B2163E4EDC58')]
    # BARIS ASLI 393: Di run_verification: Melakukan iterasi pada elemen/urutan: kh, ph, ch in vectors.
    for kh, ph, ch in vectors:
        # BARIS ASLI 394: Di run_verification: Mendekode teks heksadesimal menjadi representasi byte.
        k, p, expected = bytes.fromhex(kh), bytes.fromhex(ph), bytes.fromhex(ch)
        # BARIS ASLI 395: Di run_verification: Menghitung/menyiapkan nilai manual untuk dipakai oleh proses berikutnya.
        manual = DESManual(k)
        # BARIS ASLI 396: Di run_verification: Mengenkripsi satu blok 8 byte menggunakan mesin DES/3DES manual.
        a = manual.encrypt_block(p)
        # BARIS ASLI 397: Di run_verification: Membuat cipher dari PyCryptodome untuk implementasi library/pembanding.
        b = DES.new(k, DES.MODE_ECB).encrypt(p)
        # BARIS ASLI 398: Di run_verification: Memeriksa bahwa hasil nyata cocok dengan nilai/ketentuan pengujian.
        verify(a == b == expected, 'Vektor DES tidak cocok.')
        # BARIS ASLI 399: Di run_verification: Mendekripsi satu blok 8 byte dengan mesin DES/3DES manual.
        verify(manual.decrypt_block(b) == p, 'Dekripsi manual tidak cocok.')
        # BARIS ASLI 400: Di run_verification: Membuat cipher dari PyCryptodome untuk implementasi library/pembanding.
        verify(DES.new(k, DES.MODE_ECB).decrypt(a) == p, 'Dekripsi library tidak cocok.')
        # BARIS ASLI 401: Di run_verification: Menambahkan elemen baru pada daftar hasil atau riwayat.
        rows.append((ph,a.hex(),b.hex(),'LULUS'))
    # BARIS ASLI 402: Di run_verification: Membuat generator pseudorandom ber-seed tetap untuk uji yang bisa diulang.
    rng = random.Random(20261014)  # Seed tetap untuk pengujian, bukan kunci produksi.
    # BARIS ASLI 403: Di run_verification: Melakukan iterasi pada elemen/urutan: _ in range(128).
    for _ in range(128):
        # BARIS ASLI 404: Di run_verification: Menghitung/menyiapkan nilai k untuk dipakai oleh proses berikutnya.
        k = bytes(rng.getrandbits(8) for _ in range(8))
        # BARIS ASLI 405: Di run_verification: Menghitung/menyiapkan nilai p untuk dipakai oleh proses berikutnya.
        p = bytes(rng.getrandbits(8) for _ in range(8))
        # BARIS ASLI 406: Di run_verification: Mengenkripsi satu blok 8 byte menggunakan mesin DES/3DES manual.
        cm = DESManual(k).encrypt_block(p)
        # BARIS ASLI 407: Di run_verification: Membuat cipher dari PyCryptodome untuk implementasi library/pembanding.
        cl = DES.new(k, DES.MODE_ECB).encrypt(p)
        # BARIS ASLI 408: Di run_verification: Memeriksa bahwa hasil nyata cocok dengan nilai/ketentuan pengujian.
        verify(cm == cl, 'Pasangan pseudorandom berbeda.')
        # BARIS ASLI 409: Di run_verification: Mendekripsi satu blok 8 byte dengan mesin DES/3DES manual.
        verify(DESManual(k).decrypt_block(cl) == p, 'Pemulihan blok manual gagal.')
        # BARIS ASLI 410: Di run_verification: Membuat cipher dari PyCryptodome untuk implementasi library/pembanding.
        verify(DES.new(k, DES.MODE_ECB).decrypt(cm) == p, 'Pemulihan blok library gagal.')
    # BARIS ASLI 411: Mengimpor komponen Crypto.Util.Padding import pad as reference_pad untuk fungsi terkait.
    from Crypto.Util.Padding import pad as reference_pad
    # BARIS ASLI 412: Di run_verification: Mendekode teks heksadesimal menjadi representasi byte.
    key = bytes.fromhex(KUNCI_CONTOH)
    # BARIS ASLI 413: Di run_verification: Menghitung/menyiapkan nilai cases untuk dipakai oleh proses berikutnya.
    cases = [b'A'*n for n in (0,1,7,8,11,15,16,17,33,256)]
    # BARIS ASLI 414: Di run_verification: Menambahkan elemen baru pada daftar hasil atau riwayat.
    cases.append('Kriptografi — café 😊\r\n'.encode('utf-8'))
    # BARIS ASLI 415: Di run_verification: Melakukan iterasi pada elemen/urutan: data in cases.
    for data in cases:
        # BARIS ASLI 416: Di run_verification: Memeriksa bahwa hasil nyata cocok dengan nilai/ketentuan pengujian.
        verify(pad(data) == reference_pad(data,8), 'Padding berbeda dari library.')
        # BARIS ASLI 417: Di run_verification: Menjalankan langkah comparison(data,key) sebagai bagian dari alur fungsi ini.
        comparison(data,key)
    # BARIS ASLI 418: Di run_verification: Mengenkripsi satu blok 8 byte menggunakan mesin DES/3DES manual.
    invalid = [lambda: DESManual(b'short'), lambda: DESManual(key).encrypt_block(b'short'),
               # BARIS ASLI 419: Di run_verification: Memanggil operasi enkripsi lalu membentuk metadata ciphertext.
               lambda: encrypt_bytes(b'x',key,iv=b'short'), lambda: decrypt_record([],key),
               # BARIS ASLI 420: Di run_verification: Memulihkan plaintext berdasarkan metadata ciphertext dan kunci.
               lambda: decrypt_record({'version':2},key), lambda: unpad(b'1234567\x00'),
               # BARIS ASLI 421: Di run_verification: Menjalankan langkah lambda: unpad(b'123456\x01\x02')] sebagai bagian dari alur fungsi ini.
               lambda: unpad(b'123456\x01\x02')]
    # BARIS ASLI 422: Di run_verification: Melakukan iterasi pada elemen/urutan: action in invalid.
    for action in invalid:
        # BARIS ASLI 423: Di run_verification: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:
            # BARIS ASLI 424: Di run_verification: Menjalankan langkah action() sebagai bagian dari alur fungsi ini.
            action()
        # BARIS ASLI 425: Di run_verification: Menangani kesalahan ValueError.
        except ValueError:
            # BARIS ASLI 426: Di run_verification: Tidak melakukan aksi tambahan dalam cabang ini.
            pass
        # BARIS ASLI 427: Di run_verification: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
        else:
            # BARIS ASLI 428: Di run_verification: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
            raise AssertionError('Masukan tidak valid seharusnya ditolak.')
    # Menguji baca/tulis file sungguhan tanpa membutuhkan file contoh tambahan.
    # BARIS ASLI 430: Mengimpor modul tempfile yang diperlukan oleh aplikasi.
    import tempfile
    # BARIS ASLI 431: Di run_verification: Mengelola resource atau file sementara agar ditutup/dibersihkan otomatis.
    with tempfile.TemporaryDirectory() as directory:
        # BARIS ASLI 432: Di run_verification: Menghitung/menyiapkan nilai d untuk dipakai oleh proses berikutnya.
        d = Path(directory)
        # BARIS ASLI 433: Di run_verification: Menghitung/menyiapkan nilai data untuk dipakai oleh proses berikutnya.
        data = 'kriptografi\nUji spasi, café 😊\r\n'.encode('utf-8')
        # BARIS ASLI 434: Di run_verification: Menyimpan byte/teks hasil operasi ke berkas yang dipilih.
        source = d/'plaintext.txt'; source.write_bytes(data)
        # BARIS ASLI 435: Di run_verification: Melakukan iterasi pada elemen/urutan: backend, other in [('library','manual'),('manual','library')].
        for backend, other in [('library','manual'),('manual','library')]:
            # BARIS ASLI 436: Di run_verification: Menghitung/menyiapkan nilai ct, recovered untuk dipakai oleh proses berikutnya.
            ct, recovered = d/f'{backend}.txt', d/f'{backend}_pulih.txt'
            # BARIS ASLI 437: Di run_verification: Menghitung/menyiapkan nilai info untuk dipakai oleh proses berikutnya.
            info=process_file('encrypt',backend,key,source,ct)
            # BARIS ASLI 438: Di run_verification: Menjalankan langkah process_file('decrypt',other,key,ct,recovered) sebagai bagian dari alur fungsi ini.
            process_file('decrypt',other,key,ct,recovered)
            # BARIS ASLI 439: Di run_verification: Membaca seluruh konten file sebagai byte/teks.
            verify(recovered.read_bytes() == data, 'File dekripsi tidak identik.')
        # BARIS ASLI 440: Di run_verification: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:
            # BARIS ASLI 441: Di run_verification: Menjalankan langkah process_file('encrypt','library',key,source,source) sebagai bagian dari alur fungsi ini.
            process_file('encrypt','library',key,source,source)
        # BARIS ASLI 442: Di run_verification: Menangani kesalahan ValueError.
        except ValueError:
            # BARIS ASLI 443: Di run_verification: Tidak melakukan aksi tambahan dalam cabang ini.
            pass
        # BARIS ASLI 444: Di run_verification: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
        else:
            # BARIS ASLI 445: Di run_verification: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
            raise AssertionError('Masukan dan keluaran sama seharusnya ditolak.')
    # BARIS ASLI 446: Di run_verification: Menghitung/menyiapkan nilai keys untuk dipakai oleh proses berikutnya.
    keys = [0x1F,0x2A,0x3C,0x4D]
    # BARIS ASLI 447: Di run_verification: Memeriksa bahwa hasil nyata cocok dengan nilai/ketentuan pengujian.
    verify(feistel_encrypt(0x1234,keys) == 0x6B42,'Vektor Feistel gagal.')
    # BARIS ASLI 448: Di run_verification: Memeriksa seluruh 65.536 kemungkinan input Feistel 16-bit.
    for p in range(65536):
        # BARIS ASLI 449: Di run_verification: Memeriksa bahwa hasil nyata cocok dengan nilai/ketentuan pengujian.
        verify(feistel_decrypt(feistel_encrypt(p,keys),keys) == p,'Pemulihan Feistel gagal.')
    # BARIS ASLI 450: Di run_verification: Mendekode teks heksadesimal menjadi representasi byte.
    trace = []; DESManual(key).encrypt_block(bytes.fromhex(vectors[0][1]),trace)
    # BARIS ASLI 451: Di run_verification: Memakai operasi bit AND/OR untuk menyeleksi atau menggabungkan bit.
    log = ['HASIL PENGUJIAN DES STUDIO',f'Python {platform.python_version()} | PyCryptodome {Crypto.__version__}',
           # BARIS ASLI 452: Di run_verification: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
           '3 vektor DES tetap: LULUS', '128 pasangan blok/kunci pseudorandom: LULUS',
           # BARIS ASLI 453: Di run_verification: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
           '11 kasus CBC, padding dan UTF-8: LULUS', '2 arah file dekripsi silang: LULUS',
           # BARIS ASLI 454: Di run_verification: Menghitung/menyiapkan nilai '7 masukan tidak valid: DITOLAK', 'Fi... untuk dipakai oleh proses berikutnya.
           '7 masukan tidak valid: DITOLAK', 'File input = output: DITOLAK',
           # BARIS ASLI 455: Di run_verification: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
           '65536 blok Feistel: PULIH', '', 'Vektor dosen:',
           # BARIS ASLI 456: Di run_verification: Menghitung/menyiapkan nilai f'Key untuk dipakai oleh proses berikutnya.
           f'Key = {KUNCI_CONTOH}', 'Plaintext = 0123456789ABCDEF',
           # BARIS ASLI 457: Di run_verification: Menghitung/menyiapkan nilai 'Ciphertext manual untuk dipakai oleh proses berikutnya.
           'Ciphertext manual = library = 85e813540f0ab405', '',
           # BARIS ASLI 458: Di run_verification: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
           'Kecocokan merupakan verifikasi pada kasus yang diuji, bukan bukti matematis semua masukan.']
    # BARIS ASLI 459: Di run_verification: Mengembalikan nilai perhitungan ke pemanggil: {'rows':rows,'trace':trace,'log':'\n'.join(log),'status':'LULUS'}.
    return {'rows':rows,'trace':trace,'log':'\n'.join(log),'status':'LULUS'}


# BARIS ASLI 464: Mendefinisikan fungsi run_3des_verification. Menjalankan rangkaian pengujian 3DES manual versus library.
def run_3des_verification():
    # BARIS ASLI 465: Di run_3des_verification: Mendekode teks heksadesimal menjadi representasi byte.
    key=bytes.fromhex(KUNCI_3DES_CONTOH);plain=bytes.fromhex('0123456789ABCDEF')
    # BARIS ASLI 466: Di run_3des_verification: Mendekode teks heksadesimal menjadi representasi byte.
    expected=bytes.fromhex(ACUAN_3DES)
    # BARIS ASLI 467: Di run_3des_verification: Membuat cipher dari PyCryptodome untuk implementasi library/pembanding.
    manual=TripleDESManual(key);cl=DES3.new(key,DES3.MODE_ECB).encrypt(plain)
    # BARIS ASLI 468: Di run_3des_verification: Mengenkripsi satu blok 8 byte menggunakan mesin DES/3DES manual.
    verify(manual.encrypt_block(plain)==cl==expected,'Vektor 3DES gagal.')
    # BARIS ASLI 469: Di run_3des_verification: Mendekripsi satu blok 8 byte dengan mesin DES/3DES manual.
    verify(manual.decrypt_block(cl)==plain,'Dekripsi 3DES manual gagal.')
    # BARIS ASLI 470: Di run_3des_verification: Membuat generator pseudorandom ber-seed tetap untuk uji yang bisa diulang.
    rng=random.Random(20261021)
    # BARIS ASLI 471: Di run_3des_verification: Melakukan iterasi pada elemen/urutan: _ in range(128).
    for _ in range(128):
        # BARIS ASLI 472: Di run_3des_verification: Mengulang sampai kriteria True terpenuhi.
        while True:
            # BARIS ASLI 473: Di run_3des_verification: Menghitung/menyiapkan nilai k untuk dipakai oleh proses berikutnya.
            k=bytes(rng.getrandbits(8) for _ in range(24))
            # BARIS ASLI 474: Di run_3des_verification: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
            try:validate_algorithm_key(k,'3DES');break
            # BARIS ASLI 475: Di run_3des_verification: Menangani kesalahan ValueErrorpass.
            except ValueError:pass
        # BARIS ASLI 476: Di run_3des_verification: Mengenkripsi satu blok 8 byte menggunakan mesin DES/3DES manual.
        p=bytes(rng.getrandbits(8) for _ in range(8));cm=TripleDESManual(k).encrypt_block(p)
        # BARIS ASLI 477: Di run_3des_verification: Membuat cipher dari PyCryptodome untuk implementasi library/pembanding.
        lib=DES3.new(k,DES3.MODE_ECB)
        # BARIS ASLI 478: Di run_3des_verification: Memeriksa bahwa hasil nyata cocok dengan nilai/ketentuan pengujian.
        verify(cm==lib.encrypt(p),'Ciphertext blok 3DES berbeda.')
        # BARIS ASLI 479: Di run_3des_verification: Mendekripsi satu blok 8 byte dengan mesin DES/3DES manual.
        verify(TripleDESManual(k).decrypt_block(cm)==p,'Pemulihan 3DES manual gagal.')
        # BARIS ASLI 480: Di run_3des_verification: Membuat cipher dari PyCryptodome untuk implementasi library/pembanding.
        verify(DES3.new(k,DES3.MODE_ECB).decrypt(cm)==p,'Pemulihan 3DES library gagal.')
    # BARIS ASLI 481: Di run_3des_verification: Melakukan iterasi pada elemen/urutan: data in [b'A'*n for n in (0,1,7,8,15,16,17,33,256)]+['Menyala Abangku café 😊\r\....
    for data in [b'A'*n for n in (0,1,7,8,15,16,17,33,256)]+['Menyala Abangku café 😊\r\n'.encode('utf-8')]:
        # BARIS ASLI 482: Di run_3des_verification: Menjalankan langkah comparison(data,key,'3DES') sebagai bagian dari alur fungsi ini.
        comparison(data,key,'3DES')
    # BARIS ASLI 483: Mengimpor modul tempfile yang diperlukan oleh aplikasi.
    import tempfile
    # BARIS ASLI 484: Di run_3des_verification: Mengelola resource atau file sementara agar ditutup/dibersihkan otomatis.
    with tempfile.TemporaryDirectory() as directory:
        # BARIS ASLI 485: Di run_3des_verification: Menyimpan byte/teks hasil operasi ke berkas yang dipilih.
        d=Path(directory);p=d/'plain.txt';data=b'Menyala Abangku';p.write_bytes(data)
        # BARIS ASLI 486: Di run_3des_verification: Melakukan iterasi pada elemen/urutan: backend,other in [('manual','library'),('library','manual')].
        for backend,other in [('manual','library'),('library','manual')]:
            # BARIS ASLI 487: Di run_3des_verification: Menghitung/menyiapkan nilai c untuk dipakai oleh proses berikutnya.
            c=d/(backend+'_cipher.txt');out=d/(backend+'_pulih.txt')
            # BARIS ASLI 488: Di run_3des_verification: Menghitung/menyiapkan nilai info untuk dipakai oleh proses berikutnya.
            info=process_file('encrypt',backend,key,p,c,'3DES');process_file('decrypt',other,key,c,out,'3DES')
            # BARIS ASLI 489: Di run_3des_verification: Membaca seluruh konten file sebagai byte/teks.
            verify(out.read_bytes()==data,'Pemulihan file 3DES silang gagal.')
    # Degenerasi juga ditolak bila perbedaan byte hanya pada parity.
    # BARIS ASLI 491: Di run_3des_verification: Melakukan iterasi pada elemen/urutan: bad in [key[:8],b'\x01'*24,bytes.fromhex('0123456789ABCDEF0022446688AACCEE00112....
    for bad in [key[:8],b'\x01'*24,bytes.fromhex('0123456789ABCDEF0022446688AACCEE0011223344556677')]:
        # BARIS ASLI 492: Di run_3des_verification: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:validate_algorithm_key(bad,'3DES')
        # BARIS ASLI 493: Di run_3des_verification: Menangani kesalahan ValueErrorpass.
        except ValueError:pass
        # BARIS ASLI 494: Di run_3des_verification: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
        else:raise AssertionError('Kunci 3DES tidak valid seharusnya ditolak.')
    # BARIS ASLI 495: Di run_3des_verification: Menghitung/menyiapkan nilai log untuk dipakai oleh proses berikutnya.
    log=['HASIL PENGUJIAN 3DES','3DES manual: E(K3, D(K2, E(K1, P))); tiap tahap memakai DESManual.',
         # BARIS ASLI 496: Di run_3des_verification: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
         '3DES library: Crypto.Cipher.DES3.',
         # BARIS ASLI 497: Di run_3des_verification: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
         'Vektor tetap 3DES: LULUS','128 pasangan blok/kunci 3DES: LULUS',
         # BARIS ASLI 498: Di run_3des_verification: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
         '10 kasus CBC/padding/UTF-8: LULUS','2 arah dekripsi file silang: LULUS',
         # BARIS ASLI 499: Di run_3des_verification: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
         'Kunci pendek / degenerasi / parity: DITOLAK',
         # BARIS ASLI 500: Di run_3des_verification: Menghitung/menyiapkan nilai 'Ciphertext manual untuk dipakai oleh proses berikutnya.
         'Ciphertext manual = library = '+ACUAN_3DES,
         # BARIS ASLI 501: Di run_3des_verification: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
         'Ukuran blok tetap 8 byte. Kunci contoh 24 byte berisi K1, K2, K3; kunci 16 byte memakai K3 = K1.',
         # BARIS ASLI 502: Di run_3des_verification: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
         'Kecocokan berlaku pada kasus yang diuji.']
    # BARIS ASLI 503: Di run_3des_verification: Mengembalikan nilai perhitungan ke pemanggil: {'log':'\n'.join(log),'status':'LULUS'}.
    return {'log':'\n'.join(log),'status':'LULUS'}
