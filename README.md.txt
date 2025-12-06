Alquimia do Vinho – Sistema Inteligente de Análise e Recomendação Enológica.

Integrante: Leandro Silva da Luz Oliveira. Turma: 41. Unidade Santo Amaro Disciplina: Ciência da Computação. RA: 2224107994

O Alquimia do Vinho é uma aplicação Full Stack que une a tradição da enologia com a precisão da Inteligência Artificial.

Links de Acesso:

Repositório (Código Fonte): https://github.com/leandroluz2017/alquimia-do-vinho

Vídeo de Apresentação

O vídeo demonstrará:

Estrutura do projeto

Explicação do modelo

Como treinar e rodar

Demonstração no Streamlit

Explicação dos gráficos

Resultados e conclusão

Aplicação Online (Deploy): https://alquimia-do-vinho.streamlit.app

2. RESUMO TÉCNICO
O projeto consiste no desenvolvimento de uma aplicação Full Stack em Python voltada para o mercado de vinhos, que integra técnicas de Machine Learning (Aprendizado de Máquina) e Sistemas de Recomendação (IA Clássica).

A solução foi construída do zero, sem a utilização de plataformas de chatbot pré-prontas (wrappers de GPT), focando na implementação de algoritmos próprios de classificação e lógica de negócios.

Funcionalidades Desenvolvidas:
Módulo de Machine Learning (Analista IA): Treinamento de um modelo Random Forest Classifier utilizando a biblioteca Scikit-Learn. O modelo foi treinado com um dataset físico-químico real, capaz de prever a qualidade do vinho (Ruim, Médio, Bom) com base em 11 variáveis (acidez, álcool, sulfatos, etc.).

Sistema de Recomendação (IA Clássica): Implementação de um motor de busca especialista baseado em regras e pesos ponderados, que cruza o perfil do usuário (país, harmonização, preço) com uma base curada de rótulos.

Web Scraping & Real-Time Data: Integração com o buscador DuckDuckGo via Python para criação de um "Radar de Tendências", permitindo monitoramento do mercado em tempo real sem dependência de bancos de dados estáticos.

Interface Interativa: Desenvolvimento de Front-end em Streamlit, garantindo usabilidade e visualização de dados.

3. TECNOLOGIAS E BIBLIOTECAS APLICADAS
Para atingir a complexidade exigida, foram utilizadas as seguintes ferramentas do ecossistema Python:

Linguagem: Python 3.10

Machine Learning: Scikit-Learn (Treino, Teste e Validação do Modelo)

Manipulação de Dados: Pandas e NumPy

Visualização de Dados: Matplotlib e Seaborn (Geração de Heatmaps e Matrizes de Confusão)

Web Framework: Streamlit

Busca Semântica: DuckDuckGo Search API

Deploy/Infraestrutura: Git, GitHub e Streamlit Cloud

Estrutura do projeto.

Alquimia-do-Vinho/
│
├── app.py                 # 🖥️ Aplicação Principal (Interface Streamlit)
├── train.py               # 🧠 Treina a IA e Gera os Gráficos
├── requirements.txt       # 📦 Lista de bibliotecas necessárias
├── winequality-red.csv    # 📊 Dataset (Base de dados original)
├── README.md              # 📖 Documentação do Projeto
│
├── graficos/              # 📈 Gráficos gerados pelo treinamento
│   ├── 1_boxplot.png
│   ├── 2_heatmap.png
│   └── 3_matriz_confusao.png
│
└── models/ (Opcional - ou na raiz)
    ├── modelo_vinho.pkl   # O cérebro da IA (Salvo)
    └── scaler.pkl         # O calibrador de dados (Salvo)

4. JUSTIFICATIVA DE COMPLEXIDADE
O projeto atende aos requisitos de complexidade compatível com 3 meses de trabalho, pois envolveu o ciclo completo de ciência de dados e engenharia de software:

Coleta e Tratamento de Dados (ETL): Limpeza do dataset winequality-red.csv.

Treinamento de Modelo: Separação de arquivos de treino (train.py) e aplicação (app.py), garantindo boas práticas de arquitetura.

Persistência de Objetos: Uso de joblib para salvar o modelo treinado (.pkl) e o escalonador (scaler), permitindo que a IA funcione em produção.


Integração Web: Desenvolvimento de interface gráfica para tornar a IA acessível ao usuário final.

