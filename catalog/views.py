from catalog.models import Product, Category
from django.shortcuts import render, get_object_or_404,redirect
from reviews.models import Review
from reviews.forms import ReviewForm
from django.contrib.auth.models import User 
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def home_page(request):
    return render(request,'catalog/home.html')

def product_list(request):
    products = Product.objects.all()
    category_db = Category.objects.all()
    context = {
        'products' : products,
        'categories': category_db,
    }
    return render(request, 'catalog/product_list.html',context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    form = ReviewForm()
    
    context = {
    'product': product,
    'reviews': reviews,
    'form': form, 
    }
    return render(request, 'catalog/product_detail.html', context)

def add_to_cart(request,product_id):
    product = get_object_or_404(Product, id = product_id)
    cart = request.session.get('cart', {})

    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1

    request.session['cart'] = cart 
    request.session.modified = True
    return redirect('catalog:product_detail', product_id = product.id)


def cart_view(request):
    cart = request.session.get('cart',{})
    product_ids = cart.keys()

    products = Product.objects.filter(id__in = product_ids)
    items = []
    total_price = 0
    for product in products:
        qty = cart[str(product.id)]
        line_price = product.price * qty
        total_price+= line_price
    
        items.append({
            'product': product,
            'qty': qty,
            'line_price': line_price
        })
    return render(request, 'catalog/cart.html',{
        'items':items,
        'total_price': total_price
    } )

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
    return redirect('catalog:cart_view')

def toggle_theme(request):
    current = request.COOKIES.get('theme', 'light')
    # Смотрим текущую тему в куках браузера: читаем cookie 'theme'
    # Если cookie нет, считаем, что тема по умолчанию - 'light'

    new = 'dark' if current == 'light' else 'light'
    # если сейчас светлая - переключаем на темную, иначе на светлую

    resp = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # Создаем ответ‑редирект на предыдущую страницу (HTTP_REFERER)
    # Если заголовка Referer нет, редиректим на корень ('/')

    resp.set_cookie('theme', new, max_age=60 * 60 * 24 * 30, samesite='Lax')
    # Записываем куку 'theme'
    # max_age - срок жизни cookie 30 дней (мы пишем в секундах)
    # samesite='Lax' - защита от CSRF‑атаки при кросссайтовых запросах

    return resp

@login_required
def chat_room(request):
    return render(request, 'catalog/chat.html')
