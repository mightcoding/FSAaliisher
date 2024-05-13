import sqlite3
import math
from data import rental_options, scooters
from tkinter import *
from tkinter import messagebox, colorchooser, simpledialog

def show_timer_window(duration, seconds):
    timer_window = Toplevel()
    timer_window.title("Rental Timer")

    time_left = IntVar()
    time_left.set(seconds)
    label = Label(timer_window, textvariable=time_left, font=('Helvetica', 24))
    label.pack()

    def update_timer():
        current_time = time_left.get()
        if current_time > 0:
            time_left.set(current_time - 1)
            timer_window.after(1000, update_timer)
        else:
            messagebox.showinfo("Time's up", "Your rental period has ended.")
            timer_window.destroy()

    def cancel_rent():
        timer_window.after_cancel(update_timer)  
        messagebox.showinfo("Rent Cancelled", "Your scooter rent has been cancelled.")
        timer_window.destroy()

    cancel_button = Button(timer_window, text="Cancel Rent", command=cancel_rent)
    cancel_button.pack(pady=10)

    update_timer()