from io import BytesIO
import os
import datetime
from PIL import Image, ImageDraw, ImageFont

from django.core.files import File
from judge.choices import PATH_TO_FONT
from main.settings import BASE_DIR, MEDIA_ROOT


class CompressImage:
    def __init__(self, min_size, max_size):
        self.min_size = min_size
        self.max_size = max_size       

    def compress(self, image):
        im = Image.open(image)
        inp_img_details = self.get_input_img_details(image, im)
        
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")

        # setting input value as output values
        out_size = inp_img_details.get('size_kb')
        out_height = inp_img_details.get('height')
        out_width = inp_img_details.get('width')

        while True:
            if self.min_size > out_size:
                out_width = out_width+(out_width//2)
                out_height = out_height+(out_height//2)
                im = im.resize((out_width, out_height), Image.ANTIALIAS)
                out_size = self.get_pil_img_size_in_kb(im, inp_img_details.get('img_format'), image)
                continue
            if out_size > self.max_size:
                out_width = out_width-(out_width//2)
                out_height = out_height-(out_height//2)
                im = im.resize((out_width, out_height), Image.ANTIALIAS)
                out_size = self.get_pil_img_size_in_kb(im, inp_img_details.get('img_format'), image)
                continue
            break            
        
        # gathering output image details
        out_img_details = dict()
        out_img_details['height'] = out_height
        out_img_details['width'] = out_width
        out_img_details['img_format'] = inp_img_details.get('img_format')
        out_img_details['size_kb'] = out_size

        thumb_io = BytesIO()
        im.save(thumb_io, inp_img_details.get('img_format'))
        processed_img = File(thumb_io, name=image.name)
        return {
            'processed_img': processed_img,
            'inp_format': inp_img_details.get('img_format'),
            'inp_height': inp_img_details.get('height'),
            'inp_width': inp_img_details.get('width'),
            'inp_size_kb': inp_img_details.get('size_kb'),
            'out_format': out_img_details.get('img_format'),
            'out_height': out_img_details.get('height'),
            'out_width': out_img_details.get('width'),
            'out_size_kb': out_img_details.get('size_kb'),            
        }

    @staticmethod
    def get_input_img_details(inp_img ,pil_im):  
        width, height = pil_im.size

        return {
            'img_format': pil_im.format,
            'width': width,
            'height': height,
            'size_kb': CompressImage.get_image_size_in_kb(inp_img)
        }

    @staticmethod 
    def get_image_size_in_kb(image):
        return image.size/1024
    
    @staticmethod
    def get_pil_img_size_in_kb(im, img_format, image):
        thumb_io = BytesIO()
        im.save(thumb_io, img_format)
        processed_img = File(thumb_io, name=image.name)
        return CompressImage.get_image_size_in_kb(processed_img)
