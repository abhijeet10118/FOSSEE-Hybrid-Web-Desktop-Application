from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadCSVView.as_view()),
    path('history/', views.HistoryView.as_view()),
    path('datasets/<int:dataset_id>/', views.DatasetDetailView.as_view()),
    path('datasets/<int:dataset_id>/summary/', views.SummaryView.as_view()),
    path('datasets/<int:dataset_id>/pdf/', views.PDFReportView.as_view()),
]
