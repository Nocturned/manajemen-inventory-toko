from tkinter import *
from tkinter import ttk, messagebox

from os import sys
import mysql.connector as mysql
import datetime

from .Setting import *

from PIL import Image, ImageTk


class ManajemenInventoryWindow:

    # Fungsi header window
    def frmMappedRoot(self, e):
        self.root.update_idletasks()
        self.root.overrideredirect(True)
        self.root.state('normal')

    def frmMappedTop(self, e):
        self.top.update_idletasks()
        self.top.overrideredirect(True)
        self.top.state('normal')

    def minimizeRoot(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.state('iconic')

    def minimizeTop(self):
        self.top.update_idletasks()
        self.top.overrideredirect(False)
        self.top.state('iconic')

    def close(self):
        self.root.destroy()

    def closeEsc(self,e):
        self.root.destroy()

    def closeTop(self):
        self.top.withdraw()
        self.root.deiconify()
        self.frm_tabel.destroy()
        self.tabelInventory()

    def closeEscTop(self,e):
        self.top.withdraw()
        self.root.deiconify()
        self.frm_tabel.destroy()
        self.tabelInventory()


    # Untuk menggerakkan header (frame) window
    def mouseDown(self, e):
        self.x = e.x
        self.y = e.y

    def mouseUp(self, e):
        self.x = None
        self.y = None

    def mouseDrag(self, e):
        try:
            self.deltax = e.x - self.x
            self.deltay = e.y - self.y
            self.x0 = self.root.winfo_x() + self.deltax
            self.y0 = self.root.winfo_y() + self.deltay
            self.root.geometry("+%s+%s" % (self.x0, self.y0))

            self.x0 = self.top.winfo_x() + self.deltax
            self.y0 = self.top.winfo_y() + self.deltay
            self.top.geometry("+%s+%s" % (self.x0, self.y0))
        except:
            pass


    ## Main Program ##
    def __init__(self, username):
        self.username = username

        self.root = Tk()
        self.sv = StringVar()

        self.root_settings = SettingTheme()
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost',True)
        self.root.configure(bg='#eb8f3b')
        self.root.option_add("*TCombobox*Listbox*Background", "#FFFFFF")
        self.root.option_add("*TCombobox*Listbox*Foreground", "#F4963F")
        self.root.bind('<Escape>', self.closeEsc)


        ## Header window ##
        self.x = None
        self.y = None
        self.frm_header = Frame(self.root, bg="#ff6f00", relief='raised', height=35)
        self.frm_header.pack(side=TOP, fill=BOTH)
        self.frm_header.bind('<ButtonPress-1>', self.mouseDown)
        self.frm_header.bind('<B1-Motion>', self.mouseDrag)
        self.frm_header.bind('<ButtonRelease-1>', self.mouseUp)
        self.frm_header.bind('<Map>', self.frmMappedRoot)

        self.lbl_header_emoji = Label(self.frm_header, font=("Lucida Sans",18), text="📋")
        self.lbl_header_emoji.configure(bg='#ff6f00', fg='#FFFFFF')
        self.lbl_header_emoji.pack(side=LEFT, anchor=NW)

        self.lbl_header = Label(self.frm_header, font=("Lucida Sans",16,'bold'), text="Manajemen Inventory")
        self.lbl_header.configure(bg='#ff6f00', fg='#FFFFFF')
        self.lbl_header.pack(side=LEFT, anchor=SW)

        self.btn_close = Button(self.frm_header, width=3, height=1, command=lambda: [self.close()])
        self.btn_close.configure(font=('Lucida Sans',10,'bold'),text='X',bg='#FF7A00', fg='#E60707', activebackground='#E60707', activeforeground='#FFFFFF')
        self.btn_close.pack(side=RIGHT, anchor=NE, fill=None, expand=False)

        self.btn_min = Button(self.frm_header, width=3, height=1, command=lambda: [self.minimizeRoot()])
        self.btn_min.configure(font=('Lucida Sans',10,'bold'),text='—',bg='#FF7A00', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#545454')
        self.btn_min.pack(side=RIGHT, anchor=NE, fill=None, expand=False)

        
        ## Body window ##


        # Frame filter #
        self.frm_filter = LabelFrame(self.root,relief='groove', bg="#f08726", height=200,width=300)
        self.frm_filter.place(x=20,y=50)
        
        self.lbl_filter = Label(self.root,font=("Lucida Sans",15,'bold underline'),fg='#FFFFFF',bg='#f08726',text=" Filter*                             ").place(x=27,y=60)
        self.lbl_cari = Label(self.root,font=("Lucida Sans",13,'bold'),fg='#FFFFFF',bg='#f08726',text="Cari").place(x=30,y=100)
        self.lbl_tbl_kategori = Label(self.root,font=("Lucida Sans",13,'bold'),fg='#FFFFFF',bg='#f08726',text="Kategori").place(x=30,y=140)
        self.lbl_tbl_jenis = Label(self.root,font=("Lucida Sans",13,'bold'),fg='#FFFFFF',bg='#f08726',text="Jenis").place(x=30,y=180)

        self.sv.trace("w", lambda name, index, mode, sv=self.sv: self.filterCari(sv))
        self.txt_cari = Entry(self.root,width=17,font=("Lucida Sans",11),textvariable=self.sv)
        self.txt_cari.place(x=130,y=103)

        self.lst_tbl_kategori = ['Semua', 'Dapur', 'Elektronik', 'Fashion', 'Perawatan Tubuh', 'Alat Tulis Kantor']
        self.cmb_tbl_kategori = ttk.Combobox(self.root, style="TCombobox", state="readonly", font=("Lucida Sans",11,'bold'), value=self.lst_tbl_kategori, width=14)
        self.cmb_tbl_kategori.set(self.lst_tbl_kategori[0])
        self.cmb_tbl_kategori.bind("<<ComboboxSelected>>", self.filterCari)
        self.cmb_tbl_kategori.place(x=130,y=140)

        self.lst_tbl_jenis = ['Semua', '-', 'Ekspor', 'Impor']
        self.cmb_tbl_jenis = ttk.Combobox(self.root, style="TCombobox", state="readonly", font=("Lucida Sans",11,'bold'), value=self.lst_tbl_jenis, width=14)
        self.cmb_tbl_jenis.set(self.lst_tbl_jenis[0])
        self.cmb_tbl_jenis.bind("<<ComboboxSelected>>", self.filterCari)
        self.cmb_tbl_jenis.place(x=130,y=180)


        # Frame olah data #
        self.frm_olah_data = LabelFrame(self.root,relief='groove', bg="#f08726", height=200,width=500)
        self.frm_olah_data.place(x=450,y=50)

        self.lbl_nama = Label(self.root,font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#f08726',text="Nama").place(x=470,y=60)
        self.lbl_qty = Label(self.root,font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#f08726',text="Qty").place(x=470,y=100)
        self.lbl_harga = Label(self.root,font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#f08726',text="Harga").place(x=470,y=140)
        self.lbl_kategori = Label(self.root,font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#f08726',text="Kategori").place(x=470,y=180)
        self.lbl_jenis = Label(self.root,font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#f08726',text="Jenis").place(x=470,y=215)

        self.txt_nama = Entry(self.root,width=17,font=("Lucida Sans",11))
        self.txt_nama.place(x=580,y=63)

        self.txt_qty = Entry(self.root,width=17,font=("Lucida Sans",11))
        self.txt_qty.place(x=580,y=103)

        self.txt_harga = Entry(self.root,width=17,font=("Lucida Sans",11))
        self.txt_harga.place(x=580,y=143)


        self.lst_kategori = ['Dapur', 'Elektronik', 'Fashion', 'Perawatan Tubuh', 'Alat Tulis Kantor']
        self.lst_prefix = ['KTC-', 'ELC-', 'FSH-', 'SKC-', 'ATK-']
        self.cmb_kategori = ttk.Combobox(self.root, style="TCombobox", state="readonly", font=("Lucida Sans",11,'bold'), value=self.lst_kategori, width=14)
        self.cmb_kategori.set("Pilih Kategori")
        self.cmb_kategori.place(x=580,y=183)

        self.lst_jenis = ['-', 'Ekspor', 'Impor']
        self.cmb_jenis = ttk.Combobox(self.root, style="TCombobox", state="readonly", font=("Lucida Sans",11,'bold'), value=self.lst_jenis, width=14)
        self.cmb_jenis.set("Pilih Jenis Barang")
        self.cmb_jenis.place(x=580,y=218)

        self.btn_tambah = ttk.Button(self.root,style="TButton",text='Tambah',width=10,command=lambda:[self.dataTambah()])
        self.btn_tambah.place(x=760,y=97)

        self.btn_edit = ttk.Button(self.root,style="TButton",text='Edit',width=10,command=lambda:[self.dataEdit()])
        self.btn_edit.place(x=760,y=137)

        self.btn_hapus = ttk.Button(self.root,style="TButton",text='Hapus',width=10,command=lambda:[self.dataHapus()])
        self.btn_hapus.place(x=760,y=177)

        self.img_recycle = ImageTk.PhotoImage(Image.open("Gambar/recycle.png").resize((30,30), Image.ANTIALIAS))
        self.img_recycle_orange = ImageTk.PhotoImage(Image.open("Gambar/recycleOrange.png").resize((30,30), Image.ANTIALIAS))
        self.btn_recycle = ttk.Button(self.root,style="TButton",image=self.img_recycle,width=10,command=lambda :[self.openRecycle_Bin()])
        self.btn_recycle.place(x=890,y=130)
        self.btn_recycle.bind("<Enter>", self.onHover)
        self.btn_recycle.bind("<Leave>", self.offHover)     
        
        self.tabelInventory()
        self.root.mainloop()


    # Top level window
    def windowRecycleBin(self):
        self.top = Toplevel()

        self.top.geometry("1000x480")
        self.top_settings = SettingTheme()
        self.top.resizable(True, True)
        self.top.overrideredirect(True)
        self.top.configure(bg='#eb8f3b')
        self.top.option_add("*TCombobox*Listbox*Background", "#FFFFFF")
        self.top.option_add("*TCombobox*Listbox*Foreground", "#F4963F")
        self.top.bind('<Escape>', lambda :[self.closeEscTop()])
        self.top.attributes('-topmost',True)

        self.sv_recycle = StringVar()

        ## Header window ##
        self.x = None
        self.y = None
        self.frm_header_recycle = Frame(self.top, bg="#ff6f00", relief='raised', height=35)
        self.frm_header_recycle.pack(side=TOP, fill=BOTH)
        self.frm_header_recycle.bind('<ButtonPress-1>', self.mouseDown)
        self.frm_header_recycle.bind('<B1-Motion>', self.mouseDrag)
        self.frm_header_recycle.bind('<ButtonRelease-1>', self.mouseUp)
        self.frm_header_recycle.bind('<Map>', lambda :[self.frmMappedRoot()])

        self.img_header_emoji_recycle = ImageTk.PhotoImage(Image.open("Gambar/recycle.png").resize((25,25), Image.ANTIALIAS))
        self.lbl_header_emoji_recycle = Label(self.frm_header_recycle, image=self.img_header_emoji_recycle, borderwidth=0, bg='#FF7A00')
        self.lbl_header_emoji_recycle.configure(bg='#ff6f00', fg='#FFFFFF')
        self.lbl_header_emoji_recycle.pack(side=LEFT, anchor=W)

        self.lbl_header_recycle = Label(self.frm_header_recycle, font=("Lucida Sans",16,'bold'), text="Recycle Bin")
        self.lbl_header_recycle.configure(bg='#ff6f00', fg='#FFFFFF')
        self.lbl_header_recycle.pack(side=LEFT, anchor=SW)

        self.btn_close_recycle = Button(self.frm_header_recycle, width=3, height=1, command=lambda: [self.closeTop()])
        self.btn_close_recycle.configure(font=('Lucida Sans',10,'bold'),text='X',bg='#FF7A00', fg='#E60707', activebackground='#E60707', activeforeground='#FFFFFF')
        self.btn_close_recycle.pack(side=RIGHT, anchor=NE, fill=None, expand=False)

        self.btn_min_recycle = Button(self.frm_header_recycle, width=3, height=1, command=lambda: [self.minimizeTop()])
        self.btn_min_recycle.configure(font=('Lucida Sans',10,'bold'),text='—',bg='#FF7A00', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#FF7A00')
        self.btn_min_recycle.pack(side=RIGHT, anchor=NE, fill=None, expand=False)
    
        
        ## Body window ##
        self.lbl_cari = Label(self.top, font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#eb8f3b',text="Cari").place(x=20,y=45)
        self.lbl_kategori = Label(self.top, font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#eb8f3b',text="Kategori").place(x=20,y=80)
        self.lbl_jenis = Label(self.top, font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#eb8f3b',text="Jenis").place(x=20,y=120)

        self.sv_recycle.trace("w", lambda name, index, mode, sv_recycle=self.sv_recycle: self.filterCariRecycle(sv_recycle))
        self.txt_cari_recycle = Entry(self.top, font=("Lucida Sans",11), textvariable=self.sv_recycle)
        self.txt_cari_recycle.place(x=120,y=48)

        self.lst_tbl_kategori_recycle = ['Semua', 'Dapur', 'Elektronik', 'Fashion', 'Perawatan Tubuh', 'Alat Tulis Kantor']
        self.cmb_tbl_kategori_recycle = ttk.Combobox(self.top, style="T2.TCombobox", state="readonly", font=("Lucida Sans",11,'bold'), value=self.lst_tbl_kategori_recycle, width=17)
        self.cmb_tbl_kategori_recycle.set(self.lst_tbl_kategori_recycle[0])
        self.cmb_tbl_kategori_recycle.bind("<<ComboboxSelected>>", self.filterCariRecycle)
        self.cmb_tbl_kategori_recycle.place(x=120,y=83)

        self.lst_tbl_jenis_recycle = ['Semua', '-', 'Ekspor', 'Impor']
        self.cmb_tbl_jenis_recycle = ttk.Combobox(self.top, style="TCombobox", state="readonly", font=("Lucida Sans",11,'bold'), value=self.lst_tbl_jenis, width=17)
        self.cmb_tbl_jenis_recycle.set(self.lst_tbl_jenis[0])
        self.cmb_tbl_jenis_recycle.bind("<<ComboboxSelected>>", self.filterCariRecycle)
        self.cmb_tbl_jenis_recycle.place(x=120,y=123)

        self.btn_pulihkan_recycle = ttk.Button(self.top,style="TButton",text='Pulihkan',width=10,command=lambda:[self.dataRestore()])
        self.btn_pulihkan_recycle.place(x=845,y=80)

        self.tabelRecycleBin()


    # Menunjukkan tabel dari database
    def tabelInventory(self):
        self.frm_tabel = Frame(self.root, bg='#75B4E7', borderwidth=0)
        self.frm_tabel.place(x=20,y=260)

        self.scrollTree = ttk.Scrollbar(self.frm_tabel, style="TScrollbar", orient='vertical')
        
        self.cols = ('ID Barang','Nama','Kategori','Jenis','Qty','Harga')
        self.listBox = ttk.Treeview(self.frm_tabel, style="listBox.Treeview", columns=self.cols, show='headings', yscrollcommand=self.scrollTree.set,height=20)
        self.listBox.pack(side=LEFT, fill=Y)

        self.scrollTree.config(command=self.listBox.yview)
        self.scrollTree.pack(side=RIGHT, fill=Y)

        for self.col in self.cols:
            self.listBox.heading(self.col, text=self.col)
            self.listBox.column('ID Barang', minwidth=0, width=130, stretch=NO, anchor = CENTER)
            self.listBox.column('Nama', minwidth=0, width=270, stretch=NO, anchor = W)
            self.listBox.column('Kategori', minwidth=0, width=170, stretch=NO, anchor = W)
            self.listBox.column('Jenis', minwidth=0, width=110, stretch=NO, anchor = W)
            self.listBox.column('Qty', minwidth=0, width=100, stretch=NO, anchor = CENTER)
            self.listBox.column('Harga', minwidth=0, width=160, stretch=NO, anchor = W)

        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        self.c.execute("""SELECT CONCAT(prefix,a.id_barang) AS id, a.nama, kategori, b.jenis_barang, qty, harga
	                        FROM tb_inventory A
	                        INNER JOIN tb_detail_barang B ON a.nama = b.nama AND a.id_barang = b.id_barang
		                        WHERE a.status_data = %s AND b.status_data = %s""",
        ('Aktif','Aktif'))
        self.record = self.c.fetchall()
        self.conn.commit()
        
        for i, (id_barang,nama,kategori,jenis,qty,harga) in enumerate(self.record, start=1):
            self.listBox.insert("", "end", values=(id_barang,nama,kategori,jenis,qty,"Rp {:,},00-".format(harga)))
            self.conn.close()

        self.listBox.bind('<ButtonRelease-1>',self.GetValue)

    def tabelFiltered(self):
        self.frm_tabel = Frame(self.root, bg='#75B4E7', borderwidth=0)
        self.frm_tabel.place(x=20,y=260)

        self.scrollTree = ttk.Scrollbar(self.frm_tabel, style="TScrollbar", orient='vertical')
        
        self.cols = ('ID Barang','Nama','Kategori','Jenis','Qty','Harga')
        self.listBox = ttk.Treeview(self.frm_tabel, style="listBox.Treeview", columns=self.cols, show='headings', yscrollcommand=self.scrollTree.set,height=20)
        self.listBox.pack(side=LEFT, fill=Y)

        self.scrollTree.config(command=self.listBox.yview)
        self.scrollTree.pack(side=RIGHT, fill=Y)

        for self.col in self.cols:
            self.listBox.heading(self.col, text=self.col)
            self.listBox.column('ID Barang', minwidth=0, width=130, stretch=NO, anchor = CENTER)
            self.listBox.column('Nama', minwidth=0, width=270, stretch=NO, anchor = W)
            self.listBox.column('Kategori', minwidth=0, width=170, stretch=NO, anchor = W)
            self.listBox.column('Jenis', minwidth=0, width=110, stretch=NO, anchor = W)
            self.listBox.column('Qty', minwidth=0, width=100, stretch=NO, anchor = CENTER)
            self.listBox.column('Harga', minwidth=0, width=160, stretch=NO, anchor = W)

        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        self.c.execute("""SELECT CONCAT(prefix,a.id_barang) AS id, a.nama, kategori, b.jenis_barang, qty, harga
	                        FROM tb_inventory A
	                        INNER JOIN tb_detail_barang B ON a.nama = b.nama AND a.id_barang = b.id_barang
		                        WHERE a.status_data = %s AND b.status_data = %s
                                AND a.nama LIKE %s AND b.kategori LIKE %s AND b.jenis_barang LIKE %s""",
        ('Aktif','Aktif',"%"+self.cari+"%","%"+self.kategori+"%","%"+self.jenis+"%"))
        self.record = self.c.fetchall()
        self.conn.commit()
        
        for i, (id_barang,nama,kategori,jenis,qty,harga) in enumerate(self.record, start=1):
            self.listBox.insert("", "end", values=(id_barang,nama,kategori,jenis,qty,"Rp {:,},00-".format(harga)), tags=('ganjil',))
            self.conn.close()

        self.listBox.bind('<ButtonRelease-1>',self.GetValue)

    def tabelRecycleBin(self):
        self.frm_tabel_recycle = Frame(self.top, bg='#75B4E7', borderwidth=0)
        self.frm_tabel_recycle.place(x=20,y=170)

        self.scrollTree_recycle = ttk.Scrollbar(self.frm_tabel_recycle, style="TScrollbar", orient='vertical')
        
        self.cols_recycle = ('ID Barang','Nama','Kategori','Jenis','Qty','Harga')
        self.listBox_recycle = ttk.Treeview(self.frm_tabel_recycle, style="listBox.Treeview", columns=self.cols, show='headings', yscrollcommand=self.scrollTree_recycle.set,height=13)
        self.listBox_recycle.pack(side=LEFT, fill=Y)

        self.scrollTree_recycle.config(command=self.listBox_recycle.yview)
        self.scrollTree_recycle.pack(side=RIGHT, fill=Y)

        for self.col in self.cols_recycle:
            self.listBox_recycle.heading(self.col, text=self.col)
            self.listBox_recycle.column('ID Barang', minwidth=0, width=130, stretch=NO, anchor = CENTER)
            self.listBox_recycle.column('Nama', minwidth=0, width=340, stretch=NO, anchor = W)
            self.listBox_recycle.column('Kategori', minwidth=0, width=150, stretch=NO, anchor = W)
            self.listBox_recycle.column('Jenis', minwidth=0, width=110, stretch=NO, anchor = W)
            self.listBox_recycle.column('Qty', minwidth=0, width=80, stretch=NO, anchor = CENTER)
            self.listBox_recycle.column('Harga', minwidth=0, width=130, stretch=NO, anchor = W)

        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        self.c.execute("""SELECT CONCAT(b.prefix,a.id_barang) as ID, a.nama, b.kategori, b.jenis_barang, a.qty, b.harga
	                        from tb_inventory A
	                        inner join tb_detail_barang B on a.nama = b.nama and a.id_barang = b.id_barang
		                        where a.status_data = %s and b.status_data = %s""",
        ('Tidak Aktif','Tidak Aktif'))
        self.record = self.c.fetchall()
        self.conn.commit()
        
        for i, (id_barang,nama,kategori,jenis,qty,harga) in enumerate(self.record, start=1):
            self.listBox_recycle.insert("", "end", values=(id_barang,nama,kategori,jenis,qty,"Rp {:,},00-".format(harga)))
            self.conn.close()
        

        self.listBox_recycle.bind('<ButtonRelease-1>',self.GetValueRecycle)

    def tabelFilteredRecycleBin(self):
        self.frm_tabel_recycle = Frame(self.top, bg='#75B4E7', borderwidth=0)
        self.frm_tabel_recycle.place(x=20,y=170)

        self.scrollTree_recycle = ttk.Scrollbar(self.frm_tabel_recycle, style="TScrollbar", orient='vertical')
        
        self.cols_recycle = ('ID Barang','Nama','Kategori','Jenis','Qty','Harga')
        self.listBox_recycle = ttk.Treeview(self.frm_tabel_recycle, style="listBox.Treeview", columns=self.cols_recycle, show='headings', yscrollcommand=self.scrollTree_recycle.set,height=13)
        self.listBox_recycle.pack(side=LEFT, fill=Y)

        self.scrollTree_recycle.config(command=self.listBox_recycle.yview)
        self.scrollTree_recycle.pack(side=RIGHT, fill=Y)

        for self.col in self.cols_recycle:
            self.listBox_recycle.heading(self.col, text=self.col)
            self.listBox_recycle.column('ID Barang', minwidth=0, width=130, stretch=NO, anchor = CENTER)
            self.listBox_recycle.column('Nama', minwidth=0, width=340, stretch=NO, anchor = W)
            self.listBox_recycle.column('Kategori', minwidth=0, width=150, stretch=NO, anchor = W)
            self.listBox_recycle.column('Jenis', minwidth=0, width=110, stretch=NO, anchor = W)
            self.listBox_recycle.column('Qty', minwidth=0, width=80, stretch=NO, anchor = CENTER)
            self.listBox_recycle.column('Harga', minwidth=0, width=130, stretch=NO, anchor = W)

        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        self.c.execute("""SELECT CONCAT(prefix,a.id_barang) AS id, a.nama, kategori, b.jenis_barang, qty, harga
	                        FROM tb_inventory A
	                        INNER JOIN tb_detail_barang B ON a.nama = b.nama AND a.id_barang = b.id_barang
		                        WHERE a.status_data = %s AND b.status_data = %s
                                AND a.nama LIKE %s AND b.kategori LIKE %s AND b.jenis_barang LIKE %s""",
        ('Tidak Aktif','Tidak Aktif',"%"+self.cari+"%","%"+self.kategori+"%","%"+self.jenis+"%"))
        self.record = self.c.fetchall()
        self.conn.commit()
        
        for i, (id_barang,nama,kategori,jenis,qty,harga) in enumerate(self.record, start=1):
            self.listBox_recycle.insert("", "end", values=(id_barang,nama,kategori,jenis,qty,"Rp {:,},00-".format(harga)))
            self.conn.close()

        self.listBox_recycle.bind('<ButtonRelease-1>',self.GetValueRecycle)


    # Mengganti gambar btn_recycle saat mouse dihover ke button
    def onHover(self, e):
        self.btn_recycle.configure(image=self.img_recycle_orange)
    
    def offHover(self, e):
        self.btn_recycle.configure(image=self.img_recycle)


    # Validasi 
    def validasiNama(self):
        self.nama = ''
        self.nama_temp = str(self.txt_nama.get())

        if self.txt_nama.get() == '':
            self.nama = ''
            messagebox.showwarning("Notification", "Harap masukkan nama barang !")
            return False
        else:
            self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
            self.c = self.conn.cursor()

            self.c.execute("SELECT nama FROM tb_inventory ORDER BY id_barang ASC")
            self.cek_nama_temp = self.c.fetchall()
            self.cek_nama = [self.i[0] for self.i in self.cek_nama_temp]
            
            if self.cek_nama == []:
                self.nama = self.txt_nama.get()
                return True
            else:
                for n in range(0, len(self.cek_nama)):
                    if self.nama_temp.lower() == self.cek_nama[n].lower():
                        self.nama = ''
                        messagebox.showerror("Error", "Barang dengan nama yang sama sudah ada di database !")
                        return False
                self.nama = self.txt_nama.get()
                return True
                        
    def validasiNamaEdit(self):
        self.nama = ''
        self.nama_temp = str(self.txt_nama.get())

        if self.txt_nama.get() == '':
            self.nama = ''
            messagebox.showwarning("Notification", "Harap masukkan nama barang !")
            return False
        else:
            self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
            self.c = self.conn.cursor()

            self.c.execute("SELECT nama FROM tb_inventory ORDER BY id_barang ASC")
            self.cek_nama_temp = self.c.fetchall()
            self.cek_nama = [self.i[0] for self.i in self.cek_nama_temp]
            
            if self.cek_nama == []:
                self.nama = self.txt_nama.get()
                return True
            else:
                self.c.execute("SELECT nama FROM tb_inventory WHERE id_barang <> %s",(self.id_barang,))
                self.cek_nama_kecuali_temp = self.c.fetchall()
                self.cek_nama_kecuali = [self.i[0] for self.i in self.cek_nama_kecuali_temp]
                
                for self.n in range(0, len(self.cek_nama_kecuali)):
                    if self.nama_temp.lower() == self.cek_nama_kecuali[self.n].lower():
                        self.nama = ''
                        messagebox.showerror("Error", "Barang dengan nama yang sama sudah ada di database !\nPilih nama lain !")
                        return False
                self.nama = self.txt_nama.get()
                return True

    def validasiQty(self):
        self.qty_temp = self.txt_qty.get()

        if self.qty_temp == '':
            self.qty = ''
            messagebox.showwarning("Error", "Harap masukkan qty !")
            return False
        elif self.qty_temp.isdigit() == False:
            self.qty = ''
            messagebox.showerror("Error", "Format qty belum benar !")
            return False
        elif int(self.qty_temp) < 0:
            self.qty = ''
            messagebox.showerror("Error", "Jumlah barang tidak boleh kurang dari 0 !")
            return False
        elif int(self.qty_temp) > 100:
            self.qty = ''
            messagebox.showinfo("Error", "Jumlah maksimal barang adalah 100 !")
            return False
        elif self.qty_temp.isdigit() == True:
            self.qty = int(self.qty_temp)
            return True

    def validasiHarga(self):
        self.harga_temp = self.txt_harga.get()

        if self.harga_temp == '':
            self.harga = ''
            messagebox.showwarning("Notification", "Harap masukkan harga !")
            return False
        elif self.harga_temp.isdigit() == False:
            self.harga = ''
            messagebox.showerror("Error", "Format harga belum benar !")
            return False
        elif self.harga_temp.isdigit() == True:
            if int(self.harga_temp) < 500:
                self.harga = ''
                messagebox.showerror("Error", "Harga barang minimal adalah Rp 500,00- !")
                return False
            elif int(self.harga_temp) % 50 != 0:
                self.harga = ''
                messagebox.showerror("Error", "Harga barang hanya boleh kelipatan Rp 50,00- !")
                return False
            elif int(self.harga_temp) > 100000000:
                self.harga = ''
                messagebox.showerror("Error", "Batas maksimal harga barang adalah Rp 100,000,000,00- !")
                return False
            else:
                self.harga = int(self.harga_temp)
                return True

    def validasiKategori(self):
        if self.cmb_kategori.get() == "Pilih Kategori":
            self.prefix = False
            self.kategori = False
            messagebox.showwarning("Notification", "Harap pilih kategori !")
            return False
        else:
            for n in range(0, len(self.lst_kategori)):
                if self.cmb_kategori.get() == self.lst_kategori[n]:
                    self.prefix = self.lst_prefix[n]
                    self.kategori = self.lst_kategori[n]
                    return True

    def validasiJenis(self):
        if self.cmb_jenis.get() == "Pilih Jenis Barang":
            self.jenis = False
            messagebox.showwarning("Notification", "Harap pilih jenis barang !")
            return False
        else:
            for n in range(0, len(self.lst_jenis)):
                if self.cmb_jenis.get() == self.lst_jenis[n]:
                    self.jenis = self.lst_jenis[n]
                    return True

    def validasiId(self):
        if self.id_barang == 0 or self.id_barang == '0':
            messagebox.showwarning("Notification", "Harap pilih barang terlebih dahulu !")
            return False
        else:
            return True


    def validasiTambah(self):
        if self.validasiNama() == True:
            if self.validasiQty() == True:
                if self.validasiHarga() == True:
                    if self.validasiKategori() == True:
                        if self.validasiJenis() == True:
                            return True

    def validasiEdit(self):
        if self.validasiId() == True:
            if self.validasiNamaEdit() == True:
                if self.validasiQty() == True:
                    if self.validasiHarga() == True:
                        if self.validasiKategori() == True:
                            if self.validasiJenis() == True:
                                return True


    # Pengolahan data pada aplikasi
    def dataTambah(self):
        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        if self.validasiTambah() == True:
            try:
                self.hari_ini = datetime.datetime.now()

                self.c.execute("INSERT INTO tb_inventory (nama,qty,dibuat,status_data) VALUES (%s,%s,%s,%s)",
                (self.nama,self.qty,self.hari_ini,'Aktif'))
                self.c.execute("INSERT INTO tb_detail_barang (prefix,nama,kategori,jenis_barang,harga,dibuat,status_data) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (self.prefix,self.nama,self.kategori,self.jenis,self.harga,self.hari_ini,'Aktif'))
                self.conn.commit()

                messagebox.showinfo("information", "Barang berhasil ditambah !")

                self.listBox.destroy()
                self.tabelInventory()

                self.txt_nama.delete(0, END)
                self.txt_qty.delete(0, END)
                self.txt_harga.delete(0, END)
                self.cmb_kategori.set("Pilih Kategori")
                self.cmb_jenis.set("Pilih Jenis Barang")
                self.cmb_tbl_kategori.set(self.lst_tbl_kategori[0])
                self.cmb_tbl_jenis.set(self.lst_tbl_jenis[0])
                self.txt_nama.focus_set()

                self.id_barang = 0

            except Exception as e:
                messagebox.showinfo("error", e)
                print(e)
                self.conn.rollback()
                self.conn.close()

    def dataEdit(self):
        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        if self.validasiEdit() == True:
            try:
                self.hari_ini = datetime.datetime.now()

                self.c.execute("UPDATE tb_inventory SET nama=%s,qty=%s,diubah=%s WHERE id_barang=%s AND status_data=%s",
                (self.nama,self.qty,self.hari_ini,self.id_barang,'Aktif'))
                self.c.execute("UPDATE tb_detail_barang SET prefix=%s,nama=%s,kategori=%s,jenis_barang=%s,harga=%s,diubah=%s WHERE id_barang=%s AND status_data=%s",
                (self.prefix,self.nama,self.kategori,self.jenis,self.harga,self.hari_ini,self.id_barang,'Aktif'))
                self.conn.commit()

                messagebox.showinfo("information", "Barang berhasil diedit !")

                self.txt_nama.delete(0, END)
                self.txt_qty.delete(0, END)
                self.txt_harga.delete(0, END)
                self.cmb_kategori.set("Pilih Kategori")
                self.cmb_jenis.set("Pilih Jenis Barang")
                self.cmb_tbl_kategori.set(self.lst_tbl_kategori[0])
                self.cmb_tbl_jenis.set(self.lst_tbl_jenis[0])
                self.txt_nama.focus_set()

                self.id_barang = 0

                self.listBox.destroy()
                self.tabelInventory()

            except Exception as e:
                messagebox.showinfo("error", e)
                print(e)
                self.conn.rollback()
                self.conn.close()

    def dataHapus(self):
        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        if self.validasiId() == True:
            try:
                self.hari_ini = datetime.datetime.now()

                self.c.execute("UPDATE tb_inventory SET status_data=%s,diubah=%s WHERE id_barang=%s",
                ('Tidak Aktif',self.hari_ini,self.id_barang))
                self.c.execute("UPDATE tb_detail_barang SET status_data=%s,diubah=%s WHERE id_barang=%s",
                ('Tidak Aktif',self.hari_ini,self.id_barang))
                self.conn.commit()

                messagebox.showinfo("information", "Barang berhasil dihapus !")

                self.txt_nama.delete(0, END)
                self.txt_qty.delete(0, END)
                self.txt_harga.delete(0, END)
                self.cmb_kategori.set("Pilih Kategori")
                self.cmb_jenis.set("Pilih Jenis Barang")
                self.cmb_tbl_kategori.set(self.lst_tbl_kategori[0])
                self.cmb_tbl_jenis.set(self.lst_tbl_jenis[0])
                self.txt_nama.focus_set()

                self.id_barang = 0

                self.listBox.destroy()
                self.tabelInventory()
            
            except Exception as e:
                messagebox.showinfo("error", e)
                print(e)
                self.conn.rollback()
                self.conn.close()

    def dataRestore(self):
        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        if self.validasiId() == True:
            try:
                self.hari_ini = datetime.datetime.now()

                self.c.execute("UPDATE tb_inventory SET status_data=%s,diubah=%s WHERE id_barang=%s",
                ('Aktif',self.hari_ini,self.id_barang))
                self.c.execute("UPDATE tb_detail_barang SET status_data=%s,diubah=%s WHERE id_barang=%s",
                ('Aktif',self.hari_ini,self.id_barang))
                self.conn.commit()

                messagebox.showinfo("information", "Barang berhasil dipulihkan !")

                self.cmb_tbl_kategori.set(self.lst_tbl_kategori[0])

                self.id_barang = 0

                self.listBox.destroy()
                self.tabelRecycleBin()

            except Exception as e:
                messagebox.showinfo("error", e)
                print(e)
                self.conn.rollback()
                self.conn.close()


    # Untuk mengambil nilai pada saat tabel di klick
    def GetValue(self, e):
        self.txt_nama.delete(0, END)
        self.txt_qty.delete(0, END)
        self.txt_harga.delete(0, END)
        self.cmb_kategori.set("Pilih Kategori")
        self.cmb_jenis.set("Pilih Jenis Barang")

        rowID = self.listBox.selection()[0]
        select = self.listBox.set(rowID)

        self.id_barang_temp = ''.join(select['ID Barang'])
        self.id_barang = int(self.id_barang_temp[4:])
        
        self.kategori_temp = (select['Kategori'])
        for n in range(0, len(self.lst_kategori)):
            if self.kategori_temp == self.lst_kategori[n]:
                self.kategori = self.lst_kategori[n]

        self.jenis_temp = (select['Jenis'])
        for n in range(0, len(self.lst_jenis)):
            if self.jenis_temp == self.lst_jenis[n]:
                self.jenis = self.lst_jenis[n]

        self.txt_nama.insert(0,select['Nama'])
        self.txt_qty.insert(0,select['Qty'])
        self.cmb_kategori.set(self.kategori)
        self.cmb_jenis.set(self.jenis)

        self.harga_temp = (select['Harga'])
        self.harga = str(self.harga_temp.replace(",","")[3:][:-3])
        self.txt_harga.delete(0, END)
        self.txt_harga.insert(0, self.harga)

    def GetValueRecycle(self, e):
        rowID = self.listBox_recycle.selection()[0]
        select = self.listBox_recycle.set(rowID)

        self.id_barang_temp = ''.join(select['ID Barang'])
        self.id_barang = int(self.id_barang_temp[4:])


    # Untuk memfilter pencarian
    def filterCari(self,sv):
        self.cari = self.txt_cari.get()
        self.kategori = ''
        self.jenis = ''
        if self.cmb_tbl_kategori.get() == self.lst_tbl_kategori[0]:
            self.frm_tabel.destroy()
            self.kategori = ''
            self.tabelFiltered()
        else:
            for n in range(1, len(self.lst_tbl_kategori)):
                if self.cmb_tbl_kategori.get() == self.lst_tbl_kategori[n]:
                    self.frm_tabel.destroy()
                    self.kategori = self.lst_tbl_kategori[n]
                    self.tabelFiltered()
        
        if self.cmb_tbl_jenis.get() == self.lst_tbl_jenis[0]:
            self.frm_tabel.destroy()
            self.jenis = ''
            self.tabelFiltered()
        else:
            for n in range(0, len(self.lst_tbl_jenis)):
                if self.cmb_tbl_jenis.get() == self.lst_tbl_jenis[n]:
                    self.frm_tabel.destroy()
                    self.jenis = self.lst_tbl_jenis[n]
                    self.tabelFiltered()

        self.tabelFiltered()

    def filterCariRecycle(self,sv_recycle):
        self.cari = self.txt_cari_recycle.get()
        self.kategori = ''
        self.jenis = ''

        if self.cmb_tbl_kategori_recycle.get() == self.lst_tbl_kategori_recycle[0]:
            self.frm_tabel.destroy()
            self.kategori = ''
            self.tabelFilteredRecycleBin()
        else:
            for n in range(1, len(self.lst_tbl_kategori_recycle)):
                if self.cmb_tbl_kategori_recycle.get() == self.lst_tbl_kategori_recycle[n]:
                    self.frm_tabel_recycle.destroy()
                    self.kategori = self.lst_tbl_kategori_recycle[n]
                    self.tabelFilteredRecycleBin()
        
        if self.cmb_tbl_jenis_recycle.get() == self.lst_tbl_jenis_recycle[0]:
            self.frm_tabel_recycle.destroy()
            self.jenis = ''
            self.tabelFilteredRecycleBin()
        else:
            for n in range(1, len(self.lst_tbl_jenis_recycle)):
                if self.cmb_tbl_jenis.get() == self.lst_tbl_jenis_recycle[n]:
                    self.frm_tabel_recycle.destroy()
                    self.jenis = self.lst_tbl_jenis_recycle[n]
                    self.tabelFilteredRecycleBin()

        self.tabelFilteredRecycleBin()


    def openRecycle_Bin(self):
        self.txt_cari.delete(0, END)
        self.txt_nama.delete(0, END)
        self.txt_qty.delete(0, END)
        self.txt_harga.delete(0, END)
        self.cmb_kategori.set("Pilih Kategori")
        self.cmb_jenis.set("Pilih Jenis Barang")
        self.cmb_tbl_kategori.set(self.lst_tbl_kategori[0])
        self.cmb_tbl_jenis.set(self.lst_tbl_jenis[0])
        self.txt_nama.focus_set()

        self.id_barang = 0


        self.root.overrideredirect(False)
        self.root.withdraw()
        self.root.attributes('-topmost',False)
        self.windowRecycleBin()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost',True)




if __name__ == "__main__":
    main = ManajemenInventoryWindow()