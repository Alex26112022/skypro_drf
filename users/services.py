from datetime import datetime, timedelta

import stripe
from pytz import timezone

from config.settings import STRIPE_SECRET_KEY, TIME_ZONE
from users.models import User

stripe.api_key = STRIPE_SECRET_KEY

tz = timezone(TIME_ZONE)
logout_time_delta = timedelta(days=30)


def create_stripe_product(title, description):
    """ Создает продукт в Stripe. """
    product = stripe.Product.create(name=title, description=description)
    return product.get('id')


def create_stripe_price(amount, product_id):
    """ Создает цену в Stripe для оплаты курса. """
    return stripe.Price.create(
        currency="rub",
        product=product_id,
        unit_amount=amount * 100,
    )


def create_stripe_session(price):
    """ Создает сессию оплаты Stripe. """
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/api/users/stripe-payment/success-payment/",
        line_items=[
            {"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')


def get_status_payment(session_id):
    """ Проверяет статус платежа. """
    status = stripe.checkout.Session.retrieve(
        session_id,
    )
    return status.get('status')


def check_users_login_data():
    """ Проверяет дату крайнего входа пользователя. """
    users = User.objects.all()
    now = datetime.now(tz)
    for user in users:
        if user.last_login and user.is_active and (now - user.last_login) > logout_time_delta:
            user.is_active = False
            user.save()
            print(f'Пользователь {user.email} заблокирован!')
