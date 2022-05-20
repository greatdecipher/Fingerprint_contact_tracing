from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from tkinter import messagebox

from animations.windows_gui import ImageLabel

import threading

# Function for clearing the
# contents of text entry boxes
from db_modules import convertToBinaryData, insertdata, update_location

from functions_fingerprint import enroll_fingerprint, verify_fingerprint

import datetime

import os

import time
import subprocess as sp

from firebase_modules import upload_to_firebase, download_from_firebase

from data_logging import log_data

root_win = None


# Edit node_location.txt for each Node Devices
with open('/home/pi/Fingerprint_Contact_Tracing/node_location.txt') as f:
    location = f.readline()


# work function
def work():
    global root_win

    print("sleep time start")

    for i in range(60):
        print(i)
        time.sleep(1)

    root_win.destroy()
    root_win.update()

    print("sleep time stop")


def login_f():
    global root_win

    download_from_firebase('database/Contact_Tracing.db',
                           '/home/pi/Fingerprint_Contact_Tracing/Contact_Tracing.db')

    messagebox.showinfo("LOGIN", "Place your finger on the fingerprint sensor")

    name, id = verify_fingerprint()

    if name is False:

        message = "Fingerprint not recognized, please try again"
        messagebox.showinfo("LOGIN", message)

    else:

        log_data(name)

        update_location(id, location)
        message = "WELCOME " + name + "!"
        messagebox.showinfo("LOGIN", message)


def clear():
    # clear the content of text entry box
    name_field.delete(0, END)
    email_field.delete(0, END)
    address_field.delete(0, END)
    gender_field.delete(0, END)
    phone_field.delete(0, END)


# window and write to an excel file
def insert():
    global root_win

    # if user not fill any entry
    # then print "empty input"
    if (name_field.get() == "" or
        email_field.get() == "" or
        address_field.get() == "" or
        gender_field.get() == "" or
            phone_field.get() == ""):

        messagebox.showinfo("Error", "Incomplete Input", icon='warning')
        print("empty input")

    else:

        name = name_field.get()
        email = email_field.get()
        address = address_field.get()
        gender = gender_field.get()
        phone = phone_field.get()

        # register_window()

        # timer_window()

        MsgBox = messagebox.askquestion(
            'Verification', 'Is your personal information correct?', icon='warning')
        if MsgBox == 'yes':
            messagebox.showinfo("Registration Instruction",
                                "Place your finger on the fingerprint sensor (5 times)")

            # Enroll Fingerprint
            enroll_fingerprint()
            fingerprint = convertToBinaryData(
                "/home/pi/Fingerprint_Contact_Tracing/fingerprint_data.bin")

            insertdata(name, email, address, gender, phone,
                       location, datetime.datetime.now(), fingerprint)

            messagebox.showinfo("Registration Status",
                                "Registration Complete!")

            upload_to_firebase('database/Contact_Tracing.db',
                               '/home/pi/Fingerprint_Contact_Tracing/Contact_Tracing.db')

            name_field.focus_set()

            clear()


def login_finger_process():
    global root_win

    login_f()

    # Fingerprint Scanning here


if __name__ == "__main__":

    # create a GUI window
    root = Tk()

    # set the background colour of GUI window
    root.configure(background='#E3F6F5')

    # set the title of GUI window
    root.title("CONTACT TRACING")

    # set the configuration of GUI window
    win_w = 800
    win_h = 270
    win_x = 0
    win_y = 0
    win_geom = str(win_w) + "x" + str(win_h) + "+" + \
        str(win_x) + "+" + str(win_y)

    root.geometry(win_geom)
    root.attributes("-fullscreen", False)

    header_section = Frame(root, width=win_w, height=50, bg="#272343")
    header_section.place(x=0, y=0)

    title_head = "FINGERPRINT CONTACT TRACING SYSTEM"
    heading_l = Label(header_section, text=title_head,
                      fg="#FFFFFF", bg="#272343")
    Font_tuple = ("Modern", 20, "bold")

    heading_l.config(font=Font_tuple)
    heading_l.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Register Section
    register_section = Frame(
        root, width=win_w/2, height=win_h, bd=2, bg="#E3F6F5")
    register_section.place(x=0, y=50)

    # Login Section
    login_section = Frame(root, width=win_w/2,
                          height=win_h-50, bd=2, bg="#E3F6F5")
    login_section.place(x=win_w/2, y=50)

    login = Button(login_section, text="LOGIN", fg="#272343",
                   bg="#BAE8E8", width=15, height=5, command=login_finger_process)

    myFont = font.Font(family='Modern', size=15, weight='bold')
    login['font'] = myFont

    login.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Create Labels

    name_l = Label(register_section, text="NAME", bg="#E3F6F5", fg="#272343")

    email_l = Label(register_section, text="EMAIL", bg="#E3F6F5", fg="#272343")

    address_l = Label(register_section, text="ADDRESS",
                      bg="#E3F6F5", fg="#272343")

    gender_l = Label(register_section, text="GENDER",
                     bg="#E3F6F5", fg="#272343")

    phone_l = Label(register_section, text="PHONE", bg="#E3F6F5", fg="#272343")

    # Position Labels

    name_l.place(x=10, y=15)
    email_l.place(x=10, y=45)
    address_l.place(x=10, y=75)
    gender_l.place(x=10, y=105)
    phone_l.place(x=10, y=135)

    # create a text entry box
    def handle_click(event):
        win_id = sp.getoutput("xdotool search --onlyvisible --name Keyboard")
        move_cmd = "xdotool windowmove {} 0 290".format(win_id)
        os.system(move_cmd)
        move_cmd = "xdotool windowraise {}".format(win_id)
        os.system(move_cmd)
        print(move_cmd)

    width_field = "36"
    name_field = Entry(register_section, width=width_field)

    email_field = Entry(register_section, width=width_field)
    address_field = Entry(register_section, width=width_field)

    n = StringVar()
    gender_field = ttk.Combobox(register_section, width="10", textvariable=n)

    # Adding combobox drop down list
    gender_field['values'] = ('Male',
                              'Female',
                              )

    # gender_field = Entry(register_section, width="46")
    phone_field = Entry(register_section, width=width_field)

    email_field.bind("<1>", handle_click)
    address_field.bind("<1>", handle_click)
    gender_field.bind("<1>", handle_click)
    phone_field.bind("<1>", handle_click)
    name_field.bind("<1>", handle_click)

    # Position Entry Box
    name_field.place(x=100, y=15)
    email_field.place(x=100, y=45)
    address_field.place(x=100, y=75)
    gender_field.place(x=100, y=105)
    phone_field.place(x=100, y=135)

    # create a Submit Button and place into the root window
    submit = Button(register_section, text="REGISTER", fg="#272343",
                    bg="#BAE8E8", width=25, height=1, command=insert)
    submit.place(x=10, y=165)
    myFont = font.Font(family='Modern', size=15, weight='bold')
    submit['font'] = myFont

    # Start Keyboard

    def d():
        time.sleep(3)
        os.system("matchbox-keyboard")
        time.sleep(3)
        print('s')

    d = threading.Thread(target=d)
    d.setDaemon(False)
    d.start()

    # start the GUI
    root.mainloop()
