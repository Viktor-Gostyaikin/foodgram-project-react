''' Utils for API. '''

from django.db.models import Sum
from django.http import HttpResponse


def get_shopping_cart_file(user):
    data = (
        user.shopping_cart
            .values_list(
                'recipe__ingredients__ingredient__name',
                'recipe__ingredients__ingredient__measurement_unit',
            ).annotate(summary=Sum('recipe__ingredients__amount'))
    )
    items = (
        ['{} {}{}'.format(item[0], item[2], item[1]) for item in data]
    )
    response = HttpResponse(
        '\n'.join(items), content_type='text/plain; charset=utf-8'
    )
    response['Content-Disposition'] = ('attachment;'
                                       ' filename="shopping_cart.txt"')
    return response
