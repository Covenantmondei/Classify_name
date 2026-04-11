from django.urls import path
from .views import Query


urlpatterns = [path('classify', Query.as_view(), name='query'),]