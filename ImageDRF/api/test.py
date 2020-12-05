import datetime
from django.contrib.auth import get_user_model
from django.core.files import File

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

from ImageDRF.models import Image, User, Account
from .views import ImageAPIView

User_auth = get_user_model()

class ImageDRFAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User_auth(username='testone', email='wp@wp.pl')          # def user
        user_obj.set_password('somepassword')
        user_obj.save()

        account = Account.objects.create(
            name='Enterprise',
            img_px200 = True,
            img_px400 = True,
            img = True,
            generated_link = True,
        )

        user = User.objects.create(
            userUser = user_obj,
            account = Account.objects.get(name='Enterprise'),
        )

        image = Image.objects.create(                                       # def data Image
            user=User.objects.get(userUser=user_obj),
            img=File(open('media/home.jpg', 'rb')),
            delete_generated_link_time = 300,
            timestamp=datetime.datetime.now(),
        )


    def test_single_acount(self):                                           # test account
        acount_count = Account.objects.count()
        self.assertEqual(acount_count, 1)

    def test_single_user(self):                                             # test user
        user_count = Account.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_image(self):                                            # test image
        image_count = Account.objects.count()
        self.assertEqual(image_count, 1)

    def test_get_list(self):                                                # test list of items
        client = APIClient()
        client.login(username='testone', password='somepassword')   # authorization
        data = {}
        url = api_reverse("ImageDRF:ImageDRFapi")
        response = client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post(self):                                                    # test post
        client = APIClient()
        client.login(username='testone', password='somepassword')   # authorization
        data = {
            'img':File(open('media/home.jpg', 'rb')),
                'delete_generated_link_time':300
            }
        url = api_reverse("ImageDRF:ImageDRFapi")
        response = client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)