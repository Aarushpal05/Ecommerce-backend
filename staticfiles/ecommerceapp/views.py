from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from .forms import *
from .models import *
# from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from .serializers import *


@api_view(['POST'])

def signupAPI(request):
    username = request.data.get('username')
    email= request.data.get('email')
    password = request.data.get('password')

    # Basic validation
    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if user exists
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already taken"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response(
        {"message": "User created successfully"},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def loginAPI(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    return Response({
        "username": request.user.username,
        "email": request.user.email
    })

@login_required    
def home(request):
    now = timezone.now()
    today = now.date()

    new_customers = User.objects.filter(date_joined__date=today).count()
    new_orders = Order.objects.filter(created_at__date=today).count()
    completed_orders = Order.objects.count()

    sales_today = Order.objects.filter(created_at__date=today).aggregate(total=Sum('total_price'))['total'] or 0
    sales_monthly = Order.objects.filter(created_at__year=now.year, created_at__month=now.month).aggregate(total=Sum('total_price'))['total'] or 0
    sales_yearly = Order.objects.filter(created_at__year=now.year).aggregate(total=Sum('total_price'))['total'] or 0

    return render(request, 'index.html', {
        'new_customers': new_customers,
        'new_orders': new_orders,
        'completed_orders': completed_orders,
        'sales_today': sales_today,
        'sales_monthly': sales_monthly,
        'sales_yearly': sales_yearly,
    })

@login_required
def addproduct(request):

    categorylist= category.objects.all()

    if request.method=='POST':
        data= productForm(request.POST, request.FILES)
        data.save()
    return render(request, 'add-product.html', {'categories': categorylist})

@login_required
def addcategory(request):
    if request.method=='POST':
        data= categoryForm(request.POST, request.FILES)
        data.save()
    return render(request, 'add-category.html')


def delete_category(request, id):
    category.objects.get(id=id).delete()
    return redirect('category_list')

def update_category(request, id):
    cat = category.objects.get(id=id)
    if request.method == "POST":
        data= categoryForm(request.POST, request.FILES, instance=cat)
        data.save()
        return redirect('category_list')  # change to your page name

    return render(request, 'update-category-form.html', {'category': cat})

@login_required
def product_list(request):
    data = AddProduct.objects.all()
    return render(request, 'view-product.html', {'products': data})

@api_view(['GET'])
def product_list_api(request):
    products = AddProduct.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_list_api(request):
    categories = category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@login_required
def category_list(request):
    categories = category.objects.all()
    return render(request, 'view-category.html', {'categories': categories})

@login_required
def editProduct(request, id):
    product= AddProduct.objects.get(id=id)
    categories= category.objects.all()

    if request.method=="POST":
            product= AddProduct.objects.get(id=id)
            data= productForm(request.POST, request.FILES, instance=product)
            print(data.errors)
            data.save()
            return redirect('product_list')
    
    return render(request, 'update-product-form.html', {'data': product, 'categories': categories})

@login_required
def deleteproduct(request,id):
     product = AddProduct.objects.get(id=id)
     product.delete()
     return redirect('product_list')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)   # session create hota hai
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('loginadmin')


@api_view(['GET'])
def product_detail(request, id):
    product = AddProduct.objects.get(id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

from django.http import JsonResponse

@api_view(['GET'])
def Productsbycategory(request, category_id):
    try:
        products = AddProduct.objects.filter(category_id=category_id)

        data = []
        for p in products:
            data.append({
                'id': p.id,
                'name': p.name,
                'price': str(p.price), 
                'pic': p.pic.url# ✅ convert Decimal to string
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    product_id = request.data.get('product_id')

    try:
        product = AddProduct.objects.get(id=product_id)
    except AddProduct.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return Response({"message": "Added to cart"})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart = Cart.objects.filter(user=request.user)    
    serializer = CartSerializer(cart, many=True)
    return Response(serializer.data)

# UPDATE CART QUANTITY
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart(request, pk):
    try:
        cart_item = Cart.objects.get(id=pk, user=request.user)

        quantity = request.data.get("quantity")

        cart_item.quantity = quantity
        cart_item.save()

        return Response({
            "message": "Cart updated successfully"
        })

    except Cart.DoesNotExist:
        return Response({
            "error": "Cart item not found"
        }, status=404)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart(request, pk):
    try:
        cart_item = Cart.objects.get(id=pk, user=request.user)

        cart_item.delete()

        return Response({
            "message": "Item deleted successfully"
        })

    except Cart.DoesNotExist:
        return Response({
            "error": "Cart item not found"
        }, status=404)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import OrderSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        order = serializer.save()

        cart_item = Cart.objects.filter(user=request.user)
        cart_item.delete()      

        payment_link = ""

        if order.payment_method == "ONLINE":
            payment_link = (
                f"https://your-payment-gateway.com/pay/{order.id}"
            )

            order.payment_link = payment_link
            order.save()    

            

        return Response({
            "message": "Order placed successfully",
            "order_id": order.id,
            "payment_link": payment_link
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    recent_order = orders.first()
    history = orders[:5]

    return Response({
        'recent_order': OrderSerializer(recent_order).data if recent_order else None,
        'last_5_orders': OrderSerializer(history, many=True).data
    })


# def orderview(request):
#     orders = Order.objects.all().order_by('-created_at')
#     return render(request, 'order-view.html', {'orders': orders})

def order_view(request):

    # Logged-in user orders
    orders = Order.objects.all().order_by('-created_at')

    context = {
        'orders': orders
    }

    return render(request, 'order-view.html', context)

def delete_order(request, id):
    order= Order.objects.get(id=id)
    order.delete()
    return redirect('order_list')



def order_item(request, id):
    order = Order.objects.get(id=id)

    items = OrderItem.objects.filter(order=order)

    grand_total = 0
    for item in items:
        grand_total += item.total_price

    return render(request, 'orderitem.html', {
        'items': items,
        'order': order,
        'grand_total': grand_total,
    })
    