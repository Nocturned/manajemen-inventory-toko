from tkinter import *
from tkinter import ttk, messagebox

import datetime
import mysql.connector as mysql

from .Setting import *
from .Struk import *

from PIL import Image, ImageTk


class KasirWindow:

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
        self.top.destroy()

    def closeEsc(self,e):
        self.root.destroy()
        self.top.destroy()


    # Untuk menggerakkan header (frame) window
    def mouse_down(self, e):
        self.x = e.x
        self.y = e.y

    def mouse_up(self, e):
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
        self.root.geometry("1000x600")
        self.root_settings = SettingTheme()
        self.root.resizable(True, True)
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
        self.frm_header.bind('<ButtonPress-1>', self.mouse_down)
        self.frm_header.bind('<B1-Motion>', self.mouseDrag)
        self.frm_header.bind('<ButtonRelease-1>', self.mouse_up)
        self.frm_header.bind('<Map>', self.frmMappedRoot)

        self.lbl_header_emoji = Label(self.frm_header, font=("Lucida Sans",17), text="🛒")
        self.lbl_header_emoji.configure(bg='#ff6f00', fg='#FFFFFF')
        self.lbl_header_emoji.pack(side=LEFT, anchor=NW)

        self.lbl_header = Label(self.frm_header, font=("Lucida Sans",16,'bold'), text="Kasir")
        self.lbl_header.configure(bg='#ff6f00', fg='#FFFFFF')
        self.lbl_header.pack(side=LEFT, anchor=SW)

        self.btn_close = Button(self.frm_header, width=3, height=1, command=lambda: [self.close()])
        self.btn_close.configure(font=('Lucida Sans',10,'bold'),text='X',bg='#FF7A00', fg='#E60707', activebackground='#E60707', activeforeground='#FFFFFF')
        self.btn_close.pack(side=RIGHT, anchor=NE, fill=None, expand=False)

        self.btn_min = Button(self.frm_header, width=3, height=1, command=lambda: [self.minimizeRoot()])
        self.btn_min.configure(font=('Lucida Sans',10,'bold'),text='—',bg='#FF7A00', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#FF7A00')
        self.btn_min.pack(side=RIGHT, anchor=NE, fill=None, expand=False)
    

        # Tabel kasir dan keranjang
        self.tabelKasir()
        self.tabelKeranjang()


        ## Body window ##
        self.frm_katalog = Frame(self.root, borderwidth=2, bg="#f08726", relief=GROOVE, height=50,width=448).place(x=40,y=40)
        self.frm_keranjang = Frame(self.root, borderwidth=2, bg="#f08726", relief=GROOVE, height=50,width=448).place(x=520,y=40)
        self.lbl_katalog = Label(self.root, font=("Lucida Sans",22,'bold'),fg='#FFFFFF',bg='#f08726',text="Katalog").place(x=200,y=45)
        self.lbl_keranjang = Label(self.root, font=("Lucida Sans",22,'bold'),fg='#FFFFFF',bg='#f08726',text="Keranjang").place(x=670,y=45)
        self.lbl_cari = Label(self.root, font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#eb8f3b',text="Cari").place(x=40,y=450)
        self.lbl_qty = Label(self.root, font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#eb8f3b',text="Qty").place(x=40,y=490)
        self.lbl_total = Label(self.root, font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#eb8f3b',text="Total").place(x=760,y=450)
        self.lbl_pembayaran = Label(self.root, font=("Lucida Sans",15,'bold'),fg='#FFFFFF',bg='#eb8f3b',text="Pembayaran").place(x=690,y=490)

        self.sv = StringVar()
        self.sv.trace("w", lambda name, index, mode, sv=self.sv: self.filterCari(sv))
        self.txt_cari = Entry(self.root, font=("Lucida Sans",11), width=15, textvariable=self.sv)
        self.txt_cari.place(x=100,y=453)

        self.lst_tbl_kategori = ['Semua', 'Dapur', 'Elektronik', 'Fashion', 'Perawatan Tubuh', 'Alat Tulis Kantor']
        self.cmb_tbl_kategori = ttk.Combobox(self.root, style="TCombobox", state="readonly", font=("Lucida Sans",11,'bold'), value=self.lst_tbl_kategori, width=17)
        self.cmb_tbl_kategori.set(self.lst_tbl_kategori[0])
        self.cmb_tbl_kategori.bind("<<ComboboxSelected>>", self.filterCari)
        self.cmb_tbl_kategori.place(x=250,y=452)

        self.txt_qty = Entry(self.root, font=("Lucida Sans",11), width=5)
        self.txt_qty.place(x=100,y=493)

        self.btn_tambah = ttk.Button(self.root,style="Kasir.TButton",text='Tambah',width=10, command=self.inputKeranjang)
        self.btn_tambah.place(x=250,y=489)

        self.btn_hapus = ttk.Button(self.root,style="TButton",text='Hapus',width=10, command=self.hapusKeranjang)
        self.btn_hapus.place(x=520,y=453)

        self.txt_total = Entry(self.root, font=("Lucida Sans",11), width=14, disabledbackground='#FFFFFF', disabledforeground='#000000', borderwidth=0)
        self.txt_total.insert('end', "Rp 0,00,-")
        self.txt_total.configure(state='disabled', relief=FLAT)
        self.txt_total.place(x=830,y=453)

        self.txt_pembayaran_rp = Entry(self.root, font=("Lucida Sans",11), disabledbackground='#FFFFFF', disabledforeground='#000000', width=3, borderwidth=0)
        self.txt_pembayaran_rp.insert('end', 'Rp')
        self.txt_pembayaran_rp.configure(state='disabled')
        self.txt_pembayaran_rp.place(x=830,y=493)

        self.txt_pembarayan = Entry(self.root, font=("Lucida Sans",11), width=12, borderwidth=0)
        self.txt_pembarayan.place(x=850,y=493)

        self.btn_beli = ttk.Button(self.root,style="TButton",text='Beli',width=10, command=self.bayarKeranjang)
        self.btn_beli.place(x=840,y=540)

        self.root.mainloop()


    # Menunjukkan tabel dari database
    def tabelKasir(self):
        self.select = None

        self.frm_tabel = Frame(self.root, bg='#75B4E7', borderwidth=0)
        self.frm_tabel.place(x=40,y=90)

        self.scrollTree = ttk.Scrollbar(self.frm_tabel, style="TScrollbar", orient='vertical')
        
        self.cols = ('Nama','Kategori','Harga')
        self.listBox = ttk.Treeview(self.frm_tabel, style="listBox.Treeview", columns=self.cols, show='headings', yscrollcommand=self.scrollTree.set,height=16)
        self.listBox.pack(side=LEFT, fill=Y)

        self.scrollTree.config(command=self.listBox.yview)
        self.scrollTree.pack(side=RIGHT, fill=Y)

        for self.col in self.cols:
            self.listBox.heading(self.col, text=self.col)
            self.listBox.column('Nama', minwidth=0, width=200, stretch=NO, anchor = W)
            self.listBox.column('Kategori', minwidth=0, width=130, stretch=NO, anchor = W)
            self.listBox.column('Harga', minwidth=0, width=100, stretch=NO, anchor = W)

        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        self.c.execute("""SELECT a.nama, kategori, harga
	                        FROM tb_inventory A
	                        INNER JOIN tb_detail_barang B ON a.nama = b.nama AND a.id_barang = b.id_barang
		                        WHERE a.status_data = %s AND b.status_data = %s
                                    ORDER BY a.id_barang ASC""",
        ('Aktif','Aktif'))
        self.record = self.c.fetchall()
        self.conn.commit()
        
        for i, (nama,kategori,harga) in enumerate(self.record, start=1):
            self.listBox.insert("", "end", values=(nama,kategori,"Rp {:,},00-".format(harga)))
            self.conn.close()

        self.listBox.bind('<ButtonRelease-1>',self.GetValue)

    def tabelKasirFiltered(self):
        self.select = None

        self.frm_tabel = Frame(self.root, bg='#75B4E7', borderwidth=0)
        self.frm_tabel.place(x=40,y=90)

        self.scrollTree = ttk.Scrollbar(self.frm_tabel, style="TScrollbar", orient='vertical')
        
        self.cols = ('Nama','Kategori','Harga')
        self.listBox = ttk.Treeview(self.frm_tabel, style="listBox.Treeview", columns=self.cols, show='headings', yscrollcommand=self.scrollTree.set,height=16)
        self.listBox.pack(side=LEFT, fill=Y)

        self.scrollTree.config(command=self.listBox.yview)
        self.scrollTree.pack(side=RIGHT, fill=Y)

        for self.col in self.cols:
            self.listBox.heading(self.col, text=self.col)
            # self.listBox.column('ID Barang', minwidth=0, width=130, stretch=NO, anchor = CENTER)
            self.listBox.column('Nama', minwidth=0, width=200, stretch=NO, anchor = W)
            self.listBox.column('Kategori', minwidth=0, width=130, stretch=NO, anchor = W)
            # self.listBox.column('Qty', minwidth=0, width=100, stretch=NO, anchor = CENTER)
            self.listBox.column('Harga', minwidth=0, width=100, stretch=NO, anchor = W)

        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        self.c.execute("""SELECT a.nama, kategori, harga
	                        FROM tb_inventory A
	                        INNER JOIN tb_detail_barang B ON a.nama = b.nama AND a.id_barang = b.id_barang
		                        WHERE a.status_data = %s AND b.status_data = %s
                                    AND a.nama LIKE %s AND b.kategori LIKE %s
                                    ORDER BY a.id_barang ASC""",
        ('Aktif','Aktif', self.cari+"%", self.kategori+"%"))
        self.record = self.c.fetchall()
        self.conn.commit()
        # print(type(self.record))
        # print(self.record[0])
        
        for i, (nama,kategori,harga) in enumerate(self.record, start=1):
            self.listBox.insert("", "end", values=(nama,kategori,"Rp {:,},00-".format(harga)))
            self.conn.close()
        
        # print(self.txt_nama)

        self.listBox.bind('<ButtonRelease-1>',self.GetValue)

    def tabelKeranjang(self):
        self.select_keranjang = None

        self.frm_tabel_keranjang = Frame(self.root, bg='#75B4E7', borderwidth=0)
        self.frm_tabel_keranjang.place(x=520,y=90)

        self.scrollTree_keranjang = ttk.Scrollbar(self.frm_tabel_keranjang, style="TScrollbar", orient='vertical')
        
        self.cols_keranjang = ('Nama','Qty','Total')
        self.listBox_kerangjang = ttk.Treeview(self.frm_tabel_keranjang, style="listBox.Treeview", columns=self.cols_keranjang, show='headings', yscrollcommand=self.scrollTree.set,height=16)
        self.listBox_kerangjang.pack(side=LEFT, fill=Y)

        self.scrollTree_keranjang.config(command=self.listBox_kerangjang.yview)
        self.scrollTree_keranjang.pack(side=RIGHT, fill=Y)

        for self.col in self.cols_keranjang:
            self.listBox_kerangjang.heading(self.col, text=self.col)
            self.listBox_kerangjang.column('Nama', minwidth=0, width=210, stretch=NO, anchor = W)
            self.listBox_kerangjang.column('Qty', minwidth=0, width=100, stretch=NO, anchor = W)
            self.listBox_kerangjang.column('Total', minwidth=0, width=120, stretch=NO, anchor = W)

        self.listBox_kerangjang.bind('<ButtonRelease-1>',self.GetValueKeranjang)


    # Untuk mengambil nilai pada saat tabel di klick
    def GetValue(self, e):
        rowID = self.listBox.selection()[0]
        self.select = self.listBox.set(rowID)

        self.nama = (self.select['Nama'])
        self.kategori = (self.select['Kategori'])
        self.harga_temp = (self.select['Harga'])
        self.harga = int(self.harga_temp.replace(",","")[3:][:-3])

    def GetValueKeranjang(self, e):
        self.select_keranjang = self.listBox_kerangjang.selection()


    def filterCari(self, sv):
        self.cari = self.txt_cari.get()
        self.kategori = ''
        if self.cmb_tbl_kategori.get() == self.lst_tbl_kategori[0]:
            self.frm_tabel.destroy()
            self.kategori = ''
            self.tabelKasirFiltered()
        else:
            for n in range(1, len(self.lst_tbl_kategori)):
                if self.cmb_tbl_kategori.get() == self.lst_tbl_kategori[n]:
                    self.frm_tabel.destroy()
                    self.kategori = self.lst_tbl_kategori[n]
                    self.tabelKasirFiltered()


    # Validasi
    def validasiQty(self):
        self.qty_temp = self.txt_qty.get()

        if self.qty_temp == '':
            self.qty = ''
            messagebox.showwarning("Error", "Harap masukkan jumlah barang yang ingin dibeli !")
            return False
        elif self.qty_temp.isdigit() == False:
            self.qty = ''
            messagebox.showerror("Error", "Format qty belum benar !")
            return False
        elif int(self.qty_temp) < 1:
            self.qty = ''
            messagebox.showerror("Error", "Jumlah barang tidak boleh kurang dari 1 !")
            return False
        else:
            self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
            self.c = self.conn.cursor()

            self.c.execute("SELECT nama,qty FROM tb_inventory WHERE status_data=%s ORDER BY id_barang ASC", ('Aktif',))
            self.cek_stock = self.c.fetchall()
            for n in range(0, len(self.cek_stock)):
                if self.nama == self.cek_stock[n][0]:
                    if int(self.cek_stock[n][1]) == 0:
                        self.qty = ''
                        messagebox.showwarning("Notification", "Stock barang yg dipilih habis !")
                        return False
                    elif int(self.cek_stock[n][1]) - int(self.qty_temp) < 0:
                        self.qty = ''
                        messagebox.showwarning("Notification", "Stock barang tidak mencukupi !")
                        return False
                    else:
                        self.qty = self.qty_temp
                        return True

    def validasiNamaSama(self):
        for child in self.listBox_kerangjang.get_children():
            nm, jml, tot = self.listBox_kerangjang.item(child)["values"]

            jml_baru = int(self.qty)+jml

            tot_str = "Rp {:,},00-".format(jml_baru * self.harga)

            if self.nama == nm:
                self.listBox_kerangjang.item(child, text="", values=(nm, jml_baru, tot_str))
                self.updateTotal()
                return True
        return False

    def validasiPembayaran(self):
        self.bayar_temp = self.txt_pembarayan.get()

        if self.bayar_temp == '':
            self.bayar = ''
            messagebox.showwarning("Notification", "Harap masukkan jumlah pembayaran !")
            return False
        elif self.bayar_temp.isdigit() == False:
            self.bayar = ''
            messagebox.showerror("Error", "Format pembayaran belum benar !")
            return False
        elif self.bayar_temp.isdigit() == True:
            if int(self.bayar_temp) < self.total_semua:
                self.bayar = ''
                messagebox.showerror("Error", "Pembayaran tidak boleh kurang dari total !")
                return False
            elif int(self.bayar_temp) % 50 != 0:
                self.bayar = ''
                messagebox.showerror("Error", "Harga barang hanya boleh kelipatan Rp 50,00- !")
                return False
            elif int(self.bayar_temp) > 100000000:
                self.bayar = ''
                messagebox.showerror("Error", "Kasir hanya menerima uang maximal Rp 100,000,000,00- !")
                return False
            else:
                self.bayar = int(self.bayar_temp)
                return True


    # Fungsi-fungsi
    def inputKeranjang(self):
        if self.select != None:
            if self.validasiQty() == True:
                if self.validasiNamaSama() == False:
                    self.qty = int(self.txt_qty.get())
                    self.total = self.harga * self.qty

                    self.keranjang = [(self.nama, self.qty, self.total)]

                    for i, (nama,qty,total) in enumerate(self.keranjang, start=1):
                        self.listBox_kerangjang.insert("", "end", values=(nama,qty,"Rp {:,},00-".format(total)))
                    
                    self.updateTotal()
        else:
            messagebox.showwarning("Notification", "Barang belum dipilih")

    def hapusKeranjang(self):
        if self.select_keranjang != None:
            for selected_items in self.select_keranjang:
                self.listBox_kerangjang.delete(selected_items)
            
            self.updateTotal()
            self.select_keranjang = None
        else:
            messagebox.showwarning("Notification", "Harap pilih barang untuk dihapus")

    def updateTotal(self):
        self.total_semua = 0
        for child in self.listBox_kerangjang.get_children():
            nm, jml, tot = self.listBox_kerangjang.item(child)["values"]
            totInt = int(tot.replace(",","")[3:][:-3])
            self.total_semua += totInt

        self.txt_total.configure(state='normal')
        self.txt_total.delete(0, END)
        self.txt_total.insert('end', "Rp {:,},00-".format(self.total_semua))
        self.txt_total.configure(state='disabled')

    def bayarKeranjang(self):
        self.hari_ini = datetime.datetime.now()
        if self.listBox_kerangjang.get_children() != ():
            if self.validasiPembayaran() == True:
                isi_keranjang = []
                for child in self.listBox_kerangjang.get_children():
                    nm, jml, tot = self.listBox_kerangjang.item(child)["values"]
                    totInt = int(tot.replace(",","")[3:][:-3])
                    isi_keranjang_temp = [nm, jml, totInt]
                    isi_keranjang.append(isi_keranjang_temp)
                
                for n in range(0, len(isi_keranjang)):
                    try:
                        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
                        self.c = self.conn.cursor()

                        self.c.execute("INSERT INTO tb_riwayat_pembelian (nama,qty,total,dibuat,status_data) VALUES (%s,%s,%s,%s,%s)",
                        (isi_keranjang[n][0], isi_keranjang[n][1], isi_keranjang[n][2],self.hari_ini, 'Aktif'))
                        self.c.execute("UPDATE tb_inventory SET qty=qty-%s,diubah=%s WHERE nama=%s AND status_data=%s",
                        (isi_keranjang[n][1], self.hari_ini, isi_keranjang[n][0], 'Aktif'))
                        self.conn.commit()
                    except Exception as e:
                        print(e)
                        self.conn.rollback()
                        self.conn.close()

                printStruk(self.username, isi_keranjang, self.total_semua, self.bayar)

                self.frm_tabel_keranjang.destroy()
                self.tabelKeranjang()

                self.updateTotal()
                
                self.txt_pembarayan.delete(0, END)

                messagebox.showinfo("Informasi", "Barang berhasil dibeli !")
                messagebox.showinfo("Informasi", "Ambil struk anda didalam folder Struk")
        else:
            messagebox.showwarning("Notification", "Keranjang masih kosong")


if __name__ == "__main__":
    main = KasirWindow()