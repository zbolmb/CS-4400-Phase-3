from tkinter import *
from tkinter import messagebox
import pymysql


class App:

    def __init__(self):
        self.reg = 0
        self.Years = ['Freshman', 'Sophomore', 'Junior', 'Senior']
        self.LoginPage()

    def LoginPage(self):
        if self.reg == 1:
            self.rootreg.destroy()
            self.rootreg = 0
        else:
            self.rootreg = 0

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
    # self.root.wm_title("CS 4400 Phase 3")
    def Register(self):
        self.rootWin.destroy()
        self.rootreg = Tk()
        self.rootreg.wm_title("New Student Registration")
        self.reg = 1
        Label(self.rootreg, text='Username').grid(row=1, column=0, sticky=W)
        Label(self.rootreg, text='Email').grid(row=2, column=0, sticky=W)
        Label(self.rootreg, text='Password').grid(row=3, column=0, sticky=W)
        Label(self.rootreg, text='Confirm Password').grid(
            row=4, column=0, sticky=W)

        self.eUser = Entry(self.rootreg)
        self.eUser.grid(row=1, column=1)

        self.eEmail = Entry(self.rootreg)
        self.eEmail.grid(row=2, column=1)

        self.ePass = Entry(self.rootreg)
        self.ePass.grid(row=3, column=1)

        self.eCPass = Entry(self.rootreg)
        self.eCPass.grid(row=4, column=1)

        cancel = Button(self.rootreg, text='Cancel', command=self.LoginPage)
        cancel.grid(row=6, column=1, sticky=E)

        register = Button(self.rootreg, text='Register', command=self.RegisterNew)
        register.grid(row=6, column=2)

        self.rootreg.mainloop()

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
            self.root.destroy()
            self.LoginPage()

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
            getAdmin = "SELECT UserType FROM User WHERE Username = %s AND Password = %s"
            self.cursor.execute(getAdmin, (user, password))
            admin = self.cursor.fetchone()[0]
            self.rootWin.destroy()
            if admin == 1:
                self.AdminMainPage()
            else:
                self.MainPage()
        else:
            messagebox.showwarning(
                "Whoops!", "Either your username or password was entered incorrectly")

        self.cursor.close()

    def MainPage(self):
        self.root = Tk()
        self.root.wm_title("Main Page")
        self.cursor = self.db.cursor()
        self.Catnum = 1
        self.CategoriesSelected = []

        def addcatrow():
            if CatVar.get() != "Please Select" and not CatVar.get() in self.CategoriesSelected:
                categoryLabelText.set(categoryLabelText.get() + '\n' + CatVar.get())
                self.CategoriesSelected.append(CatVar.get())
                CatVar.set("Please Select")
        # row 1
        mePage = Button(self.root, text='Me', command=self.MePage)
        mePage.grid(row=1, column=0, sticky=W)
        Label(self.root, text='Main Page').grid(row=1, column=1, sticky=W)
        # row 2
        Label(self.root, text='Title').grid(row=2, column=0, sticky=W)
        self.eTitle = Entry(self.root)
        self.eTitle.grid(row=2, column=1)
        Label(self.root, text='Categories Selected:').grid(row=2, column=2, sticky=W)
        Label(self.root, text='Category').grid(row=3, column=2, sticky=E)
        CatVar = StringVar(self.root)
        CatVar.set("Please Select")
        CatDrop = OptionMenu(self.root, CatVar, *self.Categories)
        CatDrop.grid(row=3, column=3, padx=1, pady=1)
        AddCat = Button(self.root, text="Add Selected Category",
                        fg='blue', relief='flat', command=addcatrow)
        AddCat.grid(row=3, column=4)
        categoryLabelText = StringVar()
        categoryLabelText.set("")
        selectedCategoriesLabel = Label(self.root, textvariable=categoryLabelText, height=6)
        selectedCategoriesLabel.grid(row=2, column=3)
        Label(self.root, text='Designation').grid(row=3, column=0, sticky=W)
        Label(self.root, text='Major').grid(row=4, column=0, sticky=W)
        Label(self.root, text='Year').grid(row=5, column=0, sticky=W)
        DesVar = StringVar(self.root)
        DesVar.set("Please Select")
        MaVar = StringVar(self.root)
        MaVar.set("Please Select")
        YearVar = StringVar(self.root)
        YearVar.set("Please Select")
        YearOpt = ["Freshman", "Sophomore", "Junior", "Senior"]
        Designations = self.cursor.execute("SELECT DISTINCT Name FROM Designation")
        Designations = self.cursor.fetchall()
        Desarray = []
        for item in Designations:
            Desarray.append(item[0])
        Majors = self.cursor.execute("SELECT Name FROM Major")
        Majors = self.cursor.fetchall()
        majorArray = []
        for m in Majors:
            majorArray.append(m[0])
        DesDrop = OptionMenu(self.root, DesVar, *Desarray)
        DesDrop.grid(row=3, column=1, padx=1, pady=1)

        MajDrop = OptionMenu(self.root, MaVar, *majorArray)
        MajDrop.grid(row=4, column=1, padx=1, pady=1)

        YearDrop = OptionMenu(self.root, YearVar, *YearOpt)
        YearDrop.grid(row=5, column=1, padx=1, pady=1)

        ProjCorBo = StringVar(self.root)
        ProjCorBo.set("Both")
        ProjCorButtonOne = Radiobutton(
            self.root, text="Course", variable=ProjCorBo, value="Course").grid(row=5, column=3)
        ProjCorButtonTwo = Radiobutton(
            self.root, text="Project", variable=ProjCorBo, value="Project").grid(row=5, column=4)
        ProjCorButtonTwo = Radiobutton(
            self.root, text="Both", variable=ProjCorBo, value="Both").grid(row=5, column=5)

        AllCourse = self.cursor.execute("SELECT Name from Course")
        AllCourse = self.cursor.fetchall()
        Coursearr = []
        for item in AllCourse:
            Coursearr.append((item[0], 'Course'))
        AllCourse = Coursearr
        AllProj = self.cursor.execute("SELECT Name from Project")
        AllProj = self.cursor.fetchall()
        ProjArray = []
        for item in AllProj:
            ProjArray.append((item[0], "Project"))
        AllProj = ProjArray

        AllCourseProj = []
        for item in AllProj:
            AllCourseProj.append(item)
        for item in AllCourse:
            AllCourseProj.append(item)

        Label(self.root, text="").grid(row=7, column=0, sticky=W)

        rownum = 9
        frame = Frame(self.root, width=300, height=100)
        frame.grid(row=9, column=0, columnspan=4)
        innerframe = Frame(frame)
        vscrollbar = Scrollbar(frame, orient=VERTICAL)
        vscrollbar.pack(side=RIGHT, fill=Y)
        canvas = Canvas(frame, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        Label(innerframe, text="Name", bg='light gray', relief=RIDGE, width=65,
              anchor=W).grid(row=8, column=1, sticky=W + N + S, pady=2)
        Label(innerframe, text="Type", bg='light gray', relief=RIDGE, width=15,
              anchor=W).grid(row=8, column=4, sticky=W + N + S, pady=2)

        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        interior_id = canvas.create_window(0, 0, window=innerframe, anchor=NW)

        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (innerframe.winfo_reqwidth(), innerframe.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if innerframe.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=innerframe.winfo_reqwidth())

        innerframe.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if innerframe.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

        for item in AllCourseProj:
            NewestB = Button(innerframe, text=item[0], command=self.courseview,
                             anchor=W, relief=RIDGE, width=45, justify=LEFT, height=1)
            NewestB.grid(row=rownum, column=1, sticky=W + E + S + N, columnspan=3)
            Label(innerframe, text=item[1], relief=RIDGE, width=15, anchor=W, height=1).grid(
                row=rownum, ipady=2, column=4, sticky=W + E + S + N)
            rownum += 1

        innerframe.pack(side=LEFT)

        def ApplyFilter():
            print("To do")

        def ResetFilter():
            DesVar.set("Please Select")
            MaVar.set("Please Select")
            YearVar.set("Please Select")
            CatVar.set("Please Select")
            ProjCorBo.set("Both")
            self.CategoriesSelected.clear()
            categoryLabelText.set('')

        ApplyFil = Button(self.root, text="Apply Filter", command=ApplyFilter)
        ApplyFil.grid(row=6, column=5)
        ResetFil = Button(self.root, text="Reset Filter", command=ResetFilter)
        ResetFil.grid(row=6, column=6)

        self.root.mainloop()

    def courseview(self):
        print('do you plz')

    def MePage(self):
        self.cursor.close()
        self.root.destroy()
        self.root = Tk()
        self.root.wm_title("Me")
        mePage = Button(self.root, text='Edit Profile',
                        command=self.StudEdPro, width=30, height=4)
        mePage.grid(row=1, column=0, sticky=W + E)
        mePage = Button(self.root, text='View Application',
                        command=self.StuViewApp, width=30, height=4)
        mePage.grid(row=2, column=0, sticky=W + E)
        mePage = Button(self.root, text='Back', command=self.BacktoMainPage,
                        padx=5, pady=5, width=30, height=4)
        mePage.grid(row=3, column=0, sticky=W + E)

    def BacktoMainPage(self):
        self.root.destroy()
        self.MainPage()

    def StudEdPro(self):
        print("to do")

    def StuViewApp(self):
        print("to do")

    # AdminMainPage
    def AdminMainPage(self):
        self.root = Tk()
        self.root.wm_title("Admin Main Page")
        Label(self.root, text='Choose Functionality').grid(row=1, column=1, sticky=W)
        viewApps = Button(self.root, text='View Applications', command=self.ViewAppsPage)
        viewApps.grid(row=2, column=1)
        viewProjReport = Button(self.root, text='View Popular Project Reports', command=self.ViewProjReportPage)
        viewProjReport.grid(row=3, column=1)
        viewAppReport = Button(self.root, text='View Application Report', command=self.ViewAppReportPage)
        viewAppReport.grid(row=4, column=1)
        addProj = Button(self.root, text='Add a Project', command=self.AddProjPage)
        addProj.grid(row=5, column=1)
        addCourse = Button(self.root, text='Add a Course', command=self.AddCoursePage)
        addCourse.grid(row=6, column=1)

        logout = Button(self.root, text='Logout', command=self.Logout)
        logout.grid(row=7, column=2)

        self.root.mainloop()

    # Chris Lung
    def ViewAppsPage(self):
        self.root = Tk()
        self.root.wm_title("Applications")
        self.cursor = self.db.cursor()
        back = Button(self.root, text='Back', command=self.AdminMainPage)
        back.grid(row=3, column=1)
        accept = Button(self.root, text='Accept', command=self.accept)
        #reject = Button(self.root, text='Reject', command=self.reject)

        getCourse = "SELECT CName,Cnumber FROM Courses"
        self.cursor.execute(getCourse)
        course1 = self.cursor.fetchall()

        # grid layout?
        # make sure commands are there
        print(course1)
        print('TODO')

    def accept(self):
        print("accepted, to do")

        # Chris Lung
    def ViewAppsPage(self):
        self.root.destroy()
        self.root = Tk()
        self.root.wm_title("Applications")
        self.cursor = self.db.cursor()
        getApp = "SELECT Project_Name, Major, Year, Status FROM Apply,User WHERE Apply.Student_Name = User.Username"
        self.cursor.execute(getApp)
        app = self.cursor.fetchall()
        print(app)
        Label(self.root, text='Application').grid(row=0, column=1)
        Label(self.root, text='Project').grid(row=1, column=1)
        Label(self.root, text='Applicant Major').grid(row=1, column=2)
        Label(self.root, text='Applicant Year').grid(row=1, column=3)
        Label(self.root, text='Status').grid(row=1, column=4)

        scrollbar = Scrollbar(self.root)
        scrollbar.grid(column=5)

        v = IntVar(self.root)
        v.set = 0
        a = 5
        self.checkboxValues = dict()
        for each in app:
            self.checkboxValues[a] = Variable()
            self.checkboxValues[a].set(0)
            l = Checkbutton(self.root, variable=self.checkboxValues[a])
            l.grid(row=a, column=0)
            Label(text=each[0], relief=RIDGE, width=25).grid(row=a, column=1)
            Label(text=each[1], relief=RIDGE, width=25).grid(row=a, column=2)
            Label(text=each[2], relief=RIDGE, width=25).grid(row=a, column=3)
            Label(text=each[3], relief=RIDGE, width=25).grid(row=a, column=4)
            a = a + 1

        back = Button(self.root, text='Back', command=self.BacktoAdminPage)
        back.grid(row=a, column=0, sticky=S)

        accept = Button(self.root, text='Accept', command=self.accept)
        accept.grid(row=a, column=3)
        reject = Button(self.root, text='Reject', command=self.reject)
        reject.grid(row=a, column=4)

        print('TODO')

    def accept(self):
        # if radio button is selected, update status on DB to accepted using SQL
        # if v == each[0]:
        #     print("this will update")
        #     # update using SQL
        # print("accepted, to do")
        for rowNum, value in self.checkboxValues.items():
            print(str(rowNum) + ' ' + str(value.get()))

    def reject(self):
        print("rejected, to do")

    # Chris Lung
    def ViewProjReportPage(self):
        self.root.destroy()
        self.root = Tk()
        self.root.wm_title("Popular Project Report")
        self.cursor = self.db.cursor()

        Label(self.root, text="Popular Projects").grid(row=0, column=0, sticky=N)
        Label(self.root, text="Project").grid(row=1, column=0)
        Label(self.root, text="Number of Applicants").grid(row=1, column=1)

        getProjectName = "SELECT Name FROM Project"
        getInfo = "SELECT Project_name, Count('Student_Name') FROM Apply, Project WHERE Apply.Project_name = Project.name GROUP BY Project_name ORDER BY Count('Student_Name') DESC"
        # MAKE SURE SQL STATEMENT SORTS BY TOP PROJECT APPLICATIONS
        self.cursor.execute(getProjectName)
        projectName = self.cursor.fetchall()
        self.cursor.execute(getInfo)
        info = self.cursor.fetchall()

        textvar = "insert number of apps here"

        r = 2
        for each in info:
            Label(text=each[0], relief=RIDGE, width=25).grid(row=r, column=0)
            Label(text=each[1], relief=RIDGE, width=25).grid(row=r, column=1)
            #sb = Scrollbar(self.root,orient=VERTICAL)
            # sb.pack(side=LEFT,fill=Y)
            # sb.configure(command=lb.yview)
            # lb.configure(yscrollcommand=sb.set)
            r = r + 1

        back = Button(self.root, text='Back', command=self.BacktoAdminPage)
        back.grid(row=r, column=0, sticky=S)

        print('TODO: CONNECT TO APPS, SORT BY TOP 10 APPS, SCROLLBAR')

    def BacktoAdminPage(self):
        self.root.destroy()
        self.AdminMainPage()

    # Chris Lung
    def ViewAppReportPage(self):
        self.root.destroy()
        self.root = Tk()
        self.root.wm_title("Application Report")

        getAppReport = "SELECT Project_Name, Major, Year, Status FROM Apply,User WHERE Apply.Student_Name = User.Username"
        # project, number of applicants, accept rate, top 3 major
        self.cursor.execute(getAppReport)
        appReport = self.cursor.fetchall()
        print(appReport)
        Label(self.root, text='Application Report').grid(row=0, column=1)
        Label(self.root, text='Project').grid(row=1, column=1)
        Label(self.root, text='# of Applicants').grid(row=1, column=2)
        Label(self.root, text='Accept Rate').grid(row=1, column=3)
        Label(self.root, text='Top 3 Major').grid(row=1, column=4)

        a = 5
        for each in appReport:
            Label(text=each[0], relief=RIDGE, width=25).grid(row=a, column=1)
            Label(text=each[1], relief=RIDGE, width=25).grid(row=a, column=2)
            Label(text=each[2], relief=RIDGE, width=25).grid(row=a, column=3)
            Label(text=each[3], relief=RIDGE, width=25).grid(row=a, column=4)
            a = a + 1

        back = Button(self.root, text='Back', command=self.BacktoAdminPage)
        back.grid(row=a, column=0, sticky=S)
        print('TODO')

    def AddProjPage(self):
        self.root.destroy()
        self.root = Tk()
        self.root.wm_title("Add Project Page")

        Label(self.root, text="Add a Project").grid(row=1, column=1, sticky=W + E)
        # row 2
        Label(self.root, text="Project Name:").grid(row=2, column=0)
        self.projName = Entry(self.root)
        self.projName.grid(row=2, column=1)
        # row 3
        Label(self.root, text="Advisor:").grid(row=3, column=0)
        self.advisorName = Entry(self.root)
        self.advisorName.grid(row=3, column=1)
        # row 4
        Label(self.root, text="Advisor Email:").grid(row=4, column=0)
        self.advisorEmail = Entry(self.root)
        self.advisorEmail.grid(row=4, column=1)
        # row 5
        Label(self.root, text="Description").grid(row=5, column=0)
        self.description = Text(self.root, height=10, width=25)
        self.description.grid(row=5, column=1)
        # row 6 the current selected categories

        self.CategoriesSelected = []

        def AddCat():
            if catVar.get() != "Please Select" and not catVar.get() in self.CategoriesSelected:
                categoryLabelText.set(categoryLabelText.get() + '\n' + catVar.get())
                self.CategoriesSelected.append(catVar.get())
                catVar.set("Please Select")

        def ClearCat():
            self.CategoriesSelected.clear()
            categoryLabelText.set("")

        def CheckSelected():
            showSelectedString = ''
            for c in self.CategoriesSelected:
                showSelectedString += c + '\n'
            messagebox.showinfo(showSelectedString)

        categoriesCaption = Label(self.root, text="Selected Categories:")
        categoriesCaption.grid(row=6, column=0)
        categoryLabelText = StringVar()
        categoryLabelText.set("")
        # checkSelectedCategories = Button(self.root, text='Check Selected', command=CheckSelected)
        # checkSelectedCategories.grid(row=6, column=1)
        selectedCategoriesLabel = Label(self.root, textvariable=categoryLabelText, height=5)
        selectedCategoriesLabel.grid(row=6, column=1)
        clearCat = Button(self.root, text="Clear Selected", command=ClearCat)
        clearCat.grid(row=6, column=2)
        # row 7
        catVar = StringVar(self.root)
        catVar.set("Please Select")
        Label(self.root, text="Category").grid(row=7, column=0)
        CatDrop = OptionMenu(self.root, catVar, *self.Categories)
        CatDrop.grid(row=7, column=1, padx=1, pady=1)

        addCat = Button(self.root, text='Add Category', command=AddCat)
        addCat.grid(row=7, column=2)

        # row 8
        self.desVar = StringVar(self.root)
        self.desVar.set("Please Select")
        desLabel = Label(self.root, text="Designation")
        desLabel.grid(row=8, column=0)
        DesDrop = OptionMenu(self.root, self.desVar, *self.Designations)
        DesDrop.grid(row=8, column=1, padx=1, pady=1)
        # row 9
        estStuLabel = Label(self.root, text="Estimated # of Students")
        estStuLabel.grid(row=9, column=0)
        self.estNumStu = Entry(self.root)
        self.estNumStu.grid(row=9, column=1)
        # row 10
        # gets the majors from the database
        getMajors = "SELECT Name FROM Major"
        self.cursor.execute(getMajors)
        majorsArrayTemp = self.cursor.fetchall()
        majorsArray = []
        for m in majorsArrayTemp:
            majorsArray.append(m[0])

        self.majVar = StringVar(self.root)
        self.majVar.set("Please Select")
        majorLabel = Label(self.root, text="Major Requirement")
        majorLabel.grid(row=10, column=0)
        MajDrop = OptionMenu(self.root, self.majVar, *majorsArray)
        MajDrop.grid(row=10, column=1, padx=1, pady=1)
        # row 11
        self.yearVar = StringVar(self.root)
        self.yearVar.set("Please Select")
        yearLabel = Label(self.root, text="Year Requirement")
        yearLabel.grid(row=11, column=0)
        YearDrop = OptionMenu(self.root, self.yearVar, *self.Years)
        YearDrop.grid(row=11, column=1, padx=1, pady=1)
        # row 11
        self.depVar = StringVar(self.root)
        self.depVar.set("Please Select")
        departmentLabel = Label(self.root, text="Department Requirement")
        departmentLabel.grid(row=12, column=0)
        DepDrop = OptionMenu(self.root, self.depVar, *self.Departments)
        DepDrop.grid(row=12, column=1, padx=1, pady=1)
        # row 12
        back = Button(self.root, text='Back', command=self.AdminMainPage)
        back.grid(row=13, column=0)
        submit = Button(self.root, text='Submit', command=self.SubmitProj)
        submit.grid(row=13, column=2)

        self.root.mainloop()

    def SubmitProj(self):
        self.Connect()

        projName = self.projName.get()
        advisorName = self.advisorName.get()
        advisorEmail = self.advisorEmail.get()
        description = self.description.get("1.0", END)
        designation = self.desVar.get()
        estNumStu = self.estNumStu.get()
        majorRequirement = self.majVar.get()
        yearRequirement = self.yearVar.get()
        depRequirement = self.depVar.get()

        # check all fields must be filled
        if projName == '' or advisorName == '' or advisorEmail == '' or description == '' or len(self.CategoriesSelected) == 0 or designation == '' or estNumStu == '':
            messagebox.showwarning("Error", "Not all fields are filled!")
            return
        if not self.isNum(estNumStu):
            messagebox.showwarning("Error", "Estimated Number Of Students must be a Number")
            return
        # check project name is unique
        projNameCheck = "SELECT Name FROM Project WHERE Name = %s"
        myProjNameCheck = self.cursor.execute(projNameCheck, (projName,))
        if myProjNameCheck >= 1:
            messagebox.showwarning("This Project Name is Taken")
        else:
            sql = 'INSERT INTO Project (Name, Advisor_Name, Advisor_Email, Description, Designation_Name, EstimatedNum) VALUES (%s, %s, %s, %s, %s, %s)'
            print(designation)
            self.cursor.execute(sql, (projName, advisorName, advisorEmail, description,
                                      designation, estNumStu))

            # inserting project categories
            sql = 'INSERT INTO Project_is_category (Project_Name, Category_Name) VALUES (%s, %s)'
            for c in self.CategoriesSelected:
                self.cursor.execute(sql, (projName, c))

            # inserting project requirements
            sql = 'INSERT INTO Project_requirements (Name, Requirement) VALUES (%s, %s)'
            if not majorRequirement == 'Please Select':
                self.cursor.execute(sql, (projName, majorRequirement))
            if not yearRequirement == 'Please Select':
                self.cursor.execute(sql, (projName, yearRequirement))
            if not depRequirement == 'Please Select':
                self.cursor.execute(sql, (projName, depRequirement))

            messagebox.showinfo("Congratulations!",
                                "You have successfully added a project!")
            self.db.commit()
            self.root.destroy()
            self.AdminMainPage()

        self.cursor.close()
        self.db.close()

    def AddCoursePage(self):
        self.root.destroy()
        self.root = Tk()
        self.root.wm_title("Add Course Page")

        Label(self.root, text="Add a Course").grid(row=1, column=1, sticky=W + E)

        Label(self.root, text="Course Number:").grid(row=2, column=0)
        self.eCourseNumber = Entry(self.root)
        self.eCourseNumber.grid(row=2, column=1)

        Label(self.root, text="Course Name:").grid(row=3, column=0)
        self.eCourseName = Entry(self.root)
        self.eCourseName.grid(row=3, column=1)

        Label(self.root, text="Instructor:").grid(row=4, column=0)
        self.eInstructorName = Entry(self.root)
        self.eInstructorName.grid(row=4, column=1)

        self.desVar = StringVar(self.root)
        self.desVar.set("Please Select")
        desLabel = Label(self.root, text="Designation:")
        desLabel.grid(row=5, column=0)
        DesDrop = OptionMenu(self.root, self.desVar, *self.Designations)
        DesDrop.grid(row=5, column=1, padx=1, pady=1)

        self.CategoriesSelected = []

        def AddCat():
            if catVar.get() != "Please Select" and not catVar.get() in self.CategoriesSelected:
                categoryLabelText.set(categoryLabelText.get() + '\n' + catVar.get())
                self.CategoriesSelected.append(catVar.get())
                catVar.set("Please Select")

        def ClearCat():
            self.CategoriesSelected.clear()
            categoryLabelText.set("")

        def CheckSelected():
            showSelectedString = ''
            for c in self.CategoriesSelected:
                showSelectedString += c + '\n'
            messagebox.showinfo(showSelectedString)

        categoriesCaption = Label(self.root, text="Selected Categories:")
        categoriesCaption.grid(row=6, column=0)
        categoryLabelText = StringVar()
        categoryLabelText.set("")
        # checkSelectedCategories = Button(self.root, text='Check Selected', command=CheckSelected)
        # checkSelectedCategories.grid(row=6, column=1)
        selectedCategoriesLabel = Label(self.root, textvariable=categoryLabelText, height=5)
        selectedCategoriesLabel.grid(row=6, column=1)
        clearCat = Button(self.root, text="Clear Selected", command=ClearCat)
        clearCat.grid(row=6, column=2)
        # row 7
        catVar = StringVar(self.root)
        catVar.set("Please Select")
        Label(self.root, text="Category").grid(row=7, column=0)
        CatDrop = OptionMenu(self.root, catVar, *self.Categories)
        CatDrop.grid(row=7, column=1, padx=1, pady=1)

        addCat = Button(self.root, text='Add Category', command=AddCat)
        addCat.grid(row=7, column=2)

        estStuLabel = Label(self.root, text="Estimated # of Students")
        estStuLabel.grid(row=8, column=0)
        self.estNumStu = Entry(self.root)
        self.estNumStu.grid(row=8, column=1)

        back = Button(self.root, text='Back', command=self.AdminMainPage)
        back.grid(row=13, column=0)
        submit = Button(self.root, text='Submit', command=self.SubmitCourse)
        submit.grid(row=13, column=2)

        self.root.mainloop()

    def SubmitCourse(self):
        self.Connect()

        courseNumber = self.eCourseNumber.get()
        courseName = self.eCourseName.get()
        instructor = self.eInstructorName.get()
        designation = self.desVar.get()
        estNumStu = self.estNumStu.get()

        # check all fields must be filled
        if courseNumber == '' or courseName == '' or instructor == '' or designation == '' or len(self.CategoriesSelected) == 0 or estNumStu == '':
            messagebox.showwarning("Error", "Not all fields are filled!")
            return
        if not self.isNum(estNumStu):
            messagebox.showwarning("Error", "Estimated Number Of Students must be a Number")
            return
        courseNameCheck = "SELECT Name FROM Course WHERE Name = %s"
        myCourseNameCheck = self.cursor.execute(courseNameCheck, (courseName,))
        if myCourseNameCheck >= 1:
            messagebox.showwarning("Error", "This Course Name is Taken")
            return
        else:
            sql = 'INSERT INTO Course (Name, Course_Number, Instructor, EstimatedNum, Designation_Name) VALUES (%s, %s, %s, %s, %s)'
            print(designation)
            self.cursor.execute(sql, (courseName, courseNumber, instructor, estNumStu, designation))

            # inserting course categories
            sql = 'INSERT INTO Course_is_category (Course_Name, Category_Name) VALUES (%s, %s)'
            for c in self.CategoriesSelected:
                self.cursor.execute(sql, (courseName, c))

            messagebox.showinfo("Congratulations!",
                                "You have successfully added a project!")
            self.db.commit()
            self.root.destroy()
            self.AdminMainPage()

        self.cursor.close()
        self.db.close()

    def Logout(self):
        print('TODO')

    def Connect(self):
        try:
            self.db = pymysql.connect(
                host='academic-mysql.cc.gatech.edu',
                user='cs4400_Team_38',
                passwd='PTtMisGK',
                db='cs4400_Team_38'
            )
            self.cursor = self.db.cursor()
            self.Categories = self.cursor.execute("SELECT Name FROM Category")
            self.Categories = self.cursor.fetchall()
            Catarray = []
            for c in self.Categories:
                Catarray.append(c[0])
            self.Categories = Catarray

            Departments = self.cursor.execute("SELECT DISTINCT Name FROM Department")
            Departments = self.cursor.fetchall()
            Deparray = []
            for d in Departments:
                Deparray.append(d[0])
            self.Departments = Deparray

            Designations = self.cursor.execute("SELECT DISTINCT Name FROM Designation")
            Designations = self.cursor.fetchall()
            Desarray = []
            for item in Designations:
                Desarray.append(item[0])
            self.Designations = Desarray

        except:
            messagebox.showwarning(
                "Whoops!", "Please check your internet connection")

    def isNum(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
App()
