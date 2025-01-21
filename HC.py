import pandas as pd
import os
from datetime import datetime
import demanda_real_balance
import requerimientos_sc

ro = requerimientos_sc.columnas['Fecha','Sistema','Hora','Reservas Operativas']
db = demanda_real_balance.df_demanda_real_b['Estimacion de Demanda por Balance (MWh)']