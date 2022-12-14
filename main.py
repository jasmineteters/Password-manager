from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

Y_PADDING = 5
BUTTON_HEIGHT = 1
YOUR_EMAIL_ADDRESS = 'myEmail@email.com'


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_symbols + password_numbers + password_letters

    shuffle(password_list)

    password = "".join(password_list)
    if password_entry.get() == '':
        password_entry.insert(0, password)
        pyperclip.copy(password)
    else:
        password_entry.delete(0, END)
        password_entry.insert(0, password)
        pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            # Clearing the entries
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            # Resetting the focus to the website
            website_entry.focus()
            messagebox.showinfo(title="Success", message="Your password was saved")


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().title()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title={website}, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists")

# ---------------------------- UI SETUP ------------------------------- #

# TODO Window


window = Tk()
window.title("MyPass Manager")
window.config(padx=100, pady=100, bg='white')

# TODO Canvas
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# ---------------------------- LABELS ------------------------------- #

# TODO Website Label
website_label = Label(bg="white", pady=Y_PADDING)
website_label.config(text="Website: ", font=("Times New Roman", 14))
website_label.grid(column=0, row=1)

# TODO email/username Label
email_label = Label(bg="white", pady=Y_PADDING)
email_label.config(text="Email/Username: ", font=("Times New Roman", 14))
email_label.grid(column=0, row=2)

# TODO Password Label
website_label = Label(bg="white", pady=Y_PADDING)
website_label.config(text="Password: ", font=("Times New Roman", 14))
website_label.grid(column=0, row=3)

# ---------------------------- ENTRIES ------------------------------- #

# TODO Website Entry
website_entry = Entry(width=33)
website_entry.grid(column=1, row=1, pady=Y_PADDING)
website_entry.focus()

# TODO Email/Username Entry
email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2, pady=Y_PADDING)
email_entry.insert(0, YOUR_EMAIL_ADDRESS)

# TODO Password Entry
password_entry = Entry(width=33)
password_entry.grid(column=1, row=3, pady=Y_PADDING)

# ---------------------------- BUTTONS ------------------------------- #

# TODO Password Button
generate_password = Button(pady=Y_PADDING, height=BUTTON_HEIGHT, command=generate_password)
generate_password.config(text="Generate Password")
generate_password.grid(row=3, column=2)

# TODO Add Button
generate_password = Button(height=BUTTON_HEIGHT, width=45, pady=Y_PADDING, command=save)
generate_password.config(text="Add")
generate_password.grid(row=4, column=1, columnspan=2)

# TODO Search Button
search = Button(pady=Y_PADDING, height=BUTTON_HEIGHT, width=15, command=find_password)
search.config(text="Search")
search.grid(row=1, column=2)

window.mainloop()
