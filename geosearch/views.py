from http.client import HTTPException

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from geosearch.forms import CoordinatesForm
from geosearch.geosearch import GeoSearch


class CoordinateFormView(FormView):
    template_name = 'geosearch/index.html'
    form_class = CoordinatesForm
    success_url = reverse_lazy('geo:setcoord')

    def form_valid(self, form):
        cd = form.cleaned_data
        GeoSearch(user_id=self.request.user.pk,
                  location=(cd['longitude'], cd['latitude']))
        return super().form_valid(form)

    def form_invalid(self, form):
        print('form is invalid')
        return super().form_invalid(form)


class GeoSearchView(View):
    def get(self, request):
        if request.user.id not in GeoSearch.items:
            raise HTTPException(428)
        nearest_users = GeoSearch.items[request.user.id][request.GET.get('radius')]
        print(nearest_users)

        return JsonResponse({})
