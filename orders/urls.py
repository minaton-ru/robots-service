from django.urls import path
from . import views

urlpatterns = [
    path("order/add/",
         views.OrderCreateView.as_view(), name="order_add"),
    path("order/add/success/",
         views.OrderCreateSuccessView.as_view(), name="order_add_success"),
]
