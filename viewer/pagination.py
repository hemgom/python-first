from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'histories': data,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'total_count': self.page.paginator.count
        })
