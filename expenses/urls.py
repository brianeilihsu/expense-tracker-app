from django.urls import path
from .views import (
    UserListView, UserDetailView,
    AccountListView, AccountDetailView,
    CategoryListView, CategoryDetailView,
    TransactionListView, TransactionDetailView,
    GenerateMonthlyReportView, GetMonthlyReportView
)

urlpatterns = [
    # User URLs
    path('users/', UserListView.as_view(), name='user-list'),
    path('user-detail/', UserDetailView.as_view(), name='user-detail'),

    # Account URLs
    path('accounts/', AccountListView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Transaction URLs
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),

    # Report URLs
    path('generate-report/', GenerateMonthlyReportView.as_view(), name='create-monthly-report'),  # 新增路由
    path('report/', GetMonthlyReportView.as_view(), name='get-monthly-report'),  

]
