from PIL import Image

from django.forms import ModelForm
from django import forms
from django.core.files import File

from judge.models import WriteOnImageModel, ChangeFormatModel, CropImageModel
from judge.choices import DATE_INPUT_FORMATS


class JudgeForm(ModelForm):
    
    class Meta:
        model = WriteOnImageModel
        fields = ['raw_img', 'name']
        


class NameDOBForm(ModelForm):
    
    dob = forms.DateField(
        widget=forms.DateInput(format=DATE_INPUT_FORMATS[0], attrs={'autocomplete': 'off'}),
        input_formats=DATE_INPUT_FORMATS
    )

    class Meta:
        model = WriteOnImageModel
        fields = ['raw_img', 'name', 'dob']
        labels = {
            'raw_img': '',
            'dob': 'Date of Birth or Photo'
        }


class ChangeFormatForm(ModelForm):
    
    class Meta:
        model = ChangeFormatModel
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
        model = CropImageModel
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