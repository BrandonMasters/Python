#%%
import pandas as pd
import os
from datetime import datetime
import xlwings as xw
from xlwings.constants import DeleteShiftDirection
ruta = "C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Generacion Liquidada\\"
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
        sheet.range('1:7').api.Delete(DeleteShiftDirection.xlShiftUp)
        print(contador, "/", len(ficheros))
        contador +=1
        wb.save()
        app.kill()

##################################################################################################


#%%
import pandas as pd
import os
from datetime import datetime

ruta = "C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Generacion Liquidada\\"
os.chdir(ruta)

ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
contador = 1
l_mes = []
columnas = pd.DataFrame(columns=['Sistema', 'Dia', 'Hora', 'Fotovoltaica'])

for f in ficheros:
    g_liquidada = pd.read_csv(f)
    #print(f.split()[3:5],len(g_liquidada))
    g_liquidada.columns = [x.rstrip().lstrip() for x in g_liquidada.columns]
    g_liquidada = g_liquidada[['Sistema', 'Dia', 'Hora', 'Fotovoltaica']]
    columnas = pd.concat([columnas, g_liquidada])

columnas['Dia'] = columnas['Dia'].apply(lambda x: (datetime.strptime(x, '%d/%m/%Y').date()))
columnas = columnas.sort_values(by=['Dia', 'Hora']).reset_index(drop=True)
#columnas['Mes'] = columnas['Dia'].apply(lambda x: (x.month))
g_liquidada_mes = columnas.groupby(['Dia']).agg({'Fotovoltaica':'sum'})
# print(columnas)
print(g_liquidada_mes)
g_liquidada_mes.to_csv('Generacion Liquidada Mes/Generacion_Liquidada_Dia.csv')
# columnas = columnas.groupby()
# columnas.to_csv('Generacion_Liquidada_.csv')

#%%
columnas