#%%
import datetime
import pandas as pd
from datetime import datetime
import os

fechas = pd.date_range(start='2024/01/01', end='2024/05/31')
l_fechas, l_horas = [],[]

for f in fechas:
    for i in range(24):
        l_fechas.append(f.date())
        l_horas.append(i+1)

df_fechas = pd.DataFrame({'Fechas':l_fechas, 'Hora':l_horas})
df_fechas.to_csv(f'Dataframe_fechas {l_fechas[0]}-{l_fechas[-1]}.csv')
print(df_fechas)
