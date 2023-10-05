from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Robot
from orders.models import Order


@receiver(post_save, sender=Robot)
def new_robot_from_order_handler(sender, instance, **kwargs):
    """
    Обрабатывает событие создания нового робота.
    Если есть заказ на созданного робота с таким серийным номером,
    # то высылается письмо на email клиента,
    # который создал этот заказ раньше других клиентов.
    """

    # Кверисет заказов с серийным номером нужного робота, со статусом активный.
    # Берем заказ, который был создан раньше всех.
    order_serial = instance.serial
    order_this_robot = (
        Order.objects.filter(robot_serial=order_serial, active=True)
        .select_related("customer")
        .order_by("created")
        .first()
    )

    # Если такой заказ существует
    if order_this_robot:

        # У заказа снимаем флаг активного
        order_this_robot.active = False
        order_this_robot.save()

        # Отправляем письмо клиенту
        email_subject = "Робот в наличии"
        email_from = "bst@bst-mc.com"
        email_to = order_this_robot.customer.email
        email_message = (
            "Добрый день!\n\n"
            f"Недавно вы интересовались нашим роботом модели {instance.model},\
            версии {instance.version}.\n\n"
            "Этот робот теперь в наличии. Если вам подходит этот вариант - \
            пожалуйста, свяжитесь с нами"
        )
        send_mail(email_subject, email_message,
                  email_from, [email_to], fail_silently=False,)
