import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myapp.models import MyModel


class MyModelTests(APITestCase):

    def setUp(self):
        # Create a sample record to test the READ operation
        self.my_model = MyModel.objects.create(
            name="Test Model",
            description="This is a test model"
        )
        self.url = reverse('mymodel-detail', args=[self.my_model.id])

    def test_create_my_model(self):
        """Test the CREATE operation (POST request) for MyModel"""
        url = reverse('mymodel-list')
        data = {
            'name': 'New Model',
            'description': 'Description for new model'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Model')
        self.assertEqual(response.data['description'], 'Description for new model')

    def test_read_my_model(self):
        """Test the READ operation (GET request) for MyModel"""
        # Perform a GET request to read the data
        response = self.client.get(self.url)

        # Assert that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the correct data
        self.assertEqual(response.data['name'], self.my_model.name)
        self.assertEqual(response.data['description'], self.my_model.description)

    def test_update_my_model(self):
        """Test the UPDATE operation (PUT request) for MyModel"""
        data = {
            'name': 'Updated Model',
            'description': 'Updated description for model'
        }
        response = self.client.put(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.my_model.refresh_from_db()  # Refresh the model instance with updated data
        self.assertEqual(self.my_model.name, 'Updated Model')
        self.assertEqual(self.my_model.description, 'Updated description for model')

    def test_delete_my_model(self):
        """Test the DELETE operation for MyModel"""
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MyModel.objects.filter(id=self.my_model.id).exists())
