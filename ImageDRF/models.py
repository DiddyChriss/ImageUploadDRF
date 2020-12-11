from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class MyAccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.create_user(username=username, password=password, **kwargs)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Plan(models.Model):
<<<<<<< HEAD
    name            = models.CharField(max_length=200, default='Basic')
=======
    name            = models.CharField(max_length=200, unique=True)
>>>>>>> 838b334259b37ef4165ce94b05f742125a023c3e
    img_px200       = models.BooleanField(default=True)
    img_px400       = models.BooleanField(default=False)
    img             = models.BooleanField(default=False)
    generated_link  = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    username                = models.CharField(max_length=30, unique=True)
    plan                    = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    email                   = models.EmailField(verbose_name='email', max_length=60, unique=True)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name= 'last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)

<<<<<<< HEAD
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()
=======
class AccountUser(models.Model):
    user_account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    account  = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='Account')
>>>>>>> 838b334259b37ef4165ce94b05f742125a023c3e

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Image(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
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
