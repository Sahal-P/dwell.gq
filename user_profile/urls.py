
from django.urls import reverse_lazy

from django.urls import path
from . import views
from .views import PasswordChangeView,PasswordResetDoneView
from .forms import MyPasswordChangeForm

urlpatterns = [ 
        path("", views.user_profile, name="user_profile"),
        path("edit_user_profile", views.edit_user_profile , name="edit_user_profile"),
        path("change-password/", PasswordChangeView.as_view(template_name = 'password-change.html' , success_url = reverse_lazy('change-password-done') , form_class =MyPasswordChangeForm), name='change-password'),
        path("change-password/done", PasswordResetDoneView.as_view(template_name = 'password-change-done.html'), name='change-password-done'),
        path("remove_address/<int:id>", views.remove_address , name="remove_address")
    ]
