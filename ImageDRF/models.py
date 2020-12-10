from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from django.conf import settings
from django.db import models

class Plan(models.Model):
    name            = models.CharField(max_length=200, unique=True)
    img_px200       = models.BooleanField(default=True)
    img_px400       = models.BooleanField(default=False)
    img             = models.BooleanField(default=False)
    generated_link  = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

class AccountUser(models.Model):
    user_account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    account  = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='Account')

    def __str__(self):
        return str(self.user_account)

class Image(models.Model):
    user          = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='User')
    img           = models.ImageField(upload_to='',null=True)
    img_px200     = ImageSpecField(
        source='img',
        processors=[ResizeToFill(150, 200)],
        format='png',
        options={'quality': 70}
    )
    img_px400     = ImageSpecField(
        source='img',
        processors=[ResizeToFill(300, 400)],
        format='png',
        options={'quality': 70}
    )
    delete_generated_link_time = models.IntegerField(
        default=300)
    timestamp     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.img)

