from io import BytesIO
import os
import datetime
from PIL import Image, ImageDraw, ImageFont

from django.core.files import File
from judge.choices import PATH_TO_FONT
from main.settings import BASE_DIR, MEDIA_ROOT


class ChangeFormat:
    def __init__(self, dest_format):
        self.dest_format = dest_format
    
    def change_format(self, image):
        im = Image.open(image)
        if im.mode != 'RGB':
            im = im.convert("RGB")

        thumb_io = BytesIO()
        im.save(thumb_io, self.dest_format, quality=95)
        processed_img = File(thumb_io, name=self.get_processed_filename(image))       
        return processed_img
        
    def get_processed_filename(self, image):
        head, tail = os.path.split(image.url)
        return tail.split('.')[0] + '.' + self.dest_format.lower()
