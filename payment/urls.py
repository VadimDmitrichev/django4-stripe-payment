"""stripe_payment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from payment import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('buy/<pk>/', views.CreateCheckoutSessionView.as_view(), name='buy'),
    path('buy_order/', views.CreateOrderCheckoutSessionView.as_view(), name='buy_order'),
    path('add/<pk>/', views.AddItemInOrderView.as_view(), name='add'),
    path('delete/<pk>/', views.DeleteItemFromOrder.as_view(), name='delete'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('item/<pk>/', views.ItemView.as_view(), name='item'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
]
