from pylib.mysql_banco import banco

db = banco("localhost","getedu","getedu00","dashboard_rs")


#// INCLUIR NO BANCO
params={}    
params["nome"] = '{}'.format("Professor Teste")
params["email"] = '{}'.format("email@email.com")
params["ultimoacesso"] = '{}'.format(123131)
params["id_gsuite"] = '{}'.format(123131)
db.tabela('professores').inserir(params)
db.executar()


#TODO ROTINA DE ATUALIZAÇÃO
params={}    
params["nome"] = '{}'.format("Professor Teste")
params["email"] = '{}'.format("email@email.com")
params["ultimoacesso"] = '{}'.format(123131)
# condicao = "tipo_grafico = '{}' ".format('Professores')
# db.tabela('professores').autalizar(condicao,params)
# db.executar()


