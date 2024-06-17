# from django.conf.urls import url
from django.urls import path

from marketing.views import *

urlpatterns = [
    # marketing
    path('panel/marketing', marketing_index, name='marketing'),
    path('panel/marketing/create', marketing_create, name='marketing_create'),
    path('panel/marketing/update/<int:marketing_id>', marketing_update, name='marketing_update'),
    path('panel/marketing/delete/<int:marketing_id>', marketing_delete, name='marketing_delete'),
]