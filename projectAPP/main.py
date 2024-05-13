import sqlite3
import math
from tkinter import *
from tkinter import messagebox, colorchooser, simpledialog, PhotoImage
from data import scooters, rental_options
from logic import show_timer_window
from styles import *

def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT,
            theme_color TEXT DEFAULT '#F0F0F0' 
        )
    ''')
    conn.commit()
    conn.close()


def register_user(username, password, email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:  
        return False
    finally:
        conn.close()

def check_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    db_password = c.fetchone()
    conn.close()
    if db_password and db_password[0] == password:
        return True
    else:
        return False

def update_user_info(username, email, theme_color):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET email = ?, theme_color = ? WHERE username = ?', (email, theme_color, username))
    conn.commit()
    conn.close()

def get_user_info(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT email, theme_color FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result


def show_rental_options(scooter, user_name):
    rental_window = Toplevel()
    rental_window.title("Select Rental Duration")

    Label(rental_window, text=f"Choose a rental period for the {scooter['color']} scooter:", font=('Helvetica', 14)).pack(pady=10)

    def rent_scooter(option):
        messagebox.showinfo("Rental Confirmed", f"You have rented the scooter for {option['duration']} at ${option['price']}.")
        rental_window.destroy()
        show_timer_window(option['duration'], option['seconds'])

    for option in rental_options:
        Button(rental_window, text=f"{option['duration']} - ${option['price']}",
               command=lambda o=option: rent_scooter(o)).pack(pady=math.ceil(5))

def user_profile(user_name):
    profile_info = get_user_info(user_name)
    if profile_info:
        email, theme_color = profile_info
    else:
        email, theme_color = "", "#F0F0F0" 

    profile_window = Toplevel()
    profile_window.title("Profile Management")
    profile_window.configure(bg=theme_color)

    email_var = StringVar(value=email)

    Label(profile_window, text="Username:", bg=theme_color).pack()
    Label(profile_window, text=user_name, bg=theme_color).pack()

    Label(profile_window, text="Email:", bg=theme_color).pack()
    email_entry = Entry(profile_window, textvariable=email_var)
    email_entry.pack()

    def change_color():
        color_code = colorchooser.askcolor(title="Choose color", initialcolor=theme_color)[1]
        if color_code:
            profile_window.configure(bg=color_code)
            update_user_info(user_name, email_var.get(), color_code)

    Button(profile_window, text="Change Theme Color", command=change_color).pack()
    Button(profile_window, text="Save", command=lambda: update_user_info(user_name, email_var.get(), theme_color)).pack()

def show_main_app(user_name):
    main_app = Toplevel()
    main_app.title("Scooter Rental App")

    user_info = get_user_info(user_name)
    if user_info:
        theme_color = user_info[1]
    else:
        theme_color = "#F0F0F0"

    main_app.configure(bg=theme_color)

    def open_profile():
        user_profile(user_name)

    def select_scooter(scooter):
        main_app.destroy()
        show_rental_options(scooter, user_name)

    Button(main_app, text="Profile", command=open_profile).pack(side='top', anchor='w')
    for scooter in scooters:
        scooter_button = Button(main_app, text=f"{scooter['color']} Scooter - {scooter['max_speed']}",
                                command=lambda s=scooter: select_scooter(s))
        scooter_button.pack(pady=5)

def init_gui():
    app = Tk()
    app.title('Scooter Rental App')

    logo_image = PhotoImage(file='logoo.png')
    logo_label = Label(app, image=logo_image)
    logo_label.image = logo_image
    logo_label.pack(pady=20)



    def on_register():
        def register():
            username = simpledialog.askstring("Username", "Enter username:")
            password = simpledialog.askstring("Password", "Enter password:", show='*')
            email = simpledialog.askstring("Email", "Enter email:")
            if username and password and email and register_user(username, password, email):
                messagebox.showinfo("Success", "Registration successful!")
                show_main_app(username)
            else:
                messagebox.showerror("Error", "Registration failed or incomplete form.")

        register()

    def on_login():
        def login():
            username = simpledialog.askstring("Username", "Enter username:")
            password = simpledialog.askstring("Password", "Enter password:", show='*')
            if username and password and check_user(username, password):
                messagebox.showinfo("Success", "Login successful!")
                show_main_app(username)
            else:
                messagebox.showerror("Error", "Login failed. Check your username and password.")

        login()

    Button(app, text="Register", command=on_register, height=2, width=20).pack(pady=(20, 10))
    Button(app, text="Login", command=on_login, height=2, width=20).pack(pady=10)
    Button(app, text="Quit", command=app.quit, height=2, width=20).pack(pady=(10, 20))

    app.mainloop()

create_db()
init_gui()
