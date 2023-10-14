from pillow_heif import register_heif_opener
from PIL import Image

register_heif_opener()


def convert_heic_to_jpg(heic_file, output):
    try:
        img = Image.open(heic_file)
        img.save(output, "JPEG", quality=100)
        return True
    except Exception as e:
        print(e)
        return False
