"""Main file."""

####################################
# TASK MANAGER (v0.1 [22-03-2023]) #
####################################

#Import necessary modules
import tkinter as tk
from app import TaskManagerApp

#Set up a window for the app
root = tk.Tk()
app = TaskManagerApp(master=root, width=1080, height=720)
root.protocol("WM_DELETE_WINDOW", app.save_tasks)
app.master.mainloop()