from rest_framework.pagination import PageNumberPagination

class SearchResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class TinyResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class ItemResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CommentResultSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

class ImageResultSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100