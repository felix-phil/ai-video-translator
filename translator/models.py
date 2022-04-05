from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from uuid import uuid4


class Translator(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    labelImage = models.ImageField(
        upload_to='images/translators', null=True, blank=True)
    source_video = models.FileField(upload_to='videos/source',
                                    blank=False,
                                    null=False,
                                    validators=[FileExtensionValidator(
                                        allowed_extensions=['mp4', 'webm', 'mkv'])]
                                    )
    source_audio = models.FileField(upload_to='audios/source',
                                    blank=True, null=True,
                                    validators=[FileExtensionValidator(
                                        allowed_extensions=['flv', 'FLV', 'wav'])]
                                    )
    extracted_text = models.TextField(null=True, blank=True)
    translated_text = models.TextField(null=True, blank=True)
    translated_audio = models.FileField(upload_to='audios/destination',
                                        null=True,
                                        blank=True,
                                        validators=[FileExtensionValidator(
                                            allowed_extensions=[
                                                'flv', 'FLV', 'wav']
                                        )])
    translated_video_audio = models.FileField(upload_to='videos/destination',
                                              null=True,
                                              blank=True,
                                              validators=[FileExtensionValidator(
                                                  allowed_extensions=['mp4', 'webm', 'mkv'])]
                                              )
    LANGUAGE_CHOICES = (
        ('fr', 'French'),
        ('en', 'English'),
        ('es', 'Spanish'),
        ('it', 'Italian'),
        ('ja', 'Japanese'),
        ('zh', 'Chinese'),
        ('de', 'German'),

    )
    source_language = models.CharField(max_length=5,
                                       choices=LANGUAGE_CHOICES, null=False, blank=False)
    destination_language = models.CharField(max_length=5,
                                            choices=LANGUAGE_CHOICES, null=False, blank=False)
    STATUS = (
        ('PENDING', 'PENDING'),
        ('FAILED', 'FAILED'),
        ('COMPLETED', 'COMPLETED'),
        ('LOADING', 'LOADING')
    )
    status = models.CharField(
        choices=STATUS, default='PENDING', max_length=100)
    current_task = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self) -> str:
        return self.name or str(self.pk)

    def __repr__(self) -> str:
        return self.name or str(self.pk)

    class Meta:
        verbose_name = _("Video Translation")
        verbose_name_plural = _("Video Translations")


class Contributor(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/contributors')

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        # extension = img.filename.split('.')[-1]
        extension = img.format
        newfilename = 'contributor-{}.{}'.format(uuid4().hex, extension)

        if img.height > 1024 or img.width > 1024:
            output_size = (1024, 1024)
            img.thumbnail(output_size)
            # img.filename = newfilename
        img.save(self.image.path)

    class Meta:
        verbose_name = _("Contributor")
        verbose_name_plural = _("Contributors")
