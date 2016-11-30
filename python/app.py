from tkinter import *
from tkinter import messagebox
import pymysql


class App:

    def __init__(self):
        self.LoginPage()

    def LoginPage(self):
        self.rootWin = Tk()
        self.rootWin.wm_title("CS 4400 Phase 3")

        Label(self.rootWin, text='Username').grid(row=1, column=0, sticky=E)
        Label(self.rootWin, text='Password').grid(row=2, column=0, sticky=E)

        self.eUsername = Entry(self.rootWin)
        self.eUsername.grid(row=1, column=1)

        self.ePassword = Entry(self.rootWin)
        self.ePassword.grid(row=2, column=1)

        register = Button(self.rootWin, text='Register', command=self.Register)
        register.grid(row=3, column=1, sticky=E)

        login = Button(self.rootWin, text='Login', command=self.LoginCheck)
        login.grid(row=3, column=2)

        self.rootWin.mainloop()

    # To create a new window
    # self.rootWin.destroy()
    # self.root = Tk()
    def Register(self):
        self.rootWin.destroy()
        self.root = Tk()
        self.root.wm_title("CS 4400 Phase 3")

        Label(self.root, text='Username').grid(row=1, column=0, sticky=W)
        Label(self.root, text='Email').grid(row=2, column=0, sticky=W)
        Label(self.root, text='Password').grid(row=3, column=0, sticky=W)
        Label(self.root, text='Confirm Password').grid(
            row=4, column=0, sticky=W)

        self.eUser = Entry(self.root)
        self.eUser.grid(row=1, column=1)

        self.eEmail = Entry(self.root)
        self.eEmail.grid(row=2, column=1)

        self.ePass = Entry(self.root)
        self.ePass.grid(row=3, column=1)

        self.eCPass = Entry(self.root)
        self.eCPass.grid(row=4, column=1)

        # cancel = Button(self.root, text='Cancel', command=self.LoginPage)
        # cancel.grid(row=6, column=1, sticky=E)

        register = Button(self.root, text='Register', command=self.RegisterNew)
        register.grid(row=6, column=2)

        self.root.mainloop()

    def RegisterNew(self):

        self.Connect()

        user = self.eUser.get()
        email = self.eEmail.get()
        password = self.ePass.get()
        cPassword = self.eCPass.get()

        if user == '':
            messagebox.showwarning("Whoops!", "Please enter a username")
            return

        if email == '':
            messagebox.showwarning("Whoops!", "Please enter an Email")
            return

        if password == '' or cPassword == '':
            messagebox.showwarning(
                "Whoops!", "Please fill out the password forms")
            return

        if password != cPassword:
            messagebox.showwarning("Whoops!", "Make sure your passwords match")
            return

        userCheck = "SELECT Username FROM User WHERE Username = %s"
        myUserCheck = self.cursor.execute(userCheck, (user,))

        emailCheck = "SELECT Email FROM User WHERE Email = %s"
        myEmailCheck = self.cursor.execute(emailCheck, (email,))

        if myUserCheck >= 1:
            messagebox.showwarning(
                "Whoops!", "This username is already in use! Please choose another username.")
        elif myEmailCheck >= 1:
            messagebox.showwarning(
                "Whoops!", "This email is already in use! Please choose another email.")
        else:
            sql = 'INSERT INTO User (Username, Password, Email) VALUES (%s, %s, %s)'
            self.cursor.execute(sql, (user, password, email))
            messagebox.showinfo("Congratulations!",
                                "You have successfully registered!")
            self.db.commit()

        self.cursor.close()
        self.db.close()

    def LoginCheck(self):
        self.Connect()

        user = self.eUsername.get()
        password = self.ePassword.get()

        userCheck = "SELECT Username, Password FROM User WHERE Username = %s AND Password = %s"
        myUserCheck = self.cursor.execute(userCheck, (user, password))
        if myUserCheck == 1:
            messagebox.showinfo("Hello", "Welcome to The Database")
            self.rootWin.destroy()
            self.ChatPage()
        else:
            messagebox.showwarning(
                "Whoops!", "Either your username or password was entered incorrectly")

        self.cursor.close()

    def Connect(self):
        try:
            self.db = pymysql.connect(
                host='academic-mysql.cc.gatech.edu',
                user='cs4400_Team_38',
                passwd='PTtMisGK',
                db='cs4400_Team_38'
            )
            self.cursor = self.db.cursor()
        except:
            messagebox.showwarning(
                "Whoops!", "Please check your internet connection")
App()
