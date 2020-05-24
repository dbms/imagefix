from io import BytesIO
import os
import datetime
from PIL import Image, ImageDraw, ImageFont

from django.core.files import File
from judge.choices import PATH_TO_FONT
from main.settings import BASE_DIR, MEDIA_ROOT



class ResizeByPixel:
    def __init__(self, width, height):
        self.width = width
        self.height = height        

    def resize(self, image):
        im = Image.open(image)
        inp_img_details = self.get_input_img_details(image, im)
        
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")

        im = im.resize((self.width, self.height),Image.ANTIALIAS)
        thumb_io = BytesIO()
        im.save(thumb_io, inp_img_details.get('img_format'))
        processed_img = File(thumb_io, name=image.name)
        return {
            'processed_img': processed_img,
            'inp_format': inp_img_details.get('img_format'),
            'inp_height': inp_img_details.get('height'),
            'inp_width': inp_img_details.get('width'),
            'inp_size_kb': inp_img_details.get('size_kb'),
            'out_format': inp_img_details.get('img_format'),
            'out_size_kb': self.get_image_size_in_kb(processed_img),            
        }

    @staticmethod
    def get_input_img_details(inp_img ,pil_im):  
        width, height = pil_im.size

        return {
            'img_format': pil_im.format,
            'width': width,
            'height': height,
            'size_kb': ResizeByPixel.get_image_size_in_kb(inp_img)
        }

    @staticmethod 
    def get_image_size_in_kb(image):
        return image.size/1024
