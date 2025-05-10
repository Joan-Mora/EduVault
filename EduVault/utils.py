from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from io import BytesIO

def generate_avatar(initials, background_color="#003366", text_color="#FFFFFF", size=200):
    # Crear una nueva imagen cuadrada
    img = Image.new('RGB', (size, size), color=background_color)
    
    # Preparar dibujo
    draw = ImageDraw.Draw(img)

    # Cargar fuente (debes tenerla o usar una de sistema)
    try:
        font = ImageFont.truetype("arial.ttf", int(size/2))
    except IOError:
        font = ImageFont.load_default()

    # Obtener tamaño del texto (usando textbbox en lugar de textsize)
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Posicionar el texto al centro
    x = (size - text_width) / 2
    y = (size - text_height) / 2 - 10  # ajuste pequeño vertical

    # Dibujar texto
    draw.text((x, y), initials, fill=text_color, font=font)

    # Guardar la imagen en memoria
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    image_file = ContentFile(buffer.getvalue())

    return image_file
