from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UniversalPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100
    invalid_page_message = "Invalid page"

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("page_number", self.page.number),
                    ("page_size", self.page.paginator.per_page),
                    ("page_count", self.page.paginator.num_pages),
                    ("results", data),
                ]
            )
        )
