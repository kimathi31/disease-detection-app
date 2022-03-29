from django.db import models
from django.utils import timezone
import os

from django.utils.translation import gettext_lazy as _

class crop_analysis(models.Model):
    Analysis_REF_No = models.CharField(primary_key=True, max_length=255)
    Crop = models.CharField(max_length=255)
    Status = models.CharField(max_length=255)
    Disease = models.CharField(max_length=255)
    Probability = models.CharField(max_length=255)
    Date_Created = models.DateTimeField(default=timezone.now)


    class Meta:
        db_table='CropAnalysisReport'





class ImageModel(models.Model):
    image = models.ImageField(_("image"), upload_to='images')

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return str(os.path.split(self.image.path)[-1])