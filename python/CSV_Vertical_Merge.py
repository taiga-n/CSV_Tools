'''
The tool to vertically merge csv files in specified folder at once
created csv file will be named as folder name.csv

指定したフォルダ内に存在するCSVファイルを一括で縦結合するツールです
フォルダ名.csvとして保存されます

pip install pysimplegui
'''

import os
import numpy as np
import pandas as pd
import PySimpleGUI as sg
from os.path import basename
import glob 

size1 = (40, 1)
size2 = (30, 1)

layout = [[sg.Text('Path of the folder including csv files that to be merged', size=size1)], 
           [sg.InputText('', size=size2, key='input_folderpath'),
           sg.FolderBrowse('Chose folder')],
           [sg.Button('Merge', key='action')]]

window = sg.Window('CSV vertical merge tool', layout, finalize=True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED: #when cliked "x" button of the window
        break

    if event == 'action':
        if(values["input_folderpath"] != ""):
            
            folderpath = values["input_folderpath"]                    
            files = glob.glob(folderpath + "/*.csv")
                
            if(len(files) <= 0):
                print("Could not find the file．")
                continue
            
            savename = os.path.basename(folderpath)
            savepath = folderpath + "/" + savename + ".csv"    
            
            pd_data = pd.DataFrame()      
            print("File Merging：")
            for i in files:
                print(i)
                pd_data = pd.concat([pd_data, pd.read_csv(i, index_col=0)])
                
            #reset Index
            pd_data.reset_index(inplace=True, drop=True)
            
            try:
                pd_data.to_csv(savepath)
                sg.popup("CSV file created．\nPath: " + savepath) 
                #Open the folder( after converted to absolute path )
                os.startfile(os.path.normpath(os.path.dirname(savepath)))
            except:
                sg.PopupError("Failed to save CSV file.") 
                print("Failed to save CSV file.")
                continue