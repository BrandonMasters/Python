#%%
import pandas as pd
import os
from datetime import datetime
import xlwings as xw
from xlwings.constants import DeleteShiftDirection
ruta = "C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Ofertas Recursos Intermitentes Despachables\\"
os.chdir(ruta)
ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
contador = 1
if len(ficheros) != 0:
    for f in ficheros:
        #renglon = pd.read_csv(f)
        #primer_renglon = renglon.columns[0].lstrip().rstrip()
        app = xw.App()
        wb = app.books.open(f)
        sheet = wb.sheets[wb.sheet_names[0]]
        sheet.range('1:8').api.Delete(DeleteShiftDirection.xlShiftUp)
        print(contador, "/", len(ficheros))
        contador +=1
        wb.save()
        app.kill()

################################################