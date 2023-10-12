import os
from pillow_heif import register_heif_opener
from PIL import Image

register_heif_opener()


def convert_heic_to_jpg(heic_file, output_directory):
    try:
        img = Image.open(heic_file)
        jpg_file = os.path.join(output_directory, os.path.splitext(os.path.basename(heic_file))[0] + ".jpg")
        img.save(jpg_file, "JPEG", quality=100)
        return True
    except Exception as e:
        return False
