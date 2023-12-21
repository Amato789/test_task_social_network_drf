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

        self.valid_post_sample = {
            "title": "Test title 2",
            "text": "some text for test",
            "author": user_test.id,
        }
        self.invalid_post_sample = {
            "title": "",
            "text": "some text for test",
            "author": user_test.id,
        }

    def test_post_list_by_authorized_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Test title")
        self.assertEqual(response.data[0]["text"], "Test post text")
        self.assertEqual(response.data[0]["author"], 1)

    def test_post_detail_by_authorized_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('post_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), "Test title")
        self.assertEqual(response.json().get('text'), "Test post text")
        self.assertEqual(response.json().get('author'), 1)

    def test_fail_post_detail_by_authorized_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('post_detail', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_post_by_authorized_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('post_list'), self.valid_post_sample)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_post_by_authorized_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('post_list'), self.invalid_post_sample)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_list_by_unauthorized_user(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_detail_by_unauthorized_user(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_post_detail_by_unauthorized_user(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_by_unauthorized_user(self):
        response = self.client.post(reverse('post_list'), self.valid_post_sample)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_create_post_by_unauthorized_user(self):
        response = self.client.post(reverse('post_list'), self.invalid_post_sample)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LikeTests(APITestCase):

    def setUp(self):
        # create test-user and get jwt-access-token
        user_test = User.objects.create_user(username='test', password='1234')
        user_test.save()
        response = self.client.post(reverse('token_obtain_pair'),
                                    {'username': 'test', 'password': '1234'},
                                    format='json')
        self.token = response.data['access']

        post_test = Post.objects.create(title="Test title",
                                        text="Test post text",
                                        author=user_test)
        post_test.save()

        Like.objects.create(post=post_test,
                            user=user_test,
                            value=1)

        self.valid_like_sample = {
            "post": 1,
            "user": 1,
            "value": 1,
        }
        self.invalid_like_sample1 = {
            "post": 1,
            "user": 1,
            "value": 10,
        }
        self.invalid_like_sample2 = {
            "post": 10,
            "user": 1,
            "value": 1,
        }
        self.invalid_like_sample3 = {
            "post": 1,
            "user": 10,
            "value": 1,
        }

    def test_create_like_by_authorized_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('post_like'), self.valid_like_sample)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail1_create_like_by_authorized_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('post_like'), self.invalid_like_sample1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail2_create_like_by_authorized_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('post_like'), self.invalid_like_sample2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail3_create_like_by_authorized_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('post_like'), self.invalid_like_sample3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_like_analytics_by_authorized_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["likes"], 1)

    def test_create_like_by_unauthorized_user(self):
        response = self.client.post(reverse('post_like'), self.valid_like_sample)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail1_create_like_by_unauthorized_user(self):
        response = self.client.post(reverse('post_like'), self.invalid_like_sample1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail2_create_like_by_unauthorized_user(self):
        response = self.client.post(reverse('post_like'), self.invalid_like_sample2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail3_create_like_by_unauthorized_user(self):
        response = self.client.post(reverse('post_like'), self.invalid_like_sample3)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_analytics_by_unauthorized_user(self):
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
