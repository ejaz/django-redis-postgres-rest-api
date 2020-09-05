from django.conf.urls import url, include 
 
urlpatterns = [ 
    url(r'^', include('test_products.urls')),
]