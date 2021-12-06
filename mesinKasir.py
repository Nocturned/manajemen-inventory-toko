from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import *
import mysql.connector as mariadb
import datetime


# Membuat table riwayat pembelian jika belum ada
def createTable():
    conn = mariadb.connect(user="root", password="", database='db_inventoryToko', host="localhost", port='3306')
    c = conn.cursor()

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

    cari = txt_cari.get()
    showKatalogKategori()


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
def GetValue(event):
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


# Validasi text Qty
def validasiQty():
    global qty, qty_value

    qty_temp = txt_qty.get()

    if qty_temp == '':
        qty = ''
        qty_value = False
        messagebox.showinfo("Error", "Harap masukkan jumlah barang dibeli !")
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
            messagebox.showinfo("information", 'Stock barang ini sedang habis')
            conn.rollback()
            conn.close()


# Menunjukkan tabel/katalog
def showKatalog():
    global listBox, scrollTree, frm_tabel

    frm_tabel = Frame(root)
    frm_tabel.place(x=20,y=100)
    scrollTree = ttk.Scrollbar(frm_tabel, orient='vertical')
    
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

    frm_tabel = Frame(root)
    frm_tabel.place(x=20,y=100)
    scrollTree = ttk.Scrollbar(frm_tabel, orient='vertical')
    
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

    c.execute("SELECT id,nama,harga FROM tb_inventory WHERE kategori LIKE %s AND nama LIKE %s AND status_data=%s", ("%"+kategori+"%","%"+cari+"%","Aktif"))
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

    root = Tk()
    sv = StringVar()
    svqty = StringVar()
    root.title("Manajemen Inventory Toko BlaBlaBla")
    root.geometry("430x470")
    root.resizable(False, False)
    root.protocol('WM_DELETE_WINDOW', lambda: [root.destroy()])

    theme = ttk.Style()
    theme.theme_use('clam')
    theme.configure("listBox.Treeview.Heading", font=('Lucida Sans', 10, 'bold'), foreground="#FFFFFF", background="#009DFF", borderwidth=0)
    theme.configure("listBox.Treeview", fieldbackground="#D0D0D0")

    lst_pilih_kategori = ['Semua', 'Alat Tulis Kantor', 'Elektronik']

    lbl_kasir_emoji = Label(root, font=("Lucida Sans", 30), text="🛒").place(x=140,y=12)
    lbl_kasir = Label(root, font=("Lucida Sans", 30), text="Kasir").place(x=190,y=20)
    lbl_cari = Label(root, font=("Lucida Sans", 13), text="Cari: ").place(x=20,y=330)
    lbl_kategori = Label(root, font=("Lucida Sans", 13), text="Kategori: ").place(x=200,y=330)
    lbl_qty = Label(root, font=("Lucida Sans", 13), text="Qty").place(x=70,y=380)
    lbl_total = Label(root, font=("Lucida Sans", 13), text="Total").place(x=160,y=380)

    cmb_pilih_kategori = ttk.Combobox(root, state="readonly", value=lst_pilih_kategori, width=13, font=("Lucida Sans",10))
    cmb_pilih_kategori.bind("<<ComboboxSelected>>", kategoriShowBarang)
    cmb_pilih_kategori.set(lst_pilih_kategori[0])
    cmb_pilih_kategori.place(x=280,y=333)

    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
    txt_cari = Entry(root, width=15, textvariable=sv, font=("Lucida Sans", 10))
    txt_cari.place(x=65,y=333)

    svqty.trace("w", lambda name, index, mode, svqty=svqty: callbackqty(svqty))
    txt_qty = Entry(root, width=6, textvariable=svqty, font=("Lucida Sans", 10))
    txt_qty.place(x=110,y=383)

    txt_total = Entry(root, width=15, font=("Lucida Sans", 10), state='disabled', disabledbackground='white', disabledforeground='black')
    txt_total.place(x=230,y=383)


    btn_beli = Button(root, text="Beli", font=("Lucida Sans",10), width=10, command=lambda: [beliBarang()]).place(x=175,y=430)

    showKatalog()
    mainloop()


createTable()
windowUtama()
