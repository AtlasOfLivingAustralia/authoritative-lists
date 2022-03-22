# IBSA - Data File Processing

import geopandas as gpd
import Config as cfg
import os
import pandas as pd
from tkinter import Tk, filedialog

root = Tk()  # pointing root to Tk() to use it as Tk() in program.
root.withdraw()  # Hides small tkinter window.
root.attributes('-topmost', True)  # Opened windows will be active. above all windows despite of selection.

# Open dialog box to select images with specific extensions.
# open_file = filedialog.askopenfilenames(filetypes=[("Data Files", cfg.fType)]) # returns a tuple with opened file's complete path
open_file = filedialog.askopenfilenames(
    filetypes=[("Data Files", cfg.fType)])  # returns a tuple with opened file's complete path
fnameList = []
fCt = 0
for fval in open_file:
    fPath = os.path.split(fval)[0]
    fnameList.append(os.path.basename(fval))
    x = fnameList[fCt]
#  Add code to check file suffix
# Shapefile
    locals()[x] = gpd.read_file(fval)
# JSON file
#    locals()[x] = pd.read_json(fval)
   temp = locals()[x]
   temp.to_excel(cfg.outDir+'nsw_sensitive.xlsx',index=False)
   fCt += 1


