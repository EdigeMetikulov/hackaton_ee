from apps.cart.models import ShoppingCart


def post_create_cart_signal(sender, created, instance, *args, **kwargs):
    if created:
        ShoppingCart.objects.create(user=instance)
