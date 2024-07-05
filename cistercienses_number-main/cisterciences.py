import json
import numpy as np
from PIL import Image

base_numbers = []

# Carregar 'numbers-base.json'
with open('numbers-base.json') as f:
    numbers_base = json.load(f)


def crop_image(image, corner):
    # Recortar um pedaço de 3x4 pixels

    number = 0

    if corner == 'top_left':
        cropped_image = image.crop((0, 0, 3, 4))  # Recorta do canto superior esquerdo

    # inverte a imagem horizontalmente
        cropped_image = cropped_image.transpose(Image.FLIP_LEFT_RIGHT)

        number = 10

    elif corner == 'top_right':
        cropped_image = image.crop((4, 0, 7, 4))  # Recorta do canto superior direito

        number = 1

    elif corner == 'bottom_left':

        cropped_image = image.crop((0, 6, 3, 10))  # Recorta do canto inferior esquerdo
        # inverte a imagem horizontalmente
        cropped_image = cropped_image.transpose(Image.FLIP_LEFT_RIGHT)
        # inverte a imagem verticalmente
        cropped_image = cropped_image.transpose(Image.FLIP_TOP_BOTTOM)

        number = 1000

    elif corner == 'bottom_right':
        cropped_image = image.crop((4, 6, 7, 10))  # Recorta do canto inferior direito

        # inverte a imagem verticalmente
        cropped_image = cropped_image.transpose(Image.FLIP_TOP_BOTTOM)

        number = 100

    # Converter a imagem em uma matriz de binários
    binary_matrix = np.array(cropped_image)
    threshold = 128  # Definir um limiar para conversão em binário
    binary_matrix = np.where(binary_matrix < threshold, 1, 0)

    # Compara a matriz com as matrizes base
    for index in range(len(numbers_base)):
        base_number = numbers_base[index]
        if np.array_equal(binary_matrix, base_number):
            return (index + 1) * number

    return


def process_image(image_path):
    # Abrir a imagem
    image = Image.open(image_path).convert('L')  # Converte para escala de cinza
    image = image.resize((7, 10))  # Redimensiona a imagem para 10x7 pixels

    result = 0
    numbers = list()
    for corner in ['bottom_left', 'bottom_right', 'top_left', 'top_right']:
        binary_matrix = crop_image(image, corner)
        numbers.append(binary_matrix)

    for number in numbers:
        result = result + number

    return result


# Caminho da imagem
image_path = 'numbers-input.png'
final_number = process_image(image_path)

print('Número identificado:', final_number)