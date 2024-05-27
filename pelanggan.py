import koneksi
import datetime
import getpass
import os
from tabulate import tabulate

def pelanggan(id, nama):
    while True:
        os.system('cls')
        print(f'''
Selamat datang di RehatSejenak, {nama}
[1] Ajukan penyewaan daring
[2] Lihat status penyewaan
[3] Lihat status transaksi
[4] Ganti Password
[5] Logout
    ''')
        pilihan = input('Masukan: ')
        match pilihan:
            case '1':
                ajukan_penyewaan_daring(id)
            case '2':
                lihat_status_penyewaan(id)
            case '3':
                lihat_status_transaksi(id)
            case '4':
                ganti_password_setelah_login(id)
            case '5':
                break

def ajukan_penyewaan_daring(id_pelanggan):
    os.system('cls')
    conn = koneksi.create_connection()
    cur = conn.cursor()

    while True:
        akhir = input('Masukkan tanggal akhir sewa (yyyy-mm-dd): ')
        # Memastikan tanggalnya valid. Jika tidak, tanya lagi
        try: akhir_datetime = datetime.datetime.strptime(akhir + ' 00:00', '%Y-%m-%d %H:%M')
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
                a.append(f"Tidak tersedia (hingga {i[3].strftime('%Y-%m-%d %H:%M')})")
            else:
                a.append('Tersedia')
            tabel.append(a)
        print(tabulate(tabel))

        konsol = input('Masukkan id konsol yang disewa: ')
        if not konsol.isnumeric():
            print('id tidak valid!')
            continue

        query_konsol = '''
SELECT k.id_konsol, k.harga_sewa_per_hari, p.id_penyewaan is null as tersedia
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

    sekarang = datetime.datetime.now()
    hari_ini = sekarang.replace(hour=0, minute=0, second=0, microsecond=0)
    hari = (akhir_datetime - hari_ini).days
    harga_sewa_akhir = konsol[1] * hari

    query = '''INSERT INTO penyewaan
        (tanggal_awal_sewa, tanggal_akhir_sewa, id_konsol,
        biaya, id_pelanggan, id_status_penyewaan)
        VALUES (%s, %s, %s, %s, %s, 1)
        RETURNING id_penyewaan'''
    cur.execute(query, (hari_ini, akhir_datetime, konsol[0], harga_sewa_akhir, id_pelanggan))
    id_baru = cur.fetchone()[0]

    query2 = '''INSERT INTO transaksi
        (biaya, tanggal_dibuat, id_penyewaan)
        VALUES (%s, %s, %s)'''
    cur.execute(query2, (harga_sewa_akhir, sekarang, id_baru))
    conn.commit()

    print(f'''
Data ditambahkan
Tanggal awal: {hari_ini.strftime('%Y-%m-%d')}
Tanggal akhir: {akhir}
Biaya: {harga_sewa_akhir}
ID Konsol: {konsol[0]}
''')
    input('Silahkan pilih menu transaksi untuk mengurus pembayaran. Tekan enter untuk melanjutkan')

    cur.close()
    conn.close()

def lihat_status_penyewaan(id_pelanggan):
    os.system('cls')
    conn = koneksi.create_connection()
    cur = conn.cursor()
    query = '''SELECT p.tanggal_awal_sewa, p.tanggal_akhir_sewa, p.biaya, jk.nama_jenis, sp.deskripsi_status,
            t.kode_transaksi is not null as sudah_dibayar, t.id_pengurus_rental is not null as sudah_dikonfirmasi
            FROM penyewaan p
            JOIN konsol k ON (k.id_konsol = p.id_konsol)
            JOIN jenis_konsol jk ON (jk.id_jenis_konsol = k.id_jenis_konsol)
            JOIN status_penyewaan sp ON (sp.id_status_penyewaan = p.id_status_penyewaan)
            JOIN transaksi t ON (t.id_penyewaan = p.id_penyewaan)
            WHERE p.id_pelanggan = %s'''

    cur.execute(query, (id_pelanggan,))
    list_penyewaan = cur.fetchmany()

    tabel = [['Tanggal awal sewa', 'Tanggal akhir sewa', 'Biaya', 'Konsol yang disewa', 'Status penyewaan', 'Status transaksi']]
    for i in list_penyewaan:
        a = []
        a.append(i[0].strftime('%Y-%m-%d'))
        a.append(i[1].strftime('%Y-%m-%d'))
        a.append(i[2])
        a.append(i[3])
        a.append(i[4])
        # Sudah dibayar, sudah dikonfirmasi
        if i[6] and i[5]:
            a.append('Sudah dikonfirmasi')
        # Sudah dibayar, belum dikonfirmasi
        elif not i[6] and i[5]:
            a.append('Belum dikonfirmasi')
        # Belum dibayar
        else:
            a.append('Belum dibayar')
        tabel.append(a)
    print(tabulate(tabel))
    cur.close()
    conn.close()
    input('Tekan enter untuk melanjutkan')

def lihat_status_transaksi(id_pelanggan):
    conn = koneksi.create_connection()
    cur = conn.cursor()
    query = '''SELECT t.id_transaksi, t.biaya, t.tanggal_dibuat, t.kode_transaksi, pr.nama, jk.nama_jenis
FROM transaksi t
LEFT JOIN pengurus_rental pr ON (pr.id_pengurus_rental = t.id_pengurus_rental)
JOIN penyewaan p ON (p.id_penyewaan = t.id_penyewaan)
JOIN konsol k ON (k.id_konsol = p.id_konsol)
JOIN jenis_konsol jk ON (jk.id_jenis_konsol = k.id_jenis_konsol)
WHERE p.id_pelanggan = %s'''

    cur.execute(query, (id_pelanggan,))
    list_transaksi = cur.fetchall()
    tabel = [['id', 'Biaya', 'Tanggal dibuat', 'Kode transaksi', 'Dikonfirmasi oleh', 'Konsol yang disewa']]

    for i in list_transaksi:
        tabel.append([
            i[0],
            i[1],
            i[2],
            i[3] or '<belum dibayar>',
            i[4] or '<belum dikonfirmasi>',
            i[5]
        ])
    print(tabulate(tabel))

    while True:
        id = input('Pilih id transaksi yang ingin dibayar: ')
        if not id.isnumeric():
            print('id tidak valid!')
            continue
        query_select = '''SELECT t.kode_transaksi, t.biaya
                FROM transaksi t
                JOIN penyewaan p ON (t.id_penyewaan = p.id_penyewaan)
                WHERE t.id_transaksi = %s AND p.id_pelanggan = %s'''
        cur.execute(query_select, (id,id_pelanggan))
        transaksi = cur.fetchone()

        if not transaksi:
            print('Penyewaan tidak ditemukan!')
            continue
        elif transaksi[0]:
            print('Transaksi sudah dibayar!')
            continue
        break

    print(f'Transfer Rp. {transaksi[1]} ke rekening 12345678 (Mandiri A/N Bima Putra)')
    while True:
        kode = input('Masukkan kode transaksi (12 digit): ')[0:12]
        print(f'''
Transaksi dilakukan dengan kode {kode}. Lanjutkan?
[1] Ya
[2] Kembali
''')
        pilihan = input()
        if pilihan == '2': continue
        elif pilihan == '1':
            break
        else:
            print('Pilihan tidak valid!')

    query_update = 'UPDATE transaksi SET kode_transaksi = %s WHERE id_transaksi = %s'
    cur.execute(query_update, (kode, id))
    conn.commit()

    cur.close()
    conn.close()
    input('Berhasil! Silahkan menunggu konfirmasi oleh pengurus rental. Tekan enter untuk melanjutkan')


def ganti_password_setelah_login(id_pelanggan):
    conn = koneksi.create_connection()
    cur = conn.cursor()
    try:
        # Meminta password baru
        while True:
            password_baru = getpass.getpass("Masukkan password baru: ")
            password_baru2 = getpass.getpass("Masukkan password yang sama: ")

            if password_baru == password_baru2:
                query_update = "UPDATE pelanggan SET password = %s WHERE id_pelanggan = %s"
                cur.execute(query_update, (password_baru, id_pelanggan))
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


    #UPDATE
# UPDATE nama_tabel SET nama_kolom = value _kolom
# endog = f"UPDATE mata_kuliah SET matkul = %s, sks = %s, semester_id = %s"

# # read_matkul(cur=cur)

# endog_select = "SELECT * FROM mata_kuliah"
# cur.execute(endog_select)
# data = cur.fetchall()
# for i in data:
#     print(i)


# id_matkul = input('Masukkan id mata kuliah yang ingin diupdate : ')
# select_endog = "SELECT * FROM mata_kuliah WHERE id_matkul = id_matkul"
# cur.execute(select_endog, (id_matkul))
# data2 = cur.fetchone()
# # if data2:
# #     print('Data saat ini : ')
# #     print (f'id mata kuliah saat ini : {data2[0]}')
# #     print (f'mata kuliah saat ini : {data2[1]}')
# #     print (f'semester saat ini : {data2[2]}')



# nama_matkul = input(f"masukkan nama matkul : ") or data2[1]
# jumlah_sks = int(input(f"masukkan jumlah sks : ")) or data2 [2]
# semester_id = int(input(f"masukkan id semester : ")) or data2[3]

# endog_update = f"UPDATE mata_kuliah SET matkul = %s, sks = %s, semester_id = %s WHERE id_matkul = %s"
# cur.execute(query=endog_update, vars=(nama_matkul, jumlah_sks, semester_id, id_matkul))

# conn.commit()
# print(f'total baris yang diubah : {cur.rowcount}')

# cur.close()
# conn.close()