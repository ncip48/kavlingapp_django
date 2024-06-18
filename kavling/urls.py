# from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [    
    #SVG Editor
    path('panel/svg', svg, name='svg'),
    #kavling
    path('panel/kavling', kavling_index, name='kavling'),
    path('panel/kavling/create', kavling_create, name='kavling_create'),
    path('panel/kavling/import', kavling_import, name='kavling_import'),
    path('panel/kavling/template', kavling_template, name='kavling_template'),
    path('panel/kavling/update/<int:kavling_id>', kavling_update, name='kavling_update'),
    path('panel/kavling/delete/<int:kavling_id>', kavling_delete, name='kavling_delete'),
    path('panel/kavling/<int:kavling_id>', kavling_detail, name='kavling_detail'),
]