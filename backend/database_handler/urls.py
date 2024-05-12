from django.urls import path
from . import views


urlpatterns = [
    path("addImage/", views.addImage),
    path("getImageCountForUser/", views.getImageCountForUser),
    path("getImagesForUser/", views.getImagesForUser.as_view()),
    path("getImageFromUrl/", views.getImageFromUrl),
    path("deleteImage/", views.deleteImage),
    path("setPredictedClass/", views.setPredictedClass),
]
