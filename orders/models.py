from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    created_at = models.DateTimeField('Дата заказа',auto_now_add=True)
    is_paid = models.BooleanField('Оплачено',default=False)

    class Meta:
        verbose_name  = 'Заказ',
        verbose_name_plural  = 'Заказы'
    
    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name= 'Заказ')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name= 'Товар')
    price = models.DecimalField('Цена',max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество',default=1)

    class Meta:
        verbose_name  = 'Товар в заказе',
        verbose_name_plural  = 'Товары в заказе'
    
    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"
