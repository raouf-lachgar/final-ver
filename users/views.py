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
from .models import Product,custom_user,media_files,Wilaya,Rating,Comment,car_model,car_serie,piece,SavedProduct,Purchase
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



def save_product(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to save a product.')
        return redirect('login')
    
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        saved_product, created = SavedProduct.objects.get_or_create(user=request.user, product=product)
        if created:
            messages.success(request, 'Product saved successfully.')
        else:
            messages.info(request, 'Product already saved.')
    
    return redirect('product_detail', product_id=product_id)
def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user_products = Product.objects.filter(user=request.user).order_by('-created_at')
    saved_products = SavedProduct.objects.filter(user=request.user).select_related('product')
    user_orders = Purchase.objects.filter(user=request.user)

    return render(request, "users/profile.html", {
        'products': user_products,
        'saved_products': saved_products,
        'orders': user_orders,
    })
def remove_saved_product(request, product_id):
    if request.method == 'POST':
        saved_product = get_object_or_404(SavedProduct, product_id=product_id, user=request.user)
        saved_product.delete()
        messages.success(request, 'Product removed from saved list.')
    return redirect('cart')
    
    return HttpResponseRedirect(reverse('profile'))
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
    if not request.user.subscribed:
        return redirect('subscribe')
    from .models import car_serie,car_model,piece
    # Get all wilayas for the form select options
    wilayas = Wilaya.objects.all()
    # Get all car models, series, and pieces for the form select options
    
    # Get all car models, series, and pieces for the form select options
    car_models = car_model.objects.all()
    car_series = car_serie.objects.all()
    pieces = piece.objects.all()

    if request.method == 'POST':
        # Retrieve form data from request.POST
        name = request.POST.get('name')
        car_model_id = request.POST.get('car_model')
        car_serie_id = request.POST.get('car_serie')
        piece_id = request.POST.get('piece')
        price = request.POST.get('price')
        phone_number = request.POST.get('phone_number')
        state = request.POST.get('state')
        city_id = request.POST.get('city')  # Assuming you have a select field named 'city' in your HTML form
        
        # Get the selected wilaya
        city = Wilaya.objects.get(pk=city_id)
        
        # Get the selected car model, serie, and piece
        car_model = car_model.objects.get(pk=car_model_id)
        car_serie = car_serie.objects.get(pk=car_serie_id)
        piece = piece.objects.get(pk=piece_id)

        # Create a new product instance
        product = Product.objects.create(
            user=request.user,
            name=name,
            car_model=car_model,
            car_serie=car_serie,
            piece=piece,
            price=price,
            phone_number=phone_number,
            state=state,
            city=city
        )

        # Handle media files upload if necessary
        if 'media' in request.FILES:
            for file in request.FILES.getlist('media'):
                media = media_files(product_id=product, path=file)
                media.save()

        # Redirect or show success message
        messages.success(request, "Product submitted successfully!")
        return redirect('index')

    return render(request, "users/submit_product.html", {'wilayas': wilayas, 'car_models': car_models, 'car_series': car_series, 'pieces': pieces})
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product=product)

    if request.method == 'POST':
        if 'rating' in request.POST:
            rating_value = int(request.POST.get('rating'))
            if 1 <= rating_value <= 5:
                Rating.rate_product(user=request.user, product=product, value=rating_value)
                messages.success(request, "Thank you for rating this product!")
            else:
                messages.error(request, "Rating must be between 1 and 5.")
        elif 'comment' in request.POST:
            comment_content = request.POST.get('comment')
            if comment_content.strip():
                Comment.objects.create(user=request.user, product=product, content=comment_content)
                messages.success(request, "Your comment has been submitted!")
            else:
                messages.error(request, "Comment cannot be empty.")

        return redirect('product_detail', product_id=product_id)

    return render(request, 'users/product_detail.html', {
        'product': product,
        'comments': comments,
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

def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        card_number = request.POST.get('card_number')
        secret_number = request.POST.get('secret_number')
        product.sales += 1
        product.save()
        # Create a new purchase entry
        purchase = Purchase.objects.create(
            user=request.user,
            product=product,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            card_number=card_number,
            secret_number=secret_number
        )

        # Redirect to the product detail page
        return redirect('product_detail', product_id=product.id)

    return render(request, 'users/buy.html', {'product': product})
def cancel_order(request, order_id):
    order = get_object_or_404(Purchase, id=order_id)
    
    if request.method == 'POST':
        if order.status == 'PROCESS':
            order.status = 'CANCELLED'
            order.save()
            messages.success(request, 'Order cancelled successfully.')
        else:
            messages.error(request, 'This order cannot be cancelled.')
            
        # Delete the order if it's cancelled
        if order.status == 'CANCELLED':
            order.delete()
        
    return redirect('cart')
def product_orders(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    orders = Purchase.objects.filter(product=product)
    
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id')
        action = request.POST.get('action')
        
        if action == 'shipped':
            purchase = get_object_or_404(Purchase, id=purchase_id)
            purchase.status = 'SHIPPED'
            purchase.save()
    
    return render(request, 'users/cart.html', {'product': product, 'orders': orders})
def subscribe_view(request):
    if request.method == 'POST':
        # Handle subscription logic here
        request.user.subscribed = True
        request.user.save()
        messages.success(request, "Subscription successful! You can now submit a product.")
        return redirect('submit_product')
    else:
        # For GET request, show the subscription form
        if request.user.subscribed:
            return redirect('submit_product')

    return render(request, "users/subscribe.html")

def cart_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    
    saved_products = SavedProduct.objects.filter(user=request.user).select_related('product')
    user_orders = Purchase.objects.filter(user=request.user)

    return render(request, "users/cart.html", {
        
        'saved_products': saved_products,
        'orders': user_orders,
    })