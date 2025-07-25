from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Product
from .serializers import UserSerializer, ProductSerializer

# ✅ Frontend Pages
def home(request):
    return redirect('login')

def login_page(request):
    return render(request, "inventory/login.html")

def signup_page(request):
    return render(request, "inventory/signup.html")

def dashboard_view(request):
    return render(request, "inventory/dashboard.html")

# ✅ JWT Login (CSRF-Exempt)
@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(TokenObtainPairView):
    permission_classes = []
    authentication_classes = []

# ✅ User Registration
@method_decorator(csrf_exempt, name='dispatch')
class RegisterUser(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"username": user.username}, status=status.HTTP_201_CREATED)

# ✅ Get & Add Product
@method_decorator(csrf_exempt, name='dispatch')
class ProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        products = Product.objects.all().order_by('id')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

# ✅ Update Product (All fields except ID)
@method_decorator(csrf_exempt, name='dispatch')
class ProductUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data.pop("id", None)  # prevent ID overwrite
        serializer = ProductSerializer(product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# ✅ Update Quantity Only
@method_decorator(csrf_exempt, name='dispatch')
class UpdateQuantityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        qty = request.data.get("quantity", None)
        if qty is None:
            return Response({"detail": "Missing 'quantity' field"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            qty = int(qty)
            if qty < 0:
                raise ValueError("Quantity must be non-negative")
        except (ValueError, TypeError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        product.quantity = qty
        product.save()
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

# ✅ Delete Product
@method_decorator(csrf_exempt, name='dispatch')
class ProductDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
