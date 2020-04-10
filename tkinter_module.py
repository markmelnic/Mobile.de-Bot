
from backup_module import *
from search_module import *
from checker_module import *
from remover_module import *

import os
import threading as th
from tkinter import *
from tkinter.ttk import *
import tkinter.font as font


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
            window_show = int(settings[1])
            st.close()
            win_size = str(settings[3].strip("\n"))
            win_resizeability = str(settings[5])

        # change settings
        self.geometry(win_size)
        if win_resizeability == 0:
            self.resizable(False, False)

        # progress bar
        '''
        class progressBar:
            progressbar = Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
            progressbar.place(x=0, y=700, width=1280)
            progressbar.start()
        '''

        # feedback text
        class Feedback:
            def working():
                global workingText
                workingText = Label(text="Working, please wait...",background ="yellow",font=("Helvetica", 16))
                workingText.grid(row=16,column=0,columnspan=2,padx=(10, 10),pady=(10, 10))

            def successful():
                workingText.grid_remove()
                global successfulText
                successfulText = Label(text="Search Successful",background ="light green",font=("Helvetica", 16))
                successfulText.grid(row=16,column=0,columnspan=2,padx=(10, 10),pady=(10, 10))
                time.sleep(10)
                successfulText.grid_remove()

        # search
        class Search:
            def threadder(searchWorkingText, thread):
                thread.join()
                tree = Remover.tree
                Remover.filesList(tree)
                Feedback.successful()


            def retrieve_inputs():
                srcInput = []
                srcInput.append(Search.makeField.get())
                srcInput.append(Search.modelField.get())
                srcInput.append(Search.fieldpriceTxtFrom.get())
                srcInput.append(Search.fieldpriceTxtTo.get())
                srcInput.append(Search.fieldregTxtFrom.get())
                srcInput.append(Search.fieldregTxtTo.get())
                srcInput.append(Search.fieldmileageTxtFrom.get())
                srcInput.append(Search.fieldmileageTxtTo.get())
                srcInput.append(Search.fieldpowerTxtFrom.get())
                srcInput.append(Search.fieldpowerTxtTo.get())

                threads = []
                srchThread = th.Thread(target=search, args = (maindir, srcInput))
                srchThread.start()

                Feedback.working()

                threads.append(srchThread)
                threadsThread = th.Thread(target=Search.threadder, args = (searchWorkingText, threads[0],))
                threadsThread.start()

            # search button
            srcButton = Button(self, text="Search",command=retrieve_inputs)
            srcButton.grid(row=15,column=0,columnspan = 2,padx=(10, 10),pady=(5, 0))

            srcText = Label(text="Create a new search")
            srcText.grid(row=0,column=0,columnspan = 2,padx=(10, 10),pady=(10, 10))
            srcText['font'] = font.Font(family='Helvetica')
            srcText['font'] = font.Font(size=15)


            # manufacturer
            makeTxt = Label(text="Car manufacturer")
            makeTxt.grid(row=1,column=0,padx=(10, 10),pady=(10, 10))
            makeField = Entry()
            makeField.grid(row=1,column=1,padx=(10, 10),pady=(10, 10))


            # model
            modelTxt = Label(text="Car model")
            modelTxt.grid(row=2,column=0,padx=(10, 10),pady=(10, 10))
            modelField = Entry()
            modelField.grid(row=2,column=1,padx=(10, 10),pady=(10, 10))


            # price
            priceTxt = Label(text="Price range (EURO):")
            priceTxt.grid(row=3,column=0,padx=(10, 5),pady=(10, 10))
            # from
            priceTxtFrom = Label(text="From")
            priceTxtFrom.grid(row=4,column=0,padx=(10, 5))
            fieldpriceTxtFrom = Entry()
            fieldpriceTxtFrom.grid(row=4,column=1,padx=(5, 5))
            #to
            priceTxtTo = Label(text="to")
            priceTxtTo.grid(row=5,column=0,padx=(5, 5))
            fieldpriceTxtTo = Entry()
            fieldpriceTxtTo.grid(row=5,column=1,padx=(5, 5))


            # reg
            regTxt = Label(text="Registration years range:")
            regTxt.grid(row=6,column=0,padx=(10, 5),pady=(10, 10))
            # from
            regTxtFrom = Label(text="From")
            regTxtFrom.grid(row=7,column=0,padx=(10, 5))
            fieldregTxtFrom = Entry()
            fieldregTxtFrom.grid(row=7,column=1,padx=(5, 5))
            #to
            regTxtTo = Label(text="to")
            regTxtTo.grid(row=8,column=0,padx=(5, 5))
            fieldregTxtTo = Entry()
            fieldregTxtTo.grid(row=8,column=1,padx=(5, 5))


            # mileage
            mileageTxt = Label(text="Mileage range (KM):")
            mileageTxt.grid(row=9,column=0,padx=(10, 5),pady=(10, 10))
            # from
            mileageTxtFrom = Label(text="From")
            mileageTxtFrom.grid(row=10,column=0,padx=(10, 5))
            fieldmileageTxtFrom = Entry()
            fieldmileageTxtFrom.grid(row=10,column=1,padx=(5, 5))
            #to
            mileageTxtTo = Label(text="to")
            mileageTxtTo.grid(row=11,column=0,padx=(5, 5))
            fieldmileageTxtTo = Entry()
            fieldmileageTxtTo.grid(row=11,column=1,padx=(5, 5))


            # power
            powerTxt = Label(text="Power range (HP):")
            powerTxt.grid(row=12,column=0,padx=(10, 5),pady=(10, 10))
            # from
            powerTxtFrom = Label(text="From")
            powerTxtFrom.grid(row=13,column=0,padx=(10, 5))
            fieldpowerTxtFrom = Entry()
            fieldpowerTxtFrom.grid(row=13,column=1,padx=(5, 5))
            #to
            powerTxtTo = Label(text="to")
            powerTxtTo.grid(row=14,column=0,padx=(5, 5))
            fieldpowerTxtTo = Entry()
            fieldpowerTxtTo.grid(row=14,column=1,padx=(5, 5))

        # check
        class Check:
            def chckThread():
                checker(maindir)

            def chck():
                chckerThread = th.Thread(target=Check.chckThread)
                chckerThread.start()

            # check button
            chckText = Label(text="Check existing files for changes")
            chckText.grid(row=0,column=2,columnspan=2,padx=(10, 10),pady=(10, 10))
            chckText['font'] = font.Font(family='Helvetica')
            chckText['font'] = font.Font(size=15)

            chckButton = Button(self, text="Check", command=chck)
            chckButton.grid(row=1,column=2,padx=(10, 10),pady=(5, 0))

        # remove
        class Remover:
            def rm():
                items_to_remove = tuple(Remover.tree.selection())
                print(items_to_remove)
                remover(maindir, items_to_remove)
                for item in items_to_remove:
                    Remover.tree.delete(item)

            def filesList(tree):
                try:
                    os.chdir(maindir)
                    files = []
                    with os.scandir("./csv files") as entries:
                        for entry in entries:
                            if entry.is_file():
                                files.append(entry.name)
                    for item in items_in_tree:
                        Remover.tree.delete(item)
                except:
                    None
                os.chdir(maindir)
                files = []
                with os.scandir("./csv files") as entries:
                    for entry in entries:
                        if entry.is_file():
                            files.append(entry.name)

                for i in range(len(files)):
                    try:
                        tree.insert('', 'end', files[i], text=files[i])
                    except:
                        None
                return tree

            tree = Treeview(show="tree")
            tree.grid(row=2,column=4, columnspan=2,rowspan=10)

            # remove button
            removeText = Label(text="Stop tracking a search")
            removeText.grid(row=0,column=4,columnspan=2,padx=(10, 10),pady=(10, 10))
            removeText['font'] = font.Font(family='Helvetica')
            removeText['font'] = font.Font(size=15)

            removeButton = Button(self, text="Remove", command=rm)
            removeButton.grid(row=1,column=4,padx=(10, 10),pady=(5, 0))

            tree = filesList(tree)

        # backup
        class Backup:
            def backupthread():
                backup(maindir)
                backupSuccessfulText = Label(text="Backup Successful",background ="light green",font=("Helvetica", 16))
                backupSuccessfulText.grid(row=2,column=6,padx=(10, 10),pady=(10, 10))
                time.sleep(10)
                backupSuccessfulText.grid_remove()

            def bck():
                bckupThread = th.Thread(target=Backup.backupthread)
                bckupThread.start()

            # backup button
            backupText = Label(text="Backup existing searches")
            backupText.grid(row=0,column=6,columnspan=2,padx=(10, 10),pady=(10, 10))
            backupText['font'] = font.Font(family='Helvetica')
            backupText['font'] = font.Font(size=15)

            backupButton = Button(self, text="Backup", command=bck)
            backupButton.grid(row=1,column=6,padx=(10, 10),pady=(5, 0))