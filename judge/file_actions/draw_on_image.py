from io import BytesIO
import os
import datetime
from PIL import Image, ImageDraw, ImageFont

from django.core.files import File
from judge.choices import PATH_TO_FONT
from main.settings import BASE_DIR, MEDIA_ROOT



class DrawOnImage:
    def __init__(self, name, dob):
        self.name = name.title()
        self.dob = datetime.datetime.strftime(dob, '%d-%m-%Y')
        self.color = 'rgb(0, 0, 0)'
        self.fillsize = 100
        self.font = ImageFont.truetype(os.path.join(PATH_TO_FONT, 'FreeSansBold.ttf'), size=45)

    def draw(self, image):
        im = Image.open(image)
        
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        
        original_file_format = im.format
        self.draw = ImageDraw.Draw(im)
        
        self.width, self.height = im.size 
        self.shape = [(0, self.height-self.fillsize), (self.width, self.height)] 

        self.draw_rectangle(fill=255)
        self.draw_text(self.get_name_coordinates(), self.name)
        self.draw_text(self.get_dob_coordinates(), self.dob)

        thumb_io = BytesIO()
        im.save(thumb_io, 'JPEG')
        processed_img = File(thumb_io, name=image.name) # saving the file with same name
        return processed_img

    def draw_text(self, coordinates, text, fill=0):
        self.draw.text(coordinates, text, font=self.font, color=self.color)

    def draw_rectangle(self, fill=255):
        self.draw.rectangle(self.shape, fill=fill)

    def get_name_coordinates(self):
        w, h = self.draw.textsize(self.name, font=self.font)
        return ((self.width-w)/2, self.height - self.fillsize + 5)

    def get_dob_coordinates(self):
        w, h = self.draw.textsize(self.dob, font=self.font)
        return ((self.width-w)/2, self.height - self.fillsize + 50)
