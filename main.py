import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as message
import sqlite3
import datetime
import re
import pandas as pd

class Daily_Entry_Frame(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container)

        self.lbl_name = ttk.Label(self, text="Name:")
        self.lbl_name.grid(row=0, column=0)

        self.ent_name = ttk.Entry(self)
        self.ent_name.grid(row=0, column=1, columnspan=3, sticky=tk.EW)
        
        self.lbl_area = ttk.Label(self, text="Area:")
        self.lbl_area.grid(row=1, column=0)

        self.ent_area = ttk.Entry(self)
        self.ent_area.grid(row=1, column=1, columnspan=3, sticky=tk.EW)

        self.var = tk.StringVar()
        self.var.set("Farmer") # type: ignore

        self.rdb_farmer = ttk.Radiobutton(self, text="Farmer", variable=self.var, value="Farmer")
        self.rdb_farmer.grid(row=2, column=1)

        self.rdb_buyer = ttk.Radiobutton(self, text="Buyer", variable=self.var, value="Buyer")
        self.rdb_buyer.grid(row=2, column=2)


        self.lbl_item_name = ttk.Label(self, text="Item name")
        self.lbl_item_name.grid(row=3, column=1)

        self.lbl_item_cost = ttk.Label(self, text="Item cost")
        self.lbl_item_cost.grid(row=3, column=2)

        self.row_var = 4
        self.ent_list = []
        self.item_data_list = []
        self.total_amount = 0
        self.add_cost = 0
        self.com = 0

        self.ent_item_name = ttk.Entry(self)
        self.ent_item_name.grid(row=self.row_var, column=1)

        self.ent_item_cost = ttk.Entry(self)
        self.ent_item_cost.grid(row=self.row_var, column=2)

        self.ent_list.append((self.ent_item_name, self.ent_item_cost))
        
        self.btn_add = ttk.Button(self, text="Add item")
        self.btn_add.grid(row=self.row_var+1, column=1)
        self.btn_add.config(command=self.add_items)

        self.btn_clear = ttk.Button(self, text="Clear")
        self.btn_clear.grid(row=self.row_var+1, column=2)
        self.btn_clear.config(command=self.clear)

        self.lbl_add_cost = ttk.Label(self, text="Additional cost: ")
        self.lbl_add_cost.grid(row=self.row_var+2, column=1)

        self.ent_add_cost = ttk.Entry(self)
        self.ent_add_cost.grid(row=self.row_var+2, column=2)

        self.lbl_com = ttk.Label(self, text="Comission: ")
        self.lbl_com.grid(row=self.row_var+3, column=1)

        self.ent_com = ttk.Entry(self)
        self.ent_com.grid(row=self.row_var+3, column=2)
        
        self.btn_total = ttk.Button(self, text="Total")
        self.btn_total.grid(row=self.row_var+4, column=1)
        self.btn_total.config(command=self.total)

        self.lbl_total = ttk.Label(self, text="0")
        self.lbl_total.grid(row=self.row_var+4, column=2)
        
        self.lbl_paid = ttk.Label(self, text="Paid")
        self.lbl_paid.grid(row=self.row_var+5, column=1)
        
        self.ent_paid = ttk.Entry(self)
        self.ent_paid.grid(row=self.row_var+5, column=2)

        self.btn_add_entry = ttk.Button(self, text="Add entry")
        self.btn_add_entry.grid(row=self.row_var+6, column=1, columnspan=2)
        self.btn_add_entry.config(command=self.add_entry)
        
        self.btn_back = ttk.Button(self, text="Back")
        self.btn_back.grid(row=self.row_var+7, column=0)
        self.btn_back.config(command=lambda: controller.show_frame(Start_Page))
        
        self.conn = sqlite3.connect("user.db")

    
    def add_items(self):
        self.row_var += 1

        ent_item_name = ttk.Entry(self)
        ent_item_name.grid(row=self.row_var, column=1)

        ent_item_cost = ttk.Entry(self)
        ent_item_cost.grid(row=self.row_var, column=2)

        self.ent_list.append((ent_item_name, ent_item_cost))

        self.btn_add.grid(row=self.row_var+1, column=1)
        self.btn_clear.grid(row=self.row_var+1, column=2)
        self.btn_add_entry.grid(row=self.row_var+6, column=1, columnspan=2)

        self.lbl_add_cost.grid(row=self.row_var+2, column=1)
        self.ent_add_cost.grid(row=self.row_var+2, column=2)

        self.lbl_com.grid(row=self.row_var+3, column=1)
        self.ent_com.grid(row=self.row_var+3, column=2)

        self.btn_total.grid(row=self.row_var+4, column=1)
        self.lbl_total.grid(row=self.row_var+4, column=2)
        
        self.lbl_paid.grid(row=self.row_var+5, column=1)
        self.ent_paid.grid(row=self.row_var+5, column=2)
        
        self.btn_back.grid(row=self.row_var+7, column=0)
    
    def total(self):
        total = addi_cost = com_cost = 0
        data_list = []
        for name, cost in self.ent_list:
            if not cost.get() and not name.get(): continue
            if not cost.get(): message.showwarning("", "Empty item cost field"); return 
            if not name.get(): message.showwarning("", "Empty item name field"); return 
            try:
                data_list.append((name.get(), cost.get())) 
                total += int(cost.get())
            except: message.showwarning("", f"Invalid number \"{cost.get()}\""); return
        if self.ent_com.get():
            try: 
                if self.var.get() == "Buyer": total += (int(self.ent_com.get()) / 100) * total
                else: total -= (int(self.ent_com.get()) / 100) * total
                com_cost = int(self.ent_com.get())
            except: message.showwarning("", f"Invalid number \"{self.ent_com.get()}\""); return
        if self.ent_add_cost.get():
            try: 
                if self.var.get() == "Buyer": total += int(self.ent_add_cost.get())
                else: total -= int(self.ent_add_cost.get())
                addi_cost = int(self.ent_add_cost.get())
            except: message.showwarning("", f"Invalid number \"{self.ent_add_cost.get()}\""); return
        self.total_amount = round(total)
        self.add_cost = addi_cost
        self.com = com_cost
        self.item_data_list = data_list.copy()
        self.lbl_total.config(text=self.total_amount)
    
    def clear(self):
        self.ent_list[0][0].delete(0, tk.END)
        self.ent_list[0][1].delete(0, tk.END)
        while len(self.ent_list) > 1:
            name, cost = self.ent_list.pop()
            name.destroy()
            cost.destroy()
            self.row_var -= 1
        self.ent_add_cost.delete(0, tk.END)
        self.ent_com.delete(0, tk.END)
        self.ent_paid.delete(0, tk.END)
        self.lbl_total.config(text="0")
        self.item_data_list.clear()
        self.total_amount = 0
        self.add_cost = 0
        self.com = 0

    def add_entry(self):
        date, time = self.get_time()
        name = self.ent_name.get()
        area = self.ent_area.get()
        paid = self.ent_paid.get()
        if not name or not area or not self.item_data_list or not paid:
            message.showwarning("", "No field should be empty")
            return
        name = self.fix_str(name)
        area = self.fix_str(area)
        typ = str(self.var.get())
        add_cost = self.add_cost
        com = self.com
        total = self.total_amount
        item_names = []
        item_costs = []
        for item_name, item_cost in self.item_data_list:
            item_names.append(self.fix_str(item_name))
            item_costs.append(item_cost)
        item_name_string = "-".join(item_names)
        item_cost_string = "-".join(item_costs)
        cur = self.conn.cursor()
        query = """INSERT OR REPLACE INTO daily_entry (date, time, name, area, type, item_names, item_costs, add_cost, com, total, paid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        query_insert_account = """INSERT OR IGNORE INTO accounts (name, area, type) VALUES (?, ?, ?)"""
        query_dues = """UPDATE accounts SET dues = dues + ? WHERE name = ? AND area = ? AND type = ?"""
        cur.execute(query, (date, time, name, area, typ, item_name_string, item_cost_string, add_cost, com, total, paid))
        dues = 0
        if typ == "Buyer": dues += (int(total) - int(paid))
        if typ == "Farmer": dues += (int(paid) - int(total))
        cur.execute(query_insert_account, (name, area, typ))
        cur.execute(query_dues, (dues, name, area, typ))
        self.conn.commit()
        message.showinfo("", "Record added")
        
    def get_time(self):
        date = datetime.date.today()
        time = datetime.datetime.now().strftime("%I:%M:%S %p")
        return date, time
    
    def fix_str(self, s):
        strr = s.split()
        for i in range(len(strr)):
            strr[i] = strr[i].lower()
        return " ".join(strr)

class Records_Frame(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container)
        
        self.conn = sqlite3.connect("user.db")
        self.conn.create_function('regexp', 2, lambda x, y: 1 if re.search(x,y) else 0)
        
        self.date = str(datetime.date.today()).split('-')
        
        self.lbl_day = ttk.Label(self, text="Day")
        self.lbl_day.grid(row=0, column=0)
        
        self.ent_day = ttk.Entry(self)
        self.ent_day.grid(row=1, column=0, sticky=tk.EW)
        self.ent_day.insert(0, self.date[-1])
        
        self.lbl_month = ttk.Label(self, text="Month")
        self.lbl_month.grid(row=0, column=1)
        
        self.ent_month = ttk.Entry(self,)
        self.ent_month.grid(row=1, column=1, sticky=tk.EW)
        self.ent_month.insert(0, self.date[-2])
        
        self.lbl_year = ttk.Label(self, text="Year")
        self.lbl_year.grid(row=0, column=2)
        
        self.ent_year = ttk.Entry(self)
        self.ent_year.grid(row=1, column=2, sticky=tk.EW)
        self.ent_year.insert(0, self.date[-3])
        
        self.lbl_name = ttk.Label(self, text="Name:")
        self.lbl_name.grid(row=2, column=0)

        self.ent_name = ttk.Entry(self)
        self.ent_name.grid(row=2, column=1, columnspan=2, sticky=tk.EW)
        
        self.lbl_area = ttk.Label(self, text="Area:")
        self.lbl_area.grid(row=3, column=0)

        self.ent_area = ttk.Entry(self)
        self.ent_area.grid(row=3, column=1, columnspan=2, sticky=tk.EW)

        self.var = tk.StringVar()
        self.var.set("Farmer") # type: ignore

        self.rdb_farmer = ttk.Radiobutton(self, text="Farmer", variable=self.var, value="Farmer")
        self.rdb_farmer.grid(row=4, column=0)

        self.rdb_buyer = ttk.Radiobutton(self, text="Buyer", variable=self.var, value="Buyer")
        self.rdb_buyer.grid(row=4, column=1)
        
        self.rdb_buyer = ttk.Radiobutton(self, text="Both", variable=self.var, value="Both")
        self.rdb_buyer.grid(row=4, column=2)
        
        self.btn_gen = ttk.Button(self, text="Generate", command=self.fill_records)
        self.btn_gen.grid(row=5, column=1, columnspan=2)
        
        columns = ('date', 'time', 'name', 'area', 'type', 'total', 'paid')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        
        self.tree.column('date', anchor=tk.CENTER, stretch=tk.NO, width=80)
        self.tree.heading('date', text='Date')
        
        self.tree.column('time', anchor=tk.CENTER, stretch=tk.NO, width=80)
        self.tree.heading('time', text='Time')
        
        self.tree.column('name', anchor=tk.CENTER, stretch=tk.NO, width=120)
        self.tree.heading('name', text='Name')
        
        self.tree.column('area', anchor=tk.CENTER, stretch=tk.NO, width=120)
        self.tree.heading('area', text='Area')
        
        self.tree.column('type', anchor=tk.CENTER, stretch=tk.NO, width=120)
        self.tree.heading('type', text='Type')
        
        self.tree.column('total', anchor=tk.CENTER, stretch=tk.NO, width=80)
        self.tree.heading('total', text='Total')
        
        self.tree.column('paid', anchor=tk.CENTER, stretch=tk.NO, width=80)
        self.tree.heading('paid', text='Paid')
        
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        self.tree.grid(row=6, column=0, columnspan=7, sticky='nsew')
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=6, column=7, sticky='ns')
        
        self.btn_back = ttk.Button(self, text="Back")
        self.btn_back.grid(row=7, column=1, columnspan=2)
        self.btn_back.config(command=lambda: controller.show_frame(Start_Page))
        
        self.lbl_total = ttk.Label(self, text="Total:")
        self.lbl_total.grid(row=7, column=3)
        
        self.lbl_total_value = ttk.Label(self, text="0")
        self.lbl_total_value.grid(row=7, column=4)
        
        self.lbl_total_paid = ttk.Label(self, text="0")
        self.lbl_total_paid.grid(row=7, column=5)
        
    def fill_records(self):
        self.tree.delete(*self.tree.get_children())
        name = area = typ = date = ''
        total_amt = 0
        total_paid = 0
        if self.ent_name.get(): name = self.fix_str(self.ent_name.get())
        if self.ent_area.get(): area = self.fix_str(self.ent_area.get())
        if self.var.get() != 'Both': typ = self.var.get()
        if self.ent_day.get() and self.ent_month.get() and self.ent_year.get():
            date = f"{self.ent_year.get()}-{self.ent_month.get()}-{self.ent_day.get()}"
        query = f"SELECT date, time, name, area, type, total, paid FROM daily_entry WHERE name REGEXP '{name}.*' AND area REGEXP '{area}.*' AND type REGEXP '{typ}' AND date REGEXP '{date}.*'"
        results = self.conn.execute(query).fetchall()
        if not results: message.showinfo("", "No records found")
        for date, time, name, area, typ, total, paid in results:
            yy, mm, dd = date.split('-')
            fix_date = f"{dd}-{mm}-{yy}"
            total_amt += int(total)
            total_paid += int(paid)
            self.tree.insert('', tk.END, values=(fix_date, time, name.capitalize(), area.capitalize(), typ, total, paid))
        self.lbl_total_value.config(text=str(total_amt))
        self.lbl_total_paid.config(text=str(total_paid))
    
    def item_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            top = tk.Toplevel(self)
            
            columns = ('item_name', 'item_cost')
            tree = ttk.Treeview(top, columns=columns, show='headings')

            tree.column('item_name', anchor=tk.CENTER, stretch=tk.NO)
            tree.heading('item_name', text='Item Name')
            tree.column('item_cost', anchor=tk.CENTER, stretch=tk.NO)
            tree.heading('item_cost', text='Item Cost')

            date, time, name, area, typ, _, _ = record
            name = self.fix_str(name)
            area = self.fix_str(area)
            dd, mm, yy = date.split('-')
            fix_date = f"{yy}-{mm}-{dd}"
            query = f"SELECT item_names, item_costs, add_cost, com, total, paid FROM daily_entry WHERE date='{fix_date}' AND time='{time}' AND name='{name}' AND area='{area}' AND type='{typ}'"
            result = self.conn.execute(query).fetchone()
            item_names = result[0].split('-')
            item_costs = result[1].split('-')
            add_cost, com, total, paid = result[2:]
            
            for item_name, item_cost in zip(item_names, item_costs):
                tree.insert('', tk.END, values=(item_name.capitalize(), item_cost))
            tree.insert('', tk.END, values=("", ""))
            tree.insert('', tk.END, values=("Additional cost", add_cost))
            tree.insert('', tk.END, values=("Commision", com))
            tree.insert('', tk.END, values=("Total", total))
            tree.insert('', tk.END, values=("Paid", paid))
                
            top.title(name)
            tree.grid(row=0, column=0, sticky='nsew')
            scrollbar = ttk.Scrollbar(top, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky='ns')
            
            top.mainloop()
        
    def fix_str(self, s):
        strr = s.split()
        for i in range(len(strr)):
            strr[i] = strr[i].lower()
        return " ".join(strr)
    
class Accounts_Frame(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container)
        
        self.lbl_name = ttk.Label(self, text="Name:")
        self.lbl_name.grid(row=0, column=0)

        self.ent_name = ttk.Entry(self)
        self.ent_name.grid(row=0, column=1, columnspan=2, sticky=tk.EW)
        
        self.lbl_area = ttk.Label(self, text="Area:")
        self.lbl_area.grid(row=1, column=0)

        self.ent_area = ttk.Entry(self)
        self.ent_area.grid(row=1, column=1, columnspan=2, sticky=tk.EW)

        self.var = tk.StringVar()
        self.var.set("Farmer") # type: ignore

        self.rdb_farmer = ttk.Radiobutton(self, text="Farmer", variable=self.var, value="Farmer")
        self.rdb_farmer.grid(row=2, column=1)

        self.rdb_buyer = ttk.Radiobutton(self, text="Buyer", variable=self.var, value="Buyer")
        self.rdb_buyer.grid(row=2, column=2)
        
        self.btn_dues = ttk.Button(self, text="Get dues")
        self.btn_dues.grid(row=3, column=0)
        self.btn_dues.config(command=self.get_dues)
        
        self.lbl_dues = ttk.Label(self)
        self.lbl_dues.grid(row=3, column=1)
        
        self.btn_add_dues = ttk.Button(self, text="Add dues")
        self.btn_add_dues.grid(row=4, column=0)
        self.btn_add_dues.config(command=self.add_dues)
        
        self.ent_add_dues = ttk.Entry(self)
        self.ent_add_dues.grid(row=4, column=1, columnspan=2, sticky=tk.EW)
        
        self.btn_back = ttk.Button(self, text="Back")
        self.btn_back.grid(row=5, column=1, columnspan=2)
        self.btn_back.config(command=lambda: controller.show_frame(Start_Page))
        
        self.conn = sqlite3.connect("user.db")
    
    def get_dues(self):
        name = str(self.ent_name.get())
        area = str(self.ent_area.get())
        typ = str(self.var.get())
        if not name or not area or not typ: 
            message.showwarning("", "No fields should be empty.")
            return
        name = self.fix_str(name)
        area = self.fix_str(area)
        query = """SELECT dues FROM accounts WHERE name = ? AND area = ? AND type = ?"""
        dues = self.conn.execute(query, (name, area, typ)).fetchone()
        if dues == None: message.showinfo("", "No user found, add a due of 0 to enter them into the database."); return
        self.lbl_dues.config(text=str(dues[0]))
        
    def add_dues(self):
        name = str(self.ent_name.get())
        area = str(self.ent_area.get())
        typ = str(self.var.get())
        dues = str(self.ent_add_dues.get())
        if not name or not area or not typ or not dues: 
            message.showwarning("", "No fields should be empty.")
            return
        name = self.fix_str(name)
        area = self.fix_str(area)
        cur = self.conn.cursor()
        query_insert_account = """INSERT OR IGNORE INTO accounts (name, area, type) VALUES (?, ?, ?)"""
        query_dues = """UPDATE accounts SET dues = dues + ? WHERE name = ? AND area = ? AND type = ?"""
        cur.execute(query_insert_account, (name, area, typ))
        cur.execute(query_dues, (int(dues), name, area, typ))
        message.showinfo("", f"Due of {dues} rupees added on {name}.")
        self.conn.commit()
    
    def fix_str(self, s):
        strr = s.split()
        for i in range(len(strr)):
            strr[i] = strr[i].lower()
        return " ".join(strr)
        

class Export_Frame(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container)
        
        self.btn_records = ttk.Button(self, text="Export records")
        self.btn_records.grid(row=0, column=0)
        self.btn_records.config(command=self.export_records)
        
        self.btn_dues = ttk.Button(self,text="Export dues")
        self.btn_dues.grid(row=1, column=0)
        self.btn_dues.config(command=self.export_dues)
        
        self.btn_back = ttk.Button(self, text="Back")
        self.btn_back.grid(row=2, column=0)
        self.btn_back.config(command=lambda: controller.show_frame(Start_Page))
        
        self.conn = sqlite3.connect("user.db")

        
    def export_records(self):
        cur = self.conn.cursor()
        query = "SELECT * FROM daily_entry"
        results = cur.execute(query).fetchall()
        df = pd.DataFrame(results, columns=['Date', 'Time', 'Name', 'Area', 'Type', 'Item names', 'Item costs', 'Additional cost', 'Commission', 'Total', 'Paid'])
        df.to_excel('records.xlsx', index=False)
        message.showinfo("", "Records exported")
        cur.close()
    
    def export_dues(self):
        cur = self.conn.cursor()
        query = "SELECT * FROM accounts"
        results = cur.execute(query).fetchall()
        df = pd.DataFrame(results, columns=['Name', 'Area', 'Type', 'Dues'])
        df.to_excel('dues.xlsx', index=False) 
        message.showinfo("", "Dues exported")
        cur.close()
            
    
    
class Start_Page(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container)
        
        self.container = container
        self.btn_daily_entry = ttk.Button(self, text="Daily Entry", command=lambda: controller.show_frame(Daily_Entry_Frame))
        self.btn_daily_entry.grid(row=0, column=0)
        
        self.btn_records = ttk.Button(self, text="Records", command=lambda: controller.show_frame(Records_Frame))
        self.btn_records.grid(row=1, column=0)
        
        self.btn_accounts = ttk.Button(self, text="Accounts", command=lambda: controller.show_frame(Accounts_Frame))
        self.btn_accounts.grid(row=2, column=0)
        
        self.btn_export = ttk.Button(self, text="Export", command=lambda: controller.show_frame(Export_Frame))
        self.btn_export.grid(row=3, column=0)
        
        self.conn = sqlite3.connect("user.db")
        
        self.conn.execute(
            'CREATE TABLE IF NOT EXISTS daily_entry ('
            'date          TEXT,'
            'time          TEXT,'
            'name          TEXT,'
            'area          TEXT,'
            'type          TEXT,'
            'item_names    TEXT,'
            'item_costs    TEXT,'
            'add_cost      TEXT,'
            'com           TEXT,'
            'total         TEXT,'
            'paid          TEXT'   
            ')'
        )
        
        self.conn.execute(
            'CREATE TABLE IF NOT EXISTS accounts ('
            'name          TEXT,'
            'area          TEXT,'
            'type          TEXT,'
            'dues          INTEGER DEFAULT 0,'  
            'PRIMARY KEY   (name, area, type)'
            ')'
        )
        

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Data Entry")
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {}  
  
        for F in (Start_Page, Daily_Entry_Frame, Records_Frame, Accounts_Frame, Export_Frame):
            par_frame = tk.Frame(container, width=700, height=400)
            frame = F(par_frame, self)
            self.frames[F] = par_frame
            frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER) 
            par_frame.grid(row=0, column=0, sticky="nsew")
  

        self.show_frame(Start_Page)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()
