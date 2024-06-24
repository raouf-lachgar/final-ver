from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .forms import CustomUserCreationForm

from .forms import ProductForm,CommentForm

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
#no longer predifined djnago user ;)
from .models import Product,custom_user,media_files,Wilaya,Rating,Comment,car_model,car_serie,piece
from .forms import ProductForm, RatingForm
from .filterForm import ProductFilter
#external db for willayas
#from algerography.models import Wilaya
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    wilayas = Wilaya.objects.all()
    car_models = car_model.objects.all()
    car_series = car_serie.objects.all()
    car_pieces = piece.objects.all()

    car_model_name = request.GET.get('car_model')
    car_series_name = request.GET.get('car_series')
    piece_name = request.GET.get('piece')
    wilaya_id = request.GET.get('wilaya')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.prefetch_related('media_files_set').all()

    if car_model_name:
        products = products.filter(car_model=car_model_name)

    if car_series_name:
        products = products.filter(car_serie=car_series_name)

    if piece_name:
        products = products.filter(piece=piece_name)

    if wilaya_id:
        products = products.filter(city_id=wilaya_id)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # Handle ordering based on sales
    if 'order_sales' in request.GET:
        if request.GET.get('order_sales') == 'desc':
            products = products.order_by('-sales')
        else:
            products = products.order_by('sales')

    context = {
        'products': products,
        'wilayas': wilayas,
        'car_models': car_models,
        'car_series': car_series,
        'car_pieces': car_pieces,
    }
    return render(request, 'users/user.html', context)




def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    user_products = Product.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, "users/profile.html", {'products': user_products})

def delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.user != request.user:
        messages.error(request, "You do not have permission to delete this product.")
        return redirect('profile')
    
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('profile')

def login_view(request):
    
    if request.method == "POST":
      username = request.POST["username"]
      password = request.POST["password"]
      user = authenticate(request, username=username, password=password)
      if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
      else:
        return render(request, "users/login.html",{
          "message" : "username or password is wrong"
        })
    return render(request, "users/login.html")



def logout_view(request):
  logout(request)
  return render(request, "users/login.html",{
    "message" : "logedout"

  })
def sign_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, "users/sign.html", {'form': form})
#added view ! (deleting user,update profile)
def userDelete_view(request):
    user = custom_user.objects.get(pk=request.user.id)
    Post = Product.objects.filter(user=request.user.id)
    Post.delete()
    logout(request)
    user.delete()
    return HttpResponseRedirect(reverse('index'))
def profileUpdate_view(request):
    if request.method == 'POST':
      username = request.POST['username']
      phone_num = request.POST['phone_num']
      user = custom_user.objects.get(pk=request.user.id)
      user.username = username
      user.phone_num = phone_num
      if request.FILES:
        profile_pic = request.FILES['profile_pic']
        user.profile_pic = profile_pic
      user.save()
      alert = True
      return HttpResponseRedirect(reverse('profile'))
def submit_product_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            if 'media' in request.FILES:
             for file in request.FILES.getlist('media'):
              media = media_files(product_id=product , path=file)
              media.save()
            messages.success(request, "Product submitted successfully!")
            return redirect('index')
        else:
            messages.error(request, "There was an error with your submission. Please check the form and try again.")
    else:
        form = ProductForm()
    
    return render(request, "users/submit_product.html", {'form': form}) #, 'city':Wilaya})
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product=product)
    comment_form = CommentForm()
    rating_form = RatingForm()

    if request.method == 'POST':
        if 'value' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                value = rating_form.cleaned_data['value']
                Rating.rate_product(user=request.user, product=product, value=value)
                return redirect('product_detail', product_id=product_id)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.product = product
                comment.save()
                return redirect('product_detail', product_id=product_id)

    return render(request, 'users/product_detail.html', {
        'product': product,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
    })

def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after editing
    else:
        form = ProductForm(instance=product)

    return render(request, 'users/edit_product.html', {'form': form, 'product': product})
def buy_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.quantity > 0:
        product.quantity -= 1
        product.sales += 1
        product.save()
    return redirect('index')

