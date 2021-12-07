from tkinter import *
from tkinter import ttk, messagebox
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
        qty INT(4) UNSIGNED,
        harga INT(9) UNSIGNED,
        kategori VARCHAR(255) NOT NULL,
        dibuat datetime null,
        diubah datetime null,
        status_data VARCHAR(255) null,
        PRIMARY KEY (id),
        UNIQUE KEY (prefix, id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1
        """)
    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS tb_riwayat_pembelian (
        id int(3) UNSIGNED NOT NULL AUTO_INCREMENT,
        barang VARCHAR(255) NOT NULL,
        qty INT(4) UNSIGNED,
        total INT(9) UNSIGNED,
        dibuat datetime null,
        diubah datetime null,
        status_data VARCHAR(255) null,
        PRIMARY KEY (id),
        UNIQUE KEY (id)
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
        messagebox.showerror("Error", "Harap masukkan nama barang !")
    else:
        nama = txt_nama.get()
        nama_value = True

def validasiQty():
    global qty, qty_value

    qty_temp = txt_qty.get()

    if qty_temp == '':
        qty = ''
        qty_value = False
        messagebox.showerror("Error", "Harap masukkan qty !")
    elif qty_temp.isdigit() == False:
        qty = ''
        qty_value = False
        messagebox.showerror("Error", "Format qty belum benar !")
    elif int(qty_temp) < 0:
        qty = ''
        qty_value = False
        messagebox.showerror("Error", "Jumlah barang tidak boleh kurang dari 0 !")
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
        messagebox.showerror("Error", "Harap masukkan harga !")
    elif harga_temp.isdigit() == False:
        harga = ''
        harga_value = False
        messagebox.showerror("Error", "Format harga belum benar !")
    elif harga_temp.isdigit() == True:
        if int(harga_temp) < 500:
            harga = ''
            harga_value = False
            messagebox.showerror("Error", "Harga barang minimal adalah Rp 500,00- !")
        elif int(harga_temp) % 500 != 0:
            harga = ''
            harga_value = False
            messagebox.showerror("Error", "Harga barang hanya boleh kelipatan Rp 500,00- !")
        elif int(harga_temp) > 999999999:
            harga = ''
            harga_value = False
            messagebox.showerror("Error", "Batas maksimal harga barang adalah Rp 999,999,999,00- !")
        else:
            harga = int(harga_temp)
            harga_value = True

def validasiKategori():
    global kategori, prefix, kategori_value

    if cmb_kategori.get() == "Pilih Kategori":
        prefix = False
        kategori = False
        kategori_value = False
        messagebox.showerror("Error", "Harap pilih kategori !")
    elif cmb_kategori.get() == lst_kategori[0]:
        prefix = "ATK-"
        kategori = lst_kategori[0]
        kategori_value = True
    elif cmb_kategori.get() == lst_kategori[1]:
        prefix = "ELC-"
        kategori = lst_kategori[1]
        kategori_value = True

def validasiId():
    global id_barang, id_value

    id_value = False

    if id_barang == 0 or id_barang == '0':
        messagebox.showerror("Error", "Harap pilih barang terlebih dahulu !")
        id_value = False
        print(id_barang)
    else:
        id_value = True

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
                    validasiId()
                    if id_value == True:
                        valid = True


# Mengelola data
def tambahData():
    global id_barang

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()
    
    validasiSemua()
    if valid == True:
        try:
            hari_ini = datetime.datetime.now()

            c.execute("INSERT INTO tb_inventory (prefix,nama,qty,harga,kategori,dibuat,status_data) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (prefix,nama,qty,harga,kategori,hari_ini,'Aktif'))
            conn.commit()

            messagebox.showinfo("information", "Barang berhasil ditambah !")

            txt_nama.delete(0, END)
            txt_qty.delete(0, END)
            txt_harga.delete(0, END)
            cmb_kategori.set("Pilih Kategori")
            cmb_pilih_kategori.set(lst_pilih_kategori[0])
            txt_nama.focus_set()

            listBox.destroy()
            showInventory()

            id_barang = 0

        except Exception as e:
            messagebox.showinfo("error", e)
            conn.rollback()
            conn.close()

def editData():
    global id_barang

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    validasiSemua()
    if valid == True:
        try:
            hari_ini = datetime.datetime.now()
    
            nama = txt_nama.get()
            qty = int(txt_qty.get())
            harga = int(txt_harga.get())

            c.execute("UPDATE tb_inventory SET prefix=%s,nama=%s,qty=%s,harga=%s,kategori=%s,diubah=%s WHERE id=%s",
            (prefix,nama,qty,harga,kategori,hari_ini,id_barang))
            conn.commit()

            messagebox.showinfo("information", "Barang berhasil diedit !")

            txt_nama.delete(0, END)
            txt_qty.delete(0, END)
            txt_harga.delete(0, END)
            cmb_kategori.set("Pilih Kategori")
            cmb_pilih_kategori.set(lst_pilih_kategori[0])
            txt_nama.focus_set()

            listBox.destroy()
            showInventory()

            id_barang = 0

        except Exception as e:
            messagebox.showinfo("information", 'Harap pilih barang untuk diedit terlebih dahulu !')
            conn.rollback()
            conn.close()

def hapusData():
    global id_barang

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()
    
    try:
        hari_ini = datetime.datetime.now()

        c.execute("UPDATE tb_inventory SET diubah=%s, status_data=%s WHERE id=%s",
        (hari_ini,"Tidak Aktif", id_barang))
        conn.commit()

        messagebox.showinfo("information", "Barang berhasil dihapus !")

        txt_nama.delete(0, END)
        txt_qty.delete(0, END)
        txt_harga.delete(0, END)
        cmb_kategori.set("Pilih Kategori")
        cmb_pilih_kategori.set(lst_pilih_kategori[0])
        txt_nama.focus_set()

        listBox.destroy()
        showInventory()

        id_barang = 0

    except Exception as e:
        messagebox.showinfo("information", e)
        conn.rollback()
        conn.close()

def restoreData():
    global id_barang

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()
    
    validasiId()
    if id_value == True:
        try:
            hari_ini = datetime.datetime.now()

            c.execute("UPDATE tb_inventory SET diubah=%s, status_data=%s WHERE id=%s",
            (hari_ini, "Aktif", id_barang))
            conn.commit()

            messagebox.showinfo("information", "Barang Berhasil Dipulihkan !")
            showRecycleBin()

            id_barang = 0
        except Exception as e:
            messagebox.showinfo("information", e)
            conn.rollback()
            conn.close()
    

# Mencari data ditabel berdasarkan nama dan atau kategori
def callback(sv):
    global Id, cari, kategori

    cari = txt_cari_nama.get()
    Id = txt_cari_id.get()
    
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

    showCari()

def callbackId(svid):
    global Id, cari, kategori

    cari = txt_cari_nama.get()
    Id_search = txt_cari_id.get()

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

    showCari()


# Mengambil nilai dari tabel berdasarkan klick
def GetValue(e):
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

def GetValueRecycleBin(e):
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


# Untuk menggerakkan header (frame) window
def mouse_down(e):
    global x, y
    x, y = e.x, e.y

def mouse_up(e):
    global x, y
    x, y = None, None

def mouse_drag(e):
    global x, y
    try:
        deltax = e.x - x
        deltay = e.y - y
        x0 = root.winfo_x() + deltax
        y0 = root.winfo_y() + deltay
        root.geometry("+%s+%s" % (x0, y0))

        x0 = top.winfo_x() + deltax
        y0 = top.winfo_y() + deltay
        top.geometry("+%s+%s" % (x0, y0))
    except:
        pass


# Fungsi header window
def frm_mappedRoot(e):
    root.update_idletasks()
    root.overrideredirect(True)
    root.state('normal')

def frm_mappedTop(e):
    top.update_idletasks()
    top.overrideredirect(True)
    top.state('normal')

def minimizeRoot():
    root.update_idletasks()
    root.overrideredirect(False)
    root.state('iconic')

def minimizeTop():
    top.update_idletasks()
    top.overrideredirect(False)
    top.state('iconic')

def exit():
    root.destroy()
    top.destroy


# Menunjukkan tabel dari database
def showInventory():
    global listBox, scrollTree, frm_tabel

    frm_tabel = Frame(root, bg='#75B4E7')
    frm_tabel.place(x=20,y=240)

    scrollTree = ttk.Scrollbar(frm_tabel, style="TScrollbar", orient='vertical')
    
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

    listBox.bind('<ButtonRelease-1>',GetValue)

def showCari():
    global listBox, cari, Id
    Id = txt_cari_id.get()
    cari = txt_cari_nama.get()

    frm_tabel = Frame(root, bg='#75B4E7')
    frm_tabel.place(x=20,y=240)

    scrollTree = ttk.Scrollbar(frm_tabel, style="TScrollbar", orient='vertical')
    
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

    c.execute("SELECT CONCAT(prefix,id)AS id_barang,nama,qty,harga FROM tb_inventory WHERE id LIKE %s AND kategori LIKE %s AND nama LIKE %s AND status_data=%s", ("%"+Id+"%","%"+kategori+"%","%"+cari+"%","Aktif"))
    record = c.fetchall()
    conn.commit()
    
    for i, (id_barang,nama,qty,harga) in enumerate(record, start=1):
        listBox.insert("", "end", values=(id_barang,nama,qty,"Rp {:,},00-".format(harga)))
        conn.close()

    listBox.bind('<ButtonRelease-1>',GetValue)

def showRecycleBin():
    global listBoxRecycle, scrollTree, frm_recycle, id_barang

    frm_recycle = Frame(top, bg='#75B4E7')
    frm_recycle.place(x=20,y=95)

    scrollTree = ttk.Scrollbar(frm_recycle, style="TScrollbar", orient='vertical')
    
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

    listBoxRecycle.bind('<ButtonRelease-1>', GetValueRecycleBin)
    showInventory()

    id_barang = 0



# Window GUI program
def windowUtama():
    global root, sv, kategori
    global txt_nama, txt_qty, txt_harga, cmb_kategori, txt_cari_nama, txt_cari_id, cmb_pilih_kategori
    global btn_tambah, btn_edit, btn_hapus, btn_recycle_bin
    global lst_kategori, lst_pilih_kategori

    lst_kategori = ['Alat Tulis Kantor', 'Elektronik']
    lst_pilih_kategori = ['Semua', 'Alat Tulis Kantor', 'Elektronik']

    root = Tk()
    sv = StringVar()
    svid = StringVar()
    root.geometry("495x490")
    root.resizable(False, False)
    root.overrideredirect(True)
    root.configure(bg='#75B4E7')


    # Mengatur tema dan style
    theme = ttk.Style()
    theme.theme_use('clam')
    theme.configure("listBox.Treeview.Heading", font=('Lucida Sans', 10,'bold'), foreground="#FFFFFF", background="#009DFF", borderwidth=0)
    theme.configure("listBox.Treeview", fieldbackground="#D0D0D0")

    theme.configure("TCombobox", arrowcolor='#FFFFFF')
    theme.map("TCombobox", background=[('readonly','#00aaff')], foreground=[('readonly','#FFFFFF')])
    theme.map("TCombobox", bordercolor=[('readonly','#007DBB')], darkcolor=[('readonly','#0096E1')], lightcolor=[('readonly','#0096E1')])
    theme.map("TCombobox", fieldbackground=[('readonly','#00aaff')])
    theme.map("TCombobox", selectbackground=[('readonly','#00aaff')], selectforeground=[('readonly','#FFFFFF')])
    root.option_add("*TCombobox*Listbox*Background", "#FFFFFF")
    root.option_add("*TCombobox*Listbox*Foreground", "#009DFF")

    theme.configure("TScrollbar", troughcolor='#008BD0', background='#00aaff', bordercolor='#007DBB', darkcolor='#0096E1', lightcolor='#0096E1', arrowcolor='#FFFFFF')
    theme.map("TScrollbar", background=[('active','#00aaff'), ('disabled','#00aaff')])


    # Window header section
    x, y = None, None
    frm_header = Frame(root, bg="#009DFF", relief='raised', height=35)
    frm_header.pack(side=TOP, fill=BOTH)
    frm_header.bind('<ButtonPress-1>', mouse_down)
    frm_header.bind('<B1-Motion>', mouse_drag)
    frm_header.bind('<ButtonRelease-1>', mouse_up)
    frm_header.bind('<Map>', frm_mappedRoot)

    lbl_header_emoji = Label(frm_header, font=("Lucida Sans",16), text="📋")
    lbl_header_emoji.configure(bg='#009DFF', fg='#FFFFFF')
    lbl_header_emoji.pack(side=LEFT, anchor=NW)

    lbl_header = Label(frm_header, font=("Lucida Sans",13,'bold'), text="Inventory")
    lbl_header.configure(bg='#009DFF', fg='#FFFFFF')
    lbl_header.pack(side=LEFT, anchor=SW)

    btn_close = Button(frm_header, width=3, height=1, command=lambda: [exit()])
    btn_close.configure(font=('Lucida Sans',10,'bold'),text='X',bg='#007DCC', fg='#E60707', activebackground='#E60707', activeforeground='#FFFFFF')
    btn_close.pack(side=RIGHT, anchor=NE, fill=None, expand=False)

    btn_min = Button(frm_header, width=3, height=1, command=lambda: [minimizeRoot()])
    btn_min.configure(font=('Lucida Sans',10,'bold'),text='—',bg='#007DCC', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#007DCC')
    btn_min.pack(side=RIGHT, anchor=NE, fill=None, expand=False)


    # Window body section
    lbl_nama = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",13,'bold'), text="Nama").place(x=20,y=50)
    lbl_qty = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",13,'bold'), text="Qty").place(x=20,y=80)
    lbl_harga = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",13,'bold'), text="Harga").place(x=20,y=110)
    lbl_cari_id = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",10,'bold'), text="ID :").place(x=20,y=210)
    lbl_cari_nama = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",10,'bold'), text="Nama :").place(x=87,y=210)
    lbl_pilih_kategori = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",10,'bold'), text="Kategori :").place(x=270,y=209)
    
    txt_nama = Entry(root,width=15, font=("Lucida Sans", 10))
    txt_nama.place(x=90,y=52)

    txt_qty = Entry(root, width=15, font=("Lucida Sans", 10))
    txt_qty.place(x=90,y=82)

    txt_harga = Entry(root,width=15, font=("Lucida Sans", 10))
    txt_harga.place(x=90,y=112)

    cmb_kategori = ttk.Combobox(root, style="TCombobox", state="readonly", font=("Lucida Sans",10,'bold'), value=lst_kategori, width=14)
    cmb_kategori.set("Pilih Kategori")
    cmb_kategori.place(x=90,y=140)

    svid.trace("w", lambda name, index, mode, svid=svid: callbackId(svid))
    txt_cari_id = Entry(root, width=3, textvariable=svid, font=("Lucida Sans", 10))
    txt_cari_id.place(x=48,y=210)

    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
    txt_cari_nama = Entry(root, width=15, textvariable=sv, font=("Lucida Sans", 10))
    txt_cari_nama.place(x=140,y=210)

    cmb_pilih_kategori = ttk.Combobox(root, state="readonly", value=lst_pilih_kategori, width=13, font=("Lucida Sans",10,'bold'))
    cmb_pilih_kategori.bind("<<ComboboxSelected>>", kategoriShowBarang)
    cmb_pilih_kategori.set(lst_pilih_kategori[0])
    cmb_pilih_kategori.place(x=340,y=210)

    btn_tambah = Button(root, bg='#00aaff', fg='#FFFFFF', text="Tambah", width=15, font=("Lucida Sans",10,'bold'), command=lambda: [tambahData()])
    btn_tambah.place(x=290,y=50)

    btn_edit = Button(root, bg='#00aaff', fg='#FFFFFF', text="Edit", width=15, font=("Lucida Sans",10,'bold'), command=lambda: [editData()])
    btn_edit.place(x=290,y=80)

    btn_hapus = Button(root, bg='#00aaff', fg='#FFFFFF', text="Hapus", width=15, font=("Lucida Sans",10,'bold'), command=lambda: [hapusData()])
    btn_hapus.place(x=290,y=110)

    btn_recycle_bin = Button(root, bg='#00aaff', fg='#FFFFFF', text="🗑️Recycle Bin", font=("Lucida Sans",10,'bold'), width=15, command=lambda: [root.withdraw(), windowRecycleBin()])
    btn_recycle_bin.place(x=290,y=140)

    showInventory()
    mainloop()

def windowRecycleBin():
    global top
    global btn_restore, btn_kembali

    top = Toplevel()
    top.title("Recycle Bin")
    top.geometry("500x340")
    top.resizable(False, False)
    top.overrideredirect(True)
    top.configure(bg='#75B4E7')

    # Window header section
    x, y = None, None
    frm_header = Frame(top, bg="#009DFF", relief='raised', height=35)
    frm_header.pack(side=TOP, fill=BOTH)
    frm_header.bind('<ButtonPress-1>', mouse_down)
    frm_header.bind('<B1-Motion>', mouse_drag)
    frm_header.bind('<ButtonRelease-1>', mouse_up)
    frm_header.bind('<Map>', frm_mappedTop)

    lbl_header_emoji = Label(frm_header, font=("Lucida Sans",16), text="🗑️")
    lbl_header_emoji.configure(bg='#009DFF', fg='#FFFFFF')
    lbl_header_emoji.pack(side=LEFT, anchor=NW)

    lbl_header = Label(frm_header, font=("Lucida Sans",13,'bold'), text="Recycle Bin")
    lbl_header.configure(bg='#009DFF', fg='#FFFFFF')
    lbl_header.place(x=30,y=2)

    btn_close = Button(frm_header, width=3, command=lambda: [exit()])
    btn_close.configure(font=('Lucida Sans',10,'bold'),text='X',bg='#007DCC', fg='#E60707', activebackground='#E60707', activeforeground='#FFFFFF')
    btn_close.pack(side=RIGHT,anchor=NE)

    btn_min = Button(frm_header, width=3, command=lambda: [minimizeTop()])
    btn_min.configure(font=('Lucida Sans',10,'bold'),text='—',bg='#007DCC', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#007DCC')
    btn_min.pack(side=RIGHT,anchor=NE)

    # Window body section
    btn_kembali = Button(top, bg='#00aaff', fg='#FFFFFF', text="Kembali",font=("Lucida Sans",10,'bold'), command=lambda: [top.withdraw(), root.deiconify()]).place(x=20,y=50)
    btn_restore = Button(top, bg='#00aaff', fg='#FFFFFF', text="Pulihkan",font=("Lucida Sans",10,'bold'), command=lambda: [restoreData(), listBoxRecycle.destroy(), showRecycleBin()]).place(x=90,y=50)

    showRecycleBin()


createDatabase()
createTable()
windowUtama()
