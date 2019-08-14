"""
Environment: borchr27/stableenv

python version 3.7.3
pandas version 0.25.2
tk version 8.6.8
xlrd version 1.2.0

ABOUT --V8 2019
Program written by Borchr27 as a sub assembly tracker to allow an employee to type in a finished 
goods part number then return all the individual parts/part numbers within that assembly. 
Program uses tkinter to create a user interface. Also packaged the program into a nice little executable file.

CODE
The code uses Pandas to translate the excel file into a workable/searchable format.
The SEARCH function locates the initial part number in the excel file.
It then pulls all the sub assembly or final part numbers into two lists.
One list (fnpl, which stands for final part number list) is used to store base level part numbers that have no sub assemblies.
The next list (sub_asms) is carried thru the functions and holds part numbers that still have sub assemblies.
Next Steps: 

Example / Test Case / Uses Part Number Example Set File.xlsx
100-1049
32, 37, 40, 44, 45, 46
32, (31, 28), (1, 39), 44, 45, 46
31, 32, (4), 1, 39, 44, 45, 46
1, 1, 3, 31, 32, 39, 44, 45, 46
Finished Goods for PN 100-1049: ^
"""

version = '01.01.00'

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.messagebox import showinfo
import pandas as pd
import sys
import time


class App:
    def __init__(self, master):            
        # Window Setup
        master.geometry('650x600')
        #icon = 'UVALogo.ico' # with holding logo for now to make it easier to make .exe file
        #master.wm_iconbitmap(icon)
        master.resizable(True, True)
        master.title('Company Name - Part Number Lookup')

        self.status = ttk.Label(master, anchor='w', text=' Selct Company Name file ...', width=X, relief=SUNKEN, borderwidth=1)
        self.status.pack(side='bottom', fill=X)
        
        # Menu Bar Setup
        menu_bar = Menu(master)
        master.config(menu=menu_bar)
        sub_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=sub_menu)
        sub_menu.add_command(label='About', command=self.mb_About)
        sub_menu.add_command(label='Exit', command=master.destroy)
        
        # Frame 1 Content
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()
        
        # Labels, Entry, Buttons
        ttk.Label(self.frame_content, text = ' ').grid(row=1, column=0, sticky='w')
        ttk.Label(self.frame_content, text = 'File Selected: ').grid(row=2, column=0, sticky='w')
        ttk.Label(self.frame_content, text = ' ').grid(row=3, column=0, sticky='w')
        ttk.Label(self.frame_content, text = 'Enter Part Number(s): ').grid(row=4, column=0, sticky='w')
        ttk.Label(self.frame_content, text = ' ').grid(row=5, column=0, sticky='w')
        ttk.Label(self.frame_content, text = 'Clear Form: ').grid(row=6, column=0, sticky='w')
        ttk.Label(self.frame_content, text = ' ').grid(row=7, column=0, sticky='w')
        ttk.Label(self.frame_content, text = 'Contained Part Numbers: ').grid(row=8, column=0, sticky='w')

        self.entry_pn = ttk.Entry(self.frame_content, width=40)
        self.entry_pn.grid(row=4, column=1, sticky='w')
        
        ttk.Button(self.frame_content, text = 'Select', command = self.btn_SelectFile).grid(row=2, column=2)
        ttk.Button(self.frame_content, text = 'Calculate', command=self.btn_Calculate).grid(row=4, column=2)
        ttk.Button(self.frame_content, text = 'Clear', command=self.btn_Clear).grid(row=6, column=2)
        master.bind('<Return>', self.btn_Calculate) # binds clicking the enter key to the Calculate button
        
        # Frame 2 Content
        self.low_frame_content = ttk.Frame(master)
        self.low_frame_content.pack(padx=20, pady=20)
        
        self.out_text = Text(self.low_frame_content) 
        self.out_text.pack(fill=X)



        
    def Setup(self, part_num):
        sub_asms = [] #Sub assembly list
        fpnl = [] #Final part number list
        #print(self.excel_file_path)
        df = pd.read_excel(self.excel_file_path, index_col=0)
        #df = pd.read_excel('Part Numbering Example Set.xlsx', index_col=0)
        #This section reads in the excel file of part numbers and allows a user to input a part number to lookup
        #The part number is assigned to the row indexer and the the comlumn indexer looks for sub asm part numbers
        #The col_indexer is the name of the column we are looking at in the excel file
        row_indexer = part_num 
        col_indexer = 'PN in ASM'
        #This next section searches the data frame (xlsx file) for the row with the part number
        #It then takes the sub asms in the "PN in ASM" column and either says the part number is a single part
        #Or it builds a list of the sub asms that will be sent to the ReSearch funtion to determine the constituents
        row = df.loc[row_indexer]
        part_nums = row[col_indexer]
        if pd.isna(part_nums) == True:
            fpnl.append(row_indexer)
        else:
            sub_asms = part_nums.split(', ')
        return(sub_asms, fpnl, df)

      
    def Search(self, sub_asms, fpnl, df):
        #The ReSearch function takes a list of sub asm part numbers and adds it to one of two lists
        #One list that contains single final part numbers or a list of more sub asm numbers
        #Calling this funtion repetitively will give a list of all sub asms for a single part num 
        for item in sub_asms:
            row_indexer = item
            col_indexer = 'PN in ASM'
            row = df.loc[row_indexer]
            part_nums = row[col_indexer]
            if pd.isna(part_nums) == True:
                fpnl.append(item)
                sub_asms.remove(item)
            else:
                if len(part_nums) == 1:
                    sub_asms = [part_nums]
                else:
                    sub_asms.extend(part_nums.split(', '))
                    sub_asms.remove(item)
            return(sub_asms, fpnl)
        

    def Controller(self, part_list):
        combined_fpnl = [] #all parts in part number list
        for part_num in part_list:
            #The Controller function calls the setup funtion then calls the search funtion repeatedly
            #It then organizes and prints the data
            sub_asms, fpnl, df = self.Setup(part_num)

            while sub_asms != []:
                #print('SA: ', sub_asms) #Used for trouble shooting (Sub Asm)
                new_sub_asms, fpnl = self.Search(sub_asms, fpnl, df)
                #print('FG: ', fpnl) #Used for trouble shooting (Finished Goods)
                #print(' ')
            #Organize and print the data
            fpnl = sorted(fpnl)
            combined_fpnl.append(fpnl)
            #print('Individual Sub Assembly Part Number(s) for: ' + part_num)
            self.out_text.delete(1.0, 'end')
        
        i = 0
        for lists in combined_fpnl:
            self.out_text.insert(END, '  ------   ' + part_list[i] + '\n')
            i += 1
            for item in lists:
                self.out_text.insert(END, item + '\n')
    
    
    def btn_SelectFile(self):
        self.excel_file_path = filedialog.askopenfilename(initialdir = "/", title = "Select File",
                                                          filetypes = (("excel files","*.xlsx"),("all files","*.*")))
        file_name_text =  self.excel_file_path.split('/')
        ttk.Label(self.frame_content, text=file_name_text[-1]).grid(row=2, column=1, sticky='w')
        
        self.status['text'] = ' File selected, enter part number(s) ...'
        
        return(self.excel_file_path)
    
    
    def btn_Clear(self):
        self.entry_pn.delete(0, 'end')
        self.out_text.delete(1.0, 'end')
        self.status['text'] = ' Form cleared, enter part number(s) ...'
    
    
    def btn_Calculate(self, event=None):
        try:
            #prompt = print('Separate Part Numbers with a Comma then a Space')
            #time.sleep(0.2)
            #part_list = input('Enter Part Number(s) to Lookup: ')
            #print('\n')
            #part_list = part_list.split(', ')
            part_list = self.entry_pn.get().split(', ')
            self.Controller(part_list)
            self.status['text'] = ' Child part numbers shown, click clear to restart search ...'
        except KeyError:
            self.status['text'] = ' Please try re-entering part number(s) as shown: 100-1049, 100-1028'
            #sys.exit(1)
        except FileNotFoundError:
            self.status['text'] = ' Please select the proper file ...'
        except AttributeError:
            self.status['text'] = ' Please select the proper file ...'
        except UserWarning:
            pass
    
    def mb_About(self):
        messagebox.showinfo('About', 'Created by Borchr27 2019 for Company Name\n' 
                            'to Look up all single assembly numbers in a\n'
                            'specified part number. Version: {}'.format(version))
            
def main():            
    
    root = Tk()
    app = App(root)
    root.mainloop()
    
    
if __name__ == "__main__": main()