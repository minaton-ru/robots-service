from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import Order


class OrderCreateView(CreateView):
    model = Order
    fields = ["customer", "robot_serial"]
    template_name = "orders/order_add.html"
    success_url = reverse_lazy("order_add_success")


class OrderCreateSuccessView(TemplateView):
    template_name = "orders/order_add_success.html"
