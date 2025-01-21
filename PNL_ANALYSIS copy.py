#%%
#Importando módulos:
import pandas as pd
import os, warnings
warnings.filterwarnings('ignore')
import dateparser

#%%
#Con el módulo os, cambia de directorio y se coloca justo donde se encuentran los archivos a leer:
os.chdir('C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Data AMM\\POE\\')

#Crea una lista de las carpetas contenidas en el directorio actual, esto para después acceder a ellas:
MESES = [x for x in os.listdir(os.getcwd()) if not x.endswith('DS_Store')]
POE, LOAD = [], []

#De la lista de meses, va iterando cada carpeta y obtiene los datos de los archivos:
for m in MESES:
    try:
        os.chdir('C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Data AMM\\POE\\' + m)
        ficheros = [x for x in os.listdir(os.getcwd()) if x.endswith('.xlsx')]
        for f in ficheros:
            fecha = pd.Timestamp(dateparser.parse(f.split('.')[0]))
            poe = pd.read_excel(f, skiprows= 5, usecols=lambda x: 'Unnamed' not in x, sheet_name= 'POE')
            poe = poe.dropna() 
            poe.columns = [x.lstrip().rstrip() for x in poe.columns]
            for indx, row in poe.iterrows():
                POE.append({'Date': fecha + pd.DateOffset(hours = indx),'GENERADOR MARGINAL': row['GENERADOR MARGINAL'] , 'POE': row['POE (US$/MWh)']})
            
            load = pd.read_excel(f, skiprows= 5, sheet_name= 'Carga Horaria')
            load.drop(0, inplace = True)
            load.dropna(inplace = True)
            cols=load.columns[-5:]
            for indx, row in load.iterrows():
                hora = str(row[cols[-1]]).split('.')[0]
                minuto = str(row[cols[-1]]).split('.')[1]
                if minuto == '3':
                    minuto = int(30)
                else:
                    minuto = int(minuto)
                LOAD.append({'Date': fecha + pd.DateOffset(hours = int(hora) - 1) + pd.DateOffset(minutes = minuto), 'LOAD': row['Demanda SNI'], 'SER-I':row['SER-I']})
        print(m)
    except Exception as exc:
        print(exc, f)
#%%
try:
    POE = pd.DataFrame(POE).set_index('Date')
    LOAD = pd.DataFrame(LOAD).set_index('Date').resample('H').mean()

    POE.sort_index(inplace = True)
    LOAD.sort_index(inplace = True)

    if POE.shape[0] == LOAD.shape[0]:
        print(POE.shape, LOAD.shape, 'Same length')
        POE = POE.merge(LOAD, left_index=True, right_index=True)
    else:
        print('Something is wrong')
except Exception as exc:
    print(exc)

# %%
load = pd.read_excel(f, skiprows= 5, sheet_name= 'Carga Horaria')
# %%
POE
#%%
LOAD

# %%
POE.to_excel('C:\\Users\\regg6\\OneDrive - regulus.com.mx\\Documentos\\Data AMM\\dataframe_poe_abr_16_23_2024.xlsx')
# %%
