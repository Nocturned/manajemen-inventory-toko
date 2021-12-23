from tkinter import *
from tkinter import ttk



class SettingTheme:
    def __init__(self):
        self.theme = ttk.Style()
        self.theme.theme_use('clam')
        self.theme.configure("listBox.Treeview.Heading", font=('Lucida Sans', 10,'bold'), foreground="#FFFFFF", background="#FF7A00")
        self.theme.configure("listBox.Treeview.Heading", borderwidth=1,bordercolor="#393939",lightcolor="#FF7A00",darkcolor="#FF7A00")
        self.theme.configure("listBox.Treeview", fieldbackground="#D0D0D0", activebackground="#F4963F")
        self.theme.map("listBox.Treeview", background=[('selected', '#F4963F')], foreground=[('selected','#FFFFFF')])

        self.theme.configure("TCombobox", arrowcolor='#393939')
        self.theme.map("TCombobox", background=[('readonly','#f08726')], foreground=[('readonly','#FFFFFF')])
        self.theme.map("TCombobox", bordercolor=[('readonly','#393939')], darkcolor=[('readonly','#393939')], lightcolor=[('readonly','#393939')])
        self.theme.map("TCombobox", fieldbackground=[('readonly','#f08726')])
        self.theme.map("TCombobox", selectbackground=[('readonly','#f08726')], selectforeground=[('readonly','#FFFFFF')])

        self.theme.configure("TScrollbar", troughcolor='#c9c7c7', background='#F4963F', bordercolor='#393939', darkcolor='#393939', lightcolor='#393939', arrowcolor='#393939')
        self.theme.map("TScrollbar", background=[('active','#F4963F'), ('disabled','#F4963F')])

        self.theme.configure("TButton",background='#f08726',foreground='#FFFFFF')
        self.theme.configure("TButton",bordercolor='#393939',lightcolor='#393939',darkcolor='#393939')
        self.theme.configure("TButton",font=("Lucida Sans",11,'bold'))
        self.theme.map("TButton", foreground=[('active', '#F4963F')])

        self.theme.configure("Login.TButton",background='#f08726',foreground='#FFFFFF')
        self.theme.configure("Login.TButton",bordercolor='#393939',lightcolor='#393939',darkcolor='#393939')
        self.theme.configure("Login.TButton",font=("Lucida Sans",11,'bold'))
        self.theme.map("Login.TButton", foreground=[('active', '#F4963F')])

        self.theme.configure("Kasir.TButton",background='#f08726',foreground='#FFFFFF')
        self.theme.configure("Kasir.TButton",bordercolor='#393939',lightcolor='#393939',darkcolor='#393939')
        self.theme.configure("Kasir.TButton",font=("Lucida Sans",10,'bold'))
        self.theme.map("Kasir.TButton", foreground=[('active', '#F4963F')])

        self.theme.configure("TCheckbutton",indicatorrelief=GROOVE)
        self.theme.configure("TCheckbutton",background='#eb8f3b',foreground='#ffffff',focuscolor='#eb8f3b',font=("Lucida Sans",11,'bold'))
        self.theme.map("TCheckbutton", background=[('readonly','#ffffff'),('disabled','#ffffff'),('active','#eb8f3b')])
        self.theme.map("TCheckbutton", foreground=[('disabled','#eb8f3b'),('readonly','#ffffff'),('active','#ffffff')])
        self.theme.map("TCheckbutton", indicatorcolor=[('selected','#ffffff'),('pressed','#ffffff')])