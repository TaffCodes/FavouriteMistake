from django.urls import path, include
from django.contrib import admin
from .views import hello_world

urlpatterns = [
    path('hello/', hello_world),
]

# from django.urls import path
# from .views import report_lost_item, report_found_item, item_details

# urlpatterns = [
#     path('report-lost/', report_lost_item, name='report_lost'),
#     path('report-found/', report_found_item, name='report_found'),
#     path('item-details/<int:id>/', item_details, name='item_details'),
# ]
