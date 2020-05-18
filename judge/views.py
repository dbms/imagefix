from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.views import View
from judge.forms import JudgeForm, NameDOBForm, ChangeFormatForm, CropImageForm
from judge.models import WriteOnImageModel, ChangeFormatModel, CropImageModel


class HomeView(View):
    from_class = JudgeForm
    template_name = 'judge/home.html'

    def get(self, request, *args, **kwargs):
        form = self.from_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.from_class(request.POST, request.FILES)
        if form.is_valid():
            saved_obj = form.save()
            context = {
                'processed_img': saved_obj.processed_img
            }
            return render(request, 'judge/display.html', {'context': context})
        return render(request, self.template_name, {'form': form})


class NameDOBCreateView(CreateView):
    model = WriteOnImageModel
    template_name = 'judge/add-name-dob.html'
    form_class = NameDOBForm

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_name_dob', args=(saved_instance.id,)))


class NameDOBUpdateView(UpdateView):
    model = WriteOnImageModel
    template_name = 'judge/add-name-dob.html'
    form_class = NameDOBForm
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_name_dob', args=(saved_instance.id,)))



class ChangeFormatCreateView(CreateView):
    model = ChangeFormatModel
    template_name = 'judge/change-format.html'
    form_class = ChangeFormatForm

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_format', args=(saved_instance.id,)))


class ChangeFormatUpdateView(UpdateView):
    model = ChangeFormatModel
    template_name = 'judge/change-format.html'
    form_class = ChangeFormatForm
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_format', args=(saved_instance.id,)))

class CropImageCreateView(CreateView):
    model = CropImageModel
    template_name = 'judge/crop-image.html'
    form_class = CropImageForm

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_crop_image', args=(saved_instance.id,)))


class CropImageUpdateView(UpdateView):
    model = CropImageModel
    template_name = 'judge/crop-image.html'
    form_class = CropImageForm
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        saved_instance = form.save()
        return redirect(reverse('update_crop_image', args=(saved_instance.id,)))