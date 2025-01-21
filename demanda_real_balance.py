#%%
#Programa que juntas varios archivos CSV en un Dataframe y los exporta:
import pandas as pd
import os
from datetime import datetime

directorio = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Demanda Real por Balance\\Demanda Balance septiembre\\'
os.chdir(directorio)

ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
l_fechas = []

df_demanda_real_b = pd.DataFrame(columns=['Fecha','Sistema','Area','Hora', 'Generacion (MWh)', 'Estimacion de Demanda por Balance (MWh)'])

if len(ficheros) != 0:
    for f in ficheros:
        
        fecha = f.split()[5]
        longitud_nombre_archivo = "".join(f.split())

        if len(longitud_nombre_archivo) == 62:
            valores_demanda_real_b = pd.read_csv(f, skiprows= 9, index_col=False)
            print(valores_demanda_real_b.columns)
            valores_demanda_real_b.columns = [x.lstrip().rstrip() for x in valores_demanda_real_b.columns]
            print(datetime.strptime(fecha,'%Y-%m-%d').date())
            valores_demanda_real_b = valores_demanda_real_b[['Sistema', 'Area', 'Hora', 'Generacion (MWh)', 'Estimacion de Demanda por Balance (MWh)']]

        else:
            valores_demanda_real_b = pd.read_csv(f, skiprows= 8, index_col=False) 
            valores_demanda_real_b.columns = [x.lstrip().rstrip() for x in valores_demanda_real_b.columns]

            valores_demanda_real_b = valores_demanda_real_b.rename(columns={'CLV_SISTEMA': 'Sistema', 'CLV_AREA':'Area', 'HORA':'Hora', 'GENERACION':'Generacion (MWh)', 
                                                       'IMPORTACION':'Importacion Total (MWh)', 'EXPORTACION': 'Exportacion Total (MWh)', 'ENERGIA ENTRE GERENCIAS':'Intercambio neto entre Gerencias (MWh)',
                                                         'BALANCE':'Estimacion de Demanda por Balance (MWh)'})
            print(datetime.strptime(fecha,'%Y-%m-%d').date())
            valores_demanda_real_b = valores_demanda_real_b[['Sistema', 'Area', 'Hora', 'Generacion (MWh)', 'Estimacion de Demanda por Balance (MWh)']]

        for i in range(len(valores_demanda_real_b['Sistema'])):
            l_fechas.append(datetime.strptime(fecha,'%Y-%m-%d').date())

        df_fecha = pd.DataFrame({'Fecha':l_fechas})
        valores_demanda_real_b.insert(0, 'Fecha',df_fecha)
        #valores_demanda_real_b['Fecha'] = df_fecha
        #valores_demanda_real_b = pd.concat([df_fecha, valores_demanda_real_b], axis=1)
        print(valores_demanda_real_b)
        valores_demanda_real_b.reset_index()
        df_demanda_real_b =pd.concat([df_demanda_real_b,valores_demanda_real_b])
        l_fechas.clear()
        print(df_demanda_real_b)

# except:
#     print(f"No existe directorio o no se ha podido generar la lista de los ficheros contenidos en la carpeta: ")

#df_demanda_real_b[df_demanda_real_b.columns[7]] = df_demanda_real_b[df_demanda_real_b.columns[7]].replace('---','0')
df_demanda_real_b = df_demanda_real_b[(df_demanda_real_b['Sistema'] =='SIN')].reset_index(drop=True)
#df_demanda_real_b[df_demanda_real_b.columns[7]] = df_demanda_real_b[df_demanda_real_b.columns[7]].apply(lambda x: ((x.replace('---','0').strip())))
#df_demanda_real_b[df_demanda_real_b.columns[7]] = df_demanda_real_b[df_demanda_real_b.columns[7]].apply(lambda x: float(x))
#df_demanda_real_b = df_demanda_real_b.groupby(['Fecha', 'Sistema', 'Hora']).agg({'Generacion (MWh)':'sum', 'Estimacion de Demanda por Balance (MWh)':'sum'}).reset_index()
df_demanda_real_b.to_excel('demanda_real_balance_septiembre.xlsx')

# %%
