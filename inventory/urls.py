from django.urls import path
from .views import (
    home, login_page, signup_page, dashboard_view,
    RegisterUser,
    ProductView, ProductUpdateView, UpdateQuantityView, ProductDeleteView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('signup/', signup_page, name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # ✅ Refresh token
    path('api/signup/', RegisterUser.as_view(), name='signup_api'),               # ✅ Signup

    path('api/products/', ProductView.as_view(), name='products'),
    path('api/products/<int:pk>/', ProductUpdateView.as_view(), name='update-product'),
    path('api/products/<int:pk>/quantity/', UpdateQuantityView.as_view(), name='update-quantity'),
    path('api/products/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete-product'),
]
