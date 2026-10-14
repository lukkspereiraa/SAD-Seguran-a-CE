# SAD - Sistema de Apoio à Decisão: Segurança Pública CE 🛡️

![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-success)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red)
![Data Science](https://img.shields.io/badge/Data_Science-Plotly_%7C_Pandas-orange)

## 🎯 Propósito do Sistema

O **Sistema de Apoio à Decisão (SAD)** é uma plataforma analítica, modular e preditiva desenvolvida como Trabalho de Conclusão de Curso (TCC) em Engenharia/Ciência da Computação. O seu objetivo principal é fornecer **suporte à gestão tática e estratégica da Segurança Pública no estado do Ceará**. 

Através do processamento simultâneo de **13 bases de dados governamentais**, o sistema cruza variáveis territoriais, temporais e sociais para identificar padrões criminais, focos de vulnerabilidade e dinâmicas de operações de resgate. A plataforma transcende a análise descritiva, utilizando estatística inferencial para atuar como uma ferramenta de **Inteligência Criminológica e Preditiva**, auxiliando comandantes, delegados e assistentes sociais na alocação otimizada de recursos.

---

## 🏗️ Arquitetura do Software (Domain-Driven Design)

O projeto foi desenhado sob rigorosos padrões de engenharia de software, aplicando o princípio de responsabilidade única (SRP do SOLID), o Princípio DRY (*Don't Repeat Yourself*) e conceitos de *Domain-Driven Design* (DDD). A separação em camadas garante um código limpo, escalável e de alta performance.

*   **`app.py` (Camada de Roteamento):** Ponto de orquestração principal (Router). Gerencia os filtros globais de tempo e espaço, orquestrando a interface via `match/case` para 13 abas de domínio distintas. Permite a mesclagem final dos dados (Data Lineage) e exportação.
*   **`/views/` (Camada de Controladores):** Módulos intermediários (ex: `view_cvli.py`, `view_cvp.py`). Aplicam filtros de *drill-down* locais (ex: isolar faixa etária ou escolaridade) e invocam/injetam os gráficos do seu respetivo domínio tático.
*   **`/components/` (Camada de Visão/UI):** Organizada em subpastas por domínio de negócio, contendo os componentes isolados responsáveis pela renderização gráfica via **Plotly** e **Streamlit**. Utiliza Injeção de Dependências para partilhar gráficos de estrutura idêntica (ex: radares e matrizes) entre domínios com a mesma assinatura de dados.
*   **`/services/` (Camada de Lógica e Microsserviços):**
    *   `data_handler.py`: Responsável pelo processo de ETL (Extract, Transform, Load), limpeza automática de *strings* e carregamento paralelo das 13 bases de dados.
    *   `ibge.py`: Serviço de integração assíncrona que consome o GeoJSON do Ceará e a base populacional do Censo de 2022 em tempo real, calculando taxas precisas por 100 mil habitantes.
*   **`/dataSett/` (Camada de Dados):** Armazenamento local estático das bases em formato Excel (`.xlsx`).

---

## 📊 Ecossistema Analítico (13 Bases de Dados)

O sistema foi dividido em três eixos principais de atuação do Estado:

### 🚨 1. Eixo Criminal e Violência (Polícia Judiciária e Ostensiva)
*   **CVLI (Crimes Contra a Vida):** Cruzamento de perfis por tipificação penal, arma utilizada e dados demográficos da vítima.
*   **CVP (Roubos) e Furtos:** Análise comparativa do comportamento patrimonial, destacando a transição do crime de oportunidade (matutino) para o crime violento (noturno e rotas de trabalho).
*   **Entorpecentes e Armas de Fogo:** Mapeamento do volume de apreensões (Kg), tipificação de substâncias e cálculo de densidade de desarmamento tático.

### ⚖️ 2. Eixo de Vulnerabilidade e Direitos Humanos
*   **Crimes Sexuais:** Painéis com alertas automáticos do ECA (Estatuto da Criança e do Adolescente) focados na identificação de vítimas em idade de vulnerabilidade absoluta e cruzamento socioeconômico (Escolaridade x Raça).
*   **Maria da Penha, LGBTfobia e Racismo:** Mapeamento de crimes de ódio e intolerância, auxiliando a criação e alocação de delegacias especializadas.
*   **Povos Indígenas:** Monitorização estrita da violência contra populações originárias em territórios de demarcação (ex: Tapebas e Pitaguarys).

### 🚒 3. Eixo de Defesa Civil e Meio Ambiente (CBMCE e BPMA)
*   **Incêndios e Salvamento:** Mapeamento de manchas de calor e operações de resgate, correlacionando picos de temperatura diurnos e dinâmicas de acidentes domésticos.
*   **Animais:** Acompanhamento de ocorrências de maus-tratos e resgates ambientais.

---

## 🧠 Ciência de Dados Aplicada (Algoritmos)

Para além de ser um painel visual, o SAD incorpora ferramentas de IA e Estatística Avançada:

*   **Teorema de Pareto (Regra 80/20):** Cálculo acumulado em gráfico de duplo eixo que identifica matematicamente quais os Batalhões (AIS) que concentram a maioria das ocorrências, promovendo a otimização logística.
*   **Deteção de Anomalias (Z-Score):** Algoritmo que calcula a média móvel e o desvio padrão histórico, emitindo alertas visuais automáticos quando o volume diário de um evento rompe o "teto estatístico" (> 2 Desvios Padrão).
*   **Matriz de Probabilidade Condicional:** Transforma o volume de dados absolutos em percentagens de risco preditivo, estabelecendo a probabilidade matemática de um evento ocorrer num determinado turno, dado um dia específico da semana.

---

## ⚙️ Funcionalidades Executivas Globais

*   **Drill-Down Profundo:** Capacidade investigativa de isolar ocorrências cruzando simultaneamente Género, Raça, Escolaridade, Dia da Semana e Faixa Horária. O sistema recalcula mapas e métricas instantaneamente.
*   **Data Lineage e Unificação:** Mesclagem sob demanda dos 13 dataframes distintos num único relatório consolidado, injetando automaticamente a coluna de rastreio "Fonte dos Dados".
*   **Exportação em 1-Clique:** Geração instantânea de relatórios consolidados e limpos (sem metadados de sistema) em ficheiro `.csv` para download.

---

## 🚀 Como Executar Localmente

### Pré-requisitos
*   Python 3.9 ou superior instalado.
*   Gerenciador de pacotes `pip`.

### Instalação e Execução
1. Clone o repositório para a sua máquina local:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
2. Acesse a pasta raiz do projeto:
   ```bash
   cd seu-repositorio
   ```
3. Instale as dependências listadas:
   ```bash
   pip install -r requirements.txt
   ```
4. Inicie o servidor da aplicação:
   ```bash
   streamlit run app.py
   ```

*(O sistema abrirá automaticamente uma aba no seu navegador padrão em `http://localhost:8501`)*