from django.core import paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = 999

    def get_paginated_response(self, data):
        code = 200
        msg = "success"
        res = {
            "page": int(self.get_page_number(self.request, paginator)) or 1,
            "total": self.page.paginator.count,
            "limit": int(self.get_page_size(self.request)) or 10,
            "data": data
        }
        if not data:
            msg = "暂无数据"
            res["data"] = []

        return Response(
            {
                "code": code,
                "msg": msg,
                "data": res
            }
        )

