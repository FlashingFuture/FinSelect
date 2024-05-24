from django.urls import path, include
from . import views
urlpatterns = [
    path('fixedDeposits/', views.fixed_deposit_list ),
    path('fixedDeposits/<int:fixed_pk>/', views.fixed_deposit ),
    path('fixedDeposits/<int:fixed_pk>/like/', views.like_fixed_deposit ),
    path('SavingAccounts/', views.saving_account_list ),
    path('SavingAccounts/<int:saved_pk>/', views.saving_account ),
    path('SavingAccounts/<int:saved_pk>/like/', views.like_saving_account ),
    path('banks/', views.bank_list ),
    path('exchange/', views.exchange ),
] 