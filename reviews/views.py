from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from catalog.models import Product
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

@login_required
def add_review(request,product_id):
    product = get_object_or_404(Product, id = product_id)

    if request.method == 'POST': 
        form = ReviewForm(request.POST)
        if form.is_valid(): 
            new_review = form.save(commit=False)
            new_review.product = product 
            new_review.user = request.user 
            new_review.save() 
            
            
    return redirect('catalog:product_detail', product_id=product.id)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id = review_id, user = request.user)
    
    if request.method == "POST":
        form =  ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_detail', product_id = review.product.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/edit_review.html', {'form':form, 'review': review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id = review_id, user = request.user)
    product_id = review.product_id
    
    if request.method == "POST":
        form =  ReviewForm(request.POST, instance=review)
        review.delete()
        return redirect('catalog:product_detail', product_id = product_id)
    
    return render(request, 'reviews/confirm_delete.html', {'review': review})