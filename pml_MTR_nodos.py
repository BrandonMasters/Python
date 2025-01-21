#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import os
from datetime import datetime
from selenium.webdriver.common.keys import Keys

#Instancia de la clase ChromeOptions:
opciones = Options()

#Directorio en donde se descargaran los archivos:
directorio = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Web scraping\\Precios energia MTR\\'
#Lee la carpeta donde se encuentran los archivos descargados & cambia de directorio para leerlos & realizar los filtros de los nodos indicados:
os.chdir(directorio)

#Modifica las opciones de CHROME:
preferencias = {"download.default_directory": f"{directorio}",
                   "download.prompt_for_download": False,
                   "directory_upgrade": True,
                   "safebrowsing.enabled": True,
                   "behavior":"allow"}

opciones.add_experimental_option('prefs', preferencias)
opciones.add_argument("start-maximized")
driver = webdriver.Chrome(options=opciones)

#Petición get
url = "https://www.cenace.gob.mx/Paginas/SIM/Reportes/PreEnerServConMTR.aspx"
driver.get(url)

#Diccionarios y listas:
reportes = ['Precios Marginales Locales MTR', 'Precios en Nodos Distribuidos MTR']
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
reportes_sistemas = {'SIN':['Precios Marginales Locales MTR', 'Precios en Nodos Distribuidos MTR'], 'BCA':['Precios Marginales Locales MTR']}
nodosP = ["03POM-400","05MVC-115", "05CLI-115", "06LAA-138", "06RRD-138", "09LBR-230", "07IVY-230", "07OMS-230", "QUERETARO", "MONTERREY", "OBREGON", "CENTRO SUR"]
l_fechas, l_sistema, l_mercado, l_dataframes = [],[],[],[]

#Fecha inicio y fecha fin:
rango_fechas = pd.date_range(start='2024/12/23', end='2024/12/27')
l_rango_fechas = [l for l in rango_fechas]

#Espera a que cargue la página y aparezca el cuadro donde se descargan los archivos:
WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/table/tbody/tr[1]/th[1]'), 'Día de Operación'))

#Comprueba si la fecha que se quiere descargar esté diponible:
for f in l_rango_fechas:
    if f > datetime.strptime(driver.find_element(By.XPATH, '/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/table/tbody/tr[2]/td[1]').text, '%d/%m/%Y'):
        l_rango_fechas.remove(f)

if len(l_rango_fechas) != 0:
    #Selecciona el tipo de reporte a descargar
    for sistema in reportes_sistemas:
        for reporte in reportes_sistemas[sistema]:

            #Realiza un scroll hasta arriba:
            driver.execute_script("window.scrollTo(0, document.body.scrollTop)")
            time.sleep(2)

            #Selección de reporte:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[1]/div/div[1]/div/select")))
            driver.find_element(By.XPATH, f"/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[1]/div/div[1]/div/select").click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[1]/div/div[1]/div/select/option[text()='{reporte}']")))
            driver.find_element(By.XPATH, f"/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[1]/div/div[1]/div/select/option[text()='{reporte}']").click()

            #Espera a que el nombre del tipo de reporte aparezca & continua con la selección (diario o mensual):
            WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.ID, 'ContentPlaceHolder1_lblNombreReporte'), f'{reporte}'))
            time.sleep(2)
            driver.find_element(By.XPATH, f"/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[1]/div/div[2]/div/select").click()
            driver.find_element(By.XPATH, f"/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[1]/div/div[2]/div/select/option[text()='Diaria']").click()

            #Selecciona el sistema (BCA, BCS o SIN)
            time.sleep(2)
            driver.find_element(By.XPATH, f"/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[1]/div/div[3]/div/select").click()
            driver.find_element(By.XPATH, f"/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[1]/div/div[3]/div/select/option[text()='{sistema}']").click()

            #Itera la lista de fechas:
            for valor in l_rango_fechas:
                
                #Espera hasta que el nombre del sistema por consultar esté presente:
                WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/table/tbody/tr[2]/td[2]'), f'{sistema}'))
                time.sleep(2)

                #Presiona el calendario y espera hasta que aparezca:
                driver.find_element(By.XPATH, '/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[1]/div/div[4]/input').click()
                WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]')))
                
                #Selecciona el año:
                time.sleep(2)
                driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[2]").click()
                driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[2]/option[text()='{str(valor.year)}']").click()

                #Selecciona el mes:
                time.sleep(2)
                driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]").click()
                driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]/option[text()='{meses[valor.month - 1]}']").click()

                #Va seleccionando los dias:
                for i in range(2):
                    time.sleep(2)
                    rows_table = driver.find_element(By.XPATH, f"//div[@class ='daterangepicker ltr show-calendar opensright']/div[@class='drp-calendar left']/div[@class='calendar-table']/table[@class='table-condensed']/tbody/tr/td[text() = '{str(valor.day)}' and not(contains(@class,'off'))]") #/tr[1]/td[@class = 'available' or @class = 'weekend available' or @class = 'weekend active start-date available']")
                    rows_table.click()

                #Presiona el botón aceptar para continuar con las descargas de los archivos:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/button[2]"))).click()
                WebDriverWait(driver,10).until_not(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]')))

                #Selecciona el icono de EXCEL y lo presiona
                WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/table/tbody/tr[2]/td[1]'), f'{datetime.strftime(valor, '%d/%m/%Y')}'))
                time.sleep(2)
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/table/tbody/tr[2]/td[4]/input"))).click()
                    print(f'{reporte}',datetime.strftime(valor, '%d/%m/%Y'),sistema)
                except:
                    print("No se ha logrado descargar el archivo: " ,f'{reporte}',datetime.strftime(valor, '%d/%m/%Y'),sistema)
else:
    print("No hay archivos disponibles para descargar, prueba otra fecha o rango de fechas")           
#Espera 5 segundos para terminar de descargar los ultimos archivos & continua con la ejecución del programa:         
time.sleep(5)

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

        if tipo_nodo == 'PreciosNodosDistrib':
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
pml_mda_fecha_hora_nodo.to_excel(f"pml_{mercado}_{pml_mda_fecha_hora['Fecha'].iloc[1]}_{pml_mda_fecha_hora['Fecha'].iloc[-1]}.xlsx")

#%%
rows_table.text