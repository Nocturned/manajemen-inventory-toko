from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import *
import mysql.connector as mariadb
import datetime
import traceback


# Membuat database dan table jika belum ada
def createDatabase():
    conn = mariadb.connect(user="root", password="", host="localhost", port='3306')
    c = conn.cursor()

    c.execute("CREATE DATABASE IF NOT EXISTS db_inventoryToko")
    conn.commit()

    conn.close()

def createTable():
    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS tb_inventory (
        prefix VARCHAR(4) NOT NULL DEFAULT 'ITM-',
        id int(3) UNSIGNED NOT NULL AUTO_INCREMENT,
        nama VARCHAR(255) NOT NULL,
        qty INT(4),
        harga INT(9),
        kategori VARCHAR(255) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE KEY (prefix, id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1
        """)
    conn.commit()

    conn.close()


# Validasi
def validasiNama():
    global nama, nama_value

    if txt_nama.get() == '':
        nama = ''
        nama_value = False
        messagebox.showinfo("Error", "Harap masukkan nama !")
    else:
        nama = txt_nama.get()
        nama_value = True

def validasiQty():
    global qty, qty_value

    qty_temp = txt_qty.get()

    if qty_temp == '':
        qty = ''
        qty_value = False
        messagebox.showinfo("Error", "Harap masukkan qty !")
    elif qty_temp.isdigit() == False:
        qty = ''
        qty_value = False
        messagebox.showinfo("Error", "Format qty belum benar !")
    elif int(qty_temp) < 0:
        qty = ''
        qty_value = False
        messagebox.showinfo("Error", "Jumlah barang tidak boleh kurang dari 0 !")
    elif int(qty_temp) > 100:
        qty = ''
        qty_value = False
        messagebox.showinfo("Error", "Jumlah maksimal barang adalah 100 !")
    elif qty_temp.isdigit() == True:
        qty = int(qty_temp)
        qty_value = True

def validasiHarga():
    global harga, harga_value

    harga_temp = txt_harga.get()

    if harga_temp == '':
        harga = ''
        harga_value = False
        messagebox.showinfo("Error", "Harap masukkan harga !")
    elif harga_temp.isdigit() == False:
        harga = ''
        harga_value = False
        messagebox.showinfo("Error", "Format harga belum benar !")
    elif harga_temp.isdigit() == True:
        if int(harga_temp) < 500:
            harga = ''
            harga_value = False
            messagebox.showinfo("Error", "Harga barang minimal adalah Rp 500,00- !")
        elif int(harga_temp) % 500 != 0:
            harga = ''
            harga_value = False
            messagebox.showinfo("Error", "Harga barang hanya boleh kelipatan Rp 500,00- !")
        elif int(harga_temp) > 999999999:
            harga = ''
            harga_value = False
            messagebox.showinfo("Error", "Batas maksimal harga barang adalah Rp 999,999,999,00- !")
        else:
            harga = int(harga_temp)
            harga_value = True

def validasiKategori():
    global kategori, prefix, kategori_value

    if cmb_kategori.get() == "Pilih Kategori":
        prefix = False
        kategori = False
        kategori_value = False
        messagebox.showinfo("Error", "Harap pilih kategori !")
    elif cmb_kategori.get() == lst_kategori[0]:
        prefix = "ATK-"
        kategori = lst_kategori[0]
        kategori_value = True
    elif cmb_kategori.get() == lst_kategori[1]:
        prefix = "ELC-"
        kategori = lst_kategori[1]
        kategori_value = True

def validasiSemua():
    global valid

    valid = False

    validasiNama()
    if nama_value == True:
        validasiQty()
        if qty_value == True:
            validasiHarga()
            if harga_value == True:
                validasiKategori()
                if kategori_value == True:
                    valid = True


# Mengelola data
def tambahData():
    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()
    
    validasiSemua()
    if valid == True:
        try:
            c.execute("INSERT INTO tb_inventory (prefix,nama,qty,harga,kategori) VALUES (%s, %s, %s, %s, %s)",
            (prefix,nama,qty,harga,kategori))
            conn.commit()

            messagebox.showinfo("information", "Barang berhasil ditambah !")

            txt_nama.delete(0, END)
            txt_qty.delete(0, END)
            txt_harga.delete(0, END)
            txt_nama.focus_set()

            listBox.destroy()
            showInventory()
        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()

def editData():
    nama = txt_nama.get()
    qty = int(txt_qty.get())
    harga = int(txt_harga.get())

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    validasiSemua()
    if valid == True:
        try:
            c.execute("UPDATE tb_inventory SET prefix=%s,nama=%s,qty=%s,harga=%s,kategori=%s WHERE id=%s", (prefix,nama,qty,harga,kategori,id_barang))
            conn.commit()

            messagebox.showinfo("information", "Barang berhasil diedit !")

            txt_nama.delete(0, END)
            txt_qty.delete(0, END)
            txt_harga.delete(0, END)
            cmb_kategori.set("Pilih Kategori")
            txt_nama.focus_set()

            listBox.destroy()
            showInventory()

        except Exception as e:
            messagebox.showinfo("information", e)
            conn.rollback()
            conn.close()

def hapusData():
    nama = txt_nama.get()
    qty = int(txt_qty.get())
    harga = int(txt_harga.get())

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()
    
    try:
        c.execute("DELETE FROM tb_inventory WHERE id=%s", (id_barang,))
        conn.commit()

        messagebox.showinfo("information", "Barang berhasil dihapus !")

        txt_nama.delete(0, END)
        txt_qty.delete(0, END)
        txt_harga.delete(0, END)
        cmb_kategori.set("Pilih Kategori")
        txt_nama.focus_set()

        listBox.destroy()
        showInventory()
    except Exception as e:
       messagebox.showinfo("information", e)
       conn.rollback()
       conn.close()


# Klick event pada tabel
def GetValue(event):
    global id_barang, harga

    txt_nama.delete(0, END)
    txt_qty.delete(0, END)
    txt_harga.delete(0, END)
    rowID = listBox.selection()[0]
    select = listBox.set(rowID)

    id_barang_temp = ''.join(select['ID Barang'])
    id_barang = int(id_barang_temp[4:])

    txt_nama.insert(0,select['Nama'])
    txt_qty.insert(0,select['Qty'])
    txt_harga.insert(0,select['Harga'])
    
    kategori_temp = ''.join(select['ID Barang'])
    kategori_id = str(kategori_temp[:3])
    if kategori_id == "ATK":
        kategori = lst_kategori[0]
    elif kategori_id == "ELC":
        kategori = lst_kategori[1]
    cmb_kategori.set(kategori)

    harga_temp = txt_harga.get()
    harga = str(harga_temp.replace(",","")[3:][:-3])
    txt_harga.delete(0, END)
    txt_harga.insert(0, harga)


# Memilih kategori barang berdasarkan cmb
def kategoriShowBarang(e):
    global kategori

    if cmb_pilih_kategori.get() == lst_pilih_kategori[0]:
        frame_tabel.destroy()
        showInventory()
    elif cmb_pilih_kategori.get() == lst_pilih_kategori[1]:
        frame_tabel.destroy()
        kategori = lst_pilih_kategori[1]
        showKategori()
    elif cmb_pilih_kategori.get() == lst_pilih_kategori[2]:
        frame_tabel.destroy()
        kategori = lst_pilih_kategori[2]
        showKategori()


# Fungsi untuk menutup program
def closeProgram():
    root.destroy()
    top.destroy()


# Tabel menunjukkan tabel dari database
def showInventory():
    global listBox, scrollTree, frame_tabel

    frame_tabel = Frame(root)
    frame_tabel.place(x=20,y=170)
    scrollTree = ttk.Scrollbar(frame_tabel, orient='vertical')
    
    cols = ('ID Barang','Nama','Qty','Harga')
    listBox = ttk.Treeview(frame_tabel, columns=cols, show='headings', yscrollcommand=scrollTree.set)
    listBox.pack(side=LEFT)

    scrollTree.config(command=listBox.yview)
    scrollTree.pack(side=RIGHT, fill=Y)

    for col in cols:
        listBox.heading(col, text=col)
        listBox.column('ID Barang', minwidth=0, width=80, stretch=NO, anchor = CENTER)
        listBox.column('Nama', minwidth=0, width=150, stretch=NO, anchor = W)
        listBox.column('Qty', minwidth=0, width=80, stretch=NO, anchor = CENTER)
        listBox.column('Harga', minwidth=0, width=130, stretch=NO, anchor = W)

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    c.execute("SELECT CONCAT(prefix,id)AS id_barang,nama,qty,harga FROM tb_inventory")
    record = c.fetchall()
    conn.commit()
    for i, (id_barang,nama,qty,harga) in enumerate(record, start=1):
        listBox.insert("", "end", values=(id_barang,nama,qty,"Rp {:,},00-".format(harga)))
        conn.close()

    listBox.bind('<Double-Button-1>',GetValue)

def showKategori():
    global listBox, scrollTree, frame_tabel

    frame_tabel = Frame(root)
    frame_tabel.place(x=20,y=170)
    scrollTree = ttk.Scrollbar(frame_tabel, orient='vertical')
    
    cols = ('ID Barang','Nama','Qty','Harga')
    listBox = ttk.Treeview(frame_tabel, columns=cols, show='headings', yscrollcommand=scrollTree.set)
    listBox.pack(side=LEFT)

    scrollTree.config(command=listBox.yview)
    scrollTree.pack(side=RIGHT, fill=Y)

    for col in cols:
        listBox.heading(col, text=col)
        listBox.column('ID Barang', minwidth=0, width=80, stretch=NO, anchor = CENTER)
        listBox.column('Nama', minwidth=0, width=150, stretch=NO, anchor = W)
        listBox.column('Qty', minwidth=0, width=80, stretch=NO, anchor = CENTER)
        listBox.column('Harga', minwidth=0, width=130, stretch=NO, anchor = W)

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    c.execute("SELECT CONCAT(prefix,id)AS id_barang,nama,qty,harga FROM tb_inventory WHERE kategori = '" + kategori + "'")
    record = c.fetchall()
    conn.commit()
    for i, (id_barang,nama,qty,harga) in enumerate(record, start=1):
        listBox.insert("", "end", values=(id_barang,nama,qty,"Rp {:,},00-".format(harga)))
        conn.close()

    listBox.bind('<Double-Button-1>',GetValue)



# Window
def windowUtama():
    global root, svqty
    global txt_nama, txt_qty, txt_harga, cmb_kategori, cmb_pilih_kategori
    global btn_tambah, btn_edit, btn_hapus
    global lst_kategori, lst_pilih_kategori

    root = Tk()
    svqty = StringVar()
    root.title("Manajemen Inventory Toko BlaBlaBla")
    root.geometry("500x420")
    root.resizable(False, False)
    root.protocol('WM_DELETE_WINDOW', closeProgram)

    theme = ttk.Style()
    theme.theme_use('clam')

    jam_sekarang = datetime.datetime.now().hour
    hari_ini = datetime.datetime.now()

    lst_kategori = ['Alat Tulis Kantor', 'Elektronik']
    lst_pilih_kategori = ['Semua', 'Alat Tulis Kantor', 'Elektronik']

    lbl_nama = Label(root, font=("Arial", 13), text="Nama").place(x=20,y=30)
    lbl_qty = Label(root, font=("Arial", 13), text="Qty").place(x=20,y=60)
    lbl_harga = Label(root, font=("Arial", 13), text="Harga").place(x=20,y=90)
    lbl_pilih_kategori = Label(root, font=("Arial", 10), text="Kategori :").place(x=280,y=149)

    txt_nama = Entry(root,width=15, font=("Arial", 10))
    txt_nama.place(x=90,y=32)

    txt_qty = Entry(root, width=15, font=("Arial", 10))
    txt_qty.place(x=90,y=62)

    txt_harga = Entry(root,width=15, font=("Arial", 10))
    txt_harga.place(x=90,y=92)

    cmb_kategori = ttk.Combobox(root, state="readonly", value=lst_kategori, width=17)
    cmb_kategori.set("Pilih Kategori")
    cmb_kategori.place(x=90,y=120)

    cmb_pilih_kategori = ttk.Combobox(root, state="readonly", value=lst_pilih_kategori, width=17)
    cmb_pilih_kategori.bind("<<ComboboxSelected>>", kategoriShowBarang)
    cmb_pilih_kategori.set(lst_pilih_kategori[0])
    cmb_pilih_kategori.place(x=340,y=150)

    btn_tambah = Button(root, text="Tambah", width=15, command=lambda: [tambahData()]).place(x=290,y=30)
    btn_edit = Button(root, text="Edit", width=15, command=lambda: [editData()]).place(x=290,y=60)
    btn_hapus = Button(root, text="Hapus", width=15, command=lambda: [hapusData()]).place(x=290,y=90) 

    # cmb_kelas = ttk.Combobox(root, state="readonly", value=lst_kelas)
    # cmb_kelas.bind("<<ComboboxSelected>>", kelasPenerbangan)
    # cmb_kelas.set("Pilih Kelas")
    # cmb_kelas.place(x=210,y=130)

    # cal_tgl_berangkat = DateEntry(root, selectmode='day', date_pattern='dd-mm-yyyy', mindate=skrgLgkp)
    # cal_tgl_berangkat.delete(0, END)
    # cal_tgl_berangkat.configure(state="readonly")
    # cal_tgl_berangkat.bind("<<DateEntrySelected>>", jamSamaHari)
    # cal_tgl_berangkat.place(x=210,y=160)

    # cmb_jam_berangkat = ttk.Combobox(root, state="readonly", width=8)
    # cmb_jam_berangkat.configure(state='disabled')
    # cmb_jam_berangkat.place(x=210,y=190)

    # txt_jam_datang = Entry(root, width=7)
    # txt_jam_datang.place(x=210,y=220)
    # txt_jam_datang.configure(state='disabled',disabledbackground='white', disabledforeground='black')

    # txt_jml_dewasa = Entry(root,width=4)
    # txt_jml_dewasa.place(x=210,y=250)

    # txt_jml_anak = Entry(root,width=4)
    # txt_jml_anak.place(x=210,y=280)

    # btn_beli_tiket = Button(root, text="Pesan Tiket", command=lambda: [pesanTiket()]).place(x=110,y=330)
    # btn_lihat_riwayat = Button(root, text="Lihat Tabel", command=lambda: [windowTabel(), root.withdraw()]).place(x=200,y=330)
    # btn_selesai = Button(root, text="Selesai", command=lambda: [root.destroy(), top.destroy()]).place(x=160,y=360)


    showInventory()
    mainloop()


createDatabase()
createTable()
windowUtama()