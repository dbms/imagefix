from io import BytesIO
import os
import datetime
from PIL import Image, ImageDraw, ImageFont

from django.core.files import File
from judge.choices import PATH_TO_FONT
from main.settings import BASE_DIR, MEDIA_ROOT
import uuid


class ImageToPdf:
    def convert(self, files):
        all_files = []
        
        for f in files:
            im = Image.open(f)
            if im.mode != 'RGB':
                im = im.convert("RGB")
            all_files.append(im)

        pdf_name = str(uuid.uuid4()) + '.pdf'
        pdf_io = BytesIO()
        all_files[0].save(pdf_io, 'PDF', save_all=True, append_images=all_files[1:])
        return File(pdf_io, name=pdf_name)  
