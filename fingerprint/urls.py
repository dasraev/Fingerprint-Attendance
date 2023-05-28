from .views import clock_in,clock_out,view_attendance,student_attendances
from django.urls import path

urlpatterns = [
    path('',clock_in,name='clockin'),
    path('clockout/',clock_out,name='clockout'),
    path('attendance/', view_attendance, name='attendance'),
    path('attendance/<int:pk>/',student_attendances,name='student-attendances')
]