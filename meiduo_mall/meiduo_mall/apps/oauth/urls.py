from django.conf.urls import url
from oauth import views

urlpatterns = [
    url(r'^qq/authorization/$', views.OAuthQQURLView.as_view()),
    url(r'^qq/user/$', views.OAuthQQUserView.as_view()),
]