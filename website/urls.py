# from django.conf.urls import url
from django.urls import path

from website.views import *

urlpatterns = [
    #site
    path('panel/site', site_index, name='site'),
    path('panel/site/update/<int:site_id>', site_update, name='site_update'),
]