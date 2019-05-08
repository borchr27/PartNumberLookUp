"""
ABOUT
Program written in April/May 2018 as a sub assembly tracker to allow a user to type in a finished 
goods part number then return all the individual parts/part numbers within that assembly. Note that all assembly numbers and part numbers are in the same sequential part number list, such that an assembly can reference an assembly before or after, as long as it has been defined.

CODE
The code uses Pandas to translate the excel file into a workable/searchable format.
The SEARCH function locates the initial part number in the excel file.
It then pulls all the sub assembly or final part numbers into two lists.
One list (fnpl, which stands for final part number list) is used to store base level part numbers that have no sub assemblies.
The next list (sub_asms) is carried thru the functions and holds part numbers that still have sub assemblies.
Next Steps: 
1. Allow ability to enter multiple PN - Done
2. Create visual part number tree

Example / Test Case
100-1049
32, 37, 40, 44, 45, 46
32, (31, 28), (1, 39), 44, 45, 46
31, 32, (4), 1, 39, 44, 45, 46
1, 1, 3, 31, 32, 39, 44, 45, 46
Finished Goods for PN 100-1049: ^
"""

import pandas as pd

class PartNumberLookup(object):
    
    def __init__(self, part_list):
        self.part_list = part_list
        pass


    def Setup(self, part_num):
        sub_asms = [] #Sub assembly list
        fpnl = [] #Final part number list
        df = pd.read_excel('Part Numbering Example Set.xlsx', index_col=0)
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
        for part_num in part_list:
            #The Controller function calls the setup funtion then calls the search funtion repeatedly
            #It then organizes and prints the data
            sub_asms, fpnl, df = PartNumberLookup(part_list).Setup(part_num)
            while sub_asms != []:
                print('SA: ', sub_asms) #Used for trouble shooting (Sub Asm)
                new_sub_asms, fpnl = PartNumberLookup(part_list).Search(sub_asms, fpnl, df)
                print('FG: ', fpnl) #Used for trouble shooting (Finished Goods)
                print(' ')
            #Organize and print the data
            fpnl = sorted(fpnl)
            print('Individual Sub Assembly Part Number(s) for: ' + part_num)
            for item in fpnl:
                print(item)
            

prompt = print('Separate Part Numbers with a Comma then a Space')
part_list = input('Enter Part Number(s) to Lookup: ')
part_list = part_list.split(', ')
PartNumberLookup(part_list).Controller(part_list)
