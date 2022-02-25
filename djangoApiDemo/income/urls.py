from . import views
from django.urls import path

urlpatterns = [
    path('', views.IncomeListAPIView.as_view(), name='incomes'),
    path('<int:id>', views.IncomeDetailAPIView.as_view(), name='income'),
]
