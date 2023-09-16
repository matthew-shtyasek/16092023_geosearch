from django.urls import path

from geosearch.views import GeoSearchView, CoordinateFormView

app_name = 'geosearch'

urlpatterns = [
    path('geosearch/', GeoSearchView.as_view(), name='geosearch'),
    path('setcoord/', CoordinateFormView.as_view(), name='setcoord'),
]