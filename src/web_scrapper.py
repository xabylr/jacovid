import pandas as pd
import matplotlib.pyplot as plt

import locale
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

url = 'http://www.juntadeandalucia.es/institutodeestadisticaycartografia/salud/static/resultadosProvincialesCovid.html?prov=29'

def get_malaga_pdia_14d():
    tables = pd.read_html(url, decimal=',', thousands='.', attrs = {'id': 'table_38676'})
    malaga_table = tables[0]

    malaga_pdia_14d = malaga_table.loc[malaga_table['Lugar de residencia'] == 'Málaga (capital)']['Tasa PDIA 14 días'].values[0]
    return f'{float(malaga_pdia_14d):n}'

if __name__ == '__main__':
    print(get_malaga_pdia_14d())