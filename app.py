"""Create a new file for better organization and comfort."""

#Import necessary modules
import os
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk

class TaskManagerApp:
    """Class for the app."""
    def __init__(self, width:int=1080, height:int=720, master=tk.Tk):
        #Set up the window's title, icon, size, position and color palette
        global WIDTH, HEIGHT
        WIDTH, HEIGHT = width, height
        self.master = master
        self.master.title("Task Manager")
        self.master.iconbitmap("icon.ico")
        self.master.geometry(f"{WIDTH}x{HEIGHT}+{self.master.winfo_screenwidth() // 2 - WIDTH // 2}+{self.master.winfo_screenheight() // 2 - HEIGHT // 2}")
        self.master.resizable(False, False)
        self.master.tk_setPalette(background="grey30", foreground="SystemButtonFace")
        #Set up some fonts
        self.title_font = ("Calibri", 30, "bold")
        self.entry_font = ("Calibri", 20, "normal")
        self.button_font = ("Calibri", 15, "bold")
        self.task_font = ("Consolas", 11, "normal")
        #Bind keys
        self.master.bind("<Return>", lambda event: self.add_task())
        self.master.bind("<Delete>", lambda event: self.delete_task())
        self.master.bind("<Control-a>", lambda event: self.select_all())
        self.master.bind("<Control-A>", lambda event: self.select_all())
        self.master.bind("<Escape>", lambda event: self.unselect())
        #Create an empty lists
        self.tasks = []
        self.checkboxes = []
        #Set up the name of the file where the task will be saved
        self.filename = "tasks.txt"
        #Create the widgets
        self.create_widgets()
        #Open the tasks
        self.open_tasks()

    def create_widgets(self):
        """Create the widgets."""
        #Frame and a template scrollbar
        self.frame = ttk.Frame()
        self.scrollbar = ttk.Scrollbar(self.master, orient=tk.VERTICAL)
        #Label
        self.title_label = tk.Label(self.master, text="TASK MANAGER", font=self.title_font)
        self.title_label.place(relx=0.5, y=40, anchor="center")
        #Entry box
        self.task_entry = tk.Entry(self.master, width=59, font=self.entry_font, borderwidth=2, bg="grey40",
                                   relief="flat", highlightcolor="SystemButtonFace")
        self.task_entry.place(relx=0.44, y=100, anchor="center")
        #Add button
        self.add_button = tk.Button(self.master, text="Add Task", font=self.button_font, 
                                    relief="flat", borderwidth=0, highlightthickness=2, bg="grey40",
                                    command=self.add_task)
        self.add_button.place(relx=0.905, y=100, anchor="center")

        #List box
        self.task_listbox = tk.Listbox(self.master, width=120, height=23, font=self.task_font, 
                                       relief="flat", bg="grey40", highlightthickness=0,
                                       yscrollcommand=self.scrollbar, selectbackground="grey60",
                                       selectborderwidth=0, selectforeground="SystemButtonFace",
                                       selectmode=tk.EXTENDED)
        #Configure the scroll bar and place the list box
        self.scrollbar.config(command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.place(relx=0.5, y=375, anchor="center")
        #Select all button
        self.select_all_button = tk.Button(self.master, text="Select All", font=self.button_font,  
                                    relief="flat", borderwidth=0, highlightthickness=2, bg="grey40", 
                                    command=self.select_all)
        self.select_all_button.place(relx=0.095, y=650, anchor="center")
        #Unselect button
        self.unselect_button = tk.Button(self.master, text="Unselect", font=self.button_font,  
                                    relief="flat", borderwidth=0, highlightthickness=2, bg="grey40", 
                                    command=self.unselect)
        self.unselect_button.place(relx=0.2, y=650, anchor="center")
        #Delete button
        self.delete_button = tk.Button(self.master, text="Delete Task", font=self.button_font,  
                                    relief="flat", borderwidth=0, highlightthickness=2, bg="grey40", 
                                    command=self.delete_task)
        self.delete_button.place(relx=0.315, y=650, anchor="center")
        #Checkboxes NOT WORKING!!!
        #for i, task in enumerate(self.tasks):
        #    var = tk.BooleanVar(value=False)
        #    checkbox = tk.Checkbutton(self.master, text=task, font=self.task_font, variable=var, 
        #                            onvalue=True, offvalue=False, bg="grey30", fg="white",
        #                            selectcolor="grey60", activebackground="grey30")
        #    checkbox.place(relx=0.1, rely=0.06*(i+1))
        #    self.checkboxes.append(var)

    
    def open_tasks(self):
        """Open the tasks from the tasks.txt file."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.tasks = [line.strip() for line in file.readlines()]
                for task in self.tasks:
                    self.task_listbox.insert(tk.END, task)
                file.close()

    def add_task(self) -> str:
        """Add a task to the list."""
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            msgbox.showerror(title="Error", message="Please insert a name for the task!", icon="warning")
            return "NoTaskName"

    def delete_task(self) -> str:
        """Remove a task from the list."""
        selected_tasks = self.task_listbox.curselection()
        if selected_tasks and self.tasks:
            for i in reversed(selected_tasks):
                index = int(i)
                self.tasks.pop(index)
                self.task_listbox.delete(index)
        else:
            msgbox.showerror(title="Error", message="Please select a task to delete!", icon="warning")
            return "NoTaskSelected"

    def select_all(self):
        """Select every item in the list box."""
        self.task_listbox.select_set(0, tk.END)
    
    def unselect(self):
        """Unselect all the selected items."""
        self.task_listbox.select_clear(0, tk.END)
    
    def save_tasks(self):
        """Save the tasks to the tasks.txt file."""
        tasks = self.task_listbox.get(0, tk.END)
        with open(self.filename, "w") as file:
            for task in tasks:
                file.write(f"{task}\n")
            file.close() 
        self.master.destroy()