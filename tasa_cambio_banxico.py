#%%
import pandas as pd
from datetime import datetime
import requests
import json
from datetime import timedelta

####################################################################################
#Lista para almacenar las fechas y los numeros que representan cada dia:
l_fechas, l_dia_semana, fecha_valor = [], [], []

dias_antes = 4

#La variable fecha almacena el valor de la fecha actual (la que el sistema marca) mediante el método now() y con date() toma los datos 
#AAA-MM-DD, después con el método strftime() se le da formato a AAAA/MM/DD.
rango_fechas_columna = pd.date_range(start=(datetime.today()+timedelta(days=-dias_antes+1)).date(),end=datetime.today())
l_fechas_columna = [l.date().strftime('%Y/%m/%d') for l in rango_fechas_columna]

#Se itera n veces para almacenar las fechas de n dias anteriores al dia actual:
for i in range(1,dias_antes):
    l_fechas.append((datetime.today()+timedelta(days=-i)).date())
l_fechas.reverse()
l_fechas.append((datetime.today()+timedelta(days=-0)).date())

#dias_semana = {"Lunes":"0", "Martes":"1", "Miercoles":"2", "Jueves":"3", "Viernes":"4", "Sabado":"5", "Domingo":"6"}
#En otra lista se almacena el numero de cada dia de la semana
for j in range(dias_antes):
    l_dia_semana.append(l_fechas[j].weekday())

#Si el dia es sabado se le resta uno y si es domingo. Esto para obtener los datos del dia viernes para cuando sea sabado o domingo:
for k in range(dias_antes):
    if l_dia_semana[k] == 5:
        l_fechas[k] = l_fechas[k] + timedelta(days=-1)
    if l_dia_semana[k] == 6:
        l_fechas[k] = l_fechas[k] + timedelta(days=-2)
#####################################################################################

#h es un diccionario que contiene paramétros para la petición:
h = {
        "GET" : "/SieAPIRest/service/v1/series/SF43783/datos/oportuno HTTP/1.1",
        "Accept": "application/json",
        "Bmx-Token": "3985f2055172da5eb115528410403d9c2685bd6c2e2db5955c947824c5cab583",
        "Accept-Encoding": "gzip"
    }

for f in l_fechas:
    try:
    #se realiza la petición mediante request.get()
        url = f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/{f}/{f}'
        respuesta = requests.get(url,headers=h)
        respuesta_xml = respuesta.text

        #La respuesta se pasa a formato JSON mediante el módulo json y el método loads()
        #Además se accede a los valores de fecha y tasa de cambio mediante los valores de los diccionarios anidados:
        res_json=json.loads(respuesta_xml)
        fecha_valor.append(list(list(list(list(res_json.values())[0].values())[0][0].values())[-1][0].values()))
    except AttributeError:
        print(f"\nEs posible que aún no se haya publicado el valor de la tasa de cambio para el día: {f}.\n")
        fecha_valor.append(['-','-'])
        if f == l_fechas[-1]:
            print(f'\nDía y hora actual: {datetime.today()}')
            print(f"Consultar después de las 12:00 p.m\n")
        pass

#Lista para almacenar 24 veces el valor de la tasa de cambio:
fecha, tc, pml_dll = [],[],[]
if len(fecha_valor)!= 0:
    for i in range(len(fecha_valor)):
        #for j in range(24):
        fecha.append(fecha_valor[i][0])
        tc.append(fecha_valor[i][1])

    #Se crea un dataframe con el nombre de las columnas y otro con los valores:
    columnas_tc = pd.DataFrame(columns=['Fecha','Tasa de cambio'])
    valores_df = pd.DataFrame({'Fecha':l_fechas_columna, 'Tasa de cambio':tc})
    #Se concatenan los dataframes e imprime:
    tasa_cambio = pd.concat([columnas_tc, valores_df])

tasa_cambio.to_csv('C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Archivos_regulus\\Cenace\\Web scraping\\tasa_cambio_banxico.csv')
# %%
