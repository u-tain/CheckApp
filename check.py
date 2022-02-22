from bs4 import BeautifulSoup
import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog
import requests


class Window:
    def __init__(self, title="tata_check", icon='bit.ico'):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("700x150+500+200")
        self.root.resizable(False, False)
        if icon:
            self.root.iconbitmap(resource_path(icon))
        self.url_check = tk.Label(self.root, text="Ссылка:")
        self.url_check.grid(row=2, column=1, stick='w', pady=10, padx=5)
        self.file_name = tk.Label(self.root, text="Имя файла:")
        self.file_name.grid(row=3, column=1, stick='w', padx=5)
        self.file_name = tk.Label(self.root, text="Расположение:")
        self.file_name.grid(row=4, column=1, pady=10, padx=5)
        self.field_url = tk.Entry(self.root)
        self.field_url.grid(row=2, column=2, columnspan=3, stick='we')
        self.field_name = tk.Entry(self.root)
        self.field_name.grid(row=3, column=2, columnspan=3, stick='we')
        self.path_save = tk.Entry(self.root, width=68)
        self.path_save.grid(row=4, column=2, columnspan=2, stick='w')
        self.path_desc = os.path.join(os.path.expanduser("~"), "Desktop")
        self.path_save.insert(0, self.path_desc)
        self.btn1 = tk.Button(self.root, text='Получить табличку', command=self.get_entry)
        self.btn1.grid(row=5, column=2, columnspan=3, stick='we')
        self.btn2 = tk.Button(self.root, text='Очистить', command=self.clear)
        self.btn2.grid(row=5, column=1, stick='we', padx=5)
        self.btn3 = tk.Button(self.root, text='Изменить', command=self.change)
        self.btn3.grid(row=4, column=4, stick='we')
        self.label = tk.Label(self.root)
        self.label.grid(row=6, column=1, columnspan=4, stick='we', pady=30)

        self.root.grid_columnconfigure(0, minsize=40)
        self.root.grid_columnconfigure(1, minsize=50)
        self.root.grid_columnconfigure(2, minsize=250)
        self.root.grid_columnconfigure(3, minsize=170)
        self.root.grid_columnconfigure(4, minsize=80)
        self.root.grid_columnconfigure(5, minsize=50)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.bind("<Control-KeyPress>", self.keypress)

    def run(self):
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Надеюсь ты получил(а) все таблички, чтобы хотел(а)"):
            self.root.destroy()

    def keypress(self, event):
        if event.keycode == 86 and event.keysym != 'v':
            event.widget.event_generate("<<Paste>>")
        elif event.keycode == 67 and event.keysym != 'c':
            event.widget.event_generate("<<Copy>>")

    def clear(self):
        self.field_url.delete(0, tk.END)
        self.field_name.delete(0, tk.END)
        self.label.destroy()
        self.label = tk.Label(self.root)
        self.label.grid(row=6, column=1, columnspan=4, stick='we', pady=30)
        self.root.geometry("700x150+500+200")

    def change(self):
        output_dir = filedialog.askdirectory(initialdir=self.path_desc)
        if output_dir != '':
            self.path_save.delete(0, tk.END)
            self.path_save.insert(0, output_dir)

    def get_entry(self):
        user_url = self.field_url.get()
        user_filename = self.field_name.get()
        path = self.path_save.get()
        if user_url and user_filename.replace(' ', ''):
            if os.path.isdir(path):
                try:
                    make_excel(get_file(user_url), path, user_filename)
                except requests.exceptions.MissingSchema:
                    messagebox.showinfo('Внимание', 'Неверно введена ссылка')
                except (OSError, ValueError):
                    messagebox.showinfo('Внимание', 'Неверно введено имя файла')
                else:
                    self.root.geometry("700x560+500+200")
                    img = PhotoImage(file=resource_path('res.png'))
                    img = img.subsample(3, 3)
                    self.label.image = img
                    self.label['image'] = self.label.image
            else:
                messagebox.showinfo('Внимание', 'Неверно указан путь')
        else:
            messagebox.showinfo('Внимание', 'Остались пустые поля')


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_file(user_url):
    url = user_url
    r = requests.get(url)
    with open('test.html', 'w', encoding='utf-8') as output_file:
        output_file.write(r.text)
    return make_table()


def make_table():
    results = []
    text = open('test.html', 'r', encoding='utf-8')
    soup = BeautifulSoup(text, "lxml")
    product_list = soup.find('div', {'class': 'items'})
    items = product_list.find_all('div', {'class': ['item']})
    for item in items:
        product_name = item.find('table', {'class': 'receipt-row-1'}).find('tr').find('td').find('span', {'class': 'value'}).text
        product_name = product_name.replace("\n", "").replace(";", "").replace("кг", "").replace("шт", "").replace(".","").strip()
        numb = float(item.find('table', {'class': 'receipt-row-2'}).find('tr').find('td').find('span', {'class': 'value'}).text)
        price = float(item.find('table', {'class': 'receipt-row-2'}).find('tr').find('td', {'class': 'receipt-col2'}).find('span',{'class': 'value'}).text)
        results.append({
            'Продукт': product_name,
            'Количество': numb,
            'Стоимость': price
        })
    user_data_df = pd.DataFrame(results)
    text.close()
    os.remove("test.html")
    return user_data_df


def make_excel(df, path, user_name):
    wide = df['Продукт'].str.len().max()
    with pd.ExcelWriter(os.path.join(path, user_name + ".xlsx"), engine='xlsxwriter') as wb:
        df.to_excel(wb, sheet_name='Sheet1', index=False, encoding='cp1251')
        sheet = wb.sheets['Sheet1']
        sheet.set_column(0, 0, wide + 1)
        sheet.set_column('B:B', 12)
        sheet.set_column('C:C', 12)


win = Window()
win.run()
