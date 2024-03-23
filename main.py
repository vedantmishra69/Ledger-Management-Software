import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as message
from tkinter.messagebox import askyesno
import sqlite3
import datetime
import re
import pandas as pd


class Daily_Entry_Frame(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container)
    
        # Create a canvas object and a vertical scrollbar for scrolling it.
        canvas_frame = tk.Frame(self)
        vscrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(canvas_frame, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        canvas.pack()
        vscrollbar.config(command=canvas.yview)
        canvas_frame.pack()

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)
        
        
        def _on_mousewheel(event):         
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

        self.lbl_name = ttk.Label(interior, text="Name:")
        self.lbl_name.grid(row=0, column=0)

        self.ent_name = ttk.Entry(interior)
        self.ent_name.grid(row=0, column=1, columnspan=4, sticky=tk.EW)
        
        self.lbl_area = ttk.Label(interior, text="Area:")
        self.lbl_area.grid(row=1, column=0)

        self.ent_area = ttk.Entry(interior)
        self.ent_area.grid(row=1, column=1, columnspan=4, sticky=tk.EW)

        self.var = tk.StringVar()
        self.var.set("Farmer") # type: ignore

        self.rdb_farmer = ttk.Radiobutton(interior, text="Farmer", variable=self.var, value="Farmer")
        self.rdb_farmer.grid(row=2, column=1, columnspan=2)

        self.rdb_buyer = ttk.Radiobutton(interior, text="Buyer", variable=self.var, value="Buyer")
        self.rdb_buyer.grid(row=2, column=2, columnspan=2)

        self.lbl_item_name = ttk.Label(interior, text="Item name")
        self.lbl_item_name.grid(row=3, column=1)

        self.lbl_item_weight = ttk.Label(interior, text="Weight")
        self.lbl_item_weight.grid(row=3, column=2)
        
        self.lbl_item_rate = ttk.Label(interior, text="Rate")
        self.lbl_item_rate.grid(row=3, column=3)

        self.row_var = 4
        self.ent_list = []
        self.item_data_list = []
        self.item_sum = 0
        self.total_amount = 0
        self.add_cost = 0
        self.dana = 0
        self.com = 0

        self.ent_item_name = ttk.Entry(interior)
        self.ent_item_name.grid(row=self.row_var, column=1)

        self.ent_item_weight = ttk.Entry(interior)
        self.ent_item_weight.grid(row=self.row_var, column=2)
        
        self.ent_item_rate = ttk.Entry(interior)
        self.ent_item_rate.grid(row=self.row_var, column=3)

        self.ent_list.append((self.ent_item_name, self.ent_item_weight, self.ent_item_rate))
        
        self.btn_add = ttk.Button(interior, text="Add item")
        self.btn_add.grid(row=self.row_var+1, column=1, columnspan=2)
        self.btn_add.config(command=self.add_items)

        self.btn_clear = ttk.Button(interior, text="Clear")
        self.btn_clear.grid(row=self.row_var+1, column=2, columnspan=2)
        self.btn_clear.config(command=self.clear)
        
        self.btn_sum = ttk.Button(interior, text="Sum")
        self.btn_sum.grid(row=self.row_var+2, column=1, columnspan=2)
        self.btn_sum.config(command=self.sum_items)

        self.lbl_sum = ttk.Label(interior, text="0")
        self.lbl_sum.grid(row=self.row_var+2, column=2, columnspan=2)

        self.lbl_add_cost = ttk.Label(interior, text="Additional cost: ")
        self.lbl_add_cost.grid(row=self.row_var+3, column=1, columnspan=2)

        self.ent_add_cost = ttk.Entry(interior)
        self.ent_add_cost.grid(row=self.row_var+3, column=2, columnspan=2)
        
        self.lbl_dana = ttk.Label(interior, text="Dana: ")
        self.lbl_dana.grid(row=self.row_var+4, column=1, columnspan=2)

        self.ent_dana = ttk.Entry(interior)
        self.ent_dana.grid(row=self.row_var+4, column=2, columnspan=2)

        self.lbl_com = ttk.Label(interior, text="Comission: ")
        self.lbl_com.grid(row=self.row_var+5, column=1, columnspan=2)

        self.ent_com = ttk.Entry(interior)
        self.ent_com.grid(row=self.row_var+5, column=2, columnspan=2)
        
        self.btn_total = ttk.Button(interior, text="Total")
        self.btn_total.grid(row=self.row_var+6, column=1, columnspan=2)
        self.btn_total.config(command=self.total)

        self.lbl_total = ttk.Label(interior, text="0")
        self.lbl_total.grid(row=self.row_var+6, column=2, columnspan=2)
        
        self.lbl_paid = ttk.Label(interior, text="Paid")
        self.lbl_paid.grid(row=self.row_var+7, column=1, columnspan=2)
        
        self.ent_paid = ttk.Entry(interior)
        self.ent_paid.grid(row=self.row_var+7, column=2, columnspan=2)

        self.btn_add_entry = ttk.Button(self, text="Add entry")
        # self.btn_add_entry.grid(row=self.row_var+8, column=1, columnspan=3)
        self.btn_add_entry.pack(after=canvas_frame)
        self.btn_add_entry.config(command=self.add_entry)
        
        self.btn_back = ttk.Button(self, text="Back")
        self.btn_back.pack(after=self.btn_add_entry)
        self.btn_back.config(command=lambda: controller.show_frame(Start_Page))
        
        self.conn = sqlite3.connect("user.db")
        
    
    def add_items(self):
        self.row_var += 1

        ent_item_name = ttk.Entry(self.interior)
        ent_item_name.grid(row=self.row_var, column=1)

        ent_item_weight = ttk.Entry(self.interior)
        ent_item_weight.grid(row=self.row_var, column=2)
        
        ent_item_rate = ttk.Entry(self.interior)
        ent_item_rate.grid(row=self.row_var, column=3)

        self.ent_list.append((ent_item_name, ent_item_weight, ent_item_rate))

        self.btn_add.grid(row=self.row_var+1, column=1, columnspan=2)
        self.btn_clear.grid(row=self.row_var+1, column=2, columnspan=2)
        
        self.btn_sum.grid(row=self.row_var+2, column=1, columnspan=2)
        self.lbl_sum.grid(row=self.row_var+2, column=2, columnspan=2)

        self.lbl_add_cost.grid(row=self.row_var+3, column=1, columnspan=2)
        self.ent_add_cost.grid(row=self.row_var+3, column=2, columnspan=2)
        
        self.lbl_dana.grid(row=self.row_var+4, column=1, columnspan=2)
        self.ent_dana.grid(row=self.row_var+4, column=2, columnspan=2)

        self.lbl_com.grid(row=self.row_var+5, column=1, columnspan=2)
        self.ent_com.grid(row=self.row_var+5, column=2, columnspan=2)

        self.btn_total.grid(row=self.row_var+6, column=1, columnspan=2)
        self.lbl_total.grid(row=self.row_var+6, column=2, columnspan=2)
        
        self.lbl_paid.grid(row=self.row_var+7, column=1, columnspan=2)
        self.ent_paid.grid(row=self.row_var+7, column=2, columnspan=2)
        
        # self.btn_add_entry.grid(row=self.row_var+8, column=1, columnspan=3)
        
    def sum_items(self):
        total =  0
        data_list = []
        for name, weight, rate in self.ent_list:
            if not name.get() and not weight.get() and not rate.get(): continue
            if not rate.get(): message.showwarning("", "Empty rate field"); return 
            if not weight.get(): message.showwarning("", "Empty weight field"); return 
            if not name.get(): message.showwarning("", "Empty item name field"); return 
            try:
                data_list.append((name.get(), weight.get(), rate.get())) 
                total += float(weight.get()) * float(rate.get())
            except: message.showwarning("", f"Invalid number"); return
        self.item_sum = total
        self.lbl_sum.config(text=total)
        self.item_data_list = data_list.copy()
    
    def total(self):
        if not self.item_data_list: 
            message.showwarning("", "No items entered or click on 'Sum'.")
            return
        total = self.item_sum
        addi_cost = dana = com_cost = 0
        if self.ent_com.get():
            try: 
                if self.var.get() == "Buyer": total += (int(self.ent_com.get()) / 100) * total
                else: total -= (int(self.ent_com.get()) / 100) * total
                com_cost = float(self.ent_com.get())
            except: message.showwarning("", f"Invalid number \"{self.ent_com.get()}\""); return
        if self.ent_add_cost.get():
            try: 
                if self.var.get() == "Buyer": total += float(self.ent_add_cost.get())
                else: total -= float(self.ent_add_cost.get())
                addi_cost = float(self.ent_add_cost.get())
            except: message.showwarning("", f"Invalid number \"{self.ent_add_cost.get()}\""); return
        if self.ent_dana.get():
            try: 
                if self.var.get() == "Buyer": total += float(self.ent_dana.get())
                else: total -= float(self.ent_dana.get())
                dana = float(self.ent_dana.get())
            except: message.showwarning("", f"Invalid number \"{self.ent_dana.get()}\""); return
        self.total_amount = round(total)
        self.add_cost = addi_cost
        self.com = com_cost
        self.dana = dana
        self.lbl_total.config(text=self.total_amount)
    
    def clear(self):
        self.ent_list[0][0].delete(0, tk.END)
        self.ent_list[0][1].delete(0, tk.END)
        self.ent_list[0][2].delete(0, tk.END)
        while len(self.ent_list) > 1:
            name, weight, rate = self.ent_list.pop()
            name.destroy()
            weight.destroy()
            rate.destroy()
            self.row_var -= 1
        self.ent_add_cost.delete(0, tk.END)
        self.ent_dana.delete(0, tk.END)
        self.ent_com.delete(0, tk.END)
        self.ent_paid.delete(0, tk.END)
        self.lbl_total.config(text="0")
        self.lbl_sum.config(text="0")
        self.item_data_list.clear()
        self.total_amount = 0
        self.item_sum = 0
        self.add_cost = 0
        self.dana = 0
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
        item_sum = self.item_sum
        add_cost = self.add_cost
        dana = self.dana
        com = self.com
        total = self.total_amount
        item_names = []
        item_weight = []
        item_rate = []
        for item_name, weight, rate in self.item_data_list:
            item_names.append(self.fix_str(item_name))
            item_weight.append(weight)
            item_rate.append(rate)
        item_name_string = "-".join(item_names)
        item_weight_string = "-".join(item_weight)
        item_rate_string = "-".join(item_rate)
        dues = 0
        if typ == "Buyer": dues += (float(total) - float(paid))
        if typ == "Farmer": dues += (float(paid) - float(total))
        query = """INSERT OR REPLACE INTO daily_entry (date, time, name, area, type, item_names, item_weight, item_rate, item_sum, add_cost, dana, com, total, paid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        query_insert_account = """INSERT INTO accounts (date, time, name, area, type, dues) VALUES (?, ?, ?, ?, ?, ?)"""
        cur = self.conn.cursor()
        cur.execute(query, (date, time, name, area, typ, item_name_string, item_weight_string, item_rate_string, item_sum, add_cost, dana, com, total, paid))
        cur.execute(query_insert_account, (date, time, name, area, typ, dues))
        self.conn.commit()
        message.showinfo("", "Record added")
        
    def get_time(self):
        date = datetime.date.today()
        time = datetime.datetime.now().strftime("%I:%M:%S %p")
        return date, time
    
    def fix_str(self, s):
        s.strip()
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
        
        columns = ('date', 'time', 'name', 'area', 'type', 'sum', 'total', 'paid')
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
        
        self.tree.column('sum', anchor=tk.CENTER, stretch=tk.NO, width=80)
        self.tree.heading('sum', text='Sum')
        
        self.tree.column('total', anchor=tk.CENTER, stretch=tk.NO, width=80)
        self.tree.heading('total', text='Total')
        
        self.tree.column('paid', anchor=tk.CENTER, stretch=tk.NO, width=80)
        self.tree.heading('paid', text='Paid')
        
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        self.tree.grid(row=6, column=0, columnspan=8, sticky='nsew')
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=6, column=8, sticky='ns')
        
        self.btn_back = ttk.Button(self, text="Back")
        self.btn_back.grid(row=7, column=1)
        self.btn_back.config(command=lambda: controller.show_frame(Start_Page))
        
        self.btn_exp = ttk.Button(self, text="Export")
        self.btn_exp.grid(row=7, column=2)
        self.btn_exp.config(command=self.export_records)
        
        self.lbl_total = ttk.Label(self, text="Total:")
        self.lbl_total.grid(row=7, column=4)
        
        self.lbl_sum = ttk.Label(self, text="0")
        self.lbl_sum.grid(row=7, column=5)
        
        self.lbl_total_value = ttk.Label(self, text="0")
        self.lbl_total_value.grid(row=7, column=6)
        
        self.lbl_total_paid = ttk.Label(self, text="0")
        self.lbl_total_paid.grid(row=7, column=7)
        
        self.all_results = None
        
    def fill_records(self):
        self.tree.delete(*self.tree.get_children())
        name = area = typ = date = ''
        item_sum = 0
        total_amt = 0
        total_paid = 0
        if self.ent_name.get(): name = self.fix_str(self.ent_name.get())
        if self.ent_area.get(): area = self.fix_str(self.ent_area.get())
        if self.var.get() != 'Both': typ = self.var.get()
        if self.ent_day.get() and self.ent_month.get() and self.ent_year.get():
            date = f"{self.ent_year.get()}-{self.ent_month.get()}-{self.ent_day.get()}"
        query = f"SELECT date, time, name, area, type, item_sum, total, paid FROM daily_entry WHERE name REGEXP '{name}.*' AND area REGEXP '{area}.*' AND type REGEXP '{typ}' AND date REGEXP '{date}.*'"
        query_all = f"SELECT * FROM daily_entry WHERE name REGEXP '{name}.*' AND area REGEXP '{area}.*' AND type REGEXP '{typ}' AND date REGEXP '{date}.*'"
        results = self.conn.execute(query).fetchall()
        self.all_results = self.conn.execute(query_all).fetchall()
        if not results: message.showinfo("", "No records found")
        for date, time, name, area, typ, sum_, total, paid in results:
            yy, mm, dd = date.split('-')
            fix_date = f"{dd}-{mm}-{yy}"
            total_amt += float(total)
            total_paid += float(paid)
            item_sum += float(sum_)
            self.tree.insert('', tk.END, values=(fix_date, time, name.capitalize(), area.capitalize(), typ, sum_, total, paid))
        self.lbl_total_value.config(text=str(total_amt))
        self.lbl_sum.config(text=str(item_sum))
        self.lbl_total_paid.config(text=str(total_paid))
    
    def item_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            top = tk.Toplevel(self)
            top.grab_set()
            
            columns = ('item_name', 'item_weight', 'item_rate')
            tree = ttk.Treeview(top, columns=columns, show='headings')

            tree.column('item_name', anchor=tk.CENTER, stretch=tk.NO, width=150)
            tree.heading('item_name', text='Item Name')
            tree.column('item_weight', anchor=tk.CENTER, stretch=tk.NO, width=80)
            tree.heading('item_weight', text='Weight')
            tree.column('item_rate', anchor=tk.CENTER, stretch=tk.NO, width=80)
            tree.heading('item_rate', text='Rate')

            date, time, name, area, typ, _, _, _ = record
            name = self.fix_str(name)
            area = self.fix_str(area)
            dd, mm, yy = date.split('-')
            fix_date = f"{yy}-{mm}-{dd}"
            query = f"SELECT item_names, item_weight, item_rate, item_sum, add_cost, dana, com, total, paid FROM daily_entry WHERE date='{fix_date}' AND time='{time}' AND name='{name}' AND area='{area}' AND type='{typ}'"
            result = self.conn.execute(query).fetchone()
            if not result: 
                top.destroy()
                message.showinfo("", "Record not available.")
                return
            item_names = result[0].split('-')
            item_weight = result[1].split('-')
            item_rate = result[2].split('-')
            item_sum, add_cost, dana, com, total, paid = result[3:]
            
            for item_name, weight, rate in zip(item_names, item_weight, item_rate):
                tree.insert('', tk.END, values=(item_name.capitalize(), weight, rate))
            tree.insert('', tk.END, values=("", ""))
            tree.insert('', tk.END, values=("Sum", item_sum))
            tree.insert('', tk.END, values=("Additional cost", add_cost))
            tree.insert('', tk.END, values=("Dana", dana))
            tree.insert('', tk.END, values=("Commision", com))
            tree.insert('', tk.END, values=("Total", total))
            tree.insert('', tk.END, values=("Paid", paid))
                
            top.title(name)
            tree.grid(row=0, column=0, sticky='nsew')
            btn_del = ttk.Button(top, text="Delete")
            btn_del.grid(row=1, column=0)
            scrollbar = ttk.Scrollbar(top, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky='ns')
            
            
            def record_delete():
                ans = askyesno(title="Delete", message="Are you sure that you want to delete?")
                if ans:
                    cur = self.conn.cursor()
                    query = f"DELETE FROM daily_entry WHERE date='{fix_date}' AND time='{time}' AND name='{name}' AND area='{area}' AND type='{typ}'"
                    query_acc = f"DELETE FROM accounts WHERE date='{fix_date}' AND time='{time}' AND name='{name}' AND area='{area}' AND type='{typ}'"
                    cur.execute(query)
                    cur.execute(query_acc)
                    self.conn.commit()
                    top.destroy()
                    message.showinfo("", "Record deleted.")
            
            btn_del.config(command=record_delete)
            top.mainloop()
            
    def export_records(self):
        cur = self.conn.cursor()
        if not self.all_results: message.showinfo("", "No records found"); return
        df = pd.DataFrame(self.all_results, columns=['Date', 'Time', 'Name', 'Area', 'Type', 'Item names', 'Item weight', 'Item rate', 'Item sum', 'Additional cost', 'Dana', 'Commission', 'Total', 'Paid'])
        df.to_excel('records.xlsx', index=False)
        message.showinfo("", "Records exported")
        cur.close()
                    
            
        
    def fix_str(self, s):
        s.strip()
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
        
        self.rdb_both = ttk.Radiobutton(self, text="Both", variable=self.var, value="Both")
        self.rdb_both.grid(row=2, column=3)
        
        self.btn_add_dues = ttk.Button(self, text="Add dues")
        self.btn_add_dues.grid(row=3, column=0)
        self.btn_add_dues.config(command=self.add_dues)
        
        self.ent_add_dues = ttk.Entry(self)
        self.ent_add_dues.grid(row=3, column=1, columnspan=3, sticky=tk.EW)
        
        self.btn_gen = ttk.Button(self, text="Generate")
        self.btn_gen.grid(row=4, column=1, columnspan=2)
        self.btn_gen.config(command=self.fill_records)
        
        columns = ('date', 'time', 'name', 'area', 'type', 'dues')
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
        
        self.tree.column('dues', anchor=tk.CENTER, stretch=tk.NO, width=80)
        self.tree.heading('dues', text='Dues')
        
        self.tree.grid(row=5, column=0, columnspan=6, sticky='nsew')
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=5, column=6, sticky='ns')
        
        self.btn_back = ttk.Button(self, text="Back")
        self.btn_back.grid(row=6, column=1)
        self.btn_back.config(command=lambda: controller.show_frame(Start_Page))
        
        self.btn_exp = ttk.Button(self, text="Export")
        self.btn_exp.grid(row=6, column=2)
        self.btn_exp.config(command=self.export_records)
        
        self.lbl_total = ttk.Label(self, text="Total:")
        self.lbl_total.grid(row=6, column=4)
        
        self.lbl_total_dues = ttk.Label(self, text="0")
        self.lbl_total_dues.grid(row=6, column=5)
        
        self.conn = sqlite3.connect("user.db")
        self.conn.create_function('regexp', 2, lambda x, y: 1 if re.search(x,y) else 0)
        
        self.results = None
    
    def fill_records(self):
        self.tree.delete(*self.tree.get_children())
        name = area = typ = ''
        total_dues = 0
        if self.ent_name.get(): name = self.fix_str(self.ent_name.get())
        if self.ent_area.get(): area = self.fix_str(self.ent_area.get())
        if self.var.get() != 'Both': typ = self.var.get()
        query = f"SELECT * FROM accounts WHERE name REGEXP '{name}.*' AND area REGEXP '{area}.*' AND type REGEXP '{typ}' AND dues<>0"
        self.results = self.conn.execute(query).fetchall()
        if not self.results: message.showinfo("", "No records found")
        for date, time, name, area, typ, dues in self.results:
            yy, mm, dd = date.split('-')
            fix_date = f"{dd}-{mm}-{yy}"
            total_dues += float(dues)
            self.tree.insert('', tk.END, values=(fix_date, time, name.capitalize(), area.capitalize(), typ, dues))
        self.lbl_total_dues.config(text=str(total_dues))
    
    def export_records(self):
        if not self.results: message.showinfo("", "No records found"); return
        cur = self.conn.cursor()
        df = pd.DataFrame(self.results, columns=['Date', 'Time', 'Name', 'Area', 'Type', 'Dues'])
        df.to_excel('dues.xlsx', index=False) 
        message.showinfo("", "Dues exported")
        cur.close()
        
    
        
        
    def add_dues(self):
        date, time = self.get_time()
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
        query = """INSERT INTO accounts (date, time, name, area, type, dues) VALUES (?, ?, ?, ?, ?, ?)"""
        cur.execute(query, (date, time, name, area, typ, dues))
        message.showinfo("", f"Due of {dues} rupees added on {name}.")
        self.conn.commit()
        
    def get_time(self):
        date = datetime.date.today()
        time = datetime.datetime.now().strftime("%I:%M:%S %p")
        return date, time
    
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
        df = pd.DataFrame(results, columns=['Date', 'Time', 'Name', 'Area', 'Type', 'Item names', 'Item weight', 'Item rate', 'Item sum', 'Additional cost', 'Dana', 'Commission', 'Total', 'Paid'])
        df.to_excel('records.xlsx', index=False)
        message.showinfo("", "Records exported")
        cur.close()
    
    def export_dues(self):
        cur = self.conn.cursor()
        query = "SELECT * FROM accounts"
        results = cur.execute(query).fetchall()
        df = pd.DataFrame(results, columns=['Date', 'Time', 'Name', 'Area', 'Type', 'Dues'])
        df.to_excel('dues.xlsx', index=False) 
        message.showinfo("", "Dues exported")
        cur.close()
            
    
    
class Start_Page(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container)
        
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
            'item_weight   TEXT,'
            'item_rate     TEXT,'
            'item_sum      TEXT,'
            'add_cost      TEXT,'
            'dana          TEXT,'
            'com           TEXT,'
            'total         TEXT,'
            'paid          TEXT' 
            ')'
        )
        
        self.conn.execute(
            'CREATE TABLE IF NOT EXISTS accounts ('
            'date          TEXT,'
            'time          TEXT,'
            'name          TEXT,'
            'area          TEXT,'
            'type          TEXT,'
            'dues          TEXT'
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
            par_frame = tk.Frame(container, width=800, height=500)
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
