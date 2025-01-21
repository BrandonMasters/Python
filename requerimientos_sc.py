#%%
#Programa que juntas varios archivos CSV en un Dataframe y los exporta:
import pandas as pd
import os
from datetime import datetime

directorio = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Requerimientos de Servicios Conexos MTR\\Reservas agosto\\'
os.chdir(directorio)

l_fechas = []

columnas = pd.DataFrame(columns=['Fecha','Zona de Reserva', 'Hora', 'RT Reserva Regulacion (MW)', 'RT Reserva Rodante 10 (MW)', 'RT Reserva 10 (MW)', 'RT Reserva Suplementaria (MW)'])
contador = 1

# try:
ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
if len(ficheros) != 0:
    for f in ficheros:
        fecha = f.split()[4]
        print(fecha)
        

        sc = pd.read_csv(f, skiprows= 7)
        print(sc.columns)
        sc.columns = [x.lstrip().rstrip() for x in sc.columns]
        print(sc.columns)
        sc = sc[['Zona de Reserva','Hora','RT Reserva Regulacion (MW)', 'RT Reserva Rodante 10 (MW)', 'RT Reserva 10 (MW)', 'RT Reserva Suplementaria (MW)']]
        sc = sc.dropna()

        for i in range(len(sc['Zona de Reserva'])):
            l_fechas.append(datetime.strptime(fecha,'%Y-%m-%d').date())
        
        df_fecha = pd.DataFrame({'Fecha':l_fechas})

        sc = pd.concat([df_fecha, sc], axis=1)
        print((sc))
        columnas =pd.concat([columnas,sc])
        l_fechas.clear()

# except:
#     print(f"No existe directorio o no se ha podido generar la lista de los ficheros contenidos en la carpeta: ")
columnas['Reservas Operativas'] = columnas['RT Reserva Regulacion (MW)'] + columnas['RT Reserva Rodante 10 (MW)'] + columnas['RT Reserva 10 (MW)']
columnas = columnas.sort_values(by=['Fecha', 'Zona de Reserva']).reset_index(drop=True)
columnas.to_excel('reqe_sc_agosto.xlsx')


# %%
