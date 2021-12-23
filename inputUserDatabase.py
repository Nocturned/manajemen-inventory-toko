import mysql.connector as mysql
import hashlib


from Resources.veryVerySecret import *


# Membuat database dan tabel jika belum ada
def createDatabase():
    conn = mysql.connect(user="root", password="", host="localhost", port='3306')
    c = conn.cursor()
    try:
        c.execute("CREATE DATABASE IF NOT EXISTS db_Inventory_Toko")
        conn.commit()
        print("Berhasil membuat database....")
    except:
        print("Gagal membuat database....")
        conn.rollback()
    finally:
        conn.close()

def createTable():
    conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
    c = conn.cursor()

    try:
        c.execute("""CREATE TABLE IF NOT EXISTS tb_Inventory (
            id_barang INT(3) UNSIGNED NOT NULL AUTO_INCREMENT,
            nama VARCHAR(255) NOT NULL,
            qty INT(4) UNSIGNED NOT NULL,
            dibuat DATETIME NULL,
            diubah DATETIME NULL,
            status_data VARCHAR(255) NULL,
            PRIMARY KEY (id_barang),
            UNIQUE KEY (nama),
            INDEX (nama, qty)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1
            """)

        c.execute("""CREATE TABLE IF NOT EXISTS tb_Detail_Barang (
            prefix VARCHAR(4) NOT NULL DEFAULT 'ITM-',
            id_barang INT(3) UNSIGNED NOT NULL AUTO_INCREMENT,
            nama VARCHAR(255) NOT NULL,
            kategori VARCHAR(255) NOT NULL,
            harga INT(9) UNSIGNED NOT NULL,
            jenis_barang VARCHAR(255) NOT NULL,
            dibuat DATETIME NULL,
            diubah DATETIME NULL,
            status_data VARCHAR(255) NULL,
            PRIMARY KEY (id_barang),
            UNIQUE KEY (prefix, id_barang),
            UNIQUE KEY (nama),
            INDEX (nama, kategori, harga)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1
        """)

        c.execute("""CREATE TABLE IF NOT EXISTS tb_User (
            username VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255) NOT NULL,
            dibuat DATETIME NULL,
            diubah DATETIME NULL,
            status_data VARCHAR(255) NULL
            )
        """)

        c.execute("""CREATE TABLE IF NOT EXISTS tb_Riwayat_Pembelian (
            id_struk INT(3) UNSIGNED NOT NULL AUTO_INCREMENT,
            nama VARCHAR(255) NOT NULL,
            qty INT(4) NOT NULL,
            total INT(9) NOT NULL,
            dibuat DATETIME NULL,
            diubah DATETIME NULL,
            status_data VARCHAR(255) NULL,
            PRIMARY KEY (id_struk)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1
        """)
        conn.commit()
        
        print("Berhasil membuat tabel....")
    except:
        print("Gagal membuat tabel....")
        conn.rollback()
    finally:
        conn.close()

def truncateUser():
    conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
    c = conn.cursor()

    try:
        c.execute("TRUNCATE TABLE tb_user")
        conn.commit()
        print('Berhasil mengosongkan tabel tb_user....')
    except:
        print('Gagal mengosongkan tabel tb_user....')
        conn.rollback()
    finally:
        conn.close()

def inputAdmin():
    conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO tb_user(username,password) VALUES(%s,%s)",
        (admin,passAdminHashed))
        conn.commit()
        print('Berhasil menginput user "Admin"....')
    except:
        print('Gagal menginput user "Admin"....')
        conn.rollback()
    finally:
        conn.close()

def inputKasir():
    conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO tb_user(username,password) VALUES(%s,%s)",
        (kasir,passKasirHashed))
        conn.commit()
        print('Berhasil menginput user "Kasir"....')
    except:
        print('Gagal menginput user "Kasir"....')
        conn.rollback()
    finally:
        conn.close()


createDatabase()

createTable()


"""
Username:Password = Admin:123123
Username:Password = Manajer:123321
Username:Password = Kasir:112233
"""

admin = 'Admin'
kasir = 'Kasir'

passwordAdmin = notAdminPassword() + notSalt()
passwordKasir = notKasirPassword() + notSalt()


passAdminEnc = passwordAdmin.encode()
passKasirEnc = passwordKasir.encode()


passAdminHashed = hashlib.sha256(passAdminEnc).hexdigest()
passKasirHashed = hashlib.sha256(passKasirEnc).hexdigest()


truncateUser()

inputAdmin()

inputKasir()