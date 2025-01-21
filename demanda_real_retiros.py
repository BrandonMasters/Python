#%%
#Programa que juntas varios archivos CSV en un Dataframe y los exporta:
import pandas as pd
import os

directorio = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Demanda Real por Retiros\\'
os.chdir(directorio)

ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
l_fechas = []

df_demanda_real_retiro = pd.DataFrame(columns=['Fecha','Sistema','Zona de Carga','Hora', 'Estimacion de Demanda por Retiros (MWh)'])
contador = 1

# try:
ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
if len(ficheros) != 0:
    for f in ficheros:

        Valores_demanda_real_retiro = pd.read_csv(f, skiprows= 8, usecols = ['Sistema',' Zona de Carga',' Hora', ' Estimacion de Demanda por Retiros (MWh) '])
        Valores_demanda_real_retiro = Valores_demanda_real_retiro.dropna()
        Valores_demanda_real_retiro.columns = [x.lstrip().rstrip() for x in Valores_demanda_real_retiro.columns]
        
        fecha = f.split()[5]
        print(fecha)
        for i in range(len(Valores_demanda_real_retiro['Sistema'])):
            l_fechas.append(fecha)
        df_fecha = pd.DataFrame({'Fecha':l_fechas})

        Valores_demanda_real_retiro = pd.concat([df_fecha, Valores_demanda_real_retiro], axis=1)
        print((Valores_demanda_real_retiro))
        df_demanda_real_retiro =pd.concat([df_demanda_real_retiro,Valores_demanda_real_retiro])
        l_fechas.clear()

# except:
#     print(f"No existe directorio o no se ha podido generar la lista de los ficheros contenidos en la carpeta: ")
df_demanda_real_retiro = df_demanda_real_retiro.sort_values(by=['Fecha','Sistema','Zona de Carga']).reset_index(drop=True)
df_demanda_real_retiro.to_csv('demanda_real_retiro.csv')
# %%
