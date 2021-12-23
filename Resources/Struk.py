from fpdf import FPDF
import string
import random

import datetime

class printStruk():
    def header(self):
        hari_ini = datetime.datetime.now()
        self.jam = hari_ini.hour
        self.menit = hari_ini.minute
        self.hari = hari_ini.day
        self.bulan = hari_ini.month
        self.tahun = hari_ini.year

        self.pdf.set_font('times', '', 24)

        self.pdf.cell(0,5, "Toko", align='C', ln=1)
        self.pdf.cell(0,15, "Sahabat Masyarakat", align='C', ln=1)
        self.pdf.ln(10)

        s = 10
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = s))
        struk_tgl = '{}:{}   {}/{}/{}'.format(self.jam,self.menit, self.hari,self.bulan,self.tahun)
        self.pdf.set_font('times', '', 16)
        self.pdf.cell(0,5, "No. Pembelian: {}".format(str(ran.lower())), align='L')
        self.pdf.cell(0,5, struk_tgl, align='R', ln=1)
        self.pdf.ln(5)

        self.pdf.line(10, 47, 140, 47)


    def __init__(self, username, list_item, total, pembayaran):
        self.username = username
        self.list_item = list_item
        self.total = total
        self.pembayaran = pembayaran        

        x = 150
        y = 110
        for i in range(0, len(self.list_item)):
            y += 15
            panjang_struk = (x, y)

        self.pdf = FPDF('P', 'mm', panjang_struk)

        self.pdf.set_title("Struk Belanjaan di Toko Sahabat Masyarakat")
        self.pdf.set_author(self.username)
        self.pdf.set_auto_page_break(auto=False,margin=20)
        self.pdf.add_page()

        self.header()

        self.pdf.page
        self.pdf.set_font('times', '', 14)

        for i in range(0, len(self.list_item)):
            self.pdf.cell(5,10, "{}".format(self.list_item[i][0]), ln=1) # untuk nama barang

            self.pdf.cell(10)
            self.pdf.cell(8,5, "{}".format(self.list_item[i][1]), align='L') # untuk jumlah barang
            self.pdf.cell(8,5, "x", align='L')
            self.pdf.cell(10,5, "Rp {:,},00-".format(self.list_item[i][2]), align='L') # untuk harga barang

            self.pdf.cell(100,5, "=", align='C')

            total_barang = self.list_item[i][1] * self.list_item[i][2]

            self.pdf.cell(0,5, "Rp {:,},00-".format(total_barang), ln=1, align='R') # untuk total harga barang

        self.footer()

        nama_struk = "Struk/receipt ({}.{}__{}-{}-{}).pdf".format(self.jam,self.menit, self.hari,self.bulan,self.tahun)
        self.pdf.output(nama_struk)


    def footer(self):
        spc_u = " "
        for i in range(103): spc_u += " "

        self.pdf.ln(10)
        self.pdf.set_font('times', 'U', 14)
        self.pdf.cell(0,0, spc_u, align='L', ln=1)
        self.pdf.ln(5)

        self.pdf.set_font('times', '', 14)

        self.pdf.cell(0,10, "Total", align='L')
        self.pdf.cell(-87,10, "=", align='C')
        self.pdf.cell(0,10, "Rp {:,},00-".format(self.total), align='R', ln=1)

        self.pdf.cell(0,10, "Pembayaran", align='L')
        self.pdf.cell(-87,10, "=", align='C')
        self.pdf.cell(0,10, "Rp {:,},00-".format(self.pembayaran), ln=1, align='R')

        self.pdf.set_font('times', 'U', 14)
        self.pdf.cell(0,0, spc_u, align='L', ln=1)
        self.pdf.ln(5)

        self.kembalian = self.pembayaran - self.total
        self.pdf.set_font('times', '', 14)
        self.pdf.cell(0,10, "Kembalian", align='L')
        self.pdf.cell(-87,10, "=", align='C')
        self.pdf.cell(0,10, "Rp {:,},00-".format(self.kembalian), ln=1, align='R')


if __name__ == "__main__":
    printStruk()