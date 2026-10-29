# -*- coding: utf-8 -*-
"""Modul ciphertext untuk ZarCryptoDES."""

import base64
from cipher import parse_hex

# BARIS ASLI 256: Mendefinisikan fungsi serialize_ciphertext. Mengemas ciphertext, IV, dan penanda format menjadi teks HEX.
def serialize_ciphertext(record,wire_format='zar'):
    # BARIS ASLI 257: Di serialize_ciphertext: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
    """Format HEX v2: penanda 8 byte, IV 8 byte, ciphertext CBC."""
    # BARIS ASLI 258: Di serialize_ciphertext: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: record['mode']=='ECB':return record['ciphertext_hex'].upper()+'\n'.
    if record['mode']=='ECB':return record['ciphertext_hex'].upper()+'\n'
    # BARIS ASLI 259: Di serialize_ciphertext: Memeriksa jenis format atau mode penyimpanan data.
    if wire_format=='cbc':return (record['iv_hex']+record['ciphertext_hex']).upper()+'\n'
    # BARIS ASLI 260: Di serialize_ciphertext: Menghitung/menyiapkan nilai header untuk dipakai oleh proses berikutnya.
    header=b'ZCD2'+bytes([1 if record['algorithm']=='DES' else 3,1,1,0])
    # BARIS ASLI 261: Di serialize_ciphertext: Mengembalikan paket data/metadata ciphertext yang siap dipakai.
    return (header+bytes.fromhex(record['iv_hex']+record['ciphertext_hex'])).hex().upper()+'\n'


# BARIS ASLI 264: Mendefinisikan fungsi parse_ciphertext. Mendeteksi dan membaca format HEX ZCD2, CBC/ECB mentah, ZAR1, dan TXT berlabel.
def parse_ciphertext(value,algorithm='DES',iv_hex='',wire_format='zar'):
    # BARIS ASLI 265: Di parse_ciphertext: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
    """Baca format TXT yang sama untuk DES dan 3DES."""
    # BARIS ASLI 266: Di parse_ciphertext: Menghitung/menyiapkan nilai value untuk dipakai oleh proses berikutnya.
    value=value.lstrip('\ufeff').strip()
    # BARIS ASLI 267: Di parse_ciphertext: Menghitung/menyiapkan nilai compact untuk dipakai oleh proses berikutnya.
    compact=''.join(value.split())
    # BARIS ASLI 268: Di parse_ciphertext: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: compact and all(c in '0123456789abcdefABCDEF' for c in compact).
    if compact and all(c in '0123456789abcdefABCDEF' for c in compact):
        # BARIS ASLI 269: Di parse_ciphertext: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
        if len(compact)%2:raise ValueError('Jumlah digit HEX harus genap.')
        # BARIS ASLI 270: Di parse_ciphertext: Mendekode teks heksadesimal menjadi representasi byte.
        raw=bytes.fromhex(compact)
        # BARIS ASLI 271: Di parse_ciphertext: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: raw.startswith(b'ZCD2').
        if raw.startswith(b'ZCD2'):
            # BARIS ASLI 272: Di parse_ciphertext: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
            if len(raw)<24 or len(raw)%8:raise ValueError('Data HEX v2 terpotong atau panjangnya tidak valid.')
            # BARIS ASLI 273: Di parse_ciphertext: Memeriksa jenis format atau mode penyimpanan data.
            if raw[4] not in (1,3) or raw[5:8]!=b'\x01\x01\x00':raise ValueError('Algoritma, mode, atau padding format HEX v2 tidak didukung.')
            # BARIS ASLI 274: Di parse_ciphertext: Menghitung/menyiapkan nilai algorithm untuk dipakai oleh proses berikutnya.
            algorithm='DES' if raw[4]==1 else '3DES'
            # BARIS ASLI 275: Di parse_ciphertext: Menghitung/menyiapkan nilai iv,ct untuk dipakai oleh proses berikutnya.
            iv,ct=raw[8:16].hex(),raw[16:].hex()
        # BARIS ASLI 276: Di parse_ciphertext: Menguji kondisi alternatif: wire_format in ('cbc','ecb').
        elif wire_format in ('cbc','ecb'):
            # BARIS ASLI 277: Di parse_ciphertext: Memilih jalur operasi sesuai backend atau jenis algoritma.
            if algorithm not in ('DES','3DES'):raise ValueError('Pilih DES atau 3DES sesuai pengirim.')
            # BARIS ASLI 278: Di parse_ciphertext: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
            if len(raw)%8 or len(raw)<(16 if wire_format=='cbc' else 8):raise ValueError('Panjang HEX tidak sesuai format yang dipilih.')
            # BARIS ASLI 279: Di parse_ciphertext: Mengembalikan nilai perhitungan ke pemanggil: {'version':1,'algorithm':algorithm,'mode':'CBC' if wire_format=='cbc' else 'ECB','....
            return {'version':1,'algorithm':algorithm,'mode':'CBC' if wire_format=='cbc' else 'ECB','padding':'PKCS7','iv_hex':raw[:8].hex() if wire_format=='cbc' else '', 'ciphertext_hex':(raw[8:] if wire_format=='cbc' else raw).hex()}
        # BARIS ASLI 280: Di parse_ciphertext: Menguji kondisi alternatif: iv_hex.
        elif iv_hex:
            # BARIS ASLI 281: Di parse_ciphertext: Menjalankan langkah parse_hex(iv_hex,8,'IV') sebagai bagian dari alur fungsi ini.
            parse_hex(iv_hex,8,'IV')
            # BARIS ASLI 282: Di parse_ciphertext: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
            if not raw or len(raw)%8:raise ValueError('Panjang ciphertext lama tidak valid.')
            # BARIS ASLI 283: Di parse_ciphertext: Menghitung/menyiapkan nilai iv,ct untuk dipakai oleh proses berikutnya.
            iv,ct=iv_hex,compact
        # BARIS ASLI 284: Di parse_ciphertext: Cabang alternatif ketika kondisi sebelumnya tidak terpenuhi.
        else:
            # BARIS ASLI 285: Di parse_ciphertext: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
            raise ValueError('HEX ini tanpa penanda ZarCryptoDES. Pilih format CBC (IV + ciphertext) atau ECB sesuai pengirim, lalu pilih / tempel ulang masukan. Jangan menebak mode; samakan dengan pengirim.')
        # BARIS ASLI 286: Di parse_ciphertext: Mengembalikan nilai perhitungan ke pemanggil: {'version':1,'algorithm':algorithm,'mode':'CBC','padding':'PKCS7',.
        return {'version':1,'algorithm':algorithm,'mode':'CBC','padding':'PKCS7',
                # BARIS ASLI 287: Di parse_ciphertext: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
                'iv_hex':iv.upper(),'ciphertext_hex':ct.upper()}
    # BARIS ASLI 288: Di parse_ciphertext: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: value.startswith('ZAR1:').
    if value.startswith('ZAR1:'):
        # BARIS ASLI 289: Di parse_ciphertext: Menghitung/menyiapkan nilai parts untuk dipakai oleh proses berikutnya.
        parts=value.split(':',2)
        # BARIS ASLI 290: Di parse_ciphertext: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
        if len(parts)!=3 or parts[1] not in ('DES','3DES'):
            # BARIS ASLI 291: Di parse_ciphertext: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
            raise ValueError('Penanda algoritma ZAR1 tidak valid.')
        # BARIS ASLI 292: Di parse_ciphertext: Menghitung/menyiapkan nilai encoded untuk dipakai oleh proses berikutnya.
        encoded=''.join(parts[2].split())
        # BARIS ASLI 293: Di parse_ciphertext: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
        try:raw=base64.b64decode(encoded+'='*(-len(encoded)%4),altchars=b'-_',validate=True)
        # BARIS ASLI 294: Di parse_ciphertext: Menangani kesalahan ValueError as excraise ValueError('Isi Base64 pada ciphertext ZAR1 ....
        except ValueError as exc:raise ValueError('Isi Base64 pada ciphertext ZAR1 tidak valid.') from exc
        # BARIS ASLI 295: Di parse_ciphertext: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
        if len(raw)<16 or len(raw)%8:
            # BARIS ASLI 296: Di parse_ciphertext: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
            raise ValueError('Panjang payload ZAR1 tidak valid untuk IV 8 byte dan ciphertext CBC.')
        # Format ZAR1:ALG:Base64URL(IV 8 byte + ciphertext CBC).
        # BARIS ASLI 298: Di parse_ciphertext: Mengembalikan nilai perhitungan ke pemanggil: {'version':1,'algorithm':parts[1],'mode':'CBC','padding':'PKCS7',.
        return {'version':1,'algorithm':parts[1],'mode':'CBC','padding':'PKCS7',
                # BARIS ASLI 299: Di parse_ciphertext: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
                'iv_hex':raw[:8].hex(),'ciphertext_hex':raw[8:].hex()}
    # BARIS ASLI 300: Di parse_ciphertext: Menghitung/menyiapkan nilai lines untuk dipakai oleh proses berikutnya.
    lines=value.splitlines()
    # BARIS ASLI 301: Di parse_ciphertext: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
    if len(lines)!=6 or lines[0]!='ZarCryptoDES Ciphertext v1':
        # BARIS ASLI 302: Di parse_ciphertext: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError('File ciphertext TXT tidak valid. Pilih file hasil enkripsi aplikasi ini.')
    # BARIS ASLI 303: Di parse_ciphertext: Menghitung/menyiapkan nilai fields untuk dipakai oleh proses berikutnya.
    fields={}
    # BARIS ASLI 304: Di parse_ciphertext: Melakukan iterasi pada elemen/urutan: line in lines[1:].
    for line in lines[1:]:
        # BARIS ASLI 305: Di parse_ciphertext: Menghitung/menyiapkan nilai name,sep,content untuk dipakai oleh proses berikutnya.
        name,sep,content=line.partition(':')
        # BARIS ASLI 306: Di parse_ciphertext: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: not sep or name in fields:raise ValueError('Format ciphertext TXT tidak valid.').
        if not sep or name in fields:raise ValueError('Format ciphertext TXT tidak valid.')
        # BARIS ASLI 307: Di parse_ciphertext: Menghitung/menyiapkan nilai fields[name] untuk dipakai oleh proses berikutnya.
        fields[name]=content.strip()
    # BARIS ASLI 308: Di parse_ciphertext: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: set(fields)!={'Algoritma','Mode','Padding','IV','Ciphertext'}.
    if set(fields)!={'Algoritma','Mode','Padding','IV','Ciphertext'}:
        # BARIS ASLI 309: Di parse_ciphertext: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError('Informasi ciphertext TXT tidak lengkap.')
    # BARIS ASLI 310: Di parse_ciphertext: Memastikan dependensi atau algoritma kriptografi tersedia/valid.
    if fields['Algoritma'] not in ('DES','3DES') or fields['Mode']!='CBC' or fields['Padding']!='PKCS7':
        # BARIS ASLI 311: Di parse_ciphertext: Menghentikan operasi dengan kesalahan yang menjelaskan input tidak valid.
        raise ValueError('Algoritma, mode, atau padding ciphertext TXT tidak didukung.')
    # BARIS ASLI 312: Di parse_ciphertext: Menjalankan langkah parse_hex(fields['IV'],8,'IV') sebagai bagian dari alur fungsi ini.
    parse_hex(fields['IV'],8,'IV')
    # BARIS ASLI 313: Di parse_ciphertext: Mulai blok percobaan; jika terjadi pengecualian, tangani melalui except.
    try:ct=bytes.fromhex(fields['Ciphertext'])
    # BARIS ASLI 314: Di parse_ciphertext: Menangani kesalahan ValueError as excraise ValueError('Ciphertext bukan HEX yang valid.....
    except ValueError as exc:raise ValueError('Ciphertext bukan HEX yang valid.') from exc
    # BARIS ASLI 315: Di parse_ciphertext: Mengecek panjang data atau kunci sebelum melanjutkan pemrosesan.
    if not ct or len(ct)%8:raise ValueError('Ciphertext harus tidak kosong dan kelipatan 8 byte.')
    # BARIS ASLI 316: Di parse_ciphertext: Mengembalikan nilai perhitungan ke pemanggil: {'version':1,'algorithm':fields['Algoritma'],'mode':'CBC','padding':'PKCS7',.
    return {'version':1,'algorithm':fields['Algoritma'],'mode':'CBC','padding':'PKCS7',
            # BARIS ASLI 317: Di parse_ciphertext: Mencantumkan nilai teks/parameter lanjutan yang diperlukan oleh ekspresi.
            'iv_hex':fields['IV'],'ciphertext_hex':fields['Ciphertext']}


# BARIS ASLI 320: Mendefinisikan fungsi message_summary. Menghitung panjang pesan, jumlah padding, dan jumlah blok untuk laporan.
def message_summary(size,stored_size=None,padding_used=True):
    # BARIS ASLI 321: Di message_summary: Menghitung/menyiapkan nilai extra untuk dipakai oleh proses berikutnya.
    extra=8-size%8 if padding_used else 0
    # BARIS ASLI 322: Di message_summary: Menghitung/menyiapkan nilai processed untuk dipakai oleh proses berikutnya.
    processed=size+extra
    # BARIS ASLI 323: Di message_summary: Memakai operasi bit AND/OR untuk menyeleksi atau menggabungkan bit.
    result=(f'Plaintext: {size:,} byte / {size*8:,} bit | Blok: 8 byte / 64 bit\n'
            # BARIS ASLI 324: Di message_summary: Menjalankan langkah f'Padding: {extra} byte'+(' (HEX '+(' '.join([f'{extra:02X}']*extra))+')' if extra el... sebagai bagian dari alur fungsi ini.
            f'Padding: {extra} byte'+(' (HEX '+(' '.join([f'{extra:02X}']*extra))+')' if extra else ' (tanpa padding)')+
            # BARIS ASLI 325: Di message_summary: Memakai operasi bit AND/OR untuk menyeleksi atau menggabungkan bit.
            f' | Setelah padding: {processed:,} byte | Jumlah blok: {processed//8:,}')
    # BARIS ASLI 326: Di message_summary: Mengevaluasi syarat berikut sebelum mengeksekusi cabang: stored_size is not None:result+=f'\nCiphertext murni: {processed:,} byte | Data....
    if stored_size is not None:result+=f'\nCiphertext murni: {processed:,} byte | Data tersimpan sebelum encoding HEX: {stored_size:,} byte'
    # BARIS ASLI 327: Di message_summary: Mengembalikan nilai perhitungan ke pemanggil: result.
    return result
