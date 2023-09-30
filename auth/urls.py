from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy
from django.views.generic import CreateView

from auth.views import CustomLoginView

app_name = 'custom_auth'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('sign-up/', CreateView.as_view(form_class=UserCreationForm,
                                        template_name='registration/auth.html',
                                        success_url=reverse_lazy('auth:login'),
                                        extra_context={'button_name': 'Регистрация'})),
]
