from tkinter import *
import sqlite3
import datetime
import random



root = Tk()
root.title('Register')
root.geometry('400x600')
hobby = ['Football', 'Hockey', 'Coding']
hobby_root = Tk()
hobby_root.title('Choose your hobby')
hobby_root.geometry('300x300')
hobby_listbox = Listbox(hobby_root)
hobby_listbox.grid(row=2, column=1, padx=0, pady=0, ipadx=50, ipady=50)
hobby_listbox.insert(1)
#image = Image.open("pointer.gif")
#front_arrow = ImageTk.PhotoImage(image)
#image2 = Image.open("left_arrow.gif")
#back_arrow = ImageTk.PhotoImage(image2)
Label(root, text='Your name').grid(row=0, column=0)
nameTxtBox = Text(root, width=16, height=5)
nameTxtBox.grid(row=0, column=1)
conn = sqlite3.connect('register.db')
c = conn.cursor()
createTblSql = ("CREATE  TABLE IF NOT EXISTS register (time, hobby, id INTEGER DEFAULT 0 NOT NULL, input_name TEXT NOT NULL, CONSTRAINT register_PK PRIMARY KEY(id))")
conn.execute(createTblSql)
i = 5
listbox = Listbox(root)
listbox.grid(row=2, column=1, padx=0, pady=0, ipadx=50, ipady=50)

def get_data():
    global i
    c.execute("SELECT time, id, input_name FROM register")
    rows = c.fetchall()
    root.update_idletasks()
    for row in rows:
        Label(root, text=row[0]).grid(row=i, column=2)
        Label(root, text=row[1]).grid(row=i, column=0)
        Label(root, text=row[2]).grid(row=i, column=1)
        i += 1


class Hobby(object):

    connect = sqlite3.connect('register_hobby.db')
    cursor = connect.cursor()
    createTblhobby = ("CREATE  TABLE IF NOT EXISTS register_hobby (hobby, id INTEGER)")
    connect.execute(createTblhobby)

    def __init__(self, hobby_root, hobby):
        self.root = hobby_root
        self.hobby = hobby
        self.listbox = listbox

    global button_id
    button_id = 0

    def return_prev_hobby(self,):
        global button_id
        self.listbox.delete(0, 'end')
        button_id += 1
        self.listbox.insert(hobby[button_id])

    def go_next_hobby(self):
        global button_id
        self.listbox.delete(0, 'end')
        button_id -= 1
        self.listbox.insert(hobby[button_id])

    def list_buttons(self, root):
        previous_button = Button(self.root, text='Previous', command=self.return_prev_hobby)
        previous_button.grid(row=5, column=5)
        previous_button.pack()
        next_button = Button(self.root, text='Next', command=self.go_next_hobby)
        next_button.grid(row=5, column=1)
        next_button.pack()
        save_button = Button(self.root, text='Next', command=self.choose_hobby)
        save_button.grid(row=6, column=3)
        save_button.pack()

    def choose_hobby(self):
        #insert_hobby = self.connect.execute("INSERT INTO register (hobby, id) VALUES(?, ?)", (chosen_hobby, id))
        pass

    def insert_images(self):
        pass

    def save_text(self):
        pass


def print_data():
    listbox.delete(0, END)
    c.execute("SELECT time, id, input_name FROM register")
    rows = c.fetchall()
    for row in rows:
        listbox.insert(END, row[0])
        listbox.insert(END, row[1])
        listbox.insert(END, row[2])

def savetext():
    name = nameTxtBox.get('1.0', END)
    print(name)
    conn.execute("INSERT INTO register (time, input_name) VALUES(?, ?)", (str(datetime.datetime.now()), name))
    conn.commit()
    print_data()



def tablereset():
    conn.execute("DELETE FROM register")
    conn.commit()
    root.update_idletasks()
    resetroot.destroy()
    root.destroy()
    hobby_root.destroy()


def resettable():
    global resetroot
    resetroot = Tk()
    resetroot.title("Delete Table?")
    resetroot.geometry('200x200')
    delete = Button(resetroot, text="Del list", command=tablereset)
    delete.grid(row=0, column=0)
    not_delete = Button(resetroot, text="Cancel", command=resetroot.destroy)
    not_delete.grid(row=1, column=0)

Hobby(hobby_root, hobby)


w = Button(root, text='Register', command=savetext)
w.grid(row=0, column=2)
w.pack

f = Button(root, text='Reset', command=resettable)
f.grid(row=3, column=1)
f.pack




root.mainloop()