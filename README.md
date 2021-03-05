# NOVO DIRETÓRIO DO DASHBOARD DO RIO GRANDE DO SUL

# Follow Up
- 04/05/2021: reorganização da pasta do projeto, centralização das rotinas em um único arquivo controlador, estruturação dos scripts em conteido de processos/bots.
- 05/05/2021: conexão com BigQuery para aumentar performance do DataStudio


# Tecnologias envolvidas
- Python e Django (apenas o ORM para manipular o banco)
- Mysql para dados brutos a serem trabalhados nos scripts de agregação
- BigQuery para armazenamento das informações agregadas e disponibilização na ferramenta de BI
- DataStudio pra criar as visões de BI

# Implantação
### Rodar uma vez previamente antes de iniciar as rotinas
- 01: carregar as escolas, usando o `botCarregarEscolas`
- 02: carregar os alunos, usando o `botCarregarAlunos`
- 03: carregar os professores, usando o `botCarregarProfessores`
- 04: alimentar a o banco de acessos dos alunos, usando o `botCarregarAcessosProfessores`
- 05: alimentar a o banco de acessos dos professores, usando o `botCarregarAcessosAlunos`

### Rotinas
- 01: agendar execução dos `botCarregarAcessosProfessores` e `botCarregarAcessosAlunos` para todos os dias baixar os acessos/logins do dia anterior
- 02: agendar execução dos `botCarregarAlunos` e `botCarregarProfessores` para todos os dias atualizar os dados dos usuários no banco

### Rotinas de agregação
- 01: agendar execução para todos os domingos de `botAgregacaoProfessores` e `botAgregacaoAlunos`