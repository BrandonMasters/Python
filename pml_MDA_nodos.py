#%%
import pandas as pd
import os
from datetime import datetime

#Directorio en donde se descargaran los archivos:
raw_date = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PML\\RAW DATA\\'
clean_data = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PML\\CLEAN DATA\\'
#Lee la carpeta donde se encuentran los archivos descargados & cambia de directorio para leerlos & realizar los filtros de los nodos indicados:
os.chdir(raw_date)


nodosP = ["03POM-400","05MVC-115", "05CLI-115", "06LAA-138", "06RRD-138", "09LBR-230", "07IVY-230", 
            "07OMS-230", "QUERETARO", "MONTERREY", "OBREGON", "CENTRO SUR", 'VDM NORTE']
l_fechas, l_sistema, l_mercado, l_dataframes = [], [], [], []

#Con listdir() crea una lista de los directorios que estén en el directorio de trabajo actual "getcwd()":
ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('csv')]

if len(ficheros)!=0:
    for f in ficheros:
        tipo_nodo = f.split()[0]
        sistema = f.split()[1]
        mercado = f.split()[2][0:3]
        fecha = f.split()[4]

        pml_mda = pd.read_csv(f, index_col=False, skiprows=7)
        pml_mda.columns = [x.strip() for x in pml_mda.columns]
        pml_mda = pml_mda[[pml_mda.columns[0], pml_mda.columns[1], pml_mda.columns[2]]]

        if tipo_nodo == 'PreciosNodosDistribuidos':
            pml_mda = pml_mda.rename(columns={'Zona de Carga': 'Nodo', 'Precio Zonal ($/MWh)':'PML'})
        else:
            pml_mda = pml_mda.rename(columns={'Clave del nodo': 'Nodo', 'Precio marginal local ($/MWh)':'PML'})

        pml_mda = pml_mda[['Hora', 'Nodo', 'PML']]

        for x in range(len(pml_mda['Hora'])):
            l_sistema.append(sistema)
            l_mercado.append(mercado)
            l_fechas.append(datetime.strptime(fecha, "%Y-%m-%d").date())

        print("Archivo ",(ficheros.index(f)+1),"/",len(ficheros))

        pml_mda.insert(0, 'Fecha', l_fechas)
        pml_mda.insert(1, 'Mercado', l_mercado)
        pml_mda.insert(2, 'Sistema', l_sistema)
        l_dataframes.append(pml_mda)
        l_sistema.clear()
        l_fechas.clear()
        l_mercado.clear()

#Exporta la información a un archivo EXCEL:           
pml_mda_fecha_hora = pd.concat(l_dataframes, ignore_index=False).reset_index(drop=True).sort_values(by=['Nodo', 'Fecha'])
pml_mda_fecha_hora_nodo = pml_mda_fecha_hora[pml_mda_fecha_hora['Nodo'].isin(nodosP)].reset_index(drop=True)
os.chdir(clean_data)
pml_mda_fecha_hora_nodo.to_excel(f"pml_{mercado}_{pml_mda_fecha_hora['Fecha'].iloc[1]}_{pml_mda_fecha_hora['Fecha'].iloc[-1]}.xlsx")