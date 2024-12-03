from django.urls import path
from .views import upload,find_face,find_face_list

urlpatterns = [
    path('upload/', upload, name='upload'),
    path('face/', find_face, name='find_face'),
    path('list/', find_face_list, name='find_face_list'),
]