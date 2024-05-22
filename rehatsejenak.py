import os

# Biar rapih dikit
import login
import pengurus
import pelanggan

while True:
    os.system('cls')
    print('''
||======================================||
||    Selamat datang di RehatSejenak    ||
||  Silahkan pilih penggunaan aplikasi: ||
||                                      ||
||           [1] Pengurus               ||
||           [2] Pelanggan              ||
||           [3] Akhiri Program         ||
||======================================||
''')
    pengguna = input('Masukan: ')
    match pengguna:
        case '1':
            while True:
                autentikasi = login.login_pengurus()
                if autentikasi:
                    input('Autentikasi berhasil! Tekan enter untuk melanjutkan')
                    print("Berhasil Masuk")
                    pengurus.pengurus(autentikasi['id'], autentikasi['nama'])
                    break
                else:
                    print('Username atau password salah!')
                    print('''
||======================================||
||           [1] Coba lagi              ||
||           [2] Kembali                ||
||======================================||
''')
                    a = input('Masukan: ')
                    if a == '1':
                        continue
                    elif a == '2':
                        break
                    else:
                        input('Pilihan tidak valid! Kembali ke menu awal')
                        break
        case '2':
            while True:
                os.system('cls')
                print('''
||======================================||
||           [1] Login                  ||
||           [2] Buat akun baru         ||
||======================================||
                      ''')
                a = input('Masukan: ')
                if a == '2':
                    login.registrasi_pelanggan()
                    continue
                elif a == '1':
                    autentikasi = login.login_pelanggan()
                    if autentikasi:
                        input('Autentikasi berhasil! Tekan enter untuk melanjutkan')
                        print("Berhasil Masuk")
                        pelanggan.pelanggan(autentikasi['id'], autentikasi['nama'])
                        break
                    else:
                        print('Username atau password salah!')
                        print('''
||======================================||
||           [1] Coba lagi              ||
||           [2] Kembali                ||
||======================================||
                        ''')
                        a = input('Masukan: ')
                        if a == '1':
                            continue
                        elif a == '2':
                            break
                        else:
                            input('Pilihan tidak valid! Kembali ke menu awal')
                            break
                else:
                    input('Pilihan tidak valid! Silahkan coba lagi')
        case '3':
            break