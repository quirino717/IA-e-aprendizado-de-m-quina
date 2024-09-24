# import cv2
#
# #Captura a câmera 0, se tiver mais de uma câmera #aqui poderá ser selecionada a câmera desejada
#
# cap = cv2.VideoCapture(0)
#
# while(True): # Captura de frame por frame
#     ret, frame = cap.read()
#     # Aqui pode se executar processamento no frame
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     # Mostrando o resultado
#
#     cv2.imshow("frame",gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Libera a câmera
# cap.release()
# cv2.destroyAllWindows()

# import cv2
#
# cap = cv2.VideoCapture(0)
# ret, frame = cap.read()
# next_frame = frame
#
# while (cap.isOpened()):
#     ret, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     next_frame_gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
#
#     #Calcula a diferença absoluta por elemento entre duas matrizes
#     frame_diff = cv2.absdiff(gray, next_frame_gray)
#     cv2.imshow('frame', frame_diff)
#     cv2.imshow('gray image', gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
#     next_frame = frame.copy()
#     ret, frame = cap.read()
#
# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np

cap = cv2.VideoCapture('vtest.avi')
#cap = cv2.VideoCapture(0)

# history = número de frames usados para construir o modelo estatístico do plano de fundo.
# Quanto menor o valor, mais rápidas as alterações no plano de fundo serão consideradas pelo modelo.
# varThreshold = Limiar na distância quadrada de Mahalanobis entre o pixel e o modelo para decidir se um pixel está bem
# descrito pelo modelo de fundo.
#detectShadows = Se True, as sombras serão apresentadas na imagem.

mog = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=10, detectShadows=True)

while(cap.isOpened()):
    ret, frame = cap.read()

    fgmask = mog.apply(frame)

    cv2.imshow('frame movimento',fgmask )
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
#
# cap = cv2.VideoCapture('vtest.avi')
# #cap = cv2.VideoCapture(0)
#
# # Carregar as imagens da câmera esquerda e direita
# imgL = cv2.imread('tsukuba_l.png', cv2.IMREAD_GRAYSCALE)
# imgR = cv2.imread('tsukuba_r.png', cv2.IMREAD_GRAYSCALE)
#
# # Definir parâmetros para o cálculo do mapa de disparidade
# num_disparities = 32 # Deve ser divisível por 16
# block_size = 15 # Tamanho do bloco de correspondência, tipicamente ímpar (5, 7, 9, 11, ...)
#
# stereo = cv2.StereoBM_create(numDisparities=num_disparities, blockSize=block_size)
# disparity = stereo.compute(imgL,imgR)
#
# plt.imshow(disparity,'gray')
# plt.show()
#
# while(True):
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
