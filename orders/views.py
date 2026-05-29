from django.shortcuts import render
from .models import Order

def order_list_view(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})