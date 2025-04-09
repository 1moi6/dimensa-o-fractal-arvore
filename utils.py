import numpy as np
from PIL import Image, ImageOps,ImageDraw


def completar_quadrado(imagem,fill):
    largura, altura = imagem.size
    lado = max(largura, altura)
    delta_larg = lado - largura
    delta_alt = lado - altura
    padding = (delta_larg // 2, delta_alt // 2, delta_larg - delta_larg // 2, delta_alt - delta_alt // 2)
    return ImageOps.expand(imagem, padding, fill=fill)

def contar_caixas_numpy(imagem, subdivisoes, limiar=128, modo='preto'):
    """
    Contagem de caixas otimizada com NumPy puro.

    Parâmetros:
        imagem: PIL.Image em tons de cinza
        subdivisoes: lista de subdivisões do lado (ex: [2, 4, 8, 16])
        limiar: valor de corte
        modo: 'preto' ou 'branco'

    Retorna:
        tam_caixa: lista com tamanhos das caixas
        num_caixas: lista com número de caixas com estrutura
    """
    img_gray = imagem.convert('L')
    matriz = np.array(img_gray)
    altura, largura = matriz.shape

    tam_caixa = []
    num_caixas = []

    cnt = 1
    for s in subdivisoes:
        cnt += 1
        box_h = altura // s
        box_w = largura // s

        # Corta a imagem para múltiplo exato da caixa
        matriz_cortada = matriz[:box_h * s, :box_w * s]

        # Binarização
        if modo == 'preto':
            binaria = matriz_cortada < limiar
        else:
            binaria = matriz_cortada > limiar

        # Reshape para (s, box_h, s, box_w)
        reshaped = binaria.reshape(s, box_h, s, box_w)
        reshaped = reshaped.transpose(0, 2, 1, 3)  # (s, s, box_h, box_w)

        # Verifica se cada bloco tem algum pixel True
        presenca = np.any(reshaped, axis=(2, 3))
        count = np.sum(presenca)

        tam_caixa.append(largura / s)
        num_caixas.append(count)

    return tam_caixa, num_caixas

def preencher_caixas_ativas(imagem, tamanho_caixa, limiar=128, modo='preto', cor=(255, 0, 0, 128)):
    """
    Preenche as caixas que contêm estrutura com uma cor sólida (ou semitransparente).

    Parâmetros:
        imagem: PIL.Image em tons de cinza ou RGB
        tamanho_caixa: lado da caixa (em pixels)
        limiar: valor de corte para binarização
        modo: 'preto' (pixels < limiar) ou 'branco' (pixels > limiar)
        cor: tupla RGBA (ex: vermelho semitransparente = (255, 0, 0, 128))

    Retorna:
        imagem com sobreposição das caixas preenchidas
    """
    img_gray = imagem.convert('L')
    if modo == 'preto':
        imagem = completar_quadrado(img_gray,0)
        matriz = np.array(imagem)
        binaria = np.where(matriz < limiar, 1, 0)
    else:
        imagem = completar_quadrado(img_gray,0)
        matriz = np.array(imagem)
        binaria = np.where(matriz > limiar, 1, 0)

    largura, altura = imagem.size
    img_rgb = imagem.convert('RGBA')
    overlay = Image.new('RGBA', img_rgb.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    n_cheias = 0
    total = 0

    for x in range(0, largura - tamanho_caixa + 1, tamanho_caixa):
        for y in range(0, altura - tamanho_caixa + 1, tamanho_caixa):
            bloco = binaria[y:y+tamanho_caixa, x:x+tamanho_caixa]
            total += 1
            if np.any(bloco):
                n_cheias += 1
                draw.rectangle(
                    [x, y, x + tamanho_caixa - 1, y + tamanho_caixa - 1],
                    fill=cor
                )

    imagem_com_caixas = Image.alpha_composite(img_rgb, overlay)
    return imagem_com_caixas.convert('RGB'), n_cheias,total


def corte(imagem, valor, tipo):
    imagem = imagem.convert('L')
    if tipo == 'M':
        imagem = completar_quadrado(imagem,0)
        matriz_tons_de_cinza = np.array(imagem)
        matriz_filtrada = np.where(matriz_tons_de_cinza < valor, 255, 0)
    else:
        imagem = completar_quadrado(imagem,0)
        matriz_tons_de_cinza = np.array(imagem)
        matriz_filtrada = np.where(matriz_tons_de_cinza > valor, 255, 0)
    return Image.fromarray(matriz_filtrada.astype(np.uint8))
