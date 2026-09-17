# SAD - Sistema de Apoio à Decisão: Segurança Pública CE 🛡️

Dashboard analítico e interativo desenvolvido para suporte à gestão tática e estratégica da Segurança Pública no estado do Ceará. O sistema cruza dados territoriais, temporais e sociais para identificar padrões de criminalidade (CVLI) e intervenções policiais.

## 🏗️ Arquitetura do Software (Padrão MVC/Componentizado)
O projeto aplica os princípios de responsabilidade única (SOLID), separando a lógica de negócio da interface gráfica.

* **`/dataSett/`**: Camada de armazenamento estático (Base de dados consolidada).
* **`/services/`**: Camada de Controle/Lógica (`data_handler.py`). Responsável pelo tratamento do ETL (Extract, Transform, Load) e motor de filtragem.
* **`/components/`**: Camada de Visão (Views). Módulos isolados responsáveis pela renderização individual de cada gráfico ou mapa no Streamlit.
* **`app.py`**: Ponto de orquestração principal (Router).

## 🚀 Como Executar Localmente

1. Garanta que possui o Python 3.9+ instalado.
2. Clone o repositório e acesse a pasta raiz do projeto.
3. Instale as dependências executando:
   `pip install -r requirements.txt`
4. Inicie o servidor do Streamlit:
   `streamlit run app.py`

## 📊 Principais Funcionalidades
- **Inteligência Geográfica:** Mapeamento coroplético renderizando todas as 184 cidades do estado do Ceará (Absoluto ou por Taxa de 100k hab.).
- **Hotspots Temporais:** Matriz de densidade isolando horários e dias críticos da semana.
- **Micro-Gestão Tática:** Motor de filtros interligados por Tipificação Penal, Gênero, Arma, Idade e Escolaridade.