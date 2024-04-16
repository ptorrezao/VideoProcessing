import cv2
import os
import numpy as np
import datetime
import glob

def create_picture_in_picture(image_main, image1file, image2file, image3file, image4file, filename="", counter=1):
    # Carregar a imagem principal
    imagem_principal = cv2.imread(image_main)

    # Dividir a imagem principal em 4 quadrantes
    altura, largura, _ = imagem_principal.shape
    metade_altura = altura // 2
    metade_largura = largura // 2

    # Carregar as imagens ou criar uma imagem preta se ausente
    if os.path.exists(image1file):
        imagem_inserida1 = cv2.imread(image1file)
        imagem_inserida1_date = datetime.datetime.fromtimestamp(os.path.getmtime(image1file)).strftime('%d-%b-%Y')
    else:
        imagem_inserida1 = np.zeros((metade_altura, metade_largura, 3), dtype=np.uint8)
        imagem_inserida1_date = ""

    if os.path.exists(image2file):
        imagem_inserida2 = cv2.imread(image2file)
        imagem_inserida2_date = datetime.datetime.fromtimestamp(os.path.getmtime(image2file)).strftime('%d-%b-%Y')
    else:
        imagem_inserida2 = np.zeros((metade_altura, metade_largura, 3), dtype=np.uint8)
        imagem_inserida2_date = ""

    if os.path.exists(image3file):
        imagem_inserida3 = cv2.imread(image3file)
        imagem_inserida3_date = datetime.datetime.fromtimestamp(os.path.getmtime(image3file)).strftime('%d-%b-%Y')
    else:
        imagem_inserida3 = np.zeros((metade_altura, metade_largura, 3), dtype=np.uint8)
        imagem_inserida3_date = ""

    if os.path.exists(image4file):
        imagem_inserida4 = cv2.imread(image4file)
        imagem_inserida4_date = datetime.datetime.fromtimestamp(os.path.getmtime(image4file)).strftime('%d-%b-%Y')
    else:
        imagem_inserida4 = np.zeros((metade_altura, metade_largura, 3), dtype=np.uint8)
        imagem_inserida4_date = ""

    local = "Vilhas Velhas"
    position_title = (50, altura - 100)
    position = (50, altura - 50)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale_title = 2
    font_scale = 1.5
    font_color = (255, 255, 255, 100)
    thickness = 1

    # Redimensionar as imagens inseridas para metade da altura e largura
    imagem_inserida1 = cv2.putText(imagem_inserida1, local, position_title, font, font_scale_title, font_color, 2, cv2.LINE_AA)
    imagem_inserida1 = cv2.putText(imagem_inserida1, imagem_inserida1_date, position, font, font_scale, font_color, 2, cv2.LINE_AA)
    imagem_inserida1 = cv2.resize(imagem_inserida1, (metade_largura, metade_altura))

    imagem_inserida2 = cv2.putText(imagem_inserida2, local, position_title, font, font_scale_title, font_color, 2, cv2.LINE_AA)
    imagem_inserida2 = cv2.putText(imagem_inserida2, imagem_inserida2_date, position, font, font_scale, font_color, 2, cv2.LINE_AA)
    imagem_inserida2 = cv2.resize(imagem_inserida2, (metade_largura, metade_altura))

    imagem_inserida3 = cv2.putText(imagem_inserida3, local, position_title, font, font_scale_title, font_color, 2, cv2.LINE_AA)
    imagem_inserida3 = cv2.putText(imagem_inserida3, imagem_inserida3_date, position, font, font_scale, font_color, 2, cv2.LINE_AA)
    imagem_inserida3 = cv2.resize(imagem_inserida3, (metade_largura, metade_altura))

    imagem_inserida4 = cv2.putText(imagem_inserida4, local, position_title, font, font_scale_title, font_color, 2, cv2.LINE_AA)
    imagem_inserida4 = cv2.putText(imagem_inserida4, imagem_inserida4_date, position, font, font_scale, font_color, 2, cv2.LINE_AA)
    imagem_inserida4 = cv2.resize(imagem_inserida4, (metade_largura, metade_altura))

    # Definir os quadrantes da imagem principal
    quadrante1 = imagem_principal[0:metade_altura, 0:metade_largura]
    quadrante2 = imagem_principal[0:metade_altura, metade_largura:largura]
    quadrante3 = imagem_principal[metade_altura:altura, 0:metade_largura]
    quadrante4 = imagem_principal[metade_altura:altura, metade_largura:largura]

    # Sobrepor as imagens inseridas em cada quadrante
    quadrante1 = cv2.addWeighted(quadrante1, 0, imagem_inserida1, 1, 0)
    quadrante2 = cv2.addWeighted(quadrante2, 0, imagem_inserida2, 1 , 0)
    quadrante3 = cv2.addWeighted(quadrante3, 0, imagem_inserida3, 1, 0)
    quadrante4 = cv2.addWeighted(quadrante4, 0, imagem_inserida4, 1, 0)

    # Atualizar a imagem principal com os quadrantes modificados
    imagem_principal[0:metade_altura, 0:metade_largura] = quadrante1
    imagem_principal[0:metade_altura, metade_largura:largura] = quadrante2
    imagem_principal[metade_altura:altura, 0:metade_largura] = quadrante3
    imagem_principal[metade_altura:altura, metade_largura:largura] = quadrante4

    # Salvar a imagem resultante
    cv2.imwrite(f"Mosaic-{counter}.jpg", imagem_principal)

def processar_lote_imagens(diretorio, filename_base):
    # Listar todos os arquivos .jpg no diretório
    lista_arquivos_jpg = glob.glob(os.path.join(diretorio, '*.JPG'))

    # Processar as imagens em lotes de quatro
    for i in range(0, len(lista_arquivos_jpg), 4):
        # Selecionar quatro arquivos
        batch_files = lista_arquivos_jpg[i:i+4]
        
        # Chamar a função create_picture_in_picture para processar o lote
        create_picture_in_picture(filename_base, *batch_files,  filename_base,i)

processar_lote_imagens('Source', 'source\DJI_0075.JPG')