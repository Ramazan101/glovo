from django.urls import path, include
from .views import (UserProfileListAPIView, UserProfileDetailAPIView, CategoryListAPIView,
                    CategoryDetailAPIView, StoresListAPIView, StoresDetailAPIView,
                    ProductViewSet, OrderViewSet, CourierGlovoViewSet, ReviewCreteAPIView, ReviewEditAPIView,
                    OrderStatusListViewSet, OrderStatusDetailViewSet, StoreViewSet, RegisterView, CustomLoginView, LogoutView)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('store_create', StoreViewSet)
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)
router.register('courier_glovo', CourierGlovoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('userprofile/', UserProfileListAPIView.as_view(), name='userprofile'),
    path('userprofile/<int:pk>/', UserProfileDetailAPIView.as_view(), name='userprofile_detail'),
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='categories_detail'),
    path('stores/', StoresListAPIView.as_view(), name='stores'),
    path('stores/<int:pk>/', StoresDetailAPIView.as_view(), name='stores_detail'),
    path('review/', ReviewCreteAPIView.as_view(), name='review_create'),
    path('review/<int:pk>/', ReviewEditAPIView.as_view(), name='review'),
    path('order/', OrderStatusListViewSet.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderStatusDetailViewSet.as_view(), name='order_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]