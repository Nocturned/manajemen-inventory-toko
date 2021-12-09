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
        dibuat DATETIME NULL,
        diubah DATETIME NULL,
        status_data VARCHAR(255) NULL,
        PRIMARY KEY (id),
        UNIQUE KEY (prefix, id),
        INDEX (nama, kategori)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1
        """)
    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS tb_riwayat_pembelian (
        id INT(3) UNSIGNED NOT NULL AUTO_INCREMENT,
        barang VARCHAR(255) NOT NULL,
        qty INT(4) UNSIGNED,
        total INT(9) UNSIGNED,
        dibuat DATETIME NULL,
        diubah DATETIME NULL,
        status_data VARCHAR(255) NULL,
        PRIMARY KEY (id),
        INDEX (barang, total)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1
        """)
    conn.commit()

    conn.close()


# Mengganti kategori pada katalog
def kategoriShowBarang(e):
    global kategori

    if cmb_pilih_kategori.get() == lst_pilih_kategori[0]:
        frm_tabel.destroy()
        kategori = ''
        showKatalogKategori()
    elif cmb_pilih_kategori.get() == lst_pilih_kategori[1]:
        frm_tabel.destroy()
        kategori = lst_pilih_kategori[1]
        showKatalogKategori()
    elif cmb_pilih_kategori.get() == lst_pilih_kategori[2]:
        frm_tabel.destroy()
        kategori = lst_pilih_kategori[2]
        showKatalogKategori()


# Mencari barang berdasarkan nama dan atau kategori
def callback(sv):
    global cari, kategori

    if cmb_pilih_kategori.get() == lst_pilih_kategori[0]:
        frm_tabel.destroy()
        kategori = ''
        showKatalogKategori()
    elif cmb_pilih_kategori.get() == lst_pilih_kategori[1]:
        frm_tabel.destroy()
        kategori = lst_pilih_kategori[1]
        showKatalogKategori()
    elif cmb_pilih_kategori.get() == lst_pilih_kategori[2]:
        frm_tabel.destroy()
        kategori = lst_pilih_kategori[2]
        showKatalogKategori()

    showKatalogKategori()
    cari = txt_cari.get()


# Mengisi harga total berdasarkan Qty
def callbackqty(svqty):
    global total, qty

    qty = int(txt_qty.get())
    harga_temp = str(harga_str.replace(",","")[3:][:-3])
    harga = int(harga_temp)
    total = int(qty * harga)

    total_str = "Rp {:,},00-".format(total)

    txt_total.configure(state='normal')
    txt_total.delete(0, END)
    txt_total.insert('end', '{}'.format(total_str))
    txt_total.configure(state='disabled',disabledbackground='white', disabledforeground='black')


# Mengambil nilai dari lepas klick pada tabel katalog
def GetValue(e):
    global id_barang, nama, harga_str

    rowID = listBox.selection()[0]
    select = listBox.set(rowID)

    id_barang = select['No']
    nama = select['Nama']
    harga_str = select['Harga']

    global total, qty

    qty = int(txt_qty.get())
    harga_temp = str(harga_str.replace(",","")[3:][:-3])
    harga = int(harga_temp)
    total = int(qty * harga)

    total_str = "Rp {:,},00-".format(total)

    txt_total.configure(state='normal')
    txt_total.delete(0, END)
    txt_total.insert('end', '{}'.format(total_str))
    txt_total.configure(state='disabled',disabledbackground='white', disabledforeground='black')


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
    except:
        pass


# Fungsi header window
def frm_mapped(e):
    root.update_idletasks()
    root.overrideredirect(True)
    root.state('normal')

def minimize():
    root.update_idletasks()
    root.overrideredirect(False)
    root.state('iconic')

def exit():
    root.destroy()


# Validasi text Qty
def validasiQty():
    global qty, qty_value

    qty_temp = txt_qty.get()

    if qty_temp == '':
        qty = ''
        qty_value = False
        messagebox.showerror("Error", "Harap masukkan jumlah barang dibeli !")
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
        messagebox.showerror("Error", "Jumlah maksimal barang adalah 100 !")
    elif qty_temp.isdigit() == True:
        qty = int(qty_temp)
        qty_value = True


# Mengurangi qty barang dan membuat log pembelian
def beliBarang():
    hari_ini = datetime.datetime.now()

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    validasiQty()
    if qty_value == True:
        try:
            c.execute("UPDATE tb_inventory SET qty=qty-%s,diubah=%s WHERE id=%s AND status_data = 'Aktif'",
            (qty,hari_ini,id_barang))
            conn.commit()

            c.execute("INSERT INTO tb_riwayat_pembelian (barang, qty, total, dibuat, status_data) VALUES (%s,%s,%s,%s,%s)",
            (nama, qty, total, hari_ini, 'Aktif'))
            conn.commit()

            messagebox.showinfo("information", "Barang berhasil dibeli !")

            txt_qty.delete(0, END)
            txt_total.delete(0, END)

            frm_tabel.destroy()
            showKatalog()

        except Exception as e:
            messagebox.showinfo("information", 'Stock barang ini tidak mencukupi')
            conn.rollback()
            conn.close()


# Menunjukkan tabel/katalog
def showKatalog():
    global listBox, scrollTree, frm_tabel

    frm_tabel = Frame(root, bg='#75B4E7')
    frm_tabel.place(x=20,y=130)

    scrollTree = ttk.Scrollbar(frm_tabel, style='TScrollbar', orient='vertical')
    
    cols = ('No', 'Nama','Harga')
    listBox = ttk.Treeview(frm_tabel, style="listBox.Treeview", columns=cols, show='headings', yscrollcommand=scrollTree.set)
    listBox.pack(side=LEFT)

    scrollTree.config(command=listBox.yview)
    scrollTree.pack(side=RIGHT, fill=Y)

    for col in cols:
        listBox.heading(col, text=col)
        listBox.column('No', minwidth=0, width=50, stretch=NO, anchor = CENTER)
        listBox.column('Nama', minwidth=0, width=190, stretch=NO, anchor = W)
        listBox.column('Harga', minwidth=0, width=130, stretch=NO, anchor = W)

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    c.execute("SELECT id,nama,harga FROM tb_inventory WHERE status_data=%s",("Aktif",))
    record = c.fetchall()
    conn.commit()
    
    for i, (id,nama,harga) in enumerate(record, start=1):
        listBox.insert("", "end", values=(id,nama,"Rp {:,},00-".format(harga)))
        conn.close()

    listBox.bind('<ButtonRelease-1>',GetValue)

def showKatalogKategori():
    global cari
    cari = txt_cari.get()

    frm_tabel = Frame(root, bg='#75B4E7')
    frm_tabel.place(x=20,y=130)

    scrollTree = ttk.Scrollbar(frm_tabel, style='TScrollbar', orient='vertical')
    
    cols = ('No', 'Nama','Harga')
    listBox = ttk.Treeview(frm_tabel, style="listBox.Treeview", columns=cols, show='headings', yscrollcommand=scrollTree.set)
    listBox.pack(side=LEFT)

    scrollTree.config(command=listBox.yview)
    scrollTree.pack(side=RIGHT, fill=Y)

    for col in cols:
        listBox.heading(col, text=col)
        listBox.column('No', minwidth=0, width=50, stretch=NO, anchor = CENTER)
        listBox.column('Nama', minwidth=0, width=170, stretch=NO, anchor = W)
        listBox.column('Harga', minwidth=0, width=130, stretch=NO, anchor = W)

    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

    c.execute("SELECT id,nama,harga FROM tb_inventory WHERE kategori LIKE %s AND nama LIKE %s AND status_data=%s", (kategori+"%",cari+"%","Aktif"))
    record = c.fetchall()
    conn.commit()
    
    for i, (id,nama,harga) in enumerate(record, start=1):
        listBox.insert("", "end", values=(id,nama,"Rp {:,},00-".format(harga)))
        conn.close()

    listBox.bind('<ButtonRelease-1>',GetValue)


# Window GUI program
def windowUtama():
    global root, sv, svqty
    global txt_qty, txt_cari, cmb_pilih_kategori, txt_total
    global btn_beli
    global lst_pilih_kategori

    lst_pilih_kategori = ['Semua', 'Alat Tulis Kantor', 'Elektronik']

    root = Tk()
    sv = StringVar()
    svqty = StringVar()
    root.title("Manajemen Inventory Toko BlaBlaBla")
    root.geometry("430x500")
    root.resizable(False, False)
    root.overrideredirect(True)
    root.configure(bg='#75B4E7')


    # Mengatur tema dan style
    theme = ttk.Style()
    theme.theme_use('clam')
    theme.configure("listBox.Treeview.Heading", font=('Lucida Sans', 10, 'bold'), foreground="#FFFFFF", background="#009DFF", borderwidth=0)
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
    frm_header.bind('<Map>', frm_mapped)

    lbl_header_emoji = Label(frm_header, font=("Lucida Sans",16), text="🛒")
    lbl_header_emoji.configure(bg='#009DFF', fg='#FFFFFF')
    lbl_header_emoji.pack(side=LEFT, anchor=NW)

    lbl_header = Label(frm_header, font=("Lucida Sans",13,'bold'), text="Mesin Kasir")
    lbl_header.configure(bg='#009DFF', fg='#FFFFFF')
    lbl_header.pack(side=LEFT, anchor=SW)

    btn_close = Button(frm_header, width=3, command=lambda: [exit()])
    btn_close.configure(font=('Lucida Sans',10,'bold'),text='X',bg='#007DCC', fg='#E60707', activebackground='#E60707', activeforeground='#FFFFFF')
    btn_close.pack(side=RIGHT,anchor=NE)

    btn_min = Button(frm_header, width=3, command=lambda: [minimize()])
    btn_min.configure(font=('Lucida Sans',10,'bold'),text='—',bg='#007DCC', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#007DCC')
    btn_min.pack(side=RIGHT,anchor=NE)


    # Window body section
    lbl_kasir_emoji = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",30), text="🛒").place(x=140,y=42)
    lbl_kasir = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",30,'bold'), text="Kasir").place(x=190,y=50)
    lbl_cari = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",13,'bold'), text="Cari: ").place(x=20,y=360)
    lbl_kategori = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",13,'bold'), text="Kategori: ").place(x=195,y=360)
    lbl_qty = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",13,'bold'), text="Qty").place(x=70,y=410)
    lbl_total = Label(root, bg='#75B4E7', fg='#FFFFFF', font=("Lucida Sans",13,'bold'), text="Total").place(x=175,y=410)

    cmb_pilih_kategori = ttk.Combobox(root, style='TCombobox', state="readonly", value=lst_pilih_kategori, width=13, font=("Lucida Sans",10,'bold'))
    cmb_pilih_kategori.bind("<<ComboboxSelected>>", kategoriShowBarang)
    cmb_pilih_kategori.set(lst_pilih_kategori[0])
    cmb_pilih_kategori.place(x=280,y=363)

    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
    txt_cari = Entry(root, width=15, textvariable=sv, font=("Lucida Sans", 10))
    txt_cari.place(x=65,y=363)

    svqty.trace("w", lambda name, index, mode, svqty=svqty: callbackqty(svqty))
    txt_qty = Entry(root, width=6, textvariable=svqty, font=("Lucida Sans", 10))
    txt_qty.place(x=110,y=413)

    txt_total = Entry(root, width=15, font=("Lucida Sans", 10), state='disabled', disabledbackground='white', disabledforeground='black')
    txt_total.place(x=230,y=413)

    btn_beli = Button(root, bg='#00aaff', fg='#FFFFFF', text="Beli", font=("Lucida Sans",10,'bold'), width=10, command=lambda: [beliBarang()]).place(x=175,y=460)

    showKatalog()
    mainloop()


createDatabase()
createTable()
windowUtama()
