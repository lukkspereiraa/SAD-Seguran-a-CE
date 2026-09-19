# SAD - Sistema de Apoio à Decisão: Segurança Pública CE 🛡️

Dashboard analítico, modular e interativo desenvolvido para suporte à gestão tática e estratégica da Segurança Pública no estado do Ceará. O sistema cruza dados territoriais, temporais e sociais para identificar padrões de criminalidade (CVLI) e dinâmicas de apreensão de drogas (Entorpecentes).

## 🏗️ Arquitetura do Software (Modular / Domain-Driven Design)
O projeto aplica os princípios de responsabilidade única (SRP do SOLID) e conceitos de Domain-Driven Design (DDD) na organização de diretórios, separando a lógica de negócio, a interface gráfica e o roteamento de módulos.

* **`app.py`**: Ponto de orquestração principal (Router). Gerencia os filtros globais (Menu Lateral) e roteia a interface via `match/case` para o módulo correto.
* **`/views/`**: Camada de Controladores de Tela. Arquivos como `view_cvli.py` e `view_entorpecentes.py` que aplicam filtros específicos e invocam os gráficos do seu respectivo domínio.
* **`/components/`**: Camada de Visão (UI). Organizada em subpastas por domínio de negócio (`/cvli/` e `/entorpecentes/`), contendo os módulos isolados responsáveis pela renderização de cada gráfico com Plotly e Streamlit.
* **`/services/`**: Camada de Lógica e Dados (`data_handler.py`). Responsável pelo ETL (Extract, Transform, Load), unificação de datas e motor de filtragem de alta performance.
* **`/dataSett/`**: Camada de armazenamento estático (Bases de dados em Excel).

## 🚀 Como Executar Localmente

1. Garanta que possui o Python 3.9+ instalado.
2. Clone o repositório e acesse a pasta raiz do projeto.
3. Instale as dependências executando:
   `pip install -r requirements.txt`
4. Inicie o servidor do Streamlit:
   `streamlit run app.py`

## 📊 Principais Funcionalidades

### 🔴 Módulo CVLI (Crimes Contra a Vida)
- **Inteligência Geográfica:** Mapeamento coroplético renderizando as cidades do estado do Ceará e distribuição por AIS (Área Integrada de Segurança).
- **Hotspots Temporais:** Matriz de densidade e gráficos de linha isolando horários e dias críticos da semana.
- **Cruzamento de Perfis:** Micro-gestão tática através de filtros interligados por Tipificação Penal, Gênero, Arma, Idade e Escolaridade da vítima.

### 🟢 Módulo Entorpecentes (Tráfico de Drogas)
- **Mapeamento de Volume:** Análise quantitativa de drogas apreendidas (em Kg), isolando os municípios com maior incidência de tráfico.
- **Tipificação de Substâncias:** Distribuição gráfica identificando a proporção de apreensões por tipo (Maconha, Cocaína, Crack, etc.).
- **Evolução Temporal:** Monitoramento de picos de apreensões ao longo dos meses.

### ⚙️ Funcionalidades Globais
- **Mesclagem Inteligente de Dados (Data Lineage):** Capacidade de fundir os dataframes de múltiplos módulos no final do painel, gerando uma tabela unificada que injeta automaticamente uma coluna de rastreio ("Fonte dos Dados") para preservar a origem de cada registro sem perda de contexto.
- **Interface Padronizada:** Uso extensivo de iconografia nativa do Material Design do Google para uma interface limpa e corporativa.