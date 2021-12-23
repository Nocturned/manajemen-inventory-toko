import mysql.connector as mysql


def truncateInventory():
    conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
    c = conn.cursor()

    try:
        c.execute("TRUNCATE TABLE tb_inventory")
        conn.commit()

        print('Berhasil mengosongkan tabel tb_inventory....')
    except:
        print('Gagal mengosongkan tabel tb_inventory....')
        conn.rollback()
    finally:
        conn.close()

def truncateDetailBarang():
    conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
    c = conn.cursor()

    try:
        c.execute("TRUNCATE TABLE tb_detail_barang")
        conn.commit()

        print('Berhasil mengosongkan tabel tb_detail_barang....')
    except:
        print('Gagal mengosongkan tabel tb_detail_barang....')
        conn.rollback()
    finally:
        conn.close()

def inputInventory():
    conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO `tb_inventory` (`id_barang`, `nama`, `qty`, `dibuat`, `diubah`, `status_data`) VALUES
            (1, 'Pulpen', 40, '2021-12-22 10:29:57', NULL, 'Aktif'),
            (2, 'Pensil', 40, '2021-12-22 10:29:57', NULL, 'Aktif'),
            (3, 'Penggaris', 30, '2021-12-22 10:29:57', NULL, 'Aktif'),
            (4, 'Penghapus', 35, '2021-12-22 10:29:57', NULL, 'Aktif'),
            (5, 'Rautan', 15, '2021-12-22 10:29:57', NULL, 'Aktif'),
            (6, 'Tip-X', 20, '2021-12-22 10:29:57', NULL, 'Aktif'),
            (7, 'Correction Tape', 20, '2021-12-22 10:29:57', NULL, 'Aktif'),
            (8, 'Lem Kertas', 20, '2021-12-22 10:29:57', NULL, 'Aktif'),
            (9, 'Flashdisk 4gb', 10, '2021-12-22 10:31:17', NULL, 'Aktif'),
            (10, 'Flashdisk 8gb', 15, '2021-12-22 10:32:45', NULL, 'Aktif'),
            (11, 'Mouse', 20, '2021-12-22 10:33:03', NULL, 'Aktif'),
            (12, 'Keyboard ', 10, '2021-12-22 10:34:16', NULL, 'Aktif'),
            (13, 'Headset', 10, '2021-12-22 10:35:46', NULL, 'Aktif'),
            (14, 'Pisau', 15, '2021-12-22 10:36:14', NULL, 'Aktif'),
            (15, 'Talenan', 10, '2021-12-22 10:36:28', NULL, 'Aktif'),
            (16, 'Sabun Cair', 30, '2021-12-22 10:36:59', NULL, 'Aktif'),
            (17, 'Sabun Batang', 20, '2021-12-22 10:37:24', NULL, 'Aktif'),
            (18, 'Shampoo', 25, '2021-12-22 10:37:51', NULL, 'Aktif'),
            (19, 'Celana Panjang', 7, '2021-12-22 10:38:19', NULL, 'Aktif'),
            (20, 'Kaos Dalam', 9, '2021-12-22 10:38:45', NULL, 'Aktif');
        """)
        conn.commit()

        print("Berhasil memasukkan data tabel ke tb_inventory....")
    except:
        print("Gagal memasukkan data tabel ke tb_inventory....")
        conn.rollback()
    finally:
        conn.close()

def inputDetailBarang():
    conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO `tb_detail_barang` (`prefix`, `id_barang`, `nama`, `kategori`, `harga`, `jenis_barang`, `dibuat`, `diubah`, `status_data`) VALUES
            ('ATK-', 1, 'Pulpen', 'Alat Tulis Kantor', 3500, 'Ekspor', '2021-12-22 10:29:59', NULL, 'Aktif'),
            ('ATK-', 2, 'Pensil', 'Alat Tulis Kantor', 2500, 'Impor', '2021-12-22 10:29:59', NULL, 'Aktif'),
            ('ATK-', 3, 'Penggaris', 'Alat Tulis Kantor', 6500, 'Impor', '2021-12-22 10:29:59', NULL, 'Aktif'),
            ('ATK-', 4, 'Penghapus', 'Alat Tulis Kantor', 1500, 'Ekspor', '2021-12-22 10:29:59', NULL, 'Aktif'),
            ('ATK-', 5, 'Rautan', 'Alat Tulis Kantor', 2500, 'Impor', '2021-12-22 10:29:59', NULL, 'Aktif'),
            ('ATK-', 6, 'Tip-X', 'Alat Tulis Kantor', 6500, 'Impor', '2021-12-22 10:29:59', NULL, 'Aktif'),
            ('ATK-', 7, 'Correction Tape', 'Alat Tulis Kantor', 13000, 'Impor', '2021-12-22 10:29:59', NULL, 'Aktif'),
            ('ATK-', 8, 'Lem Kertas', 'Alat Tulis Kantor', 2000, 'Impor', '2021-12-22 10:29:59', NULL, 'Aktif'),
            ('ELC-', 9, 'Flashdisk 4gb', 'Elektronik', 35000, 'Impor', '2021-12-22 10:31:17', NULL, 'Aktif'),
            ('ELC-', 10, 'Flashdisk 8gb', 'Elektronik', 60000, '-', '2021-12-22 10:32:45', NULL, 'Aktif'),
            ('ELC-', 11, 'Mouse', 'Elektronik', 45000, 'Ekspor', '2021-12-22 10:33:03', NULL, 'Aktif'),
            ('ELC-', 12, 'Keyboard ', 'Elektronik', 55000, 'Ekspor', '2021-12-22 10:34:16', NULL, 'Aktif'),
            ('ELC-', 13, 'Headset', 'Elektronik', 120000, 'Ekspor', '2021-12-22 10:35:46', NULL, 'Aktif'),
            ('KTC-', 14, 'Pisau', 'Dapur', 35000, '-', '2021-12-22 10:36:14', NULL, 'Aktif'),
            ('KTC-', 15, 'Talenan', 'Dapur', 25000, 'Ekspor', '2021-12-22 10:36:28', NULL, 'Aktif'),
            ('SKC-', 16, 'Sabun Cair', 'Perawatan Tubuh', 40000, '-', '2021-12-22 10:36:59', NULL, 'Aktif'),
            ('SKC-', 17, 'Sabun Batang', 'Perawatan Tubuh', 2000, 'Impor', '2021-12-22 10:37:24', NULL, 'Aktif'),
            ('SKC-', 18, 'Shampoo', 'Perawatan Tubuh', 33500, 'Ekspor', '2021-12-22 10:37:51', NULL, 'Aktif'),
            ('FSH-', 19, 'Celana Panjang', 'Fashion', 25000, '-', '2021-12-22 10:38:19', NULL, 'Aktif'),
            ('FSH-', 20, 'Kaos Dalam', 'Fashion', 23000, 'Impor', '2021-12-22 10:38:45', NULL, 'Aktif');
        """)
        conn.commit()

        print("Berhasil memasukkan data ke tabel tb_detail_barang....")
    except:
        print("Gagal memasukkan data ke tabel tb_detail_barang....")
        conn.rollback()
    finally:
        conn.close()


truncateInventory()
truncateDetailBarang()
inputInventory()
inputDetailBarang()