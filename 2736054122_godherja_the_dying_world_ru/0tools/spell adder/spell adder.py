from tkinter import *
import spell_adder_classes as spellClasses

class MultiListBox(Frame):
    def __init__(self, master, lists, masterWindow, heightOfListbox: int):
        Frame.__init__(self, master)
        self.lists = []
        self._headerLabels = []
        for l,w in lists:
            frame = Frame(self); frame.pack(side=LEFT, expand=YES, fill=BOTH)
            currentHeader = Label(frame, text=l, borderwidth=1, relief=RAISED)
            self._headerLabels.append(currentHeader)
            currentHeader.pack(fill=X)
            lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                         relief=FLAT, exportselection=FALSE, height=heightOfListbox)
            lb.pack(expand=YES, fill=BOTH)
            self.lists.append(lb)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
            lb.bind('<MouseWheel>', lambda e, s=self: s._scrollParts(e.delta//120))
        frame = Frame(self); frame.pack(side=LEFT, fill=Y)
        Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
        sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        sb.bind('<MouseWheel>', lambda e, s=self: s._scrollParts(e.delta//120))
        self.lists[0]['yscrollcommand']=sb.set

        self.myMaster = masterWindow

    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, END)
        self.selection_set(row)
        return 'break'

    def _button2(self, x, y):
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        # print(args)
        for l in self.lists:
            l.yview_moveto(float(args[1]))

    def _scrollParts(self, diff: float):
        for l in self.lists:
            l.yview_scroll(diff, 'units')

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        if last is None:
            return tuple(thisList.get(first) for thisList in self.lists)
        else:
            return tuple((thisList.get(i) for thisList in self.lists) for i in range(first, last))

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i += 1

    def size(self):
        return self.lists[0].size(  )

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

        self.myMaster.reloadButtons()
        



# MAIN

class BaseWindow:

    def __init__(self):
        self.spells = spellClasses.spellList()
        self.settingsObj = spellClasses.Settings()
        self.setDefaultSort()
        
        self.loadBaseWindow()
        self.editWindow = None
        self.codeNameWindow = None
        
        self.window.mainloop()
        return

    def setDefaultSort(self):
        self.sortBy = 0 # default is asc in order of codename
        self.sortDesc = False
        return


    def loadBaseWindow(self):
        
        self.window = Tk()

        topBar = Frame(master=self.window, height=5)

        # eventually we want icons
        self.button_new = Button(topBar, text="new", command=self.newSpell)
        self.button_copy = Button(topBar, text="copy", command=self.copySpell)
        self.button_edit = Button(topBar, text="edit", command=self.editSpell)
        self.button_delete = Button(topBar, text="delete", command=self.deleteSpell)

        self.button_new.pack(side=LEFT, fill=Y)
        self.button_copy.pack(side=LEFT, fill=Y)
        self.button_edit.pack(side=LEFT, fill=Y)
        self.button_delete.pack(side=LEFT, fill=Y)
        topBar.pack(fill=X, side=TOP)

        bottomBar = Frame(master=self.window, height=5)
        Button(bottomBar, text="save", command=self.save).pack(side=RIGHT, fill=Y)
        Button(bottomBar, text="reload", command=self.reload).pack(side=RIGHT, fill=Y)
        Button(bottomBar, text="reload from disk", command=self.reloadFull).pack(side=RIGHT, fill=Y)
        bottomBar.pack(fill=X, side=BOTTOM)

        scrollBox = Frame(master=self.window)
        self.spellListGrid = self.loadSpellList(scrollBox)
        self.spellListGrid.pack(expand=True)
        
        scrollBox.pack(expand=True)

        self.reloadButtons()

        return

    def reloadFull(self):
        """reads files from disk and reloads everything"""
        self.spells = spellClasses.spellList()
        self.settingsObj = spellClasses.Settings()
        self.reload()
        self.setDefaultSort()
        return

    def setSortBy(self, sortingListIndex: int):
        print('loooool' + str(sortingListIndex))
        if self.sortBy == sortingListIndex:
            self.sortDesc = not self.sortDesc
        else:
            self.sortBy = sortingListIndex
        self.reload()
        return

    def reload(self):
        """reloads the spells from the spell list obj"""
        self.window.destroy()
        self.loadBaseWindow()
        return

    def loadSpell(self, editingSpell: spellClasses.Spell = None, entries: dict = None):
        """loads the options window up with the specified spell; the entries are filled with the spell if unspecified. Use an empty dictionary for empty entries."""

        print(entries)

        if entries is None:
            entries = editingSpell._getPublicAttributes()

        print(entries)
        
        self.editWindow = editSpellWindow(self, entries, editingSpell)
        return
    

    def loadSpellList(self, Master, spellTypesShown: set = ('living', 'dead', 'mixed', 'other', 'generation')): #, columnsShown: tuple
        spellBox = MultiListBox(
                Master,
                (('codename', 20), ('name', 20), ('base ai chance', 20), ('school', 15)),
                self,
                30
            )
        
        valuesList = [i.getShortValues() for i in self.spells.getSpells() if i.spellType in spellTypesShown]
        valuesList.sort(key=lambda x: x[self.sortBy], reverse=self.sortDesc)
        
        for i in valuesList:
            spellBox.insert(END, i)

        # click on the labels to sort the columns
        for index in range(len(spellBox._headerLabels)):
            spellBox._headerLabels[index].bind("<ButtonRelease>", lambda e, x=index: self.setSortBy(x))

        return spellBox

    def getSelectedSpell(self):
        return self.spells.getSpell(self.spellListGrid.get(self.spellListGrid.curselection()[0])[0])

    def _noOtherWindowOpen(self):
        return not (self.editWindow or self.codeNameWindow)

    def newSpell(self):
        if self._noOtherWindowOpen():
            self.codeNameWindow = defineCodenameWindow(self.spells.getCodeNames(), self)
        return

    def copySpell(self):
        if self._noOtherWindowOpen():
            self.codeNameWindow = defineCodenameWindow(self.spells.getCodeNames(), self, self.getSelectedSpell())
        return

    def editSpell(self):
        if self._noOtherWindowOpen():
            mySpell = self.getSelectedSpell()
            self.loadSpell(mySpell)
        return

    def deleteSpell(self):
        if self._noOtherWindowOpen():
            self.spells.deleteSpell(self.getSelectedSpell())
            self.reload()
        return

    def save(self):
        # confirmation box?
        self.spells.saveSpells()
        return

    def reloadButtons(self):
        # new is always allowed
        
        if self.spellListGrid.curselection == ():
            self.button_copy['state'] = DISABLED
            self.button_edit['state'] = DISABLED
            self.button_delete['state'] = DISABLED
        else:
            self.button_copy['state'] = NORMAL
            self.button_edit['state'] = NORMAL
            self.button_delete['state'] = NORMAL

        return
    

class defineCodenameWindow:

    def __init__(self, spellcodenames: iter, baseWindowInstance: BaseWindow, spellToCopy: spellClasses.Spell = None):
        self.baseWindowInstance = baseWindowInstance
        self.spellToCopy = spellToCopy
        self.spellcodenames = spellcodenames
        
        self.window = Tk()
        entryframe = Frame(self.window)
        Label(entryframe, text="enter code name here: ").pack(fill=X)
        self.entry_box = Entry(entryframe)
        self.entry_box.pack(fill=Y, side=LEFT)
        #warningSign = PhotoImage(entryFrame, file='warning_sign.png', visible='no')
        #warningSign.pack()
        entryframe.pack(expand=True)
        Button(self.window, command=self.copySpell, text='confirm').pack(side=RIGHT)
        Button(self.window, command=self.window.destroy, text='cancel').pack(side=RIGHT)
        self.window.mainloop()
        return

    def copySpell(self):
        entry = self.entry_box.get()

        # debugging
        #print(entry not in self.spellcodenames)
        #print(list(self.spellcodenames))
        #print(entry)

        stripped = entry.strip()

        # 'none' is banned because it causes problems with the ai file
        if stripped and stripped != 'none' and stripped not in self.spellcodenames:
            if self.spellToCopy: # are we copying or creating new?
                attrDict = self.spellToCopy._getPublicAttributes()
            else:
                attrDict = dict()
            attrDict['codename'] = entry
            self.window.destroy()
            self.baseWindowInstance.codeNameWindow = None
            self.baseWindowInstance.loadSpell(entries=attrDict) # we are not linking to any existing spell
        return

def labelAndEntryFrame(master: object, codeLabel: str, entryClass: callable, saveTo: dict, labelText: str = None, defaultText: str = None, height: int = None, width: int = None, padding: tuple = (0, 0)):
    if labelText is None:
        labelText = codeLabel + ':'
    if defaultText is None:
        # the following is inoperable :(((((
        defaultText = textDict[label] # from the caller - Python will check there too

    coolFrame = Frame(master)
    Label(coolFrame, text=labelText).pack()
    entryArgs = {'master': coolFrame}
    if height != None:
        entryArgs['height'] = height
    if width != None:
        entryArgs['width'] = width
    
    saveTo[codeLabel] = entryClass(**entryArgs) # left side is pass by reference
    saveTo[codeLabel].insert(END, defaultText)
    saveTo[codeLabel].pack()
    coolFrame.pack(padx = padding)
    return

class editSpellWindow:

    def __init__(self, baseWindow: BaseWindow, textDict: dict, spellRef: spellClasses.Spell = None):
        self.spellRef = spellRef
        self.currentCodeName = textDict['codename']
        
        self.baseWindow = baseWindow
        
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.quitMe) # if you click on X you can open a new window

        topBar = Frame(master=self.window, height=5)
        Label(topBar, text=self.currentCodeName).pack(fill=X) 
        topBar.pack(fill=X, side=TOP)

        bottomBar = Frame(master=self.window, height=5)
        Button(bottomBar, text='save', command=self.save).pack(side=RIGHT, fill=Y)
        Button(bottomBar, text='cancel', command=self.quitMe).pack(side=RIGHT, fill=Y)
        bottomBar.pack(fill=X, side=BOTTOM)

        self.entriesDict = dict()

        leftSide = Frame(self.window)


        leftEntryFrame = lambda label, frameType, labelText=None, height=None, width=None: labelAndEntryFrame(
            leftSide,
            label,
            frameType,
            self.entriesDict,
            labelText,
            spellClasses.returnIfPresent(textDict, label),
            height,
            width,
            (6, 4)
        )

        leftEntryFrame('name', Entry)
        leftEntryFrame('desc', Text, 'description:', 7)
        leftEntryFrame('cost', Text, None, 3, 30)
        leftEntryFrame('effect', Text, None, 30)

        
        rightSide = Frame(self.window)

        # copy and pasted from above, mostly
        rightEntryFrame = lambda label, frameType, labelText=None, height=None, width=None: labelAndEntryFrame(
            rightSide,
            label,
            frameType,
            self.entriesDict,
            labelText,
            spellClasses.returnIfPresent(textDict, label),
            height,
            width,
            (4, 6)
        )
        rightEntryFrame('is_shown_trigger', Text, "visibility trigger:", 5)
        rightEntryFrame('trigger', Text, None, 15)
        rightEntryFrame('trigger_desc', Text, "trigger description (optional):", 10)
        rightEntryFrame('ai_value_base', Entry, "base AI chance:")
        rightEntryFrame('ai_value', Text, "ai chance modifiers:", 13)

        # seems easier to do this one manually
        schoolFrame = Frame(rightSide)
        Label(schoolFrame, text='school:').pack()
        try:
            self.entriesDict['school'] = StringVar(schoolFrame, value=textDict['school'])
        except KeyError:
            self.entriesDict['school'] = StringVar(schoolFrame, value=next(iter(spellClasses.spellTypesDict.keys()))) # choose the first spell type as default
        OptionMenu(schoolFrame, self.entriesDict['school'], *spellClasses.spellTypesDict.keys()).pack()
        schoolFrame.pack()

        leftSide.pack(side=LEFT)
        rightSide.pack(side=RIGHT)

        return

    def save(self):
        #debug
        for key, value in self.entriesDict.items():
            print(key)
            print(value)
            print(value.get('1.0', 'end-1c') if isinstance(value, Text) else value.get())
            print('lol')
        #\debug
        partsDict = {key: value.get('1.0', 'end-1c') if isinstance(value, Text) else value.get() for key, value in self.entriesDict.items()}
        partsDict['codename'] = self.currentCodeName
        school = partsDict.pop('school')
        
        if self.spellRef:
            self.baseWindow.spells.editSpell(self.spellRef, partsDict, school)  
        else:
            self.baseWindow.spells.addSpell(spellClasses.genSpellObj(school, partsDict))

        self.baseWindow.reload()
    
        self.quitMe()
        return

    def quitMe(self): # quit is a system function
        self.window.destroy()
        self.baseWindow.editWindow = None
        return
    

class SettingsWindow:
    pass

class confirmQuit:
    userText = "Are you sure you want to quit? Any unsaved changes will be lost"

    def __init__(self, action: callable, title: str = "", yestext: str = "Confirm", arguments: tuple = ()):
        self.window = Tk()

        Label(self.window, text=title).pack()
        Label(self.window, text=userText, height=3).pack()

        Button(self.window, command=self.window.destroy, text="Cancel").pack(side=RIGHT, fill=Y)
        Button(self.window, command=self.yes, text=yestext).pack(side=RIGHT, fill=Y)

        self.action = action
        self.arguments = arguments

        return

    def yes(self):
        self.action(*self.arguments)

class confirmRefresh(confirmQuit):
    userText = "Are you sure you want to refresh the spells? Any unsaved changes will be lost"


spellClasses.resetLog()
if __name__ == '__main__':
    baseWindow = BaseWindow()
