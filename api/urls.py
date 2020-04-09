from api import views
from django.urls import path


urlpatterns = [
    path('campaign/', views.CampaignList.as_view()),
    path('campaign/<int:pk>/', views.CampaignDetail.as_view()),
    path('campaignSearch/', views.CampaignSearch.as_view()),
    path('predictionCalculator/', views.PredictionCalculator.as_view()),
#     path('donation/', views.DonationList.as_view()),
#     path('donation/<int:pk>/', views.DonationDetail.as_view()),
#     path('update/', views.UpdateList.as_view()),
#     path('update/<int:pk>/', views.UpdateDetail.as_view()),
]
