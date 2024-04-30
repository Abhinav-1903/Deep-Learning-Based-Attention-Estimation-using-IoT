import pandas as pd
import numpy as np
import xlsxwriter as xls
import math


standard_frames = 120
#column numbers
c0 = 0
c1 = 1
c2 = 2
c3 = 3
c4 = 4
row_counter = 0

#sheet variables
sheet = None
hr = []
vr = []

#read the excel sheet as a data frame
with pd.ExcelFile("hrvr_table.xls") as reader:
    sheet = pd.read_excel(reader, sheet_name = 'hrvr_table')
data = sheet.to_numpy() #convert to np array

#strip the values to horizontal and vertical to individual lists
for i in data:
    hr.append(i[0])
    vr.append(i[1])

#lists are ready
#print(hr)
#print(vr)
wb = xls.Workbook('hrvr_table.xls',{'nan_inf_to_errors': True})
sheet = wb.add_worksheet('hrvr_table')
frames = 1
average_hr = 0
average_vr = 0
sum_hr = 0
sum_vr = 0
nan_s = 0
for i in range(len(hr)):
    if(frames == standard_frames ):
        if(nan_s > 60): # more than 1/2 of time was spent undetected, so deem the frame unecessary
            sheet.write(row_counter,c3,-1)
            sheet.write(row_counter,c4,-1)
        else:
        #calculate averages
        #log the averages in to the excel sheet
            average_hr = sum_hr / (frames - (nan_s) )#ignore the number of time the model did not detect of person not found
            average_vr = sum_vr / (frames - (nan_s) ) # fix this bug later
            sheet.write(row_counter,c3,average_hr)
            sheet.write(row_counter,c4,average_vr)
            #print(sum_hr)
            #print(sum_vr)
        row_counter = row_counter +  1 #standard_frames
        nan_s = 0
        sum_hr = 0
        sum_vr = 0
        frames = 1
    if(math.isnan(hr[i])):
        nan_s= nan_s + 1
    else:
        sum_hr = sum_hr + hr[i]
        sum_vr = sum_vr + vr[i]
        print("sum_hr=",sum_hr)
        print("sum_vr=",sum_vr)
    frames = frames + 1
#log the rest of the data after the loop ends, might have less than 120 frames captured
if(frames > 20):
    average_hr = sum_hr / (frames - (nan_s)) 
    average_vr = sum_hr / (frames - (nan_s)) 
    sheet.write(row_counter,c3,average_hr)
    sheet.write(row_counter,c4,average_vr)

wb.close()