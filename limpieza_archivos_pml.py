#%%
#De los archivos de precios de energía, lee las primeras columnas & al final deja el documento listo para ser convertido en dataframe:
import pandas as pd
import os
import datetime

directorio = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PML\\RAW DATA\\'
os.chdir(directorio)

ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('csv')]
l_mercado, l_fecha, l_sistema = [], [], []

contador = 1
if len(ficheros)!=0:
    for f in ficheros:
        
        tipo = f.split()[0]
        sistema = f.split()[1]
        mercado = f.split()[2]#[0:3]
        fecha = pd.to_datetime(f.split()[4]).date()
        
        renglon = pd.read_csv(f, index_col=False, nrows=0)
        primer_renglon = renglon.columns[0].lstrip().rstrip()

        if primer_renglon == "Precios marginales locales del MDA" or primer_renglon == "Precios de energia en nodos distribuidos del MDA" or primer_renglon == "Precios marginales locales del MTR (Calculo ExPost)":
            df = pd.read_csv(f, skiprows=6, index_col=False)
        else:
            df = pd.read_csv(f, skiprows=7, index_col=False)
        
        df.columns = [c.rstrip().lstrip() for c in df.columns]

        for i in range(len(df)):
            l_mercado.append(mercado)
            l_fecha.append(fecha)
            l_sistema.append(sistema)

        df.insert(0, 'Fecha', pd.DataFrame({'Fecha':l_fecha}))
        df.insert(1, 'Mercado', pd.DataFrame({'Mercado':l_mercado}))
        df.insert(2, 'Sistema', pd.DataFrame({'Sistema': l_sistema}))
        
        print(contador, "/", len(ficheros))
        contador +=1
        df.to_csv(f'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PML\CLEAN DATA\\{tipo}_{sistema}_{mercado}_Dia_{fecha}.csv')
        l_fecha.clear()
        l_mercado.clear()


#%%
pd.to_datetime(f.split()[4]).date()

###############################################################################################################

# #%%
# import pandas as pd
# import os
# from datetime import datetime
# import re

# #Ahora agrega a cada archivo la fecha correspondiente y el mercado correspondiente:
# ruta = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PEND MDA\\Limpios\\BCS\\'
# os.chdir(ruta)
# #getcwd() obtiene el directorio de trabjo actual
# ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('csv')]

# l_fecha, l_mercado, l_archivos_no_procesados = [], [],[]

# for f in ficheros:
    
#     try:
#         df_mda = pd.read_csv(f)
#         fecha = f.split('_')[4][0:-4]
#         df_mda.columns = [re.sub('\\s+', ' ',x.lstrip().rstrip()) for x in df_mda.columns] #re.sub() es una expresión regular en donde el método sub(patron, reemplazo,cadena_texto) retorna un String despues de reemplazar un patron que coincida
#         df_mda = df_mda[['Mercado','Hora','Zona de Carga', 'Precio Zonal ($/MWh)','Componente energia ($/MWh)','Componente perdidas ($/MWh)','Componente Congestion ($/MWh)']]
#     except:
#         l_archivos_no_procesados.append(fecha)
#         print(f"El archivo con fecha: {fecha} no se ha podido completar")
#         continue

#     try:
#         for l in range(len(df_mda)):
#             l_fecha.append(datetime.strftime(datetime.strptime(fecha, '%Y-%m-%d').date(), '%d/%m/%Y'))
#             #print(fecha)
#         df_mda.insert(0,'Fecha', pd.DataFrame({'Fecha':l_fecha}))
#         #df_mda.insert(1,'Mercado ', pd.DataFrame({'Mercado':l_mercado}))
#         df_mda.to_csv(f'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PEND MDA\\Limpios\\BCS CLEAN\\{f}')
#         print(int(ficheros.index(f))+1,'/',len(ficheros))
#     except:
#         l_archivos_no_procesados.append(fecha)
#         print(f"El archivo con fecha: {fecha} no se ha podido completar")

#     l_fecha.clear()
