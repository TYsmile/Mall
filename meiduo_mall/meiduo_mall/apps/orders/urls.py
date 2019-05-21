from django.conf.urls import url
from orders import views

urlpatterns = [
    url(r'^order/settlement/$', views.OrderSettlementView.as_view()),
    url(r'^orders/$', views.OrderCommitView.as_view()),
]