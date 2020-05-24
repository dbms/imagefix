from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views import View
import judge.forms as forms
import judge.models as models
from judge.file_actions.image_to_pdf import ImageToPdf

from PIL import Image

class HomeView(generic.TemplateView):
    template_name = 'judge/home.html'

class NameDOBCreateView(generic.CreateView):
    model = models.WriteOnImageModel
    template_name = 'judge/add-name-dob.html'
    form_class = forms.NameDOBForm

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_name_dob', args=(saved_instance.id,)))


class NameDOBUpdateView(generic.UpdateView):
    model = models.WriteOnImageModel
    template_name = 'judge/add-name-dob.html'
    form_class = forms.NameDOBForm
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_name_dob', args=(saved_instance.id,)))



class ChangeFormatCreateView(generic.CreateView):
    model = models.ChangeFormatModel
    template_name = 'judge/change-format.html'
    form_class = forms.ChangeFormatForm

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_format', args=(saved_instance.id,)))


class ChangeFormatUpdateView(generic.UpdateView):
    model = models.ChangeFormatModel
    template_name = 'judge/change-format.html'
    form_class = forms.ChangeFormatForm
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_format', args=(saved_instance.id,)))

class CropImageCreateView(generic.CreateView):
    model = models.CropImageModel
    template_name = 'judge/crop-image.html'
    form_class = forms.CropImageForm

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_crop_image', args=(saved_instance.id,)))


class CropImageUpdateView(generic.UpdateView):
    model = models.CropImageModel
    template_name = 'judge/crop-image.html'
    form_class = forms.CropImageForm
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_crop_image', args=(saved_instance.id,)))

'''
Create pdf from the images uploaded by the user
'''

class ImagePdfCreateView(generic.CreateView):
    model = models.ImagePdfModel
    template_name = 'judge/image-to-pdf.html'
    form_class = forms.ImageToPdfForm

    def form_valid(self, form):
        img_files = self.request.FILES.getlist('upload_images')
        
        saved_instance = form.save(commit=False)

        i2p_obj = ImageToPdf()
        saved_instance.processed_pdf = i2p_obj.convert(img_files)
        saved_instance.save()
        context = {
            'form': self.form_class,
            'processed_pdf_path': saved_instance.processed_pdf.url,            
        }
        return render(self.request, self.template_name, context)



'''
resize the image by pixel provided the the user
height - x
width - y
'''
class ResizeByPixelCreateView(generic.CreateView):
    model = models.ResizeByPixelModel
    template_name = 'judge/resize-by-pixel.html'
    form_class = forms.ResizeByPixelForm

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_resize_by_pixel', args=(saved_instance.uuid,)))


class ResizeByPixelUpdateView(generic.UpdateView):
    model = models.ResizeByPixelModel
    template_name = 'judge/resize-by-pixel.html'
    form_class = forms.ResizeByPixelForm
    pk_url_kwarg = 'uuid'

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_resize_by_pixel', args=(saved_instance.uuid,)))



'''
Compress image provided the the user
min-size
max_size
'''
class CompressImageCreateView(generic.CreateView):
    model = models.CompressImageModel
    template_name = 'judge/compress-image.html'
    form_class = forms.CompressImageForm

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_compress_image', args=(saved_instance.uuid,)))


class CompressImageUpdateView(generic.UpdateView):
    model = models.CompressImageModel
    template_name = 'judge/compress-image.html'
    form_class = forms.CompressImageForm
    pk_url_kwarg = 'uuid'

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_compress_image', args=(saved_instance.uuid,)))


'''
Privacy Policy View
'''
class PrivacyPolicyView(generic.ListView):
    model = models.PrivacyPolicyModel
    template_name = 'privacy-policy.html'


'''
Contact View
'''
class ContactCreateView(generic.CreateView):
    model = models.ContactModel
    template_name = 'contact-us.html'
    form_class = forms.ContactForm

    def form_valid(self, form):
        saved_instance = form.save()
        messages.success(self.request, 'Message Recieved.')
        return redirect(reverse('contact_us'))
