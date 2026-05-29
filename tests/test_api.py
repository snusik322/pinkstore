import pytest
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from catalog.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review



@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def category(db):
    return Category.objects.create(name="Смартфоны", slug="smartphones")


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        category=category,
        title="iPhone 15",
        description="Крутой телефон",
        price=Decimal("99999.99"),
        stock=10,
        is_available=True,
    )


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        password="pass123",
        email="alice@example.com",
    )


@pytest.fixture
def order(db, user):
    return Order.objects.create(user=user)


@pytest.fixture
def order_with_item(db, order, product):
    OrderItem.objects.create(
        order=order,
        product=product,
        price=Decimal("99999.99"),
        quantity=2,
    )
    return order


@pytest.fixture
def review(db, user, product):
    return Review.objects.create(
        product=product,
        user=user,
        text="Отличный телефон!",
        rating=5,
    )


@pytest.mark.django_db
def test_products_api_returns_list(api_client, product):
    """Список товаров: 200, один товар, нужные поля"""
    url = reverse("catalog:api_products-list")
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "iPhone 15"
    assert data[0]["price"] == "99999.99"


@pytest.mark.django_db
def test_product_detail(api_client, product):
    """Detail-эндпоинт товара возвращает правильный объект"""
    url = reverse("catalog:api_products-detail", kwargs={"pk": product.pk})
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "iPhone 15"
    assert data["price"] == "99999.99"



@pytest.mark.django_db
def test_categories_api_returns_list(api_client, category):
    """Список категорий: 200, одна категория, нужные ключи"""
    url = reverse("catalog:api_categories-list")
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Смартфоны"
    assert data[0]["slug"] == "smartphones"


@pytest.mark.django_db
def test_category_detail(api_client, category):
    """Detail-эндпоинт категории возвращает правильный объект"""
    url = reverse("catalog:api_categories-detail", kwargs={"pk": category.pk})
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Смартфоны"
    assert data["slug"] == "smartphones"



@pytest.mark.django_db
def test_orders_api_requires_auth(api_client, order):
    """Анонимный запрос к списку заказов должен вернуть 401/403"""
    url = reverse("orders:api_orders-list")
    response = api_client.get(url)

    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_orders_api_returns_list(api_client, user, order):
    """Авторизованный пользователь получает список заказов"""
    api_client.force_authenticate(user=user)
    url = reverse("orders:api_orders-list")
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == order.pk


@pytest.mark.django_db
def test_order_detail_contains_nested_items(api_client, user, order_with_item, product):
    """
    Detail-эндпоинт заказа содержит вложенный список items,
    product внутри item тоже вложенный объект, user — вложенный объект
    """
    api_client.force_authenticate(user=user)
    url = reverse("orders:api_orders-detail", kwargs={"pk": order_with_item.pk})
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert len(data["items"]) == 1

    item = data["items"][0]
    assert item["price"] == "99999.99"
    assert item["quantity"] == 2

    assert isinstance(item["product"], dict)
    assert item["product"]["title"] == "iPhone 15"
    assert item["product"]["price"] == "99999.99"
    assert isinstance(data["user"], dict)
    assert data["user"]["username"] == user.username



@pytest.mark.django_db
def test_reviews_api_returns_list(api_client, review):
    """Список отзывов доступен анонимно, возвращает 200 и один отзыв"""
    url = reverse("reviews:api_reviews-list")
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["text"] == "Отличный телефон!"
    assert data[0]["rating"] == 5



@pytest.mark.django_db
def test_reviews_create_requires_auth(api_client, product):
    """Анонимный пользователь не может создать отзыв"""
    url = reverse("reviews:api_reviews-list")
    payload = {"product_id": product.pk, "text": "Текст", "rating": 3}
    response = api_client.post(url, payload, format="json")

    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_api_me_returns_profile_for_authenticated_user(api_client, user):
    """Авторизованный пользователь получает свой профиль"""
    api_client.force_authenticate(user=user)
    url = reverse("users:api_my_profile")
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == user.username
    assert "phone" in data
    assert "address" in data


@pytest.mark.django_db
def test_api_me_requires_auth(api_client):
    """Анонимный запрос к /api/me/ должен вернуть 401/403"""
    url = reverse("users:api_my_profile")
    response = api_client.get(url)

    assert response.status_code in (401, 403)