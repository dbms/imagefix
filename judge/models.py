import uuid

from django.db import models
from judge.choices import IMAGE_FORMATS, CONTACT_REASON
from judge.file_actions import (
    change_format, 
    draw_on_image, 
    resize_by_pixel,
    compress_image,
)
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError


class ImageBaseModel(models.Model):
    inp_format = models.CharField(max_length=128, null=True)
    inp_height = models.IntegerField(null=True)
    inp_width = models.IntegerField(null=True)
    inp_size = models.DecimalField(null=True, max_digits=10, decimal_places=2)

    out_format = models.CharField(max_length=128, null=True)
    out_height = models.IntegerField(null=True)
    out_width = models.IntegerField(null=True)
    out_size = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)

class WriteOnImageModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=128, null=True)
    raw_img = models.ImageField(upload_to='raw_images', null=True)
    processed_img = models.ImageField(upload_to='processed_images', null=True)
    dob = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        obj = draw_on_image.DrawOnImage(self.name, self.dob)
        self.processed_img = obj.draw(self.raw_img)
        super().save(*args, **kwargs)


class ChangeFormatModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    dest_format = models.CharField(max_length=20, null=True, choices=IMAGE_FORMATS, default='JPG')
    raw_img = models.ImageField(upload_to='raw_images', null=True)
    processed_img = models.ImageField(upload_to='processed_images', null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        obj = change_format.ChangeFormat(self.dest_format)
        self.processed_img = obj.change_format(self.raw_img)
        super().save(*args, **kwargs)
    

class CropImageModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    dest_format = models.CharField(max_length=20, null=True, choices=IMAGE_FORMATS, default='JPG')
    processed_img = models.ImageField(upload_to='processed_images', null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class ImagePdfModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    processed_pdf = models.FileField(upload_to='converted_pdfs', null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class PrivacyPolicyModel(models.Model):
    content = HTMLField()


class ContactModel(models.Model):
    reason = models.CharField(max_length=50, choices=CONTACT_REASON, default='Suggestion')
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True)
    attach_screenshot = models.ImageField(upload_to='processed_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reason

class ResizeByPixelModel(ImageBaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    raw_img = models.ImageField(upload_to='raw_images', null=True)
    processed_img = models.ImageField(upload_to='processed_images', null=True)

    def __str__(self):
        return str(self.uuid)

    def save(self, *args, **kwargs):
        obj = resize_by_pixel.ResizeByPixel(self.out_width, self.out_height)
        img_info_dict = obj.resize(self.raw_img)
        self.processed_img = img_info_dict.get('processed_img')
        self.out_format = img_info_dict.get('out_format')
        self.out_size = img_info_dict.get('out_size_kb')

        self.inp_format = img_info_dict.get('inp_format')
        self.inp_height = img_info_dict.get('inp_height')
        self.inp_width = img_info_dict.get('inp_width')
        self.inp_size = img_info_dict.get('inp_size_kb')

        super().save(*args, **kwargs)
    


class CompressImageModel(ImageBaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    min_size = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    max_size = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    raw_img = models.ImageField(upload_to='raw_images', null=True)
    processed_img = models.ImageField(upload_to='processed_images', null=True)
    

    def __str__(self):
        return str(self.uuid)

    def clean(self):
        if self.min_size >= self.max_size:
            raise ValidationError('Min size should be less than Max Size')

    def save(self, *args, **kwargs):
        obj = compress_image.CompressImage(self.min_size, self.max_size)
        img_info_dict = obj.compress(self.raw_img)
        self.processed_img = img_info_dict.get('processed_img')

        self.out_format = img_info_dict.get('out_format')
        self.out_height = img_info_dict.get('out_height')
        self.out_width = img_info_dict.get('out_width')
        self.out_size = img_info_dict.get('out_size_kb')

        self.inp_format = img_info_dict.get('inp_format')
        self.inp_height = img_info_dict.get('inp_height')
        self.inp_width = img_info_dict.get('inp_width')
        self.inp_size = img_info_dict.get('inp_size_kb')

        super().save(*args, **kwargs)