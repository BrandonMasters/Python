#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
from datetime import datetime

#Instancia de la clase ChromeOptions:
opciones = Options()

#Directorio en donde se descargaran los archivos:
directorio = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PML MDA MENSUAL\\'
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



#MERCADO MDA O MTR:
mercado = 'MTR'

#Petición get
url = f"https://www.cenace.gob.mx/Paginas/SIM/Reportes/PreEnerServCon{mercado}.aspx"
driver.get(url)

#Diccionarios y listas:
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
reportes_sistemas_MDA = {'SIN':[f'Precios en Nodos Distribuidos {mercado}'], 'BCA':[f'Precios Marginales Locales {mercado}', f'Precios en Nodos Distribuidos {mercado}'], 'BCS':[f'Precios Marginales Locales {mercado}', f'Precios en Nodos Distribuidos {mercado}']}
##reportes_sistemas_MDA = {'BCS':[f'Precios Marginales Locales {mercado}', f'Precios en Nodos Distribuidos {mercado}']}
l_fechas, l_sistema, l_mercado, l_dataframes = [],[],[],[]

#Fecha inicio & fin:
fecha_inicio = '2016/1/1'
fecha_fin = '2024/10/1'

#Fecha inicio y fecha fin:
rango_fechas = pd.date_range(start=fecha_inicio, end=datetime.strptime(fecha_fin,'%Y/%m/%d') + pd.DateOffset(months=1), freq='ME')
l_rango_fechas = [l for l in rango_fechas]

#Espera a que cargue la página y aparezca el cuadro donde se descargan los archivos:
WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/table/tbody/tr[1]/th[1]'), 'Día de Operación'))

#Comprueba si la fecha que se quiere descargar esté diponible:
time.sleep(2)
for f in l_rango_fechas:
    if f.date() > datetime.strptime(driver.find_element(By.XPATH, '/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/table/tbody/tr[2]/td[1]').text, '%d/%m/%Y').date():
        l_rango_fechas.remove(f)

if len(l_rango_fechas) != 0:
    #Selecciona el tipo de reporte a descargar
    for sistema in reportes_sistemas_MDA:
        for reporte in reportes_sistemas_MDA[sistema]:

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
            driver.find_element(By.XPATH, f"/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[1]/div/div[2]/div/select/option[text()='Mensual']").click()

            #Selecciona el sistema (BCA, BCS o SIN)
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/table/tbody/tr[1]/th[1]'), 'Periodo de Operación'))
            #time.sleep(2)
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
                
                try:
                    #Selecciona el año:
                    time.sleep(2)
                    driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[2]").click()
                    driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[2]/option[text()='{str(valor.year)}']").click()

                    #Selecciona el mes:
                    time.sleep(2)
                    driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]").click()
                    try:
                        if driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]/option[text()='{meses[valor.month - 1]}' and contains(@disabled, 'disabled')]"):
                            continue
                    except:
                        driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]/option[text()='{meses[valor.month - 1]}']").click()
                    
                    #Va seleccionando los dias:
                    for i in range(2):
                        time.sleep(2)
                        rows_table = driver.find_element(By.XPATH, f"//div[@class ='daterangepicker ltr show-calendar opensright']/div[@class='drp-calendar left']/div[@class='calendar-table']/table[@class='table-condensed']/tbody/tr/td[text() = '{str(valor.day)}' and not(contains(@class,'off'))]") #/tr[1]/td[@class = 'available' or @class = 'weekend available' or @class = 'weekend active start-date available']")
                        rows_table.click()
                except:
                    print("No se ha logrado seleccionar la fecha: ", valor.date())
                    continue

                #Presiona el botón aceptar para continuar con las descargas de los archivos:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/button[2]"))).click()
                WebDriverWait(driver,10).until_not(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]')))

                #Selecciona el icono de EXCEL y lo presiona
                print(str(f'{meses[valor.month - 1]} - {str(valor.year)}').upper())
                WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/table/tbody/tr[2]/td[1]'), str(f'{meses[valor.month - 1]} - {str(valor.year)}').upper()))
                time.sleep(2)
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/table/tbody/tr[2]/td[4]/input"))).click()
                    print(f'{reporte}',f'{meses[valor.month - 1]} - {str(valor.year)}',sistema)
                except:
                    print("No se ha logrado descargar el archivo 1: ", f'{meses[valor.month - 1]} - {str(valor.year)}',sistema)
                time.sleep(2)
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[4]/main/div/section[1]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/table/tbody/tr[3]/td[4]/input"))).click()
                    print(f'{reporte}',f'{meses[valor.month - 1]} - {str(valor.year)}',sistema)
                except:
                    print("No se ha logrado descargar el archivo 2: ", f'{meses[valor.month - 1]} - {str(valor.year)}',sistema)
else:
    print("No hay archivos disponibles para descargar, prueba otra fecha o rango de fechas")           
#%%
#Cambia el nombre del archivo y le coloca el Año al inicio:
import os
directorio = 'C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Historial PML MTR MENSUAL\\'
os.chdir(directorio)

ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.csv')]

for f in ficheros:
    #print(f.split()[5][1:])
    #print(directorio+f)
    os.rename(directorio+f, directorio+f.split()[5][1:]+" "+f)
 