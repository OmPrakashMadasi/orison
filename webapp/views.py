from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import *
from uuid import uuid4
from django.utils.text import slugify
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import urllib.parse
from datetime import datetime, timedelta


# Create your views here.

# def regenerate_slugs():
#     for school in School.objects.all():
#         school.slug = slugify(school.name) + '-' + str(uuid4())
#         school.save()
#
# regenerate_slugs()

# def regenerate_category_slugs():
#     for category in Categories.objects.all():
#         category.slug = generate_category_slug(category.name)
#         category.save()
# regenerate_category_slugs()

# Registration views :-
def register_user(request, slug):
    schools = School.objects.all()
    school = get_object_or_404(School, slug=slug)
    query = request.GET.get('query', '')
    if query:
        # If a query is provided, filter the schools by name
        schools = schools.filter(name__icontains=query)
        if schools.exists():
            # Redirect to the register page of the first matched school
            return redirect('register', slug=schools.first().slug)
        else:
            # Show a message if no schools are found
            messages.success(request, f"No schools found for '{query}'.")
            return redirect('home')
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            profile, created = Profile.objects.get_or_create(user=user)
            profile.school = school
            profile.save()
            mobile_number = request.POST.get('mobile_number')

            if mobile_number:
                profile.mobile_number = mobile_number
                profile.save()

            # Store the selected school in the session
            request.session['school_slug'] = school.slug

            messages.success(request, 'Registration is Successful, Please Login!!!...')
            return redirect('login', slug=school.slug)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect('register', slug=slug)
    else:
        return render(request, 'registration/register.html', {'form': form, 'school': school, 'schools': schools})



def login_user(request, slug):
    # Get the school object by slug
    school = get_object_or_404(School, slug=slug)
    schools = School.objects.all()

    # Handling search query for schools
    query = request.GET.get('query', '')
    if query:
        schools = schools.filter(name__icontains=query)
        if schools.exists():
            return redirect('register', slug=schools.first().slug)
        else:
            messages.success(request, f"No schools found for '{query}'.")
            return redirect('home')

    if request.method == 'POST':
        username_or_email_or_mobile = request.POST.get('username_or_email_or_mobile')  # Username/email/mobile input
        password = request.POST['password']

        # Try to authenticate the user using username, email, or mobile number
        user = None

        # Check if it's an email
        if '@' in username_or_email_or_mobile:
            user = User.objects.filter(email=username_or_email_or_mobile).first()

        # Check if it's a mobile number
        elif username_or_email_or_mobile.isdigit():
            user = User.objects.filter(profile__mobile_number=username_or_email_or_mobile).first()

        # Otherwise, treat it as a username
        else:
            user = User.objects.filter(username=username_or_email_or_mobile).first()

        if user:
            # Authenticate the user with the given password
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                # Retrieve the profile and check if the user's school matches the selected school
                try:
                    profile = Profile.objects.get(user=user)
                except Profile.DoesNotExist:
                    messages.error(request, 'Profile not found for the user.')
                    return redirect('login', slug=slug)

                if profile.school.id == school.id:
                    login(request, user)
                    request.session['school_slug'] = school.slug  # Store the school slug in session
                    return redirect('school_detail', slug=school.slug)
                else:
                    messages.error(request, 'The user does not belong to the selected school.')
            else:
                messages.error(request, 'Invalid username, email, or password.')
        else:
            messages.error(request, 'No account found with that username, email, or mobile number.')

    # Render the login page with schools and selected school context for GET requests
    return render(request, 'registration/login.html', {'schools': schools, 'school': school})



def logout_user(request):
    # Clear the school slug from session on logout
    if 'school_slug' in request.session:
        del request.session['school_slug']

    logout(request)
    messages.success(request, "You have successfully logged out from the Orison world!!!")
    return redirect('home')


def home(request):
    schools = School.objects.all()
    query = request.GET.get('query', '')
    if query:
        # If a query is provided, filter the schools by name
        schools = schools.filter(name__icontains=query)
        if schools.exists():
            # Redirect to the register page of the first matched school
            return redirect('register', slug=schools.first().slug)
        else:
            # Show a message if no schools are found
            messages.success(request, f"No schools found for '{query}'.")
            return redirect('home')

    cart_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()
    else:
        cart_count = request.session.get("cart_count", 0)

    return render(request, 'index.html',
                  {'schools': schools, 'query': query, 'school': schools.first(), 'cart_count': cart_count})


def about(request):
    schools = School.objects.all()
    query = request.GET.get('query', '')
    if query:
        # If a query is provided, filter the schools by name
        schools = schools.filter(name__icontains=query)
        if schools.exists():
            # Redirect to the register page of the first matched school
            return redirect('register', slug=schools.first().slug)
        else:
            # Show a message if no schools are found
            messages.success(request, f"No schools found for '{query}'.")
            return redirect('about')

    cart_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()
    else:
        cart_count = request.session.get("cart_count", 0)

    return render(request, 'about.html',
                  {'schools': schools, 'query': query, 'school': schools.first(), 'cart_count': cart_count})


def contact(request):
    schools = School.objects.all()
    query = request.GET.get('query', '')
    if query:
        # If a query is provided, filter the schools by name
        schools = schools.filter(name__icontains=query)
        if schools.exists():
            # Redirect to the register page of the first matched school
            return redirect('register', slug=schools.first().slug)
        else:
            # Show a message if no schools are found
            messages.success(request, f"No schools found for '{query}'.")
            return redirect('contact')

    cart_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()
    else:
        cart_count = request.session.get("cart_count", 0)

    return render(request, 'ContactUs.html',
                  {'schools': schools, 'query': query, 'school': schools.first(), 'cart_count': cart_count})


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        Message.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, 'Message sent successfully, We will get in touch!!!')
        return redirect('contact')
    messages.error(request, 'Invalid Details')
    return redirect('home')


def school_detail(request, slug):
    # First, check if a school is stored in the session
    school_slug = request.session.get('school_slug', None)

    # If a school is in session, use it, otherwise, use the slug from the URL
    if school_slug:
        school = get_object_or_404(School, slug=school_slug)
    else:
        school = get_object_or_404(School, slug=slug)

    # Check if the logged-in user belongs to the school being viewed
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        if user_profile.school.slug != school.slug:
            return redirect('login')  # Redirect to login or show an error message
    else:
        return redirect('home')  # Redirect to login if the user is not authenticated

    categories = Categories.objects.filter(school=school).order_by('sequence')

    # Get the user's cart
    cart = get_user_cart(request)
    cart_count = cart.items.count() if cart else 0

    # categories = Categories.objects.filter(product__school=school).distinct()

    # Add pagination here
    products_by_category = {}
    for category in categories:
        products = Product.objects.filter(school=school, category=category).prefetch_related('sizes')
        paginator = Paginator(products, 8)  # 8 products per page
        page_number = request.GET.get(f'page_{category.slug}', 1)

        try:
            products_page = paginator.page(page_number)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)

        products_by_category[category] = products_page

    return render(request, 'schoolscreens/school_detail.html', {
        'school': school,
        'categories': categories,
        'products_by_category': products_by_category,
        'cart': cart,
        'cart_count': cart_count,
    })


def get_user_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key or request.session.create()
        cart, _ = Cart.objects.get_or_create(session_id=session_id)

    return cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    size_id = request.POST.get("size")
    size = Size.objects.get(id=size_id) if size_id else None

    # Get the quantity from the form input, default to 1 if not provided
    quantity = int(request.POST.get("quantity", 1))

    # Check if there is enough stock of the product
    if product.stock < quantity:
        messages.error(request, 'Sorry, we don’t have enough stock of this product!')
        return redirect("school_detail", slug=product.school.slug)

    # Check if the item already exists in the cart with the same size
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size
    )

    if not created:
        # If the item already exists in the cart, update the quantity
        cart_item.quantity += quantity  # Add the new quantity to the existing one
        cart_item.save()
    else:
        # If it's a new item, set the quantity directly
        cart_item.quantity = quantity
        cart_item.save()

    # Decrease the product stock after adding it to the cart
    product.stock -= quantity
    product.save()

    # Update the session cart count after modifying the cart
    request.session["cart_count"] = CartItem.objects.filter(cart=cart).count()

    messages.success(request, 'Product added to cart!')
    return redirect("school_detail", slug=product.school.slug)


def cart_summary(request, slug):
    school = get_object_or_404(School, slug=slug)
    cart = Cart.objects.get(user=request.user) if request.user.is_authenticated else None
    cart_count = cart.items.count() if cart else 0

    total_price = sum(
        (item.product.price or 0) * (item.quantity or 1)  # Default price to 0 and quantity to 1 if None
        for item in cart.items.all()
    ) if cart else 0

    context = {
        'cart': cart,
        'cart_count': cart_count,
        'total_price': total_price,
        'school': school,
    }
    return render(request, 'summary/cart_summary.html', context)


def remove_from_cart(request, item_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = cart.items.filter(id=item_id).first()

    if cart_item:
        # Get the product associated with the cart item
        product = cart_item.product

        # Restore the product stock after removal
        product.stock += cart_item.quantity
        product.save()

        # Get the school slug for redirection
        school_slug = cart_item.product.school.slug

        # Remove the cart item from the cart
        cart_item.delete()

        # Update the session cart count after removal
        request.session['cart_count'] = cart.items.count()

        # Show a success message
        messages.success(request, 'Product is Removed!!!')

        # Redirect back to the cart summary page (or another appropriate page)
        return redirect('cart_summary', slug=school_slug)

    # If no cart item found, fallback to home or another page
    return redirect('home')


@csrf_exempt
def update_cart_quantity(request):
    if request.method == "POST":
        data = json.loads(request.body)
        item_id = data.get("item_id")
        new_quantity = data.get("quantity")

        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.quantity = new_quantity
            cart_item.save()
            return JsonResponse({"success": True})
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "Item not found"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def cart_count_api(request):
    cart_count = request.session.get('cart_count', 0)
    return JsonResponse({"cart_count": cart_count})


def checkout(request, slug):
    school = get_object_or_404(School, slug=slug)

    if request.method == 'POST':
        # Get form data directly from POST
        name = request.POST.get("name")
        student_class = request.POST.get("class")
        section = request.POST.get("section")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # # Basic validation (you can expand this)
        # if not all([name, student_class, section, phone, address]):
        #     messages.error(request, "All fields are required!")
        #     return redirect("checkout", slug=slug)  # Assumes a GET redirect to same page

        # Get the user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            messages.error(request, "No cart found!")
            return redirect("cart_summary", slug=slug)

        if not cart.items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect("cart_summary", slug=slug)

        # Calculate total price from cart
        total_price = sum((item.product.price or 0) * item.quantity for item in cart.items.all())

        # Create the order
        order = Order.objects.create(
            user=request.user,
            school=school,
            name=name,
            student_class=student_class,
            section=section,
            phone=phone,
            address=address,
            total_price=total_price,  # Set initially from cart
        )

        # Transfer cart items to OrderItem
        for cart_item in cart.items.all():
            product_price = cart_item.product.price or 0  # Ensure price is not None
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                size=cart_item.size,
                price=product_price,  # Use actual product price
            )

        # Format items for WhatsApp message
        items_message = "\n".join(
            f"*Product:* {item.product.name}\n*Quantity:* {item.quantity}\n*Size:* {item.size.size if item.size else 'No Size'}\n*Price:* ₹{(item.product.price or 0) * item.quantity}"
            for item in cart.items.all()
        )

        # Clear the cart
        cart.items.all().delete()
        request.session["cart_count"] = 0

        # Calculate delivery date
        delivery_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')

        # Create WhatsApp message
        message = (
            f"Hello {name},\n\n"
            f"your order will be ready to pickup from the store , payment to be done during the delivery time\n"
            f"*School:* {school.name}\n"
            f"*Class/Section:*({student_class}/{section})\n"
            f"*Address:* {address}\n"
            f"*Items:*\n{items_message}\n"
            f"*Total Price:* ₹{total_price}\n"
            f"*Delivery Date:* {delivery_date}\n\n"
            f"Thank you for shopping with us!"
        )
        encoded_message = urllib.parse.quote(message)
        whatsapp_link = f"https://wa.me/+919550590693?text={encoded_message}"  # Hardcoded as per your original

        messages.success(request, f"Order placed successfully!")
        return redirect(whatsapp_link)

    # For GET requests, you’d need a template (not provided in your original)
    return redirect("home", slug=slug)  # Fallback as per your original



def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)