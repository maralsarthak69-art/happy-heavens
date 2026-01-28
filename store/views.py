from django.shortcuts import render, get_object_or_404, redirect # <--- Added get_object_or_404
from .models import Product
from .forms import CustomRequestForm
from .cart import Cart
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from .forms import CustomRequestForm, SignUpForm, LoginForm # <--- Added SignUpForm, LoginForm

def product_list(request):
    # Fetch all products from the database
    products = Product.objects.all()
    # Send them to the index.html template
    return render(request, 'index.html', {'products': products})

# --- NEW FUNCTION ADDED BELOW ---
def product_detail(request, pk):
    # 'pk' is the Primary Key (ID) passed from the URL
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def customize_idea(request):
    if request.method == 'POST':
        form = CustomRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'customize_success.html') # We will make this simple page next
    else:
        form = CustomRequestForm()
    
    return render(request, 'customize.html', {'form': form})

def add_to_cart(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.add(product=product)
    
    # After adding, stay on the same page but show the updated quantity
    return redirect('product_detail', pk=pk)

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart_summary.html', {'cart': cart})

def remove_from_cart(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.remove(product)
    return redirect('cart_summary')

def search(request):
    query = request.GET.get('q') # Get what the user typed
    results = []

    if query:
        # Search in the Name OR the Description (icontains means case-insensitive)
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'search_results.html', {'query': query, 'results': results})

def category_detail(request, category_name):
    # Filter products where the category name matches exactly
    products = Product.objects.filter(category__name=category_name)
    
    return render(request, 'category_detail.html', {
        'products': products, 
        'category_name': category_name
    })

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log them in immediately after signing up
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # 'next' handles the "redirect back" logic (e.g., if they were at checkout)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')