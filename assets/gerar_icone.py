"""
Gera assets/icon.ico: icone do Controle de Proventos (moeda dourada com
grafico de crescimento em verde), usado no executavel (build.spec) e no
instalador (proventos_setup.iss).

Uso: python assets/gerar_icone.py
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SUPERSAMPLE = 1024
CENTER = SUPERSAMPLE / 2
RAIO = SUPERSAMPLE * 0.46

VERDE_ESCURO = (13, 74, 51)
VERDE_CLARO = (34, 139, 92)
DOURADO_CLARO = (247, 223, 145)
DOURADO = (212, 175, 55)
DOURADO_ESCURO = (154, 120, 30)
BRANCO = (255, 255, 255)


def gerar_base_moeda():

    y, x = np.mgrid[0:SUPERSAMPLE, 0:SUPERSAMPLE]

    dx = (x - CENTER) - RAIO * 0.28
    dy = (y - CENTER) - RAIO * 0.28

    dist = np.sqrt(dx * dx + dy * dy) / RAIO
    dist = np.clip(dist, 0, 1)

    t = dist[..., None]

    cor = (
        np.array(VERDE_CLARO)[None, None, :] * (1 - t)
        + np.array(VERDE_ESCURO)[None, None, :] * t
    )

    dist_centro = np.sqrt(
        (x - CENTER) ** 2 + (y - CENTER) ** 2
    )

    alpha = np.where(dist_centro <= RAIO, 255, 0).astype(np.uint8)

    rgb = np.clip(cor, 0, 255).astype(np.uint8)

    base = np.dstack([rgb, alpha])

    return Image.fromarray(base, mode="RGBA")


def desenhar_anel_dourado(imagem):

    desenho = ImageDraw.Draw(imagem)

    espessura = SUPERSAMPLE * 0.028

    caixa_externa = [
        CENTER - RAIO, CENTER - RAIO,
        CENTER + RAIO, CENTER + RAIO,
    ]

    caixa_interna = [
        CENTER - RAIO + espessura, CENTER - RAIO + espessura,
        CENTER + RAIO - espessura, CENTER + RAIO - espessura,
    ]

    desenho.ellipse(caixa_externa, outline=DOURADO, width=int(espessura * 1.15))
    desenho.ellipse(caixa_interna, outline=DOURADO_ESCURO, width=int(espessura * 0.35))

    return imagem


def desenhar_grafico_crescimento(imagem):

    desenho = ImageDraw.Draw(imagem)

    n_barras = 4
    largura_barra = RAIO * 0.24
    espaco = RAIO * 0.10

    alturas = [0.30, 0.48, 0.68, 0.92]

    largura_total = n_barras * largura_barra + (n_barras - 1) * espaco
    x0 = CENTER - largura_total / 2

    base_y = CENTER + RAIO * 0.42

    pontos_topo = []

    for i, h in enumerate(alturas):

        altura_barra = RAIO * 0.85 * h

        x1 = x0 + i * (largura_barra + espaco)
        x2 = x1 + largura_barra

        y1 = base_y - altura_barra
        y2 = base_y

        raio_canto = largura_barra * 0.28

        cor_barra = DOURADO_CLARO if i == n_barras - 1 else DOURADO

        desenho.rounded_rectangle(
            [x1, y1, x2, y2],
            radius=raio_canto,
            fill=cor_barra,
        )

        pontos_topo.append(((x1 + x2) / 2, y1))

    # Seta ascendente ligando o topo das barras, reforcando "crescimento"
    largura_linha = int(SUPERSAMPLE * 0.018)

    inicio = (pontos_topo[0][0], pontos_topo[0][1] - RAIO * 0.10)
    fim = (pontos_topo[-1][0], pontos_topo[-1][1] - RAIO * 0.14)

    desenho.line([inicio, fim], fill=BRANCO, width=largura_linha, joint="curve")

    angulo = math.atan2(fim[1] - inicio[1], fim[0] - inicio[0])
    tamanho_ponta = RAIO * 0.16

    ponta_a = (
        fim[0] - tamanho_ponta * math.cos(angulo - math.radians(28)),
        fim[1] - tamanho_ponta * math.sin(angulo - math.radians(28)),
    )
    ponta_b = (
        fim[0] - tamanho_ponta * math.cos(angulo + math.radians(28)),
        fim[1] - tamanho_ponta * math.sin(angulo + math.radians(28)),
    )

    desenho.polygon([fim, ponta_a, ponta_b], fill=BRANCO)

    return imagem


def desenhar_brilho(imagem):

    brilho = Image.new("L", imagem.size, 0)
    desenho = ImageDraw.Draw(brilho)

    desenho.ellipse(
        [
            CENTER - RAIO * 0.75, CENTER - RAIO * 0.95,
            CENTER + RAIO * 0.15, CENTER - RAIO * 0.05,
        ],
        fill=70,
    )

    brilho = brilho.filter(ImageFilter.GaussianBlur(SUPERSAMPLE * 0.02))

    branco = Image.new("RGBA", imagem.size, (255, 255, 255, 0))
    branco.putalpha(brilho)

    return Image.alpha_composite(imagem, branco)


def main():

    imagem = gerar_base_moeda()
    imagem = desenhar_brilho(imagem)
    imagem = desenhar_anel_dourado(imagem)
    imagem = desenhar_grafico_crescimento(imagem)

    imagem = imagem.filter(ImageFilter.GaussianBlur(SUPERSAMPLE * 0.0015))

    destino = os.path.join(
        os.path.dirname(__file__),
        "icon.ico",
    )

    tamanhos = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

    imagem.save(destino, format="ICO", sizes=tamanhos)

    print(f"Icone gerado em: {destino}")


if __name__ == "__main__":
    main()
