import datetime
from upload_validator import FileTypeValidator
from django.utils import timezone

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ImageField, IntegerField

from ImageDRF.models import Image, User, Account


class UserSerializer(ModelSerializer):
    img            = ImageField()
    img_original   = SerializerMethodField()
    img_px400      = SerializerMethodField(read_only=True)
    img_px200      = ImageField(read_only=True)
    user           = SerializerMethodField()
    generated_link = SerializerMethodField(read_only=True)
    delete_generated_link_time = IntegerField()

    class Meta:
        model   = Image
        fields  = [
            'pk',
            'user',
            'img_px200',
            'img_px400',
            'img',
            'img_original',
            'delete_generated_link_time',
            'generated_link',
        ]

    def get_fields(self, *args, **kwargs):
        fields = super(UserSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        user = User.objects.get(userUser=request.user)
        if user.account.generated_link == False:
            fields['delete_generated_link_time'].read_only = True
        return fields

    def to_representation(self, obj,  *args, **kwargs):                                      # remove selected fields
        ret = super(UserSerializer, self).to_representation(obj)
        ret.pop('img')
        if obj.user.account.img == False:
            ret.pop('img_original')
        if obj.user.account.img_px400 == False:
            ret.pop('img_px400')
        if obj.user.account.generated_link == False:
            ret.pop('delete_generated_link_time')
            ret.pop('generated_link')
        else:
            now_time = timezone.now()
            delete_time = obj.timestamp + datetime.timedelta(
                seconds=int(obj.delete_generated_link_time)
            )
            if now_time > delete_time:
                ret.pop('delete_generated_link_time')
                ret.pop('generated_link')
        return ret

    def get_img_px400(self, obj, *args, **kwargs):                     # genarate link for 200px thumbnail
        request = self.context.get("request")
        if obj.user.account.img_px400 == True:
            return request.build_absolute_uri(obj.img_px400.url)

    def get_img_original(self, obj, *args, **kwargs):                  # genarate link for original size image
        request = self.context.get("request")
        if obj.user.account.img == True:
            return request.build_absolute_uri(obj.img.url)

    def get_generated_link(self, obj, *args, **kwargs):                # genarate expiring link for original size image
        request = self.context.get("request")
        if obj.user.account.generated_link == True:
            return request.build_absolute_uri(obj.img.url)

    def get_user(self, obj):                                           # user
        return str(obj.user.userUser)

    def validate(self, data, *args, **kwargs):                                          # validation
        img = data.get("img", None)
        delete_generated_link_time = data.get("delete_generated_link_time", None)
        request = self.context.get('request', None)
        user = User.objects.get(userUser=request.user)
        if img is None:
            raise serializers.ValidationError("Image must be provided!")
        if user.account.generated_link == True and (delete_generated_link_time is None or
                                                    delete_generated_link_time < 300 or
                                                    delete_generated_link_time > 30000):
            raise serializers.ValidationError(
                "Enter the number of seconds! The number cannot be less than 300 and greater than 30000 !",
            )
        validator = FileTypeValidator(
            allowed_types=['image/*'],
            allowed_extensions=['.jpg', '.png']
        )
        validator(img)
        return data
