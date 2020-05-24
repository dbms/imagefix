from PIL import Image

from django.forms import ModelForm
from django import forms
from django.core.files import File

import judge.models as models
from judge.choices import DATE_INPUT_FORMATS


class JudgeForm(ModelForm):
    
    class Meta:
        model = models.WriteOnImageModel
        fields = ['raw_img', 'name']
        

class NameDOBForm(ModelForm):
    
    dob = forms.DateField(
        widget=forms.DateInput(format=DATE_INPUT_FORMATS[0], attrs={'autocomplete': 'off'}),
        input_formats=DATE_INPUT_FORMATS
    )

    class Meta:
        model = models.WriteOnImageModel
        fields = ['raw_img', 'name', 'dob']
        labels = {
            'raw_img': '',
            'dob': 'Date of Birth or Photo'
        }


class ChangeFormatForm(ModelForm):
    
    class Meta:
        model = models.ChangeFormatModel
        fields = ['raw_img', 'dest_format']
        labels = {
            'raw_img': '',
            'dest_format': 'Convert To'
        }

class CropImageForm(ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = models.CropImageModel
        fields = ('processed_img', 'x', 'y', 'width', 'height', )
        labels = {
            'processed_img': '',
        }

    def save(self):
        photo = super(CropImageForm, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        im = Image.open(photo.processed_img)
        if im.mode != 'RGB':
            im = im.convert("RGB")
        cropped_image = im.crop((x, y, w+x, h+y))
        # resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        cropped_image.save(photo.processed_img.path)

        return photo

class ImageToPdfForm(ModelForm):
    upload_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = models.ImagePdfModel
        fields = ['upload_images',]        

class ResizeByPixelForm(ModelForm):
    
    class Meta:
        model = models.ResizeByPixelModel
        fields = ['raw_img', 'out_width', 'out_height']
        labels = {
            'raw_img': '',
            'out_height': 'Height(px)',
            'out_width': 'Width(px)'
        }

class CompressImageForm(ModelForm):
    
    class Meta:
        model = models.CompressImageModel
        fields = ['raw_img', 'min_size', 'max_size']
        labels = {
            'raw_img': '',
            'min_size': 'Minimum Size(kB)',
            'max_size': 'Maximum Size(kB)'
        }

class ContactForm(ModelForm):
    
    class Meta:
        model = models.ContactModel
        fields = ['reason', 'email', 'message', 'attach_screenshot']
        labels = {
            'attach_screenshot': 'Attach Screenshot',
        }
        widgets = {
          'message': forms.Textarea(attrs={'rows':4}),
        }