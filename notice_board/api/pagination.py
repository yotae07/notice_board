from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    default_limit = 25

    def get_next_link(self):
        return ''

    def get_previous_link(self):
        return ''
