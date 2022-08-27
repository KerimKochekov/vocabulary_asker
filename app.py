from tkinter import *
import random
from PIL import ImageTk,Image

data = []
with open('data.txt') as f:
    for line in f.readlines():
        if len(data) == 25:
            break
        word, meaning = line.split('-')
        data.append((word[:-1], meaning[1:-1]))

class Table:
    def __init__(self,root, answers):
        cur_y = 0.0078
        self.values = []
        self.events = []
        for i in range(len(data)):
            tmp = IntVar()
            checkbox = Checkbutton(root, variable=tmp)
            checkbox.place(relx=0.96, rely = cur_y)
            self.events.append(checkbox)
            cur_y += 0.0378
            self.values.append(tmp)
            for j in range(3):
                entry = Entry(root, width=31, fg='blue', font=('Arial', 16, 'bold'))
                entry.grid(row=i, column=j)
                if j == 2:
                    entry.insert(END, answers[i])
                else:
                    entry.insert(END, data[i][j])
                self.events.append(entry)
    
    def destroy(self):
        for event in self.events:
            event.destroy()

    def get(self):
        result = 0
        for value in self.values:
            result += value.get()
        return (result, len(self.values))

class app:
    def __init__(self):
        self.root = Tk()
        self.answers = []
        self.label_word = None
        self.label_number = None
        self.back_button = None
        self.next_button = None
        self.menu_button = None
        self.finish_button = None
        self.input = None
        app_width = 1200
        app_height = 820
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2)-(app_width/2)
        y = (screen_height/2)-(app_height/2)
        self.root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.root.configure(bg="#ab9cf7")
        self.root.bind('<Return>', self.next_key)
        self.root.bind('<Escape>', self.end_key)
        self.start_page()
        self.root.mainloop()
    
    def end_key(self, event):
        self.root.quit()

    def next_key(self, event):
        # print(event)
        self.getvalue()
        self.increase()
        self.show_page()
        
    def destroy(self, event):
        if event != None:
            event.destroy()
            event = None
    
    def destroy_all(self):
        self.destroy(self.label_word)
        self.destroy(self.label_number)
        self.destroy(self.next_button)
        self.destroy(self.back_button)
        self.destroy(self.menu_button)
        self.destroy(self.finish_button)
        self.destroy(self.input)

    def start_page(self):
        self.destroy_all()
        
        self.answers = [''] * len(data)
        random.shuffle(data)
        self.start_label = Label(self.root, bg = "#ab9cf7", text = "WELCOME TO THE ENGLISH WORD QUIZ GAME",
                                        font = ("Helvetica", 32, "bold"))
        self.start_label.place(relx=0.5, rely=0.4, anchor=CENTER)
        
        self.start_button = Button(self.root, text="START", padx = 250, pady = 15, bg = "#f7ff59", 
                                                            activebackground = "yellow", command = self.first_page)
        self.start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    def first_page(self):
        self.start_label.destroy()
        self.start_button.destroy()
        self.word_number = 0

        self.menu_button = Button(self.root, text = "MENU", font = ('Bold',20), bg = '#1877f2',
                                             fg = 'white', width = 12, command = self.start_page)
        self.finish_button = Button(self.root, text="FINISH", font=('Bold',20), bg = '#1877f2',
                                             fg = 'white', width = 12, command = self.end_page)
        self.back_button = Button(self.root, text = "BACK", font = ('Bold',20), bg = '#1877f2',
                                             fg = 'white', width = 12, command = lambda: [self.decrease(), self.show_page()])
        self.next_button = Button(self.root, text = "NEXT", font = ('Bold',20), bg = '#1877f2',
                                            fg = 'white', width=12, command = lambda: [self.getvalue(), self.increase(), self.show_page()])
        self.input = Entry(self.root, width=30, borderwidth=5, font=("Arial",28,"bold"))

        self.menu_button.place(relx=0, rely=0)
        self.finish_button.place(relx=0.805, rely=0)
        self.next_button.place(relx=0.5, rely=0.94)
        self.back_button.place(relx=0.3, rely=0.94)
        self.input.place(relx=0.5,rely=0.55, anchor=CENTER)
        
        self.show_page()

    def getvalue(self):
        self.answers[self.word_number] = self.input.get()
        self.input.delete(0, 'end')
    
    def decrease(self):
        self.word_number -= 1
        
    def increase(self):
        self.word_number += 1

    def show_page(self):
        if self.word_number < 0:
            return
        if self.word_number >= len(data):
            self.end_page()
            return

        self.destroy(self.label_word)
        self.destroy(self.label_number)
        self.label_word = Label(self.root,bg="#ab9cf7",text=data[self.word_number][0], font=("Helvetica",34,"bold"))
        self.label_word.place(relx=0.5, rely=0.45, anchor=CENTER)
        self.label_number = Label(self.root,bg="#ab9cf7",text=f"{self.word_number + 1}/{len(data)}", font=("Helvetica",25,"bold"))
        self.label_number.place(relx=0.5, rely=0.05, anchor=CENTER)

    def end_page(self):
        self.destroy_all()
        table = Table(self.root, self.answers)
        self.result_button = Button(self.root, text = "RESULT", font = ('Bold',10), bg = '#ff0000',
                                        fg = 'white', width = 20, command = lambda: self.result_page(table))
        self.result_button.place(relx=0.45, rely = 0.95)
    
    def result_page(self, table):
        a, b = table.get()
        table.destroy()
        self.result_button.destroy()

        self.label_word = Label(self.root,bg="#ab9cf7",text=f"Your result\n {a} / {b}\n\n {(100*a)//b}%", font=("Helvetica",34,"bold"))
        self.label_word.place(relx=0.5, rely=0.5, anchor=CENTER)
task = app()
