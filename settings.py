import tkinter as tk
from tkinter import ttk

class GUI(tk.Frame):
    def __init__(self, db):
        self.db = db
        self.root = tk.Tk()
        super().__init__(self.root)
        self.table_name = self.db.getAllTable()[0]
        self.pack()
        self.init_main()

    def init_main(self):
        self.root.title("Settings")
        self.root.resizable(False, False)


        self.toolbar = tk.Frame(self, bg='#595F72', bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        [btn.pack(side=tk.LEFT, padx=5, pady=5) for btn in self.__gen_btns()]

        self.__gen_tree()
        self.__update_tree()



    def __gen_tree(self):
        colums = self.db.getColumsNamesFromTable(self.table_name)
        self.tree = ttk.Treeview(self, height=15, columns=colums, show="headings")
        for c in colums:
            self.tree.column(str(c), anchor=tk.CENTER)
            self.tree.heading(str(c), text=str(c).upper())
        self.tree.pack(side=tk.BOTTOM, fill=tk.X)

        if self.db.getChangedTable(self.table_name):
            self.__insert_btn_add()
            self.__insert_btn_remove()
            self.__insert_btn_redact()

    def __update_tree(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.getAllDataFromTable(self.table_name)]

    def __gen_btns(self):
        btns = []
        for t in self.db.getAllTable():
            btns.append(tk.Button(self.toolbar, text=t, command=lambda t=t: self.open_tables(t), bg="#C3D350", bd=0, compound=tk.TOP, padx=20, pady=5, font=("Arial", 12)))
        return btns

    def open_tables(self, table_name):
        if hasattr(self, "btn_add"):
            self.btn_add.destroy()
            delattr(self, "btn_add")
        if hasattr(self, "btn_remove"):
            self.btn_remove.destroy()
            delattr(self, "btn_remove")
        if hasattr(self, "btn_redact"):
            self.btn_redact.destroy()
            delattr(self, "btn_redact")

        self.close_rbar()

        self.tree.after(10, self.tree.destroy())
        self.table_name = table_name
        self.__gen_tree()
        self.__update_tree()

    def __insert_btn_add(self):
        self.btn_add = tk.Button(self.toolbar, text='+', command=self.add,
                                 bg="#C3D350", bd=0, compound=tk.TOP, width=3, height=1, font=("Arial", 16))
        self.btn_add.pack(side=tk.RIGHT, padx=5, pady=5)

    def __insert_btn_remove(self):
        self.btn_remove = tk.Button(self.toolbar, text='-', command=lambda: self.remove(self.tree.item(self.tree.focus())['values']), bg="#C3D350", bd=0,
                                    compound=tk.TOP, width=3, height=1, font=("Arial", 16))
        self.btn_remove.pack(side=tk.RIGHT, padx=5, pady=5)

    def __insert_btn_redact(self):
        self.btn_redact = tk.Button(self.toolbar, text='r', command=lambda: self.redact(self.tree.item(self.tree.focus())['values']), bg="#C3D350", bd=0,
                                    compound=tk.TOP, width=3, height=1, font=("Arial", 16))
        self.btn_redact.pack(side=tk.RIGHT, padx=5, pady=5)

    def redact(self, data):
        bg = '#575D90'
        fg = '#FFFFFF'
        self.close_rbar()

        if len(data) == 0:
            return

        if self.table_name == 'messages':
            def get_prof_id(list_prof, login):
                for p in list_prof:
                    if login == p['login']:
                        return p['id']
                return None

            def get_prof_login(list_prof, id):
                for p in list_prof:
                    if id == p['id']:
                        return p['login']
                return None

            all_profiles = self.db.getProfile()
            drop_value = [x['login'] for x in all_profiles]

            self.r_bar = tk.Frame(self, bg=bg, bd=2)
            self.r_bar.pack(side=tk.BOTTOM, fill=tk.X)
            l_msg = tk.Label(self.r_bar, text="Message text: ", bg=bg, fg=fg, font=("Arial", 13))
            l_msg.pack(side=tk.LEFT, pady=10)

            msg = ttk.Entry(self.r_bar, font=("Arial", 13))
            msg.insert('', data[2])
            msg.pack(side=tk.LEFT, pady=10)

            l_prof = tk.Label(self.r_bar, text="Profile: ", bg=bg, fg=fg, font=("Arial", 13))
            l_prof.pack(side=tk.LEFT, pady=10)

            prof_dropmenu = ttk.Combobox(self.r_bar, values=drop_value)
            prof_dropmenu.pack(side=tk.LEFT, pady=10)
            prof_dropmenu.current(drop_value.index(get_prof_login(all_profiles, data[3])))

            l_status = tk.Label(self.r_bar, text="Status: ", bg=bg, fg=fg, font=("Arial", 13))
            l_status.pack(side=tk.LEFT, pady=10)

            status_dropmenu = ttk.Combobox(self.r_bar, values=[0, 1])
            status_dropmenu.pack(side=tk.LEFT, pady=10)
            status_dropmenu.current(data[1])

            btn_close = tk.Button(self.r_bar, text="close", command=self.close_rbar, font=("Arial", 13), bg="#C3D350", bd=0)
            btn_close.pack(side=tk.RIGHT, padx=10)
            btn_close = tk.Button(self.r_bar, text="save", font=("Arial", 13), bg="#C3D350", bd=0,
                                  command=lambda: self.save('update', (data[0], msg.get(), get_prof_id(all_profiles, prof_dropmenu.get()), status_dropmenu.get())))
            btn_close.pack(side=tk.RIGHT)
        elif self.table_name == 'profiles':
            self.r_bar = tk.Frame(self, bg=bg, bd=2)
            self.r_bar.pack(side=tk.BOTTOM, fill=tk.X)

            l_login = tk.Label(self.r_bar, text="Login: ", bg=bg, fg=fg, font=("Arial", 13))
            l_login.pack(side=tk.LEFT, pady=10)

            login = ttk.Entry(self.r_bar, font=("Arial", 13))
            login.insert('', data[1])
            login.pack(side=tk.LEFT, pady=10)

            l_password = tk.Label(self.r_bar, text="Password: ", bg=bg, fg=fg, font=("Arial", 13))
            l_password.pack(side=tk.LEFT, pady=10)

            password = ttk.Entry(self.r_bar, font=("Arial", 13))
            password.insert('', data[2])
            password.pack(side=tk.LEFT, pady=10)

            btn_close = tk.Button(self.r_bar, text="close", command=self.close_rbar, font=("Arial", 13), bg="#C3D350",
                                  bd=0)
            btn_close.pack(side=tk.RIGHT, padx=10)
            btn_close = tk.Button(self.r_bar, text="save", font=("Arial", 13), bg="#C3D350", bd=0,
                                  command=lambda: self.save('update', (data[0], login.get(), password.get())))
            btn_close.pack(side=tk.RIGHT)

    def remove(self, data):
        if self.table_name == 'profiles':
            self.db.removeProfile(id=data[0])
        if self.table_name == 'messages':
            self.db.removeMessage(msg_id=data[0])
        self.close_rbar()
        self.__update_tree()

    def add(self):
        bg = '#575D90'
        fg = '#FFFFFF'
        self.close_rbar()
        if self.table_name == 'messages':
            def get_prof_id(list_prof, login):
                for p in list_prof:
                    if login == p['login']:
                        return p['id']
                return None

            all_profiles = self.db.getProfile()
            drop_value = [x['login'] for x in all_profiles]

            self.r_bar = tk.Frame(self, bg=bg, bd=2)
            self.r_bar.pack(side=tk.BOTTOM, fill=tk.X)

            l_msg = tk.Label(self.r_bar, text="Message text: ", bg=bg, fg=fg, font=("Arial", 13))
            l_msg.pack(side=tk.LEFT, pady=10)

            msg = ttk.Entry(self.r_bar, font=("Arial", 13))
            msg.pack(side=tk.LEFT, pady=10)

            l_prof = tk.Label(self.r_bar, text="Profile: ", bg=bg, fg=fg, font=("Arial", 13))
            l_prof.pack(side=tk.LEFT, pady=10)

            prof_dropmenu = ttk.Combobox(self.r_bar, values=drop_value)
            prof_dropmenu.pack(side=tk.LEFT, pady=10)

            l_status = tk.Label(self.r_bar, text="Status: ", bg=bg, fg=fg, font=("Arial", 13))
            l_status.pack(side=tk.LEFT, pady=10)

            status_dropmenu = ttk.Combobox(self.r_bar, values=[0, 1])
            status_dropmenu.pack(side=tk.LEFT, pady=10)


            btn_close = tk.Button(self.r_bar, text="close", command=self.close_rbar, font=("Arial", 13), bg="#C3D350", bd=0)
            btn_close.pack(side=tk.RIGHT, padx=10)
            btn_close = tk.Button(self.r_bar, text="save", font=("Arial", 13), bg="#C3D350", bd=0,
                                  command=lambda: self.save('add', (msg.get(), get_prof_id(all_profiles, prof_dropmenu.get()), status_dropmenu.get())))
            btn_close.pack(side=tk.RIGHT)
        elif self.table_name == 'profiles':
            self.r_bar = tk.Frame(self, bg=bg, bd=2)
            self.r_bar.pack(side=tk.BOTTOM, fill=tk.X)
            l_login = tk.Label(self.r_bar, text="Login: ", bg=bg, fg=fg, font=("Arial", 13))
            l_login.pack(side=tk.LEFT, pady=10)
            login = ttk.Entry(self.r_bar, font=("Arial", 13))
            login.pack(side=tk.LEFT, pady=10)
            l_password = tk.Label(self.r_bar, text="Password: ", bg=bg, fg=fg, font=("Arial", 13))
            l_password.pack(side=tk.LEFT, pady=10)
            password = ttk.Entry(self.r_bar, font=("Arial", 13))
            password.pack(side=tk.LEFT, pady=10)
            btn_close = tk.Button(self.r_bar, text="close", command=self.close_rbar, font=("Arial", 13), bg="#C3D350",
                                  bd=0)
            btn_close.pack(side=tk.RIGHT, padx=10)
            btn_close = tk.Button(self.r_bar, text="save", font=("Arial", 13), bg="#C3D350", bd=0,
                                  command=lambda: self.save('add', (login.get(), password.get())))
            btn_close.pack(side=tk.RIGHT)

    def close_rbar(self):
        if hasattr(self, "r_bar"):
            self.r_bar.destroy()
            delattr(self, "r_bar")

    def save(self, action, data):
        if action == 'add':
            if self.table_name == 'profiles':
                self.db.addProfile(data[0], data[1])
            if self.table_name == 'messages':
                self.db.addMessage(data[0], data[1], data[2])
        elif action == 'update':
            if self.table_name == 'profiles':
                self.db.updateProfile(data[0], data[1], data[2])
            if self.table_name == 'messages':
                self.db.updateMessage(data[0], data[1], data[2], data[3])
        self.close_rbar()
        self.__update_tree()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GUI()
    app.run()
