from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    '''
    Task to sent an email notification when an order has been successfully created
    '''
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order_id}'
    message = f'Dear {order.first_name},\n\nYou have successfully cteated an order.\'' \
              f'Your order id is {order.id}'
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent