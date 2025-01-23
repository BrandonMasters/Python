#%%
#Librerias:
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import datetime
from datetime import datetime
import requests
import os

#Directorio en el cual se descargarán los archivos:
dir_presas = "C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\RAW DATA\\"

#Instancia de la clase Options:
opciones = Options()

#Modifica las opciones de CHROME:
preferencias = {"download.default_directory": dir_presas,
                   "download.prompt_for_download": False,
                   "directory_upgrade": True,
                   "safebrowsing.enabled": True,
                   "behavior":"allow"}

opciones.add_experimental_option('prefs', preferencias)
opciones.add_argument("start-maximized")

#Instancia de la clase Chrome (libreria webdriver)
driver = webdriver.Chrome(options = opciones)

#Establece las fechas para la descarga de archivos:
rango_fechas = pd.date_range(start="2024/12/02", end="2024/12/23")
l_fechas = [l for l in rango_fechas]
# archivos_pendientes = pd.read_csv('C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\Niveles de agua (Presas)\\Archivos_pendientes_Presas.csv', index_col=0)
# archivos_pendientes = archivos_pendientes[archivos_pendientes.columns[0]].apply(lambda x : datetime.strptime(x, '%Y-%m-%d').date())
# l_fechas = [l for l in archivos_pendientes.to_list()]

#Petición get
url = "https://sinav30.conagua.gob.mx:8080/Presas/"
driver.get(url)
status = requests.get(url).status_code

if status == 200:
    #Espera a que la fecha con información mas reciente esté disponible y después da click en el botón de "REPORTE:
    WebDriverWait(driver,10).until_not(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div/h5"), "undefined"))

    #Primero escribe la fecha del archivo por descargar:
    for fecha in l_fechas:
        #Emmpieza seleccionando y mandando datos de la forma: DIA, MES y al final el AÑO
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/input[2]").click() #Se presiona para seleccionar el DIA
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/input[2]").clear() #Se borra el DIA
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/input[2]").send_keys(fecha.day) #Se mandan valores a la parte del DIA
        
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/input[3]").click() #Se presiona para seleccionar el MES
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/input[3]").clear() #Se borra el MES
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/input[3]").send_keys(fecha.month) #Se mandan valores a la parte del MES
        
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/input[4]").click() #Se presiona para seleccionar el AÑO
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/input[4]").clear() #Se borra el AÑO
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/input[4]").send_keys(fecha.year) #Se mandan valores a la parte del AÑO

        
        #Espera a que el POP UP aparezca y despues desaparezca:
        try:
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div')))
            WebDriverWait(driver,10).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]/div')))
        except:
            continue
        #Da click fuera del calendario para que este se cierre:
        time.sleep(2)
        #WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/span/div/div')))
        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/button[2]').click()
        except:
            print("No se ha logrado cerrar el calendario")
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/div/button[2]').click()
        WebDriverWait(driver,10).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div/div/span/div/div')))

        #Click en el botón REPORTE, el cual abre una ventana emergente para descargar los archivos:
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[4]/div/div").click()

        #Espera a que encuentre texto presente en la pantalla emergente:
        WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[4]/div/div/div[1]/div/b'), f'Reportes'))

        #Click para descargar el archivo:    
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div[2]/div/div[1]/div[3]/a"))).click()
        #driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div[2]/div/div[1]/div[3]/a").click()

        #Click para cerrar ventana emergente
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[1]/button[2]'))).click()
        #driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[1]/button[2]").click()

        print(fecha.year, fecha.month, fecha.day)
    driver.close()
else:
    print("Status Code %d" % status)

#%%
############### Se limpian los archivos y se agrega nueva columna "Porcentaje de llenado" ####################
import pandas as pd
import datetime
from datetime import datetime
import requests
import os
import chardet

#Directorio en el cual se descargarán los archivos:
dir_presas = "C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\Nivel de Presas\\"
carpetas = [x for x in os.scandir(dir_presas) if x.is_dir()]

l_fechas, l_df_presas = [],[]
contador = 1

#Explora cada carpeta y lee cada archivo:
for c in carpetas:
    carpeta = os.chdir(dir_presas + '\\' + str(c.name))
    ficheros = [x for x in os.listdir(carpeta) if x.endswith('.csv')]
    for f in ficheros:
        #Abre el archivo y lee la codificación y la usa en el metodo "read_csv". Con esto se asegura que la codificacion siempre es correcta
        with open(f, "rb") as file:
            contenido = file.read()
            codificion_detectada = chardet.detect(contenido)['encoding']
        archivo_presas = pd.read_csv(f, delimiter=',', encoding=codificion_detectada).reset_index(drop=True)
        
        archivo_presas.columns = [' '.join(columna.split()) for columna in archivo_presas.columns]

        #Toma el valor de la fecha y lo agrega al dataframe:
        fecha = f.split('_')[2][0:-4]
        for l in range(len(archivo_presas)):
            l_fechas.append(str(fecha))
        column_fecha = pd.DataFrame({'fecha':l_fechas})
        archivo_presas.insert(0,'fecha', column_fecha)

        #Elimina espacios en blanco en cada renglón:
        archivo_presas['Nombre de presa'] = archivo_presas['Nombre de presa'].apply(lambda x: ' '.join(x.split()))
        archivo_presas['Entidad federativa'] = archivo_presas['Entidad federativa'].apply(lambda x: ' '.join(x.split()))

        #Homologa la columna Entidad Federativa y agrega una nueva columna de porcentaje de llenado pero con dos decimales:
        archivo_presas['Entidad federativa'] = archivo_presas['Entidad federativa'].replace({'Coahuila de Zaragoza':'Coahuila', 'Veracruz de Ignacio de la Llave':'Veracruz', 'México':'Estado de México'})
        
        archivo_presas['porcentaje de llenado'] = round((archivo_presas['Almacenamiento Actual (hm³)'].astype(float)) / (archivo_presas['NAMO Almacenamiento (hm³)'].astype(float))*100, 2)
        archivo_presas['Nombre de presa'] = archivo_presas['Nombre de presa'].replace({r'á':'a', r'é':'e', r'í':'i', r'ó':'o', r'ú':'u', r'Á':r'A', r'É':'E', r'Í':'I', r'Ó':'O', r'Ú':'U'}, regex=True)
        archivo_presas['Nombre de presa'] = archivo_presas['Nombre de presa'].replace({r"\.,":","}, regex=True)
        for i in range(len(archivo_presas)):
            #print(archivo_presas.loc[i, "Nombre de presa"])
            archivo_presas.loc[i, "Nombre de presa"] = archivo_presas.loc[i, "Nombre de presa"].split(',')[0]
        
        #print(archivo_presas)
        l_df_presas.append(archivo_presas)
        l_fechas.clear()

    df_presas = pd.concat(l_df_presas)
    df_presas = df_presas[['fecha', 'Nombre de presa', 'Entidad federativa', 'NAME Almacenamiento (hm³)', 'NAMO Almacenamiento (hm³)', 'Almacenamiento Actual (hm³)', 'porcentaje de llenado']]
    #df_presas.to_csv(f'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\CLEAN DATA 2\\Nivel de presas {str(2024)}.csv', encoding='latin-1', index=0)

    df_presas.to_csv(f'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\CLEAN DATA 2\\Nivel de presas {c.name}.csv', encoding='latin-1', index=0)
    print(contador, "/", len(carpetas))
    contador += 1
    l_df_presas.clear()
    

#%%
archivo_presas

#%%
############### Se consulta qué archivos hacen falta, dado que el webscraping de los niveles de presas arroja datos repetidos ##################
import pandas as pd
import datetime
from datetime import datetime
import os

dir = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\Niveles de agua (Presas)\\'
os.chdir(dir)

ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
l_fechas_archivos = []
for f in ficheros:
    l_fechas_archivos.append(datetime.strptime(f.split('_')[2][0:-4], "%Y-%m-%d").date())
#df_fechas_archivos = pd.DataFrame({'Fechas':l_fechas_archivos})

#df_rango_fechas = pd.DataFrame({'Fechas': pd.date_range(start='1991/01/01', end='2024/8/28')})
#l_rango_fechas = [l.date() for l in df_rango_fechas]
l_fechas_generadas = pd.date_range(start='1991/01/01', end='2024/8/28').date

set_archivos = set(l_fechas_archivos)
set_fechas_generadas = set(l_fechas_generadas)

archivos_pendientes = set_fechas_generadas - set_archivos
df_fechas_pendientes = pd.DataFrame({'Fechas':list(archivos_pendientes)}).sort_values(by="Fechas").reset_index(drop=True)
df_fechas_pendientes
#df_fechas_pendientes.to_csv('Archivos_pendientes_Presas.csv')


#%%
############# Programa que mueve archivos en distintos directorios ###############
import pandas as pd
import datetime
from datetime import datetime
import os
import shutil

dir = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\Nivel de Presas\\'
os.chdir(dir)
ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
carpetas = [x for x in os.scandir(os.getcwd()) if x.is_dir()]

l_dataframes = []
contador = 1
for c in carpetas:
    for f in ficheros:
        anio_archivo = f.split('_')[2][0:4]
        print(anio_archivo, str(c.name))
        if anio_archivo == str(c.name):
            src_path = os.path.join(os.getcwd(), f)
            dst_path = os.path.join(os.getcwd() + '\\' + str(c.name) + '\\',f)
            shutil.move(src_path, dst_path)
            print(src_path, dst_path)
        print(contador,'/',len(ficheros))
        contador+=1

#%%
#Mueve en cada carpeta, sus archivos correspondientes:
import pandas as pd
import datetime
from datetime import datetime
import os

dir = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\Nivel de Presas\\'
os.chdir(dir)
#ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
carpetas = [x for x in os.scandir(os.getcwd()) if x.is_dir()]

l_dataframes = []
contador = 1
for c in carpetas:
    os.chdir(dir + '\\' + c.name)
    ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]
    #print(ficheros)
    for f in ficheros:
        l_dataframes.append(pd.read_csv(f, encoding='latin-1'))
    pd.concat(l_dataframes).to_csv(f'Nivel_de_presas_{c.name}.csv', encoding='latin-1')
    print(contador,'/',len(carpetas))
    contador+=1
    l_dataframes.clear()

#%%
###################### Coloca las coordenadas correspondientes a las presas #########################
import pandas as pd
import datetime
from datetime import datetime
import os

dir_presas = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\Niveles de agua (Presas)\\'
coordenadas_presas = pd.read_excel('C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\Registro_presas_2023_2024_V2.xlsx', 0)
os.chdir(dir_presas)
l_archivos_presas = [x for x in os.listdir(os.getcwd()) if x.endswith('csv')]
l_coordenas_cartesianas, l_longitud, l_latitud, l_presas_coordenadas_pendientes = [],[],[],[]

dic_coordenas_cartesianas = dict(zip(coordenadas_presas['Nombre de presa'], coordenadas_presas['Coordenadas cartesianas']))
dic_longitud = dict(zip(coordenadas_presas['Nombre de presa'], coordenadas_presas['Longitud']))
dic_latitud = dict(zip(coordenadas_presas['Nombre de presa'], coordenadas_presas['Latitud']))

for archivo in l_archivos_presas:
    nombre_archivo = archivo[0:-4]
    df_presa = pd.read_csv(archivo, encoding='latin-1')
    df_presa.columns = [x.rstrip().lstrip() for x in df_presa.columns]
    try:
        df_presa['Nombre de presa'] = df_presa['Nombre de presa'].apply(lambda x: x.strip())
        df_presa['Nombre común'] = df_presa['Nombre común'].apply(lambda x: x.strip())
        df_presa['Organismo de cuenca'] = df_presa['Organismo de cuenca'].apply(lambda x: x.strip())
        df_presa['Entidad federativa'] = df_presa['Entidad federativa'].apply(lambda x: x.strip())
    except:
        print('No se ha logrado eliminar los espacios en blanco para el archivo: ', (archivo[0:-4]))
        continue
    l_nombre_presas = list(df_presa['Nombre de presa'])
    try:
        for c in l_nombre_presas:
            l_coordenas_cartesianas.append(dic_coordenas_cartesianas[c])
        df_presa['Coordenadas cartesianas'] = l_coordenas_cartesianas
        #df_presa['Coordenadas cartesianas'] = [dic_coordenas_cartesianas[i] for i in l_nombre_presas]
        df_presa['Longitud'] = [dic_longitud[i] for i in l_nombre_presas]
        df_presa['Latitud'] = [dic_latitud[i] for i in l_nombre_presas]
        
    except:
        print('No se ha logrado colocar las coordenadas para los archivos: ', (archivo[0:-4]))
        print('La presa que no tiene coordenadas es: ', c)
        l_presas_coordenadas_pendientes.append(c)
        continue
    df_presa = df_presa[['Fecha', '#', 'Nombre de presa', 'Nombre común', 'Organismo de cuenca', 'Entidad federativa', 'NAME Elevación (msnm)', 'NAME Almacenamiento (hm³)', 'NAMO Elevación (msnm)', 'NAMO Almacenamiento (hm³)', 'Elevación Actual (msnm)', 'Almacenamiento Actual (hm³)', 'Porcentaje de llenado', 'Coordenadas cartesianas', 'Longitud', 'Latitud']]
    df_presa.to_csv(f'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\Nivel de presas limpios\\{nombre_archivo}.csv', encoding='latin-1')
pd.DataFrame({'Coordenadas Presas Pendientes':l_presas_coordenadas_pendientes}).to_csv('C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\coordenadas_presas_pendientes.csv', encoding='latin-1')


#%%
###################### Genera el catálogo de Presas #########################
import pandas as pd
import datetime
from datetime import datetime
import os

#Cambia de directorio y genera una lista de los archivos CSV ubicados en esa carpeta:
dir_presas = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\DATOS VARIOS\\CLEAN DATA\\'
os.chdir(dir_presas)
l_archivos_presas = [x for x in os.listdir(os.getcwd()) if x.endswith('csv')]
l_df_presas = []
contador = 1

#Utiliza solamente algunas columnas y genera una nueva "Porcentaje de llenado"
for archivo in l_archivos_presas:
    archivo_presas = pd.read_csv(archivo, sep=',', index_col=0, encoding='latin-1')
    archivo_presas = archivo_presas.reset_index(drop=True)
    archivo_presas.columns = [' '.join(columna.split()) for columna in archivo_presas.columns]
    archivo_presas = archivo_presas[['Fecha', 'Nombre de presa', 'Entidad federativa', 'NAME Almacenamiento (hm³)', 'NAMO Almacenamiento (hm³)', 'Almacenamiento Actual (hm³)']]
    
    #Elimina espacios en blanco en cada renglón:
    archivo_presas['Nombre de presa'] = archivo_presas['Nombre de presa'].apply(lambda x: ' '.join(x.split()))
    archivo_presas['Entidad federativa'] = archivo_presas['Entidad federativa'].apply(lambda x: ' '.join(x.split()))

    #Elimina duplicados agrega nueva columna, elimina acentos y homologa nombres de presa:
    archivo_presas = archivo_presas.drop_duplicates().reset_index(drop=True)
    archivo_presas['Porcentaje de llenado'] = round(archivo_presas['Almacenamiento Actual (hm³)'] / archivo_presas['NAMO Almacenamiento (hm³)'] *100, 2)
    archivo_presas['Nombre de presa'] = archivo_presas['Nombre de presa'].replace({r'á':'a', r'é':'e', r'í':'i', r'ó':'o', r'ú':'u', r'Á':r'A', r'É':'E', r'Í':'I', r'Ó':'O', r'Ú':'U'}, regex=True)
    archivo_presas['Nombre de presa'] = archivo_presas['Nombre de presa'].replace({r"\.,":","}, regex=True)
    for i in range(len(archivo_presas)):
        #print(archivo_presas.loc[i, "Nombre de presa"])
        archivo_presas.loc[i, "Nombre de presa"] = archivo_presas.loc[i, "Nombre de presa"].split(',')[0]
    l_df_presas.append(archivo_presas)
    print(contador, "/", len(l_archivos_presas))
    contador += 1

df_presas = pd.concat(l_df_presas).drop_duplicates().reset_index(drop=True)

#%%
df_presas