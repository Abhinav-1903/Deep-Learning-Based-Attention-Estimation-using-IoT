"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import sys
import xlwt
import time
import cv2
from gaze_tracking import GazeTracking
from evaluate_sheet import _process_sheet


gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
TT = 600  #number of frames it is going to run
wb = xlwt.Workbook()
sheet = wb.add_sheet('hrvr_table')
c0 = 0
c1 = 1
c2 = 2
i = 0

while TT > 0:
    _, frame = webcam.read()
    gaze.refresh(frame)
    frame = gaze.annotated_frame()
    cv2.imshow("Demo", frame)
    sheet.write(i,c0,gaze.horizontal_ratio()) #first row
    sheet.write(i,c1,gaze.vertical_ratio())   #second row
    TT = TT - 1
    i = i + 1
    time.sleep(0.5)
    if cv2.waitKey(1) == 27:
        break

wb.save('hrvr_table.xls')

_process_sheet()