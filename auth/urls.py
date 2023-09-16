from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy
from django.views.generic import CreateView

app_name = 'custom_auth'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/auth.html'), name='login'),
    path('sign-up/', CreateView.as_view(form_class=UserCreationForm,
                                        template_name='registration/auth.html',
                                        success_url=reverse_lazy('auth:login'),
                                        extra_context={'button_name': 'Регистрация'})),
]
