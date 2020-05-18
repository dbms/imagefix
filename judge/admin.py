from django.contrib import admin
from judge.models import WriteOnImageModel, ChangeFormatModel, CropImageModel

admin.site.register(WriteOnImageModel)
admin.site.register(ChangeFormatModel)
admin.site.register(CropImageModel)

