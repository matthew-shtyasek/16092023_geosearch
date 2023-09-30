from http.client import HTTPException

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy

from auth.forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    template_name = 'registration/auth.html'
    extra_context = {'type': 'auth' }
    success_url = reverse_lazy('geo:setcoord')

    def post(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            form = CustomAuthenticationForm(data=request.POST)
            if form.is_valid():
                return self.form_valid(form) #super(CustomLoginView, self).post(request, *args, **kwargs)

        raise PermissionDenied()

    def form_valid(self, form: CustomAuthenticationForm):
        cd = form.cleaned_data
        user = authenticate(self.request, **cd)
        if user is not None:
            return JsonResponse({'address': self.success_url})
        return HttpResponse('Unauthorized', status=401)
        #return JsonResponse({'description': 'Unauthorized'}, status=401)
