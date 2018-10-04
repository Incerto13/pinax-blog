from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, UpdateProfileView, user_detail, SignUpView


app_name = 'account'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name="account/login_form.html"), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^signup/$', SignUpView.as_view(), name="signup"),
    url(r'^(?P<username>[-\w]+)/$', user_detail, name='user_detail'),
    url(r'^update/(?P<slug>[-\w]+)/$', UpdateProfileView.as_view(), name='user_update'),
    url(r'^$', index, name="index"),
]

