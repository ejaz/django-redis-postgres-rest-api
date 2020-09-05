from django.conf.urls import url 
from test_products import views 
 
urlpatterns = [ 
    url(r'^api/product$', views.tutorial_list),
    url(r'^api/product/(?P<pk>[0-9]+)$', views.tutorial_detail),
]