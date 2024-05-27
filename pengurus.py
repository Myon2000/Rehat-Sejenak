import koneksi
import datetime
import getpass
import os
import math
from tabulate import tabulate

def pengurus(id, nama):
    while True:
        os.system('cls')
        print(f'''
Selamat datang, {nama}
[1] Tambahkan penyewaan luring
[2] Konfirmasi pembayaran pelanggan
[3] Perbarui status penyewaan
[4] Ganti Password
[5] Logout
    ''')
        pilihan = input('Masukan: ')
        match pilihan:
            case '1':
                tambah_penyewaan_luring(id)
            case '2':
                konfirmasi_pembayaran_pelanggan(id)
            case '3':
                perbarui_status_penyewaan()
            case '4':
                ganti_password_pengurus(id)
            case '5':
                break

def tambah_penyewaan_luring(id_pengurus_rental):
    os.system('cls')
    conn = koneksi.create_connection()
    cur = conn.cursor()

    while True:
        awal = input('Masukkan tanggal dan jam awal sewa (yyyy-mm-dd hh:mm): ')
        # Memastikan tanggalnya valid. Jika tidak, tanya lagi
        try: awal_datetime = datetime.datetime.strptime(awal, '%Y-%m-%d %H:%M')
        except:
            print('Tanggal tidak valid!')
            continue
        break
    while True:
        akhir = input('Masukkan tanggal dan jam akhir sewa (yyyy-mm-dd hh:mm): ')
        # Memastikan tanggalnya valid. Jika tidak, tanya lagi
        try: akhir_datetime = datetime.datetime.strptime(akhir, '%Y-%m-%d %H:%M')
        except:
            print('Tanggal tidak valid!')
            continue
        break

    while True:
        query_select = """
SELECT k.id_konsol, k.harga_sewa_per_jam, jk.nama_jenis, p.tanggal_akhir_sewa as tersedia_pada
FROM konsol k
JOIN jenis_konsol jk ON (jk.id_jenis_konsol = k.id_jenis_konsol)
LEFT JOIN penyewaan p ON (
	p.id_konsol = k.id_konsol and
	p.id_status_penyewaan <> 3
)"""

        cur.execute(query_select)
        list_konsol = cur.fetchall()
        tabel = [['id', 'Jenis Konsol', 'Harga per Jam', 'Ketersediaan']]

        for i in list_konsol:
            a = []
            a.append(i[0])
            a.append(i[2])
            a.append(i[1])
            if i[3]:
                a.append(f"Tidak tersedia (hingga {i[3].strftime('%y-%m-%d %H:%M')})")
            else:
                a.append('Tersedia')
            tabel.append(a)
        print(tabulate(tabel))

        konsol = input('Masukkan id konsol yang disewa: ')
        if not konsol.isnumeric():
            print('id tidak valid!')
            continue

        query_konsol = '''
SELECT k.id_konsol, k.harga_sewa_per_jam, p.id_penyewaan is null as tersedia
FROM konsol k
LEFT JOIN penyewaan p ON (
	p.id_konsol = k.id_konsol and
	p.id_status_penyewaan <> 3
) WHERE k.id_konsol = %s'''
        cur.execute(query_konsol, (konsol))
        konsol = cur.fetchone()

        # Memastikan ID konsol ada
        if not konsol:
            print('Konsol tidak ditemukan!')
            continue
        # Memastikan konsol tidak sedang dipinjam
        elif konsol[2] == False:
            print('Konsol sedang tidak tersedia!')
            continue
        else: break
        
    jam = math.ceil((akhir_datetime - awal_datetime).total_seconds() / 3600)
    harga_sewa_akhir = konsol[1] * jam

    query = '''INSERT INTO penyewaan
        (tanggal_awal_sewa, tanggal_akhir_sewa, id_konsol,
        biaya, id_pengurus_rental, id_status_penyewaan)
        VALUES (%s, %s, %s, %s, %s, 2)'''
    cur.execute(query, (awal, akhir, konsol[0], harga_sewa_akhir, id_pengurus_rental))
    conn.commit()

    print(f'''
Data ditambahkan
Tanggal awal: {awal}
Tanggal akhir: {akhir}
Biaya: {harga_sewa_akhir} ({jam} jam)
ID Konsol: {konsol[0]}
''')
    input('Tekan enter untuk melanjutkan')

    cur.close()
    conn.close()

def perbarui_status_penyewaan():
    os.system('cls')
    conn = koneksi.create_connection()
    cur = conn.cursor()

    query_select = '''SELECT p.id_penyewaan, p.tanggal_awal_sewa, p.tanggal_akhir_sewa, pel.nama, jk.nama_jenis, sp.deskripsi_status
FROM penyewaan p
left join pelanggan pel ON pel.id_pelanggan = p.id_pelanggan
join konsol k ON k.id_konsol = p.id_konsol
join jenis_konsol jk ON k.id_jenis_konsol = jk.id_jenis_konsol
join status_penyewaan sp ON sp.id_status_penyewaan = p.id_status_penyewaan'''
    cur.execute(query_select)

    semua_penyewaan = cur.fetchall()
    tabel = [['id', 'Tanggal Awal', 'Tanggal Akhir', 'Nama Penyewa', 'Konsol yang Disewa', 'Status']]
    for penyewaan in semua_penyewaan:
        a = []
        a.append(penyewaan[0])
        a.append(penyewaan[1])
        a.append(penyewaan[2])
        a.append(penyewaan[3] or '<offline>')
        a.append(penyewaan[4])
        a.append(penyewaan[5])
        tabel.append(a)
    print(tabulate(tabel))

    while True:
        id = input('Pilih id penyewaan yang ingin diubah: ')
        if not id.isnumeric():
            print('id tidak valid!')
            continue
        query_select = '''SELECT sp.deskripsi_status FROM penyewaan p
            JOIN status_penyewaan sp ON (sp.id_status_penyewaan = p.id_status_penyewaan) WHERE p.id_penyewaan = %s'''
        cur.execute(query_select, (id,))
        penyewaan = cur.fetchone()

        if not penyewaan:
            print('Penyewaan tidak ditemukan!')
            continue
        break

    print('Status saat ini: ' + penyewaan[0])
    print('''
Ubah menjadi
[1] Belum diambil
[2] Belum dikembalikan
[3] Selesai
''')

    while True:
        pilihan = input('Masukan: ')
        if pilihan not in ('1', '2', '3'):
            print('Pilihan tidak valid!')
            continue

        query_update = 'UPDATE penyewaan SET id_status_penyewaan = %s WHERE id_penyewaan = %s'
        cur.execute(query_update, (pilihan, id))
        conn.commit()
        break
    input('Berhasil! Tekan enter untuk melanjutkan.')
    cur.close()
    conn.close()

def konfirmasi_pembayaran_pelanggan(id_pengurus_rental):
    os.system('cls')
    conn = koneksi.create_connection()
    cur = conn.cursor()

    query = '''SELECT t.id_transaksi, pel.nama, t.biaya, t.tanggal_dibuat, t.kode_transaksi, pr.nama, jk.nama_jenis
FROM transaksi t
LEFT JOIN pengurus_rental pr ON (pr.id_pengurus_rental = t.id_pengurus_rental)
JOIN penyewaan p ON (p.id_penyewaan = t.id_penyewaan)
JOIN pelanggan pel ON (pel.id_pelanggan = p.id_pelanggan)
JOIN konsol k ON (k.id_konsol = p.id_konsol)
JOIN jenis_konsol jk ON (jk.id_jenis_konsol = k.id_jenis_konsol)
ORDER BY t.tanggal_dibuat'''

    cur.execute(query)
    list_transaksi = cur.fetchall()

    tabel = [['id', 'Nama pelanggan', 'Biaya', 'Tanggal dibuat', 'Kode transaksi', 'Dikonfirmasi oleh', 'Konsol yang disewa']]

    for i in list_transaksi:
        tabel.append([
            i[0],
            i[1],
            i[2],
            i[3],
            i[4] or '<belum dibayar>',
            i[5] or '<belum dikonfirmasi>',
            i[6]
        ])
    print(tabulate(tabel))

    while True:
        id = input('Pilih id transaksi yang ingin dikonfirmasi: ')
        if id == '':
            break
        elif not id.isnumeric():
            print('id tidak valid!')
            continue
        query_select = 'SELECT id_pengurus_rental FROM transaksi WHERE id_transaksi = %s'
        cur.execute(query_select, (id,))
        transaksi = cur.fetchone()

        if not transaksi:
            print('Penyewaan tidak ditemukan!')
            continue
        elif transaksi[0]:
            print('Transaksi sudah dikonfirmasi!')
            continue

        break

    while True:
        print(f'''
Mengonfirmasi transaksi dengan id {id}. Lanjutkan?
[1] Ya
[2] Kembali
''')
        pilihan = input()
        if pilihan == '2': continue
        elif pilihan == '1':
            break
        else:
            print('Pilihan tidak valid!')

    query_update = 'UPDATE transaksi SET id_pengurus_rental = %s WHERE id_transaksi = %s'
    cur.execute(query_update, (id_pengurus_rental, id))
    conn.commit()

    cur.close()
    conn.close()
    input('Berhasil! Jangan lupa untuk mengubah status penyewaan setelah pelanggan meminjam. Tekan enter untuk melanjutkan')    


def ganti_password_pengurus(id_pengurus_rental):
    conn = koneksi.create_connection()
    cur = conn.cursor()
    try:
        # Meminta password baru
        while True:
            password_baru = getpass.getpass("Masukkan password baru: ")
            password_baru2 = getpass.getpass("Masukkan password yang sama: ")

            if password_baru == password_baru2:
                query_update = "UPDATE pengurus_rental SET password = %s WHERE id_pengurus_rental = %s"
                cur.execute(query_update, (password_baru, id_pengurus_rental))
                conn.commit()
                print('Password telah diganti. Tekan enter untuk lanjut.')
                input()
                break
            else:
                print('''
1. Coba lagi
2. Keluar
''')
                pilih = input("Masukkan pilihan: ")
                if pilih == '1':
                    continue
                elif pilih == '2':
                    break
                else:
                    print('Masukkan yang sesuai dengan opsi yang diberikan')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()