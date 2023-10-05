from django.test import TestCase

from .models import Order
from customers.models import Customer


class OrderModelTest(TestCase):
    """
    Тест максимальной длины поля серийного номера в заказе.
    """
    @classmethod
    def setUpTestData(cls):
        test_customer = Customer.objects.create(email="testing@mail.ru")
        Order.objects.create(customer=test_customer,
                             robot_serial="R3-D2",
                             created="2023-09-30 20:59:59")

    def test_robot_serial_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('robot_serial').max_length
        self.assertEquals(max_length, 5)
