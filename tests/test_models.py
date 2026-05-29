import pytest
from decimal import Decimal
from django.contrib.auth.models import User


from catalog.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review
from users.models import Profile

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
    )


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="pass123")


@pytest.fixture
def order(db, user):
    return Order.objects.create(user=user)

@pytest.mark.django_db
class TestCategory:
    def test_str(self, category):
        """Category.__str__ должен возвращать название категории"""
        assert str(category) == "Смартфоны"

@pytest.mark.django_db
class TestOrderItem:
    def test_price_snapshot(self, order, product):
        """Цена в OrderItem должна сохраняться как снимок на момент заказа и не меняться, если потом изменилась цена самого товара"""
        item = OrderItem.objects.create(
        order=order,
        product=product,
        price=Decimal("12345.00"),
        quantity=1,
        )
        product.price = Decimal("1.00")
        product.save()
        item.refresh_from_db()
        assert item.price == Decimal("12345.00")


@pytest.mark.django_db
class TestProfileSignals:
    def test_auto_created_on_user_create(self):
        """При создании User должен автоматически создаваться Profile"""
        new_user = User.objects.create_user(username="bob", password="pass")
        assert Profile.objects.filter(user=new_user).exists()


@pytest.mark.django_db
class TestProduct:
    def test_str(self, product):
        assert str(product) == "iPhone 15 (99999.99 руб.)"

    def test_defaults(self, category):
        p = Product.objects.create(
            category=category,
            title="Test",
            description="desc",
            price=Decimal("100.00"),
        )
        assert p.is_available is True
        assert p.stock == 0

    def test_cascade_delete_with_category(self, product, category):
        category.delete()
        assert not Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
class TestOrderItemProtect:
    def test_cannot_delete_product_in_order(self, order, product):
        from django.db.models import ProtectedError
        OrderItem.objects.create(order=order, product=product, price=product.price)
        with pytest.raises(ProtectedError):
            product.delete()


@pytest.mark.django_db
class TestProfileSignals:
    def test_no_duplicate_on_resave(self, user):
        user.save()  
        assert Profile.objects.filter(user=user).count() == 1