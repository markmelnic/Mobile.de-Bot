
from backup_module import *
from search_module import *
from checker_module import *
from remover_module import *

import os
import csv
import operator
import webbrowser
import threading as th

from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkfont

global maindir
maindir = os.getcwd()

class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.title("Mobile.de Bot")
        self.iconbitmap('./resources/icon.ico')

        # read settings
        with open('./resources/settings.txt', mode='r') as st:
            settings = st.readlines()
            st.close()
            
        window_show = int(settings[1])
        win_size = str(settings[3].strip("\n"))
        win_resizeability = int(settings[5])
        
        # change settings
        #self.geometry(win_size)
        if win_resizeability == 0:
            self.resizable(0, 0)
    
        '''
        # tk options
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family='Montserrat')
        self.configure(bg='#fff')
        '''
        
        self._frame = None
        self.switch_frame(SearchPage)
            
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

        
def navMenu(self, master, nr):
    navmenu = Frame(self)
    navmenu.config(height = 50, width = 600)
    navmenu.grid(row = 0, column = 0,sticky="new")
    
    
    navf = tkfont.Font(family='Montserrat' ,size=16 ,weight="bold")
    # nav search button
    searchIcon = PhotoImage(file="./resources/icons/search.png")
    searchIcon = searchIcon.subsample(8,8) 
    navSearchButton = Button(navmenu, image = searchIcon, text = 'Search', compound = LEFT, bg='#fff',command=lambda: master.switch_frame(SearchPage))
    if nr == 1:
        navSearchButton.config(relief=SUNKEN)
    navSearchButton['font'] = navf
    navSearchButton.image = searchIcon
    navSearchButton.grid(row=10, column=10)
    navSearchButton.config(width=150, height=50)
    
    # nav track button
    trackIcon = PhotoImage(file="./resources/icons/radar.png")
    trackIcon = trackIcon.subsample(8,8) 
    navTrackButton = Button(navmenu, image = trackIcon, text = 'Track', compound = LEFT, bg='#fff',command=lambda: master.switch_frame(TrackPage))
    if nr == 2:
        navTrackButton.config(relief=SUNKEN)
    navTrackButton['font'] = navf
    navTrackButton.image = trackIcon
    navTrackButton.grid(row=10, column=20)
    navTrackButton.config(width=150, height=50)
    
    # nav favorites button
    favoIcon = PhotoImage(file="./resources/icons/favorites.png")
    favoIcon = favoIcon.subsample(6,6) 
    navFavoButton = Button(navmenu, image = favoIcon, text = 'Favorites', compound = LEFT, bg='#fff')
    navFavoButton['font'] = navf
    navFavoButton.image = favoIcon
    navFavoButton.grid(row=10, column=30)
    navFavoButton.config(width=150, height=50)
    
    # nav settings button
    settingsIcon = PhotoImage(file="./resources/icons/settings.png")
    settingsIcon = settingsIcon.subsample(8,8) 
    navSettingsButton = Button(navmenu, image = settingsIcon, text = 'Settings', compound = LEFT, bg='#fff')
    navSettingsButton['font'] = navf
    navSettingsButton.image = settingsIcon
    navSettingsButton.grid(row=10, column= 40)
    navSettingsButton.config(width=150, height=50)
    
        
class SearchPage(Frame):
        
    def __init__(self, master):
        Frame.__init__(self, master)
        
        def retrieve_inputs():
            srcInput = []
            srcInput.append(makeField.get())
            srcInput.append(modelField.get())
            srcInput.append(fieldpriceTxtFrom.get())
            srcInput.append(fieldpriceTxtTo.get())
            srcInput.append(fieldregTxtFrom.get())
            srcInput.append(fieldregTxtTo.get())
            srcInput.append(fieldmileageTxtFrom.get())
            srcInput.append(fieldmileageTxtTo.get())
            srcInput.append(fieldpowerTxtFrom.get())
            srcInput.append(fieldpowerTxtTo.get())

            threads = []
            srchThread = th.Thread(target=search, args = (maindir, srcInput))
            srchThread.start()
        
        nr = 1
        navMenu(self, master, nr)
    # ========== MAIN CONTENT
        titlef = tkfont.Font(family='Montserrat' ,size=16)
        labelf = tkfont.Font(family='Montserrat' ,size=12)
        
        mainc = ttk.Frame(self)
        mainc.config(width = 600, height = 700)
        mainc.grid(row = 20, column = 0,sticky="new")
        
        title = ttk.Label(mainc, text = "Index a new search")
        title.grid(row = 10, column = 10, columnspan = 40,padx=(10,10), pady=(5,5))
        title['font'] = titlef
        
        '''
        # Vehicle type radio button
        vehTypeTxt = ttk.Label(mainc, text="Vehicle types:",justify = RIGHT)
        vehTypeTxt['font'] = labelf
        vehTypeTxt.grid(row=20,column=50,padx=(10,10), pady=(5,5), sticky = 'e')
        
        vehs = ["Sedan", "SUV","Estate car","Coupe/Sports car","Cabriolet/Roadster","Small/City Car"]
        images = [PhotoImage(file="./resources/vehicles/sedan.png"),PhotoImage(file="./resources/vehicles/suv.png")]
        
        cbs = [1,2,3,4,5,6]
        for i in range(len(vehs)):
            cbs[i] = Checkbutton(mainc,text = vehs[i], image = images[i],indicatoron=False,onvalue=1, offvalue=0,compound='right',bg='#fff')
            cbs[i].image = images[i]
            cbs[i]['font'] = titlef
            cbs[i].grid(row=(30+i*10),column=50, padx=5,pady=5) 
        '''
        
        # manufacturer
        makeTxt = ttk.Label(mainc, text="Car manufacturer:")
        makeTxt['font'] = labelf
        makeTxt.grid(row=20,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        makeField = ttk.Entry(mainc)
        makeField.grid(row=20,column=20)
        

        # model
        modelTxt = ttk.Label(mainc, text="Car model:")
        modelTxt['font'] = labelf
        modelTxt.grid(row=30,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        modelField = ttk.Entry(mainc)
        modelField.grid(row=30,column=20)


        # price
        priceTxt = ttk.Label(mainc, text="Price range (EURO):")
        priceTxt['font'] = labelf
        priceTxt.grid(row=40,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        # from
        fieldpriceTxtFrom = ttk.Entry(mainc)
        fieldpriceTxtFrom.grid(row=40,column=20)
        #to
        priceTxtTo = ttk.Label(mainc, text="to")
        priceTxtTo['font'] = labelf
        priceTxtTo.grid(row=40,column=30,padx=(10,10), pady=(5,5))
        fieldpriceTxtTo = ttk.Entry(mainc)
        fieldpriceTxtTo.grid(row=40,column=40)
        
        
        # mileage
        mileageTxt = ttk.Label(mainc, text="Mileage range (KM):")
        mileageTxt['font'] = labelf
        mileageTxt.grid(row=50,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        # from
        fieldmileageTxtFrom = ttk.Entry(mainc)
        fieldmileageTxtFrom.grid(row=50,column=20)
        #to
        mileageTxtTo = ttk.Label(mainc, text="to")
        mileageTxtTo['font'] = labelf
        mileageTxtTo.grid(row=50,column=30,padx=(10,10), pady=(5,5))
        fieldmileageTxtTo = ttk.Entry(mainc)
        fieldmileageTxtTo.grid(row=50,column=40)
        
        
        # registration
        regTxt = ttk.Label(mainc, text="Registration years:")
        regTxt['font'] = labelf
        regTxt.grid(row=60,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        # from
        fieldregTxtFrom = ttk.Entry(mainc)
        fieldregTxtFrom.grid(row=60,column=20)
        #to
        regTxtTo = ttk.Label(mainc, text="to")
        regTxtTo['font'] = labelf
        regTxtTo.grid(row=60,column=30,padx=(10,10), pady=(5,5))
        fieldregTxtTo = ttk.Entry(mainc)
        fieldregTxtTo.grid(row=60,column=40)
        
        
        # engine power
        powerTxt = ttk.Label(mainc, text="Engine power (HP):")
        powerTxt['font'] = labelf
        powerTxt.grid(row=70,column=10,padx=(10,10), pady=(5,5), sticky = 'w')
        # from
        fieldpowerTxtFrom = ttk.Entry(mainc)
        fieldpowerTxtFrom.grid(row=70,column=20)
        #to
        powerTxtTo = ttk.Label(mainc, text="to")
        powerTxtTo['font'] = labelf
        powerTxtTo.grid(row=70,column=30,padx=(10,10), pady=(5,5))
        fieldpowerTxtTo = ttk.Entry(mainc)
        fieldpowerTxtTo.grid(row=70,column=40)
        
        
        # search button
        srcButton = Button(mainc, text="Search!",bg='#5e5e5e', fg='#eae8e8', command=retrieve_inputs)
        srcButton.grid(row=80,column=10,columnspan=40,padx=(10, 10),pady=(10, 10))
        srcButton['font'] = titlef

        
class TrackPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        nr = 2
        navMenu(self, master, nr)  
        
        def chck():
            chckerThread = th.Thread(target=checker, args=(maindir,))
            chckerThread.start()
            threads = []
            threads.append(chckerThread)
            threadsThread = th.Thread(target=chckThread, args = (threads[0],))
            threadsThread.start()
            
        def chckThread(thread):
                thread.join()
                printTable()
                master.switch_frame(TrackPage)
            
        def printTable():
            os.chdir(maindir)
            os.chdir("./csv files")
            with open("changesTemp.csv", mode="r", newline='') as changesFile:
                changesReader = csv.reader(changesFile)
                changes = list(changesReader)
                changesFile.close()
            print(changes)
            for i in range(len(changes)):
                col = "column"+str(i)
                if int(changes[i][0]) > 0:
                    pr = "+" + str(changes[i][0])
                else:
                    pr = changes[i][0]
                changesTree.insert('', 'end', text=changes[i][0], values=(changes[i][2], changes[i][3], changes[i][4], changes[i][5], changes[i][6], changes[i][1]))
            os.chdir(maindir)
            
            
    # ========== MAIN CONTENT

        # styles
        titlef = tkfont.Font(family='Montserrat' ,size=16, weight = "bold")
        labelf = tkfont.Font(family='Montserrat' ,size=12)
        
        ntbkStyle = ttk.Style()
        ntbkStyle.configure('TNotebook.Tab', font=('Montserrat','11','bold'), padding=(10, 3, 10, 2))

        # main content frame
        mainc = ttk.Frame(self)
        mainc.config(width = 600, height = 700)
        mainc.grid(row = 20, column = 0,sticky="new",pady=5)
        
        
        #verify icon
        trVerifyIcon = PhotoImage(file="./resources/icons/verify.png")
        trVerifyIcon = trVerifyIcon.subsample(6,6) 
        trVerifyButton = Button(mainc, image = trVerifyIcon,compound = LEFT, bg='#fff', command = chck)
        trVerifyButton.image = trVerifyIcon
        trVerifyButton.grid(row=11, column=20,padx=10)
        trVerifyButton.config(width=50, height=50)
        
        
        # browse button
        def printSelected():
            trees = [changesTree]
            for tree in adsTrees:
                trees.append(tree)
                
            for tree in trees:
                selectedItem = tuple(tree.selection())
                for item in selectedItem:
                    item = tree.item(item)
                    try:
                        link = item['values'][5]
                        webbrowser.open(link)
                    except:
                        None
            master.switch_frame(TrackPage)
                
        trBrowseIcon = PhotoImage(file="./resources/icons/browse.png")
        trBrowseIcon = trBrowseIcon.subsample(6,6) 
        trBrowseButton = Button(mainc, image = trBrowseIcon,compound = LEFT, bg='#fff',command = printSelected)
        trBrowseButton.image = trBrowseIcon
        trBrowseButton.grid(row=12, column=20,padx=10)
        trBrowseButton.config(width=50, height=50)
        
        
        # add to favorites button
        trAddtofavIcon = PhotoImage(file="./resources/icons/add_to_favorites.png")
        trAddtofavIcon = trAddtofavIcon.subsample(6,6) 
        trAddtofavButton = Button(mainc, image = trAddtofavIcon,compound = LEFT, bg='#fff')
        trAddtofavButton.image = trAddtofavIcon
        trAddtofavButton.grid(row=13, column=20,padx=10)
        trAddtofavButton.config(width=50, height=50)


        # remove function
        def removeFile():
            file_to_remove = files[notebk.index("current")]
            remover(maindir, file_to_remove)
            master.switch_frame(TrackPage)
        # remove button 
        trRmIcon = PhotoImage(file="./resources/icons/remove.png")
        trRmIcon = trRmIcon.subsample(6,6) 
        trRmButton = Button(mainc, image = trRmIcon,compound = LEFT, bg='#fff', command=removeFile)
        trRmButton.image = trRmIcon
        trRmButton.grid(row=29, column=20,padx=10)
        trRmButton.config(width=50, height=50)
        
    # ========== NOTEBOOK
        # get all files in './csv files'
        with os.scandir("./csv files") as entries:
            files = []
            for entry in entries:
                if entry.is_file():
                    if str(entry) != "<DirEntry 'changesTemp.csv'>":
                        if str(entry) != "<DirEntry 'changesTimestamp.txt'>":
                            files.append(entry.name)
           
        tabs = []   
        adsTrees = []  
        for i in range(len(files)):    
            tabs.append(i)
            adsTrees.append(i)
        
        # create the notebook
        notebk = ttk.Notebook(mainc,width=540, height=425)
        notebk.grid(row=10,column=10,rowspan=20)
        for i in range(len(tabs)):
            tabs[i] = ttk.Frame(notebk, width = 400, height = 400, relief = SUNKEN)
            title = files[i].split("_")
            title = (title[0] + " " + title[1].replace("-", " ")).upper()
            notebk.add(tabs[i], text = title)
            
            # get content in csv file
            os.chdir("./csv files")
            with open(files[i], mode="r", newline='') as csvFile:
                csvReader = csv.reader(csvFile)
                data = sorted(csvReader, reverse=True, key = operator.itemgetter(6))
                data.pop(0)
                csvFile.close()
            os.chdir(maindir)
            
            # generate treeview
            adsTrees[i] = ttk.Treeview(tabs[i], height=20)
            adsTrees[i]["columns"]=("Registration","Price","Mileage","Power","Score")
            adsTrees[i].column("#0", width=280, minwidth=140,anchor=W)
            adsTrees[i].column("#2", width=60, minwidth=60,anchor=CENTER)
            adsTrees[i].column("#1", width=40, minwidth=40,anchor=CENTER)
            adsTrees[i].column("#3", width=70, minwidth=70,anchor=CENTER)
            adsTrees[i].column("#4", width=45, minwidth=45,anchor=CENTER)
            adsTrees[i].column("#5", width=45, minwidth=45,anchor=CENTER)
            
            adsTrees[i].heading("#0",text="Title", anchor=CENTER)
            adsTrees[i].heading("#1", text="Year", anchor=CENTER)
            adsTrees[i].heading("#2", text="Price", anchor=CENTER)
            adsTrees[i].heading("#3", text="Mileage", anchor=CENTER)
            adsTrees[i].heading("#4", text="Power", anchor=CENTER)
            adsTrees[i].heading("#5", text="Score", anchor=CENTER)
            
            adsTrees[i].grid(row=0,column=0, columnspan=2,rowspan=10)
            
            # insert data
            sortedData = sorted(data)
            for d in data:
                adsTrees[i].insert('', 'end', text=d[1], values=(d[2],d[3],d[4],d[5],d[6],d[0]))
                
    # =========== CHANGES TREE

        # changes title
        os.chdir("./csv files")
        with open("changesTimestamp.txt", mode="r") as timestampFile:
            timetxt = timestampFile.read() 
            timestampFile.close()
        os.chdir(maindir)
        chl = Label(mainc, text="Changes since " + timetxt)
        chl['font'] = titlef
        chl.grid(row=32,column=10,padx=5)
        
        # generate treeview
        changesTree = ttk.Treeview(mainc, height=5)
        changesTree["columns"]=("Title","Registration","Price","Mileage","Power")
        changesTree.column("#0", width=80, minwidth=70,anchor=W)
        changesTree.column("#1", width=210, minwidth=60,anchor=CENTER)
        changesTree.column("#2", width=65, minwidth=40,anchor=CENTER)
        changesTree.column("#3", width=55, minwidth=70,anchor=CENTER)
        changesTree.column("#4", width=70, minwidth=45,anchor=CENTER)
        changesTree.column("#5", width=60, minwidth=45,anchor=CENTER)
        
        changesTree.heading("#0", text="Value", anchor=CENTER)
        changesTree.heading("#1",text="Title", anchor=CENTER)
        changesTree.heading("#2", text="Year", anchor=CENTER)
        changesTree.heading("#3", text="Price", anchor=CENTER)
        changesTree.heading("#4", text="Mileage", anchor=CENTER)
        changesTree.heading("#5", text="Power", anchor=CENTER)
        
        changesTree.grid(row=40,column=10)
        
        os.chdir("./csv files")
        with open("changesTemp.csv", mode="r", newline='') as changesFile:
            changesReader = csv.reader(changesFile)
            changes = list(changesReader)
            changesFile.close()
        os.chdir(maindir)
        for i in range(len(changes)):
            changesTree.insert('', 'end', text=changes[i][0], values=(changes[i][2], changes[i][3], changes[i][4], changes[i][5], changes[i][6], changes[i][1]))

        
'''
        # feedback text
        class Feedback:
            def working():
                global workingText
                workingText = Label(text="Working, please wait...",background ="yellow",font=("Helvetica", 16))
                workingText.grid(row=16,column=0,columnspan=2,padx=(10, 10),pady=(10, 10))

            def successful():
                try:
                    workingText.grid_remove()
                except:
                    None
                    
                global successfulText
                try:
                    successfulText.grid_remove()
                except:
                    None
                    
                successfulText = Label(text="Execution Successful",background ="light green",font=("Helvetica", 16))
                successfulText.grid(row=16,column=0,columnspan=2,padx=(10, 10),pady=(10, 10))
                time.sleep(10)
                successfulText.grid_remove()

        class Backup:
        
            def backupthread():
                backup(maindir)
                Feedback.successful()

            def bck():
                bckupThread = th.Thread(target=Backup.backupthread)
                bckupThread.start()

            # backup button
            backupText = Label(text="Backup existing searches")
            backupText.grid(row=0,column=2,columnspan=2,padx=(10, 10),pady=(10, 10))
            backupText['font'] = font.Font(family='Helvetica')
            backupText['font'] = font.Font(size=15)

            backupButton = Button(self, text="Backup", command=bck)
            backupButton.grid(row=1,column=2,columnspan=2,padx=(10, 10),pady=(5, 0))
'''