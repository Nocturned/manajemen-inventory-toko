from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import *
import mysql.connector as mariadb
import datetime


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
        dibuat datetime null,
        diubah datetime null,
        status_data VARCHAR(255) null,
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
    hari_ini = datetime.datetime.now()
    
    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()
    
    validasiSemua()
    if valid == True:
        try:
            c.execute("INSERT INTO tb_inventory (prefix,nama,qty,harga,kategori,dibuat,status_data) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (prefix,nama,qty,harga,kategori,hari_ini,'Aktif'))
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
    hari_ini = datetime.datetime.now()
    
    nama = txt_nama.get()
    qty = int(txt_qty.get())
    harga = int(txt_harga.get())

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    validasiSemua()
    if valid == True:
        try:
            c.execute("UPDATE tb_inventory SET prefix=%s,nama=%s,qty=%s,harga=%s,kategori=%s,diubah=%s WHERE id=%s",
            (prefix,nama,qty,harga,kategori,hari_ini,id_barang))
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
    hari_ini = datetime.datetime.now()

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()
    
    try:
        c.execute("UPDATE tb_inventory SET diubah=%s, status_data=%s WHERE id=%s",
        (hari_ini,"Tidak Aktif", id_barang))
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

def restoreData():
    hari_ini = datetime.datetime.now()

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()
    
    try:
        c.execute("UPDATE tb_inventory SET diubah=%s, status_data=%s WHERE id=%s",
        (hari_ini, "Aktif", id_barang))
        conn.commit()

        messagebox.showinfo("information", "Barang Berhasil Diambil Dari Gudang")
        showInventory()
    except Exception as e:
       messagebox.showinfo("information", e)
       conn.rollback()
       conn.close()
    

# Mencari data ditabel berdasarkan nama dan atau kategori
def callback(sv):
    global cari, kategori

    if cmb_pilih_kategori.get() == lst_pilih_kategori[0]:
        frm_tabel.destroy()
        kategori = ''
        showCari()
    elif cmb_pilih_kategori.get() == lst_pilih_kategori[1]:
        frm_tabel.destroy()
        kategori = lst_pilih_kategori[1]
        showCari()
    elif cmb_pilih_kategori.get() == lst_pilih_kategori[2]:
        frm_tabel.destroy()
        kategori = lst_pilih_kategori[2]
        showCari()

    cari = txt_cari.get()
    showCari()


# Mengambil nilai dari tabel berdasarkan klick
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

def GetValueRecycleBin(event):
    global id_barang, harga

    txt_nama.delete(0, END)
    txt_qty.delete(0, END)
    txt_harga.delete(0, END)
    rowID = listBoxRecycle.selection()[0]
    select = listBoxRecycle.set(rowID)

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

    print(id_barang, kategori_id)


# Menunjukkan tabel dari database berdasarkan kategori
def kategoriShowBarang(e):
    global kategori

    if cmb_pilih_kategori.get() == lst_pilih_kategori[0]:
        frm_tabel.destroy()
        kategori = ''
        showCari()
    elif cmb_pilih_kategori.get() == lst_pilih_kategori[1]:
        frm_tabel.destroy()
        kategori = lst_pilih_kategori[1]
        showCari()
    elif cmb_pilih_kategori.get() == lst_pilih_kategori[2]:
        frm_tabel.destroy()
        kategori = lst_pilih_kategori[2]
        showCari()


# Menunjukkan tabel dari database
def showInventory():
    global listBox, scrollTree, frm_tabel

    frm_tabel = Frame(root)
    frm_tabel.place(x=20,y=220)
    scrollTree = ttk.Scrollbar(frm_tabel, orient='vertical')
    
    cols = ('ID Barang','Nama','Qty','Harga')
    listBox = ttk.Treeview(frm_tabel, style="listBox.Treeview", columns=cols, show='headings', yscrollcommand=scrollTree.set)
    listBox.pack(side=LEFT)

    scrollTree.config(command=listBox.yview)
    scrollTree.pack(side=RIGHT, fill=Y)

    for col in cols:
        listBox.heading(col, text=col)
        listBox.column('ID Barang', minwidth=0, width=80, stretch=NO, anchor = CENTER)
        listBox.column('Nama', minwidth=0, width=170, stretch=NO, anchor = W)
        listBox.column('Qty', minwidth=0, width=60, stretch=NO, anchor = CENTER)
        listBox.column('Harga', minwidth=0, width=130, stretch=NO, anchor = W)

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    c.execute("SELECT CONCAT(prefix,id)AS id_barang,nama,qty,harga FROM tb_inventory WHERE status_data=%s",("Aktif",))
    record = c.fetchall()
    conn.commit()
    
    for i, (id_barang,nama,qty,harga) in enumerate(record, start=1):
        listBox.insert("", "end", values=(id_barang,nama,qty,"Rp {:,},00-".format(harga)), tags=('ganjil',))
        conn.close()

    listBox.bind('<Single-Button-1>',GetValue)

def showCari():
    global cari
    cari = txt_cari.get()

    frm_tabel = Frame(root)
    frm_tabel.place(x=20,y=220)
    scrollTree = ttk.Scrollbar(frm_tabel, orient='vertical')
    
    cols = ('ID Barang','Nama','Qty','Harga')
    listBox = ttk.Treeview(frm_tabel, style="listBox.Treeview", columns=cols, show='headings', yscrollcommand=scrollTree.set)
    listBox.pack(side=LEFT)

    scrollTree.config(command=listBox.yview)
    scrollTree.pack(side=RIGHT, fill=Y)

    for col in cols:
        listBox.heading(col, text=col)
        listBox.column('ID Barang', minwidth=0, width=80, stretch=NO, anchor = CENTER)
        listBox.column('Nama', minwidth=0, width=170, stretch=NO, anchor = W)
        listBox.column('Qty', minwidth=0, width=60, stretch=NO, anchor = CENTER)
        listBox.column('Harga', minwidth=0, width=130, stretch=NO, anchor = W)

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    c.execute("SELECT CONCAT(prefix,id)AS id_barang,nama,qty,harga FROM tb_inventory WHERE kategori LIKE %s AND nama LIKE %s AND status_data=%s", ("%"+kategori+"%","%"+cari+"%","Aktif"))
    record = c.fetchall()
    conn.commit()
    
    for i, (id_barang,nama,qty,harga) in enumerate(record, start=1):
        listBox.insert("", "end", values=(id_barang,nama,qty,"Rp {:,},00-".format(harga)))
        conn.close()

    listBox.bind('<Single-Button-1>',GetValue)

def showRecycleBin():
    global listBoxRecycle, scrollTree, frm_recycle

    frm_recycle = Frame(top)
    frm_recycle.place(x=20,y=80)
    scrollTree = ttk.Scrollbar(frm_recycle, orient='vertical')
    
    cols = ('ID Barang','Nama','Qty','Harga')
    listBoxRecycle = ttk.Treeview(frm_recycle, style="listBox.Treeview",  columns=cols, show='headings', yscrollcommand=scrollTree.set)
    listBoxRecycle.pack(side=LEFT)

    scrollTree.config(command=listBoxRecycle.yview)
    scrollTree.pack(side=RIGHT, fill=Y)

    for col in cols:
        listBoxRecycle.heading(col, text=col)
        listBoxRecycle.column('ID Barang', minwidth=0, width=80, stretch=NO, anchor = CENTER)
        listBoxRecycle.column('Nama', minwidth=0, width=170, stretch=NO, anchor = W)
        listBoxRecycle.column('Qty', minwidth=0, width=60, stretch=NO, anchor = CENTER)
        listBoxRecycle.column('Harga', minwidth=0, width=130, stretch=NO, anchor = W)

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    c.execute("SELECT CONCAT(prefix,id)AS id_barang,nama,qty,harga FROM tb_inventory WHERE status_data=%s",("Tidak Aktif",))
    record = c.fetchall()
    conn.commit()
    
    for i, (id_barang,nama,qty,harga) in enumerate(record, start=1):
        listBoxRecycle.insert("", "end", values=(id_barang,nama,qty,"Rp {:,},00-".format(harga)), tags=('ganjil',))
        conn.close()

    listBoxRecycle.bind('<Single-Button-1>', GetValueRecycleBin)
    showInventory()


# Window GUI program
def windowUtama():
    global root, sv, kategori
    global txt_nama, txt_qty, txt_harga, cmb_kategori, txt_cari, cmb_pilih_kategori
    global btn_tambah, btn_edit, btn_hapus, btn_recycle_bin
    global lst_kategori, lst_pilih_kategori

    root = Tk()
    sv = StringVar()
    root.title("Manajemen Inventory Toko BlaBlaBla")
    root.geometry("500x470")
    root.resizable(False, False)
    root.protocol('WM_DELETE_WINDOW', lambda: [root.destroy(), top.destroy()])

    theme = ttk.Style()
    theme.theme_use('clam')
    theme.configure("listBox.Treeview.Heading", font=('Lucida Sans', 10, 'bold'), foreground="#FFFFFF", background="#009DFF", borderwidth=0)
    theme.configure("listBox.Treeview", fieldbackground="#D0D0D0")

    lst_kategori = ['Alat Tulis Kantor', 'Elektronik']
    lst_pilih_kategori = ['Semua', 'Alat Tulis Kantor', 'Elektronik']

    lbl_nama = Label(root, font=("Lucida Sans", 13), text="Nama").place(x=20,y=30)
    lbl_qty = Label(root, font=("Lucida Sans", 13), text="Qty").place(x=20,y=60)
    lbl_harga = Label(root, font=("Lucida Sans", 13), text="Harga").place(x=20,y=90)
    lbl_cari = Label(root, font=("Lucida Sans", 10), text="Cari :").place(x=20,y=190)
    lbl_pilih_kategori = Label(root, font=("Lucida Sans", 10), text="Kategori :").place(x=277,y=189)
    
    txt_nama = Entry(root,width=15, font=("Lucida Sans", 10))
    txt_nama.place(x=90,y=32)

    txt_qty = Entry(root, width=15, font=("Lucida Sans", 10))
    txt_qty.place(x=90,y=62)

    txt_harga = Entry(root,width=15, font=("Lucida Sans", 10))
    txt_harga.place(x=90,y=92)

    cmb_kategori = ttk.Combobox(root, state="readonly", font=("Lucida Sans",10), value=lst_kategori, width=14)
    cmb_kategori.set("Pilih Kategori")
    cmb_kategori.place(x=90,y=120)

    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
    txt_cari = Entry(root, width=15, textvariable=sv, font=("Lucida Sans", 10))
    txt_cari.place(x=60,y=192)

    cmb_pilih_kategori = ttk.Combobox(root, state="readonly", value=lst_pilih_kategori, width=13, font=("Lucida Sans",10))
    cmb_pilih_kategori.bind("<<ComboboxSelected>>", kategoriShowBarang)
    cmb_pilih_kategori.set(lst_pilih_kategori[0])
    cmb_pilih_kategori.place(x=343,y=190)

    btn_tambah = Button(root, text="Tambah", width=15, font=("Lucida Sans",10), command=lambda: [tambahData()]).place(x=290,y=30)
    btn_edit = Button(root, text="Edit", width=15, font=("Lucida Sans",10), command=lambda: [editData()]).place(x=290,y=60)
    btn_hapus = Button(root, text="Hapus", width=15, font=("Lucida Sans",10), command=lambda: [hapusData()]).place(x=290,y=90)
    btn_recycle_bin = Button(root, text="🗑️Recycle Bin", font=("Lucida Sans",10), width=15, command=lambda: [windowRecycleBin(), root.withdraw()]).place(x=290,y=120)

    showInventory()
    mainloop()

def windowRecycleBin():
    global top
    global btn_restore

    top = Toplevel()
    top.title("Recycle Bin")
    top.geometry("500x340")
    top.resizable(False, False)
    top.protocol('WM_DELETE_WINDOW', lambda: [root.deiconify(), top.withdraw()])

    lbl_nama = Label(top, font=("Lucida Sans", 16), text="Pilih data untuk direstore").place(x=20,y=10)

    btn_restore = Button(top, text="Restore",font=("Lucida Sans",10), command=lambda: [restoreData(), listBoxRecycle.destroy(), showRecycleBin()]).place(x=20,y=45)

    showRecycleBin()


createDatabase()
createTable()
windowUtama()
