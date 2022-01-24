''' Pagination classes for API. '''

from rest_framework.pagination import PageNumberPagination


class PageNumberLimitPagination(PageNumberPagination):
    '''
    PageNumberPagination class that supports page size as
    query parameter 'limit'.
    '''
    page_size_query_param = 'limit'
