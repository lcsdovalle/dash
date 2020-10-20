import datetime
from pylib.pycsv import PyCsv



e_medio = PyCsv('escolas_ensino_medio').get_content()
emedio = {}
for item in e_medio:
    if item[0] not in emedio:
        emedio[item[0]] = item[0]

relatorio = PyCsv('relatorio_prof_emedio').get_content()

so_medio = PyCsv('escolas_medio_lista')

for linha in relatorio:
    if str(linha[1]) in emedio:
        linha
        so_medio.add_row_csv(linha)
    else:
        print(linha[1],"Não tem")