from tkinter import *
from tkinter import ttk, messagebox

import mysql.connector as mysql
import hashlib

from Resources.Kasir import *
from Resources.veryVerySecret import *
from Resources.Setting import *
from Resources.Manajemen_Inventory import *


from PIL import Image, ImageTk


class MainWindow:

    # Fungsi header windowKas
    def frmMappedRoot(self, e):
        self.root.update_idletasks()
        self.root.overrideredirect(True)
        self.root.state('normal')
    
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
        self.top.destroy

    def closeEsc(self,e):
        self.root.destroy()
        self.top.destroy()


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
    def __init__(self):
        self.root = Tk()
        self.root_settings = SettingTheme()
        self.root.geometry("900x500")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
        self.root.attributes('-topmost',True)
        self.root.configure(bg='#eb8f3b')
        self.root.option_add("*TCombobox*Listbox*Background", "#FFFFFF")
        self.root.option_add("*TCombobox*Listbox*Foreground", "#F4963F")
        self.root.bind('<Escape>', self.closeEsc)
        self.root.bind('<Return>', self.loginAkunReturn)


        ## Header window ##
        self.x = None
        self.y = None
        self.frm_header = Frame(self.root, bg="#ff6f00", relief='raised', height=35)
        self.frm_header.pack(side=TOP, fill=BOTH)
        self.frm_header.bind('<ButtonPress-1>', self.mouseDown)
        self.frm_header.bind('<B1-Motion>', self.mouseDrag)
        self.frm_header.bind('<ButtonRelease-1>', self.mouseUp)
        self.frm_header.bind('<Map>', self.frmMappedRoot)
    
        self.img_header_emoji = ImageTk.PhotoImage(Image.open("Gambar/userWhite.png").resize((25,25), Image.ANTIALIAS))
        self.lbl_header_emoji = Label(self.frm_header, image=self.img_header_emoji, borderwidth=0, bg='#ff6f00')
        self.lbl_header_emoji.pack(side=LEFT, anchor=W)

        self.lbl_header = Label(self.frm_header, font=("Lucida Sans",16,'bold'), text="Login")
        self.lbl_header.configure(bg='#ff6f00', fg='#FFFFFF')
        self.lbl_header.pack(side=LEFT, anchor=SW)

        self.btn_close = Button(self.frm_header, width=3, height=1, command=lambda: [self.close()])
        self.btn_close.configure(font=('Lucida Sans',10,'bold'),text='X',bg='#FF7A00', fg='#E60707', activebackground='#E60707', activeforeground='#FFFFFF')
        self.btn_close.pack(side=RIGHT, anchor=NE, fill=None, expand=False)

        self.btn_min = Button(self.frm_header, width=3, height=1, command=lambda: [self.minimizeRoot()])
        self.btn_min.configure(font=('Lucida Sans',10,'bold'),text='—',bg='#FF7A00', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#FF7A00')
        self.btn_min.pack(side=RIGHT, anchor=NE, fill=None, expand=False)


        ## Body window ##
        self.frm_login = Frame(self.root, width=310, bg='#eb8f3b').pack(side=RIGHT, fill=Y)

        self.img_login = ImageTk.PhotoImage(Image.open("Gambar/SuperMarketFaded.png").resize((600, 500), Image.ANTIALIAS))
        self.lbl_img_login = Label(self.root, image=self.img_login, borderwidth=0).pack(side=LEFT)

        self.lbl_login1 = Label(self.frm_login, font=('Lucida Sans',22,'bold'),bg="#eb8f3b",fg="#FFFFFF",text="Selamat Datang").place(x=625,y=80)
        self.lbl_login2 = Label(self.frm_login, font=('Lucida Sans',22,'bold'),bg="#eb8f3b",fg="#FFFFFF",text="Di").place(x=720,y=115)
        self.lbl_login3 = Label(self.frm_login, font=('Lucida Sans',22,'bold'),bg="#eb8f3b",fg="#FFFFFF",text="Sahabat Masyarakat").place(x=590,y=150)

        self.lbl_user_pass = Label(self.frm_login, font=('Lucida Sans',11,'bold'),bg="#eb8f3b",fg="#FFFFFF",text="Masukkan Username dan Password").place(x=602,y=250)

        self.img_user = ImageTk.PhotoImage(Image.open("Gambar/userWhite.png").resize((40,40), Image.ANTIALIAS))
        self.lbl_img_user = Label(self.frm_login, image=self.img_user, bg='#eb8f3b', borderwidth=0).place(x=610,y=280)

        self.img_pass = ImageTk.PhotoImage(Image.open("Gambar/keyWhite.png").resize((30,30), Image.ANTIALIAS))
        self.lbl_img_pass = Label(self.frm_login, image=self.img_pass, bg='#eb8f3b', borderwidth=0).place(x=615,y=330)

        self.frm_txt_user = Frame(self.frm_login, width=210, height=30,bg='#FFFFFF').place(x=660,y=283)
        self.txt_user = Entry(self.frm_txt_user,bg='#FFFFFF',width=20,font=('Lucida Sans',12),borderwidth=0)
        self.txt_user.place(x=663,y=288)

        self.frm_txt_pass = Frame(self.frm_login, width=210, height=30,bg='#FFFFFF').place(x=660,y=327)
        self.strv_pass = StringVar()
        self.txt_pass = Entry(self.frm_txt_user,bg='#FFFFFF',width=20,font=('Lucida Sans',12),borderwidth=0,show="*",textvariable=self.strv_pass)
        self.txt_pass.place(x=663,y=332)

        self.intv_pass = IntVar(value=0)
        self.cb_show_pass = ttk.Checkbutton(self.frm_login, style="TCheckbutton",text="Show password")
        self.cb_show_pass.configure(variable=self.intv_pass, onvalue=1, offvalue=0, command=self.showPass)
        self.cb_show_pass.place(x=660,y=365)

        self.btn_masuk = ttk.Button(self.frm_login,style="TButton", text="Masuk", width=10, command=lambda: [self.loginAkun()])
        self.btn_masuk.place(x=695,y=400)


    # Untuk menampilkan password
    def showPass(self):
        if self.intv_pass.get() == 1:
            self.txt_pass.configure(show='')
        else:
            self.txt_pass.configure(show='*')


    # Untuk login akun + validasi
    def loginAkun(self):
        self.username = str(self.txt_user.get())
        self.password = str(self.txt_pass.get())

        self.passSalted = self.password + notSalt()
        self.passEncoded = self.passSalted.encode()
        self.passHashed = hashlib.sha256(self.passEncoded).hexdigest()

        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        self.c.execute("SELECT username,password FROM tb_user WHERE username=%s", (self.username,))
        self.cekLogin = self.c.fetchall()

        if self.username != '':
            if self.cekLogin != []:
                self.cekUser = self.cekLogin[0][0]
                self.cekPass = self.cekLogin[0][1]

                if self.username == self.cekUser:
                    if self.passHashed == self.cekPass:
                        if self.username == 'Admin':
                            self.root.destroy()
                            ManajemenInventoryWindow(self.username)
                        else:
                            self.root.destroy()
                            KasirWindow(self.username)
                    else:
                        messagebox.showwarning("Notification", "Password yang anda masukkan salah !")
                else:
                    messagebox.showerror("Error", "Username belum terdaftar !")
            else:
                messagebox.showerror("Error", "Username belum terdaftar !")
        else:
            messagebox.showwarning("Notification", "Harap masukkan username !")

    def loginAkunReturn(self, e):
        self.username = str(self.txt_user.get())
        self.password = str(self.txt_pass.get())

        self.passSalted = self.password+notSalt()
        self.passEncoded = self.passSalted.encode()
        self.passHashed = hashlib.sha256(self.passEncoded).hexdigest()

        self.conn = mysql.connect(user="root", password="", database='db_Inventory_Toko', host="localhost", port='3306')
        self.c = self.conn.cursor()

        self.c.execute("SELECT username,password FROM tb_user WHERE username=%s", (self.username,))
        self.cekLogin = self.c.fetchall()

        if self.username != '':
            if self.cekLogin != []:
                self.cekUser = self.cekLogin[0][0]
                self.cekPass = self.cekLogin[0][1]

                if self.username == self.cekUser:
                    if self.passHashed == self.cekPass:
                        if self.username == 'Admin':
                            self.root.destroy()
                            ManajemenInventoryWindow(self.username)
                        else:
                            self.root.destroy()
                            KasirWindow(self.username)
                    else:
                        messagebox.showwarning("Notification", "Password yang anda masukkan salah !")
                else:
                    messagebox.showerror("Error", "Username belum terdaftar !")
            else:
                messagebox.showerror("Error", "Username belum terdaftar !")
        else:
            messagebox.showwarning("Notification", "Harap masukkan username !")



if __name__ == "__main__":
    main = MainWindow()
    main.root.mainloop()