#%%
#Importando módulos:
import pandas as pd
import os
from datetime import datetime

#directorio = 'C:\\Users\\Hp\\OneDrive\\Documentos\\Brandon\\Python\\Cenace\\Capacidad de Transferencia\\'
directorio = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Capacidad de Transferencia\\'
#Con el módulo os, cambia de directorio y se coloca justo donde se encuentran los archivos a leer:
os.chdir(directorio)

columnas = pd.DataFrame(columns=['Sistema','Fecha','Horario','Enlace', 'Capacidad de Transferencia Disponible para Exportacion Comercial (MWh)'])

ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
if len(ficheros) != 0:
    for f in ficheros:
        
        #Separa el titulo en una lista:
        fecha = datetime.strptime(f.split()[4], '%Y-%m-%d').strftime('%d/%m/%Y')
        
        #Lee el archivo y usa dos columnas de la hora especificada, borra los valores nulos:
        cap_trans_1 = pd.read_csv(f, skiprows= 7)
        cap_trans_1.columns = [x.lstrip().rstrip() for x in cap_trans_1.columns]
        cap_trans_1 = cap_trans_1[['Sistema','Fecha','Horario','Enlace', 'Capacidad de Transferencia Disponible para Exportacion Comercial (MWh)']]
        cap_trans_1 = cap_trans_1.dropna()
        cap_trans_1 = cap_trans_1[cap_trans_1['Fecha'] == fecha]
        columnas = pd.concat([columnas,cap_trans_1])

columnas = columnas[columnas['Enlace'] == 'TAPACHULA-LOS BRILLANTES']
columnas = columnas.reset_index(drop=True)

# for idx, row in columnas.iterrows():
#     fecha_hora = pd.to_datetime(row['Horario'], format='%d/%m/%Y')
#     columnas.loc[idx,'Horario'] = fecha_hora

# for idx, row in columnas.iterrows():
#     fecha_hora = (pd.Timestamp(row['Fecha']).strftime("%d/%m/%Y").replace(minute=0, hour=0, second=0) + pd.DateOffset(hours= row['Horario']-1)).strftime("%d/%m/%Y %H:%M:%S")
#     columnas.loc[idx,'Fecha & Hora'] = fecha_hora

for idx, row in columnas.iterrows():
    fecha_hora = (datetime.strptime(row['Fecha'], '%d/%m/%Y').replace(minute=0, hour=0, second=0) + pd.DateOffset(hour=row['Horario']-1)).strftime("%d/%m/%Y %H:%M:%S")
    columnas.loc[idx,'Fecha & Hora'] = fecha_hora
    
print(columnas)
columnas.to_csv('capacidad_transferencia_v3.csv')

# %%
