from rest_framework import  pagination


class CommentPagination(pagination.PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'  
    max_page_size = 100  


class NotificationPagination(pagination.PageNumberPagination):
    page_size = 1000