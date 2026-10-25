from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Product


class ProductAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!",
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.product = Product.objects.create(
            name="Laptop",
            description="16GB RAM laptop",
            price=Decimal("55000.00"),
            stock_quantity=10,
            category="Electronics",
        )

        self.list_url = "/api/products/"
        self.detail_url = f"/api/products/{self.product.id}/"

        self.valid_payload = {
            "name": "Keyboard",
            "description": "Mechanical keyboard",
            "price": "2500.00",
            "stock_quantity": 20,
            "category": "Accessories",
        }

    def test_create_product(self):
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data["name"], "Keyboard")

    def test_fetch_product_list(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Laptop")

    def test_fetch_product_detail(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Laptop")
        self.assertEqual(response.data["category"], "Electronics")

    def test_update_product(self):
        payload = {
            "name": "Updated Laptop",
            "description": "Updated description",
            "price": "60000.00",
            "stock_quantity": 15,
            "category": "Computers",
        }

        response = self.client.put(
            self.detail_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()

        self.assertEqual(self.product.name, "Updated Laptop")
        self.assertEqual(self.product.price, Decimal("60000.00"))
        self.assertEqual(self.product.stock_quantity, 15)

    def test_delete_product(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Product.objects.filter(id=self.product.id).exists()
        )

    def test_negative_price_is_rejected(self):
        payload = {
            **self.valid_payload,
            "price": "-100.00",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)
        self.assertEqual(Product.objects.count(), 1)

    def test_zero_price_is_rejected(self):
        payload = {
            **self.valid_payload,
            "price": "0.00",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)

    def test_negative_stock_is_rejected(self):
        payload = {
            **self.valid_payload,
            "stock_quantity": -5,
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("stock_quantity", response.data)

    def test_unauthenticated_request_is_rejected(self):
        self.client.credentials()

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)