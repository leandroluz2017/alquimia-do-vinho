import streamlit as st
import joblib
import numpy as np
from duckduckgo_search import DDGS
import os

st.set_page_config(
    page_title="Alquimia do Vinho",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stMetric { background-color: #f9f9f9; padding: 10px; border-radius: 10px; border-left: 5px solid #722F37; }
    .css-1button { width: 100%; }
    h1 { color: #722F37; font-family: 'Helvetica Neue', sans-serif; }
    h3 { color: #722F37; }
    [data-testid="stSidebar"] { background-color: #f7f7f7; }
    a { text-decoration: none; color: #722F37; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    model = joblib.load('modelo_vinho.pkl')
    scaler = joblib.load('scaler.pkl')
except FileNotFoundError:
    st.error("Erro: Arquivos do modelo não encontrados. Execute 'python train.py' primeiro.")
    st.stop()

DATABASE_VINHOS = [
    {"nome": "Catena Zapata Malbec Argentino", "pais": "Argentina", "ano": 2019, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Amadeirado", "preco": "Alto", "comida": ["Churrasco", "Carnes Vermelhas"], "desc": "Um dos melhores Malbecs do mundo. Intenso, luxuoso e pontuado."},
    {"nome": "Alamos Malbec", "pais": "Argentina", "ano": 2022, "corpo": "Médio", "tanino": "Médio", "sabor": "Frutado", "preco": "Baixo", "comida": ["Pizza", "Hambúrguer", "Dia a Dia"], "desc": "O clássico do dia a dia. Confiável e saboroso."},
    {"nome": "El Enemigo Cabernet Franc", "pais": "Argentina", "ano": 2019, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Especiarias", "preco": "Médio", "comida": ["Carnes Vermelhas", "Queijos Fortes"], "desc": "O queridinho dos críticos. Notas herbáceas e muita elegância."},
    {"nome": "Benjamin Nieto Senetiner", "pais": "Argentina", "ano": 2023, "corpo": "Leve", "tanino": "Suave", "sabor": "Frutado", "preco": "Baixo", "comida": ["Massas Leves", "Dia a Dia"], "desc": "Jovem, fácil de beber e muito barato. Ideal para iniciantes."},
    {"nome": "Cobos Bramare", "pais": "Argentina", "ano": 2018, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Doce/Geleia", "preco": "Alto", "comida": ["Bife Ancho", "Costela"], "desc": "Explosão de frutas maduras e chocolate. Quase uma sobremesa alcoólica."},
    {"nome": "DV Catena Cabernet-Malbec", "pais": "Argentina", "ano": 2020, "corpo": "Encorpado", "tanino": "Médio", "sabor": "Amadeirado", "preco": "Médio", "comida": ["Churrasco", "Jantar Especial"], "desc": "O vinho argentino mais famoso nos restaurantes brasileiros."},
    {"nome": "Don Melchor Cabernet Sauvignon", "pais": "Chile", "ano": 2018, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Amadeirado", "preco": "Alto", "comida": ["Cordeiro", "Carnes de Caça"], "desc": "Um ícone chileno premiado. Potente, complexo e elegante."},
    {"nome": "Casillero del Diablo Reserva", "pais": "Chile", "ano": 2021, "corpo": "Médio", "tanino": "Médio", "sabor": "Frutado", "preco": "Baixo", "comida": ["Massas", "Pizza"], "desc": "A lenda do vinho. O mais vendido e conhecido."},
    {"nome": "Purple Angel (Montes)", "pais": "Chile", "ano": 2019, "corpo": "Encorpado", "tanino": "Médio", "sabor": "Especiarias", "preco": "Alto", "comida": ["Porco", "Massas Pesadas"], "desc": "O melhor Carmenère do mundo. Notas de páprica e frutas azuis."},
    {"nome": "Cousiño Macul Antiguas Reservas", "pais": "Chile", "ano": 2020, "corpo": "Médio", "tanino": "Forte", "sabor": "Terroso", "preco": "Médio", "comida": ["Queijos", "Massas"], "desc": "Cabernet clássico, seco e sério. Ótimo custo-benefício."},
    {"nome": "Santa Helena Reservado", "pais": "Chile", "ano": 2023, "corpo": "Leve", "tanino": "Suave", "sabor": "Frutado", "preco": "Baixo", "comida": ["Dia a Dia", "Petiscos"], "desc": "Simples, barato e fácil de beber geladinho."},
    {"nome": "Almaviva", "pais": "Chile", "ano": 2017, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Amadeirado", "preco": "Alto", "comida": ["Alta Gastronomia"], "desc": "Parceria entre Baron Philippe de Rothschild e Concha y Toro. Luxo puro."},
    {"nome": "Miolo Lote 43", "pais": "Brasil", "ano": 2020, "corpo": "Encorpado", "tanino": "Médio", "sabor": "Amadeirado", "preco": "Médio", "comida": ["Churrasco", "Queijos Fortes"], "desc": "O orgulho da Serra Gaúcha. Merlot e Cabernet de guarda."},
    {"nome": "Salton Intenso Tannat", "pais": "Brasil", "ano": 2022, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Terroso", "preco": "Baixo", "comida": ["Feijoada", "Carnes Gordurosas"], "desc": "Rústico e intenso. A acidez perfeita para limpar gordura."},
    {"nome": "Casa Valduga Leopoldina Merlot", "pais": "Brasil", "ano": 2021, "corpo": "Médio", "tanino": "Suave", "sabor": "Frutado", "preco": "Médio", "comida": ["Massas", "Frango"], "desc": "Aveludado. O Merlot brasileiro é reconhecido mundialmente."},
    {"nome": "Guaspari Vista da Mata", "pais": "Brasil", "ano": 2018, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Amadeirado", "preco": "Alto", "comida": ["Alta Gastronomia"], "desc": "Vinho de colheita de inverno (São Paulo). Premiadíssimo."},
    {"nome": "Lidio Carraro Dádivas", "pais": "Brasil", "ano": 2021, "corpo": "Médio", "tanino": "Médio", "sabor": "Frutado", "preco": "Baixo", "comida": ["Pizza", "Hambúrguer"], "desc": "Jovem, alegre e sem madeira. Fruta pura no copo."},
    {"nome": "Garzón Reserva Tannat", "pais": "Uruguai", "ano": 2020, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Terroso", "preco": "Médio", "comida": ["Churrasco", "Cordeiro"], "desc": "O Tannat moderno: potente mas sem ser agressivo. Vinícola modelo."},
    {"nome": "Bouza Monte Vide Eu", "pais": "Uruguai", "ano": 2019, "corpo": "Encorpado", "tanino": "Médio", "sabor": "Amadeirado", "preco": "Alto", "comida": ["Jantar Especial"], "desc": "Um dos vinhos mais prestigiados do Uruguai. Blend complexo."},
    {"nome": "Pêra-Manca Tinto", "pais": "Portugal", "ano": 2015, "corpo": "Encorpado", "tanino": "Médio", "sabor": "Especiarias", "preco": "Alto", "comida": ["Bacalhau", "Cordeiro"], "desc": "Uma lenda do Alentejo. O vinho mais famoso e histórico de Portugal."},
    {"nome": "Periquita Original", "pais": "Portugal", "ano": 2022, "corpo": "Médio", "tanino": "Médio", "sabor": "Terroso", "preco": "Baixo", "comida": ["Dia a Dia", "Petiscos"], "desc": "O primeiro vinho engarrafado de Portugal. Vai bem com tudo."},
    {"nome": "Papa Figos", "pais": "Portugal", "ano": 2021, "corpo": "Encorpado", "tanino": "Médio", "sabor": "Frutado", "preco": "Médio", "comida": ["Carnes Vermelhas"], "desc": "Do Douro, mesma região do Porto. Intenso e gastronômico."},
    {"nome": "Porta 6", "pais": "Portugal", "ano": 2022, "corpo": "Médio", "tanino": "Suave", "sabor": "Doce/Geleia", "preco": "Baixo", "comida": ["Pizza", "Massas"], "desc": "Famoso pelo rótulo desenhado. Muito macio e fácil de beber."},
    {"nome": "Brunello di Montalcino", "pais": "Itália", "ano": 2017, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Terroso", "preco": "Alto", "comida": ["Risotos", "Trufas"], "desc": "O rei da Toscana. Seco, tânico e com incrível longevidade."},
    {"nome": "Primitivo di Manduria", "pais": "Itália", "ano": 2021, "corpo": "Encorpado", "tanino": "Suave", "sabor": "Doce/Geleia", "preco": "Médio", "comida": ["Queijos", "Sobremesas"], "desc": "Parece uma geleia de frutas negras. Taninos muito macios."},
    {"nome": "Chianti Classico", "pais": "Itália", "ano": 2020, "corpo": "Médio", "tanino": "Forte", "sabor": "Especiarias", "preco": "Médio", "comida": ["Massas", "Pizza"], "desc": "A acidez perfeita para cortar o molho de tomate da pizza."},
    {"nome": "Tignanello", "pais": "Itália", "ano": 2018, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Amadeirado", "preco": "Alto", "comida": ["Alta Gastronomia"], "desc": "O primeiro 'Super Toscano'. Favorito da realeza."},
    {"nome": "Château Margaux", "pais": "França", "ano": 2010, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Terroso", "preco": "Alto", "comida": ["Alta Gastronomia"], "desc": "Um Premier Grand Cru de Bordeaux. Experiência de vida."},
    {"nome": "Beaujolais Villages", "pais": "França", "ano": 2023, "corpo": "Leve", "tanino": "Suave", "sabor": "Frutado", "preco": "Médio", "comida": ["Queijos Leves", "Frango"], "desc": "A alegria engarrafada. Jovem, fresco e sem taninos."},
    {"nome": "Côtes du Rhône", "pais": "França", "ano": 2020, "corpo": "Médio", "tanino": "Médio", "sabor": "Especiarias", "preco": "Médio", "comida": ["Ensopados"], "desc": "Apimentado e rústico. O vinho clássico de bistrô."},
    {"nome": "Marqués de Riscal Reserva", "pais": "Espanha", "ano": 2018, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Amadeirado", "preco": "Médio", "comida": ["Presunto Ibérico"], "desc": "Um clássico de Rioja. Muita madeira, baunilha e coco."},
    {"nome": "Pata Negra Oro", "pais": "Espanha", "ano": 2020, "corpo": "Médio", "tanino": "Médio", "sabor": "Terroso", "preco": "Baixo", "comida": ["Petiscos", "Dia a Dia"], "desc": "O espanhol mais vendido nos mercados brasileiros."},
    {"nome": "Vega Sicilia Unico", "pais": "Espanha", "ano": 2012, "corpo": "Encorpado", "tanino": "Médio", "sabor": "Terroso", "preco": "Alto", "comida": ["Alta Gastronomia"], "desc": "O vinho mais prestigiado da Espanha. Mítico."},
    {"nome": "Opus One", "pais": "Estados Unidos", "ano": 2017, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Amadeirado", "preco": "Alto", "comida": ["Steak"], "desc": "O encontro de Napa Valley com Bordeaux. Luxo californiano."},
    {"nome": "Robert Mondavi Private Sel.", "pais": "Estados Unidos", "ano": 2020, "corpo": "Encorpado", "tanino": "Médio", "sabor": "Doce/Geleia", "preco": "Médio", "comida": ["Costelinha BBQ"], "desc": "Envelhecido em barris de Bourbon. Notas de caramelo."},
    {"nome": "Apothic Red", "pais": "Estados Unidos", "ano": 2021, "corpo": "Médio", "tanino": "Suave", "sabor": "Doce/Geleia", "preco": "Baixo", "comida": ["Hambúrguer", "Só beber"], "desc": "Blend suave, adocicado e muito popular entre jovens."},
    {"nome": "Kanonkop Kadette Pinotage", "pais": "África do Sul", "ano": 2021, "corpo": "Encorpado", "tanino": "Médio", "sabor": "Defumado/Café", "preco": "Médio", "comida": ["Churrasco", "Pizza"], "desc": "A uva típica da África do Sul. Notas de café e banana grelhada."},
    {"nome": "Nederburg Baronne", "pais": "África do Sul", "ano": 2022, "corpo": "Médio", "tanino": "Médio", "sabor": "Especiarias", "preco": "Baixo", "comida": ["Dia a Dia"], "desc": "Um clássico sul-africano. Cabernet com Shiraz."},
    {"nome": "Yellow Tail Shiraz", "pais": "Austrália", "ano": 2022, "corpo": "Médio", "tanino": "Suave", "sabor": "Frutado", "preco": "Baixo", "comida": ["Churrasco", "Dia a Dia"], "desc": "O vinho do canguru. Descomplicado, doce e frutado."},
    {"nome": "Penfolds Grange", "pais": "Austrália", "ano": 2016, "corpo": "Encorpado", "tanino": "Forte", "sabor": "Especiarias", "preco": "Alto", "comida": ["Carnes Exóticas"], "desc": "Patrimônio histórico da Austrália. Potência pura."},
    {"nome": "Cloudy Bay Pinot Noir", "pais": "Nova Zelândia", "ano": 2020, "corpo": "Leve", "tanino": "Suave", "sabor": "Terroso", "preco": "Alto", "comida": ["Peixes", "Cogumelos"], "desc": "Elegância pura. Um dos melhores Pinot Noirs fora da França."},
]

def recomendar_vinho_v2(pais, sabor, tanino_input, preco_input, comida_input):
    recomendacoes = []
    for vinho in DATABASE_VINHOS:
        pontos = 0
        if vinho['pais'] == pais: pontos += 3
        if vinho['sabor'] == sabor: pontos += 2
        if preco_input == "Não importa" or vinho['preco'] == preco_input: pontos += 2
        if comida_input in vinho['comida'] or "Dia a Dia" in vinho['comida']: pontos += 3
        
        match_tanino = False
        if tanino_input <= 3 and vinho['tanino'] == "Suave": match_tanino = True
        elif 4 <= tanino_input <= 7 and vinho['tanino'] == "Médio": match_tanino = True
        elif tanino_input >= 8 and vinho['tanino'] == "Forte": match_tanino = True
        if match_tanino: pontos += 1
        
        if pontos >= 5: 
            recomendacoes.append((vinho, pontos))
            
    recomendacoes.sort(key=lambda x: x[1], reverse=True)
    return [rec[0] for rec in recomendacoes]

def buscar_noticias(termo):
    try:
        results = DDGS().text(f"{termo} vinho", region='br-pt', max_results=6)
        return results
    except Exception as e:
        return []

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/wine-bottle--v1.png", width=100)
    
    st.markdown("""
        <div style="text-align: left; margin-top: -20px;">
            <h1 style="color: #722F37; font-size: 32px; margin-bottom: 0px; font-weight: 800;">Alquimia do Vinho</h1>
            <p style="color: #666; font-size: 14px; font-style: italic; margin-top: 5px; font-family: serif;">
                "A tradição milenar encontra a Inteligência Artificial"
            </p>
        </div>
        <hr style="border-top: 1px solid #ddd; margin-top: 20px;">
    """, unsafe_allow_html=True)
    
    st.info("💡 Dica: Navegue pelas abas acima para acessar as diferentes ferramentas do sistema.")
    st.write("**Versão:** 5.0 Ultimate")

st.markdown("""
    <h1 style='text-align: center; color: #722F37;'>🍷 Alquimia do Vinho</h1>
    <p style='text-align: center; color: gray; font-style: italic;'>O assistente enológico mais completo do mercado.</p>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🕵️ Encontrar Vinho", "🌐 Radar de Tendências", "🔬 Analista IA", "📚 Academy", "📊 Relatórios Técnicos"])

with tab1:
    st.header("Descubra seu próximo vinho")
    col_filtros1, col_filtros2 = st.columns(2)
    
    with col_filtros1:
        f_pais = st.selectbox("🌎 Região", [
            "Brasil", "Argentina", "Chile", "Uruguai", "Portugal", 
            "Itália", "França", "Espanha", "Estados Unidos", 
            "África do Sul", "Austrália", "Nova Zelândia"
        ])
        f_comida = st.selectbox("🍽️ Comida", ["Churrasco", "Pizza", "Massas", "Queijos", "Hambúrguer", "Bacalhau", "Só beber"])
        
    with col_filtros2:
        f_sabor = st.selectbox("🍓 Aroma", [
            "Frutado", "Amadeirado", "Especiarias", 
            "Terroso", "Doce/Geleia", "Defumado/Café"
        ])
        f_preco = st.radio("💰 Preço", ["Baixo", "Médio", "Alto", "Não importa"], horizontal=True)
        f_tanino = st.slider("👅 Tanino", 1, 10, 5)

    st.divider()
    resultados = recomendar_vinho_v2(f_pais, f_sabor, f_tanino, f_preco, f_comida)
    
    if resultados:
        st.success(f"Encontramos {len(resultados)} rótulo(s) perfeitos!")
        for vinho in resultados:
            with st.container():
                c1, c2, c3 = st.columns([1, 4, 2])
                with c1:
                    st.markdown(f"## {'💎' if vinho['preco'] == 'Alto' else '🏷️'}")
                with c2:
                    st.subheader(f"{vinho['nome']} ({vinho['ano']})")
                    st.caption(f"{vinho['pais']} | {vinho['corpo']} | {vinho['sabor']}")
                    st.write(vinho['desc'])
                with c3:
                    st.write("")
                    st.write("")
                    termo_busca = f"Comprar vinho {vinho['nome']} preço"
                    url_google = f"https://www.google.com/search?q={termo_busca.replace(' ', '+')}&tbm=shop"
                    st.link_button("🛒 Ver Preço Atual", url_google)
                st.markdown("---")
    else:
        st.warning("Nenhum vinho exato encontrado. Tente 'Não importa' no preço.")

with tab2:
    st.header("🌐 Radar de Tendências Enológicas")
    st.write("Acompanhe o que está acontecendo no mundo dos vinhos em tempo real.")
    
    termo_tendencia = st.text_input("Digite um assunto:", placeholder="Ex: Melhores tintos 2024, História do Malbec, Premiações...")
    
    if st.button("📡 Pesquisar Agora"):
        if termo_tendencia:
            st.info(f"🔍 Buscando tendências sobre: **'{termo_tendencia}'**...")
            
            with st.spinner('Decantando as informações da rede...'):
                noticias = buscar_noticias(termo_tendencia)
                
                if noticias:
                    st.markdown("### 📰 Últimas Notícias")
                    st.markdown("---")
                    for news in noticias:
                        st.markdown(f"### 🍷 {news['title']}")
                        st.caption(f"Fonte: Google News | Relevância: Alta")
                        st.markdown(f"_{news['body']}_")
                        st.link_button("Ler Artigo Completo ➜", news['href'])
                        st.markdown("---")
                else:
                    st.warning("Não encontramos resultados exatos. Tente termos mais simples.")
        else:
            st.error("Por favor, digite algum assunto antes de clicar.")

with tab3:
    st.header("Laboratório Químico")
    
    with st.form("form_ia"):
        c1, c2 = st.columns(2)
        with c1:
            alcohol = st.slider('Teor Alcoólico (%)', 8.0, 15.0, 11.0)
            sulphates = st.slider('Sulfatos', 0.3, 2.0, 0.65)
        with c2:
            volatile_acidity = st.slider('Acidez Volátil', 0.1, 1.6, 0.5)
            citric_acid = st.slider('Ácido Cítrico', 0.0, 1.0, 0.3)

        with st.expander("⚙️ Ajustar Detalhes Avançados"):
            fixed_acidity = st.number_input('Acidez Fixa', 4.0, 16.0, 8.5)
            residual_sugar = st.number_input('Açúcar Residual', 0.0, 16.0, 2.2)
            chlorides = st.number_input('Cloretos', 0.01, 0.6, 0.08)
            free_sulfur = st.number_input('Enxofre Livre', 1.0, 72.0, 16.0)
            total_sulfur = st.number_input('Enxofre Total', 6.0, 300.0, 45.0)
            density = st.number_input('Densidade', 0.990, 1.004, 0.996, format="%.4f")
            ph = st.number_input('pH', 2.7, 4.0, 3.3)
        
        submitted = st.form_submit_button("🧬 Processar Análise")

    if submitted:
        features = np.array([[fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
                              chlorides, free_sulfur, total_sulfur, density, ph,
                              sulphates, alcohol]])
        
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)
        resultado = prediction[0]
        
        st.divider()
        col_res1, col_res2 = st.columns([1, 2])
        
        with col_res1:
            if resultado == 'Bom':
                cor, txt, icon = "#2ecc71", "EXCELENTE", "🌟"
                st.balloons()
            elif resultado == 'Médio':
                cor, txt, icon = "#f1c40f", "REGULAR", "⚖️"
            else:
                cor, txt, icon = "#e74c3c", "RUIM", "🚩"
            
            st.markdown(f"""
                <div style="background-color: #262730; padding: 20px; border-radius: 10px; border: 1px solid #464b5f; text-align: center;">
                    <h4 style="color: white; margin:0;">Qualidade Prevista</h4>
                    <h1 style="color: {cor}; margin:0;">{txt}</h1>
                    <div style="font-size: 30px;">{icon}</div>
                </div>
            """, unsafe_allow_html=True)

        with col_res2:
            st.info("A IA analisou os componentes químicos e comparou com uma base de dados de vinhos testados.")

with tab4:
    st.header("📚 Wine Academy")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**Tanino**\n\nSensação de boca seca (adstringência). Vem da casca da uva.")
    with c2:
        st.warning("**Acidez Volátil**\n\nO cheiro de vinagre. Se estiver alto, o vinho está estragado.")
    with c3:
        st.success("**Corpo**\n\nO peso do vinho na boca (Água vs Leite vs Creme).")

with tab5:
    st.header("📊 Relatórios de Treinamento da IA")
    st.write("Estes gráficos mostram como o modelo aprendeu a classificar os vinhos durante a etapa de treinamento.")
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("1. Matriz de Confusão")
        st.caption("Mostra onde a IA acertou e errou.")
        if os.path.exists('graficos/3_matriz_confusao.png'):
            st.image('graficos/3_matriz_confusao.png')
        else:
            st.warning("Gráfico não encontrado. Rode 'train.py'.")

    with col_graf2:
        st.subheader("2. Correlação de Variáveis")
        st.caption("Mostra quais químicas influenciam mais.")
        if os.path.exists('graficos/2_heatmap.png'):
            st.image('graficos/2_heatmap.png')
        else:
            st.warning("Gráfico não encontrado. Rode 'train.py'.")

    st.divider()
    st.subheader("3. Distribuição de Álcool vs. Qualidade")
    if os.path.exists('graficos/1_boxplot.png'):
        st.image('graficos/1_boxplot.png')
    else:
        st.warning("Gráfico não encontrado. Rode 'train.py'.")