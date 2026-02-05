from django.urls import path
from . import views

app_name = 'docs'

urlpatterns = [
    path('app_docs/', views.app_docs, name='app_docs'),
    path('user_guide/', views.user_guide, name='user_guide'),
    path('download/totals_support/', views.dl_totalmac, name='totals_macro_support'),
]