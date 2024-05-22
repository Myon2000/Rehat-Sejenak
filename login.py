import getpass
import os
import koneksi

def login_pengurus():
    conn = koneksi.create_connection()
    cur = conn.cursor()

    os.system('cls')
    username = input('Masukkan username pengurus: ')
    password = getpass.getpass('Masukkan password: ')
    try:
        
        query_login = "SELECT id_pengurus_rental, nama FROM pengurus_rental WHERE nama = %s AND password = %s"
        cur.execute(query_login, (username, password))

        pengurus = cur.fetchone()

        if pengurus:
            return {'id': pengurus[0], 'nama': pengurus[1]}
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def registrasi_pelanggan():
    conn = koneksi.create_connection()
    cur = conn.cursor()

    os.system('cls')
    nama = input('Masukkan nama Anda: ')
    nomor_telepon = input('Masukkan nomor telepon Anda: ')
    alamat_email = input('Masukkan alamat email Anda: ')
    alamat = input('Masukkan alamat Anda: ')
    password = getpass.getpass('Masukkan password pilihan Anda: ')

    query_register = "INSERT INTO pelanggan (nama, nomor_telepon, alamat_email, alamat, password) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(query_register, (nama, nomor_telepon, alamat_email, alamat, password))
    conn.commit()
    cur.close()
    conn.close()

    input('Akun Anda berhasil dibuat! Tekan enter untuk kembali ke menu login.')

def login_pelanggan():
    conn = koneksi.create_connection()
    cur = conn.cursor()

    os.system('cls')
    username = input('Masukkan username/email/nomor telepon Anda: ')
    password = getpass.getpass('Masukkan password: ')
    try:
        # Menjalankan query untuk mendapatkan data pengguna
        query_login = "SELECT id_pelanggan, nama FROM pelanggan WHERE %s in (nama, nomor_telepon, alamat_email) AND password = %s"
        cur.execute(query_login, (username, password))

        # Mendapatkan hasil query
        pelanggan = cur.fetchone()

        if pelanggan:
            return {'id': pelanggan[0], 'nama': pelanggan[1]}
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        cur.close()
        conn.close()