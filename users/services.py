import stripe
from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_price(amount):
    """ Создает цену в Stripe для оплаты курса. """
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": "Course Payment"},
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
