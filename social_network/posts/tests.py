from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Post, Like, User


class PostsTests(APITestCase):

    def setUp(self):
        # create test-user and get jwt-access-token
        user_test = User.objects.create_user(username='test', password='1234')
        user_test.save()
        response = self.client.post(reverse('token_obtain_pair'),
                                    {'username': 'test', 'password': '1234'},
                                    format='json')
        self.token = response.data['access']

        # create post
        Post.objects.create(title="Test title",
                            text="Test post text",
                            author=user_test)

        # sample of post
        self.data = {
            "title": "Test title 2",
            "text": "some text for test",
            "author": user_test.id,
        }

    def test_post_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Test title")

    def test_post_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('post_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test title")

    def test_fail_post_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('post_detail', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_detail2(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('post_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), "Test title")

    def test_create_post_by_unauthorized_user(self):
        response = self.client.post(reverse('post_list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_by_authorized_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('post_list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
