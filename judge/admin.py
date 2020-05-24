from django.contrib import admin
import judge.models as models

admin.site.register(models.WriteOnImageModel)
admin.site.register(models.ChangeFormatModel)
admin.site.register(models.CropImageModel)
admin.site.register(models.PrivacyPolicyModel)
admin.site.register(models.ContactModel)
admin.site.register(models.ImagePdfModel)
admin.site.register(models.ResizeByPixelModel)
admin.site.register(models.CompressImageModel)

