''' Utils for API. '''
import pdfkit

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
    pdf = pdfkit.from_string('\n'.join(items), 'shopping_cart.pdf')
    response = HttpResponse(
        pdf, content_type='application/pdf'
    )
    response['Content-Disposition'] = ('attachment;'
                                       ' filename="shopping_cart.pdf"')
    return response
