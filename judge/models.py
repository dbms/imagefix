import uuid

from django.db import models
from judge.choices import IMAGE_FORMATS
from judge.file_actions import DrawOnImage, ChangeFormat


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
        obj = DrawOnImage(self.name, self.dob)
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
        obj = ChangeFormat(self.dest_format)
        self.processed_img = obj.change_format(self.raw_img)
        super().save(*args, **kwargs)
    

class CropImageModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    dest_format = models.CharField(max_length=20, null=True, choices=IMAGE_FORMATS, default='JPG')
    processed_img = models.ImageField(upload_to='processed_images', null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)