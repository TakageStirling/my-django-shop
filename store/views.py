from django.shortcuts import render
from .models import Product
import stripe
from django.conf import settings
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })

def checkout(request, product_id):
    product = Product.objects.get(id=product_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': int(product.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return JsonResponse({'id': session.id})
