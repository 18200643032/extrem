from django.db import models

# Create your models here.




class SDK_ias():
    """
    ias表
    """
    images = models.CharField()

    class Meta:
        verbose_name = "ias"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.images


class SDK_standard():
    """
    standard表
    """
    images = models.CharField()

    class Meta:
        verbose_name = "standard"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.images