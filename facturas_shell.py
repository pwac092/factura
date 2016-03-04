from datetime import date
import os
from babel.dates import format_date, format_datetime, format_time
import subprocess
from num2words import num2words



class sales():
    def __init__(self):
        #[(concept,five,ten,excempt),...]
        self.concept = ""
        self.quantity = 0
        self.price = 0
        self.five = 0 
        self.ten = 0
        self.excempt = 0

class invoice():
    def __init__ (self):
        self.name = ""
        self.ruc = ""
        self.date = ""
        self.address = ""
        self.phone = ""
        self.sales = list()
        self.sale_type = ""

    def number_of_sales(self):
        return len(self.sales)

    def add_sale(self, new_sale):
        self.sales.append(new_sale)
#file handling.


def print_header(filename):
    with open(filename, 'w') as f:
        f.write("""
\\documentclass{scrartcl}
\\pdfoptionpdfminorversion=6
\\usepackage[utf8]{inputenc}
\\usepackage{amssymb}
\\usepackage[T1]{fontenc}
\\usepackage[left=0cm,right=0cm,top=0cm,bottom=0cm]{geometry}
\\usepackage{graphicx}
\\usepackage{lpic}
\\setlength{\parindent}{0pt}
\\begin{document}
\\begin{lpic}[]{fact(0.999)} % coords(20)
            """)


def print_invoice(filename, invoice):

    with open(filename, 'a') as f:
        #date
        f.write("\\lbl[l]{36,256;\\textcolor{black}{\\small \\textbf{ "+ invoice.date+"}}}\n")
        f.write("\\lbl[l]{152,255.9;\\textcolor{black}{$\\blacksquare$}}\n")
        f.write("\\lbl[l]{36,118;\\textcolor{black}{\\small \\textbf{ "+ invoice.date+"}}}\n")
        f.write("\\lbl[l]{152,117.9;\\textcolor{black}{$\\blacksquare$}}\n")
        #RUC
        f.write("\\lbl[l]{32,251;\\textcolor{black}{\\small \\textbf{"+invoice.ruc+"}}}\n")
        f.write("\\lbl[l]{153.3,251;\\textcolor{black}{\\small \\textbf{---}}}\n")
        f.write("\\lbl[l]{32,113;\\textcolor{black}{\\small \\textbf{"+invoice.ruc+"}}}\n")
        f.write("\\lbl[l]{153.3,114.6;\\textcolor{black}{\\small \\textbf{---}}}\n")
        #Nombre o razonlsocial
        f.write("\\lbl[l]{56,247;\\textcolor{black}{\\small \\textbf{"+invoice.name+"}}}\n")
        f.write("\\lbl[l]{56,110;\\textcolor{black}{\\small \\textbf{"+invoice.name+"}}}\n")
        #Direccion
        f.write("\\lbl[l]{138,247;\\textcolor{black}{\\small \\textbf{"+invoice.phone+"}}}\n")
        f.write("\\lbl[l]{138,110;\\textcolor{black}{\\small \\textbf{"+invoice.phone+"}}}\n")
        #Telefono
        f.write("\\lbl[l]{40,243;\\textcolor{black}{\\small \\textbf{"+invoice.address+"}}}\n")
        f.write("\\lbl[l]{40,106;\\textcolor{black}{\\small \\textbf{"+invoice.address+"}}}\n")
        #Cantidad
        #f.write("\\lbl[l]{28,232;\\textcolor{black}{\\small{1}}}\n")
        #f.write("\\lbl[l]{28,94.3;\\textcolor{black}{\\small{1}}}\n")

        total_five = 0
        total_ten = 0
        total_excempt = 0
        for sale in invoice.sales:
            #Descripciones
            f.write("\\lbl[l]{34,232;\\textcolor{black}{\\small{" + sale.concept +"}}}\n")
            f.write("\\lbl[l]{34,94.3;\\textcolor{black}{\\small{" + sale.concept +"}}}\n")

            #precio unitario
            f.write("\\lbl[l]{125,232;\\textcolor{black}{\\small{"+str(sale.price) +"}}}\n")
            f.write("\\lbl[l]{125,94.3;\\textcolor{black}{\\small{"+str(sale.price)+"}}}\n")


            if sale.five:
                total_five += int(sale.five)
                if int(sale.five) > 0:
                    #five percent
                    f.write("\\lbl[l]{156.2,232;\\textcolor{black}{\\small{" + str(sale.five) + "}}}\n")
                    f.write("\\lbl[l]{156.2,94.3;\\textcolor{black}{\\small{" + str(sale.five) + "}}}\n")

            if sale.ten:
                total_ten += int(sale.ten)
                if int(sale.ten) > 0:
                    #ten percent
                    f.write("\\lbl[l]{170.2,232;\\textcolor{black}{\\small{"+str(sale.ten)+"}}}\n")
                    f.write("\\lbl[l]{170.2,94.3;\\textcolor{black}{\\small{"+str(sale.ten)+"}}}\n")

            if sale.excempt:
                total_excempt += int(sale.excempt)
                if int(sale.excempt) > 0:
                    #exentas
                    f.write("\\lbl[l]{140.2,232;\\textcolor{black}{\\small{"+str(sale.excempt)+"}}}\n")
                    f.write("\\lbl[l]{140.2,94.3;\\textcolor{black}{\\small{"+str(sale.excempt) +"}}}\n")

        #exentas subtotales
        if total_excempt > 0:
            f.write("\\lbl[l]{140.2,184.5;\\textcolor{black}{\\small{"+str(total_excempt)+"}}}\n")
            f.write("\\lbl[l]{140.2,46.5;\\textcolor{black}{\\small{"+str(total_excempt)+"}}}\n")

        if total_five > 0:
            #five percent subtotales
            f.write("\\lbl[l]{156.2,184.5;\\textcolor{black}{\\small{"+str(total_five)+"}}}\n")
            f.write("\\lbl[l]{156.2,46.5;\\textcolor{black}{\\small{"+str(total_five)+"}}}\n")

        if total_ten > 0:
            #ten percent subtotales
            f.write("\\lbl[l]{170.2,184.5;\\textcolor{black}{\\small{"+str(total_ten)+"}}}\n")
            f.write("\\lbl[l]{170.2,46.5;\\textcolor{black}{\\small{"+str(total_ten)+"}}}\n")

        #Totales a pagar
        f.write("\\lbl[l]{42,180;\\textcolor{black}{\\small{"+num2words((total_excempt + total_five + total_ten), lang='es').title()+ ".--"+"}}}\n")

        f.write("\\lbl[l]{42,42;\\textcolor{black}{\\small{"+num2words((total_excempt + total_five + total_ten), lang='es').title() + ".--"+"}}}\n")

        #Totales IVA
        f.write("\\lbl[l]{54,175.4;\\textcolor{black}{\\small{"+ str(round(total_five * 0.05)) +"}}}\n")
        f.write("\\lbl[l]{77,175.4;\\textcolor{black}{\\small{"+ str(round(total_ten * 0.1)) + "}}}\n")
        f.write("\\lbl[l]{136,175.4;\\textcolor{black}{\\small{"+ str(round((total_five * 0.05) +(total_ten * 0.1)))+"}}}\n")

        f.write("\\lbl[l]{54,37.7;\\textcolor{black}{\\small{"+ str(round(total_five * 0.05)) +"}}}\n")
        f.write("\\lbl[l]{77,37.7;\\textcolor{black}{\\small{"+ str(round(total_ten * 0.1)) + "}}}\n")
        f.write("\\lbl[l]{136,37.7;\\textcolor{black}{\\small{"+ str(round((total_five * 0.05) +(total_ten * 0.1)))+"}}}\n")




def print_trailer(filename):
    with open(filename, 'a') as f:
        f.write("\\end{lpic}\n")
        f.write("\\end{document}\n")
        #complie the file and open to show it.

#print data
def produce_invoice(destination, invoice):
    filename = destination + invoice.date.replace(' ','_') + ".tex"
    print_header(filename)
    #finish the file and compile it.
    print_invoice(filename, new_invoice)
    print_trailer(filename)


#input data
if __name__ == "__main__":

    new_invoice = invoice()

    #read the data. This could come from the console.
    new_invoice.name = input('Nombre: (Universidad Paraguayo Alemana)')
    if new_invoice.name == "":
        new_invoice.name = 'Universidad Paraguayo Alemana'

    new_invoice.ruc = input('RUC: (123123123) ')
    if new_invoice.ruc == "":
        new_invoice.ruc = '2123123123'

    new_invoice.address = input('Direccion: (Lope de Vega esq. Atilio Galfre. San Lorenzo)')
    if new_invoice.address == "":
        new_invoice.address = "Lope de Vega esq. Atilio Galfre. San Lorenzo"

    new_invoice.phone = input('Telefono: (021 514 597)')
    if new_invoice.phone == "":
        new_invoice.phone= "021 514 597"

    todays_date = input('Todays date?(Y/N):')

    if todays_date.upper() == 'N':
        print('Date format:')
        print(format_date(date.today(), locale='es', format='long'))
        new_invoice.date = input('Input date:')
    else:
        new_invoice.date = format_date(date.today(), locale='es', format='long')

    new_invoice.sale_type = 'CONTADO'

    #process sales
    while(True):
        new_sale = sales()

        new_sale.quantity = 1 #this will be usually 1. So fix it for now.

        new_sale.concept = input('Concept: (Servicios de docencia) ')
        if new_sale.concept == "":
            new_sale.concept = "Servicios de docencia"


        new_sale.price = input('Unit price: (18.000.000)')
        if new_sale.price == "":
            new_sale.price = "18000000"

        #new_sale.five = input('Taxed 5%: ') 
        new_sale.five = '0' #this wil usually be 0, so fix it for now.
        if new_sale.five == "":
            new_sale.five = '0'

        new_sale.ten = input('Taxed 10%: (0)')
        if new_sale.ten == "":
            new_sale.ten = '0'

        new_sale.excempt = input('Excempt: (18.000.000)')
        if new_sale.excempt == "":
            new_sale.excempt = '18000000'

        new_invoice.add_sale(new_sale)

        cont = input('Add another entry? (Y/N): (N) ')

        if cont.upper() == 'N' or cont == '':
            #verify(invoice)
            produce_invoice('./invoices/', new_invoice)
            exit()
