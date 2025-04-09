import streamlit as st
import numpy as np
from PIL import Image
import altair as alt
from utils import corte, contar_caixas_numpy, preencher_caixas_ativas
import pandas as pd


st.set_page_config(page_title="Dimensão Fractal")
# st.logo("./assets/images/ialogo.png", icon_image="./assets/images/ialogo2.png")


if 'df_b' not in st.session_state:
    st.session_state.df_b = None
if 'df_p' not in st.session_state:
    st.session_state.df_p = None

if 'imagem' not in st.session_state:
    st.session_state.imagem = None

if 'imagem_cheia' not in st.session_state:
    st.session_state.imagem_cheia = [None,None]


def load_css(file_name: str):
    """Função para carregar CSS externo e aplicá-lo no Streamlit."""
    with open(file_name, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


load_css("styles.css")

if 'labels' not in st.session_state:
    st.session_state.labels = [None, None]

def callback():
    st.session_state.df_b = None
    st.session_state.df_p = None
    st.session_state.labels = [None, None]
    st.session_state.imagem_cheia = [None,None]
    pass



def calcular_dimensao_fractal(imagem,label,limiar):
    largura, altura = imagem.size
    dados = {}
    cnt = 1
    if label == 'branco':
        subdivs = np.geomspace(largura/4,largura, num=100, dtype=int)
        tam_lados, num_caixas = contar_caixas_numpy(imagem, subdivs, limiar=limiar, modo='branco')
        log_inv_eps = np.log(subdivs) 
        log_N = np.log(num_caixas)
        coef, _ = np.polyfit(log_inv_eps, log_N, 1)

        st.session_state.df_b = coef
        st.session_state.dado_b = pd.DataFrame({
            "x": subdivs,
            "y": num_caixas,
            "x_log": np.log(subdivs),
            "y_log": np.log(num_caixas)
        })
        return coef
    else:
        subdivs = np.geomspace(largura/4,largura, num=100, dtype=int)
        tam_lados, num_caixas = contar_caixas_numpy(imagem, subdivs, limiar=limiar, modo='preto')
        log_inv_eps = np.log(subdivs) 
        log_N = np.log(num_caixas)
        coef, _ = np.polyfit(log_inv_eps, log_N, 1)

        st.session_state.df_p = coef
        st.session_state.dado_p = pd.DataFrame({
            "x": subdivs,
            "y": num_caixas,
            "x_log": np.log(subdivs),
            "y_log": np.log(num_caixas)
        })
        return coef
    
def dim_frac():
    imagem_pb_branco = corte(st.session_state.imagem, st.session_state.valor_corte, 'M')
    calcular_dimensao_fractal(imagem_pb_branco, 'branco',st.session_state.valor_corte)
    imagem_pb_preto = corte(st.session_state.imagem, st.session_state.valor_corte, 'm')
    calcular_dimensao_fractal(imagem_pb_preto, 'preto',st.session_state.valor_corte)

def calback_cc():
    num_div = st.session_state.tam_caixa
    img_com_branca,n_cheias_b,total_b = preencher_caixas_ativas(st.session_state.imagem, tamanho_caixa=num_div, limiar=st.session_state.valor_corte, modo='branco')
    img_com_preto,n_cheias_p,total_p = preencher_caixas_ativas(st.session_state.imagem, tamanho_caixa=num_div, limiar=st.session_state.valor_corte, modo='preto')
    st.session_state.imagem_cheia = [img_com_branca,img_com_preto]
    st.session_state.labels = [f"Número de caixa cheias: {n_cheias_b}. \n\nTotal de caixas: {total_b} caixas", f"Número de caixa cheias: {n_cheias_p}. \n\nTotal de caixas: {total_p} caixas"]
    pass

def main():
    caption_text_preto = "Ramificação em preto"
    caption_text_branco = "Ramificação em branco"
    st.markdown(f"\n<h5 style='text-align: center;'>Dimensão Fractal de Ramificações de Árvores</h5>",
                unsafe_allow_html=True)
    st.sidebar.header("Parâmentros e configurações")
    imagens_exemplo = {"Árvore 1": "image2.png",
                       "Árvore 2": "image6.png", "Árvore 3": "image8.png"}
    opcao = st.sidebar.selectbox("Escolha uma imagem de exemplo:", list(
        imagens_exemplo.keys()), on_change=callback)

    arquivo = st.sidebar.file_uploader(
        "Carregue sua imagem:", type=["png", "jpg", "jpeg"], on_change=callback)
    if arquivo:
        st.session_state.imagem = Image.open(arquivo)
    else:
        caminho = imagens_exemplo[opcao]
        st.session_state.imagem= Image.open(f"./imagens/{caminho}")


    if st.session_state.imagem:
        conttg = st.sidebar.container(border=True)
        conttg2 = st.sidebar.container(border=True)
        valor_corte = conttg.slider(
        "Ajuste o valor de corte para P&B: ", 0, 255, 20, key='valor_corte', on_change=callback)
        # on = conttg.toggle("Ver imagens em linhas", value=False, key="toggle")

        # conttg2.divider()
        opcao = conttg2.radio('Selecion:',['Dimensão fractal','Contagem de caixas'],label_visibility="hidden")
        
        if opcao=='Dimensão fractal':
            conttg2.button("Calcular dimensão fractal", use_container_width=True, on_click=dim_frac)
            

            if "df_p" in st.session_state and st.session_state.df_p is not None:
                caption_text_preto += f"\n\nDimensão fractal: {st.session_state.df_p:.4f}"

            if "df_b" in st.session_state and st.session_state.df_b is not None:
                caption_text_branco += f"\n\nDimensão fractal: {st.session_state.df_b:.4f}"

            # if st.session_state.toggle:
            if False:
                cols = st.columns([0.2, 0.6, 0.2])
                show_image = conttg.radio('Visualizar image: ', [
                                        'Original', 'Ramificação em preto', 'Ramificação em branco'])
                if show_image == 'Original':
                    cols[1].image(st.session_state.imagem, caption="Imagem original",
                                use_container_width=True)
                elif show_image == 'Ramificação em preto':
                    cols[1].image(corte(st.session_state.imagem, valor_corte, 'M'),
                                caption=caption_text_preto, use_container_width=True)
                else:
                    # imagem_pb_branco = corte(st.session_state.imagem, valor_corte, 'M')
                    cols[1].image(corte(st.session_state.imagem, valor_corte, 'm'),
                                caption=caption_text_branco, use_container_width=True)

            else:
                cols = st.container(border=True).columns(3)
                cols[0].image(st.session_state.imagem, caption="Imagem original",
                            use_container_width=True)

                cols[1].image(corte(st.session_state.imagem, valor_corte, 'M'),
                            caption=caption_text_preto, use_container_width=True)
                cols[2].image(corte(st.session_state.imagem, valor_corte, 'm'),
                            caption=caption_text_branco, use_container_width=True)

            if st.session_state.df_p:
                cont1 = st.container(border=True)
                cont1.markdown(f"\n<h6 style='text-align: center;'> Gráficos com dados do algoritmo de Contagem de Caixas</h6>",
                            unsafe_allow_html=True)
                cont2 = st.container(border=True)
                cont2.markdown(f"\n<h6 style='text-align: center;'> Tabela com dados do algoritmo de Contagem de Caixas</h6>",
                            unsafe_allow_html=True)
                cols2 = cont1.columns(2)
                cols3 = cont2.columns(2)

                st.sidebar.markdown(
                    f"**Dimensão fractal da ramificação em preto:** {st.session_state.df_p:.4f}")
                chart = alt.Chart(st.session_state.dado_p).mark_line(strokeDash=[5, 2],  # Linha tracejada
                                                                    color="blue").encode(
                    x=alt.X("x_log", title="Log da número de divisões"),
                    y=alt.Y("y_log", title="Log do número de caixas com pixel preto",scale=alt.Scale(zero=False)),
                    tooltip=[alt.Tooltip("x", title="r: "), alt.Tooltip("y", title="N: "), alt.Tooltip("x_log", title="Log(r): "), alt.Tooltip("y_log", title="Log(N)"),
                            alt.Tooltip(
                                "y_log", title="Log do número de caixas com pixel preto"),
                            ]
                ).properties(height=400,
                            title=alt.TitleParams(
                                text="Ramificação em preto",
                                anchor="middle"  # Centraliza o título
                            )
                            )

                pontos = alt.Chart(st.session_state.dado_p).mark_point(
                    size=100,  # Tamanho dos pontos
                    color="white",
                    stroke="red",  # Borda vermelha
                    strokeWidth=2  # Espessura da borda
                ).encode(
                    x="x_log",
                    y="y_log"
                )

                chart = chart + pontos

                cols2[0].altair_chart(
                    chart, use_container_width=True)

                cols3[0].dataframe(st.session_state.dado_b.rename(columns={"x": "No de divisões (x)", "y": "No de caixas não vazias (N)","x_log":"Log(x)", "y_log": "Log(N)" }),hide_index=True)

            if st.session_state.df_b:

                st.sidebar.markdown(
                    f"**Dimensão fractal da ramificação em branco:** {st.session_state.df_b:.4f}")

                chart = alt.Chart(st.session_state.dado_b).mark_line(
                    strokeDash=[5, 2],  # Linha tracejada
                    color="blue"
                ).encode(
                    x=alt.X("x_log", title="Log do número de divisões"),
                    y=alt.Y("y_log", title="Log do número de caixas com pixel branco",scale=alt.Scale(zero=False)),
                    tooltip=[
                        alt.Tooltip("x", title="r: "),
                        alt.Tooltip("y", title="N: "),
                        alt.Tooltip("x_log", title="Log(r): "),
                        alt.Tooltip("y_log", title="Log(N)")
                    ]
                ).properties(
                        height=400,
                        title=alt.TitleParams(
                            text="Ramificação em branco",
                            anchor="middle"  # Centraliza o título
                        )
                    )

                pontos = alt.Chart(st.session_state.dado_b).mark_point(
                    size=100,  # Tamanho dos pontos
                    color="white",
                    stroke="red",  # Borda vermelha
                    strokeWidth=2  # Espessura da borda
                ).encode(
                    x="x_log",
                    y="y_log"
                )

                chart = chart + pontos

                # Exibir gráfico no Streamlit
                cols2[1].altair_chart(
                    chart, use_container_width=True)

                cols3[1].dataframe(st.session_state.dado_b.rename(columns={"x": "No de divisões (x)", "y": "No de caixas não vazias (N)","x_log":"Log(x)", "y_log": "Log(N)" }),hide_index=True)
        else:
            conttg2.number_input('Tamanho da caixa em pixels:',min_value=1,max_value=max(st.session_state.imagem.size),value=10,key='tam_caixa')
            conttg2.button("Contar caixas", use_container_width=True,on_click=calback_cc)
            cols = st.container(border=True).columns(2)
            if st.session_state.imagem_cheia[0] and st.session_state.imagem_cheia[1]:
                cols[0].image(st.session_state.imagem_cheia[0],caption=st.session_state.labels[0])
                cols[1].image(st.session_state.imagem_cheia[1],caption=st.session_state.labels[1])
            else:
                cols[0].image(corte(st.session_state.imagem, valor_corte, 'm'),
                            caption=caption_text_preto, use_container_width=True)
                cols[1].image(corte(st.session_state.imagem, valor_corte, 'M'),
                            caption=caption_text_branco, use_container_width=True)
                


if __name__ == "__main__":
    main()
