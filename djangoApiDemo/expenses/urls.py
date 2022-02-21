from . import views
from django.urls import path

urlpatterns = [
    path('', views.ExpenseListAPIView.as_view(), name='expenses'),
    path('<int:id>', views.ExpenseDetailAPIView.as_view(), name='expense'),
]
