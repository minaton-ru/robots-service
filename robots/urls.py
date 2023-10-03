from django.urls import path
from . import views

urlpatterns = [
    path("robots/create/",
         views.RobotCreateView.as_view(), name="robot_create"),
    path("robots/week/",
         views.LastWeekExportView.as_view(), name="week_report"),
]
