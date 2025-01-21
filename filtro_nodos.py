#%%
#Lee los archivos CSV, filtra un nodo y exporta el historial del PML de dicho nodo:
import pandas as pd
import os

ruta_pmls = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PML MDA\\Limpios\\SIN\\'
os.chdir(ruta_pmls)

ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
l_df_pmls = []
nodoP = '03TIM-400'

for f in ficheros:
    df_mda = pd.read_csv(f)
    df_mda.columns = [x.lstrip().rstrip() for x in df_mda.columns]
    df_mda = df_mda[['Fecha','Hora','Clave del nodo', 'Precio marginal local ($/MWh)','Componente de energia ($/MWh)','Componente de perdidas ($/MWh)','Componente de congestion ($/MWh)']]
    df_mda_ZonasCarga = df_mda[df_mda['Clave del nodo'] == nodoP]
    print(df_mda_ZonasCarga)
    l_df_pmls.append(df_mda_ZonasCarga)
    print(ficheros.index(f),"/",len(ficheros))

df_pmls=pd.concat(l_df_pmls).reset_index(drop=True)
df_pmls.to_csv(f'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PML MDA\\Limpios\\Nodos Filtrados\\PML_MDA_{nodoP}.csv')
print(df_pmls)


#%%
#Lee los archivos CSV, filtra un nodo y exporta el historial del PML de dicho nodo:
import pandas as pd
import os

ruta_pmls = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PEND MDA\\Limpios\\SIN\\'
os.chdir(ruta_pmls)

ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
l_df_pmls = []
ZonaCarga = 'SALTILLO'

for f in ficheros:
    df_mda = pd.read_csv(f)
    df_mda.columns = [x.lstrip().rstrip() for x in df_mda.columns]
    df_mda = df_mda[['Fecha','Hora','Zona de Carga', 'Precio Zonal ($/MWh)','Componente energia ($/MWh)','Componente perdidas ($/MWh)','Componente Congestion ($/MWh)']]
    df_mda_ZonasCarga = df_mda[df_mda['Zona de Carga'] == ZonaCarga]
    print(df_mda_ZonasCarga)
    l_df_pmls.append(df_mda_ZonasCarga)
    print(ficheros.index(f),"/",len(ficheros))

df_pmls=pd.concat(l_df_pmls).reset_index(drop=True)
df_pmls.to_csv(f'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PML MDA\\Limpios\\Nodos Filtrados\\PML_MDA_{ZonaCarga}.csv')
print(df_pmls)
#%%
############### Lee el historial de los nodos y los junta ##################
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

ruta_pmls = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PML MDA\\Limpios\\Nodos Filtrados\\'
os.chdir(ruta_pmls)

ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
longitud_nodos = {}
l_df_pmls = []
##{0:Fecha, 1:Hora, 2:Precio Marginal Local, 3:Componente Energía, 4:Componente Pérdidas, 5: Componente Congestión}
l_componentes = [0,1,3]

for f in ficheros:
    df_nodo = pd.read_csv(f, index_col=0)
    longitud_nodos[f'{df_nodo["Clave del nodo"][0]}'] = len(df_nodo)
    df_nodo = df_nodo.rename(columns={'Precio marginal local ($/MWh)':f'Precio marginal local ($/MWh) {df_nodo['Clave del nodo'][0]}', 'Componente de energia ($/MWh)':f'Componente de energia ($/MWh) {df_nodo['Clave del nodo'][0]}', 'Componente de perdidas ($/MWh)':f'Componente de perdidas ($/MWh) {df_nodo['Clave del nodo'][0]}', 'Componente de congestion ($/MWh)': f'Componente de congestion ($/MWh) {df_nodo['Clave del nodo'][0]}'})
    #print(df_nodo.columns)
    df_nodo = df_nodo[df_nodo.columns[l_componentes]]
    #df_nodo = df_nodo[["Fecha","Hora", f"Precio marginal local ($/MWh) {df_nodo['Clave del nodo'][0]}",f"Componente de energia ($/MWh) {df_nodo['Clave del nodo'][0]}", f"Componente de perdidas ($/MWh) {df_nodo['Clave del nodo'][0]}", f"Componente de congestion ($/MWh) {df_nodo['Clave del nodo'][0]}"]]
    df_nodo = df_nodo.set_index(['Fecha','Hora'])
    l_df_pmls.append(df_nodo)
    #print(df_nodo)
    # df_nodo['Fecha'] = df_nodo['Fecha'].apply(lambda x:datetime.strptime(x,'%d/%m/%Y'))
    # #df_nodo['Hora'] = df_nodo['Hora'].apply(lambda x: x) 
    # df_fecha_hora = pd.to_datetime(df_nodo['Fecha'] + df_nodo['Hora'].apply(pd.DateOffset(hour=+1)))
    # df_nodo.insert(0,'Fecha y Hora', df_fecha_hora)
    # df_nodo.to_csv(f)
    # print(ficheros.index(f),'/', len(ficheros))
l_df_pmls.sort(key=lambda x:len(x), reverse=True)
df_nodos_union = pd.concat(l_df_pmls, axis=1)
df_nodos_union.to_csv('Nodos_filtrados.csv')
# l_longitud_nodos = list(longitud_nodos.items())
# l_longitud_nodos.sort(key=lambda x:x[1], reverse=True)
#%%
############Graficando Nodos#############
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

ruta_pmls = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PML MDA\\Limpios\\Nodos Filtrados\\'
os.chdir(ruta_pmls)
ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]

pd.read_csv(ficheros[0]).plot(x='Fecha y Hora', y='Precio marginal local ($/MWh)')

# for f in ficheros:
#     nodo = pd.read_csv(f, index_col=0)
#     nodo = nodo[['Fecha y Hora', 'Precio marginal local ($/MWh)']]
#     plt.plot(nodo['Fecha y Hora'], nodo['Precio marginal local ($/MWh)'])


#%%
print(type(df_pmls['Precio marginal local ($/MWh)'][0]))

#%%
##### Junta los archivos y filtra los Nodos #####
import pandas as pd
import os
from datetime import datetime

ruta_pmls = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PEND MDA\\Limpios\\SIN\\'
os.chdir(ruta_pmls)

ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.xlsx')]
l_dataframes_pml = []
contador = 1

for f in ficheros:
    nom_archivo = f[1:61].replace("'","").replace(",","").replace(" ","_")
    print(nom_archivo)

    df_pml = pd.read_excel(f, index_col=False)
    df_pml.to_csv(f"{nom_archivo}.csv", index=False)
    # l_dataframes_pml.append(df_pml)
    print(contador, "/",len(ficheros))
    contador += 1 

# df_joined_pml = pd.concat(l_dataframes_pml)
# print(df_joined_pml)

