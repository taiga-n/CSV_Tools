'''
A tool to split CSV file in constant intervals
For Example, when lines are 1,2,3,4,5,6 and Data extract interval is 3,
three csv files which consists of lines 1,4 and 2,5 and 3,6 are generated.

CSVファイルの行を一定間隔で抽出分割するツールです
例えば行が1,2,3,4,5,6で，抽出間隔が3のとき，1,4と2,5と3,6の行で構成された3つのcsvファイルが生成されます

pip install pysimplegui
'''

import os
import numpy as np
import pandas as pd
import PySimpleGUI as sg
from os.path import basename

interval = 12

size1 = (40, 1)
size2 = (30, 1)

layout = [[sg.Text('CSV file to be splitted in constant intervals', size=size1)], 
           [sg.InputText('', size=size2, key='input_filepath'),
           sg.FileBrowse('Choose CSV', file_types=(('CSV files','*.csv'),))],
           [sg.Text('Data extract interval', size=size1)],
            [sg.InputText('12', size=size2, key='data_interval')],
            [sg.Button('Split', key='action')]]

window = sg.Window('splitting CSV in constant intervals tools', layout, finalize=True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED: #when clicked "x" button of the window
        break

    if event == 'action':
        if(values["input_filepath"] != "" and values["data_interval"] != ""):
            
            filepath = values["input_filepath"]
            pd_file = None
            
            try:
                interval = int(values["data_interval"])
            except:
                print("Please enter integer")
                continue
                
            try:
                pd_file = pd.read_csv(filepath)
            except:
                print("Failed to open the CSV file")
                continue
            
            filename_without_ext = os.path.splitext(os.path.basename(filepath))[0]
            ditname = os.path.dirname(filepath)
            savepath = ditname + "/" + filename_without_ext
            
            l = 1
            while(os.path.exists(savepath)):
                savepath = savepath + "_" + l
                l = l + 1
                         
            try:
                os.makedirs(savepath)
            except:
                print("Failed to make directory")
                continue
                
            for i in range(0,interval):
                pd_file_edited = pd_file[pd_file.index % interval == i]
                pd_file_edited.to_csv(savepath + "/" + filename_without_ext + "_" + str(i) + ".csv",encoding="shift jis")
            
            sg.popup("CSV file created．\nPath: " + savepath)
            #Open the folder( after converted to absolute path )
            os.startfile(os.path.normpath(savepath))