# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:48:50 2019

@author: Dat Le-Phan
"""

file = []
final_list = []
f = 'C:\\Users\\' #File Path
import os
import xlwt
from xlwt import Workbook
def main(): 
    collect()
    print(str(file))
    print(len(file))
    
    
    
#    print(str(final_list))
    


def collect():
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    
    n = 0
    
    for filename in os.listdir(f): 
        tempFi_ = filename.rpartition('_')[0]
        tempFi__ = tempFi_.rsplit('_',1)[0]
        if tempFi__ not in file:
            sheet1.write(n,0,tempFi__)
            if "_" not in tempFi__:
                file.append(tempFi__)
            else:
                tempFi__.rsplit('_',1)[0]
            n = n + 1
    wb.save('x.xls') #New File save


def output(filename, sheet, list1, list2, x, y, z):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)

    variables = [x, y, z]
    x_desc = 'x'
    y_desc = 'y'
    z_desc = 'z'
    desc = [x_desc, y_desc, z_desc]

    col1_name = 'i'
    col2_name = 'j'

    #You may need to group the variables together
    #for n, (v_desc, v) in enumerate(zip(desc, variables)):
    for n, v_desc, v in enumerate(zip(desc, variables)):
        sh.write(n, 0, v_desc)
        sh.write(n, 1, v)

    n+=1

    sh.write(n, 0, col1_name)
    sh.write(n, 1, col2_name)

    for m, e1 in enumerate(list1, n+1):
        sh.write(m, 0, e1)

    for m, e2 in enumerate(list2, n+1):
        sh.write(m, 1, e2)

    book.save(filename)


#def names():
#    collect()
#    for text in file:
#        x = text.split(" ", 1)
#        final_list.append(x)

# Driver Code 
if __name__ == '__main__': 
      
    # Calling main() function 
    main() 