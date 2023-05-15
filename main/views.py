from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, CartForm
from .models import FoodProduct, Cart, Favorite, Order
from django.contrib.auth.decorators import login_required
from pixqrcode import PixQrCode
from django.db.models import Sum, F
from datetime import datetime, timedelta
from django.contrib import messages


def login(request):
    error_message = None

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            username = request.POST.get('Username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                print("User is authenticated")
                return redirect('home')
            else:
                print("User is not authenticated")
                error_message = "Invalid login credentials. Please try again."

        elif form_type == 'signup':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                print("User is created")
                return redirect('login')
            else:
                error_message = "Invalid sign up information. Please try again."
                print("User is not created")
                print(form.errors)
            error_message = "Invalid request."

    form = SignUpForm()
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

@login_required(login_url='login')
def catalog(request):
    pesquisa = request.GET.get('search', '')
    food_product = FoodProduct.objects.filter(name__icontains=pesquisa)
    return render(request, 'catalog.html', {'food_products': food_product})

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(FoodProduct, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, product=product, defaults={'quantity': 0})

    selected_quantity = int(request.POST.get('quantity', 1))

    if not created:
        cart.quantity += selected_quantity
    else:
        cart.quantity = selected_quantity

    cart.save()

    return redirect('home')



@login_required(login_url='login')
def product_detail_view(request, product_id):
    product = get_object_or_404(FoodProduct, id=product_id)
    quant, created = Cart.objects.get_or_create(user=request.user, product=product)
    context = {'product': product, 'quant': quant}
    return render(request, 'product_detail.html', context)

@login_required(login_url='login')
def remove_from_cart(request, product_id):
    product = get_object_or_404(FoodProduct, id=product_id)
    cart_item = get_object_or_404(Cart, user=request.user, product=product)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def increment_quantity(request, product_id):
    product = get_object_or_404(FoodProduct, id=product_id)
    product = Cart.objects.get(user=request.user, product=product)
    if product.quantity < 9:
        product.quantity += 1
        product.save()
    return redirect('cart')

@login_required(login_url='login')
def decrement_quantity(request, product_id):
    product = get_object_or_404(FoodProduct, id=product_id)
    product = Cart.objects.get(user=request.user, product=product)
    if product.quantity > 1:
        product.quantity -= 1
        product.save()
    return redirect('cart')

@login_required(login_url='login')
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return redirect('cart')

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items_total = []
    
    for item in cart_items:
        total = item.product.price * item.quantity
        cart_items_total.append((item, total))
    
    cart_total = sum([total for _, total in cart_items_total])
    
    if request.method == "POST":
        form = CartForm(request.POST)
        if form.is_valid():
            obs = form.cleaned_data["text_box_obs"]
            request.session["cart_obs"] = obs
            return redirect('cart')
    else:
        form = CartForm()

    context = {
        'cart_items_total': cart_items_total,
        'cart_total': cart_total,
        'form': form,
    }

    return render(request, 'cart.html', context)

@login_required(login_url='login')
def increment_quantity_prod_detail(request, product_id):
    product = get_object_or_404(FoodProduct, id=product_id)
    product = Cart.objects.get(user=request.user, product=product)
    if product.quantity < 9:
        product.quantity += 1
        product.save()
    return redirect( 'product_detail', product_id=product_id)

@login_required(login_url='login')
def decrement_quantity_prod_detail(request, product_id):
    product = get_object_or_404(FoodProduct, id=product_id)
    product = Cart.objects.get(user=request.user, product=product)
    if product.quantity > 1:
        product.quantity -= 1
        product.save()
    return redirect( 'product_detail', product_id=product_id )

@login_required(login_url='login')
def order_status(request):
    return render(request, 'order_status.html')

@login_required(login_url='login')
def generate_qr_code(request):
    name = 'Ana'
    mobile = '(81)992867651'
    city = 'Recife'

    cart_items = Cart.objects.filter(user=request.user)

    total = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total']

    if total is None:
        return render(request, 'payments/error.html', {'message': 'Cart is empty'})

    total_str = format(float(total), '.2f')

    pix = PixQrCode(name, mobile, city, total_str)

    if pix.is_valid():
        qr_base64 = pix.export_base64()
        return render(request, 'qr_code.html', {'qr_base64': qr_base64})
    else:
        return render(request, 'error.html', {'message': 'Invalid input fields'})

def payment(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total']
    total_str = format(float(total), '.2f') if total is not None else '0.00'

    if request.method == 'POST':
        payment_method = request.POST.get('payment-method')
        
        if payment_method == 'pix':
            return redirect('generate_qr_code')

    return render(request, 'payment.html', {'total': total_str})

@login_required(login_url='login')
def order_status(request):
    cart = Cart.objects.filter(user=request.user)
    total = cart.aggregate(total=Sum(F('product__price') * F('quantity')))['total']
    
    if request.method == 'POST':
        pickup_time = datetime.now() + timedelta(minutes=30)
        order_products = [f"{item.quantity}x {item.product.name}" for item in cart]
        order_summary = ", ".join(order_products)
        order = Order.objects.create(user=request.user, order=order_summary, total=total, 
        pickup_time=pickup_time)
        messages.success(request, 'Pedido realizado com sucesso!')        
        cart.delete()
    else:
        # busca o último pedido do usuário quando a requisição for 'GET'
        order = Order.objects.filter(user=request.user).last()

    context = {
        'order': order,
    }
    # renderiza o template order_status.html com as informações do pedido
    return render(request, 'order_status.html', context)
   
@login_required(login_url='login')
def add_to_cart_from_detail(request, product_id):
    product = get_object_or_404(FoodProduct, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.save()
    return redirect('home')