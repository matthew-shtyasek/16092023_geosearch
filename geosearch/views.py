from http.client import HTTPException

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from geosearch.forms import CoordinatesForm
from geosearch.geosearch import GeoSearch


class CoordinateFormView(LoginRequiredMixin, FormView):
    template_name = 'geosearch/index.html'
    form_class = CoordinatesForm
    success_url = reverse_lazy('geo:setcoord')
    extra_context = dict()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'is_form_valid' in self.__dict__ and self.is_form_valid:
            self.extra_context['data_saved'] = 'Данные успешно сохранены'
        elif 'data_saved' in self.extra_context:
            del self.extra_context['data_saved']
        return context

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        context.update(self.extra_context)
        return render(request, self.template_name, context)

    def form_valid(self, form):
        cd = form.cleaned_data
        self.is_form_valid = True
        GeoSearch(user_id=self.request.user.pk,
                  location=(cd['longitude'], cd['latitude']))
        return super().form_valid(form)

    def form_invalid(self, form):
        self.is_form_valid = False
        print('form is invalid')
        return super().form_invalid(form)


class GeoSearchView(View):
    template_name = 'geosearch/nearest_users.html'

    def get(self, request, *args, **kwargs):
        print(123)
        if request.user.id not in GeoSearch.items:
            raise HTTPException(428)
        nearest_users = GeoSearch.items[request.user.id][request.GET.get('radius')]
        users = User.objects.filter(pk__in=list(nearest_users.keys()))

        users = [{'id': user.id,
                  'login': user.username,
                  'latitude': nearest_users[user.id][0],
                  'longitude': nearest_users[user.id][1]}
                 for user in users
                 if request.user.id != user.id]


        context = {'users': users}
        return render(request, self.template_name, context)
