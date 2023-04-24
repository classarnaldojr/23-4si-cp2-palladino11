import cv2
import matplotlib.pyplot as plt
import numpy as np

pontuacao_direita = 0
pontuacao_esquerda = 0
cont = 0

def titulo():
    (cv2.putText(video_final, "Jokenpo", (250, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 179), 2, cv2.LINE_AA))

def jogada_da_mao_esquerda(jogada_esquerda):
    (cv2.putText(video_final, ("Esquerda: " + str(jogada_esquerda)), (25, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA))

def jogada_da_mao_direita(jogada_direita):
    (cv2.putText(video_final, ("Direita: " + str(jogada_direita)), (425, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA))

def placar_mao_esquerda(pontos_esquerda):
    (cv2.putText(video_final, "Esquerda: " + str(pontos_esquerda), (25, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 179), 1, cv2.LINE_AA))

def placar_mao_direita(pontos_direita):
    (cv2.putText(video_final, "Direita: " + str(pontos_direita), (425, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 179), 1, cv2.LINE_AA))

def vencedor_da_rodada(vitoria):
    (cv2.putText(video_final, str(vitoria), (250, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 179), 1, cv2.LINE_AA))

def gray_and_blur(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    k_size = (35, 35)
    filtro_blur = cv2.GaussianBlur(img_gray, k_size, 0)

    _, thresh = cv2.threshold(filtro_blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return thresh

def area(contours):
    area_total = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > area_total:
            area_total = area

    return area_total

def contornos(thresh):
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contours

def jogadas(area):
    if area > 14500 and area < 17000:
        jogada = "Papel"
        return jogada
    elif area > 11500 and area < 14000:
        jogada = "Pedra"
        return jogada
    elif area < 11500 and area > 6000:
        jogada = "Tesoura"
        return jogada

def vencedor(jogada_esquerda, jogada_direita):

    if jogada_esquerda == jogada_direita:
        resultado = "Empate!"
        return resultado

    elif (jogada_esquerda == "Tesoura" and jogada_direita == "Papel"):
        resultado = "Mao Esquerda Venceu!"
        return resultado
    elif (jogada_esquerda == "Papel" and jogada_direita == "Tesoura"):
        resultado = "Mao Direita Venceu!"
        return resultado
    elif (jogada_esquerda == "Pedra" and jogada_direita == "Tesoura"):
        resultado = "Mao Esquerda Venceu!"
        return resultado
    elif (jogada_esquerda == "Tesoura" and jogada_direita == "Pedra"):
        resultado = "Mao Direita Venceu!"
        return resultado
    elif (jogada_esquerda == "Papel" and jogada_direita == "Pedra"):
        resultado = "Mao Esquerda Venceu!"
        return resultado
    elif (jogada_esquerda == "Pedra" and jogada_direita == "Papel"):
        resultado = "Mao Direita Venceu!"
        return resultado


def placarEsquerda(vitorioso, pontuacao_mao_esquerda):
    if vitorioso == "Mao Esquerda Venceu!":
        pontuacao_mao_esquerda = pontuacao_mao_esquerda + 1
    return pontuacao_mao_esquerda

def placarDireita(vitorioso, pontuacao_mao_direita):
    if vitorioso == "Mao Direita Venceu!":
        pontuacao_mao_direita = pontuacao_mao_direita + 1
    return pontuacao_mao_direita

def vencedorGeral(resultado_esquerda, resultado_direita):
    if resultado_esquerda > resultado_direita:
        return "Mão Esquerda ganhou mais que a direita!"
    elif resultado_direita > resultado_esquerda:
        return "Mão Direita ganhou mais que a esquerda!"
    else:
        return "As duas mãos ganharam a mesma quantidade de vezes!"

video = cv2.VideoCapture('pedra-papel-tesoura.mp4')

while True:

    ret, rec = video.read()

    video_final = cv2.resize(rec, (800, 600))

    crop_video_esquerda = video_final[100:600, 100:450]

    crop_video_direita = video_final[100:600, 350:800]

    imagem_gray1 = gray_and_blur(crop_video_esquerda)
    imagem_gray2 = gray_and_blur(crop_video_direita)

    contorno_mao_esquerda = contornos(imagem_gray1)
    contorno_mao_direita = contornos(imagem_gray2)

    area_mao_esquerda = area(contorno_mao_esquerda)
    area_mao_direita = area(contorno_mao_direita)

    jogada_mao_esquerda = jogadas(area_mao_esquerda)
    jogada_mao_direita = jogadas(area_mao_direita)

    ganhador = vencedor(jogada_mao_esquerda, jogada_mao_direita)

    cont += 1
    if cont >= 90:
        cont = 0
        pontuacao_esquerda = placarEsquerda(ganhador, pontuacao_esquerda)
        pontuacao_direita = placarDireita(ganhador, pontuacao_direita)

    resultado_final = vencedorGeral(pontuacao_esquerda, pontuacao_direita)

    titulo()
    jogada_da_mao_esquerda(jogada_mao_esquerda)
    jogada_da_mao_direita(jogada_mao_direita)
    placar_mao_esquerda(pontuacao_esquerda)
    placar_mao_direita(pontuacao_direita)
    vencedor_da_rodada(ganhador)

    cv2.imshow("Video final", video_final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(resultado_final)
        break

    if not ret:
        break

video.release()

cv2.destroyAllWindows()
