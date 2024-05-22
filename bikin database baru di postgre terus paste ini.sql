CREATE TABLE jenis_konsol (
    id_jenis_konsol SERIAL NOT NULL,
    nama_jenis      TEXT NOT NULL
);

ALTER TABLE jenis_konsol ADD CONSTRAINT jenis_konsol_pk PRIMARY KEY ( id_jenis_konsol );

CREATE TABLE konsol (
    id_konsol               SERIAL NOT NULL,
    harga_sewa_per_jam      INTEGER NOT NULL,
    harga_sewa_per_hari     INTEGER NOT NULL,
    id_jenis_konsol         INTEGER NOT NULL
);

ALTER TABLE konsol ADD CONSTRAINT konsol_pk PRIMARY KEY ( id_konsol );

CREATE TABLE pelanggan (
    id_pelanggan  SERIAL NOT NULL,
    nama          VARCHAR(50) NOT NULL,
    nomor_telepon VARCHAR(15) NOT NULL,
    alamat_email  VARCHAR(50) NOT NULL,
    alamat        VARCHAR(50) NOT NULL,
    password      VARCHAR(50) NOT NULL
);

ALTER TABLE pelanggan ADD CONSTRAINT pelanggan_pk PRIMARY KEY ( id_pelanggan );

CREATE TABLE pengurus_rental (
    id_pengurus_rental SERIAL NOT NULL,
    nama               VARCHAR(50) NOT NULL,
    nomor_telepon      VARCHAR(15) NOT NULL,
    alamat_email       VARCHAR(50) NOT NULL,
    password           VARCHAR(50) NOT NULL
);

ALTER TABLE pengurus_rental ADD CONSTRAINT pengurus_rental_pk PRIMARY KEY ( id_pengurus_rental );

CREATE TABLE penyewaan (
    id_penyewaan        SERIAL NOT NULL,
    tanggal_awal_sewa   TIMESTAMP NOT NULL,
    tanggal_akhir_sewa  TIMESTAMP NOT NULL,
    biaya               INTEGER NOT NULL,
    id_pelanggan        INTEGER,
    id_pengurus_rental  INTEGER,
    id_konsol           INTEGER NOT NULL,
    id_status_penyewaan INTEGER NOT NULL
);

ALTER TABLE penyewaan ADD CONSTRAINT penyewaan_pk PRIMARY KEY ( id_penyewaan );

CREATE TABLE status_penyewaan (
    id_status_penyewaan SERIAL NOT NULL,
    deskripsi_status    VARCHAR(20) NOT NULL
);

ALTER TABLE status_penyewaan ADD CONSTRAINT status_penyewaan_pk PRIMARY KEY ( id_status_penyewaan );

CREATE TABLE transaksi (
    id_transaksi       SERIAL NOT NULL,
    biaya              INTEGER NOT NULL,
    tanggal_dibuat     TIMESTAMP NOT NULL,
    kode_transaksi     CHAR(12),
    id_pengurus_rental INTEGER,
    id_penyewaan       INTEGER NOT NULL
);

ALTER TABLE transaksi ADD CONSTRAINT transaksi_pk PRIMARY KEY ( id_transaksi );

ALTER TABLE konsol
    ADD CONSTRAINT konsol_jenis_konsol_fk FOREIGN KEY ( id_jenis_konsol )
        REFERENCES jenis_konsol ( id_jenis_konsol );

ALTER TABLE penyewaan
    ADD CONSTRAINT penyewaan_konsol_fk FOREIGN KEY ( id_konsol )
        REFERENCES konsol ( id_konsol );

ALTER TABLE penyewaan
    ADD CONSTRAINT penyewaan_pelanggan_fk FOREIGN KEY ( id_pelanggan )
        REFERENCES pelanggan ( id_pelanggan );

ALTER TABLE penyewaan
    ADD CONSTRAINT penyewaan_pengurus_rental_fk FOREIGN KEY ( id_pengurus_rental )
        REFERENCES pengurus_rental ( id_pengurus_rental );

ALTER TABLE penyewaan
    ADD CONSTRAINT penyewaan_status_penyewaan_fk FOREIGN KEY ( id_status_penyewaan )
        REFERENCES status_penyewaan ( id_status_penyewaan );

ALTER TABLE transaksi
    ADD CONSTRAINT transaksi_pengurus_rental_fk FOREIGN KEY ( id_pengurus_rental )
        REFERENCES pengurus_rental ( id_pengurus_rental );

ALTER TABLE transaksi
    ADD CONSTRAINT transaksi_penyewaan_fk FOREIGN KEY ( id_penyewaan )
        REFERENCES penyewaan ( id_penyewaan );

INSERT INTO jenis_konsol(nama_jenis)
VALUES ('PS 3'), 
                ('PS 4'), 
                ('PS 5'), 
                ('XBOX S'), 
                ('Steam Deck');

insert INTO konsol(harga_sewa_per_jam, harga_sewa_per_hari, id_jenis_konsol)
VALUES  (4000, 55000, 1), 
		(5000, 60000, 2), 
		(5500 ,65000, 3), 
		(6000, 80000, 4), 
		(7000, 150000, 5);

INSERT INTO pelanggan(nama, nomor_telepon, alamat_email, alamat, password)
VALUES	('Putra', 081283919323, 'putra@mail.com', 'Jln Manuk Wari no. 15, Jember', 'wasf'),
		('Nanda', 084952347845, 'nanda@mail.com', 'Jln Sumatra Kiri no. 12, Jember', 'wesa'),
		('Ren', 082188384812, 'ren@mail.com', 'Jln Jawir Kanan no. 69, Jember', 'jowo1'),
		('Obi', 081882838489, 'quer@mail.com', 'Jln Senopati no. 72, Jember', 'gowo'),
		('Mahmed', 081828391291, 'mdmd@mail.com', 'Jln Manuk Wari no. 34, Jember', 'bibd');

INSERT INTO pengurus_rental(nama, nomor_telepon, alamat_email, password)
VALUES	('Saiful', 081239491923, 'sekaiju@mail.com', 'seiyuu'),
		('Saito', 083123491924, 'neko@mail.com', 'pola'),
		('Joro', 091224123456, 'saiba@mail.com', 'sekao'),
		('Asep', 082319990012, 'cahyadi@mail.com', 'seno'),
		('Anik', 087345875001, 'organik@mail.com', 'dewan');

INSERT INTO status_penyewaan(deskripsi_status)
VALUES	('Belum Diambil'), 
		('Belum Dikembalikan'), ('Selesai');

INSERT INTO penyewaan(tanggal_awal_sewa, tanggal_akhir_sewa, biaya, id_pelanggan, id_pengurus_rental, id_konsol, id_status_penyewaan)
VALUES	('2023-6-9 15:10:01', '2023-6-10 12:30:03', 26310, 1, NULL, 1, 3),
		('2023-8-4 12:10:34', '2023-8-8 10:30:12', 75700, 2, NULL, 3, 3),
		('2023-8-5 08:00:17', '2023-8-5 17:45:08', 344200, NULL, 5, 3, 3),
		('2023-12-31 11:50:31', '2024-1-05 11:11:11', 500000, 3, NULL, 4, 3),
		('2024-2-25 12:23:12', '2024-2-28 12:00:00', 800000, 5, NULL, 1, 3);

INSERT INTO transaksi(biaya, tanggal_dibuat, kode_transaksi, id_pengurus_rental, id_penyewaan)
VALUES	(26310, '2023-6-9 15:10:01', 'FD298482913H', 1, 1),
		(75700, '2023-8-4 12:10:34', 'AB67483SS32D', 3, 2),
		(500000, '2023-12-31 11:50:31', 'FFS78625LMAO', 1, 4),
		(800000, '2024-2-25 12:23:12', 'CA874239NO3N', 5, 5);